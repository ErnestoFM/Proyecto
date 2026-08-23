import type { RouteRecordRaw } from 'vue-router';

export const routes: RouteRecordRaw[] = [
  // === Rutas Públicas (Prerenderizadas con vite-ssg para SEO) ===
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/public/HomePage.vue'),
    meta: { public: true, title: 'Monchis Café — Café Orgánico de Especialidad' },
  },
  {
    path: '/nosotros',
    name: 'About',
    component: () => import('@/views/public/AboutPage.vue'),
    meta: { public: true, title: 'Sobre Nosotros — Monchis Café' },
  },
  {
    path: '/menu',
    name: 'Menu',
    component: () => import('@/views/public/MenuPage.vue'),
    meta: { public: true, title: 'Nuestro Menú — Monchis Café' },
  },
  {
    path: '/contacto',
    name: 'Contact',
    component: () => import('@/views/public/ContactPage.vue'),
    meta: { public: true, title: 'Contacto — Monchis Café' },
  },
  {
    path: '/legal',
    name: 'Legal',
    component: () => import('@/views/legal/LegalPage.vue'),
    meta: { public: true, title: 'Centro Legal, Privacidad y Cookies — Monchis Café' },
  },

  // === Rutas de Autenticación ===
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/LoginPage.vue'),
    meta: { public: true, title: 'Iniciar Sesión — Monchis Café', noIndex: true },
  },
  {
    path: '/registro',
    name: 'Register',
    component: () => import('@/views/auth/RegisterPage.vue'),
    meta: { public: true, title: 'Registro — Monchis Café', noIndex: true },
  },

  // === Rutas Protegidas (SPA, no prerenderizadas, noindex) ===
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/dashboard/DashboardPage.vue'),
    meta: { requiresAuth: true, noIndex: true, title: 'Panel — Monchis Café' },
  },
  {
    path: '/pos',
    name: 'POS',
    component: () => import('@/views/pos/POSPage.vue'),
    meta: { requiresAuth: true, roles: ['ADMIN', 'CAJERO'], noIndex: true, title: 'Punto de Venta — Monchis Café' },
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/admin/AdminPage.vue'),
    meta: { requiresAuth: true, roles: ['ADMIN'], noIndex: true, title: 'Administración — Monchis Café' },
  },

  // === 404 ===
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/public/NotFoundPage.vue'),
    meta: { public: true, title: 'Página no encontrada — Monchis Café' },
  },
];
