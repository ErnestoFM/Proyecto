<script setup lang="ts">
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

const auth = useAuthStore();
const router = useRouter();
const route = useRoute();

const nombre = ref('');
const email = ref('');
const password = ref('');
const aceptaTerminos = ref(false);
const recaptchaToken = ref('test-valid-recaptcha-token'); // TODO: Integrar widget reCAPTCHA real

// Capturar parámetros UTM de la URL
const utmSource = (route.query.utm_source as string) || undefined;
const utmMedium = (route.query.utm_medium as string) || undefined;
const utmCampaign = (route.query.utm_campaign as string) || undefined;

async function handleRegister() {
  const success = await auth.register(
    nombre.value,
    email.value,
    password.value,
    recaptchaToken.value,
    { source: utmSource, medium: utmMedium, campaign: utmCampaign }
  );
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
          <span class="auth-card__emoji">🌿</span>
          <h1>Únete a Monchis Café</h1>
          <p>Crea tu cuenta y comienza a acumular Monchis Rewards</p>
        </div>

        <form @submit.prevent="handleRegister" class="auth-card__form">
          <div class="form-group">
            <label for="reg-nombre">Nombre Completo</label>
            <input id="reg-nombre" v-model="nombre" type="text" placeholder="Tu nombre" required autocomplete="name" />
          </div>

          <div class="form-group">
            <label for="reg-email">Correo Electrónico</label>
            <input id="reg-email" v-model="email" type="email" placeholder="tu@correo.com" required autocomplete="email" />
          </div>

          <div class="form-group">
            <label for="reg-password">Contraseña</label>
            <input id="reg-password" v-model="password" type="password" placeholder="Mínimo 8 caracteres" required minlength="8" autocomplete="new-password" />
          </div>

          <div class="form-group legal-consent">
            <label class="consent-label">
              <input v-model="aceptaTerminos" type="checkbox" required />
              <span>
                He leído y acepto los <RouterLink to="/legal?tab=terminos" target="_blank">Términos y Condiciones</RouterLink> y el <RouterLink to="/legal?tab=privacidad" target="_blank">Aviso de Privacidad</RouterLink> de Monchis Café.
              </span>
            </label>
          </div>

          <div class="recaptcha-placeholder">
            <small>🛡️ Protegido por Google reCAPTCHA</small>
          </div>

          <p v-if="auth.error" class="error-message">{{ auth.error }}</p>

          <button type="submit" class="btn btn--primary auth-card__submit" :disabled="auth.isLoading || !aceptaTerminos">
            {{ auth.isLoading ? 'Creando cuenta...' : 'Registrarme' }}
          </button>
        </form>

        <div class="auth-card__footer">
          <p>¿Ya tienes cuenta? <RouterLink to="/login">Inicia sesión</RouterLink></p>
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

.auth-card__header { text-align: center; margin-bottom: 2rem; }
.auth-card__emoji { font-size: 3rem; display: block; margin-bottom: 0.8rem; }
.auth-card__header h1 { font-size: 1.6rem; margin-bottom: 0.3rem; }
.auth-card__header p { color: var(--color-text-muted); font-size: 0.95rem; margin: 0 auto; }
.auth-card__submit { width: 100%; margin-top: 0.5rem; }

.recaptcha-placeholder {
  text-align: center;
  padding: 0.8rem;
  background: rgba(243, 201, 201, 0.15);
  border-radius: var(--radius-sm);
  margin-bottom: 1rem;
}
.recaptcha-placeholder small { color: var(--color-text-muted); font-size: 0.8rem; }

.auth-card__footer { text-align: center; margin-top: 1.5rem; font-size: 0.9rem; }
.auth-card__footer a { font-weight: 600; }
</style>
