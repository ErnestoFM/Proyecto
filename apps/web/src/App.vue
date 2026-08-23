<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router';
import { useHead } from '@vueuse/head';
import { computed } from 'vue';
import AppNavbar from '@/components/layout/AppNavbar.vue';
import AppFooter from '@/components/layout/AppFooter.vue';
import CookieBanner from '@/components/common/CookieBanner.vue';

const route = useRoute();

useHead({
  title: computed(() => (route.meta.title as string) || 'Monchis Café'),
  meta: computed(() => {
    const meta: any[] = [
      { name: 'description', content: 'Monchis Café — Café orgánico de especialidad de proveedores regionales. Disfruta la mejor experiencia cafetera en un ambiente cálido y acogedor.' },
      { property: 'og:title', content: (route.meta.title as string) || 'Monchis Café' },
      { property: 'og:description', content: 'Café orgánico de especialidad, lotes trazables y la mejor repostería artesanal.' },
      { property: 'og:type', content: 'website' },
      { name: 'twitter:card', content: 'summary_large_image' },
    ];

    if (route.meta.noIndex) {
      meta.push({ name: 'robots', content: 'noindex, nofollow' });
    }

    return meta;
  }),
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
