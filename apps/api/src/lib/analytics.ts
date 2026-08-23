// ==============================================================================
// Monchis Café — Servicio de Analítica Administrativa y Atribución UTM
// ==============================================================================

import type { AttributionTrafficDTO } from '@monchis/shared-types';

export interface ProductSalesStat {
  productoId: string;
  nombre: string;
  tipo: 'ORGANICO' | 'COMERCIAL';
  unidadesVendidas: number;
  ingresosTotales: number;
}

export interface DLQMessageSummary {
  id: string;
  orderId: string;
  tipoEvento: string;
  motivoFallo: string;
  intentos: number;
  timestamp: string;
  estado: 'PENDIENTE_REVISION' | 'REINTENTADO' | 'DESCARTADO';
}

export class AnalyticsService {
  /**
   * Calcula el desglose de tráfico y conversiones por canal (Google Maps, Instagram, Directo).
   */
  static calcularMetricasTrafico(
    visitas: Array<{ source: string; convertido: boolean; monto: number }>
  ): AttributionTrafficDTO[] {
    const mapa = new Map<string, { visitas: number; ventas: number; monto: number }>();

    for (const v of visitas) {
      const src = v.source || 'direct';
      if (!mapa.has(src)) {
        mapa.set(src, { visitas: 0, ventas: 0, monto: 0 });
      }
      const data = mapa.get(src)!;
      data.visitas++;
      if (v.convertido) {
        data.ventas++;
        data.monto += v.monto;
      }
    }

    const resultado: AttributionTrafficDTO[] = [];
    mapa.forEach((val, key) => {
      resultado.push({
        source: key,
        totalVisitas: val.visitas,
        totalVentas: val.ventas,
        montoGenerado: Number(val.monto.toFixed(2)),
      });
    });

    return resultado.sort((a, b) => b.montoGenerado - a.montoGenerado);
  }

  /**
   * Identifica los productos más vendidos y menos vendidos.
   */
  static clasificarVentasProductos(itemsVendidos: Array<{ productoId: string; nombre: string; tipo: 'ORGANICO' | 'COMERCIAL'; cantidad: number; precio: number }>): {
    topVendidos: ProductSalesStat[];
    menosVendidos: ProductSalesStat[];
    totalVentasOrganico: number;
    totalVentasComercial: number;
  } {
    const mapa = new Map<string, ProductSalesStat>();

    for (const item of itemsVendidos) {
      if (!mapa.has(item.productoId)) {
        mapa.set(item.productoId, {
          productoId: item.productoId,
          nombre: item.nombre,
          tipo: item.tipo,
          unidadesVendidas: 0,
          ingresosTotales: 0,
        });
      }
      const entry = mapa.get(item.productoId)!;
      entry.unidadesVendidas += item.cantidad;
      entry.ingresosTotales += item.cantidad * item.precio;
    }

    const lista = Array.from(mapa.values());
    const ordenadosDesc = [...lista].sort((a, b) => b.unidadesVendidas - a.unidadesVendidas);
    const ordenadosAsc = [...lista].sort((a, b) => a.unidadesVendidas - b.unidadesVendidas);

    const totalVentasOrganico = lista
      .filter((i) => i.tipo === 'ORGANICO')
      .reduce((sum, i) => sum + i.ingresosTotales, 0);

    const totalVentasComercial = lista
      .filter((i) => i.tipo === 'COMERCIAL')
      .reduce((sum, i) => sum + i.ingresosTotales, 0);

    return {
      topVendidos: ordenadosDesc.slice(0, 5),
      menosVendidos: ordenadosAsc.slice(0, 5),
      totalVentasOrganico: Number(totalVentasOrganico.toFixed(2)),
      totalVentasComercial: Number(totalVentasComercial.toFixed(2)),
    };
  }
}
