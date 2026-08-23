// ==============================================================================
// Monchis Café — Endpoint GET /api/admin/audit/dlq (Auditoría Dead Letter Queue)
// ==============================================================================

import { NextResponse } from 'next/server';
import { verifyAccessToken } from '@/lib/jwt';
import type { DLQMessageSummary } from '@/lib/analytics';

const REGISTROS_DLQ: DLQMessageSummary[] = [
  {
    id: 'dlq_msg_001',
    orderId: 'ord_fallida_ejemplo',
    tipoEvento: 'STOCK_DEDUCTION_FAILED',
    motivoFallo: 'Stock insuficiente en Lote MC-CHP-2026-A1 tras 4 reintentos automáticos (10s, 60s, 300s)',
    intentos: 4,
    timestamp: '2026-08-23T12:00:00Z',
    estado: 'PENDIENTE_REVISION',
  },
];

export async function GET(req: Request) {
  try {
    const authHeader = req.headers.get('Authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json({ error: 'No autorizado' }, { status: 401 });
    }

    const payload = verifyAccessToken(authHeader.split(' ')[1]);
    if (!payload || payload.rol !== 'ADMIN') {
      return NextResponse.json({ error: 'Acceso restringido a administradores' }, { status: 403 });
    }

    return NextResponse.json({
      totalMensajesDLQ: REGISTROS_DLQ.length,
      mensajes: REGISTROS_DLQ,
    });
  } catch (error: any) {
    return NextResponse.json({ error: 'Error al consultar DLQ' }, { status: 500 });
  }
}
