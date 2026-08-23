<script setup lang="ts">
const valores = [
  {
    icono: '🤝',
    titulo: 'Trato Directo y Precio Justo',
    descripcion:
      'Pagamos hasta un 40% por encima del precio internacional a nuestros productores asociados, garantizando que el fruto de su esfuerzo se quede en sus hogares.',
  },
  {
    icono: '🌿',
    titulo: 'Cultivo Bajo Sombra & Biodiversidad',
    descripcion:
      'Nuestros cafetales conviven en armonía con la flora y fauna nativa de la sierra. Sin pesticidas sintéticos ni deforestación.',
  },
  {
    icono: '♻️',
    titulo: 'Economía Circular y Empatía',
    descripcion:
      'Desde el compostaje de la pulpa y la borra de café hasta la premiación con doble sello a quien lleva su termo reutilizable.',
  },
];

const estadisticas = [
  { numero: '14+', etiqueta: 'Familias Productoras' },
  { numero: '100%', etiqueta: 'Granos Orgánicos Trazables' },
  { numero: '0g', etiqueta: 'Pesticidas Sintéticos' },
  { numero: '1,200+', etiqueta: 'Termos Reutilizados' },
];
</script>

<template>
  <div class="about-page">
    <!-- Hero Editorial -->
    <section class="about-hero">
      <div class="container text-center" v-motion-slide-bottom>
        <span class="badge badge--organic">🌱 Nuestras Raíces</span>
        <h1>El Café no es solo una bebida,<br /><span class="about-hero__highlight">es la historia de una familia</span>.</h1>
        <p class="about-hero__lead">
          Monchis Café nació en un pequeño rancho con una promesa sencilla: honrar el trabajo de la tierra y servir café honesto, cálido y sin prisas.
        </p>
      </div>
    </section>

    <!-- La Historia Conmovedora -->
    <section class="section">
      <div class="container story-container">
        <div class="story-grid">
          <div class="story-text" v-motion-slide-left>
            <span class="badge badge--commercial">📖 El Comienzo</span>
            <h2>De la cocina del abuelo a tu taza diaria</h2>
            <p>
              Todo comenzó con las mañanas de neblina en el campo. Recordamos el fogón de leña encendido antes del amanecer, la cafetera de peltre y el aroma a canela y piloncillo que llenaba cada rincón de la casa. El abuelo solía decir: <em>"Quien respeta la tierra, recibe el mejor grano; y quien comparte su mesa, nunca está solo."</em>
            </p>
            <p>
              Durante años vimos cómo los grandes intermediarios pagaban centavos por el grano de altura que a los campesinos les tomaba meses cosechar a mano en pendientes empinadas. Decidimos que las cosas tenían que cambiar.
            </p>
            <p>
              <strong>Monchis Café</strong> nació para cerrar esa brecha. Un puente cálido entre las manos que cosechan bajo el sol de Chiapas y Oaxaca, y tu taza humeante de cada mañana.
            </p>
          </div>

          <div class="story-card card" v-motion-slide-right>
            <span class="story-emoji">🏡</span>
            <blockquote>
              "No queríamos abrir una cafetería más; queríamos crear un refugio donde cada sorbo te haga sentir bienvenido y donde cada compra apoye el sustento digno de una familia campesina."
            </blockquote>
            <cite>— Familia Monchis Café</cite>
          </div>
        </div>
      </div>
    </section>

    <!-- Por Qué Consumir Local y Orgánico -->
    <section class="section section--alt">
      <div class="container">
        <div class="section-header text-center" v-motion-fade-visible>
          <span class="badge badge--organic">🌎 El Valor de lo Nuestro</span>
          <h2>¿Por Qué Elegir Café Orgánico y Consumir Local?</h2>
          <p class="section__subtitle">
            Cada vez que eliges una taza en Monchis Café, estás tomando una postura consciente por la salud de tu cuerpo y el futuro de nuestra comunidad.
          </p>
        </div>

        <div class="values-grid">
          <div v-for="val in valores" :key="val.titulo" class="card value-card" v-motion-slide-visible-bottom>
            <span class="value-icon">{{ val.icono }}</span>
            <h3>{{ val.titulo }}</h3>
            <p>{{ val.descripcion }}</p>
          </div>
        </div>

        <!-- Estadísticas de Impacto -->
        <div class="stats-row card" v-motion-slide-visible-bottom>
          <div v-for="stat in estadisticas" :key="stat.etiqueta" class="stat-item">
            <h2>{{ stat.numero }}</h2>
            <p>{{ stat.etiqueta }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Manifiesto & Invitación -->
    <section class="section manifesto-section">
      <div class="container text-center" v-motion-fade-visible>
        <span class="badge badge--commercial">🌿 Nuestro Compromiso</span>
        <h2>La Mesa Siempre Está Puesta para Ti</h2>
        <p class="manifesto-lead">
          Pasa, siéntate, pide tu café favorito y tómate cinco minutos para respirar. En Monchis Café eres bienvenido tal como eres.
        </p>
        <div class="manifesto-actions">
          <RouterLink to="/menu" class="btn btn--primary">Ver Nuestro Menú ☕</RouterLink>
          <RouterLink to="/contacto" class="btn btn--secondary">Visítanos Hoy 📍</RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.about-page {
  background: var(--color-bg-base);
  overflow-x: hidden;
}

.about-hero {
  padding: 5rem 0 3rem;
  background: linear-gradient(135deg, rgba(243, 201, 201, 0.2), var(--color-bg-base));
}

.about-hero h1 {
  font-size: 2.6rem;
  line-height: 1.3;
  margin: 1rem 0 1.2rem;
}

.about-hero__highlight {
  color: var(--color-primary-dark);
}

.about-hero__lead {
  max-width: 65ch;
  margin: 0 auto;
  font-size: 1.15rem;
  line-height: 1.8;
  color: var(--color-text-muted);
}

.story-grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 3.5rem;
  align-items: center;
}

.story-text h2 {
  font-size: 2rem;
  margin: 0.6rem 0 1.2rem;
}

.story-text p {
  font-size: 1rem;
  line-height: 1.8;
  margin-bottom: 1.2rem;
  color: var(--color-text-muted);
}

.story-text em {
  color: var(--color-secondary-dark);
  font-weight: 600;
}

.story-card {
  padding: 3rem 2.5rem;
  background: linear-gradient(135deg, var(--color-bg-surface), rgba(243, 201, 201, 0.15));
  border-left: 4px solid var(--color-primary-dark);
  text-align: center;
}

.story-emoji {
  font-size: 4rem;
  display: block;
  margin-bottom: 1.2rem;
}

.story-card blockquote {
  font-style: italic;
  font-size: 1.1rem;
  line-height: 1.8;
  color: var(--color-text-main);
  margin-bottom: 1.2rem;
}

.story-card cite {
  font-family: var(--font-heading);
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--color-primary-dark);
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-bottom: 3rem;
}

.value-card {
  padding: 2.2rem 1.8rem;
  text-align: center;
}

.value-icon {
  font-size: 2.8rem;
  display: block;
  margin-bottom: 1rem;
}

.value-card h3 {
  font-size: 1.2rem;
  margin-bottom: 0.8rem;
}

.value-card p {
  font-size: 0.9rem;
  line-height: 1.7;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  padding: 2.5rem;
  text-align: center;
  background: var(--color-bg-surface);
}

.stat-item h2 {
  font-size: 2.2rem;
  color: var(--color-primary-dark);
  margin-bottom: 0.3rem;
}

.stat-item p {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.manifesto-section {
  background: linear-gradient(135deg, rgba(243, 201, 201, 0.2), rgba(201, 168, 139, 0.15));
}

.manifesto-section h2 {
  font-size: 2.2rem;
  margin: 0.6rem 0 1rem;
}

.manifesto-lead {
  max-width: 55ch;
  margin: 0 auto 2rem;
  font-size: 1.1rem;
  line-height: 1.8;
}

.manifesto-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

@media (max-width: 900px) {
  .story-grid {
    grid-template-columns: 1fr;
  }
  .values-grid {
    grid-template-columns: 1fr;
  }
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
  }
}

@media (max-width: 600px) {
  .about-hero h1 {
    font-size: 1.9rem;
  }
  .stats-row {
    grid-template-columns: 1fr;
  }
}
</style>
