<script setup lang="ts">
import { ref, computed } from 'vue';

interface MenuItem {
  id: string;
  nombre: string;
  categoria: 'CALIENTES' | 'FRIOS' | 'METODOS' | 'REPOSTERIA' | 'GRANOS';
  tipo: 'ORGANICO' | 'COMERCIAL';
  precio: number;
  origen?: string;
  perfil?: string;
  descripcion: string;
  icono: string;
}

const categoriaActiva = ref<'TODOS' | 'CALIENTES' | 'FRIOS' | 'METODOS' | 'REPOSTERIA' | 'GRANOS'>('TODOS');
const soloOrganicos = ref(false);
const busqueda = ref('');

const menuCompleto: MenuItem[] = [
  // Cafés Calientes
  {
    id: 'c1',
    nombre: 'Café de Olla Tradicional',
    categoria: 'CALIENTES',
    tipo: 'ORGANICO',
    precio: 48.0,
    origen: 'Finca Santa Rosa, Chiapas (1,450 msnm)',
    perfil: 'Piloncillo de caña pura, canela en raja y clavo dulce',
    descripcion: 'Nuestra receta insignia cocinada a fuego lento en olla de barro tradicional.',
    icono: '☕',
  },
  {
    id: 'c2',
    nombre: 'Espresso Doble de Especialidad',
    categoria: 'CALIENTES',
    tipo: 'ORGANICO',
    precio: 42.0,
    origen: 'Pluma Hidalgo, Oaxaca (1,300 msnm)',
    perfil: 'Cuerpo denso, crema dorada y notas a avellana tostada',
    descripcion: 'Extracción precisa de 36g a 9 bares de presión. La máxima pureza del grano.',
    icono: '🤎',
  },
  {
    id: 'c3',
    nombre: 'Latte Lavanda & Miel de Rancho',
    categoria: 'CALIENTES',
    tipo: 'ORGANICO',
    precio: 72.0,
    origen: 'Coatepec, Veracruz',
    perfil: 'Lavanda francesa orgánica y miel cruda de abeja',
    descripcion: 'Espresso balanceado con leche cremada y sutil aroma floral relajante.',
    icono: '🌸',
  },
  {
    id: 'c4',
    nombre: 'Capuchino Clásico Tostado',
    categoria: 'CALIENTES',
    tipo: 'ORGANICO',
    precio: 58.0,
    origen: 'Chiapas / Oaxaca Blend',
    perfil: 'Cacao amargo y crema de leche aterciopelada',
    descripcion: 'Tercio perfecto de espresso, leche caliente y microespuma sedosa.',
    icono: '☕',
  },
  {
    id: 'c5',
    nombre: 'Mocha con Chocolate Oaxaqueño',
    categoria: 'CALIENTES',
    tipo: 'ORGANICO',
    precio: 75.0,
    origen: 'Pluma Hidalgo, Oaxaca',
    perfil: 'Chocolate de metate 70% cacao artesanal',
    descripcion: 'La combinación perfecta entre espresso de especialidad y auténtico chocolate de metate.',
    icono: '🍫',
  },

  // Bebidas Frías
  {
    id: 'f1',
    nombre: 'Cold Brew de la Sierra (18h)',
    categoria: 'FRIOS',
    tipo: 'ORGANICO',
    precio: 65.0,
    origen: 'Rancho Las Nubes, Oaxaca',
    perfil: 'Notas afrutadas, miel y acidez baja sedosa',
    descripcion: 'Maceración lenta en frío por 18 horas. Refrescante, dulce y energizante.',
    icono: '🧊',
  },
  {
    id: 'f2',
    nombre: 'Iced Latte Vainilla Papantla',
    categoria: 'FRIOS',
    tipo: 'ORGANICO',
    precio: 68.0,
    origen: 'Chiapas & Vainilla de Veracruz',
    perfil: 'Vainilla natural en vaina y leche fresca sobre hielo',
    descripcion: 'Infusión de vainilla natural de Papantla con espresso doble frío.',
    icono: '🥤',
  },
  {
    id: 'f3',
    nombre: 'Tónica Espresso & Cítricos',
    categoria: 'FRIOS',
    tipo: 'ORGANICO',
    precio: 70.0,
    origen: 'Chiapas de Altura',
    perfil: 'Agua tónica premium, rodaja de naranja deshidratada y café',
    descripcion: 'Bebida burbujeante y aromática ideal para tardes calurosas.',
    icono: '🍊',
  },

  // Métodos de Extracción Artesanal
  {
    id: 'm1',
    nombre: 'Filtrado V60 Pour-Over',
    categoria: 'METODOS',
    tipo: 'ORGANICO',
    precio: 65.0,
    origen: 'Lote Exclusivo Chiapas Santa Rosa',
    perfil: 'Cuerpo ligero, claridad cristalina y notas florales',
    descripcion: 'Goteo manual con filtro de papel cónico. Resalta los matices más sutiles del café.',
    icono: '🧪',
  },
  {
    id: 'm2',
    nombre: 'Prensa Francesa de Inmersión',
    categoria: 'METODOS',
    tipo: 'ORGANICO',
    precio: 60.0,
    origen: 'Oaxaca Pluma Hidalgo',
    perfil: 'Cuerpo pleno, aceites esenciales y regusto a chocolate',
    descripcion: 'Inmersión completa por 4 minutos para una taza robusta y reconfortante.',
    icono: '🫖',
  },
  {
    id: 'm3',
    nombre: 'Aeropress Barista Signature',
    categoria: 'METODOS',
    tipo: 'ORGANICO',
    precio: 65.0,
    origen: 'Coatepec, Veracruz',
    perfil: 'Intensidad media, acidez limpia y dulzor prolongado',
    descripcion: 'Extracción por presión de aire rápida que produce una taza limpia y aromática.',
    icono: '☕',
  },

  // Repostería Artesanal
  {
    id: 'r1',
    nombre: 'Panqué Artesanal de Elote Criollo',
    categoria: 'REPOSTERIA',
    tipo: 'COMERCIAL',
    precio: 45.0,
    perfil: 'Maíz dulce campesino y toque de canela',
    descripcion: 'Horneado cada mañana con granos tiernos de elote. Textura suave y húmeda.',
    icono: '🌽',
  },
  {
    id: 'r2',
    nombre: 'Galleta Rústica de Avena & Arándanos',
    categoria: 'REPOSTERIA',
    tipo: 'COMERCIAL',
    precio: 28.0,
    perfil: 'Avena integral, arándanos secos y miel de agave',
    descripcion: 'Crujiente por fuera y tierna por dentro. Sin azúcar refinada.',
    icono: '🍪',
  },
  {
    id: 'r3',
    nombre: 'Tarta de Manzana y Nuez de la Región',
    categoria: 'REPOSTERIA',
    tipo: 'COMERCIAL',
    precio: 55.0,
    perfil: 'Masa quebrada con mantequilla y manzanas especiadas',
    descripcion: 'Receta tradicional horneada con frutos de huertos vecinos.',
    icono: '🥧',
  },

  // Bolsas de Café en Grano
  {
    id: 'g1',
    nombre: 'Bolsa de Grano Entero Chiapas (500g)',
    categoria: 'GRANOS',
    tipo: 'ORGANICO',
    precio: 220.0,
    origen: 'Finca Santa Rosa, Tapachula (1,450 msnm)',
    perfil: 'Tueste Medio • Notas a Chocolate, Caramelo y Avellana',
    descripcion: 'Lote fresco empacado con válvula desgasificadora para llevar la experiencia a casa.',
    icono: '📦',
  },
  {
    id: 'g2',
    nombre: 'Bolsa de Grano Entero Oaxaca Honey (500g)',
    categoria: 'GRANOS',
    tipo: 'ORGANICO',
    precio: 240.0,
    origen: 'Rancho Las Nubes, Pluma Hidalgo (1,300 msnm)',
    perfil: 'Tueste Medio-Claro • Miel de azahar, jazmín y durazno',
    descripcion: 'Proceso honey artesanal con secado en camas africanas.',
    icono: '📦',
  },
];

const itemsFiltrados = computed(() => {
  return menuCompleto.filter((item) => {
    const matchCat = categoriaActiva.value === 'TODOS' || item.categoria === categoriaActiva.value;
    const matchOrg = !soloOrganicos.value || item.tipo === 'ORGANICO';
    const matchSearch =
      item.nombre.toLowerCase().includes(busqueda.value.toLowerCase()) ||
      item.descripcion.toLowerCase().includes(busqueda.value.toLowerCase()) ||
      (item.perfil && item.perfil.toLowerCase().includes(busqueda.value.toLowerCase()));
    return matchCat && matchOrg && matchSearch;
  });
});
</script>

<template>
  <div class="menu-page section">
    <div class="container">
      <!-- Encabezado del Menú -->
      <header class="menu-header text-center" v-motion-fade-visible>
        <span class="badge badge--organic">📜 Catálogo Demostrativo</span>
        <h1>Menú de Especialidad — <strong>Monchis Café</strong></h1>
        <p class="menu-subtitle">
          Explora nuestra selección completa de bebidas, métodos de extracción y repostería artesanal.
        </p>

        <!-- Banner Explicativo Informativo -->
        <div class="menu-info-banner card">
          <span class="banner-icon">ℹ️</span>
          <div class="banner-text">
            <strong>Catálogo informativo de barra:</strong>
            <p>
              Este menú es para consulta de precios, orígenes y notas de cata. Las compras se realizan en nuestro mostrador físico o a través del
              <RouterLink to="/pos">Punto de Venta (POS)</RouterLink> del barista. Trae tu termo y recibe <strong>doble sello Monchis Rewards</strong>. 🌿
            </p>
          </div>
        </div>
      </header>

      <!-- Filtros y Buscador -->
      <div class="menu-controls">
        <div class="categories-tabs">
          <button :class="['cat-tab', { active: categoriaActiva === 'TODOS' }]" @click="categoriaActiva = 'TODOS'">
            ☕ Todo
          </button>
          <button :class="['cat-tab', { active: categoriaActiva === 'CALIENTES' }]" @click="categoriaActiva = 'CALIENTES'">
            🔥 Calientes
          </button>
          <button :class="['cat-tab', { active: categoriaActiva === 'FRIOS' }]" @click="categoriaActiva = 'FRIOS'">
            🧊 Fríos & Cold Brew
          </button>
          <button :class="['cat-tab', { active: categoriaActiva === 'METODOS' }]" @click="categoriaActiva = 'METODOS'">
            🧪 Métodos de Extracción
          </button>
          <button :class="['cat-tab', { active: categoriaActiva === 'REPOSTERIA' }]" @click="categoriaActiva = 'REPOSTERIA'">
            🥐 Repostería
          </button>
          <button :class="['cat-tab', { active: categoriaActiva === 'GRANOS' }]" @click="categoriaActiva = 'GRANOS'">
            📦 Café en Grano
          </button>
        </div>

        <div class="filter-row">
          <input
            v-model="busqueda"
            type="search"
            placeholder="🔍 Buscar bebida, ingrediente o nota..."
            class="menu-search"
          />
          <label class="organic-toggle">
            <input v-model="soloOrganicos" type="checkbox" />
            <span>🌿 Solo 100% Orgánicos</span>
          </label>
        </div>
      </div>

      <!-- Cuadrícula del Catálogo -->
      <div class="menu-grid">
        <div v-for="item in itemsFiltrados" :key="item.id" class="menu-card card" v-motion-slide-visible-bottom>
          <div class="menu-card__top">
            <span class="menu-item-icon">{{ item.icono }}</span>
            <span
              :class="[
                'badge',
                item.tipo === 'ORGANICO' ? 'badge--organic' : 'badge--commercial',
              ]"
            >
              {{ item.tipo === 'ORGANICO' ? '🌿 Orgánico' : '🥐 Artesanal' }}
            </span>
          </div>

          <div class="menu-card__body">
            <div class="name-price-row">
              <h3>{{ item.nombre }}</h3>
              <span class="item-price">${{ item.precio.toFixed(2) }}</span>
            </div>

            <p class="item-desc">{{ item.descripcion }}</p>

            <div v-if="item.origen" class="item-extra origin">
              <span class="extra-label">📍 Origen:</span>
              <p>{{ item.origen }}</p>
            </div>

            <div v-if="item.perfil" class="item-extra notes">
              <span class="extra-label">✨ Notas / Perfil:</span>
              <p>{{ item.perfil }}</p>
            </div>
          </div>

          <div class="menu-card__footer">
            <small class="order-hint">📍 Pídelo en barra con tu barista</small>
            <span class="rewards-tag">🎁 Suma sellos Rewards</span>
          </div>
        </div>
      </div>

      <!-- Footer CTA del Menú -->
      <section class="menu-cta card text-center" v-motion-fade-visible>
        <h2>¿Quieres disfrutar tu café favorito hoy?</h2>
        <p>Visítanos en nuestra cafetería o encuentra cómo llegar en el mapa interactivo.</p>
        <div class="menu-cta-actions">
          <RouterLink to="/contacto" class="btn btn--primary">Encontrar la Cafetería 📍</RouterLink>
          <RouterLink to="/nosotros" class="btn btn--secondary">Conocer a los Productores 🌱</RouterLink>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.menu-page {
  background: var(--color-bg-base);
  min-height: 90vh;
}

.menu-header {
  margin-bottom: 2.5rem;
}

.menu-header h1 {
  font-size: 2.3rem;
  margin: 0.6rem 0;
}

.menu-subtitle {
  font-size: 1.05rem;
  color: var(--color-text-muted);
  max-width: 60ch;
  margin: 0 auto 1.5rem;
}

.menu-info-banner {
  max-width: 760px;
  margin: 0 auto;
  padding: 1.2rem 1.6rem;
  display: flex;
  align-items: center;
  gap: 1.2rem;
  background: linear-gradient(135deg, rgba(243, 201, 201, 0.2), var(--color-bg-surface));
  border: 1px solid var(--color-border);
  text-align: left;
}

.banner-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.banner-text strong {
  color: var(--color-primary-dark);
  font-size: 0.95rem;
}

.banner-text p {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  margin-top: 0.2rem;
}

.menu-controls {
  margin-bottom: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.categories-tabs {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
  justify-content: center;
}

.cat-tab {
  padding: 0.65rem 1.2rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--color-border);
  background: var(--color-bg-surface);
  font-family: var(--font-heading);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.cat-tab.active {
  background: var(--color-primary-dark);
  color: #fff;
  border-color: var(--color-primary-dark);
  box-shadow: var(--shadow-sm);
}

.filter-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.menu-search {
  max-width: 380px;
  width: 100%;
  padding: 0.75rem 1.2rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--color-border);
  background: var(--color-bg-surface);
  outline: none;
  font-family: var(--font-body);
}

.organic-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  margin-bottom: 3.5rem;
}

.menu-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 2rem;
}

.menu-card__top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.menu-item-icon {
  font-size: 2.5rem;
}

.name-price-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.8rem;
  margin-bottom: 0.6rem;
}

.name-price-row h3 {
  font-size: 1.15rem;
  color: var(--color-text-main);
}

.item-price {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-primary-dark);
}

.item-desc {
  font-size: 0.85rem;
  line-height: 1.6;
  color: var(--color-text-muted);
  margin-bottom: 1rem;
}

.item-extra {
  font-size: 0.8rem;
  padding: 0.5rem 0.8rem;
  border-radius: var(--radius-sm);
  margin-bottom: 0.6rem;
}

.item-extra.origin {
  background: rgba(201, 168, 139, 0.15);
}

.item-extra.notes {
  background: rgba(243, 201, 201, 0.15);
}

.extra-label {
  font-weight: 700;
  color: var(--color-secondary-dark);
  display: block;
  font-size: 0.75rem;
  text-transform: uppercase;
}

.item-extra p {
  color: var(--color-text-main);
  margin-top: 0.1rem;
}

.menu-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--color-border);
  padding-top: 1rem;
  margin-top: 1rem;
}

.order-hint {
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.rewards-tag {
  font-size: 0.75rem;
  font-weight: 600;
  color: #5a8a52;
}

.menu-cta {
  padding: 3rem;
  background: linear-gradient(135deg, rgba(243, 201, 201, 0.25), rgba(201, 168, 139, 0.15));
}

.menu-cta h2 {
  font-size: 1.8rem;
  margin-bottom: 0.6rem;
}

.menu-cta p {
  max-width: 50ch;
  margin: 0 auto 1.5rem;
}

.menu-cta-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .menu-info-banner {
    flex-direction: column;
    text-align: center;
  }
  .menu-grid {
    grid-template-columns: 1fr;
  }
  .categories-tabs {
    justify-content: flex-start;
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }
}
</style>
