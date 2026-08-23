import { ViteSSG } from 'vite-ssg';
import { createPinia } from 'pinia';
import { createHead } from '@vueuse/head';
import { MotionPlugin } from '@vueuse/motion';
import App from './App.vue';
import { routes } from './router';
import { setupAuthGuard } from './composables/useAuthGuard';
import './assets/main.css';

export const createApp = ViteSSG(App, { routes }, ({ app, router, isClient }) => {
  const pinia = createPinia();
  const head = createHead();

  app.use(pinia);
  app.use(head);
  app.use(MotionPlugin);

  // Solo aplicar guards en el cliente (no durante SSG)
  if (isClient) {
    setupAuthGuard(router);
  }
});
