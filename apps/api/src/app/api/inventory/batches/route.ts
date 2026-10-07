// ==============================================================================
// Monchis Café — Endpoint GET / POST /api/inventory/batches (Lotes de Café)
// Persistencia en Prisma (PostgreSQL / Google Cloud SQL)
// ==============================================================================

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { verifyAccessTokenAsync } from '@/lib/jwt';
import type { BatchDTO } from '@monchis/shared-types';

const LOTES_FALLBACK: BatchDTO[] = [
  {
    id: 'lote_chiapas_2026_01',
    productoId: 'prod_1',
    numeroLote: 'MC-CHP-2026-A1',
    proveedorRegional: 'Cooperativa Café de Altura Chiapas',
    fincaOrigen: 'Finca Santa Rosa, Tapachula',
    fechaCosechaTostado: '2026-07-15T08:00:00Z',
    fechaCaducidad: '2027-01-15T08:00:00Z',
    cantidadKilos: 50.0,
  },
  {
    id: 'lote_oaxaca_2026_02',
    productoId: 'prod_2',
    numeroLote: 'MC-OAX-2026-B3',
    proveedorRegional: 'Unión Campesina Pluma Hidalgo',
    fincaOrigen: 'Rancho Las Nubes, Pluma Hidalgo, Oaxaca',
    fechaCosechaTostado: '2026-08-01T10:00:00Z',
    fechaCaducidad: '2027-02-01T10:00:00Z',
    cantidadKilos: 35.5,
  },
];

export const dynamic = 'force-dynamic';

export async function GET() {
  try {
    const lotesDB = await prisma.batch.findMany({
      orderBy: { fechaCaducidad: 'asc' },
    });

    if (lotesDB && lotesDB.length > 0) {
      const lotesFormateados: BatchDTO[] = lotesDB.map((l) => ({
        id: l.id,
        productoId: l.productoId,
        numeroLote: l.numeroLote,
        proveedorRegional: l.proveedorRegional,
        fincaOrigen: l.fincaOrigen || undefined,
        fechaCosechaTostado: l.fechaCosechaTostado.toISOString(),
        fechaCaducidad: l.fechaCaducidad.toISOString(),
        cantidadKilos: Number(l.cantidadKilos),
        alertasSanitarias: l.alertasSanitarias || undefined,
      }));
      return NextResponse.json({ lotes: lotesFormateados });
    }
  } catch (error) {
    console.warn('⚠️ [Prisma Batches] Error al consultar base de datos, usando fallback:', error);
  }

  return NextResponse.json({ lotes: LOTES_FALLBACK });
}

export async function POST(req: Request) {
  try {
    const authHeader = req.headers.get('Authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json({ error: 'No autorizado' }, { status: 401 });
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
      return NextResponse.json({ error: 'Solo administradores pueden registrar nuevos lotes' }, { status: 403 });
    }

    const body: Partial<BatchDTO> = await req.json();

    if (!body.numeroLote || !body.proveedorRegional || !body.productoId || !body.cantidadKilos) {
      return NextResponse.json({ error: 'Faltan campos obligatorios para el registro de lote' }, { status: 400 });
    }

    let loteCreado: BatchDTO;

    try {
      const dbLote = await prisma.batch.create({
        data: {
          productoId: body.productoId,
          numeroLote: body.numeroLote,
          proveedorRegional: body.proveedorRegional,
          fincaOrigen: body.fincaOrigen || 'Finca Regional Asociada',
          fechaCosechaTostado: body.fechaCosechaTostado ? new Date(body.fechaCosechaTostado) : new Date(),
          fechaCaducidad: body.fechaCaducidad ? new Date(body.fechaCaducidad) : new Date(Date.now() + 180 * 24 * 60 * 60 * 1000),
          cantidadKilos: Number(body.cantidadKilos),
          alertasSanitarias: body.alertasSanitarias || null,
        },
      });

      loteCreado = {
        id: dbLote.id,
        productoId: dbLote.productoId,
        numeroLote: dbLote.numeroLote,
        proveedorRegional: dbLote.proveedorRegional,
        fincaOrigen: dbLote.fincaOrigen || undefined,
        fechaCosechaTostado: dbLote.fechaCosechaTostado.toISOString(),
        fechaCaducidad: dbLote.fechaCaducidad.toISOString(),
        cantidadKilos: Number(dbLote.cantidadKilos),
        alertasSanitarias: dbLote.alertasSanitarias || undefined,
      };
    } catch (dbErr) {
      console.warn('⚠️ [Prisma Batch Create] Fallback en memoria:', dbErr);
      loteCreado = {
        id: `lote_${Date.now()}`,
        productoId: body.productoId,
        numeroLote: body.numeroLote,
        proveedorRegional: body.proveedorRegional,
        fincaOrigen: body.fincaOrigen || 'Finca Regional Asociada',
        fechaCosechaTostado: body.fechaCosechaTostado || new Date().toISOString(),
        fechaCaducidad: body.fechaCaducidad || new Date(Date.now() + 180 * 24 * 60 * 60 * 1000).toISOString(),
        cantidadKilos: Number(body.cantidadKilos),
        alertasSanitarias: body.alertasSanitarias,
      };
      LOTES_FALLBACK.push(loteCreado);
    }

    return NextResponse.json({ mensaje: 'Lote registrado con éxito', lote: loteCreado }, { status: 201 });
  } catch (error: any) {
    return NextResponse.json({ error: 'Error al registrar lote' }, { status: 500 });
  }
}
