<script setup lang="ts">
</script>

<template>
  <div>
    <!-- Hero Section -->
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

.hero__text { display: flex; flex-direction: column; gap: 1.2rem; }

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
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-16px); }
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
    width: 200px;
    height: 200px;
  }

  .hero__emoji { font-size: 5rem; }

  .values-grid {
    grid-template-columns: 1fr;
  }

  .cta-actions { flex-direction: column; align-items: center; }
}
</style>
