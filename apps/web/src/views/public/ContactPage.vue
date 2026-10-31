<script setup lang="ts">
import { ref, computed } from 'vue';

// --- Estado del Formulario de Contacto ---
const nombre = ref('');
const email = ref('');
const telefono = ref('');
const motivo = ref('menu');
const mensaje = ref('');
const aceptaPrivacidad = ref(false);
const enviando = ref(false);
const enviadoExitoso = ref(false);

const motivosContacto = [
  { valor: 'menu', etiqueta: '☕ Preguntas sobre el Menú o Café Orgánico' },
  { valor: 'pedidos', etiqueta: '🛍️ Pedidos para Llevar o Eventos Especiales' },
  { valor: 'proveedores', etiqueta: '🌱 Productores Campesinos y Alianzas' },
  { valor: 'bolsa_trabajo', etiqueta: '💼 Bolsa de Trabajo (Baristas & Equipo)' },
  { valor: 'facturacion', etiqueta: '🧾 Facturación Electrónica' },
  { valor: 'otro', etiqueta: '💬 Otro Asunto / Sugerencia' },
];

async function enviarFormulario() {
  enviando.value = true;
  // Simular envío de mensaje con retroalimentación instantánea
  await new Promise((resolve) => setTimeout(resolve, 800));
  enviando.value = false;
  enviadoExitoso.value = true;

  // Limpiar campos del formulario
  nombre.value = '';
  email.value = '';
  telefono.value = '';
  motivo.value = 'menu';
  mensaje.value = '';
  aceptaPrivacidad.value = false;
}

// --- Cálculo Dinámico de Estado Abierto / Cerrado ---
const estadoHorario = computed(() => {
  const ahora = new Date();
  const dia = ahora.getDay(); // 0 = Domingo, 1 = Lunes, ..., 6 = Sábado
  const hora = ahora.getHours() + ahora.getMinutes() / 60;

  // Lunes a Viernes: 07:30 a 20:30
  if (dia >= 1 && dia <= 5) {
    if (hora >= 7.5 && hora < 20.5) {
      return { abierto: true, texto: 'Abierto ahora · Cierra a las 20:30' };
    }
  }
  // Sábado: 08:00 a 21:00
  else if (dia === 6) {
    if (hora >= 8 && hora < 21) {
      return { abierto: true, texto: 'Abierto ahora · Cierra a las 21:00' };
    }
  }
  // Domingo: 08:30 a 18:00
  else if (dia === 0) {
    if (hora >= 8.5 && hora < 18) {
      return { abierto: true, texto: 'Abierto ahora · Cierra a las 18:00' };
    }
  }

  return { abierto: false, texto: 'Cerrado por ahora · Abre mañana temprano' };
});

// --- Preguntas Frecuentes (FAQ) ---
const faqAbierto = ref<number | null>(0);
function toggleFaq(index: number) {
  faqAbierto.value = faqAbierto.value === index ? null : index;
}

const faqs = [
  {
    pregunta: '¿Tienen opciones de leches vegetales o productos sin gluten?',
    respuesta:
      '¡Sí! Contamos con leche de avena, almendra y coco sin costo adicional en todas nuestras preparaciones orgánicas. También ofrecemos repostería artesanal sin harinas refinadas y opciones veganas.',
  },
  {
    pregunta: '¿Puedo comprar café en grano y pedir que lo muelan?',
    respuesta:
      'Totalmente. Puedes adquirir bolsas de nuestros lotes de Chiapas y Oaxaca (250g o 1kg) y nuestro barista calibra la molienda al momento según tu cafetera (Prensa Francesa, Espresso, V60, Moka Italiana o grano entero).',
  },
  {
    pregunta: '¿Cómo funciona el descuento por traer termo?',
    respuesta:
      'Si traes tu termo o taza reutilizable a la cafetería, recibes un sello adicional en tu tarjeta digital de Monchis Rewards (+1 sello ecológico), completando tu 8vo café de regalo el doble de rápido.',
  },
  {
    pregunta: '¿Tienen espacio para trabajar o estudiar (Coworking)?',
    respuesta:
      'Sí, nuestras instalaciones cuentan con mesas amplias, WiFi de fibra óptica de alta velocidad y conexiones eléctricas accesibles en casi todas las mesas.',
  },
  {
    pregunta: '¿Puedo apartar la terraza para un evento o reunión privada?',
    respuesta:
      'Con gusto. Puedes escribirnos a través del formulario seleccionando "Pedidos para Llevar o Eventos Especiales" o contactarnos directamente por WhatsApp con al menos 48 horas de anticipación.',
  },
];

// --- Redes Sociales Mockeadas ---
const redesSociales = [
  {
    nombre: 'Instagram',
    usuario: '@monchiscafe',
    icono: '📸',
    url: 'https://instagram.com/monchiscafe',
    descripcion: 'Fotos de lotes recién tostados, historias diarias y promociones.',
    clase: 'social-card--instagram',
  },
  {
    nombre: 'Facebook',
    usuario: 'Monchis Café Oficial',
    icono: '📘',
    url: 'https://facebook.com/monchiscafe',
    descripcion: 'Comunidad, avisos de talleres de barismo y eventos culturales.',
    clase: 'social-card--facebook',
  },
  {
    nombre: 'TikTok',
    usuario: '@monchiscafe',
    icono: '🎵',
    url: 'https://tiktok.com/@monchiscafe',
    descripcion: 'Recetas de café en casa, métodos de extracción y vida en el rancho.',
    clase: 'social-card--tiktok',
  },
  {
    nombre: 'Spotify Playlist',
    usuario: 'Monchis Café Radio',
    icono: '☕',
    url: 'https://open.spotify.com',
    descripcion: 'La música acústica, jazz y lo-fi que suena todos los días en la barra.',
    clase: 'social-card--spotify',
  },
];
</script>

<template>
  <div class="contact-page">
    <!-- Hero Principal -->
    <section class="contact-hero">
      <div class="container text-center" v-motion-slide-bottom>
        <span class="badge badge--organic">💬 Hablemos de Buen Café</span>
        <h1>Visítanos o Escríbenos</h1>
        <p class="contact-hero__lead">
          En Monchis Café nos encanta recibirte con una sonrisa y una taza humeante. Ya sea que
          quieras visitarnos, hacer un pedido para recoger o sumarte a nuestra red de comercio justo,
          estamos a un mensaje de distancia.
        </p>
      </div>
    </section>

    <!-- Barra de Canales Directos (WhatsApp, Teléfono, Correo, Ubicación) -->
    <section class="section direct-channels-section">
      <div class="container">
        <div class="channels-grid">
          <!-- WhatsApp Primario -->
          <a
            href="https://wa.me/5213300000000?text=%C2%A1Hola%20Monchis%20Caf%C3%A9!%20Me%20gustar%C3%ADa%20m%C3%A1s%20informaci%C3%B3n."
            target="_blank"
            rel="noopener noreferrer"
            class="channel-card channel-card--whatsapp card"
            v-motion-slide-visible-bottom
          >
            <div class="channel-card__icon">💬</div>
            <div class="channel-card__content">
              <span class="channel-card__badge">Respuesta Rápida</span>
              <h3>WhatsApp Directo</h3>
              <p>Pedidos para recoger, dudas rápidas y atención en mostrador.</p>
              <span class="channel-card__action">Iniciar Chat →</span>
            </div>
          </a>

          <!-- Teléfono Fijo / Mostrador -->
          <a
            href="tel:+523312345678"
            class="channel-card card"
            v-motion-slide-visible-bottom
            :delay="100"
          >
            <div class="channel-card__icon">📞</div>
            <div class="channel-card__content">
              <span class="channel-card__badge">Llamada Directa</span>
              <h3>+52 (33) 1234-5678</h3>
              <p>Comunícate directamente a la barra de baristas en horario laboral.</p>
              <span class="channel-card__action">Llamar Ahora →</span>
            </div>
          </a>

          <!-- Correo Institucional -->
          <a
            href="mailto:hola@monchiscafe.com"
            class="channel-card card"
            v-motion-slide-visible-bottom
            :delay="200"
          >
            <div class="channel-card__icon">✉️</div>
            <div class="channel-card__content">
              <span class="channel-card__badge">Atención Escrita</span>
              <h3>hola@monchiscafe.com</h3>
              <p>Para facturación, dudas administrativas y proveedores regionales.</p>
              <span class="channel-card__action">Enviar Correo →</span>
            </div>
          </a>

          <!-- Ubicación Resumida -->
          <div
            class="channel-card card"
            v-motion-slide-visible-bottom
            :delay="300"
          >
            <div class="channel-card__icon">📍</div>
            <div class="channel-card__content">
              <span class="channel-card__badge">Encuéntranos</span>
              <h3>Corredor Verde 1450</h3>
              <p>Zona Suburbana / Tonalá, Jalisco, México. Frente al Parque Arbolado.</p>
              <a href="#mapa-seccion" class="channel-card__action">Ver en Mapa ↓</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Sección Principal: Formulario + Mapa & Horarios -->
    <section class="section" id="formulario-seccion">
      <div class="container main-contact-grid">
        <!-- Columna 1: Formulario de Contacto -->
        <div class="contact-form-column card" v-motion-slide-left>
          <div class="form-header">
            <span class="badge badge--commercial">📬 Mensaje Directo</span>
            <h2>Envíanos un mensaje</h2>
            <p>Déjanos tus datos y nos pondremos en contacto contigo a la brevedad.</p>
          </div>

          <!-- Mensaje de éxito tras envío -->
          <div v-if="enviadoExitoso" class="success-banner">
            <span class="success-banner__icon">✨</span>
            <div>
              <h4>¡Mensaje Recibido!</h4>
              <p>
                Muchas gracias por escribirnos. Nuestro equipo revisará tu solicitud y te
                responderá en menos de 24 horas hábiles.
              </p>
              <button class="btn btn--secondary btn--sm" @click="enviadoExitoso = false">
                Enviar otro mensaje
              </button>
            </div>
          </div>

          <!-- Formulario interactivo -->
          <form v-else @submit.prevent="enviarFormulario" class="contact-form">
            <div class="form-row">
              <div class="form-group">
                <label for="c-nombre">Nombre Completo *</label>
                <input
                  id="c-nombre"
                  v-model="nombre"
                  type="text"
                  placeholder="Tu nombre y apellido"
                  required
                />
              </div>

              <div class="form-group">
                <label for="c-email">Correo Electrónico *</label>
                <input
                  id="c-email"
                  v-model="email"
                  type="email"
                  placeholder="correo@ejemplo.com"
                  required
                />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="c-telefono">Teléfono / WhatsApp (Opcional)</label>
                <input
                  id="c-telefono"
                  v-model="telefono"
                  type="tel"
                  placeholder="+52 33 0000 0000"
                />
              </div>

              <div class="form-group">
                <label for="c-motivo">Motivo de Contacto *</label>
                <select id="c-motivo" v-model="motivo" required>
                  <option
                    v-for="opc in motivosContacto"
                    :key="opc.valor"
                    :value="opc.valor"
                  >
                    {{ opc.etiqueta }}
                  </option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label for="c-mensaje">Tu Mensaje *</label>
              <textarea
                id="c-mensaje"
                v-model="mensaje"
                rows="4"
                placeholder="Cuéntanos en qué podemos ayudarte..."
                required
              ></textarea>
            </div>

            <div class="form-group legal-consent">
              <label class="consent-label">
                <input v-model="aceptaPrivacidad" type="checkbox" required />
                <span>
                  He leído y acepto el
                  <RouterLink to="/legal?tab=privacidad" target="_blank"
                    >Aviso de Privacidad</RouterLink
                  >
                  para el tratamiento seguro de mis datos de contacto.
                </span>
              </label>
            </div>

            <button
              type="submit"
              class="btn btn--primary btn--submit"
              :disabled="enviando || !aceptaPrivacidad"
            >
              <span v-if="enviando">Enviando mensaje...</span>
              <span v-else>Enviar Mensaje 🚀</span>
            </button>
          </form>
        </div>

        <!-- Columna 2: Horarios, Amenidades y Mapa -->
        <div class="contact-info-column" v-motion-slide-right>
          <!-- Tarjeta de Horarios y Estatus en Vivo -->
          <div class="card hours-card">
            <div class="hours-header">
              <h3>🕒 Horarios de Barra & Cocina</h3>
              <span
                :class="[
                  'status-pill',
                  estadoHorario.abierto ? 'status-pill--open' : 'status-pill--closed',
                ]"
              >
                ● {{ estadoHorario.texto }}
              </span>
            </div>

            <ul class="hours-list">
              <li>
                <span>Lunes a Viernes</span>
                <strong>07:30 — 20:30 hrs</strong>
              </li>
              <li>
                <span>Sábados</span>
                <strong>08:00 — 21:00 hrs</strong>
              </li>
              <li>
                <span>Domingos</span>
                <strong>08:30 — 18:00 hrs</strong>
              </li>
            </ul>

            <div class="hours-footer">
              <small>☕ Barra de extracción y cocina cierran 20 min antes del horario de corte.</small>
            </div>
          </div>

          <!-- Amenidades de la Cafetería -->
          <div class="card amenities-card">
            <h4>🌿 Servicios & Amenidades en Tienda</h4>
            <div class="amenities-grid">
              <div class="amenity-item">
                <span class="amenity-icon">🐾</span>
                <div>
                  <strong>Pet Friendly</strong>
                  <small>Terraza techada con agua fresca para mascotas</small>
                </div>
              </div>
              <div class="amenity-item">
                <span class="amenity-icon">💻</span>
                <div>
                  <strong>WiFi de Alta Velocidad</strong>
                  <small>Fibra óptica 200 Mbps y enchufes en cada mesa</small>
                </div>
              </div>
              <div class="amenity-item">
                <span class="amenity-icon">🚲</span>
                <div>
                  <strong>Bicicletero Seguro</strong>
                  <small>Área designada para ciclistas en la entrada</small>
                </div>
              </div>
              <div class="amenity-item">
                <span class="amenity-icon">🎁</span>
                <div>
                  <strong>Monchis Rewards</strong>
                  <small>+1 sello ecológico si traes tu termo reutilizable</small>
                </div>
              </div>
            </div>
          </div>

          <!-- Mapa Embebido de Google Maps -->
          <div class="card map-card" id="mapa-seccion">
            <div class="map-header">
              <h4>📍 Nuestra Ubicación</h4>
              <p>Av. Corredor Verde Principal #1450, Tonalá / ZMG, Jalisco</p>
            </div>

            <div class="map-embed-container">
              <iframe
                title="Mapa de ubicación Monchis Café"
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d119460.6725357993!2d-103.3918239!3d20.6737777!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x8428b18cb52fd39f%3A0x2e38a0e0e1a17dc6!2sGuadalajara%2C%20Jal.!5e0!3m2!1ses-419!2smx!4v1700000000000!5m2!1es-419!2smx"
                width="100%"
                height="220"
                style="border: 0;"
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
              ></iframe>
            </div>

            <div class="map-actions">
              <a
                href="https://maps.google.com/?q=Monchis+Cafe+Guadalajara"
                target="_blank"
                rel="noopener noreferrer"
                class="btn btn--secondary btn--sm"
              >
                🗺️ Abrir en Google Maps
              </a>
              <a
                href="https://waze.com/ul?q=Monchis+Cafe"
                target="_blank"
                rel="noopener noreferrer"
                class="btn btn--outline btn--sm"
              >
                🚗 Abrir en Waze
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Sección de Redes Sociales y Comunidad -->
    <section class="section section--alt social-section">
      <div class="container text-center">
        <span class="badge badge--organic">📱 Comunidad Digital</span>
        <h2>Síguenos en Redes Sociales</h2>
        <p class="section__subtitle">
          Entérate de las nuevas cosechas campesinas, promociones de temporada y momentos en barra.
        </p>

        <div class="social-grid">
          <a
            v-for="red in redesSociales"
            :key="red.nombre"
            :href="red.url"
            target="_blank"
            rel="noopener noreferrer"
            :class="['social-card', red.clase, 'card']"
            v-motion-slide-visible-bottom
          >
            <div class="social-card__top">
              <span class="social-card__icon">{{ red.icono }}</span>
              <span class="social-card__platform">{{ red.nombre }}</span>
            </div>
            <strong class="social-card__handle">{{ red.usuario }}</strong>
            <p class="social-card__desc">{{ red.descripcion }}</p>
            <span class="social-card__link">Seguir Comunidad →</span>
          </a>
        </div>
      </div>
    </section>

    <!-- Sección de Preguntas Frecuentes (FAQ) -->
    <section class="section faq-section">
      <div class="container">
        <div class="text-center" style="margin-bottom: 2.5rem;">
          <span class="badge badge--commercial">💡 Preguntas Frecuentes</span>
          <h2>Todo lo que necesitas saber antes de visitarnos</h2>
          <p class="section__subtitle">
            Respuestas rápidas a las consultas más comunes de nuestros clientes y amigos.
          </p>
        </div>

        <div class="faq-container">
          <div
            v-for="(faq, idx) in faqs"
            :key="idx"
            :class="['faq-item', 'card', { active: faqAbierto === idx }]"
            @click="toggleFaq(idx)"
          >
            <div class="faq-question">
              <h4>{{ faq.pregunta }}</h4>
              <span class="faq-arrow">{{ faqAbierto === idx ? '−' : '+' }}</span>
            </div>
            <div v-show="faqAbierto === idx" class="faq-answer">
              <p>{{ faq.respuesta }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Banner Final CTA de WhatsApp -->
    <section class="section whatsapp-cta-section">
      <div class="container">
        <div class="whatsapp-cta card text-center">
          <span class="whatsapp-cta__emoji">☕💬</span>
          <h2>¿Prefieres atención personalizada al instante?</h2>
          <p>
            Escríbenos por WhatsApp para consultar la disponibilidad de tus bebidas favoritas o
            apartar tus bolsas de café en grano recién tostado.
          </p>
          <div class="whatsapp-cta__buttons">
            <a
              href="https://wa.me/5213300000000?text=%C2%A1Hola%20Monchis%20Caf%C3%A9!%20Quiero%20hacer%20un%20pedido%20para%20recoger."
              target="_blank"
              rel="noopener noreferrer"
              class="btn btn--whatsapp"
            >
              💬 WhatsApp: Pedidos para Llevar
            </a>
            <a
              href="https://wa.me/5213300000000?text=%C2%A1Hola!%20Represento%20a%20productores%20campesinos%20y%20deseo%20m%C3%A1s%20informaci%C3%B3n."
              target="_blank"
              rel="noopener noreferrer"
              class="btn btn--outline"
            >
              🌱 WhatsApp: Productores & Alianzas
            </a>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.contact-page {
  padding-bottom: 3rem;
}

/* --- Hero --- */
.contact-hero {
  padding: 4rem 1rem 2rem;
  background: linear-gradient(180deg, rgba(243, 201, 201, 0.2) 0%, transparent 100%);
}

.contact-hero__lead {
  font-size: 1.15rem;
  margin: 1rem auto 0;
  max-width: 680px;
}

/* --- Canales Directos --- */
.channels-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.25rem;
  margin-top: 1rem;
}

.channel-card {
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  text-decoration: none;
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
}

.channel-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.channel-card__icon {
  font-size: 2rem;
  margin-bottom: 0.75rem;
}

.channel-card__badge {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-primary-dark);
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
  display: inline-block;
}

.channel-card h3 {
  font-size: 1.15rem;
  margin-bottom: 0.4rem;
  color: var(--color-text-main);
}

.channel-card p {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  line-height: 1.4;
  margin-bottom: 1rem;
  flex-grow: 1;
}

.channel-card__action {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--color-primary-dark);
}

.channel-card--whatsapp {
  border-color: rgba(37, 211, 102, 0.3);
  background: linear-gradient(135deg, #ffffff 0%, rgba(37, 211, 102, 0.05) 100%);
}

.channel-card--whatsapp .channel-card__badge {
  color: #128c7e;
}

.channel-card--whatsapp .channel-card__action {
  color: #128c7e;
}

/* --- Grid Principal (Formulario + Información) --- */
.main-contact-grid {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 2rem;
  align-items: start;
}

@media (max-width: 900px) {
  .main-contact-grid {
    grid-template-columns: 1fr;
  }
}

/* Formulario */
.contact-form-column {
  padding: 2.2rem;
}

.form-header {
  margin-bottom: 1.5rem;
}

.form-header h2 {
  font-size: 1.7rem;
  margin-top: 0.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

.form-group {
  margin-bottom: 1.25rem;
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  font-size: 0.88rem;
  margin-bottom: 0.4rem;
  color: var(--color-text-main);
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.92rem;
  background: var(--color-bg-base);
  color: var(--color-text-main);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--color-primary-dark);
  box-shadow: 0 0 0 3px rgba(217, 140, 127, 0.15);
}

.legal-consent {
  margin-bottom: 1.5rem;
}

.consent-label {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  cursor: pointer;
  font-size: 0.85rem;
  color: var(--color-text-muted);
  line-height: 1.4;
}

.consent-label input {
  margin-top: 0.2rem;
  accent-color: var(--color-primary-dark);
}

.btn--submit {
  width: 100%;
  padding: 0.9rem;
  font-size: 1rem;
}

.success-banner {
  background: rgba(183, 217, 177, 0.25);
  border: 1px solid var(--color-success);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.success-banner__icon {
  font-size: 2rem;
}

.success-banner h4 {
  color: #2e5927;
  margin-bottom: 0.3rem;
}

.success-banner p {
  color: #3b5e34;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

/* --- Columna Derecha: Horarios, Amenidades, Mapa --- */
.contact-info-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.hours-card {
  padding: 1.5rem;
}

.hours-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.hours-header h3 {
  font-size: 1.15rem;
}

.status-pill {
  font-size: 0.78rem;
  font-weight: 700;
  padding: 0.3rem 0.75rem;
  border-radius: var(--radius-full);
}

.status-pill--open {
  background: #e6f7e4;
  color: #276721;
  border: 1px solid #b7d9b1;
}

.status-pill--closed {
  background: #fdf2e9;
  color: #9c5221;
  border: 1px solid #f5d59e;
}

.hours-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.hours-list li {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px dashed var(--color-border);
}

.hours-footer {
  margin-top: 0.8rem;
  font-size: 0.8rem;
  color: var(--color-text-muted);
}

/* Amenidades */
.amenities-card {
  padding: 1.5rem;
}

.amenities-card h4 {
  font-size: 1.05rem;
  margin-bottom: 1rem;
}

.amenities-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 500px) {
  .amenities-grid {
    grid-template-columns: 1fr;
  }
}

.amenity-item {
  display: flex;
  gap: 0.6rem;
  align-items: flex-start;
}

.amenity-icon {
  font-size: 1.4rem;
  line-height: 1;
}

.amenity-item strong {
  display: block;
  font-size: 0.85rem;
  color: var(--color-text-main);
}

.amenity-item small {
  display: block;
  font-size: 0.75rem;
  color: var(--color-text-muted);
  line-height: 1.3;
}

/* Mapa */
.map-card {
  padding: 1.5rem;
}

.map-header {
  margin-bottom: 0.8rem;
}

.map-header h4 {
  font-size: 1.05rem;
}

.map-header p {
  font-size: 0.85rem;
  color: var(--color-text-muted);
}

.map-embed-container {
  border-radius: var(--radius-sm);
  overflow: hidden;
  margin-bottom: 1rem;
  border: 1px solid var(--color-border);
}

.map-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

/* --- Redes Sociales --- */
.social-section {
  padding: 3rem 0;
}

.social-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.25rem;
  margin-top: 2rem;
}

.social-card {
  padding: 1.5rem;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  text-align: left;
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
}

.social-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.social-card__top {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.social-card__icon {
  font-size: 1.5rem;
}

.social-card__platform {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-muted);
}

.social-card__handle {
  font-size: 1.1rem;
  color: var(--color-text-main);
  margin-bottom: 0.4rem;
}

.social-card__desc {
  font-size: 0.82rem;
  color: var(--color-text-muted);
  line-height: 1.4;
  margin-bottom: 1rem;
  flex-grow: 1;
}

.social-card__link {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--color-primary-dark);
}

/* Estilos Temáticos Sutiles de Redes Sociales */
.social-card--instagram:hover {
  border-color: rgba(225, 48, 108, 0.4);
}
.social-card--facebook:hover {
  border-color: rgba(24, 119, 242, 0.4);
}
.social-card--tiktok:hover {
  border-color: rgba(0, 0, 0, 0.4);
}
.social-card--spotify:hover {
  border-color: rgba(30, 215, 96, 0.4);
}

/* --- FAQ Acordeón --- */
.faq-section {
  padding: 3rem 0;
}

.faq-container {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.faq-item {
  padding: 1.25rem 1.5rem;
  cursor: pointer;
  transition: background-color var(--transition-fast);
}

.faq-item.active {
  border-color: var(--color-primary-dark);
}

.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.faq-question h4 {
  font-size: 1rem;
  margin: 0;
}

.faq-arrow {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--color-primary-dark);
}

.faq-answer {
  margin-top: 0.8rem;
  padding-top: 0.8rem;
  border-top: 1px solid var(--color-border);
}

.faq-answer p {
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--color-text-muted);
}

/* --- WhatsApp CTA --- */
.whatsapp-cta-section {
  padding-top: 1rem;
}

.whatsapp-cta {
  padding: 3rem 2rem;
  background: linear-gradient(135deg, rgba(243, 201, 201, 0.3) 0%, rgba(201, 168, 139, 0.15) 100%);
}

.whatsapp-cta__emoji {
  font-size: 2.5rem;
  display: block;
  margin-bottom: 0.5rem;
}

.whatsapp-cta h2 {
  font-size: 1.8rem;
  margin-bottom: 0.6rem;
}

.whatsapp-cta p {
  margin: 0 auto 1.5rem;
  max-width: 600px;
}

.whatsapp-cta__buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn--whatsapp {
  background: #25d366;
  color: #ffffff;
  border: none;
  font-weight: 700;
  box-shadow: 0 4px 14px rgba(37, 211, 102, 0.3);
}

.btn--whatsapp:hover {
  background: #1ebc59;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(37, 211, 102, 0.4);
}
</style>
