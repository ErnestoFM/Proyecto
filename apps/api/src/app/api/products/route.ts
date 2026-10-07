// ==============================================================================
// Monchis Café — Endpoint GET /api/products (Catálogo de Productos)
// Persistencia en Prisma (PostgreSQL / Google Cloud SQL) con Resilient Fallback
// ==============================================================================

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import type { ProductDTO } from '@monchis/shared-types';

// Catálogo base de contingencia (fallback offline)
const CATALOGO_PRODUCTOS_FALLBACK: ProductDTO[] = [
  {
    id: 'prod_1',
    nombre: 'Café de Olla Orgánico',
    descripcion: 'Infusión tradicional con piloncillo, canela y granos orgánicos de Chiapas.',
    tipo: 'ORGANICO',
    precio: 48.0,
    stockActual: 150,
    stockMinimo: 20,
    activo: true,
  },
  {
    id: 'prod_2',
    nombre: 'Cold Brew de la Sierra',
    descripcion: 'Extracción en frío por 18 horas con notas achocolatadas y florales.',
    tipo: 'ORGANICO',
    precio: 65.0,
    stockActual: 80,
    stockMinimo: 15,
    activo: true,
  },
  {
    id: 'prod_3',
    nombre: 'Latte Lavanda y Miel',
    descripcion: 'Espresso doble de especialidad con leche cremada, infusión de lavanda y miel pura.',
    tipo: 'ORGANICO',
    precio: 72.0,
    stockActual: 95,
    stockMinimo: 20,
    activo: true,
  },
  {
    id: 'prod_4',
    nombre: 'Panqué Artesanal de Elote',
    descripcion: 'Horneado diariamente con maíz dulce de productores regionales.',
    tipo: 'COMERCIAL',
    precio: 45.0,
    stockActual: 30,
    stockMinimo: 5,
    activo: true,
  },
  {
    id: 'prod_5',
    nombre: 'Galleta de Avena y Arándanos',
    descripcion: 'Elaborada artesanalmente sin conservadores artificiales.',
    tipo: 'COMERCIAL',
    precio: 28.0,
    stockActual: 50,
    stockMinimo: 10,
    activo: true,
  },
];

export const dynamic = 'force-dynamic';

export async function GET() {
  try {
    const productosDB = await prisma.product.findMany({
      where: { activo: true },
      orderBy: { nombre: 'asc' },
    });

    if (productosDB && productosDB.length > 0) {
      const productosFormateados: ProductDTO[] = productosDB.map((p) => ({
        id: p.id,
        nombre: p.nombre,
        descripcion: p.descripcion || undefined,
        tipo: p.tipo as 'ORGANICO' | 'COMERCIAL',
        precio: Number(p.precio),
        stockActual: p.stockActual,
        stockMinimo: p.stockMinimo,
        activo: p.activo,
      }));
      return NextResponse.json({ productos: productosFormateados });
    }
  } catch (error) {
    console.warn('⚠️ [Prisma Products] Error al consultar base de datos, usando catálogo maestro:', error);
  }

  return NextResponse.json({ productos: CATALOGO_PRODUCTOS_FALLBACK });
}
