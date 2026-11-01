<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/authStore';

const auth = useAuthStore();
const API_URL = import.meta.env.VITE_API_URL || '';

interface OrderItem {
  id: string;
  productoNombre: string;
  tipo: string;
  cantidad: number;
  precioUnitario: number;
  subtotal: number;
}

interface OrderHistoryItem {
  id: string;
  folio: string;
  fecha: string;
  total: number;
  descuento: number;
  metodoPago: string;
  referenciaPago?: string;
  estado: string;
  cajero: string;
  items: OrderItem[];
}

const ordenes = ref<OrderHistoryItem[]>([]);
const cargando = ref(true);
const error = ref<string | null>(null);

// Modal de Factura / Ticket
const modalFacturaAbierto = ref(false);
const ordenSeleccionada = ref<OrderHistoryItem | null>(null);

async function cargarHistorial() {
  cargando.value = true;
  error.value = null;
  try {
    const res = await fetch(`${API_URL}/api/orders/my-orders`, {
      headers: {
        ...auth.getAuthHeaders(),
      },
    });
    if (res.ok) {
      const data = await res.json();
      ordenes.value = data.ordenes || [];
    } else {
      error.value = 'No se pudo cargar el historial de pedidos.';
    }
  } catch (e) {
    error.value = 'Error al conectar con el servidor para consultar pedidos.';
  } finally {
    cargando.value = false;
  }
}

function verTicket(orden: OrderHistoryItem) {
  ordenSeleccionada.value = orden;
  modalFacturaAbierto.value = true;
}

function cerrarModalFactura() {
  modalFacturaAbierto.value = false;
  ordenSeleccionada.value = null;
}

function imprimirTicket() {
  window.print();
}

const sellos = computed(() => auth.user?.sellosAcumulados ?? 0);
const puntos = computed(() => auth.user?.puntosFidelidad ?? 0);
const sellosRestantes = computed(() => Math.max(0, 8 - (sellos.value % 8)));

const nivelUsuario = computed(() => {
  if (sellos.value >= 35) return { nombre: 'Maestro Caficultor (Oro)', icono: '👑', color: '#c98a2c' };
  if (sellos.value >= 15) return { nombre: 'Amante del Café (Plata)', icono: '☕', color: '#7a8288' };
  return { nombre: 'Grano Verde (Bienvenida)', icono: '🌱', color: '#4a8251' };
});

function formatearFecha(fechaStr: string) {
  try {
    const d = new Date(fechaStr);
    return d.toLocaleDateString('es-MX', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return fechaStr;
  }
}

function calcularSubtotalSinIva(total: number) {
  return (total / 1.16).toFixed(2);
}

function calcularIva(total: number) {
  const subtotal = total / 1.16;
  return (total - subtotal).toFixed(2);
}

function generarUuidSimulado(id: string) {
  const clean = id.replace(/[^a-zA-Z0-9]/g, '').padEnd(32, 'a');
  return `${clean.substring(0, 8)}-${clean.substring(8, 12)}-4${clean.substring(13, 16)}-a${clean.substring(17, 20)}-${clean.substring(20, 32)}`.toUpperCase();
}

onMounted(() => {
  cargarHistorial();
});
</script>

<template>
  <div class="dashboard-page section">
    <div class="container">
      <!-- Encabezado de Bienvenida -->
      <header class="dashboard-header" v-motion-fade-visible>
        <div class="header-info">
          <span class="user-badge" :style="{ borderColor: nivelUsuario.color, color: nivelUsuario.color }">
            {{ nivelUsuario.icono }} {{ nivelUsuario.nombre }}
          </span>
          <h1>¡Hola, {{ auth.user?.nombre || 'Café Lover' }}!</h1>
          <p class="header-subtitle">
            Aquí puedes consultar tus compras en tienda, descargar tus facturas y revisar tus sellos acumulados.
          </p>
        </div>

        <div class="header-actions">
          <RouterLink to="/menu" class="btn btn--primary btn--sm">
            ☕ Ver Menú
          </RouterLink>
          <RouterLink to="/rewards" class="btn btn--secondary btn--sm">
            🎁 Recompensas
          </RouterLink>
          <RouterLink to="/perfil" class="btn btn--ghost btn--sm">
            ⚙️ Mi Cuenta
          </RouterLink>
        </div>
      </header>

      <!-- Tarjeta Digital de Miembro & Resumen Rápido -->
      <div class="member-overview-grid">
        <!-- Tarjeta Digital Monchis Rewards -->
        <div class="loyalty-card" v-motion-slide-visible-bottom :delay="100">
          <div class="loyalty-card__top">
            <div class="brand-mini">
              <span class="logo-emoji">☕</span>
              <strong>MONCHIS REWARDS</strong>
            </div>
            <span class="membership-level">{{ nivelUsuario.icono }} {{ nivelUsuario.nombre }}</span>
          </div>

          <div class="loyalty-card__middle">
            <div class="client-name">{{ auth.user?.nombre || 'Cliente Frecuente' }}</div>
            <div class="client-email">{{ auth.user?.email }}</div>
          </div>

          <!-- Sellos de café en tarjeta -->
          <div class="card-stamps-bar">
            <span class="stamps-title">Sellos acumulados ({{ sellos % 8 }}/8 para bebida gratis):</span>
            <div class="stamps-grid">
              <div
                v-for="i in 8"
                :key="i"
                :class="['stamp-slot', { filled: i <= (sellos % 8) }]"
              >
                <span>{{ i <= (sellos % 8) ? '☕' : '○' }}</span>
              </div>
            </div>
          </div>

          <div class="loyalty-card__bottom">
            <div class="barcode-wrapper">
              <div class="barcode-lines"></div>
              <small class="member-id">ID: MC-{{ (auth.user?.id || 'CLIENTE').substring(0, 8).toUpperCase() }}</small>
            </div>
            <div class="points-badge">
              <span class="points-val">${{ puntos }} MXN</span>
              <small class="points-lbl">en Puntos Cashback</small>
            </div>
          </div>
        </div>

        <!-- Métricas Rápidas -->
        <div class="stats-cards-col" v-motion-slide-visible-bottom :delay="200">
          <div class="stat-box card">
            <span class="stat-box__icon">🪙</span>
            <div>
              <h3>${{ puntos }}.00 MXN</h3>
              <p>Puntos acumulados para pagar tus consumos directos en barra.</p>
            </div>
          </div>

          <div class="stat-box card">
            <span class="stat-box__icon">🎁</span>
            <div>
              <h3>{{ sellosRestantes }} cafés más</h3>
              <p>Faltan {{ sellosRestantes }} compras con tu termo para tu próxima bebida de especialidad gratis.</p>
            </div>
          </div>

          <div class="stat-box card">
            <span class="stat-box__icon">🧾</span>
            <div>
              <h3>{{ ordenes.length }} Pedidos</h3>
              <p>Compras registradas en Monchis Café con comprobante digital disponible.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Sección: Historial de Compras y Facturación -->
      <section class="orders-section card" v-motion-slide-visible-bottom :delay="300">
        <div class="orders-section__header">
          <div>
            <h2>📜 Historial de Compras & Comprobantes</h2>
            <p>Todas tus compras realizadas en sucursal con desglose fiscal simplificado e IVA.</p>
          </div>
          <button class="btn btn--ghost btn--sm" @click="cargarHistorial" :disabled="cargando">
            🔄 {{ cargando ? 'Cargando...' : 'Actualizar' }}
          </button>
        </div>

        <!-- Indicador de Carga -->
        <div v-if="cargando" class="state-container">
          <div class="spinner"></div>
          <p>Consultando tu historial de compras...</p>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="state-container state--error">
          <p>⚠️ {{ error }}</p>
          <button class="btn btn--sm btn--primary" @click="cargarHistorial">Reintentar</button>
        </div>

        <!-- Estado Vacío -->
        <div v-else-if="ordenes.length === 0" class="state-container">
          <span class="empty-icon">☕</span>
          <h3>Aún no tienes compras vinculadas</h3>
          <p>
            Al comprar en barra, indica tu correo o muestra el código de tu <strong>Tarjeta Digital Monchis</strong> al barista para acumular sellos y guardar tus tickets aquí.
          </p>
          <RouterLink to="/menu" class="btn btn--primary btn--sm" style="margin-top: 1rem;">
            Ver Menú y Probar Café de Especialidad
          </RouterLink>
        </div>

        <!-- Tabla / Lista de Órdenes -->
        <div v-else class="orders-table-wrapper">
          <table class="orders-table">
            <thead>
              <tr>
                <th>Folio</th>
                <th>Fecha</th>
                <th>Productos</th>
                <th>Método de Pago</th>
                <th>Total</th>
                <th>Estado</th>
                <th class="text-right">Comprobante</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="orden in ordenes" :key="orden.id">
                <td class="order-folio">
                  <strong>{{ orden.folio }}</strong>
                </td>
                <td class="order-date">{{ formatearFecha(orden.fecha) }}</td>
                <td class="order-items">
                  <div class="items-summary">
                    <span v-for="(item, idx) in orden.items" :key="item.id">
                      {{ item.cantidad }}x {{ item.productoNombre }}<span v-if="idx < orden.items.length - 1">, </span>
                    </span>
                  </div>
                </td>
                <td class="order-payment">
                  <span class="payment-tag">{{ orden.metodoPago }}</span>
                </td>
                <td class="order-total">
                  <strong>${{ orden.total.toFixed(2) }}</strong>
                </td>
                <td>
                  <span class="badge badge--organic">✓ {{ orden.estado }}</span>
                </td>
                <td class="text-right">
                  <button class="btn btn--secondary btn--sm btn-ticket" @click="verTicket(orden)">
                    🧾 Ver Factura
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>

    <!-- Modal de Factura / Ticket Fiscal Simplificado -->
    <div v-if="modalFacturaAbierto && ordenSeleccionada" class="modal-overlay" @click.self="cerrarModalFactura">
      <div class="ticket-modal card">
        <div class="ticket-modal__actions no-print">
          <button class="btn btn--ghost btn--sm" @click="cerrarModalFactura">✕ Cerrar</button>
          <button class="btn btn--primary btn--sm" @click="imprimirTicket">🖨️ Imprimir / Guardar PDF</button>
        </div>

        <!-- Cuerpo del Comprobante Fiscal -->
        <div class="ticket-paper">
          <!-- Encabezado Fiscal -->
          <div class="ticket-header">
            <span class="ticket-logo">☕</span>
            <h2 class="ticket-empresa">MONCHIS CAFÉ S.A.S. DE C.V.</h2>
            <p class="ticket-tax-info">
              <strong>RFC:</strong> MCA260823-9K2<br />
              <strong>Régimen Fiscal:</strong> 601 General de Ley Personas Morales<br />
              <strong>Lugar de Expedición:</strong> C.P. 44100, Guadalajara, Jalisco, México<br />
              <strong>Sucursal Matriz:</strong> Av. Chapultepec Sur 420, Col. Americana
            </p>
            <div class="ticket-divider">--------------------------------------------------</div>
            <div class="ticket-title-doc">COMPROBANTE FISCAL DIGITAL SIMPLIFICADO</div>
            <div class="ticket-meta">
              <div><strong>Folio Interno:</strong> {{ ordenSeleccionada.folio }}</div>
              <div><strong>Folio Fiscal (UUID):</strong> {{ generarUuidSimulado(ordenSeleccionada.id) }}</div>
              <div><strong>Fecha de Emisión:</strong> {{ formatearFecha(ordenSeleccionada.fecha) }}</div>
              <div><strong>Atendido por:</strong> {{ ordenSeleccionada.cajero }}</div>
            </div>
          </div>

          <div class="ticket-divider">--------------------------------------------------</div>

          <!-- Datos del Receptor -->
          <div class="ticket-receptor">
            <div class="section-title">DATOS DEL CLIENTE / RECEPTOR:</div>
            <div><strong>Nombre:</strong> {{ auth.user?.nombre || 'Cliente Frecuente' }}</div>
            <div><strong>Email:</strong> {{ auth.user?.email }}</div>
            <div><strong>RFC:</strong> XAXX010101000 (Público en General)</div>
            <div><strong>Uso de CFDI:</strong> S01 - Sin efectos fiscales / G03 - Gastos en general</div>
          </div>

          <div class="ticket-divider">--------------------------------------------------</div>

          <!-- Partidas de Compra -->
          <table class="ticket-items-table">
            <thead>
              <tr>
                <th class="col-cant">Cant.</th>
                <th class="col-desc">Descripción</th>
                <th class="col-precio">P. Unit</th>
                <th class="col-subtotal">Importe</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in ordenSeleccionada.items" :key="item.id">
                <td class="col-cant">{{ item.cantidad }}</td>
                <td class="col-desc">
                  {{ item.productoNombre }}
                  <small class="sat-code">(SAT: 50201706 / {{ item.tipo }})</small>
                </td>
                <td class="col-precio">${{ item.precioUnitario.toFixed(2) }}</td>
                <td class="col-subtotal">${{ item.subtotal.toFixed(2) }}</td>
              </tr>
            </tbody>
          </table>

          <div class="ticket-divider">--------------------------------------------------</div>

          <!-- Totales Fiscales -->
          <div class="ticket-totals">
            <div class="tot-row">
              <span>Subtotal (Base Imponible):</span>
              <span>${{ calcularSubtotalSinIva(ordenSeleccionada.total) }} MXN</span>
            </div>
            <div v-if="ordenSeleccionada.descuento > 0" class="tot-row tot-discount">
              <span>Descuento Monchis Rewards:</span>
              <span>-${{ ordenSeleccionada.descuento.toFixed(2) }} MXN</span>
            </div>
            <div class="tot-row">
              <span>IVA Trasladado (16%):</span>
              <span>${{ calcularIva(ordenSeleccionada.total) }} MXN</span>
            </div>
            <div class="tot-row tot-final">
              <span>TOTAL PAGADO:</span>
              <span>${{ ordenSeleccionada.total.toFixed(2) }} MXN</span>
            </div>
          </div>

          <div class="ticket-divider">--------------------------------------------------</div>

          <!-- Método de Pago y Leyendas SAT -->
          <div class="ticket-footer-info">
            <div><strong>Forma de Pago:</strong> {{ ordenSeleccionada.metodoPago }}</div>
            <div v-if="ordenSeleccionada.referenciaPago"><strong>Referencia SPEI:</strong> {{ ordenSeleccionada.referenciaPago }}</div>
            <div><strong>Método de Pago SAT:</strong> PUE - Pago en una sola exhibición</div>
            <div><strong>Moneda:</strong> MXN - Peso Mexicano</div>

            <div class="ticket-eco-seal">
              🌿 <strong>Certificación de Café de Especialidad:</strong> Lote 100% orgánico trazable de pequeños productores de Chiapas y Oaxaca.
            </div>

            <!-- Código de barras simulado fiscal -->
            <div class="ticket-qr-fiscal">
              <div class="qr-box">QR SAT</div>
              <div class="qr-text">
                <small>Verificación Fiscal Digital SAT</small><br />
                <small class="cadena-sat">sello: {{ ordenSeleccionada.id.substring(0, 18) }}...cfdi4.0</small>
              </div>
            </div>

            <p class="ticket-legal">
              Este documento es una representación impresa de un comprobante de venta fiscal digital. Para facturas con RFC nominativo, solicita tu complemento en contacto@monchiscafe.com con tu número de folio dentro del mes de compra.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-page {
  background: var(--color-bg-base);
  min-height: 85vh;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.user-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  font-size: 0.8rem;
  font-weight: 700;
  border: 1px solid;
  border-radius: var(--radius-full);
  margin-bottom: 0.5rem;
  background: #fff;
}

.header-subtitle {
  color: var(--color-text-muted);
  max-width: 600px;
  margin-top: 0.25rem;
}

.header-actions {
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
}

/* Tarjeta Digital de Miembro & Resumen */
.member-overview-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2.5rem;
}

.loyalty-card {
  background: linear-gradient(135deg, #2d2420 0%, #46342b 60%, #1f1815 100%);
  color: #f7ede2;
  border-radius: var(--radius-lg);
  padding: 2rem;
  box-shadow: 0 10px 25px rgba(45, 36, 32, 0.35);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 280px;
  position: relative;
  overflow: hidden;
}

.loyalty-card::after {
  content: '☕';
  position: absolute;
  right: -20px;
  bottom: -20px;
  font-size: 10rem;
  opacity: 0.05;
  pointer-events: none;
}

.loyalty-card__top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand-mini {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  letter-spacing: 1.5px;
}

.membership-level {
  background: rgba(255, 255, 255, 0.15);
  padding: 0.25rem 0.65rem;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 600;
  backdrop-filter: blur(4px);
}

.loyalty-card__middle {
  margin: 1.2rem 0;
}

.client-name {
  font-size: 1.4rem;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: 0.5px;
}

.client-email {
  font-size: 0.85rem;
  color: #d1c7bd;
}

.card-stamps-bar {
  background: rgba(0, 0, 0, 0.25);
  padding: 0.8rem 1rem;
  border-radius: var(--radius-md);
  margin-bottom: 1.2rem;
}

.stamps-title {
  display: block;
  font-size: 0.75rem;
  color: #e3d5ca;
  margin-bottom: 0.5rem;
}

.stamps-grid {
  display: flex;
  gap: 0.6rem;
  justify-content: space-between;
}

.stamp-slot {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-full);
  border: 1px dashed rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  background: rgba(255, 255, 255, 0.05);
}

.stamp-slot.filled {
  background: #f3c9c9;
  border-color: #f3c9c9;
  box-shadow: 0 0 8px rgba(243, 201, 201, 0.5);
}

.loyalty-card__bottom {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.barcode-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.barcode-lines {
  width: 140px;
  height: 24px;
  background: repeating-linear-gradient(
    90deg,
    #fff,
    #fff 2px,
    transparent 2px,
    transparent 5px,
    #fff 5px,
    #fff 8px
  );
  opacity: 0.85;
}

.member-id {
  font-family: monospace;
  font-size: 0.75rem;
  color: #e3d5ca;
  letter-spacing: 1px;
}

.points-badge {
  text-align: right;
}

.points-val {
  display: block;
  font-size: 1.2rem;
  font-weight: 700;
  color: #f3c9c9;
}

.points-lbl {
  font-size: 0.7rem;
  color: #d1c7bd;
}

/* Columna de Estadísticas */
.stats-cards-col {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stat-box {
  display: flex;
  align-items: center;
  gap: 1.2rem;
  padding: 1.25rem 1.5rem;
}

.stat-box__icon {
  font-size: 2.2rem;
  flex-shrink: 0;
}

.stat-box h3 {
  margin: 0 0 0.2rem 0;
  font-size: 1.15rem;
}

.stat-box p {
  margin: 0;
  font-size: 0.85rem;
  color: var(--color-text-muted);
}

/* Sección de Pedidos */
.orders-section {
  padding: 2rem;
}

.orders-section__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.orders-section__header h2 {
  margin-bottom: 0.3rem;
}

.orders-section__header p {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  margin: 0;
}

.state-container {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--color-text-muted);
}

.state--error {
  color: #b73838;
}

.empty-icon {
  font-size: 3.5rem;
  display: block;
  margin-bottom: 1rem;
}

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-top-color: var(--color-primary-dark);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.orders-table-wrapper {
  overflow-x: auto;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.orders-table th {
  text-align: left;
  padding: 0.8rem 1rem;
  border-bottom: 2px solid var(--color-border);
  color: var(--color-text-muted);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.orders-table td {
  padding: 1rem;
  border-bottom: 1px solid var(--color-border);
  vertical-align: middle;
}

.order-folio {
  color: var(--color-primary-dark);
  font-family: monospace;
  font-size: 0.95rem;
}

.order-date {
  color: var(--color-text-muted);
  font-size: 0.85rem;
}

.items-summary {
  font-size: 0.85rem;
  max-width: 320px;
}

.payment-tag {
  background: var(--color-bg-base);
  padding: 0.2rem 0.5rem;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid var(--color-border);
}

.btn-ticket {
  white-space: nowrap;
}

/* Modal de Factura / Ticket Fiscal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 1rem;
}

.ticket-modal {
  max-width: 480px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 1.5rem;
  background: #faf8f5;
  border-radius: var(--radius-lg);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.25);
}

.ticket-modal__actions {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.2rem;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 0.8rem;
}

.ticket-paper {
  background: #ffffff;
  padding: 1.8rem;
  border-radius: var(--radius-md);
  border: 1px solid #e3d5ca;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  font-family: 'Courier New', Courier, monospace;
  color: #2b2b2b;
  font-size: 0.82rem;
  line-height: 1.4;
}

.ticket-header {
  text-align: center;
}

.ticket-logo {
  font-size: 2.2rem;
}

.ticket-empresa {
  font-size: 1.1rem;
  font-weight: bold;
  margin: 0.3rem 0;
}

.ticket-tax-info {
  font-size: 0.72rem;
  color: #555;
  margin: 0.4rem 0;
}

.ticket-divider {
  text-align: center;
  color: #999;
  overflow: hidden;
  margin: 0.6rem 0;
  font-size: 0.75rem;
}

.ticket-title-doc {
  text-align: center;
  font-weight: bold;
  font-size: 0.85rem;
  margin-bottom: 0.4rem;
}

.ticket-meta {
  font-size: 0.75rem;
  text-align: left;
}

.ticket-receptor {
  font-size: 0.75rem;
}

.section-title {
  font-weight: bold;
  margin-bottom: 0.2rem;
}

.ticket-items-table {
  width: 100%;
  border-collapse: collapse;
  margin: 0.5rem 0;
}

.ticket-items-table th {
  border-bottom: 1px dashed #999;
  padding: 0.3rem 0;
  font-size: 0.75rem;
  text-align: left;
}

.ticket-items-table td {
  padding: 0.4rem 0;
  vertical-align: top;
}

.col-cant { width: 12%; }
.col-desc { width: 50%; }
.col-precio { width: 18%; text-align: right; }
.col-subtotal { width: 20%; text-align: right; }

.sat-code {
  display: block;
  font-size: 0.65rem;
  color: #777;
}

.ticket-totals {
  font-size: 0.8rem;
  margin-top: 0.5rem;
}

.tot-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.2rem;
}

.tot-discount {
  color: #b73838;
}

.tot-final {
  font-size: 1rem;
  font-weight: bold;
  border-top: 1px dashed #999;
  padding-top: 0.4rem;
  margin-top: 0.4rem;
}

.ticket-footer-info {
  font-size: 0.72rem;
  margin-top: 0.5rem;
}

.ticket-eco-seal {
  background: #f1f8f3;
  padding: 0.5rem;
  border-radius: 4px;
  margin: 0.8rem 0;
  border: 1px dashed #81c784;
  color: #2e7d32;
}

.ticket-qr-fiscal {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin: 0.8rem 0;
  background: #f5f5f5;
  padding: 0.5rem;
  border-radius: 4px;
}

.qr-box {
  width: 50px;
  height: 50px;
  background: #333;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.65rem;
  font-weight: bold;
}

.cadena-sat {
  color: #888;
}

.ticket-legal {
  font-size: 0.65rem;
  color: #888;
  margin-top: 0.5rem;
  text-align: justify;
}

@media print {
  body * {
    visibility: hidden;
  }
  .no-print {
    display: none !important;
  }
  .ticket-paper, .ticket-paper * {
    visibility: visible;
  }
  .ticket-modal {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    max-width: 100%;
    box-shadow: none;
    border: none;
  }
}

@media (max-width: 900px) {
  .member-overview-grid {
    grid-template-columns: 1fr;
  }
}
</style>
