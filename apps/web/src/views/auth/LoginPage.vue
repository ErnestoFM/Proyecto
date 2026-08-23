<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

const auth = useAuthStore();
const router = useRouter();

const email = ref('');
const password = ref('');
const recaptchaToken = ref('test-valid-recaptcha-token'); // TODO: Integrar widget reCAPTCHA real

async function handleLogin() {
  const success = await auth.login(email.value, password.value, recaptchaToken.value);
  if (success) {
    router.push('/dashboard');
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="container">
      <div class="auth-card card" v-motion-slide-visible-bottom>
        <div class="auth-card__header">
          <span class="auth-card__emoji">☕</span>
          <h1>Bienvenido de Vuelta</h1>
          <p>Ingresa a tu cuenta de Monchis Café</p>
        </div>

        <form @submit.prevent="handleLogin" class="auth-card__form">
          <div class="form-group">
            <label for="login-email">Correo Electrónico</label>
            <input
              id="login-email"
              v-model="email"
              type="email"
              placeholder="tu@correo.com"
              required
              autocomplete="email"
            />
          </div>

          <div class="form-group">
            <label for="login-password">Contraseña</label>
            <input
              id="login-password"
              v-model="password"
              type="password"
              placeholder="••••••••"
              required
              autocomplete="current-password"
            />
          </div>

          <!-- TODO: Insertar widget de Google reCAPTCHA aquí -->
          <div class="recaptcha-placeholder">
            <small>🛡️ Protegido por Google reCAPTCHA</small>
          </div>

          <p v-if="auth.error" class="error-message">{{ auth.error }}</p>

          <button type="submit" class="btn btn--primary auth-card__submit" :disabled="auth.isLoading">
            {{ auth.isLoading ? 'Verificando...' : 'Iniciar Sesión' }}
          </button>
        </form>

        <div class="auth-card__footer">
          <p>¿No tienes cuenta? <RouterLink to="/registro">Regístrate aquí</RouterLink></p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
  padding: 3rem 0;
}

.auth-card {
  max-width: 440px;
  margin: 0 auto;
  padding: 2.5rem;
}

.auth-card__header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-card__emoji {
  font-size: 3rem;
  display: block;
  margin-bottom: 0.8rem;
}

.auth-card__header h1 {
  font-size: 1.6rem;
  margin-bottom: 0.3rem;
}

.auth-card__header p {
  color: var(--color-text-muted);
  font-size: 0.95rem;
  margin: 0 auto;
}

.auth-card__submit {
  width: 100%;
  margin-top: 0.5rem;
}

.recaptcha-placeholder {
  text-align: center;
  padding: 0.8rem;
  background: rgba(243, 201, 201, 0.15);
  border-radius: var(--radius-sm);
  margin-bottom: 1rem;
}

.recaptcha-placeholder small {
  color: var(--color-text-muted);
  font-size: 0.8rem;
}

.auth-card__footer {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
}

.auth-card__footer a {
  font-weight: 600;
}
</style>
