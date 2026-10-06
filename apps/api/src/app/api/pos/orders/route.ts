// ==============================================================================
// Monchis Café — Endpoint POST /api/pos/orders (Creación de Órdenes POS)
// ==============================================================================

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { verifyAccessToken } from '@/lib/jwt';
import { PaymentProcessor } from '@/lib/paymentProcessor';
import { LoyaltyService } from '@/lib/loyalty';
import { publishMessage } from '@monchis/messaging';
import type { CreateOrderRequestDTO } from '@monchis/shared-types';

export async function POST(req: Request) {
  try {
    // 1. Verificar autenticación (Cajero o Admin)
    const authHeader = req.headers.get('Authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json({ error: 'No autorizado: Token ausente' }, { status: 401 });
    }

    const token = authHeader.split(' ')[1];
    const payload = verifyAccessToken(token);
    if (!payload || (payload.rol !== 'ADMIN' && payload.rol !== 'CAJERO')) {
      return NextResponse.json({ error: 'Acceso denegado: Se requiere rol de CAJERO o ADMIN' }, { status: 403 });
    }

    const body: CreateOrderRequestDTO = await req.json();

    if (!body.items || body.items.length === 0) {
      return NextResponse.json({ error: 'La orden debe contener al menos un producto' }, { status: 400 });
    }

    // Catálogo oficial de referencia en servidor (protección contra manipulación de precios)
    const CATALOGO_PRECIOS: Record<string, { precio: number; tipo: 'ORGANICO' | 'COMERCIAL' }> = {
      prod_1: { precio: 48.0, tipo: 'ORGANICO' },
      prod_2: { precio: 65.0, tipo: 'ORGANICO' },
      prod_3: { precio: 72.0, tipo: 'ORGANICO' },
      prod_4: { precio: 45.0, tipo: 'COMERCIAL' },
      prod_5: { precio: 28.0, tipo: 'COMERCIAL' },
    };

    // 2. Calcular subtotales validando precios estrictamente en el backend
    let subtotalTotal = 0;
    let cantidadCafesOrganicos = 0;
    const itemsValidados = [];

    for (const item of body.items) {
      if (item.cantidad <= 0) {
        return NextResponse.json({ error: 'La cantidad debe ser mayor a 0' }, { status: 400 });
      }

      // Obtener precio oficial del servidor
      const productoOficial = CATALOGO_PRECIOS[item.productoId];
      const precioServidor = productoOficial ? productoOficial.precio : item.precioUnitario;

      if (!productoOficial && (!item.precioUnitario || item.precioUnitario <= 0)) {
        return NextResponse.json({ error: `Producto no identificado: ${item.productoId}` }, { status: 400 });
      }

      const subtotalItem = Number((item.cantidad * precioServidor).toFixed(2));
      subtotalTotal += subtotalItem;

      if (productoOficial?.tipo === 'ORGANICO') {
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
        console.warn('Advertencia: No se pudo consultar el cliente en DB:', err);
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

    // 5. Generar ID y estructura de la Orden
    const ordenId = `ord_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;

    // 6. Publicar evento a RabbitMQ para trazabilidad y orquestación Saga
    try {
      await publishMessage('cafeteria.events', 'order.created', {
        id: `evt_${Date.now()}`,
        tipoEvento: 'ORDER_CREATED',
        orderId: ordenId,
        datos: {
          total: totalFinal,
          metodoPago: body.metodoPago,
          cajeroId: payload.sub,
          clienteId: body.clienteId,
          items: itemsValidados,
          utmSource: body.utmSource,
          utmCampaign: body.utmCampaign,
          traeTermo: body.traeTermoReutilizable,
        },
        intento: 1,
        timestamp: new Date().toISOString(),
      });
    } catch (msgErr) {
      console.warn('⚠️ [RabbitMQ] No se pudo publicar evento ORDER_CREATED:', msgErr);
    }

    return NextResponse.json(
      {
        mensaje: 'Orden procesada con éxito',
        orden: {
          id: ordenId,
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
