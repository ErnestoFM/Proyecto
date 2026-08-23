// Extensión de tipos de vue-router para meta de rutas
import 'vue-router';
import type { UserRole } from '@monchis/shared-types';

declare module 'vue-router' {
  interface RouteMeta {
    /** Ruta pública (no requiere autenticación) */
    public?: boolean;
    /** Requiere usuario autenticado */
    requiresAuth?: boolean;
    /** Roles permitidos (RBAC) */
    roles?: UserRole[];
    /** No indexar en buscadores */
    noIndex?: boolean;
    /** Título para useHead/SEO */
    title?: string;
  }
}
