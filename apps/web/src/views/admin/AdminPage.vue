<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAdminStore } from '@/stores/adminStore';
import { useAuthStore } from '@/stores/authStore';

const admin = useAdminStore();
const auth = useAuthStore();

const modal2FAAbierto = ref(false);
const setup2FAData = ref<{ secret: string; otpAuthUrl: string; qrCodeDataUrl: string } | null>(null);
const codigoTOTP = ref('');
const cargando2FA = ref(false);
const mensaje2FA = ref<string | null>(null);
const error2FA = ref<string | null>(null);

async function abrirModal2FA() {
  modal2FAAbierto.value = true;
  codigoTOTP.value = '';
  mensaje2FA.value = null;
  error2FA.value = null;

  if (!auth.user?.dosFactoresActivo) {
    cargando2FA.value = true;
    const data = await auth.setup2FA();
    if (data) {
      setup2FAData.value = data;
    }
    cargando2FA.value = false;
  }
}

async function activar2FA() {
  if (!setup2FAData.value || codigoTOTP.value.length !== 6) return;
  cargando2FA.value = true;
  error2FA.value = null;
  const ok = await auth.enable2FA(setup2FAData.value.secret, codigoTOTP.value);
  cargando2FA.value = false;
  if (ok) {
    mensaje2FA.value = '¡Doble factor de autenticación activado con éxito!';
    codigoTOTP.value = '';
  } else {
    error2FA.value = auth.error || 'Código incorrecto. Intente de nuevo.';
  }
}

async function desactivar2FA() {
  if (codigoTOTP.value.length !== 6) return;
  cargando2FA.value = true;
  error2FA.value = null;
  const ok = await auth.disable2FA(codigoTOTP.value);
  cargando2FA.value = false;
  if (ok) {
    mensaje2FA.value = '2FA desactivado correctamente.';
    codigoTOTP.value = '';
    const data = await auth.setup2FA();
    if (data) setup2FAData.value = data;
  } else {
    error2FA.value = auth.error || 'Código incorrecto.';
  }
}

function refrescarTodo() {
  admin.cargarMetricas();
  admin.cargarDLQ();
  admin.cargarLotes();
}

onMounted(() => {
  refrescarTodo();
});

// Función para exportar reporte completo a Excel (CSV con formato amigable y UTF-8 BOM)
function exportarExcel() {
  const hoy = new Date().toISOString().split('T')[0];
  const BOM = '\uFEFF';
  let csv = 'REPORTE EJECUTIVO DE VENTAS Y ANALÍTICA — MONCHIS CAFÉ\r\n';
  csv += `Fecha de Generación:;${hoy}\r\n\r\n`;

  // 1. Resumen de KPIs
  csv += '1. RESUMEN FINANCIERO Y OPERATIVO\r\n';
  csv += 'Métrica;Valor\r\n';
  csv += `Ingresos Totales;$${admin.resumen?.totalIngresos?.toFixed(2) || '0.00'} MXN\r\n`;
  csv += `Total de Órdenes;${admin.resumen?.totalOrdenes || 0}\r\n`;
  csv += `Ventas Café Orgánico;$${admin.resumen?.totalVentasOrganico?.toFixed(2) || '0.00'} MXN\r\n`;
  csv += `Ventas Comercial;$${admin.resumen?.totalVentasComercial?.toFixed(2) || '0.00'} MXN\r\n`;
  csv += `Porcentaje Orgánico;${admin.resumen?.porcentajeOrganico || 0}%\r\n`;
  csv += `Mensajes en DLQ;${admin.mensajesDLQ.length}\r\n\r\n`;

  // 2. Atribución de Tráfico
  csv += '2. ATRIBUCIÓN DE TRÁFICO (MARKETING Y CONVERSIÓN)\r\n';
  csv += 'Canal de Origen;Visitas;Ventas;Conversión (%);Monto Generado (MXN)\r\n';
  admin.atribucionTrafico.forEach((canal) => {
    const conv = canal.totalVisitas > 0 ? ((canal.totalVentas / canal.totalVisitas) * 100).toFixed(1) : '0.0';
    csv += `${canal.source};${canal.totalVisitas};${canal.totalVentas};${conv}%;$${canal.montoGenerado.toFixed(2)}\r\n`;
  });
  csv += '\r\n';

  // 3. Productos Más Vendidos
  csv += '3. PRODUCTOS MÁS VENDIDOS\r\n';
  csv += 'Producto;Categoría;Unidades Vendidas;Ingresos Totales (MXN)\r\n';
  admin.topVendidos.forEach((p) => {
    csv += `${p.nombre};${p.tipo};${p.unidadesVendidas};$${p.ingresosTotales.toFixed(2)}\r\n`;
  });
  csv += '\r\n';

  // 4. Lotes Activos
  csv += '4. TRAZABILIDAD Y LOTES DE CAFÉ ORGÁNICO\r\n';
  csv += 'Número de Lote;Proveedor Regional;Finca de Origen;Kilos Disponibles;Caducidad\r\n';
  admin.lotesActivos.forEach((l) => {
    csv += `${l.numeroLote};${l.proveedorRegional};${l.fincaOrigen || 'N/A'};${l.cantidadKilos};${l.fechaCaducidad.split('T')[0]}\r\n`;
  });

  const blob = new Blob([BOM + csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', `Reporte_Monchis_Cafe_${hoy}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

// Función para imprimir / exportar reporte formal a PDF
function exportarPDF() {
  window.print();
}
</script>

<template>
  <div class="admin-page section">
    <div class="container">
      <header class="admin-header">
        <div>
          <span class="badge badge--organic">👑 Panel de Administración</span>
          <h1>Métricas & Analítica — <strong>Monchis Café</strong></h1>
          <p>Supervisión en tiempo real de ingresos, canales de tráfico, trazabilidad y mensajería</p>
        </div>
        <div class="admin-actions">
          <button class="btn btn--secondary btn--sm" @click="refrescarTodo" :disabled="admin.isLoading">
            🔄 {{ admin.isLoading ? 'Actualizando...' : 'Refrescar' }}
          </button>
          <button
            class="btn btn--secondary btn--sm"
            @click="abrirModal2FA"
            :title="auth.user?.dosFactoresActivo ? '2FA Activo y Protegido' : 'Configurar Doble Factor'"
          >
            🔐 {{ auth.user?.dosFactoresActivo ? '2FA Activo' : 'Configurar 2FA' }}
          </button>
          <button class="btn btn--secondary btn--sm export-btn" @click="exportarExcel" title="Exportar reporte compatible con Excel">
            📊 Exportar Excel
          </button>
          <button class="btn btn--primary btn--sm export-btn" @click="exportarPDF" title="Generar versión imprimible en PDF">
            📄 Exportar PDF
          </button>
        </div>
      </header>

      <!-- KPI Summary Cards -->
      <section class="kpi-grid">
        <div class="kpi-card card" v-motion-slide-visible-bottom :delay="100">
          <span class="kpi-icon">💰</span>
          <div class="kpi-info">
            <small>Ingresos Totales</small>
            <h2>${{ admin.resumen?.totalIngresos?.toLocaleString('es-MX', { minimumFractionDigits: 2 }) }}</h2>
          </div>
        </div>

        <div class="kpi-card card" v-motion-slide-visible-bottom :delay="200">
          <span class="kpi-icon">☕</span>
          <div class="kpi-info">
            <small>Total de Órdenes</small>
            <h2>{{ admin.resumen?.totalOrdenes }}</h2>
          </div>
        </div>

        <div class="kpi-card card" v-motion-slide-visible-bottom :delay="300">
          <span class="kpi-icon">🌿</span>
          <div class="kpi-info">
            <small>% Café Orgánico</small>
            <h2>{{ admin.resumen?.porcentajeOrganico }}%</h2>
          </div>
        </div>

        <div class="kpi-card card" v-motion-slide-visible-bottom :delay="400">
          <span class="kpi-icon">🛡️</span>
          <div class="kpi-info">
            <small>Mensajes en DLQ</small>
            <h2>{{ admin.mensajesDLQ.length }}</h2>
          </div>
        </div>
      </section>

      <!-- Grid Principal: Tráfico UTM y Top Productos -->
      <div class="admin-main-grid">
        <!-- Panel de Atribución de Tráfico (Google Maps / Instagram / Directo) -->
        <section class="card traffic-card" v-motion-slide-visible-bottom :delay="200">
          <div class="section-title">
            <span class="title-icon">📍</span>
            <div>
              <h3>Atribución de Tráfico & Conversión</h3>
              <p>Rendimiento por canal de origen capturado mediante parámetros UTM</p>
            </div>
          </div>

          <table class="admin-table">
            <thead>
              <tr>
                <th>Canal de Origen</th>
                <th>Visitas</th>
                <th>Ventas</th>
                <th>Conversión</th>
                <th>Ingresos Generados</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="canal in admin.atribucionTrafico" :key="canal.source">
                <td>
                  <span class="channel-badge" :data-source="canal.source">
                    {{ canal.source === 'google_maps' ? '🗺️ Google Maps' : canal.source === 'instagram' ? '📸 Instagram' : '🌐 Tráfico Directo' }}
                  </span>
                </td>
                <td>{{ canal.totalVisitas }}</td>
                <td>{{ canal.totalVentas }}</td>
                <td>
                  <strong>{{ ((canal.totalVentas / canal.totalVisitas) * 100).toFixed(1) }}%</strong>
                </td>
                <td class="revenue-cell">${{ canal.montoGenerado.toLocaleString('es-MX', { minimumFractionDigits: 2 }) }}</td>
              </tr>
            </tbody>
          </table>
        </section>

        <!-- Productos Más Vendidos -->
        <section class="card products-card" v-motion-slide-visible-bottom :delay="300">
          <div class="section-title">
            <span class="title-icon">🏆</span>
            <div>
              <h3>Top Productos</h3>
              <p>Artículos con mayor demanda</p>
            </div>
          </div>

          <div class="top-products-list">
            <div v-for="(prod, idx) in admin.topVendidos" :key="prod.productoId" class="top-product-item">
              <span class="rank-badge">#{{ idx + 1 }}</span>
              <div class="prod-info">
                <h4>{{ prod.nombre }}</h4>
                <small>{{ prod.unidadesVendidas }} unidades vendidas</small>
              </div>
              <span class="prod-revenue">${{ prod.ingresosTotales.toFixed(2) }}</span>
            </div>
          </div>
        </section>
      </div>

      <!-- Trazabilidad de Lotes de Café Orgánico -->
      <section class="card batches-card" v-motion-slide-visible-bottom :delay="400">
        <div class="section-title">
          <span class="title-icon">🌱</span>
          <div>
            <h3>Trazabilidad de Lotes de Café Regional</h3>
            <p>Control de lotes activos, origen en fincas y fechas de tostado</p>
          </div>
        </div>

        <table class="admin-table">
          <thead>
            <tr>
              <th>Nº de Lote</th>
              <th>Proveedor Regional</th>
              <th>Finca de Origen</th>
              <th>Fecha de Tostado</th>
              <th>Stock Restante</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lote in admin.lotesActivos" :key="lote.id">
              <td><code>{{ lote.numeroLote }}</code></td>
              <td>{{ lote.proveedorRegional }}</td>
              <td>{{ lote.fincaOrigen }}</td>
              <td>{{ new Date(lote.fechaCosechaTostado).toLocaleDateString('es-MX') }}</td>
              <td><strong>{{ lote.cantidadKilos }} kg</strong></td>
              <td><span class="badge badge--organic">Activo / Fresco</span></td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- Modal de Configuración y Gestión 2FA / TOTP -->
      <div v-if="modal2FAAbierto" class="modal-overlay" @click.self="modal2FAAbierto = false">
        <div class="modal-card card" v-motion-pop>
          <div class="modal-header">
            <h3>🔐 Seguridad — Doble Factor de Autenticación (2FA)</h3>
            <button class="close-btn" @click="modal2FAAbierto = false">✕</button>
          </div>

          <div class="modal-body">
            <!-- Estado Activo -->
            <div v-if="auth.user?.dosFactoresActivo" class="twofa-status active">
              <span class="status-badge success">🛡️ 2FA Activo y Protegido</span>
              <p>Tu cuenta de Administrador exige autenticación con aplicación móvil (Google Authenticator / Authy) en cada inicio de sesión.</p>

              <div class="disable-section">
                <h4>Desactivar Doble Factor</h4>
                <p class="small-text">Para desactivarlo, ingresa tu código TOTP actual de 6 dígitos:</p>
                <div class="input-inline">
                  <input
                    v-model="codigoTOTP"
                    type="text"
                    maxlength="6"
                    placeholder="123456"
                    class="totp-code-input"
                  />
                  <button
                    class="btn btn--danger btn--sm"
                    :disabled="cargando2FA || codigoTOTP.length !== 6"
                    @click="desactivar2FA"
                  >
                    Desactivar 2FA
                  </button>
                </div>
              </div>
            </div>

            <!-- Estado Inactivo (Configuración Inicial) -->
            <div v-else class="twofa-status inactive">
              <span class="status-badge warning">⚠️ 2FA Desactivado (Obligatorio para Administradores)</span>
              <p>Escanea el código QR con <strong>Google Authenticator</strong> o <strong>Authy</strong>:</p>

              <div v-if="cargando2FA && !setup2FAData" class="loading-state">
                <span>🔄 Generando secreto criptográfico...</span>
              </div>

              <div v-else-if="setup2FAData" class="qr-container">
                <img :src="setup2FAData.qrCodeDataUrl" alt="Código QR TOTP" class="qr-image" />
                <div class="secret-box">
                  <small>Clave de configuración manual:</small>
                  <code>{{ setup2FAData.secret }}</code>
                </div>

                <div class="verify-step">
                  <label>Ingresa el código de 6 dígitos para validar la vinculación:</label>
                  <div class="input-inline">
                    <input
                      v-model="codigoTOTP"
                      type="text"
                      maxlength="6"
                      placeholder="123456"
                      class="totp-code-input"
                    />
                    <button
                      class="btn btn--primary btn--sm"
                      :disabled="cargando2FA || codigoTOTP.length !== 6"
                      @click="activar2FA"
                    >
                      Verificar y Activar 2FA
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="mensaje2FA" class="feedback success">✅ {{ mensaje2FA }}</div>
            <div v-if="error2FA" class="feedback error">❌ {{ error2FA }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-page {
  background: var(--color-bg-base);
  min-height: calc(100vh - 70px);
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2.5rem;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.kpi-card {
  display: flex;
  align-items: center;
  gap: 1.2rem;
  padding: 1.5rem;
}

.kpi-icon {
  font-size: 2.5rem;
}

.kpi-info small {
  color: var(--color-text-muted);
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.kpi-info h2 {
  font-size: 1.8rem;
  margin-top: 0.2rem;
  color: var(--color-primary-dark);
}

.admin-main-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 2rem;
  margin-bottom: 2.5rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 1.5rem;
}

.title-icon {
  font-size: 1.8rem;
}

.section-title h3 {
  font-size: 1.2rem;
}

.section-title p {
  font-size: 0.85rem;
  color: var(--color-text-muted);
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.admin-table th {
  text-align: left;
  padding: 0.8rem;
  color: var(--color-text-muted);
  font-weight: 600;
  border-bottom: 2px solid var(--color-border);
}

.admin-table td {
  padding: 1rem 0.8rem;
  border-bottom: 1px solid rgba(232, 216, 205, 0.4);
}

.channel-badge {
  font-weight: 600;
  font-size: 0.85rem;
}

.revenue-cell {
  font-weight: 700;
  color: var(--color-secondary-dark);
}

.top-products-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.top-product-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.8rem;
  background: var(--color-bg-base);
  border-radius: var(--radius-md);
}

.rank-badge {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--color-primary-dark);
  min-width: 30px;
}

.prod-info {
  flex: 1;
}

.prod-info h4 {
  font-size: 0.95rem;
}

.prod-info small {
  color: var(--color-text-muted);
}

.prod-revenue {
  font-weight: 700;
  color: var(--color-primary-dark);
}

.batches-card {
  margin-bottom: 2.5rem;
}

@media (max-width: 992px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .admin-main-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .kpi-grid {
    grid-template-columns: 1fr;
  }
  .admin-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}

.admin-actions {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.export-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-weight: 600;
}

@media print {
  .admin-header .admin-actions,
  .admin-header button,
  .badge {
    display: none !important;
  }

  .admin-page {
    padding: 0 !important;
  }

  .container {
    max-width: 100% !important;
    padding: 0 !important;
  }

  .card {
    box-shadow: none !important;
    border: 1px solid #CBD5E1 !important;
    break-inside: avoid;
  }
}

/* Modal 2FA */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(40, 30, 25, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-card {
  max-width: 520px;
  width: 100%;
  padding: 2rem;
  background: var(--color-bg-card, #FFFFFF);
  border-radius: var(--radius-md, 16px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-header h3 {
  font-size: 1.15rem;
  color: var(--color-primary-dark);
}

.close-btn {
  background: transparent;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: var(--color-text-muted);
}

.status-badge {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
}

.status-badge.success {
  background: #E8F5E9;
  color: #2E7D32;
}

.status-badge.warning {
  background: #FFF3E0;
  color: #E65100;
}

.qr-container {
  text-align: center;
  margin: 1.2rem 0;
}

.qr-image {
  width: 180px;
  height: 180px;
  margin: 0 auto 1rem;
  border-radius: 12px;
  border: 4px solid var(--color-border);
}

.secret-box {
  background: rgba(243, 201, 201, 0.2);
  padding: 0.6rem;
  border-radius: 8px;
  margin-bottom: 1.2rem;
}

.secret-box code {
  display: block;
  font-family: monospace;
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--color-primary-dark);
  margin-top: 0.2rem;
}

.input-inline {
  display: flex;
  gap: 0.8rem;
  margin-top: 0.5rem;
}

.totp-code-input {
  font-family: monospace;
  font-size: 1.3rem;
  letter-spacing: 0.3rem;
  text-align: center;
  font-weight: 700;
  max-width: 180px;
  padding: 0.5rem;
}

.disable-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-border);
}

.feedback {
  margin-top: 1rem;
  padding: 0.6rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  text-align: center;
}

.feedback.success {
  background: #E8F5E9;
  color: #2E7D32;
}

.feedback.error {
  background: #FFEBEE;
  color: #C62828;
}
</style>
