<script setup lang="ts">
import { ref, computed } from 'vue';
import { usePosStore } from '@/stores/posStore';
import type { ProductType, PaymentMethod } from '@monchis/shared-types';

const pos = usePosStore();

const categoriaSeleccionada = ref<'TODOS' | ProductType>('TODOS');
const filtroBusqueda = ref('');
const modalVentaAbierto = ref(false);

const productosFiltrados = computed(() => {
  return pos.productos.filter((p) => {
    const matchCat = categoriaSeleccionada.value === 'TODOS' || p.tipo === categoriaSeleccionada.value;
    const matchSearch = p.nombre.toLowerCase().includes(filtroBusqueda.value.toLowerCase());
    return matchCat && matchSearch;
  });
});

async function realizarCobro() {
  const success = await pos.procesarVenta();
  if (success) {
    modalVentaAbierto.value = true;
  }
}

function cerrarModal() {
  modalVentaAbierto.value = false;
  pos.ultimaVenta = null;
}
</script>

<template>
  <div class="pos-layout">
    <!-- Panel Izquierdo: Catálogo de Productos -->
    <div class="pos-catalog">
      <header class="pos-catalog__header">
        <div>
          <h1>Punto de Venta — <strong>Monchis Café</strong></h1>
          <p>Selecciona los productos para agregar a la orden</p>
        </div>
        <input
          v-model="filtroBusqueda"
          type="search"
          placeholder="🔍 Buscar café o alimento..."
          class="pos-search"
        />
      </header>

      <!-- Filtro de Categorías -->
      <div class="pos-categories">
        <button
          :class="['pos-tab', { active: categoriaSeleccionada === 'TODOS' }]"
          @click="categoriaSeleccionada = 'TODOS'"
        >
          ☕ Todos
        </button>
        <button
          :class="['pos-tab', { active: categoriaSeleccionada === 'ORGANICO' }]"
          @click="categoriaSeleccionada = 'ORGANICO'"
        >
          🌿 Café Orgánico
        </button>
        <button
          :class="['pos-tab', { active: categoriaSeleccionada === 'COMERCIAL' }]"
          @click="categoriaSeleccionada = 'COMERCIAL'"
        >
          🥐 Repostería & Otros
        </button>
      </div>

      <!-- Cuadrícula de Productos -->
      <div class="product-grid">
        <div
          v-for="producto in productosFiltrados"
          :key="producto.id"
          class="product-card card"
          @click="pos.agregarProducto(producto)"
        >
          <div class="product-card__header">
            <span
              :class="[
                'badge',
                producto.tipo === 'ORGANICO' ? 'badge--organic' : 'badge--commercial',
              ]"
            >
              {{ producto.tipo === 'ORGANICO' ? '🌿 Orgánico' : '🥐 Alimento' }}
            </span>
            <span class="product-card__stock">Stock: {{ producto.stockActual }}</span>
          </div>

          <h3 class="product-card__name">{{ producto.nombre }}</h3>
          <p class="product-card__desc">{{ producto.descripcion }}</p>

          <div class="product-card__footer">
            <span class="product-card__price">${{ producto.precio.toFixed(2) }}</span>
            <button class="btn btn--primary btn--sm" @click.stop="pos.agregarProducto(producto)">
              + Agregar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Panel Derecho: Carrito & Cobro -->
    <aside class="pos-sidebar">
      <div class="pos-sidebar__header">
        <h2>Orden Actual</h2>
        <button v-if="pos.cart.length > 0" class="btn btn--ghost btn--sm" @click="pos.limpiarCarrito">
          Vaciar
        </button>
      </div>

      <!-- Items del Carrito -->
      <div class="cart-items">
        <div v-if="pos.cart.length === 0" class="cart-empty">
          <span>🛒</span>
          <p>El carrito está vacío</p>
        </div>

        <div v-for="item in pos.cart" :key="item.producto.id" class="cart-item">
          <div class="cart-item__info">
            <h4>{{ item.producto.nombre }}</h4>
            <small>${{ item.producto.precio.toFixed(2) }} c/u</small>
          </div>

          <div class="cart-item__actions">
            <button class="qty-btn" @click="pos.decrementarProducto(item.producto.id)">-</button>
            <span class="qty-val">{{ item.cantidad }}</span>
            <button class="qty-btn" @click="pos.agregarProducto(item.producto)">+</button>
            <span class="item-subtotal">${{ (item.producto.precio * item.cantidad).toFixed(2) }}</span>
          </div>
        </div>
      </div>

      <!-- Beneficios Monchis Rewards -->
      <div class="pos-rewards card">
        <h4>🎁 Monchis Rewards</h4>
        <label class="eco-checkbox">
          <input v-model="pos.traeTermo" type="checkbox" />
          <span>🌿 Trae termo reusable (+1 sello ecológico)</span>
        </label>
        <div class="rewards-summary">
          <small>Sellos ganados: <strong>+{{ pos.sellosEstimados }}</strong></small>
          <small>Cashback en puntos: <strong>+${{ pos.cashbackEstimado }}</strong></small>
        </div>
      </div>

      <!-- Selección de Método de Pago -->
      <div class="pos-payment">
        <label>Método de Pago</label>
        <div class="payment-methods">
          <button
            v-for="metodo in (['EFECTIVO', 'TARJETA', 'TRANSFERENCIA', 'MIXTO'] as PaymentMethod[])"
            :key="metodo"
            :class="['payment-btn', { active: pos.metodoPago === metodo }]"
            @click="pos.metodoPago = metodo"
          >
            {{ metodo }}
          </button>
        </div>

        <!-- Campos condicionales de pago -->
        <div v-if="pos.metodoPago === 'EFECTIVO'" class="form-group" style="margin-top: 1rem;">
          <label>Monto Recibido en Efectivo ($)</label>
          <input
            v-model.number="pos.montoRecibidoEfectivo"
            type="number"
            :placeholder="`Total: $${pos.total}`"
            step="any"
          />
          <small v-if="pos.cambioEfectivo > 0" class="cambio-preview">
            💵 Cambio a entregar: <strong>${{ pos.cambioEfectivo }}</strong>
          </small>
        </div>

        <div v-if="pos.metodoPago === 'TRANSFERENCIA' || pos.metodoPago === 'MIXTO'" class="form-group" style="margin-top: 1rem;">
          <label>Clave de Rastreo / Referencia SPEI</label>
          <input
            v-model="pos.referenciaTransferencia"
            type="text"
            placeholder="Ej. SPEI-89234871"
          />
        </div>
      </div>

      <!-- Totales y Acción de Cobro -->
      <div class="pos-totals">
        <div class="totals-row">
          <span>Subtotal:</span>
          <span>${{ pos.subtotal.toFixed(2) }}</span>
        </div>
        <div v-if="pos.descuentoPuntos > 0" class="totals-row discount">
          <span>Descuento Puntos:</span>
          <span>-${{ pos.descuentoPuntos.toFixed(2) }}</span>
        </div>
        <div class="totals-row total-final">
          <span>Total a Pagar:</span>
          <span>${{ pos.total.toFixed(2) }}</span>
        </div>

        <p v-if="pos.error" class="error-message">{{ pos.error }}</p>

        <button
          class="btn btn--primary btn--cobrar"
          :disabled="pos.cart.length === 0 || pos.isLoading"
          @click="realizarCobro"
        >
          {{ pos.isLoading ? 'Procesando Venta...' : `💳 Cobrar $${pos.total.toFixed(2)}` }}
        </button>
      </div>
    </aside>

    <!-- Modal de Venta Exitosa -->
    <div v-if="modalVentaAbierto" class="modal-overlay">
      <div class="modal-card card" v-motion-pop>
        <span class="modal-emoji">🎉</span>
        <h2>¡Venta Procesada con Éxito!</h2>
        <p>Orden ID: <code>{{ pos.ultimaVenta?.id }}</code></p>

        <div class="ticket-details">
          <p>Total Pagado: <strong>${{ pos.ultimaVenta?.total?.toFixed(2) }}</strong></p>
          <p>Método: <strong>{{ pos.ultimaVenta?.metodoPago }}</strong></p>
          <p v-if="pos.ultimaVenta?.cambio > 0">Cambio: <strong>${{ pos.ultimaVenta?.cambio?.toFixed(2) }}</strong></p>
        </div>

        <button class="btn btn--primary" @click="cerrarModal">Nueva Venta</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pos-layout {
  display: grid;
  grid-template-columns: 1fr 420px;
  min-height: calc(100vh - 70px);
  background: var(--color-bg-base);
}

.pos-catalog {
  padding: 2rem;
  overflow-y: auto;
}

.pos-catalog__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1.5rem;
}

.pos-catalog__header h1 {
  font-size: 1.5rem;
}

.pos-search {
  max-width: 300px;
  padding: 0.6rem 1rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--color-border);
  outline: none;
}

.pos-categories {
  display: flex;
  gap: 0.8rem;
  margin-bottom: 2rem;
}

.pos-tab {
  padding: 0.6rem 1.2rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--color-border);
  background: var(--color-bg-surface);
  font-family: var(--font-heading);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.pos-tab.active {
  background: var(--color-primary-dark);
  color: #fff;
  border-color: var(--color-primary-dark);
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.5rem;
}

.product-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  cursor: pointer;
  padding: 1.5rem;
}

.product-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}

.product-card__stock {
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.product-card__name {
  font-size: 1.1rem;
  margin-bottom: 0.4rem;
}

.product-card__desc {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  line-height: 1.4;
  margin-bottom: 1rem;
}

.product-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-card__price {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--color-primary-dark);
}

/* Sidebar Carrito */
.pos-sidebar {
  background: var(--color-bg-surface);
  border-left: 1px solid var(--color-border);
  padding: 2rem;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.pos-sidebar__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.cart-items {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.cart-empty {
  text-align: center;
  padding: 3rem 0;
  color: var(--color-text-muted);
}

.cart-empty span {
  font-size: 3rem;
  display: block;
}

.cart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0;
  border-bottom: 1px solid rgba(232, 216, 205, 0.4);
}

.cart-item__info h4 {
  font-size: 0.95rem;
}

.cart-item__actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.qty-btn {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  background: var(--color-bg-base);
  cursor: pointer;
}

.qty-val {
  font-weight: 600;
  font-size: 0.9rem;
}

.item-subtotal {
  font-weight: 700;
  margin-left: 0.5rem;
  min-width: 60px;
  text-align: right;
}

.pos-rewards {
  padding: 1rem;
  margin-bottom: 1rem;
  background: rgba(243, 201, 201, 0.1);
}

.eco-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  cursor: pointer;
  margin: 0.5rem 0;
}

.rewards-summary {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: var(--color-text-muted);
}

.payment-methods {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.payment-btn {
  padding: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-bg-base);
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
}

.payment-btn.active {
  background: var(--color-secondary-dark);
  color: #fff;
  border-color: var(--color-secondary-dark);
}

.cambio-preview {
  color: #5a8a52;
  font-weight: 600;
  display: block;
  margin-top: 0.4rem;
}

.pos-totals {
  border-top: 2px solid var(--color-border);
  padding-top: 1rem;
}

.totals-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.4rem;
  font-size: 0.95rem;
}

.totals-row.discount {
  color: #e39a9a;
}

.total-final {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-text-main);
  margin: 0.8rem 0;
}

.btn--cobrar {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-card {
  max-width: 400px;
  width: 90%;
  text-align: center;
  padding: 2.5rem;
}

.modal-emoji {
  font-size: 3.5rem;
  display: block;
  margin-bottom: 1rem;
}

.ticket-details {
  background: var(--color-bg-base);
  padding: 1rem;
  border-radius: var(--radius-md);
  margin: 1.5rem 0;
  text-align: left;
}

@media (max-width: 900px) {
  .pos-layout {
    grid-template-columns: 1fr;
  }
}
</style>
