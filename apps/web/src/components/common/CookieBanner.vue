<script setup lang="ts">
import { onMounted } from 'vue';
import { useCookieStore } from '@/stores/cookieStore';
import { RouterLink } from 'vue-router';

const cookieStore = useCookieStore();

onMounted(() => {
  cookieStore.cargarPreferencias();
});
</script>

<template>
  <div v-if="!cookieStore.haRespondido" class="cookie-banner" v-motion-slide-bottom>
    <div class="container cookie-banner__inner">
      <div class="cookie-banner__text">
        <span class="cookie-icon">🍪</span>
        <div>
          <h4>Tu Privacidad en Monchis Café</h4>
          <p>
            Utilizamos cookies para garantizar la seguridad de tu sesión, proteger transacciones y entender cómo nos conoces (ej. Google Maps o Instagram). Puedes ajustar tus preferencias o consultar nuestra
            <RouterLink to="/legal?tab=cookies">Política de Cookies</RouterLink>.
          </p>
        </div>
      </div>

      <div class="cookie-banner__actions">
        <button class="btn btn--primary btn--sm" @click="cookieStore.aceptarTodas">Aceptar Todas</button>
        <button class="btn btn--secondary btn--sm" @click="cookieStore.rechazarOpcionales">Solo Necesarias</button>
        <RouterLink to="/legal?tab=cookies" class="btn btn--ghost btn--sm">Personalizar</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cookie-banner {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(250, 243, 237, 0.96);
  backdrop-filter: blur(12px);
  border-top: 1px solid var(--color-border);
  box-shadow: 0 -4px 20px rgba(74, 59, 50, 0.1);
  padding: 1.2rem 0;
  z-index: 999;
}

.cookie-banner__inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.cookie-banner__text {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.cookie-icon {
  font-size: 2.2rem;
}

.cookie-banner__text h4 {
  font-size: 1rem;
  margin-bottom: 0.2rem;
}

.cookie-banner__text p {
  font-size: 0.85rem;
  line-height: 1.4;
  max-width: 60ch;
}

.cookie-banner__actions {
  display: flex;
  gap: 0.6rem;
  flex-shrink: 0;
}

@media (max-width: 860px) {
  .cookie-banner__inner {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  .cookie-banner__actions {
    width: 100%;
    justify-content: flex-end;
    flex-wrap: wrap;
  }
}
</style>
