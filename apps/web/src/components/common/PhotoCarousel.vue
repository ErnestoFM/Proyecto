<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

const slides = [
  {
    titulo: 'Granos de Altura Cosechados a Mano',
    subtitulo: 'Chiapas & Oaxaca — 1,450 msnm',
    descripcion: 'Trabajamos con familias campesinas que cultivan café bajo sombra natural, seleccionando cerezas maduras una por una.',
    tag: 'Trazabilidad 100% Orgánica',
    imagen: '/slide1.jpg',
  },
  {
    titulo: 'Tueste Artesanal en Lotes Pequeños',
    subtitulo: 'Tostado Semanal para Máxima Frescura',
    descripcion: 'Tostamos cada lote resaltando las notas naturales a chocolate, avellana y miel de azahar sin quemar los granos.',
    tag: 'Perfil de Tueste de Especialidad',
    imagen: '/slide2.jpg',
  },
  {
    titulo: 'Preparación de Barra y Métodos Manuales',
    subtitulo: 'Extracción Precisa de Barista',
    descripcion: 'V60, Prensa Francesa y Cold Brew de 18 horas elaborados con agua a temperatura controlada y molienda al instante.',
    tag: 'Café de Especialidad',
    imagen: '/slide3.jpg',
  },
  {
    titulo: 'Repostería Artesanal & Panqué de Elote',
    subtitulo: 'Horneado Diario en Casa',
    descripcion: 'Elaborado con maíz dulce de campesinos locales y mantequilla pura. El acompañamiento perfecto para tu café.',
    tag: 'Hecho con Cariño en Casa',
    imagen: '/slide4.jpg',
  },
];

const slideActual = ref(0);
let intervalo: any = null;

function siguiente() {
  slideActual.value = (slideActual.value + 1) % slides.length;
}

function anterior() {
  slideActual.value = (slideActual.value - 1 + slides.length) % slides.length;
}

function irASlide(index: number) {
  slideActual.value = index;
}

onMounted(() => {
  intervalo = setInterval(siguiente, 5500);
});

onUnmounted(() => {
  if (intervalo) clearInterval(intervalo);
});
</script>

<template>
  <div class="photo-carousel card">
    <div class="carousel-track">
      <div
        v-for="(slide, idx) in slides"
        :key="slide.titulo"
        :class="['carousel-item', { active: slideActual === idx }]"
      >
        <img :src="slide.imagen" :alt="slide.titulo" class="slide-photo" />
        <div class="slide-overlay">
          <div class="slide-badge-row">
            <span class="badge badge--organic">{{ slide.tag }}</span>
          </div>
          <h3>{{ slide.titulo }}</h3>
          <h4>{{ slide.subtitulo }}</h4>
          <p>{{ slide.descripcion }}</p>
        </div>
      </div>
    </div>

    <!-- Controles -->
    <button class="nav-btn prev" @click="anterior" aria-label="Anterior">❮</button>
    <button class="nav-btn next" @click="siguiente" aria-label="Siguiente">❯</button>

    <!-- Indicadores -->
    <div class="carousel-indicators">
      <button
        v-for="(_, idx) in slides"
        :key="idx"
        :class="['indicator-dot', { active: slideActual === idx }]"
        @click="irASlide(idx)"
      ></button>
    </div>
  </div>
</template>

<style scoped>
.photo-carousel {
  position: relative;
  overflow: hidden;
  padding: 0;
  border-radius: var(--radius-lg);
  margin: 3.5rem 0;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--color-border);
  height: 480px;
}

.carousel-track {
  width: 100%;
  height: 100%;
  position: relative;
}

.carousel-item {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 0.8s ease-in-out;
  display: flex;
  align-items: flex-end;
}

.carousel-item.active {
  opacity: 1;
  z-index: 1;
}

.slide-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  inset: 0;
}

.slide-overlay {
  position: relative;
  z-index: 2;
  width: 100%;
  background: linear-gradient(180deg, rgba(74, 59, 50, 0) 0%, rgba(74, 59, 50, 0.85) 60%, rgba(74, 59, 50, 0.98) 100%);
  padding: 3rem 4rem 2.5rem;
  color: #fff;
}

.slide-badge-row {
  margin-bottom: 0.6rem;
}

.slide-overlay h3 {
  font-size: 2rem;
  color: #fff;
  line-height: 1.25;
  margin-bottom: 0.3rem;
}

.slide-overlay h4 {
  font-size: 1.1rem;
  color: var(--color-primary);
  font-weight: 600;
  margin-bottom: 0.6rem;
}

.slide-overlay p {
  font-size: 0.95rem;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.88);
  max-width: 65ch;
}

.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(250, 243, 237, 0.85);
  backdrop-filter: blur(8px);
  border: 1px solid var(--color-border);
  color: var(--color-text-main);
  font-size: 1.3rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
  z-index: 10;
}

.nav-btn:hover {
  background: #fff;
  transform: translateY(-50%) scale(1.1);
  box-shadow: var(--shadow-md);
}

.nav-btn.prev {
  left: 1.5rem;
}

.nav-btn.next {
  right: 1.5rem;
}

.carousel-indicators {
  position: absolute;
  bottom: 1.2rem;
  right: 4rem;
  display: flex;
  gap: 0.6rem;
  z-index: 10;
}

.indicator-dot {
  width: 12px;
  height: 12px;
  border-radius: var(--radius-full);
  background: rgba(255, 255, 255, 0.4);
  border: none;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.indicator-dot.active {
  width: 32px;
  background: var(--color-primary);
}

@media (max-width: 768px) {
  .photo-carousel {
    height: 420px;
  }
  .slide-overlay {
    padding: 2rem 1.5rem 1.5rem;
  }
  .slide-overlay h3 {
    font-size: 1.4rem;
  }
  .slide-overlay h4 {
    font-size: 0.95rem;
  }
  .slide-overlay p {
    font-size: 0.85rem;
    line-height: 1.5;
  }
  .nav-btn {
    display: none;
  }
  .carousel-indicators {
    right: 1.5rem;
    bottom: 1rem;
  }
}
</style>
