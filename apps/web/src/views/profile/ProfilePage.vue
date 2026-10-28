<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

const router = useRouter();
const auth = useAuthStore();

// Modal / Estados para 2FA
const modal2FAAbierto = ref(false);
const setup2FAData = ref<{ secret: string; otpAuthUrl: string; qrCodeDataUrl: string } | null>(null);
const codigoTOTP = ref('');
const cargando2FA = ref(false);
const mensaje2FA = ref<string | null>(null);
const error2FA = ref<string | null>(null);

const maxSellos = 8;
const sellos = computed(() => auth.user?.sellosAcumulados ?? 0);
const puntos = computed(() => auth.user?.puntosFidelidad ?? 0);

const rolLegible = computed(() => {
  switch (auth.user?.rol) {
    case 'ADMIN':
      return 'Administrador General';
    case 'CAJERO':
      return 'Cajero de Turno (POS)';
    case 'CLIENTE':
      return 'Cliente Frecuente';
    default:
      return auth.user?.rol || 'Usuario';
  }
});

const fechaRegistro = computed(() => {
  if (!auth.user?.creadoEn) return 'Reciente';
  try {
    return new Date(auth.user.creadoEn).toLocaleDateString('es-MX', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  } catch {
    return auth.user.creadoEn;
  }
});

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

function cerrarModal2FA() {
  modal2FAAbierto.value = false;
  setup2FAData.value = null;
  codigoTOTP.value = '';
  mensaje2FA.value = null;
  error2FA.value = null;
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
    error2FA.value = auth.error || 'Código incorrecto. Verifica en tu app de autenticación e intenta de nuevo.';
  }
}

async function desactivar2FA() {
  if (codigoTOTP.value.length !== 6) return;
  cargando2FA.value = true;
  error2FA.value = null;
  const ok = await auth.disable2FA(codigoTOTP.value);
  cargando2FA.value = false;
  if (ok) {
    mensaje2FA.value = 'Doble factor de autenticación desactivado.';
    codigoTOTP.value = '';
  } else {
    error2FA.value = auth.error || 'Código incorrecto. Intente de nuevo.';
  }
}

function cerrarSesion() {
  auth.logout();
  router.push('/login');
}
</script>

<template>
  <div class="section profile-view">
    <div class="container">
      <div class="profile-header" v-motion-fade-visible>
        <div class="profile-avatar">👤</div>
        <div class="profile-title-group">
          <h1>{{ auth.user?.nombre || 'Mi Perfil' }}</h1>
          <p class="profile-subtitle">
            <span class="badge" :class="'badge--' + (auth.user?.rol?.toLowerCase() || 'cliente')">
              {{ rolLegible }}
            </span>
            <span class="user-email">{{ auth.user?.email }}</span>
          </p>
        </div>
      </div>

      <div class="profile-grid">
        <!-- Tarjeta de Datos Personales y Cuenta -->
        <div class="card profile-card" v-motion-slide-visible-bottom :delay="100">
          <div class="card-header">
            <h3>📋 Información de la Cuenta</h3>
          </div>
          <div class="card-body">
            <div class="info-row">
              <span class="info-label">Nombre completo:</span>
              <strong class="info-value">{{ auth.user?.nombre }}</strong>
            </div>
            <div class="info-row">
              <span class="info-label">Correo electrónico:</span>
              <span class="info-value">{{ auth.user?.email }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Identificador (ID):</span>
              <span class="info-value font-mono">{{ auth.user?.id }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Rol del sistema:</span>
              <span class="info-value">{{ rolLegible }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Miembro desde:</span>
              <span class="info-value">{{ fechaRegistro }}</span>
            </div>
          </div>
        </div>

        <!-- Tarjeta de Monchis Rewards & Lealtad -->
        <div class="card profile-card" v-motion-slide-visible-bottom :delay="200">
          <div class="card-header">
            <h3>🎁 Monchis Rewards</h3>
            <RouterLink to="/rewards" class="card-header-link">Ver catálogo ↗</RouterLink>
          </div>
          <div class="card-body">
            <div class="rewards-summary">
              <div class="metric-box">
                <span class="metric-value">{{ sellos }} / {{ maxSellos }}</span>
                <span class="metric-label">Sellos Digitales</span>
              </div>
              <div class="metric-box">
                <span class="metric-value">{{ puntos }}</span>
                <span class="metric-label">Puntos ($ {{ puntos }} MXN)</span>
              </div>
            </div>

            <!-- Visualizador de los 8 sellos -->
            <div class="stamps-card">
              <div class="stamps-header">
                <span>Tu tarjeta de café gratis</span>
                <small>{{ maxSellos - (sellos % maxSellos) }} sellos para tu próximo café de regalo</small>
              </div>
              <div class="stamps-grid">
                <div
                  v-for="i in maxSellos"
                  :key="i"
                  class="stamp-slot"
                  :class="{
                    'stamp-slot--filled': i <= (sellos % maxSellos === 0 && sellos > 0 ? maxSellos : sellos % maxSellos),
                    'stamp-slot--reward': i === maxSellos
                  }"
                >
                  <span v-if="i <= (sellos % maxSellos === 0 && sellos > 0 ? maxSellos : sellos % maxSellos)">
                    {{ i === maxSellos ? '🎉' : '☕' }}
                  </span>
                  <span v-else class="stamp-empty">
                    {{ i === maxSellos ? '🎁' : i }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tarjeta de Seguridad y 2FA -->
        <div class="card profile-card" v-motion-slide-visible-bottom :delay="300">
          <div class="card-header">
            <h3>🔐 Seguridad de la Cuenta</h3>
          </div>
          <div class="card-body">
            <div class="security-status-box">
              <div class="security-icon">
                {{ auth.user?.dosFactoresActivo ? '🛡️' : '⚠️' }}
              </div>
              <div class="security-details">
                <strong>Autenticación de Dos Factores (2FA / TOTP)</strong>
                <p>
                  {{ auth.user?.dosFactoresActivo
                    ? 'Tu cuenta está protegida con código de verificación temporal (Google Authenticator / Authy).'
                    : 'Añade una capa extra de protección a tu cuenta configurando una app de autenticación.'
                  }}
                </p>
              </div>
            </div>

            <div class="security-actions">
              <button
                v-if="!auth.user?.dosFactoresActivo"
                @click="abrirModal2FA"
                class="btn btn--secondary btn--sm"
              >
                Activar 2FA
              </button>
              <button
                v-else
                @click="abrirModal2FA"
                class="btn btn--outline btn--sm"
              >
                Desactivar o Gestionar 2FA
              </button>
            </div>
          </div>
        </div>

        <!-- Tarjeta de Accesos Directos según Rol -->
        <div class="card profile-card" v-motion-slide-visible-bottom :delay="400">
          <div class="card-header">
            <h3>🚀 Accesos Rápidos</h3>
          </div>
          <div class="card-body quick-links">
            <RouterLink to="/dashboard" class="quick-link-btn">
              <span>📊</span>
              <div>
                <strong>Panel de Control</strong>
                <small>Resumen general de tu cuenta y pedidos</small>
              </div>
            </RouterLink>

            <RouterLink
              v-if="auth.user?.rol === 'ADMIN' || auth.user?.rol === 'CAJERO'"
              to="/pos"
              class="quick-link-btn"
            >
              <span>🛒</span>
              <div>
                <strong>Punto de Venta (POS)</strong>
                <small>Terminal de cobro y registro de pedidos</small>
              </div>
            </RouterLink>

            <RouterLink
              v-if="auth.user?.rol === 'ADMIN'"
              to="/admin"
              class="quick-link-btn"
            >
              <span>⚙️</span>
              <div>
                <strong>Panel de Administración</strong>
                <small>Inventario, lotes de café y métricas de atribución</small>
              </div>
            </RouterLink>

            <button @click="cerrarSesion" class="quick-link-btn quick-link-btn--danger">
              <span>🚪</span>
              <div>
                <strong>Cerrar Sesión</strong>
                <small>Finalizar sesión actual en este navegador</small>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para Configuración de 2FA -->
    <div v-if="modal2FAAbierto" class="modal-overlay" @click.self="cerrarModal2FA">
      <div class="modal-card">
        <div class="modal-header">
          <h3>
            {{ auth.user?.dosFactoresActivo ? 'Desactivar Doble Factor (2FA)' : 'Configurar Doble Factor (2FA)' }}
          </h3>
          <button class="modal-close" @click="cerrarModal2FA">✕</button>
        </div>

        <div class="modal-body">
          <div v-if="mensaje2FA" class="alert alert--success">
            {{ mensaje2FA }}
          </div>
          <div v-if="error2FA" class="alert alert--error">
            {{ error2FA }}
          </div>

          <!-- Caso: Activar 2FA -->
          <template v-if="!auth.user?.dosFactoresActivo">
            <div v-if="cargando2FA" class="text-center py-4">
              <p>Generando llave de autenticación segura...</p>
            </div>
            <div v-else-if="setup2FAData" class="setup-2fa-content">
              <p class="step-desc">
                1. Escanea este código QR con <strong>Google Authenticator</strong>, <strong>Authy</strong> o 1Password:
              </p>
              <div class="qr-container">
                <img :src="setup2FAData.qrCodeDataUrl" alt="Código QR 2FA" />
              </div>
              <p class="step-desc">
                O introduce manualmente este código secreto:
              </p>
              <div class="secret-box">
                <code>{{ setup2FAData.secret }}</code>
              </div>

              <div class="form-group mt-4">
                <label for="codigoTOTP">2. Ingresa el código de 6 dígitos que muestra tu app:</label>
                <input
                  id="codigoTOTP"
                  v-model="codigoTOTP"
                  type="text"
                  maxlength="6"
                  placeholder="123456"
                  class="totp-input"
                  autocomplete="one-time-code"
                />
              </div>

              <div class="modal-actions mt-4">
                <button
                  @click="activar2FA"
                  class="btn btn--primary btn--full"
                  :disabled="codigoTOTP.length !== 6 || cargando2FA"
                >
                  {{ cargando2FA ? 'Verificando...' : 'Confirmar y Activar 2FA' }}
                </button>
              </div>
            </div>
          </template>

          <!-- Caso: Desactivar 2FA -->
          <template v-else>
            <p>
              Para desactivar la protección 2FA de tu cuenta, ingresa tu código actual de 6 dígitos:
            </p>
            <div class="form-group mt-3">
              <input
                v-model="codigoTOTP"
                type="text"
                maxlength="6"
                placeholder="123456"
                class="totp-input"
                autocomplete="one-time-code"
              />
            </div>
            <div class="modal-actions mt-4">
              <button
                @click="desactivar2FA"
                class="btn btn--outline btn--full"
                :disabled="codigoTOTP.length !== 6 || cargando2FA"
              >
                {{ cargando2FA ? 'Procesando...' : 'Desactivar 2FA' }}
              </button>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-view {
  min-height: calc(100vh - 120px);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--color-border);
}

.profile-avatar {
  width: 75px;
  height: 75px;
  background: var(--color-primary-light);
  color: var(--color-primary-dark);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  box-shadow: var(--shadow-sm);
  flex-shrink: 0;
}

.profile-title-group h1 {
  margin-bottom: 0.25rem;
}

.profile-subtitle {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.user-email {
  color: var(--color-text-muted);
  font-size: 0.95rem;
}

.badge {
  display: inline-block;
  padding: 0.2rem 0.65rem;
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge--admin {
  background: #fde8e8;
  color: #9b1c1c;
}

.badge--cajero {
  background: #feecdc;
  color: #b43403;
}

.badge--cliente {
  background: #e1effe;
  color: #1e429f;
}

.profile-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}

.profile-card {
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  background: var(--color-bg-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--color-border);
}

.card-header h3 {
  font-size: 1.15rem;
  margin: 0;
}

.card-header-link {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-primary);
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0;
  border-bottom: 1px dashed var(--color-border);
  font-size: 0.95rem;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  color: var(--color-text-muted);
}

.info-value {
  color: var(--color-text-main);
  text-align: right;
}

.font-mono {
  font-family: monospace;
  font-size: 0.85rem;
}

.rewards-summary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.metric-box {
  background: var(--color-bg-base);
  border-radius: var(--radius-md);
  padding: 1rem;
  text-align: center;
  border: 1px solid var(--color-border);
}

.metric-value {
  display: block;
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--color-primary-dark);
}

.metric-label {
  font-size: 0.85rem;
  color: var(--color-text-muted);
}

.stamps-card {
  background: var(--color-bg-base);
  border-radius: var(--radius-md);
  padding: 1.2rem;
  border: 1px dashed var(--color-primary-light);
}

.stamps-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  font-size: 0.85rem;
  font-weight: 600;
}

.stamps-header small {
  color: var(--color-primary);
  font-weight: 500;
}

.stamps-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
}

.stamp-slot {
  aspect-ratio: 1;
  border-radius: var(--radius-md);
  background: var(--color-bg-surface);
  border: 2px dashed var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 700;
  transition: all var(--transition-fast);
}

.stamp-slot--filled {
  background: var(--color-primary-light);
  border: 2px solid var(--color-primary);
  box-shadow: 0 2px 4px rgba(224, 122, 95, 0.2);
}

.stamp-slot--reward {
  border-color: #f59e0b;
}

.stamp-slot--reward.stamp-slot--filled {
  background: #fef3c7;
  border-color: #d97706;
}

.stamp-empty {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  opacity: 0.6;
}

.security-status-box {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  background: var(--color-bg-base);
  padding: 1rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  margin-bottom: 1.25rem;
}

.security-icon {
  font-size: 1.8rem;
  line-height: 1;
}

.security-details strong {
  display: block;
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
}

.security-details p {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  margin: 0;
}

.quick-links {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.quick-link-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.85rem 1rem;
  background: var(--color-bg-base);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-main);
  text-decoration: none;
  transition: all var(--transition-fast);
  cursor: pointer;
  text-align: left;
}

.quick-link-btn span {
  font-size: 1.4rem;
}

.quick-link-btn strong {
  display: block;
  font-size: 0.95rem;
}

.quick-link-btn small {
  color: var(--color-text-muted);
  font-size: 0.8rem;
}

.quick-link-btn:hover {
  border-color: var(--color-primary);
  transform: translateX(4px);
  background: #fff;
}

.quick-link-btn--danger {
  width: 100%;
  border-color: #fca5a5;
  background: #fff5f5;
}

.quick-link-btn--danger:hover {
  background: #fee2e2;
  border-color: #ef4444;
}

/* Modal 2FA */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  padding: 1.5rem;
  backdrop-filter: blur(4px);
}

.modal-card {
  background: var(--color-bg-surface);
  border-radius: var(--radius-lg);
  max-width: 480px;
  width: 100%;
  padding: 2rem;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--color-border);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-close {
  background: transparent;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: var(--color-text-muted);
}

.qr-container {
  display: flex;
  justify-content: center;
  margin: 1.5rem 0;
}

.qr-container img {
  width: 180px;
  height: 180px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.secret-box {
  background: var(--color-bg-base);
  padding: 0.75rem;
  border-radius: var(--radius-md);
  text-align: center;
  font-family: monospace;
  font-size: 0.9rem;
  border: 1px dashed var(--color-border);
  user-select: all;
}

.totp-input {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1.5rem;
  letter-spacing: 0.5rem;
  text-align: center;
  border-radius: var(--radius-md);
  border: 2px solid var(--color-border);
  font-family: monospace;
}

.totp-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.alert {
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.alert--success {
  background: #def7ec;
  color: #03543f;
}

.alert--error {
  background: #fde8e8;
  color: #9b1c1c;
}

@media (max-width: 900px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
}
</style>
