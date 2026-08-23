// ==============================================================================
// Pruebas Unitarias TDD — Panel de Administración y Analítica (Fase 5)
// AnalyticsService (Atribución de Tráfico y Ventas)
// ==============================================================================

import { describe, it, expect } from 'vitest';
import { AnalyticsService } from '../src/lib/analytics';

describe('📊 Analítica y Auditoría — Monchis Café (TDD)', () => {
  // ============================================================================
  // 1. Atribución de Tráfico UTM
  // ============================================================================
  describe('🎯 1. Atribución de Canales de Tráfico (Google Maps vs Instagram vs Directo)', () => {
    it('Debe calcular visitas, ventas y monto por canal correctamente', () => {
      const visitasMuestra = [
        { source: 'google_maps', convertido: true, monto: 100 },
        { source: 'google_maps', convertido: false, monto: 0 },
        { source: 'instagram', convertido: true, monto: 200 },
        { source: 'direct', convertido: true, monto: 50 },
      ];

      const resultado = AnalyticsService.calcularMetricasTrafico(visitasMuestra);

      expect(resultado).toHaveLength(3);

      const ig = resultado.find((r) => r.source === 'instagram');
      expect(ig?.totalVisitas).toBe(1);
      expect(ig?.totalVentas).toBe(1);
      expect(ig?.montoGenerado).toBe(200);

      const gmaps = resultado.find((r) => r.source === 'google_maps');
      expect(gmaps?.totalVisitas).toBe(2);
      expect(gmaps?.totalVentas).toBe(1);
      expect(gmaps?.montoGenerado).toBe(100);
    });

    it('Debe agrupar bajo "direct" si no se proporciona fuente UTM', () => {
      const visitas = [
        { source: '', convertido: true, monto: 80 },
        { source: 'direct', convertido: false, monto: 0 },
      ];

      const res = AnalyticsService.calcularMetricasTrafico(visitas);
      const direct = res.find((r) => r.source === 'direct');

      expect(direct?.totalVisitas).toBe(2);
      expect(direct?.totalVentas).toBe(1);
      expect(direct?.montoGenerado).toBe(80);
    });
  });

  // ============================================================================
  // 2. Clasificación de Productos Más y Menos Vendidos
  // ============================================================================
  describe('☕ 2. Clasificación de Ventas y Proporción Orgánico vs Comercial', () => {
    it('Debe ordenar productos por unidades vendidas y clasificar por tipo', () => {
      const itemsVendidos = [
        { productoId: '1', nombre: 'Café de Olla', tipo: 'ORGANICO' as const, cantidad: 50, precio: 40 },
        { productoId: '2', nombre: 'Cold Brew', tipo: 'ORGANICO' as const, cantidad: 30, precio: 60 },
        { productoId: '3', nombre: 'Panqué', tipo: 'COMERCIAL' as const, cantidad: 10, precio: 30 },
      ];

      const res = AnalyticsService.clasificarVentasProductos(itemsVendidos);

      expect(res.topVendidos[0].nombre).toBe('Café de Olla');
      expect(res.topVendidos[0].unidadesVendidas).toBe(50);
      expect(res.menosVendidos[0].nombre).toBe('Panqué');

      // Total Orgánico: (50*40) + (30*60) = 2000 + 1800 = 3800
      expect(res.totalVentasOrganico).toBe(3800);
      // Total Comercial: 10 * 30 = 300
      expect(res.totalVentasComercial).toBe(300);
    });
  });
});
