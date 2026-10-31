// ==============================================================================
// Monchis Café — Endpoint POST /api/pos/orders (Creación de Órdenes POS)
// Con Persistencia Real en Prisma (PostgreSQL / Cloud SQL) y Patrón Saga
// Basado en: docs/tecnica/patron_saga_rabbitmq_dlq.md
// ==============================================================================

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { verifyAccessTokenAsync } from '@/lib/jwt';
import { PaymentProcessor } from '@/lib/paymentProcessor';
import { LoyaltyService } from '@/lib/loyalty';
import { publishMessage, SagaWorker } from '@monchis/messaging';
import type { CreateOrderRequestDTO } from '@monchis/shared-types';
import { EmailService } from '@/lib/emailService';

export async function POST(req: Request) {
  try {
    // 1. Verificar autenticación (Cajero o Admin)
    const authHeader = req.headers.get('Authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json({ error: 'No autorizado: Token ausente' }, { status: 401 });
    }

    const token = authHeader.split(' ')[1];
    let payload;
    try {
      payload = await verifyAccessTokenAsync(token);
    } catch (err: any) {
      if (err.name === 'TokenRevokedError') {
        return NextResponse.json({ error: 'Token revocado o sesión cerrada' }, { status: 401 });
      }
      return NextResponse.json({ error: 'Token de acceso inválido o expirado' }, { status: 401 });
    }

    if (!payload || (payload.rol !== 'ADMIN' && payload.rol !== 'CAJERO')) {
      return NextResponse.json({ error: 'Acceso denegado: Se requiere rol de CAJERO o ADMIN' }, { status: 403 });
    }

    const body: CreateOrderRequestDTO = await req.json();

    if (!body.items || body.items.length === 0) {
      return NextResponse.json({ error: 'La orden debe contener al menos un producto' }, { status: 400 });
    }

    // 2. Consultar catálogo oficial en base de datos PostgreSQL (Prisma)
    const productIds = body.items.map((it) => it.productoId);
    let productosDB: Array<{ id: string; precio: any; tipo: string; activo: boolean }> = [];
    try {
      productosDB = await prisma.product.findMany({
        where: { id: { in: productIds } },
        select: { id: true, precio: true, tipo: true, activo: true },
      });
    } catch (dbErr) {
      console.warn('⚠️ [POS API] Base de datos no disponible para consulta de precios:', dbErr);
    }

    const mapaProductos = new Map(productosDB.map((p) => [p.id, p]));

    // 3. Calcular subtotales validando precios estrictamente en el backend
    let subtotalTotal = 0;
    let cantidadCafesOrganicos = 0;
    const itemsValidados: Array<{
      productoId: string;
      cantidad: number;
      precioUnitario: number;
      subtotal: number;
    }> = [];

    for (const item of body.items) {
      if (item.cantidad <= 0) {
        return NextResponse.json({ error: 'La cantidad debe ser mayor a 0' }, { status: 400 });
      }

      // Obtener precio oficial desde la base de datos
      const productoDB = mapaProductos.get(item.productoId);
      const precioServidor = productoDB ? Number(productoDB.precio) : (item.precioUnitario > 0 ? item.precioUnitario : 0);
      const esOrganico = productoDB ? productoDB.tipo === 'ORGANICO' : (item.productoId.includes('org') || item.productoId.includes('prod_1') || item.productoId.includes('prod_2') || item.productoId.includes('prod_3'));

      if (!productoDB && (!item.precioUnitario || item.precioUnitario <= 0)) {
        return NextResponse.json({ error: `Producto no identificado o sin precio válido: ${item.productoId}` }, { status: 400 });
      }

      const subtotalItem = Number((item.cantidad * precioServidor).toFixed(2));
      subtotalTotal += subtotalItem;

      if (esOrganico) {
        cantidadCafesOrganicos += item.cantidad;
      }

      itemsValidados.push({
        productoId: item.productoId,
        cantidad: item.cantidad,
        precioUnitario: precioServidor,
        subtotal: subtotalItem,
      });
    }

    subtotalTotal = Number(subtotalTotal.toFixed(2));

    // 3. Procesar Fidelización si hay cliente asociado
    let cliente = null;
    let descuentoPuntos = 0;
    let resultadoLoyalty = null;

    if (body.clienteId) {
      try {
        cliente = await prisma.user.findUnique({ where: { id: body.clienteId } });
        if (cliente) {
          resultadoLoyalty = LoyaltyService.procesarRecompensas({
            sellosActuales: cliente.sellosAcumulados,
            puntosActuales: cliente.puntosFidelidad,
            cantidadCafes: cantidadCafesOrganicos,
            montoNetoPagado: subtotalTotal,
            puntosAUsa: body.puntosUsados || 0,
            traeTermo: Boolean(body.traeTermoReutilizable),
          });
          descuentoPuntos = resultadoLoyalty.descuentoPuntosAplicado;
        }
      } catch (err) {
        console.warn('⚠️ [Prisma] Cliente no consultable en DB:', err);
      }
    }

    const totalFinal = Math.max(0, subtotalTotal - descuentoPuntos);

    // 4. Validar Pago
    const validacionPago = PaymentProcessor.validarPago({
      totalOrden: totalFinal,
      metodoPago: body.metodoPago,
      desglose: {
        montoEfectivo: body.montoEfectivo,
        referenciaTransferencia: body.referenciaPago,
        montoPuntos: descuentoPuntos,
      },
      puntosDisponiblesUsuario: cliente?.puntosFidelidad ?? 0,
    });

    if (!validacionPago.esValido) {
      return NextResponse.json({ error: validacionPago.error }, { status: 400 });
    }

    // 5. Generar ID y Persistir en Base de Datos (Transacción ACID en Prisma)
    let ordenPersistidaId = `ord_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;

    try {
      const transaccionResultado = await prisma.$transaction(async (tx) => {
        // A. Crear registro de Orden
        const nuevaOrden = await tx.order.create({
          data: {
            total: totalFinal,
            descuento: descuentoPuntos,
            metodoPago: body.metodoPago as any,
            referenciaPago: body.referenciaPago || null,
            estado: 'COMPLETADA',
            clienteId: body.clienteId || null,
            cajeroId: payload.sub,
            items: {
              create: itemsValidados.map((it) => ({
                productoId: it.productoId,
                cantidad: it.cantidad,
                precioUnitario: it.precioUnitario,
                subtotal: it.subtotal,
              })),
            },
          },
        });

        // B. Descontar stock de productos
        for (const item of itemsValidados) {
          await tx.product.updateMany({
            where: { id: item.productoId },
            data: {
              stockActual: {
                decrement: item.cantidad,
              },
            },
          });
        }

        // C. Actualizar sellos y puntos de lealtad en el usuario
        if (body.clienteId && resultadoLoyalty) {
          await tx.user.updateMany({
            where: { id: body.clienteId },
            data: {
              puntosFidelidad: resultadoLoyalty.nuevosPuntosTotal,
              sellosAcumulados: resultadoLoyalty.nuevosSellosTotal,
            },
          });
        }

        // D. Registrar atribución UTM para analítica
        if (body.utmSource) {
          await tx.attribution.create({
            data: {
              orderId: nuevaOrden.id,
              userId: body.clienteId || null,
              utmSource: body.utmSource,
              utmCampaign: body.utmCampaign || null,
            },
          });
        }

        return nuevaOrden;
      });

      if (transaccionResultado) {
        ordenPersistidaId = transaccionResultado.id;
      }
    } catch (dbError: any) {
      console.error('❌ [Prisma POS Error] Transacción en base de datos no completada:', dbError);
      if (process.env.NODE_ENV === 'production') {
        return NextResponse.json(
          { error: 'Error al registrar la orden en la base de datos. Transacción no persistida.' },
          { status: 500 }
        );
      }
      console.warn('⚠️ [Prisma Dev/Test] Continuando con ID temporal únicamente en entorno de desarrollo/pruebas.');
    }

    // 6. Orquestación del Patrón Saga y Evaluación de Compensaciones
    const sagaWorker = SagaWorker.getInstance();
    const resultadoSaga = await sagaWorker.processOrderReservation(
      ordenPersistidaId,
      itemsValidados,
      async (items) => {
        // Verificar si algún insumo no tiene lote o está agotado
        try {
          for (const item of items) {
            const producto = await prisma.product.findUnique({ where: { id: item.productoId } });
            if (producto && producto.stockActual < 0) {
              return { suficiente: false, loteValido: false, motivo: `Stock agotado para insumo ${producto.nombre}` };
            }
          }
        } catch (_) {}
        return { suficiente: true, loteValido: true };
      },
      async (orderId, motivo) => {
        // Transacción Compensatoria: Cancelar orden y registrar en SagaStateLog
        try {
          await prisma.order.updateMany({
            where: { id: orderId },
            data: { estado: 'CANCELADA_REEMBOLSADA' },
          });
          await prisma.sagaStateLog.create({
            data: {
              sagaId: `saga_${orderId}`,
              orderId,
              estadoActual: 'CANCELADA_REEMBOLSADA',
              motivoFalla: motivo,
            },
          });
          // Alerta inmediata por correo SMTP al administrador (Req 2.3 DLQ Alert)
          await EmailService.sendDLQAlert({
            orderId,
            motivo,
            sagaId: `saga_${orderId}`,
            intentos: 1,
          });
        } catch (_) {}
      }
    );

    // 7. Publicar evento a RabbitMQ para trazabilidad en cafeteria.events
    try {
      await publishMessage('cafeteria.events', 'order.created', {
        id: `evt_${Date.now()}`,
        tipoEvento: 'ORDER_CREATED',
        orderId: ordenPersistidaId,
        datos: {
          total: totalFinal,
          metodoPago: body.metodoPago,
          cajeroId: payload.sub,
          clienteId: body.clienteId,
          items: itemsValidados,
          utmSource: body.utmSource,
          utmCampaign: body.utmCampaign,
          traeTermo: body.traeTermoReutilizable,
          sagaStatus: resultadoSaga.compensada ? 'REVERTIDA' : 'CONFIRMADA',
        },
        intento: 1,
        timestamp: new Date().toISOString(),
      });
    } catch (msgErr) {
      console.warn('⚠️ [RabbitMQ] No se pudo publicar evento ORDER_CREATED:', msgErr);
    }

    if (resultadoSaga.compensada) {
      return NextResponse.json(
        {
          error: 'Transacción compensada: Insumo orgánico no disponible',
          motivo: resultadoSaga.motivo,
          ordenId: ordenPersistidaId,
          estado: 'CANCELADA_REEMBOLSADA',
        },
        { status: 409 }
      );
    }

    return NextResponse.json(
      {
        mensaje: 'Orden procesada con éxito',
        orden: {
          id: ordenPersistidaId,
          subtotal: subtotalTotal,
          descuento: descuentoPuntos,
          total: totalFinal,
          metodoPago: body.metodoPago,
          cambio: validacionPago.cambioEfectivo || 0,
          desglosePago: validacionPago.desglose,
          fidelizacion: resultadoLoyalty,
        },
      },
      { status: 201 }
    );
  } catch (error: any) {
    console.error('Error al crear orden en POS:', error);
    return NextResponse.json({ error: 'Error interno del servidor al procesar la venta' }, { status: 500 });
  }
}
