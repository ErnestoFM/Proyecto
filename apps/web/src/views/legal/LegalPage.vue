<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useCookieStore } from '@/stores/cookieStore';

const route = useRoute();
const cookieStore = useCookieStore();

type TabType = 'terminos' | 'privacidad' | 'cookies';
const tabActiva = ref<TabType>('terminos');

// Si viene con hash o query param ej. /legal?tab=cookies
onMounted(() => {
  const queryTab = route.query.tab as TabType;
  if (queryTab && ['terminos', 'privacidad', 'cookies'].includes(queryTab)) {
    tabActiva.value = queryTab;
  }
  cookieStore.cargarPreferencias();
});

const formCookies = ref({
  analitica: cookieStore.preferencias.analitica,
  marketing: cookieStore.preferencias.marketing,
});

const guardadoExitoso = ref(false);

function guardarCookies() {
  cookieStore.guardarPreferencias({
    analitica: formCookies.value.analitica,
    marketing: formCookies.value.marketing,
  });
  guardadoExitoso.value = true;
  setTimeout(() => {
    guardadoExitoso.value = false;
  }, 3000);
}
</script>

<template>
  <div class="legal-page section">
    <div class="container">
      <header class="legal-header text-center">
        <span class="badge badge--organic">📜 Marco Normativo & Privacidad</span>
        <h1>Centro Legal — <strong>Monchis Café</strong></h1>
        <p>Transparencia, protección de datos personales y términos de uso de nuestros servicios.</p>
      </header>

      <!-- Pestañas de Navegación Legal -->
      <div class="legal-tabs">
        <button
          :class="['legal-tab', { active: tabActiva === 'terminos' }]"
          @click="tabActiva = 'terminos'"
        >
          📄 Términos y Condiciones
        </button>
        <button
          :class="['legal-tab', { active: tabActiva === 'privacidad' }]"
          @click="tabActiva = 'privacidad'"
        >
          🔒 Aviso de Privacidad
        </button>
        <button
          :class="['legal-tab', { active: tabActiva === 'cookies' }]"
          @click="tabActiva = 'cookies'"
        >
          🍪 Ajustes de Cookies
        </button>
      </div>

      <!-- Contenido de las Pestañas -->
      <div class="legal-content card" v-motion-fade-visible>
        <!-- 1. Términos y Condiciones -->
        <article v-if="tabActiva === 'terminos'" class="legal-article">
          <h2>Términos y Condiciones de Uso</h2>
          <p class="legal-date">Última actualización: 23 de agosto de 2026</p>

          <section>
            <h3>1. Aceptación de los Términos</h3>
            <p>
              Al registrar una cuenta, acceder o realizar compras en la plataforma digital y Punto de Venta de <strong>Monchis Café</strong>, el usuario acepta de manera expresa los presentes Términos y Condiciones.
            </p>
          </section>

          <section>
            <h3>2. Programa de Fidelización "Monchis Rewards"</h3>
            <p>
              - <strong>Sellos Digitales:</strong> Se otorga 1 sello por cada bebida de café adquirida. Al acumular 8 sellos, el cliente tiene derecho a 1 café gratis equivalente al valor de un café tradicional de la casa.<br />
              - <strong>Bonificación Ecológica:</strong> Aquellos clientes que porten su termo o recipiente reutilizable recibirán 1 sello adicional por compra.<br />
              - <strong>Puntos Cashback:</strong> Los puntos acumulados (5% del valor de compra neta) equivalen a $1.00 MXN por punto y no son canjeables por dinero en efectivo, únicamente aplicables como descuento en órdenes futuras.
            </p>
          </section>

          <section>
            <h3>3. Métodos de Pago y Transacciones</h3>
            <p>
              Se aceptan pagos en efectivo, tarjeta bancaria, puntos de recompensa y transferencias electrónicas (SPEI). Para pagos vía transferencia, es requisito indispensable ingresar la clave de rastreo o referencia bancaria oficial para la validación y emisión de la comanda.
            </p>
          </section>

          <section>
            <h3>4. Lotes de Café Orgánico y Trazabilidad</h3>
            <p>
              Monchis Café garantiza que el café comercializado bajo el distintivo orgánico proviene de cooperativas y productores regionales certificados, con trazabilidad verificable de lote, finca y fecha de tostado.
            </p>
          </section>
        </article>

        <!-- 2. Aviso de Privacidad -->
        <article v-if="tabActiva === 'privacidad'" class="legal-article">
          <h2>Aviso de Privacidad Integral</h2>
          <p class="legal-date">Conforme a la Ley Federal de Protección de Datos Personales</p>

          <section>
            <h3>1. Responsable del Tratamiento de Datos</h3>
            <p>
              <strong>Monchis Café</strong> es responsable del uso y protección de sus datos personales recabados mediante formularios web, registro de clientes y compras en mostrador.
            </p>
          </section>

          <section>
            <h3>2. Datos Personales Recabados</h3>
            <p>
              Para la prestación de servicios recabamos: nombre completo, correo electrónico, historial de compras, saldo de recompensas y datos analíticos de origen de tráfico (parámetros UTM como Google Maps o Instagram).
            </p>
          </section>

          <section>
            <h3>3. Finalidades del Tratamiento</h3>
            <p>
              - <strong>Primarias:</strong> Creación de cuenta, procesamiento de pedidos en el POS, emisión de comprobantes de pago y asignación de recompensas de fidelización.<br />
              - <strong>Secundarias:</strong> Evaluación de calidad, estadísticas de afluencia por canal publicitario y envío de promociones (previa autorización).
            </p>
          </section>

          <section>
            <h3>4. Derechos ARCO</h3>
            <p>
              Usted tiene derecho a Acceder, Rectificar, Cancelar u Oponerse al tratamiento de sus datos personales enviando un correo a <code>privacidad@monchiscafe.com</code>.
            </p>
          </section>
        </article>

        <!-- 3. Configuración y Ajuste de Cookies -->
        <article v-if="tabActiva === 'cookies'" class="legal-article">
          <h2>Centro de Preferencias de Cookies</h2>
          <p class="legal-date">Gestiona cómo utilizamos las cookies y tecnologías de rastreo.</p>

          <p>
            Utilizamos cookies para garantizar la seguridad de tu sesión, recordar tus preferencias y comprender de qué canales provienen nuestras visitas (como Google Maps o redes sociales).
          </p>

          <div class="cookie-options">
            <!-- Cookies Necesarias -->
            <div class="cookie-item">
              <div class="cookie-info">
                <h4>🔒 Cookies Estrictamente Necesarias <span class="badge badge--commercial">Obligatorias</span></h4>
                <p>Imprescindibles para el inicio de sesión stateless (JWT), protección CSRF y prevención contra bots mediante Google reCAPTCHA.</p>
              </div>
              <div class="cookie-switch">
                <input type="checkbox" checked disabled />
              </div>
            </div>

            <!-- Cookies de Analítica -->
            <div class="cookie-item">
              <div class="cookie-info">
                <h4>📊 Cookies de Rendimiento y Analítica</h4>
                <p>Nos ayudan a medir el volumen de visitas y saber si llegaste a Monchis Café desde Google Maps o búsqueda directa.</p>
              </div>
              <div class="cookie-switch">
                <label class="switch-label">
                  <input v-model="formCookies.analitica" type="checkbox" />
                  <span class="slider"></span>
                </label>
              </div>
            </div>

            <!-- Cookies de Marketing -->
            <div class="cookie-item">
              <div class="cookie-info">
                <h4>🎯 Cookies de Marketing y Publicidad</h4>
                <p>Permiten personalizar promociones y medir el impacto de nuestras publicaciones en Instagram y redes sociales.</p>
              </div>
              <div class="cookie-switch">
                <label class="switch-label">
                  <input v-model="formCookies.marketing" type="checkbox" />
                  <span class="slider"></span>
                </label>
              </div>
            </div>
          </div>

          <div class="cookie-actions">
            <button class="btn btn--primary" @click="guardarCookies">Guardar Mis Preferencias</button>
            <button class="btn btn--secondary" @click="cookieStore.aceptarTodas(); formCookies.analitica = true; formCookies.marketing = true; guardarCookies();">
              Aceptar Todas
            </button>
            <button class="btn btn--ghost" @click="cookieStore.rechazarOpcionales(); formCookies.analitica = false; formCookies.marketing = false; guardarCookies();">
              Solo Necesarias
            </button>
          </div>

          <p v-if="guardadoExitoso" class="success-message" style="margin-top: 1rem; font-weight: 600;">
            ✅ Tus preferencias de cookies se han actualizado con éxito.
          </p>
        </article>
      </div>
    </div>
  </div>
</template>

<style scoped>
.legal-page {
  background: var(--color-bg-base);
  min-height: 80vh;
}

.legal-header {
  margin-bottom: 2.5rem;
}

.legal-header h1 {
  margin: 0.5rem 0;
}

.legal-tabs {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.legal-tab {
  padding: 0.8rem 1.6rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--color-border);
  background: var(--color-bg-surface);
  font-family: var(--font-heading);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.legal-tab.active {
  background: var(--color-primary-dark);
  color: #fff;
  border-color: var(--color-primary-dark);
  box-shadow: var(--shadow-sm);
}

.legal-content {
  max-width: 860px;
  margin: 0 auto;
  padding: 3rem;
}

.legal-article h2 {
  font-size: 1.8rem;
  margin-bottom: 0.3rem;
}

.legal-date {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  margin-bottom: 2rem;
}

.legal-article section {
  margin-bottom: 2rem;
}

.legal-article h3 {
  font-size: 1.2rem;
  margin-bottom: 0.6rem;
  color: var(--color-text-main);
}

.legal-article p {
  color: var(--color-text-muted);
  line-height: 1.8;
}

.cookie-options {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin: 2rem 0;
}

.cookie-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
  padding: 1.2rem;
  background: var(--color-bg-base);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.cookie-info h4 {
  font-size: 1rem;
  margin-bottom: 0.3rem;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.cookie-info p {
  font-size: 0.85rem;
}

.cookie-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .legal-content {
    padding: 1.5rem;
  }
  .cookie-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  .cookie-actions {
    flex-direction: column;
  }
}
</style>
