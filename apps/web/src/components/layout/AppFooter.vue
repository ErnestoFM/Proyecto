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
        <RouterLink to="/menu">Menú de Especialidad</RouterLink>
        <RouterLink to="/rewards">Monchis Rewards</RouterLink>
        <RouterLink to="/nosotros">Nuestra Historia</RouterLink>
        <RouterLink to="/contacto">Contacto & Ubicación</RouterLink>
      </nav>

      <nav class="footer__links">
        <h4>Legal & Comunidad</h4>
        <RouterLink to="/legal?tab=terminos">Términos y Condiciones</RouterLink>
        <RouterLink to="/legal?tab=privacidad">Aviso de Privacidad</RouterLink>
        <RouterLink to="/legal?tab=cookies">Ajustes de Cookies</RouterLink>
        <a href="https://instagram.com/monchiscafe" target="_blank" rel="noopener noreferrer">Instagram</a>
        <a href="https://facebook.com/monchiscafe" target="_blank" rel="noopener noreferrer">Facebook</a>
      </nav>

      <div class="footer__contact">
        <h4>Visítanos</h4>
        <p>📍 Av. Corredor Verde 1450, Tonalá / ZMG, Jalisco</p>
        <p>📧 <a href="mailto:hola@monchiscafe.com" style="color: inherit; text-decoration: underline;">hola@monchiscafe.com</a></p>
        <p>📱 <a href="tel:+523312345678" style="color: inherit; text-decoration: underline;">+52 (33) 1234-5678</a></p>
        <p>💬 <a href="https://wa.me/5213300000000" target="_blank" rel="noopener noreferrer" style="color: #25D366; font-weight: 700;">WhatsApp Directo →</a></p>
      </div>
    </div>

    <div class="footer__bottom">
      <div class="container footer__bottom-inner">
        <p>&copy; {{ new Date().getFullYear() }} Monchis Café — Café de Especialidad y Comercio Justo.</p>
        <div class="footer__bottom-links">
          <a href="/sitemap.xml" target="_blank" rel="noopener noreferrer">Sitemap XML</a>
          <span>·</span>
          <a href="/robots.txt" target="_blank" rel="noopener noreferrer">Robots.txt</a>
        </div>
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
  grid-template-columns: 1.5fr 1fr 1fr 1.2fr;
  gap: 2.5rem;
}

@media (max-width: 900px) {
  .footer__inner {
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
  }
}

@media (max-width: 550px) {
  .footer__inner {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}

.footer__brand { display: flex; flex-direction: column; gap: 0.5rem; }

.footer__logo { font-size: 2rem; }

.footer__logo-img {
  width: 44px;
  height: 44px;
  object-fit: contain;
}

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

.footer__bottom-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.footer__bottom p {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
}

.footer__bottom-links {
  display: flex;
  gap: 0.6rem;
  align-items: center;
  font-size: 0.85rem;
}

.footer__bottom-links a {
  color: rgba(255, 255, 255, 0.4);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.footer__bottom-links a:hover {
  color: var(--color-primary);
}

.footer__bottom-links span {
  color: rgba(255, 255, 255, 0.2);
}

@media (max-width: 768px) {
  .footer__bottom-inner {
    flex-direction: column;
    text-align: center;
  }
}
</style>
