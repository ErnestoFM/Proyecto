// ==============================================================================
// Monchis Café — Endpoint GET /api/orders/my-orders (Historial de Compras del Cliente)
// ==============================================================================

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { verifyAccessTokenAsync } from '@/lib/jwt';

export const dynamic = 'force-dynamic';

export async function GET(req: Request) {
  try {
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

    if (!payload || !payload.sub) {
      return NextResponse.json({ error: 'Token inválido' }, { status: 401 });
    }

    // Consultar órdenes vinculadas al usuario autenticado
    const orders = await prisma.order.findMany({
      where: { clienteId: payload.sub },
      orderBy: { createdAt: 'desc' },
      include: {
        items: {
          include: {
            producto: {
              select: {
                id: true,
                nombre: true,
                tipo: true,
                precio: true,
              },
            },
          },
        },
        cajero: {
          select: {
            nombre: true,
          },
        },
      },
    });

    const ordenesDTO = orders.map((o) => ({
      id: o.id,
      folio: `FOL-${o.id.substring(0, 8).toUpperCase()}`,
      fecha: o.createdAt.toISOString(),
      total: Number(o.total),
      descuento: Number(o.descuento),
      metodoPago: o.metodoPago,
      referenciaPago: o.referenciaPago,
      estado: o.estado,
      cajero: o.cajero?.nombre || 'Barra Principal',
      items: o.items.map((it) => ({
        id: it.id,
        productoNombre: it.producto.nombre,
        tipo: it.producto.tipo,
        cantidad: it.cantidad,
        precioUnitario: Number(it.precioUnitario),
        subtotal: Number(it.subtotal),
      })),
    }));

    return NextResponse.json({ ordenes: ordenesDTO });
  } catch (error: any) {
    console.error('❌ [Orders API] Error al obtener historial de compras:', error);
    return NextResponse.json(
      { error: 'Error interno del servidor al consultar historial de compras' },
      { status: 500 }
    );
  }
}

