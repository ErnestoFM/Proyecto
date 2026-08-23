# Monchis Café — Plataforma Web Segura para Cafetería Orgánica y Comercial

## 1. Características del Proyecto Final

### 1.1 Problemática y Contexto del Negocio
**Monchis Café** es una cafetería familiar ubicada en una zona rural/suburbana que ofrece café orgánico de alta calidad mediante proveedores regionales de especialidad, junto con productos complementarios comerciales (galletas, leches vegetales, repostería).

**Situación Actual:**
- Falta de control digital de inventario, pedidos y trazabilidad de lotes de café orgánico (finca de origen, fecha de tostado/cosecha, caducidad).
- Control de caja manual y vulnerable a discrepancias.
- Ausencia de analítica sobre clientes y origen de tráfico (visitas desde Google Maps, campañas en Instagram, tráfico directo).
- Carencia de mecanismos modernos de fidelización y seguridad web (protección contra bots, transacciones inconsistentes y ataques web).

### 1.2 Objetivo General
Desarrollar la plataforma web integral y segura de **Monchis Café** en arquitectura **Monorepo** (Frontend Vue 3 con Vite + Backend Next.js API Routes) orientada a eventos con **RabbitMQ y Patrón Saga (Reversas)**, autenticación stateless (**JWT + Google reCAPTCHA**), panel de administración con **atribución de tráfico**, sistema de **SEO con prerenderizado (`vite-ssg`)** y diseño UI/UX cálido pastel, garantizado mediante metodología **TDD** y testing multicapa.

### 1.3 Alineación con los Objetivos de Desarrollo Sostenible (ODS)
- **ODS 8: Trabajo decente y crecimiento económico:** Optimización operativa y digitalización del punto de venta.
- **ODS 9: Industria, innovación e infraestructura:** Arquitectura moderna en monorepo, eventos asíncronos con RabbitMQ y contenedorización Docker.
- **ODS 12: Producción y consumo responsables:** Trazabilidad estricta de café orgánico, bonificaciones por tazas/termos reutilizables y control de mermas.
- **ODS 16: Paz, justicia e instituciones sólidas:** Protección de datos, autenticación stateless robusta, auditoría de eventos y transacciones transparentes.

---

## 2. Estructura y Módulos del Sistema

### 2.1 Módulo de Autenticación Stateless y Seguridad
- **Login / Registro:** Autenticación stateless mediante **JWT** (Access Token de corta duración en memoria + Refresh Token en cookie `httpOnly + Secure + SameSite=Strict` con rotación).
- **Protección Anti-Bot:** Integración obligatoria de **Google reCAPTCHA v2/v3** en formularios de acceso y registro.
- **Control de Acceso basado en Roles (RBAC):** Roles definidos (`admin`, `cajero`, `cliente`).
- **Doble Factor (2FA):** 2FA obligatorio para el rol Administrador.

### 2.2 Módulo de Trazabilidad y Gestión de Inventario
- **Catálogo Segmentado:** Productos orgánicos (café en grano/molido de especialidad regional) y comerciales (compras mayoristas).
- **Trazabilidad de Lotes Orgánicos:** Registro de proveedor regional, finca/origen, número de lote, fecha de tostado/compra y fecha de caducidad.
- **Alertas de Stock y Vencimiento:** Notificaciones por correo electrónico (SMTP) ante caducidad próxima o mermas.

### 2.3 Módulo de Punto de Venta (POS) y Métodos de Pago
- **Registro de Ventas Ágil:** Soporte para lectura de código de barras e ingreso manual.
- **Métodos de Pago:**
  1. `Efectivo` (cálculo automático de cambio).
  2. `Tarjeta de Crédito / Débito`.
  3. `Transferencia / SPEI` (registro de clave de rastreo / referencia bancaria).
  4. `Puntos de Lealtad / Monedero Monchis`.
  5. `Pago Mixto`.
- **Transacciones Distribuidas con RabbitMQ (Patrón Saga):**
  - Si una venta se procesa y cobra pero los insumos de café orgánico se agotan en el inventario, el orquestador Saga ejecuta la **Transacción Compensatoria (Reversa)**: emite reembolso, cancela el pedido y notifica al cajero/cliente.
- **Dead Letter Queue (DLQ):** Reintentos progresivos con retraso (10s, 60s, 300s) y desvío a DLQ con alerta por correo SMTP al administrador si se superan los límites.

### 2.4 Programa de Fidelización: "Monchis Rewards"
1. **Sellos Digitales (Bebidas preparadas):** Por cada café preparado, 1 sello digital. Al acumular 7 sellos, el **8vo café es gratis**.
2. **Puntos Cashback (Café en grano y productos):** 1 punto por cada $10 MXN gastados ($1 MXN de saldo monedero).
3. **Bonificación Ecológica (ODS 12):** Descuento directo o doble puntaje al llevar termo o taza reutilizable.
4. **Bienvenida y Cumpleaños:** Descuento de bienvenida (asociado a la campaña de origen) y cortesía en el mes de cumpleaños.

### 2.5 Panel de Administración y Atribución de Tráfico
- **Métricas de Ventas y Compras:** Ventas totales, ticket promedio, desglose orgánico vs comercial y alertas de caducidad.
- **Atribución de Tráfico (Marketing Digital):**
  - Captura y persistencia de `utm_source`, `utm_medium`, `utm_campaign`.
  - Reporte de conversiones: clientes provenientes de **Google Maps** (ficha de Google Business), **Instagram** (posts/reels/historias) y tráfico directo.
- **Exportes:** Generación de reportes semanales en **PDF y Excel**.

---

## 3. Estrategia de SEO y Sistema de Diseño (UI/UX)

### 3.1 SEO y Renderizado Prerenderizado (`vite-ssg`)
- **Páginas Públicas Prerenderizadas:** Landing (`/`), `/nosotros`, `/menu`, `/contacto` prerenderizadas en build time con `vite-ssg` para máxima indexabilidad sin requerir SSR completo.
- **Páginas Privadas SPA:** Rutas `/admin/*` y `/pos` protegidas con `<meta name="robots" content="noindex, nofollow">`.
- **Checklist SEO:**
  - Meta tags dinámicos (`title`, `description`, `og:image`, `twitter:card`) con `@vueuse/head` / `unhead`.
  - `sitemap.xml` y `robots.txt` automáticos.
  - Datos estructurados Schema.org (`LocalBusiness` / `CoffeeShop` para potenciar búsquedas locales y Google Maps).
  - Canonical tags y URLs limpias en `history mode`.

### 3.2 Sistema de Diseño UI/UX: Cálido, Dulce y Pastel
- **Paleta de Colores:**
  - *Rosa suave (Primario):* `#F3C9C9` | *Rosa terracota (Hover/Acentos):* `#D98C7F`
  - *Café con leche (Secundario):* `#C9A88B` | *Café tostado:* `#8C6B52`
  - *Crema cálido (Fondo base):* `#FAF3ED` | *Blanco cálido (Secciones):* `#FFFDFB`
  - *Café oscuro cálido (Texto):* `#4A3B32` | *Café grisáceo (Secundario):* `#8A7A6D`
  - *Verde pastel (Éxito):* `#B7D9B1` | *Rosa-rojo suave (Error):* `#E39A9A`
- **Tipografía:** Encabezados redondeados (*Fraunces* o *Poppins*) y cuerpo legible (*Nunito* o *Inter*).
- **Iconografía:** Phosphor Icons (duotone / rounded).
- **Animaciones y Transiciones de Scroll:** `@vueuse/motion` para micro-interacciones suaves y `GSAP + ScrollTrigger` para transiciones de imágenes al scroll, respetando `prefers-reduced-motion`.

---

## 4. Metodología: TDD por Fases (Sprints)

1. **Fase 0 — Setup del Monorepo:** `pnpm workspaces`, `Turborepo`, linters, CI base.
2. **Fase 1 — Diseño de Arquitectura y Mockups:** Mockups con la paleta de Monchis Café, MER en Prisma, casos de uso Given/When/Then y diagramas de arquitectura.
3. **Fase 2 — Backend Core:** Next.js API, Prisma, JWT stateless, Google reCAPTCHA, RabbitMQ Saga, colas de retardo y DLQ, probados con Supertest y validación Zod.
4. **Fase 3 — Frontend Core:** Vue 3 SPA + `vite-ssg` para SEO, Pinia, tokens de diseño CSS pastel, pruebas Vitest y E2E Playwright.
5. **Fase 4 — Módulo de Negocio:** Insumos orgánicos, trazabilidad de lotes, POS (efectivo, tarjeta, transferencias), orquestador Saga con reversas.
6. **Fase 5 — Panel de Administración:** Dashboard con analítica de ventas y atribución de tráfico (Google Maps vs Instagram).
7. **Fase 6 — QA Integral:**
   - *Viewport / Multi-resolución:* Playwright (360px, 768px, 1024px, 1440px+).
   - *Regresión Visual:* Playwright Screenshot Diff pixel por pixel.
   - *Validación CSS / Media Queries:* Verificación de breakpoints.
   - *Lighthouse CI & axe-core:* Accesibilidad >90 y rendimiento >85.
   - *Seguridad DAST:* OWASP ZAP (XSS, SQLi, CSRF, CSP/HSTS).
8. **Fase 7 — Despliegue e Infraestructura:** Docker Compose, Terraform y GitHub Actions.
