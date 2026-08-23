<script setup lang="ts">
import PhotoCarousel from '@/components/common/PhotoCarousel.vue';
</script>

<template>
  <div>
    <!-- Hero Section con la estructura original limpia -->
    <section class="hero">
      <div class="container hero__inner">
        <div class="hero__text" v-motion-slide-left :delay="200">
          <span class="badge badge--organic">☕ Café Orgánico de Especialidad</span>
          <h1>Bienvenido a <span class="hero__highlight">Monchis</span>Café</h1>
          <p class="hero__subtitle">
            Cada taza cuenta una historia. Café orgánico trazable de proveedores regionales,
            servido con cariño en un rincón cálido y acogedor.
          </p>
          <div class="hero__actions">
            <RouterLink to="/menu" class="btn btn--primary">Explora Nuestro Menú</RouterLink>
            <RouterLink to="/nosotros" class="btn btn--secondary">Conócenos</RouterLink>
          </div>
        </div>

        <div class="hero__visual" v-motion-slide-right :delay="400">
          <div class="hero__coffee-circle">
            <span class="hero__emoji">☕</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Carrusel Visual de Comercio Justo y Producto -->
    <section class="section" style="padding-top: 2rem; padding-bottom: 2rem;">
      <div class="container">
        <PhotoCarousel />
      </div>
    </section>

    <!-- Bloques Split Estilo Editorial / Rewards Showcase (Inspiración Visual) -->
    <section class="section">
      <div class="container feature-splits">
        <!-- Bloque 1: Juntémonos más -->
        <div class="split-row card" v-motion-slide-visible-bottom>
          <div class="split-img">
            <img src="/feature1.jpg" alt="Amigos compartiendo café en Monchis Café" />
          </div>
          <div class="split-info block-coffee">
            <span class="split-badge">COMUNIDAD & AMISTAD</span>
            <h2>Juntémonos Más</h2>
            <p>Los mejores momentos también se improvisan con una buena taza de café y pan recién horneado.</p>
            <RouterLink to="/menu" class="split-btn">Explora nuestras bebidas →</RouterLink>
          </div>
        </div>

        <!-- Bloque 2: Trae tu termo (Invertido) -->
        <div class="split-row card reverse" v-motion-slide-visible-bottom>
          <div class="split-info block-sage">
            <span class="split-badge">🌿 CONSUMO RESPONSABLE</span>
            <h2>Trae Tu Termo, Gana Doble</h2>
            <p>Un pequeño gesto diario que cuida la sierra. Recibe <strong>+1 sello ecológico de regalo</strong> en cada café para completar tu tarjeta más rápido.</p>
            <RouterLink to="/rewards" class="split-btn">Conoce Monchis Rewards →</RouterLink>
          </div>
          <div class="split-img">
            <img src="/feature2.jpg" alt="Termo reutilizable para café de especialidad" />
          </div>
        </div>

        <!-- Bloque 3: Pide, Acumula y Disfruta -->
        <div class="split-row card" v-motion-slide-visible-bottom>
          <div class="split-img">
            <img src="/feature3.jpg" alt="Recompensas y cashback en Monchis Café" />
          </div>
          <div class="split-info block-terracotta">
            <span class="split-badge">PUNTOS & MONEDERO</span>
            <h2>Pide, Acumula y Disfruta</h2>
            <p>Únete a nuestro programa gratuito. Disfruta tu 8vo café de regalo y 5% de cashback en monedero digital en cada visita.</p>
            <RouterLink to="/registro" class="split-btn">¡Regístrate y empieza hoy! →</RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Valores Section -->
    <section class="section section--alt">
      <div class="container">
        <h2 class="text-center" v-motion-fade-visible>Lo que nos hace especiales</h2>
        <p class="text-center section__subtitle" v-motion-fade-visible :delay="100">
          En Monchis Café, cada grano tiene nombre y cada taza tiene propósito.
        </p>
        <div class="values-grid">
          <div class="card values__card" v-motion-slide-visible-bottom :delay="200">
            <span class="values__icon">🌿</span>
            <h3>Trazabilidad Orgánica</h3>
            <p>Conoce el origen exacto de tu café: finca, lote, fecha de tostado y proveedor regional.</p>
          </div>
          <div class="card values__card" v-motion-slide-visible-bottom :delay="350">
            <span class="values__icon">🎁</span>
            <h3>Monchis Rewards</h3>
            <p>Acumula sellos por cada café y gana tu 8vo gratis. Trae tu termo y gana doble.</p>
          </div>
          <div class="card values__card" v-motion-slide-visible-bottom :delay="500">
            <span class="values__icon">🌎</span>
            <h3>Consumo Responsable</h3>
            <p>Comprometidos con la producción sostenible y el desarrollo de comunidades rurales.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="section cta-section">
      <div class="container text-center" v-motion-fade-visible>
        <h2>¿Listo para probar el mejor café orgánico?</h2>
        <p class="section__subtitle">Visítanos o únete a nuestro programa de lealtad hoy.</p>
        <div class="cta-actions">
          <RouterLink to="/registro" class="btn btn--primary">Crear mi Cuenta</RouterLink>
          <RouterLink to="/contacto" class="btn btn--secondary">Encontrar la Cafetería</RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero {
  padding: 6rem 0 4rem;
  background: linear-gradient(135deg, var(--color-bg-base) 0%, rgba(243, 201, 201, 0.15) 100%);
  overflow: hidden;
}

.hero__inner {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  align-items: center;
  gap: 3rem;
}

.hero__text {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.hero__highlight {
  color: var(--color-primary-dark);
}

.hero__subtitle {
  font-size: 1.15rem;
  line-height: 1.8;
  max-width: 50ch;
}

.hero__actions {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.hero__visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.hero__coffee-circle {
  width: 320px;
  height: 320px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-lg);
  animation: float 6s ease-in-out infinite;
}

.hero__emoji {
  font-size: 8rem;
  filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.15));
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-16px);
  }
}

.section__subtitle {
  margin: 0.8rem auto 2.5rem;
  font-size: 1.05rem;
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.values__card {
  text-align: center;
  padding: 2.5rem 1.5rem;
}

.values__icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

.values__card h3 {
  margin-bottom: 0.6rem;
}

.cta-section {
  background: linear-gradient(135deg, rgba(243, 201, 201, 0.2), rgba(201, 168, 139, 0.15));
}

.cta-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

@media (max-width: 768px) {
  .hero__inner {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero__actions {
    justify-content: center;
    flex-wrap: wrap;
  }

  .hero__coffee-circle {
    width: 240px;
    height: 240px;
    padding: 1.8rem;
  }

  .values-grid {
    grid-template-columns: 1fr;
  }

  .cta-actions {
    flex-direction: column;
    align-items: center;
  }
}
/* Bloques Split Estilo Editorial */
.feature-splits {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.split-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: 0;
  overflow: hidden;
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-md);
}

.split-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  min-height: 360px;
  display: block;
}

.split-info {
  padding: 3.5rem 4rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 1rem;
  color: #fff;
}

.split-badge {
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.split-info h2 {
  font-size: 2.2rem;
  line-height: 1.25;
  color: #fff;
}

.split-info p {
  font-size: 1.05rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.92);
}

.split-btn {
  font-weight: 700;
  font-size: 0.95rem;
  margin-top: 0.5rem;
  color: #FAF3ED;
  text-decoration: underline;
  display: inline-flex;
  align-items: center;
  transition: transform var(--transition-fast);
}

.split-btn:hover {
  transform: translateX(4px);
}

.block-coffee {
  background: #C9A88B; /* Café con leche */
}

.block-sage {
  background: #8C6B52; /* Café tostado cálido */
}
.block-sage .split-badge {
  color: #F3C9C9;
}

.block-terracotta {
  background: #D98C7F; /* Rosa terracota */
}

@media (max-width: 900px) {
  .split-row {
    grid-template-columns: 1fr;
  }
  .split-row.reverse {
    display: flex;
    flex-direction: column-reverse;
  }
  .split-info {
    padding: 2.5rem 1.8rem;
  }
  .split-info h2 {
    font-size: 1.8rem;
  }
}
</style>
