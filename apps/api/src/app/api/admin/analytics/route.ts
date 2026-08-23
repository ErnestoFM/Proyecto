// ==============================================================================
// Monchis Café — Endpoint GET /api/admin/analytics
// ==============================================================================

import { NextResponse } from 'next/server';
import { verifyAccessToken } from '@/lib/jwt';
import { AnalyticsService } from '@/lib/analytics';

// Muestras de datos representativas para la analítica del panel
const VISITAS_TRAFICO = [
  { source: 'google_maps', convertido: true, monto: 145.0 },
  { source: 'google_maps', convertido: true, monto: 96.0 },
  { source: 'google_maps', convertido: false, monto: 0 },
  { source: 'instagram', convertido: true, monto: 210.0 },
  { source: 'instagram', convertido: false, monto: 0 },
  { source: 'instagram', convertido: true, monto: 135.0 },
  { source: 'direct', convertido: true, monto: 48.0 },
  { source: 'direct', convertido: false, monto: 0 },
];

const ITEMS_VENDIDOS: Array<{ productoId: string; nombre: string; tipo: 'ORGANICO' | 'COMERCIAL'; cantidad: number; precio: number }> = [
  { productoId: 'prod_1', nombre: 'Café de Olla Orgánico', tipo: 'ORGANICO', cantidad: 85, precio: 48.0 },
  { productoId: 'prod_2', nombre: 'Cold Brew de la Sierra', tipo: 'ORGANICO', cantidad: 62, precio: 65.0 },
  { productoId: 'prod_3', nombre: 'Latte Lavanda y Miel', tipo: 'ORGANICO', cantidad: 45, precio: 72.0 },
  { productoId: 'prod_4', nombre: 'Panqué Artesanal de Elote', tipo: 'COMERCIAL', cantidad: 38, precio: 45.0 },
  { productoId: 'prod_5', nombre: 'Galleta de Avena y Arándanos', tipo: 'COMERCIAL', cantidad: 18, precio: 28.0 },
];

export async function GET(req: Request) {
  try {
    const authHeader = req.headers.get('Authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json({ error: 'No autorizado: Token ausente' }, { status: 401 });
    }

    const payload = verifyAccessToken(authHeader.split(' ')[1]);
    if (!payload || payload.rol !== 'ADMIN') {
      return NextResponse.json({ error: 'Acceso restringido a administradores' }, { status: 403 });
    }

    const trafico = AnalyticsService.calcularMetricasTrafico(VISITAS_TRAFICO);
    const productos = AnalyticsService.clasificarVentasProductos(ITEMS_VENDIDOS);

    const totalIngresos = Number((productos.totalVentasOrganico + productos.totalVentasComercial).toFixed(2));
    const totalOrdenes = ITEMS_VENDIDOS.reduce((sum, i) => sum + i.cantidad, 0);

    return NextResponse.json({
      resumen: {
        totalIngresos,
        totalOrdenes,
        totalVentasOrganico: productos.totalVentasOrganico,
        totalVentasComercial: productos.totalVentasComercial,
        porcentajeOrganico: Number(((productos.totalVentasOrganico / totalIngresos) * 100).toFixed(1)),
      },
      atribucionTrafico: trafico,
      productos: {
        topVendidos: productos.topVendidos,
        menosVendidos: productos.menosVendidos,
      },
    });
  } catch (error: any) {
    return NextResponse.json({ error: 'Error al obtener analítica' }, { status: 500 });
  }
}
