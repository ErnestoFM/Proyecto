// ==============================================================================
// Admin Store — Pruebas Unitarias TDD (Vitest + Pinia)
// ==============================================================================

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useAdminStore } from '@/stores/adminStore';
import { useAuthStore } from '@/stores/authStore';

const mockFetch = vi.fn();
vi.stubGlobal('fetch', mockFetch);

describe('useAdminStore (Analítica, Atribución UTM y DLQ)', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    mockFetch.mockReset();
  });

  describe('1. Estado Inicial', () => {
    it('Debe inicializar con métricas predeterminadas y lotes activos', () => {
      const admin = useAdminStore();
      expect(admin.resumen?.totalIngresos).toBeGreaterThan(0);
      expect(admin.atribucionTrafico).toHaveLength(3);
      expect(admin.lotesActivos).toHaveLength(2);
      expect(admin.isLoading).toBe(false);
    });
  });

  describe('2. Carga de Métricas y Atribución', () => {
    it('Debe actualizar el estado con los datos devueltos por el API', async () => {
      const admin = useAdminStore();
      const auth = useAuthStore();
      auth.accessToken = 'mock-admin-token';

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve({
            resumen: {
              totalIngresos: 25000.0,
              totalOrdenes: 500,
              totalVentasOrganico: 20000.0,
              totalVentasComercial: 5000.0,
              porcentajeOrganico: 80.0,
            },
            atribucionTrafico: [
              { source: 'google_maps', totalVisitas: 300, totalVentas: 150, montoGenerado: 12000.0 },
            ],
            productos: {
              topVendidos: [{ productoId: '1', nombre: 'Café de Olla', unidadesVendidas: 120, ingresosTotales: 5760 }],
            },
          }),
      });

      await admin.cargarMetricas();

      expect(admin.resumen?.totalIngresos).toBe(25000.0);
      expect(admin.atribucionTrafico[0].source).toBe('google_maps');
      expect(admin.topVendidos[0].nombre).toBe('Café de Olla');
    });

    it('Debe capturar errores si la petición falla', async () => {
      const admin = useAdminStore();
      mockFetch.mockResolvedValueOnce({ ok: false, status: 500 });

      await admin.cargarMetricas();

      expect(admin.error).toBe('Error al cargar analítica');
    });
  });

  describe('3. Consulta de DLQ (Dead Letter Queue)', () => {
    it('Debe cargar mensajes fallidos desde la API de auditoría', async () => {
      const admin = useAdminStore();
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve({
            mensajes: [{ id: 'dlq_1', tipoEvento: 'ORDER_FAILED', intentos: 4 }],
          }),
      });

      await admin.cargarDLQ();

      expect(admin.mensajesDLQ).toHaveLength(1);
      expect(admin.mensajesDLQ[0].tipoEvento).toBe('ORDER_FAILED');
    });
  });
});
