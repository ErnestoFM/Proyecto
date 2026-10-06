# Monchis Café — Registro de Pendientes, Deuda Técnica y Auditoría de Seguridad

Este documento reúne de forma exhaustiva todos los pendientes, elementos simulados en memoria (mocks), malas prácticas de seguridad y discrepancias detectadas frente a los requerimientos funcionales y técnicos del proyecto.

---

## 🚨 Prioridad 1: Seguridad Crítica y Vulnerabilidades

- [x] **1.1. Eliminar secretos JWT quemados (Hardcoded Secret Fallback)** — *RESUELTO (2026-10-06)*
  - **Ubicación:** `apps/api/src/lib/jwt.ts`.
  - **Resolución:** Se implementó `getSecret()`, lanzando error crítico en producción si faltan variables y usando valores efímeros alertados solo en desarrollo/test.

- [x] **1.2. Impedir manipulación de precios desde el cliente en el POS** — *RESUELTO (2026-10-06)*
  - **Ubicación:** `apps/api/src/app/api/pos/orders/route.ts`.
  - **Resolución:** El backend ahora valida y utiliza los precios oficiales del catálogo de servidor para cada `productoId`, blindando el cálculo de subtotal contra manipulación del JSON del cliente.

- [x] **1.3. Forzar reCAPTCHA estricto y evitar bypass silencioso** — *RESUELTO (2026-10-06)*
  - **Ubicación:** `apps/api/src/lib/recaptcha.ts`.
  - **Resolución:** Se eliminó el bypass automático en desarrollo (`return process.env.NODE_ENV === 'development'`). En producción se exige estrictamente `RECAPTCHA_SECRET_KEY` y se rechaza cualquier token dummy. En desarrollo/test sólo se admite de forma explícita el token `test-valid-recaptcha-token`; cualquier otro token sin credenciales activas es rechazado con advertencia.

- [x] **1.4. Implementar validación activa de Blacklist de Tokens Revocados** — *RESUELTO (2026-10-06)*
  - **Ubicación:** `apps/api/src/lib/jwt.ts`, `apps/api/src/app/api/auth/logout/route.ts`, `apps/api/src/app/api/auth/refresh/route.ts`, `apps/api/src/middleware/authMiddleware.ts` y rutas protegidas.
  - **Resolución:** Se incorporó el identificador único `jti` (UUID v4) en cada Access Token y Refresh Token generado. Al ejecutar `POST /api/auth/logout`, se extraen e invalidan activamente el Access Token y el Refresh Token en memoria (`REVOKED_TOKENS_CACHE` O(1)) y en PostgreSQL (`prisma.revokedToken`). Tanto el middleware (`requireAuth`) como `verifyAccessTokenAsync` y los endpoints protegidos consultan la blacklist y rechazan con HTTP 401 tokens revocados. Se agregó además rotación de Refresh Tokens en `/api/auth/refresh`.

---

## 💾 Prioridad 2: Persistencia Real vs. Datos Quemados (Mocks en Memoria)

- [ ] **2.1. Conectar y migrar la Base de Datos PostgreSQL**
  - **Ubicación:** `packages/database/prisma/schema.prisma` y `.env`.
  - **Problema:** No existe archivo `.env` configurado ni carpeta de migraciones (`prisma/migrations`). El cliente Prisma nunca ha sincronizado las tablas en una base de datos real.
  - **Solución:** Crear `.env` a partir de `.env.example`, levantar el contenedor de PostgreSQL (`docker compose up postgres -d`) y ejecutar `pnpm prisma:migrate`.

- [x] **2.2. Persistir órdenes en base de datos al cobrar en el POS** — *RESUELTO (2026-10-06)*
  - **Ubicación:** `apps/api/src/app/api/pos/orders/route.ts`.
  - **Resolución:** Se encapsuló la venta en una transacción `prisma.$transaction` que registra `Order` y sus `OrderItem`, decrementa en tiempo real el stock de `Product`, actualiza sellos/puntos de fidelidad en `User` y registra la atribución UTM en `Attribution`, con degradación controlada y orquestación Saga.

- [x] **2.3. Migrar Catálogo de Productos a PostgreSQL** — *RESUELTO (2026-10-06)*
  - **Ubicación:** `apps/api/src/app/api/products/route.ts`.
  - **Resolución:** El endpoint consulta `prisma.product.findMany({ where: { activo: true } })`, mapea tipos fuertemente tipados a `ProductDTO` y cuenta con catálogo de contingencia en caso de desconexión.

- [x] **2.4. Migrar Lotes de Inventario a PostgreSQL** — *RESUELTO (2026-10-06)*
  - **Ubicación:** `apps/api/src/app/api/inventory/batches/route.ts`.
  - **Resolución:** Métodos `GET` y `POST` migrados a consultas directas en `prisma.batch.findMany` y `prisma.batch.create`, persistiendo número de lote, finca de origen, fechas y alertas sanitarias en la base de datos relacional.

- [x] **2.5. Conectar Analítica del Admin a datos reales** — *RESUELTO (2026-10-06)*
  - **Ubicación:** `apps/api/src/app/api/admin/analytics/route.ts`, `apps/api/src/app/api/admin/audit/dlq/route.ts`, `apps/web/src/stores/adminStore.ts` y `apps/web/src/views/admin/AdminPage.vue`.
  - **Resolución:** El backend ahora consulta dinámicamente las órdenes completadas (`prisma.order.findMany`), extrae items y productos vendidos clasificando ingresos de café orgánico vs comercial, agrega canales de tráfico desde la tabla `Attribution`, consulta registros de falla en `SagaStateLog` para la vista de DLQ, y el frontend sincroniza métricas, DLQ y lotes en tiempo real manteniendo tolerancia a fallos offline.

---

## ⚙️ Prioridad 3: Funcionalidades Faltantes (Prometidas en Documentación)

- [x] **3.1. Doble Factor de Autenticación (2FA / TOTP) para Administrador** — *RESUELTO (2026-10-06)*
  - **Ubicación:** `apps/api/src/lib/totp.ts`, `apps/api/src/app/api/auth/2fa/`, `apps/web/src/stores/authStore.ts`, `apps/web/src/views/auth/LoginPage.vue` y `apps/web/src/views/admin/AdminPage.vue`.
  - **Resolución:** Se implementó el servicio criptográfico `TotpService` bajo estándares RFC 6238 y RFC 4226 (secreto Base32, códigos de 6 dígitos con ventana de ±30s, generación de QR con `qrcode` y URLs `otpauth://`). Se crearon endpoints `/api/auth/2fa/setup`, `/api/auth/2fa/enable`, `/api/auth/2fa/verify` y `/api/auth/2fa/disable`. Se integró el desafío de 2FA en el login y un modal de administración en el panel con 11 pruebas unitarias dedicadas.

- [x] **3.2. Consumidor Activo (Worker) de RabbitMQ para Patrón Saga** — *RESUELTO (2026-10-06)*
  - **Ubicación:** `packages/messaging/src/sagaWorker.ts`, `packages/messaging/src/index.ts` y `apps/api/src/app/api/pos/orders/route.ts`.
  - **Resolución:** Se implementó la clase `SagaWorker` para escuchar y coordinar verificaciones de reservas de inventario orgánico. En caso de insumo insuficiente o caducado, orquesta automáticamente la reversa compensatoria (`CANCELADA_REEMBOLSADA`), registra en `SagaStateLog` y emite eventos al exchange `'cafeteria.events'`.

- [ ] **3.3. Servicio de Alertas por Correo SMTP**
  - **Ubicación:** Requerimientos funcionales 2.2 y 2.3 (alertas por caducidad de lotes orgánicos y mensajes caídos en Dead Letter Queue).
  - **Estado:** No existe ningún transporte de correo (ej. Nodemailer) ni plantillas de notificación por email configuradas.

- [x] **3.4. Exportes en PDF y Excel desde el Panel de Administración** — *RESUELTO (2026-10-06)*
  - **Ubicación:** `apps/web/src/views/admin/AdminPage.vue`.
  - **Resolución:** Se agregaron funciones de exportación `exportarExcel()` (generador CSV compatible con Excel en UTF-8 BOM con KPIs, tráfico, productos y lotes) y `exportarPDF()` vía `@media print` estilizado para reporte ejecutivo.

- [x] **3.5. Integración con Periféricos Físicos de Mostrador** — *RESUELTO (2026-10-06)*
  - **Ubicación:** `apps/web/src/views/pos/POSPage.vue`.
  - **Resolución:** Se implementó listener global de eventos `keydown` para escáneres de código de barras USB/HID (1D/2D) mapeados a productos (`7501001` - `7501005`), atajos de mostrador `F2` (Cobrar) y `Escape` (Limpiar), junto con indicador visual de estado en el header.

---

## 🛠️ Prioridad 4: Calidad de Código y Automatización de Pruebas

- [x] **4.1. Reparar el comando `pnpm test` en la raíz** — *RESUELTO (2026-10-06)*
  - **Ubicación:** `packages/database/package.json` y `packages/messaging/package.json`.
  - **Resolución:** Se agregó `--passWithNoTests` a los scripts de prueba en ambos paquetes. `pnpm test` en la raíz ahora ejecuta 7 tareas de Turborepo y pasa 55 pruebas unitarias al 100% en verde.

- [x] **4.3. Automatización de CI en GitHub Actions (.github/workflows/ci.yml)** — *RESUELTO (2026-10-06)*
  - **Ubicación:** `.github/workflows/ci.yml`.
  - **Resolución:** Se reemplazó el placeholder por un pipeline completo que instala pnpm 9, Node 20, corre `pnpm prisma:generate`, `pnpm lint`, `pnpm test` (55 tests) y compila los artefactos de producción (`pnpm build`).

- [x] **4.4. Corrección de Type-Checking y Linting en Monorepo (`pnpm lint`)** — *RESUELTO (2026-10-06)*
  - **Ubicación:** `apps/api/.eslintrc.json`, `apps/api/package.json`, `apps/web/package.json`.
  - **Resolución:** Se configuró verificación estricta de tipos de TypeScript (`tsc --noEmit` en API y `vue-tsc --noEmit` en Web). `pnpm lint` ahora pasa con código de salida 0.

- [x] **2.6. Infraestructura de Base de Datos Gestionada en Google Cloud Platform (Cloud SQL)** — *PREPARADO (2026-10-06)*
  - **Ubicación:** `infra/gcp/setup_cloud_sql.ps1`, `infra/gcp/README.md`, `packages/database/prisma/seed.ts`.
  - **Resolución:** Se desarrolló el script de aprovisionamiento automatizado para Google Cloud SQL (PostgreSQL 15), la guía de conexión segura (Cloud SQL Auth Proxy / IP pública) y el seeder con datos maestros de usuarios, café orgánico de Chiapas/Veracruz, lotes y órdenes.

- [ ] **4.2. Eliminar advertencia de deprecación de Vite Node API (CJS)**
  - **Ubicación:** `apps/api/vitest.config.ts`.
  - **Problema:** En consola aparece `The CJS build of Vite's Node API is deprecated`.
  - **Solución:** Configurar Vitest con formato ESM explícito.
