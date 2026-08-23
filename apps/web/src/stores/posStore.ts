// ==============================================================================
// Monchis Café — POS Store (Pinia) — Gestión de Ventas y Pagos Mixtos
// ==============================================================================

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { ProductDTO, PaymentMethod, OrderItemDTO } from '@monchis/shared-types';
import { useAuthStore } from './authStore';

export interface CartItem {
  producto: ProductDTO;
  cantidad: number;
}

export const usePosStore = defineStore('pos', () => {
  const auth = useAuthStore();

  const productos = ref<ProductDTO[]>([
    {
      id: 'prod_1',
      nombre: 'Café de Olla Orgánico',
      descripcion: 'Infusión tradicional con piloncillo, canela y granos de Chiapas.',
      tipo: 'ORGANICO',
      precio: 48.0,
      stockActual: 150,
      stockMinimo: 20,
      activo: true,
    },
    {
      id: 'prod_2',
      nombre: 'Cold Brew de la Sierra',
      descripcion: 'Extracción en frío 18h con notas florales de Oaxaca.',
      tipo: 'ORGANICO',
      precio: 65.0,
      stockActual: 80,
      stockMinimo: 15,
      activo: true,
    },
    {
      id: 'prod_3',
      nombre: 'Latte Lavanda y Miel',
      descripcion: 'Espresso doble de especialidad con leche cremada y miel pura.',
      tipo: 'ORGANICO',
      precio: 72.0,
      stockActual: 95,
      stockMinimo: 20,
      activo: true,
    },
    {
      id: 'prod_4',
      nombre: 'Panqué Artesanal de Elote',
      descripcion: 'Horneado con maíz dulce de productores regionales.',
      tipo: 'COMERCIAL',
      precio: 45.0,
      stockActual: 30,
      stockMinimo: 5,
      activo: true,
    },
    {
      id: 'prod_5',
      nombre: 'Galleta de Avena y Arándanos',
      descripcion: 'Artesanal sin conservadores artificiales.',
      tipo: 'COMERCIAL',
      precio: 28.0,
      stockActual: 50,
      stockMinimo: 10,
      activo: true,
    },
  ]);

  const cart = ref<CartItem[]>([]);
  const clienteId = ref<string | null>(null);
  const clientePuntos = ref<number>(0);
  const clienteSellos = ref<number>(0);
  const puntosARedimir = ref<number>(0);
  const traeTermo = ref<boolean>(false);

  // Configuración del método de pago
  const metodoPago = ref<PaymentMethod>('EFECTIVO');
  const montoRecibidoEfectivo = ref<number>(0);
  const montoTarjeta = ref<number>(0);
  const montoTransferencia = ref<number>(0);
  const referenciaTransferencia = ref<string>('');

  const isLoading = ref<boolean>(false);
  const error = ref<string | null>(null);
  const ultimaVenta = ref<any | null>(null);

  // Computed
  const subtotal = computed(() => {
    return cart.value.reduce((sum, item) => sum + item.producto.precio * item.cantidad, 0);
  });

  const totalCafesOrganicos = computed(() => {
    return cart.value
      .filter((item) => item.producto.tipo === 'ORGANICO')
      .reduce((sum, item) => sum + item.cantidad, 0);
  });

  const descuentoPuntos = computed(() => {
    return Math.min(puntosARedimir.value, clientePuntos.value, subtotal.value);
  });

  const total = computed(() => {
    return Math.max(0, subtotal.value - descuentoPuntos.value);
  });

  const cambioEfectivo = computed(() => {
    if (metodoPago.value === 'EFECTIVO' && montoRecibidoEfectivo.value > total.value) {
      return Number((montoRecibidoEfectivo.value - total.value).toFixed(2));
    }
    return 0;
  });

  const sellosEstimados = computed(() => {
    if (totalCafesOrganicos.value === 0) return 0;
    return totalCafesOrganicos.value + (traeTermo.value ? 1 : 0);
  });

  const cashbackEstimado = computed(() => {
    return Math.floor(total.value * 0.05);
  });

  // Acciones de Carrito
  function agregarProducto(producto: ProductDTO) {
    const existing = cart.value.find((i) => i.producto.id === producto.id);
    if (existing) {
      if (existing.cantidad < producto.stockActual) {
        existing.cantidad++;
      }
    } else {
      cart.value.push({ producto, cantidad: 1 });
    }
  }

  function decrementarProducto(productoId: string) {
    const idx = cart.value.findIndex((i) => i.producto.id === productoId);
    if (idx !== -1) {
      if (cart.value[idx].cantidad > 1) {
        cart.value[idx].cantidad--;
      } else {
        cart.value.splice(idx, 1);
      }
    }
  }

  function eliminarProducto(productoId: string) {
    cart.value = cart.value.filter((i) => i.producto.id !== productoId);
  }

  function limpiarCarrito() {
    cart.value = [];
    puntosARedimir.value = 0;
    traeTermo.value = false;
    montoRecibidoEfectivo.value = 0;
    montoTarjeta.value = 0;
    montoTransferencia.value = 0;
    referenciaTransferencia.value = '';
    error.value = null;
  }

  // Procesar Venta
  async function procesarVenta(): Promise<boolean> {
    if (cart.value.length === 0) {
      error.value = 'El carrito está vacío';
      return false;
    }

    isLoading.value = true;
    error.value = null;

    const items: OrderItemDTO[] = cart.value.map((i) => ({
      productoId: i.producto.id,
      cantidad: i.cantidad,
      precioUnitario: i.producto.precio,
      subtotal: i.producto.precio * i.cantidad,
    }));

    try {
      const res = await fetch('/api/pos/orders', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...auth.getAuthHeaders(),
        },
        credentials: 'include',
        body: JSON.stringify({
          clienteId: clienteId.value || undefined,
          items,
          metodoPago: metodoPago.value,
          referenciaPago: referenciaTransferencia.value || undefined,
          montoEfectivo: metodoPago.value === 'EFECTIVO' ? total.value : undefined,
          puntosUsados: descuentoPuntos.value,
          traeTermoReutilizable: traeTermo.value,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        error.value = data.error || 'Error al procesar la venta';
        return false;
      }

      ultimaVenta.value = data.orden;
      limpiarCarrito();
      return true;
    } catch (e: any) {
      error.value = 'Error de conexión con el servidor POS';
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  return {
    productos,
    cart,
    clienteId,
    clientePuntos,
    clienteSellos,
    puntosARedimir,
    traeTermo,
    metodoPago,
    montoRecibidoEfectivo,
    montoTarjeta,
    montoTransferencia,
    referenciaTransferencia,
    isLoading,
    error,
    ultimaVenta,
    subtotal,
    totalCafesOrganicos,
    descuentoPuntos,
    total,
    cambioEfectivo,
    sellosEstimados,
    cashbackEstimado,
    agregarProducto,
    decrementarProducto,
    eliminarProducto,
    limpiarCarrito,
    procesarVenta,
  };
});
