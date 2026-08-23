// ==============================================================================
// POS Store — Pruebas Unitarias TDD (Vitest + Pinia)
// ==============================================================================

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { usePosStore } from '@/stores/posStore';
import { useAuthStore } from '@/stores/authStore';

// Mock global fetch
const mockFetch = vi.fn();
vi.stubGlobal('fetch', mockFetch);

describe('usePosStore (Carrito, Pagos y Rewards)', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    mockFetch.mockReset();
  });

  describe('1. Operaciones del Carrito', () => {
    it('Debe iniciar con el carrito vacío', () => {
      const pos = usePosStore();
      expect(pos.cart).toHaveLength(0);
      expect(pos.subtotal).toBe(0);
      expect(pos.total).toBe(0);
    });

    it('Debe agregar productos y calcular el subtotal correctamente', () => {
      const pos = usePosStore();
      const prodCafe = pos.productos[0]; // Café de Olla $48

      pos.agregarProducto(prodCafe);
      expect(pos.cart).toHaveLength(1);
      expect(pos.cart[0].cantidad).toBe(1);
      expect(pos.subtotal).toBe(48);

      // Agregar el mismo producto incrementa cantidad
      pos.agregarProducto(prodCafe);
      expect(pos.cart[0].cantidad).toBe(2);
      expect(pos.subtotal).toBe(96);
    });

    it('Debe decrementar cantidad y eliminar producto al llegar a 0', () => {
      const pos = usePosStore();
      const prod = pos.productos[0];

      pos.agregarProducto(prod);
      pos.agregarProducto(prod);
      expect(pos.cart[0].cantidad).toBe(2);

      pos.decrementarProducto(prod.id);
      expect(pos.cart[0].cantidad).toBe(1);

      pos.decrementarProducto(prod.id);
      expect(pos.cart).toHaveLength(0);
      expect(pos.subtotal).toBe(0);
    });
  });

  describe('2. Reglas de Negocio Monchis Rewards en POS', () => {
    it('Debe calcular sellos normales y bonificación por termo', () => {
      const pos = usePosStore();
      const prodCafeOrganico = pos.productos[0]; // tipo ORGANICO

      pos.agregarProducto(prodCafeOrganico);
      pos.agregarProducto(prodCafeOrganico);

      // Sin termo -> 2 sellos
      pos.traeTermo = false;
      expect(pos.sellosEstimados).toBe(2);

      // Con termo reutilizable -> 2 + 1 = 3 sellos ecológicos
      pos.traeTermo = true;
      expect(pos.sellosEstimados).toBe(3);
    });

    it('Debe calcular 5% de cashback en puntos sobre el total', () => {
      const pos = usePosStore();
      const prodPanque = pos.productos[3]; // $45
      pos.agregarProducto(prodPanque);
      pos.agregarProducto(prodPanque); // Subtotal = $90

      // 90 * 0.05 = 4.5 -> floor = 4 puntos
      expect(pos.cashbackEstimado).toBe(4);
    });

    it('Debe aplicar descuento por redención de puntos sin exceder el subtotal', () => {
      const pos = usePosStore();
      const prod = pos.productos[0]; // $48
      pos.agregarProducto(prod);

      pos.clientePuntos = 30;
      pos.puntosARedimir = 20;

      expect(pos.descuentoPuntos).toBe(20);
      expect(pos.total).toBe(28); // 48 - 20 = 28
    });
  });

  describe('3. Métodos de Pago y Cálculo de Cambio', () => {
    it('Debe calcular cambio en efectivo si el monto recibido es mayor al total', () => {
      const pos = usePosStore();
      const prod = pos.productos[0]; // $48
      pos.agregarProducto(prod);

      pos.metodoPago = 'EFECTIVO';
      pos.montoRecibidoEfectivo = 100;

      expect(pos.cambioEfectivo).toBe(52);
    });
  });

  describe('4. Procesamiento de la Venta', () => {
    it('Debe procesar la venta exitosamente contra el endpoint /api/pos/orders', async () => {
      const pos = usePosStore();
      const auth = useAuthStore();
      auth.accessToken = 'test-token';

      pos.agregarProducto(pos.productos[0]); // $48

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve({
            mensaje: 'Orden procesada con éxito',
            orden: { id: 'ord_123', total: 48, metodoPago: 'EFECTIVO' },
          }),
      });

      const exito = await pos.procesarVenta();

      expect(exito).toBe(true);
      expect(pos.cart).toHaveLength(0); // El carrito se vacía tras la venta
      expect(pos.ultimaVenta?.id).toBe('ord_123');
    });

    it('Debe manejar errores si el carrito está vacío', async () => {
      const pos = usePosStore();
      const exito = await pos.procesarVenta();

      expect(exito).toBe(false);
      expect(pos.error).toBe('El carrito está vacío');
    });
  });
});
