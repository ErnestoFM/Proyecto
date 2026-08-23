<script setup lang="ts">
import { RouterLink } from 'vue-router';
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore';

const auth = useAuthStore();
const menuOpen = ref(false);

function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}
</script>

<template>
  <header class="navbar">
    <div class="container navbar__inner">
      <RouterLink to="/" class="navbar__brand">
        <span class="navbar__logo">☕</span>
        <span class="navbar__name">Monchis<strong>Café</strong></span>
      </RouterLink>

      <button class="navbar__toggle" @click="toggleMenu" aria-label="Menú de navegación">
        <span :class="['navbar__hamburger', { open: menuOpen }]"></span>
      </button>

      <nav :class="['navbar__menu', { 'navbar__menu--open': menuOpen }]">
        <RouterLink to="/" class="navbar__link" @click="menuOpen = false">Inicio</RouterLink>
        <RouterLink to="/menu" class="navbar__link" @click="menuOpen = false">Menú</RouterLink>
        <RouterLink to="/nosotros" class="navbar__link" @click="menuOpen = false">Nosotros</RouterLink>
        <RouterLink to="/contacto" class="navbar__link" @click="menuOpen = false">Contacto</RouterLink>

        <template v-if="auth.isAuthenticated">
          <RouterLink to="/dashboard" class="navbar__link" @click="menuOpen = false">Panel</RouterLink>
          <button class="btn btn--ghost" @click="auth.logout(); menuOpen = false">Salir</button>
        </template>
        <template v-else>
          <RouterLink to="/login" class="btn btn--primary" @click="menuOpen = false">Iniciar Sesión</RouterLink>
        </template>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(250, 243, 237, 0.85);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
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

.navbar__logo-img {
  width: 38px;
  height: 38px;
  object-fit: contain;
  filter: drop-shadow(0 2px 4px rgba(74, 59, 50, 0.1));
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

.navbar__menu {
  display: flex;
  align-items: center;
  gap: 1.8rem;
}

.navbar__link {
  font-family: var(--font-body);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--color-text-muted);
  text-decoration: none;
  transition: color var(--transition-fast);
  position: relative;
}

.navbar__link::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--color-primary-dark);
  border-radius: var(--radius-full);
  transition: width var(--transition-normal);
}

.navbar__link:hover,
.navbar__link.router-link-active {
  color: var(--color-primary-dark);
}

.navbar__link:hover::after,
.navbar__link.router-link-active::after {
  width: 100%;
}

.navbar__toggle {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.navbar__hamburger {
  display: block;
  width: 24px;
  height: 2px;
  background: var(--color-text-main);
  border-radius: 2px;
  position: relative;
  transition: background var(--transition-fast);
}

.navbar__hamburger::before,
.navbar__hamburger::after {
  content: '';
  display: block;
  width: 24px;
  height: 2px;
  background: var(--color-text-main);
  border-radius: 2px;
  position: absolute;
  left: 0;
  transition: all var(--transition-normal);
}

.navbar__hamburger::before { top: -7px; }
.navbar__hamburger::after { top: 7px; }

.navbar__hamburger.open { background: transparent; }
.navbar__hamburger.open::before { top: 0; transform: rotate(45deg); }
.navbar__hamburger.open::after { top: 0; transform: rotate(-45deg); }

@media (max-width: 768px) {
  .navbar__toggle { display: block; }

  .navbar__menu {
    position: fixed;
    top: 0;
    right: -100%;
    width: 80%;
    max-width: 320px;
    height: 100vh;
    background: var(--color-bg-base);
    flex-direction: column;
    align-items: flex-start;
    padding: 5rem 2rem 2rem;
    gap: 1.5rem;
    box-shadow: var(--shadow-lg);
    transition: right var(--transition-smooth);
    z-index: 99;
  }

  .navbar__menu--open { right: 0; }
}
</style>
