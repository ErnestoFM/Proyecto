// ==============================================================================
// Monchis Café — Endpoint POST /api/admin/notifications/check-alerts
// Evalúa en tiempo real vencimiento de lotes y stock bajo y emite alertas SMTP
// ==============================================================================

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { verifyAccessTokenAsync } from '@/lib/jwt';
import { EmailService } from '@/lib/emailService';

export async function POST(req: Request) {
  try {
    const authHeader = req.headers.get('Authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json({ error: 'No autorizado: Token ausente' }, { status: 401 });
    }

    let payload;
    try {
      payload = await verifyAccessTokenAsync(authHeader.split(' ')[1]);
    } catch (err: any) {
      if (err.name === 'TokenRevokedError') {
        return NextResponse.json({ error: 'Token revocado o sesión cerrada' }, { status: 401 });
      }
      return NextResponse.json({ error: 'No autorizado: Token inválido o expirado' }, { status: 401 });
    }

    if (!payload || payload.rol !== 'ADMIN') {
      return NextResponse.json({ error: 'Acceso restringido a administradores' }, { status: 403 });
    }

    const alertasEmitidas = [];
    const hoy = new Date();
    const fechaLimite15Dias = new Date(hoy.getTime() + 15 * 24 * 60 * 60 * 1000);

    // 1. Evaluar Lotes próximos a vencer (Req 2.2)
    try {
      const lotesPorVencer = await prisma.batch.findMany({
        where: {
          fechaCaducidad: {
            lte: fechaLimite15Dias,
          },
        },
        include: {
          producto: true,
        },
      });

      for (const lote of lotesPorVencer) {
        const msRestantes = new Date(lote.fechaCaducidad).getTime() - hoy.getTime();
        const diasRestantes = Math.max(0, Math.ceil(msRestantes / (1000 * 60 * 60 * 24)));

        const resultado = await EmailService.sendBatchExpiryAlert({
          numeroLote: lote.numeroLote,
          productoNombre: lote.producto?.nombre || 'Café de Especialidad',
          fincaOrigen: lote.fincaOrigen || undefined,
          fechaCaducidad: lote.fechaCaducidad.toISOString().split('T')[0],
          diasRestantes,
        });

        alertasEmitidas.push({
          tipo: 'CADUCIDAD_LOTE',
          numeroLote: lote.numeroLote,
          diasRestantes,
          enviado: resultado.success,
        });
      }
    } catch (dbError) {
      console.warn('⚠️ [Alertas] No se pudieron consultar lotes en BD:', dbError);
    }

    // 2. Evaluar Productos con Stock Bajo (Req 2.2)
    try {
      const productos = await prisma.product.findMany({
        where: { activo: true },
      });

      for (const prod of productos) {
        if (prod.stockActual <= prod.stockMinimo) {
          const resultado = await EmailService.sendLowStockAlert({
            productoId: prod.id,
            productoNombre: prod.nombre,
            stockActual: prod.stockActual,
            stockMinimo: prod.stockMinimo,
            tipo: prod.tipo,
          });

          alertasEmitidas.push({
            tipo: 'STOCK_MINIMO',
            producto: prod.nombre,
            stockActual: prod.stockActual,
            enviado: resultado.success,
          });
        }
      }
    } catch (dbError) {
      console.warn('⚠️ [Alertas] No se pudieron consultar productos en BD:', dbError);
    }

    return NextResponse.json({
      mensaje: 'Chequeo de alertas ejecutado con éxito',
      totalAlertas: alertasEmitidas.length,
      alertas: alertasEmitidas,
    });
  } catch (error: any) {
    console.error('❌ Error general al procesar alertas:', error);
    return NextResponse.json({ error: 'Error interno al procesar alertas' }, { status: 500 });
  }
}
