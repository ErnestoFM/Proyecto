// ==============================================================================
// Monchis Café — Admin Store (Pinia) — Analítica y Auditoría
// ==============================================================================

import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { AttributionTrafficDTO, BatchDTO } from '@monchis/shared-types';
import { useAuthStore } from './authStore';

export interface AdminResumen {
  totalIngresos: number;
  totalOrdenes: number;
  totalVentasOrganico: number;
  totalVentasComercial: number;
  porcentajeOrganico: number;
}

export interface AdminProductSales {
  productoId: string;
  nombre: string;
  tipo: 'ORGANICO' | 'COMERCIAL';
  unidadesVendidas: number;
  ingresosTotales: number;
}

export const useAdminStore = defineStore('admin', () => {
  const auth = useAuthStore();

  const resumen = ref<AdminResumen | null>({
    totalIngresos: 12450.0,
    totalOrdenes: 246,
    totalVentasOrganico: 9800.0,
    totalVentasComercial: 2650.0,
    porcentajeOrganico: 78.7,
  });

  const atribucionTrafico = ref<AttributionTrafficDTO[]>([
    { source: 'google_maps', totalVisitas: 145, totalVentas: 82, montoGenerado: 5400.0 },
    { source: 'instagram', totalVisitas: 110, totalVentas: 56, montoGenerado: 4120.0 },
    { source: 'direct', totalVisitas: 75, totalVentas: 40, montoGenerado: 2930.0 },
  ]);

  const topVendidos = ref<AdminProductSales[]>([
    { productoId: 'prod_1', nombre: 'Café de Olla Orgánico', tipo: 'ORGANICO', unidadesVendidas: 98, ingresosTotales: 4704.0 },
    { productoId: 'prod_2', nombre: 'Cold Brew de la Sierra', tipo: 'ORGANICO', unidadesVendidas: 74, ingresosTotales: 4810.0 },
    { productoId: 'prod_3', nombre: 'Latte Lavanda y Miel', tipo: 'ORGANICO', unidadesVendidas: 52, ingresosTotales: 3744.0 },
  ]);

  const lotesActivos = ref<BatchDTO[]>([
    {
      id: 'lote_1',
      productoId: 'prod_1',
      numeroLote: 'MC-CHP-2026-A1',
      proveedorRegional: 'Cooperativa Café de Altura Chiapas',
      fincaOrigen: 'Finca Santa Rosa, Tapachula',
      fechaCosechaTostado: '2026-07-15T08:00:00Z',
      fechaCaducidad: '2027-01-15T08:00:00Z',
      cantidadKilos: 42.5,
    },
    {
      id: 'lote_2',
      productoId: 'prod_2',
      numeroLote: 'MC-OAX-2026-B3',
      proveedorRegional: 'Unión Campesina Pluma Hidalgo',
      fincaOrigen: 'Rancho Las Nubes, Oaxaca',
      fechaCosechaTostado: '2026-08-01T10:00:00Z',
      fechaCaducidad: '2027-02-01T10:00:00Z',
      cantidadKilos: 28.0,
    },
  ]);

  const mensajesDLQ = ref<any[]>([]);
  const isLoading = ref<boolean>(false);
  const error = ref<string | null>(null);

  async function cargarMetricas() {
    isLoading.value = true;
    error.value = null;

    try {
      const res = await fetch('/api/admin/analytics', {
        headers: {
          'Content-Type': 'application/json',
          ...auth.getAuthHeaders(),
        },
        credentials: 'include',
      });

      if (!res.ok) {
        throw new Error('Error al cargar analítica');
      }

      const data = await res.json();
      resumen.value = data.resumen;
      atribucionTrafico.value = data.atribucionTrafico;
      topVendidos.value = data.productos?.topVendidos || [];
    } catch (e: any) {
      error.value = e.message;
    } finally {
      isLoading.value = false;
    }
  }

  async function cargarDLQ() {
    try {
      const res = await fetch('/api/admin/audit/dlq', {
        headers: { ...auth.getAuthHeaders() },
        credentials: 'include',
      });
      if (res.ok) {
        const data = await res.json();
        mensajesDLQ.value = data.mensajes || [];
      }
    } catch (e) {
      console.warn('Error al consultar DLQ:', e);
    }
  }

  return {
    resumen,
    atribucionTrafico,
    topVendidos,
    lotesActivos,
    mensajesDLQ,
    isLoading,
    error,
    cargarMetricas,
    cargarDLQ,
  };
});
