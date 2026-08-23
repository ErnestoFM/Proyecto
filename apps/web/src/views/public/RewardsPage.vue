<script setup lang="ts">
import { ref, computed } from 'vue';

// Calculadora interactiva
const tazasSemana = ref(3);
const usaTermo = ref(true);

const sellosMes = computed(() => {
  const base = tazasSemana.value * 4;
  const eco = usaTermo.value ? tazasSemana.value * 4 : 0;
  return base + eco;
});

const cafesGratisMes = computed(() => Math.floor(sellosMes.value / 8));
const cashbackMes = computed(() => Math.floor(tazasSemana.value * 55 * 4 * 0.05));

const niveles = [
  {
    nivel: 'Grano Verde (Bienvenida)',
    icono: '🌱',
    requisito: 'Al registrarte gratis',
    beneficios: [
      'Tarjeta digital de 8 sellos en tu perfil',
      '1 sello por cada bebida preparada en barra',
      '5% de cashback en Puntos Monchis ($1 MXN por punto)',
    ],
  },
  {
    nivel: 'Amante del Café (Plata)',
    icono: '☕',
    requisito: '15 cafés acumulados en el año',
    beneficios: [
      'Todos los beneficios de Grano Verde',
      'Bebida gratis el día de tu cumpleaños 🎂',
      'Acceso prioritario a lotes de café de edición limitada',
      'Promociones sorpresa en repostería artesanal',
    ],
  },
  {
    nivel: 'Maestro Caficultor (Oro)',
    icono: '👑',
    requisito: '35 cafés acumulados en el año',
    beneficios: [
      'Todos los beneficios anteriores',
      '7% de cashback en Puntos Monchis en todas tus compras',
      'Taller virtual/presencial de cata y métodos de extracción gratis',
      'Personalización de bebidas sin costo extra (leche vegetal, jarabe)',
    ],
  },
];

const faqs = [
  {
    pregunta: '¿Cómo acumulo sellos en mis visitas?',
    respuesta:
      'Al pagar en caja o mostrar tu código de usuario en el POS, el barista registra tu compra automáticamente en tu cuenta. También puedes dar tu correo o número telefónico registrado.',
  },
  {
    pregunta: '¿Cómo funciona el Sello Ecológico (+1 sello)?',
    respuesta:
      'Si traes tu propio termo o taza reutilizable a la cafetería, el barista activará la opción de termo en el Punto de Venta y recibirás 2 sellos en lugar de 1 por cada café servido.',
  },
  {
    pregunta: '¿Los puntos y sellos caducan?',
    respuesta:
      'Tus sellos no caducan mientras mantengas actividad en tu cuenta al menos una vez cada 6 meses. Los puntos de cashback se conservan intactos en tu monedero digital.',
  },
  {
    pregunta: '¿Cómo canjeo mi 8vo café de regalo?',
    respuesta:
      'Cuando completas tu tarjeta de 8 sellos, el sistema te genera un cupón digital instantáneo aplicable en tu siguiente visita a cualquier café preparado de la carta.',
  },
];
</script>

<template>
  <div class="rewards-page">
    <!-- Hero Editorial de Rewards -->
    <section class="rewards-hero">
      <div class="container text-center" v-motion-fade-visible>
        <span class="badge badge--organic">🎁 Programa Monchis Rewards</span>
        <h1>Haz que cada visita cuente.<br /><span class="rewards-highlight">Recompensas con propósito</span>.</h1>
        <p class="rewards-lead">
          En Monchis Café premiamos tu preferencia y tu cariño por el medio ambiente. Acumula sellos digitales, gana cafés de regalo y ahorra dinero con cada taza.
        </p>
        <div class="hero-actions">
          <RouterLink to="/registro" class="btn btn--primary">¡Únete Gratis en 1 Minuto!</RouterLink>
          <RouterLink to="/menu" class="btn btn--secondary">Ver Menú de Bebidas</RouterLink>
        </div>
      </div>
    </section>

    <!-- Bloques Estilo Split (Inspiración Starbucks / Editorial) -->
    <section class="rewards-splits section">
      <div class="container splits-container">
        <!-- Bloque 1: Juntémonos más -->
        <div class="split-card card" v-motion-slide-visible-bottom>
          <div class="split-image">
            <img src="/feature1.jpg" alt="Amigos disfrutando café en Monchis Café" />
          </div>
          <div class="split-text primary-block">
            <span class="split-tag">COMUNIDAD & AMISTAD</span>
            <h2>Juntémonos más</h2>
            <p>Los mejores momentos y las pláticas más entrañables se acompañan con café de altura recién preparado.</p>
            <RouterLink to="/contacto" class="split-link">Visítanos con amigos →</RouterLink>
          </div>
        </div>

        <!-- Bloque 2: Compromiso Verde (Invertido) -->
        <div class="split-card card reverse" v-motion-slide-visible-bottom>
          <div class="split-text green-block">
            <span class="split-tag">🌿 IMPACTO ECOLÓGICO</span>
            <h2>Trae tu termo, gana doble</h2>
            <p>Cuidemos juntos el planeta. Cada vez que llevas tu termo o vaso reutilizable a la barra, te premiamos con <strong>2 sellos</strong> para tu café gratis.</p>
            <RouterLink to="/nosotros" class="split-link">Conoce nuestro compromiso →</RouterLink>
          </div>
          <div class="split-image">
            <img src="/feature2.jpg" alt="Termo reutilizable para café" />
          </div>
        </div>

        <!-- Bloque 3: Pide, Acumula y Disfruta -->
        <div class="split-card card" v-motion-slide-visible-bottom>
          <div class="split-image">
            <img src="/feature3.jpg" alt="App Monchis Rewards en el móvil" />
          </div>
          <div class="split-text terracotta-block">
            <span class="split-tag">PUNTOS & CASHBACK</span>
            <h2>Pide, acumula y disfruta</h2>
            <p>Monitorea tus sellos en vivo, acumula 5% en saldo monedero y canjea tu 8vo café de regalo sin letras chiquitas.</p>
            <RouterLink to="/registro" class="split-link">Crear cuenta Monchis Rewards →</RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Niveles y Beneficios -->
    <section class="section section--alt">
      <div class="container">
        <div class="section-header text-center" v-motion-fade-visible>
          <span class="badge badge--commercial">⭐ Niveles del Club</span>
          <h2>Beneficios Exclusivos para Ti</h2>
          <p class="section-subtitle">Entre más disfrutes de Monchis Café, más sorpresas desbloqueas.</p>
        </div>

        <div class="tiers-grid">
          <div v-for="nv in niveles" :key="nv.nivel" class="card tier-card" v-motion-slide-visible-bottom>
            <div class="tier-icon">{{ nv.icono }}</div>
            <h3>{{ nv.nivel }}</h3>
            <span class="tier-req">{{ nv.requisito }}</span>

            <ul class="tier-perks">
              <li v-for="b in nv.beneficios" :key="b">
                <span class="check">✓</span> {{ b }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Calculadora Dinámica -->
    <section class="section">
      <div class="container">
        <div class="calc-box card" v-motion-fade-visible>
          <div class="calc-left">
            <span class="badge badge--organic">🧮 Simulador de Recompensas</span>
            <h2>¿Cuánto ganas con tus hábitos cafeteros?</h2>
            <p>Mueve los controles para ver cuántos cafés de regalo y dinero en puntos acumulas al mes.</p>

            <div class="calc-control-group">
              <label>Cafés por semana: <strong>{{ tazasSemana }}</strong></label>
              <input v-model.number="tazasSemana" type="range" min="1" max="14" class="calc-slider" />
            </div>

            <label class="calc-check">
              <input v-model="usaTermo" type="checkbox" />
              <span>🌿 Traeré mi termo reutilizable (+1 sello eco por taza)</span>
            </label>
          </div>

          <div class="calc-right">
            <div class="stat-pill">
              <span class="stat-value">{{ sellosMes }}</span>
              <span class="stat-label">Sellos Digitales al Mes</span>
            </div>
            <div class="stat-pill highlight">
              <span class="stat-value">{{ cafesGratisMes }}</span>
              <span class="stat-label">Cafés Gratis al Mes ☕</span>
            </div>
            <div class="stat-pill">
              <span class="stat-value">${{ cashbackMes }}</span>
              <span class="stat-label">Dinero en Puntos Monedero</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Preguntas Frecuentes (FAQ) -->
    <section class="section section--alt">
      <div class="container faqs-container">
        <div class="section-header text-center" v-motion-fade-visible>
          <span class="badge badge--commercial">❓ Dudas Comunes</span>
          <h2>Preguntas Frecuentes sobre Rewards</h2>
        </div>

        <div class="faq-list">
          <div v-for="faq in faqs" :key="faq.pregunta" class="card faq-card" v-motion-slide-visible-bottom>
            <h4>{{ faq.pregunta }}</h4>
            <p>{{ faq.respuesta }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.rewards-page {
  background: var(--color-bg-base);
  min-height: 90vh;
}

.rewards-hero {
  padding: 5.5rem 0 3.5rem;
  background: linear-gradient(135deg, rgba(243, 201, 201, 0.25) 0%, var(--color-bg-base) 100%);
}

.rewards-hero h1 {
  font-size: 2.6rem;
  line-height: 1.3;
  margin: 1rem 0;
}

.rewards-highlight {
  color: var(--color-primary-dark);
}

.rewards-lead {
  max-width: 65ch;
  margin: 0 auto 2rem;
  font-size: 1.15rem;
  line-height: 1.8;
  color: var(--color-text-muted);
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

/* Splits Cards (Estilo Starbucks / Editorial) */
.splits-container {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.split-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: 0;
  overflow: hidden;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--color-border);
}

.split-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  min-height: 380px;
  display: block;
}

.split-text {
  padding: 3.5rem 4rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 1rem;
}

.split-tag {
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.split-text h2 {
  font-size: 2.2rem;
  line-height: 1.25;
}

.split-text p {
  font-size: 1.05rem;
  line-height: 1.8;
}

.split-link {
  font-weight: 700;
  font-size: 0.95rem;
  margin-top: 0.5rem;
  display: inline-flex;
  align-items: center;
  transition: transform var(--transition-fast);
}

.split-link:hover {
  transform: translateX(4px);
}

/* Variantes de Color Armonizadas */
.primary-block {
  background: #C9A88B; /* Café con leche */
  color: #fff;
}
.primary-block h2, .primary-block .split-tag { color: #FAF3ED; }
.primary-block p { color: rgba(255, 255, 255, 0.92); }
.primary-block .split-link { color: #FFFDFB; text-decoration: underline; }

.green-block {
  background: #8C6B52; /* Café tostado cálido */
  color: #fff;
}
.green-block h2, .green-block .split-tag { color: #F3C9C9; }
.green-block p { color: rgba(255, 255, 255, 0.92); }
.green-block .split-link { color: #F3C9C9; text-decoration: underline; }

.terracotta-block {
  background: #D98C7F; /* Rosa terracota */
  color: #fff;
}
.terracotta-block h2, .terracotta-block .split-tag { color: #FFFDFB; }
.terracotta-block p { color: rgba(255, 255, 255, 0.95); }
.terracotta-block .split-link { color: #FAF3ED; text-decoration: underline; }

/* Tiers Grid */
.tiers-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.tier-card {
  padding: 2.5rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.tier-icon {
  font-size: 3rem;
  margin-bottom: 0.8rem;
}

.tier-req {
  font-size: 0.85rem;
  color: var(--color-primary-dark);
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.tier-perks {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  text-align: left;
  width: 100%;
}

.tier-perks li {
  font-size: 0.9rem;
  line-height: 1.5;
  display: flex;
  gap: 0.5rem;
}

.check {
  color: #5a8a52;
  font-weight: bold;
}

/* Calculadora */
.calc-box {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 3rem;
  padding: 3.5rem;
  background: var(--color-bg-surface);
  align-items: center;
}

.calc-control-group {
  margin: 1.5rem 0 1rem;
}

.calc-slider {
  width: 100%;
  accent-color: var(--color-primary-dark);
  cursor: pointer;
  margin-top: 0.5rem;
}

.calc-check {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 0.8rem;
  background: rgba(183, 217, 177, 0.2);
  border-radius: var(--radius-sm);
}

.calc-right {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stat-pill {
  padding: 1.2rem;
  background: var(--color-bg-base);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  text-align: center;
}

.stat-pill.highlight {
  border-color: var(--color-primary-dark);
  background: rgba(243, 201, 201, 0.25);
}

.stat-value {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--color-primary-dark);
  display: block;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--color-text-muted);
}

/* FAQs */
.faqs-container {
  max-width: 820px;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.faq-card {
  padding: 1.8rem 2rem;
}

.faq-card h4 {
  font-size: 1.15rem;
  color: var(--color-text-main);
  margin-bottom: 0.5rem;
}

.faq-card p {
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--color-text-muted);
}

@media (max-width: 900px) {
  .split-card {
    grid-template-columns: 1fr;
  }
  .split-card.reverse {
    display: flex;
    flex-direction: column-reverse;
  }
  .split-text {
    padding: 2.5rem 1.8rem;
  }
  .tiers-grid, .calc-box {
    grid-template-columns: 1fr;
    gap: 2rem;
    padding: 2rem;
  }
}
</style>
