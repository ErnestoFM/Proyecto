// ==============================================================================
// Navigation Guard — Protección de rutas autenticadas
// ==============================================================================

import type { Router } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

export function setupAuthGuard(router: Router) {
  router.beforeEach(async (to, _from, next) => {
    const auth = useAuthStore();

    // Rutas públicas no requieren verificación
    if (to.meta.public && !to.meta.requiresAuth) {
      return next();
    }

    // Si no hay token, intentar refresh silencioso
    if (!auth.isAuthenticated) {
      const refreshed = await auth.refreshSession();
      if (!refreshed) {
        return next({ name: 'Login', query: { redirect: to.fullPath } });
      }
    }

    // Verificar roles si la ruta lo requiere
    if (to.meta.roles && Array.isArray(to.meta.roles)) {
      const userRole = auth.userRole;
      if (!userRole || !to.meta.roles.includes(userRole)) {
        return next({ name: 'Dashboard' });
      }
    }

    next();
  });
}
