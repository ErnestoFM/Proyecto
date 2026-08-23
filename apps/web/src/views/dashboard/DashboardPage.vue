<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore';

const auth = useAuthStore();
</script>

<template>
  <div class="section">
    <div class="container">
      <h1 v-motion-fade-visible>Panel de Control</h1>
      <p class="section__subtitle" v-motion-fade-visible :delay="100">
        Bienvenido, <strong>{{ auth.user?.nombre || 'Usuario' }}</strong>. Aquí puedes gestionar tus pedidos y recompensas.
      </p>

      <div class="dashboard-grid">
        <div class="card" v-motion-slide-visible-bottom :delay="200">
          <span class="dashboard__icon">☕</span>
          <h3>Mis Pedidos</h3>
          <p>Historial y estado de tus órdenes.</p>
        </div>
        <div class="card" v-motion-slide-visible-bottom :delay="350">
          <span class="dashboard__icon">🎁</span>
          <h3>Monchis Rewards</h3>
          <p>Sellos, puntos cashback y beneficios activos.</p>
        </div>
        <div class="card" v-motion-slide-visible-bottom :delay="500">
          <span class="dashboard__icon">👤</span>
          <h3>Mi Perfil</h3>
          <p>Datos personales y configuración de cuenta.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 2rem;
}

.dashboard__icon {
  font-size: 2.5rem;
  display: block;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
</style>
