// ==============================================================================
// Monchis Café — Endpoint GET /api/pos/customers (Búsqueda de Clientes para POS)
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
    } catch {
      return NextResponse.json({ error: 'Token de acceso inválido o expirado' }, { status: 401 });
    }

    if (!payload || (payload.rol !== 'ADMIN' && payload.rol !== 'CAJERO')) {
      return NextResponse.json({ error: 'Acceso denegado: Se requiere rol de CAJERO o ADMIN' }, { status: 403 });
    }

    const { searchParams } = new URL(req.url);
    const query = (searchParams.get('q') || searchParams.get('search') || '').trim();

    const clientes = await prisma.user.findMany({
      where: {
        AND: [
          query
            ? {
                OR: [
                  { email: { contains: query, mode: 'insensitive' } },
                  { nombre: { contains: query, mode: 'insensitive' } },
                ],
              }
            : {},
        ],
      },
      select: {
        id: true,
        nombre: true,
        email: true,
        rol: true,
        puntosFidelidad: true,
        sellosAcumulados: true,
      },
      take: 10,
      orderBy: { nombre: 'asc' },
    });

    return NextResponse.json({ clientes });
  } catch (error: any) {
    console.error('❌ [POS API] Error al buscar clientes:', error);
    return NextResponse.json(
      { error: 'Error interno del servidor al buscar clientes' },
      { status: 500 }
    );
  }
}

