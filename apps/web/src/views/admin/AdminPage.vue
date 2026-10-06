<script setup lang="ts">
import { onMounted } from 'vue';
import { useAdminStore } from '@/stores/adminStore';

const admin = useAdminStore();

onMounted(() => {
  admin.cargarMetricas();
  admin.cargarDLQ();
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
          <button class="btn btn--secondary btn--sm" @click="admin.cargarMetricas" :disabled="admin.isLoading">
            🔄 {{ admin.isLoading ? 'Actualizando...' : 'Refrescar' }}
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
</style>
