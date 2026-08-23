<script setup lang="ts">
</script>

<template>
  <footer class="footer">
    <div class="container footer__inner">
      <div class="footer__brand">
        <span class="footer__logo">☕</span>
        <span class="footer__name">Monchis<strong>Café</strong></span>
        <p class="footer__tagline">Café orgánico de especialidad con alma de rancho.</p>
      </div>

      <nav class="footer__links">
        <h4>Navegación</h4>
        <RouterLink to="/">Inicio</RouterLink>
        <RouterLink to="/menu">Menú</RouterLink>
        <RouterLink to="/nosotros">Nosotros</RouterLink>
        <RouterLink to="/contacto">Contacto</RouterLink>
      </nav>

      <div class="footer__contact">
        <h4>Encuéntranos</h4>
        <p>📍 Zona rural/suburbana, México</p>
        <p>📧 hola@monchiscafe.com</p>
        <p>📱 +52 (XXX) XXX-XXXX</p>
      </div>
    </div>

    <div class="footer__bottom">
      <div class="container">
        <p>&copy; {{ new Date().getFullYear() }} Monchis Café — Hecho con ❤️ y café orgánico.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: var(--color-text-main);
  color: rgba(255, 255, 255, 0.8);
  padding: 3rem 0 0;
  margin-top: auto;
}

.footer__inner {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 3rem;
}

.footer__brand { display: flex; flex-direction: column; gap: 0.5rem; }

.footer__logo { font-size: 2rem; }

.footer__name {
  font-family: var(--font-heading);
  font-size: 1.3rem;
  color: var(--color-primary);
}
.footer__name strong { color: #fff; }

.footer__tagline {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.9rem;
  max-width: 30ch;
}

.footer__links,
.footer__contact {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.footer__links h4,
.footer__contact h4 {
  color: #fff;
  font-size: 1rem;
  margin-bottom: 0.3rem;
}

.footer__links a {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  transition: color var(--transition-fast);
}

.footer__links a:hover {
  color: var(--color-primary);
}

.footer__contact p {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
}

.footer__bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.2rem 0;
  margin-top: 2.5rem;
}

.footer__bottom p {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.4);
  text-align: center;
}

@media (max-width: 768px) {
  .footer__inner {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}
</style>
