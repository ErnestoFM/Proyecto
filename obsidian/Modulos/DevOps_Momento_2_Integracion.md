# Módulo: Desarrollo e Integración Continua — Momento 2 (Equipo 2)

#devops #integracion_continua #momento2 #equipo2 #gitflow #vitest #mvp #seguridad #devsecops #monchis_cafe

Nota técnica y estratégica que documenta la fase de **Desarrollo e Integración Continua (Momento 2)** para el proyecto **"Gestión Web Segura para Cafetería Orgánica y Comercial"** ([[Contexto/Index|Monchis Café]]), en cumplimiento de las directrices académicas del **Dr. Gabriel Navarro Salcedo** para la cátedra de **Productos Integradores de Desarrollo de Software** (Universidad de Guadalajara / CUTonalá).

---

## 1. Evidencias del Control de Versiones (SCM GitHub)

- **Repositorio Central:** `https://github.com/ErnestoFM/Proyecto`
- **Estructura Monorepo:** Turborepo + pnpm workspaces con paquetes desacoplados:
  - `apps/web`: Frontend Vue 3 + Vite + vite-ssg + Pinia
  - `apps/api`: Backend API RESTful en Node.js + Next.js Route Handlers
  - `packages/database`: Prisma ORM con PostgreSQL 15
  - `packages/messaging`: AMQP RabbitMQ Saga Orchestrator y Dead Letter Queue (DLQ)
- **Estrategia GitFlow:**
  - `master` / `main`: Rama de producción estable.
  - `develop`: Rama de integración activa para Pull Requests y validación de CI.
  - `feature/auth-rbac-recaptcha`: Desarrollo de autenticación stateless, roles RBAC y Google reCAPTCHA.
  - `feature/pos-trazabilidad-ods12`: Desarrollo del Punto de Venta (POS) táctil y trazabilidad ODS 12.
- **Convención Semántica:** Conventional Commits (`feat:`, `fix:`, `test:`, `docs:`, `infra:`).

---

## 2. Testing Automatizado Multicapa (Vitest)

Ejecución y aprobación ininterrumpida de **77 pruebas unitarias** en el pipeline de CI:

1. **Backend API (`apps/api`):** 5 suites de prueba, **47 pruebas unitarias aprobadas**:
   - `auth.test.ts` (17 pruebas): JWT rotativos, Refresh Tokens en cookies `httpOnly`, validación estricta de Google reCAPTCHA v2/v3 sin bypass y revocación activa de tokens (Blacklist en logout).
   - `totp.test.ts` (11 pruebas): 2FA / TOTP (RFC 6238), códigos QR Base32 y prevención de reutilización de tokens temporales.
   - `business.test.ts` (11 pruebas): Lógica de cobro POS, bonificación ecológica directa de **$5.00 MXN** y sellos dobles (ODS 12 - Meta 12.5), y monedero Monchis Rewards.
   - `email.test.ts` (5 pruebas): Notificaciones SMTP ante fallos en colas DLQ y alertas de caducidad de lotes.
   - `admin.test.ts` (3 pruebas): Métricas de ventas y atribución de tráfico mediante parámetros UTM (`utm_source`, `utm_medium`, `utm_campaign`).
2. **Frontend Web (`apps/web`):** 4 suites de prueba, **30 pruebas unitarias aprobadas**:
   - `posStore.test.ts` (9 pruebas): Carrito táctil, cálculo de cambio en efectivo y selector de termo reutilizable.
   - `authStore.test.ts` (13 pruebas): Gestión reactiva de tokens en memoria y guards de navegación por roles.
   - `adminStore.test.ts` (4 pruebas): Indicadores KPI y gráficos de rendimiento de ventas.
   - `cookieStore.test.ts` (4 pruebas): Gestión de consentimiento y almacenamiento de sesión seguro.

---

## 3. Características del Prototipo Funcional (MVP)

- **Punto de Venta (POS) de Mostrador:** Cobro simultáneo en efectivo, tarjeta bancaria, SPEI y puntos de lealtad, adaptado a resoluciones táctiles de barra.
- **Sostenibilidad ODS 12:** Descuento directo por uso de envase reutilizable y trazabilidad por cooperativa campesina regional (Michoacán, Chiapas y Oaxaca) con rotación PEPS.
- **Ciberseguridad y RBAC:** Sesiones stateless blindadas, doble factor obligatorio para administradores y protección anti-bots en capas perimetrales.
- **Resiliencia Transaccional:** Compensación automática de transacciones con RabbitMQ (Patrón Saga) y desvío a colas Dead Letter Queue (DLQ).

---

## 4. Reporte de Errores y Métrica DevSecOps

**Métrica Oficial Asignada:** Cantidad de vulnerabilidades y errores corregidos.  
**Resultado:** **5 incidentes críticos corregidos y documentados**:
- **BUG-001 (Seguridad - Alta):** Corrección de bypass en reCAPTCHA cuando faltaba clave secreta -> Rechazo estricto sin bypass.
- **BUG-002 (Disponibilidad - Media):** Timeout de 5000ms en tests de blacklist sin base de datos -> Inclusión de cláusula de guarda `NODE_ENV === 'test'` y caché en memoria O(1).
- **BUG-003 (Consistencia - Alta):** Desincronización de inventario en cobros concurrentes -> Implementación de transacción compensatoria Saga en RabbitMQ.
- **BUG-004 (Compilación - Media):** Error de SSR en `vite-ssg build` por acceso a `window`/`localStorage` -> Encapsulación en hook `onMounted` y directivas `noindex`.
- **BUG-005 (Usabilidad - Baja):** Desbordamiento de botones POS en pantallas de 768px -> Refactorización con CSS Grid fluido y áreas de toque mínimas de 48px (WCAG 2.1).

---

## 5. Entregables Oficiales Generados

- [`Proyecto_Equipo2_Momento2_Integracion.pdf`](file:///d:/ernestofm/Proyecto/docs/entregables/Proyecto_Equipo2_Momento2_Integracion.pdf)
- [`Proyecto_MonchisCafe_Momento2_Integracion.pdf`](file:///d:/ernestofm/Proyecto/docs/entregables/Proyecto_MonchisCafe_Momento2_Integracion.pdf)
- [`Proyecto_Equipo2_Momento2_Integracion.docx`](file:///d:/ernestofm/Proyecto/docs/entregables/Proyecto_Equipo2_Momento2_Integracion.docx)
- [`Proyecto_Equipo2_Momento2_Integracion.md`](file:///d:/ernestofm/Proyecto/docs/entregables/Proyecto_Equipo2_Momento2_Integracion.md)
- Copias listas para entrega en `C:\Users\erfierro\Downloads\`.

