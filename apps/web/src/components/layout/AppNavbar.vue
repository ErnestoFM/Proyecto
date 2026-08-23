<script setup lang="ts">
import { RouterLink } from 'vue-router';
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore';

const auth = useAuthStore();
const menuOpen = ref(false);

function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}

function closeMenu() {
  menuOpen.value = false;
}
</script>

<template>
  <header class="navbar">
    <div class="container navbar__inner">
      <!-- Marca / Logo -->
      <RouterLink to="/" class="navbar__brand" @click="closeMenu">
        <span class="navbar__logo">☕</span>
        <span class="navbar__name">Monchis<strong>Café</strong></span>
      </RouterLink>

      <!-- Menú Desktop -->
      <nav class="navbar__desktop-links">
        <RouterLink to="/" class="nav-link">Inicio</RouterLink>
        <RouterLink to="/menu" class="nav-link">Menú</RouterLink>
        <RouterLink to="/rewards" class="nav-link nav-link--rewards">Rewards</RouterLink>
        <RouterLink to="/nosotros" class="nav-link">Nosotros</RouterLink>
        <RouterLink to="/contacto" class="nav-link">Contacto</RouterLink>
      </nav>

      <!-- Acciones (Login / Perfil) y Botón Hamburguesa -->
      <div class="navbar__actions">
        <template v-if="auth.isAuthenticated">
          <RouterLink v-if="auth.user?.rol === 'ADMIN'" to="/admin" class="btn btn--secondary btn--sm desktop-only">Admin</RouterLink>
          <RouterLink v-if="auth.user?.rol === 'CAJERO' || auth.user?.rol === 'ADMIN'" to="/pos" class="btn btn--primary btn--sm desktop-only">POS</RouterLink>
          <RouterLink to="/perfil" class="navbar__user desktop-only">
            <span class="user-avatar">👤</span>
            <span class="user-name">{{ auth.user?.nombre }}</span>
          </RouterLink>
          <button @click="auth.logout()" class="btn btn--outline btn--sm desktop-only">Salir</button>
        </template>
        <template v-else>
          <RouterLink to="/login" class="btn btn--primary btn--sm desktop-only">Iniciar Sesión</RouterLink>
        </template>

        <!-- Botón Hamburguesa Móvil (icono que rota / cambia a ✕) -->
        <button
          class="navbar__toggle"
          @click="toggleMenu"
          :aria-label="menuOpen ? 'Cerrar menú de navegación' : 'Abrir menú de navegación'"
        >
          <span v-if="!menuOpen" class="hamburger-icon">☰</span>
          <span v-else class="close-icon">✕</span>
        </button>
      </div>
    </div>

    <!-- Menú Desplegable Lateral / Móvil -->
    <transition name="slide-menu">
      <div v-if="menuOpen" class="navbar__mobile-drawer">
        <div class="drawer-header">
          <div class="drawer-brand">
            <span class="navbar__logo">☕</span>
            <span class="navbar__name">Monchis<strong>Café</strong></span>
          </div>
          <!-- Botón de Cerrar Dedicado y Visible ✕ -->
          <button class="drawer-close-btn" @click="closeMenu" aria-label="Cerrar menú">
            ✕
          </button>
        </div>

        <nav class="drawer-links">
          <RouterLink to="/" class="drawer-link" @click="closeMenu">
            <span>🏠</span> Inicio
          </RouterLink>
          <RouterLink to="/menu" class="drawer-link" @click="closeMenu">
            <span>☕</span> Menú & Bebidas
          </RouterLink>
          <RouterLink to="/rewards" class="drawer-link drawer-link--rewards" @click="closeMenu">
            <span>🎁</span> Monchis Rewards
          </RouterLink>
          <RouterLink to="/nosotros" class="drawer-link" @click="closeMenu">
            <span>📖</span> Nuestra Historia
          </RouterLink>
          <RouterLink to="/contacto" class="drawer-link" @click="closeMenu">
            <span>📍</span> Contacto & Horarios
          </RouterLink>
          <RouterLink to="/legal" class="drawer-link" @click="closeMenu">
            <span>⚖️</span> Legal & Cookies
          </RouterLink>
        </nav>

        <div class="drawer-footer">
          <template v-if="auth.isAuthenticated">
            <RouterLink v-if="auth.user?.rol === 'ADMIN'" to="/admin" class="btn btn--secondary btn--full" @click="closeMenu">Panel Admin</RouterLink>
            <RouterLink v-if="auth.user?.rol === 'CAJERO' || auth.user?.rol === 'ADMIN'" to="/pos" class="btn btn--primary btn--full" @click="closeMenu">Punto de Venta (POS)</RouterLink>
            <button @click="auth.logout(); closeMenu()" class="btn btn--outline btn--full">Cerrar Sesión</button>
          </template>
          <template v-else>
            <RouterLink to="/login" class="btn btn--primary btn--full" @click="closeMenu">Iniciar Sesión</RouterLink>
            <RouterLink to="/registro" class="btn btn--secondary btn--full" @click="closeMenu">Crear Cuenta</RouterLink>
          </template>
        </div>
      </div>
    </transition>

    <!-- Overlay oscuro para cerrar al hacer clic afuera -->
    <div v-if="menuOpen" class="drawer-backdrop" @click="closeMenu"></div>
  </header>
</template>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(250, 243, 237, 0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border);
  padding: 0.8rem 0;
}

.navbar__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar__brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: var(--color-text-main);
}

.navbar__logo {
  font-size: 1.8rem;
}

.navbar__name {
  font-family: var(--font-heading);
  font-size: 1.4rem;
  font-weight: 400;
  color: var(--color-secondary-dark);
}

.navbar__name strong {
  color: var(--color-primary-dark);
  font-weight: 700;
}

/* Enlaces Desktop */
.navbar__desktop-links {
  display: flex;
  align-items: center;
  gap: 1.8rem;
}

.nav-link {
  font-family: var(--font-body);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--color-text-muted);
  text-decoration: none;
  transition: color var(--transition-fast);
  position: relative;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--color-primary-dark);
}

.nav-link--rewards {
  color: var(--color-primary-dark);
  font-weight: 700;
}

.navbar__actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.navbar__user {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.9rem;
  font-weight: 600;
}

/* Botón Hamburguesa */
.navbar__toggle {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.4rem;
  font-size: 1.8rem;
  color: var(--color-text-main);
  line-height: 1;
  border-radius: var(--radius-sm);
}

.close-icon {
  color: var(--color-primary-dark);
  font-weight: bold;
}

/* Drawer / Menú Lateral Móvil */
.navbar__mobile-drawer {
  position: fixed;
  top: 0;
  right: 0;
  width: 82%;
  max-width: 320px;
  height: 100vh;
  background: var(--color-bg-surface);
  box-shadow: -4px 0 20px rgba(74, 59, 50, 0.2);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  padding: 1.8rem;
  overflow-y: auto;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1.2rem;
  border-bottom: 1px solid var(--color-border);
  margin-bottom: 1.5rem;
}

.drawer-brand {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.drawer-close-btn {
  background: var(--color-bg-base);
  border: 1px solid var(--color-border);
  font-size: 1.4rem;
  font-weight: bold;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary-dark);
  transition: all var(--transition-fast);
}

.drawer-close-btn:hover {
  background: var(--color-primary);
  color: #fff;
}

.drawer-links {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  flex: 1;
}

.drawer-link {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem 1rem;
  border-radius: var(--radius-md);
  color: var(--color-text-main);
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: all var(--transition-fast);
}

.drawer-link:hover,
.drawer-link.router-link-active {
  background: rgba(243, 201, 201, 0.25);
  color: var(--color-primary-dark);
}

.drawer-link--rewards {
  color: var(--color-primary-dark);
  font-weight: 700;
}

.drawer-footer {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-border);
}

.btn--full {
  width: 100%;
  text-align: center;
}

/* Backdrop */
.drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(74, 59, 50, 0.4);
  backdrop-filter: blur(4px);
  z-index: 999;
}

/* Animaciones del Drawer */
.slide-menu-enter-active,
.slide-menu-leave-active {
  transition: transform 0.3s ease-in-out;
}

.slide-menu-enter-from,
.slide-menu-leave-to {
  transform: translateX(100%);
}

/* Responsividad */
@media (max-width: 860px) {
  .navbar__desktop-links {
    display: none; /* Ocultar links horizontales para que no se encimen */
  }

  .desktop-only {
    display: none;
  }

  .navbar__toggle {
    display: block; /* Mostrar botón hamburguesa */
  }
}
</style>
