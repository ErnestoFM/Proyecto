<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router';
import { useHead } from '@vueuse/head';
import { computed } from 'vue';
import AppNavbar from '@/components/layout/AppNavbar.vue';
import AppFooter from '@/components/layout/AppFooter.vue';
import CookieBanner from '@/components/common/CookieBanner.vue';

const route = useRoute();
const APP_URL = 'https://monchiscafe.com';

useHead({
  title: computed(() => (route.meta.title as string) || 'Monchis Café — Café Orgánico de Especialidad'),
  meta: computed(() => {
    const currentTitle = (route.meta.title as string) || 'Monchis Café — Café Orgánico de Especialidad';
    const currentDesc =
      'Monchis Café — Granos de altura 100% orgánicos cosechados en Chiapas y Oaxaca. Tostado artesanal, repostería casera y programa Monchis Rewards.';

    const metaList: any[] = [
      // Primarias SEO
      { name: 'description', content: currentDesc },
      { name: 'keywords', content: 'café orgánico, café de especialidad, Chiapas, Oaxaca, café de olla, Monchis Café, cafetería pet friendly, comercio justo' },
      { name: 'author', content: 'Monchis Café' },

      // Open Graph / Facebook / WhatsApp
      { property: 'og:site_name', content: 'Monchis Café' },
      { property: 'og:title', content: currentTitle },
      { property: 'og:description', content: currentDesc },
      { property: 'og:type', content: 'website' },
      { property: 'og:url', content: `${APP_URL}${route.path}` },
      { property: 'og:image', content: `${APP_URL}/og-image.jpg` },
      { property: 'og:image:alt', content: 'Monchis Café — Café Orgánico de Especialidad y Repostería' },
      { property: 'og:image:width', content: '1200' },
      { property: 'og:image:height', content: '630' },
      { property: 'og:locale', content: 'es_MX' },

      // Twitter Cards
      { name: 'twitter:card', content: 'summary_large_image' },
      { name: 'twitter:title', content: currentTitle },
      { name: 'twitter:description', content: currentDesc },
      { name: 'twitter:image', content: `${APP_URL}/og-image.jpg` },
    ];

    // Directiva noindex para rutas privadas
    if (route.meta.noIndex) {
      metaList.push({ name: 'robots', content: 'noindex, nofollow' });
    } else {
      metaList.push({ name: 'robots', content: 'index, follow, max-image-preview:large' });
    }

    return metaList;
  }),
  link: computed(() => [
    { rel: 'canonical', href: `${APP_URL}${route.path}` },
  ]),
  script: [
    // Datos Estructurados Schema.org para Google Search & Google Maps
    {
      type: 'application/ld+json',
      children: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'CafeOrCoffeeShop',
        name: 'Monchis Café',
        image: 'https://monchiscafe.com/og-image.jpg',
        '@id': 'https://monchiscafe.com',
        url: 'https://monchiscafe.com',
        telephone: '+52-XXX-XXX-XXXX',
        priceRange: '$$',
        servesCuisine: 'Café de Especialidad, Repostería Artesanal, Café Orgánico',
        address: {
          '@type': 'PostalAddress',
          streetAddress: 'Corredor Verde Principal',
          addressLocality: 'Zona Suburbana',
          addressRegion: 'México',
          addressCountry: 'MX',
        },
        geo: {
          '@type': 'GeoCoordinates',
          latitude: 19.4326,
          longitude: -99.1332,
        },
        openingHoursSpecification: [
          {
            '@type': 'OpeningHoursSpecification',
            dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            opens: '07:30',
            closes: '20:30',
          },
          {
            '@type': 'OpeningHoursSpecification',
            dayOfWeek: 'Sunday',
            opens: '08:30',
            closes: '18:00',
          },
        ],
        sameAs: [
          'https://instagram.com/monchiscafe',
          'https://facebook.com/monchiscafe',
        ],
      }),
    },
  ],
});
</script>

<template>
  <div id="monchis-app">
    <AppNavbar />
    <main>
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>
    <AppFooter />
    <CookieBanner />
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-normal);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

#monchis-app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
}
</style>
