// ==============================================================================
// Monchis Café — Endpoint GET / POST /api/inventory/batches (Lotes de Café)
// ==============================================================================

import { NextResponse } from 'next/server';
import { verifyAccessToken } from '@/lib/jwt';
import type { BatchDTO } from '@monchis/shared-types';

const LOTES_MEMORIA: BatchDTO[] = [
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

export async function GET() {
  return NextResponse.json({ lotes: LOTES_MEMORIA });
}

export async function POST(req: Request) {
  try {
    const authHeader = req.headers.get('Authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json({ error: 'No autorizado' }, { status: 401 });
    }

    const payload = verifyAccessToken(authHeader.split(' ')[1]);
    if (!payload || payload.rol !== 'ADMIN') {
      return NextResponse.json({ error: 'Solo administradores pueden registrar nuevos lotes' }, { status: 403 });
    }

    const body: Partial<BatchDTO> = await req.json();

    if (!body.numeroLote || !body.proveedorRegional || !body.productoId || !body.cantidadKilos) {
      return NextResponse.json({ error: 'Faltan campos obligatorios para el registro de lote' }, { status: 400 });
    }

    const nuevoLote: BatchDTO = {
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

    LOTES_MEMORIA.push(nuevoLote);

    return NextResponse.json({ mensaje: 'Lote registrado con éxito', lote: nuevoLote }, { status: 201 });
  } catch (error: any) {
    return NextResponse.json({ error: 'Error al registrar lote' }, { status: 500 });
  }
}
