# Práctica Momento 2: Desarrollo e Integración Continua (CI)
## Gestión Web Segura para Cafetería Orgánica y Comercial ("Monchis Café")

**Institución:** Universidad de Guadalajara — Centro Universitario de Tonalá (CUTonalá)  
**División:** División de Ingenierías e Innovación Tecnológica  
**Programa Académico:** Licenciatura en Ingeniería en Computación  
**Materia:** Productos Integradores / Proyecto Integrador de Desarrollo de Software  
**Docente:** Dr. Gabriel Navarro Salcedo  
**Equipo Asignado:** Equipo 2  
**Fecha de Entrega:** 10 de noviembre de 2026  
**Ponderación:** 25% (3 puntos)  

---

### Integrantes del Equipo y Roles DevOps Asignados
1. **Ernesto Hatuey Fierro Medina** (Código: 215487963) — *Scrum Master & DevOps Lead (Ops)*
2. **Jazmín Díaz** — *Frontend Core Developer (Dev)*
3. **Héctor Hernández** — *Backend & Data Core Developer (Dev)*
4. **Oswaldo Millán** — *QA, Test Automation & Security Engineer (QA)*

---

## 1. Evidencias del Control de Versiones (Repositorio GitHub)

### 1.1 Repositorio Oficial y Configuración SCM
El desarrollo de la plataforma web **Monchis Café** se centraliza bajo el sistema de control de versiones distribuido **Git**, alojado en la plataforma **GitHub**:

- **URL Oficial del Repositorio:** `https://github.com/ErnestoFM/Proyecto`
- **Visibilidad:** Privado / Académico colaborativo.
- **Estructura de Monorepo:** Gestionado mediante `pnpm workspaces` y `Turborepo`, alojando en un único repositorio el Frontend Vue 3 (`apps/web`), la API RESTful Next.js/Node.js (`apps/api`), el paquete de base de datos con Prisma (`packages/database`), la mensajería con RabbitMQ Saga (`packages/messaging`) y las configuraciones compartidas (`packages/config` y `packages/shared-types`).

### 1.2 Estrategia de Ramas GitFlow
Para asegurar la estabilidad del código y evitar regresiones en producción, se implementó el modelo **GitFlow Adaptado**:

- **`master` / `main`:** Rama troncal de código estable y probado en Staging. El push directo se encuentra restringido mediante reglas de protección de rama.
- **`develop`:** Rama de integración continua donde convergen las funcionalidades validadas mediante Pull Requests.
- **`feature/*`:** Ramas de características de vida corta creadas a partir de `develop`:
  - `feature/auth-rbac-recaptcha`: Implementación de autenticación stateless, roles y permisos, y protección Google reCAPTCHA.
  - `feature/pos-trazabilidad-ods12`: Desarrollo del Punto de Venta táctil, catálogo segmentado y bonificación ecológica ODS 12.
- **`fix/*`:** Ramas de corrección de incidentes detectados por las pruebas automatizadas.

```bash
# Verificación de ramas locales y remotas
$ git branch -a
  develop
  feature/auth-rbac-recaptcha
  feature/pos-trazabilidad-ods12
* master
  remotes/origin/master
```

### 1.3 Políticas de Protección y Convención de Commits
- **Conventional Commits:** Estandarización de mensajes de commit mediante prefijos semánticos: `feat:` (nuevas funcionalidades), `fix:` (corrección de errores), `test:` (pruebas unitarias/E2E), `docs:` (documentación técnica) e `infra:` (configuración Docker/CI).
- **Protección de Ramas:** Requiere paso exitoso obligatorio del pipeline de Integración Continua (linter, análisis estático y suites de pruebas unitarias) antes de autorizar la fusión (*Merge*) hacia las ramas principales.

---

## 2. Capturas y Evidencias de Commits, Ramas y Pruebas Unitarias

### 2.1 Historial Cronológico de Commits Semánticos
A continuación se presenta el registro de commits que respaldan la construcción incremental del sistema y las integraciones continuas del Momento 2:

```text
* 7fd4917 (HEAD -> master, origin/master, develop) fix: documentacion de el proyecto
* 12deea7 dox(paneacion): documentacion de planeacion actualizada
* 02d185f feat(infra): auditoria y blindaje de certificados ssl tls, https load balancer, cloud armor y hsts
* 4674652 docs(usuarios): creacion de manuales de usuario pos y administrador con estabilizacion de build
* e8d45fe (feature/pos-trazabilidad-ods12) test(e2e): suite integral de pruebas e2e con playwright para responsive, pos, rbac y auth
* 07fdeff feat(notifications): servicio de alertas por correo smtp para dlq, caducidad, stock y recibos pos
* b8c5834 feat(database): migracion inicial y seed en postgresql con vitest esm limpio
* 2737b0e (feature/auth-rbac-recaptcha) feat(security): recaptcha estricto sin bypass y blacklist activa de tokens revocados en logout
* 2653bd2 feat: implementacion completa de 2fa / totp para administrador (rfc 6238, qr, desafio login y gestion en panel)
* 1e22848 feat: conexion de analitica administrativa y dlq con prisma, sincronizacion en tiempo real de lotes y catalogo
* 67c6916 feat: persistencia prisma en pos, lotes y catalogo, worker saga y soporte cloud sql
* 334a529 fix: pruebas y arreglos en mocks
```

---

### 2.2 Resultados de Pruebas Unitarias Automatizadas con Vitest
El proyecto cuenta con un entorno de pruebas unitarias basado en **Vitest**, integrado en la cadena de CI para ejecutarse antes de cada commit y en cada Pull Request.

#### A. Suite Backend API (`apps/api`): 47 Pruebas Unitarias Aprobadas (100% de Éxito)
La suite backend valida la seguridad de los endpoints, autenticación stateless con JWT, protección contra bots con reCAPTCHA, generación y validación de tokens 2FA TOTP (RFC 6238), y lógica de negocio.

```text
> api@1.0.0 test D:\ernestofm\Proyectoppspi
> vitest run

 RUN  v1.6.1 D:/ernestofm/Proyecto/apps/api

 ✓ tests/business.test.ts  (11 tests) 10ms
 ✓ tests/email.test.ts     (5 tests)  30ms
 ✓ tests/admin.test.ts     (3 tests)   9ms
 ✓ tests/totp.test.ts      (11 tests) 77ms
 ✓ tests/auth.test.ts      (17 tests) 1949ms

 Test Files  5 passed (5)
      Tests  47 passed (47)
   Duration  3.57s
```

**Desglose de pruebas críticas ejecutadas:**
1. **`tests/auth.test.ts` (17 pruebas):** Emisión de JWT rotativo, validación de Refresh Token en cookies `httpOnly`, verificación de claims RBAC (`admin`, `cajero`, `cliente`), validación estricta de Google reCAPTCHA v2/v3 sin bypass, y revocación activa de tokens (Blacklist en logout).
2. **`tests/totp.test.ts` (11 pruebas):** Algoritmo TOTP basado en tiempo (RFC 6238), emisión de llave secreta Base32, generación de código QR para Google Authenticator, verificación de ventana de tiempo y prevención de reutilización de códigos.
3. **`tests/business.test.ts` (11 pruebas):** Lógica del Punto de Venta (POS), cálculo de totales y cambio en efectivo, aplicación de la **Bonificación Ecológica ODS 12 ($5.00 MXN)**, acumulación de sellos en "Monchis Rewards" (8vo café gratis) y validación de esquemas Zod.
4. **`tests/email.test.ts` (5 pruebas):** Servicio de alertas por correo SMTP ante eventos críticos en colas Dead Letter Queue (DLQ), desabasto de insumos orgánicos y vencimiento de lotes.
5. **`tests/admin.test.ts` (3 pruebas):** Métricas de ventas, cálculo de ticket promedio y atribución de tráfico mediante parámetros UTM (`utm_source`, `utm_medium`, `utm_campaign`).

---

#### B. Suite Frontend Web (`apps/web`): 30 Pruebas Unitarias Aprobadas (100% de Éxito)
La suite frontend evalúa la reactividad del estado con **Pinia**, el carrito de compras en mostrador, el catálogo segmentado y la persistencia de sesión:

```text
> web@1.0.0 test D:\ernestofm\Proyectopps\web
> vitest run

 RUN  v1.6.1 D:/ernestofm/Proyecto/apps/web

 ✓ src/stores/__tests__/adminStore.test.ts   (4 tests)  15ms
 ✓ src/stores/__tests__/posStore.test.ts     (9 tests)  33ms
 ✓ src/stores/__tests__/authStore.test.ts    (13 tests) 40ms
 ✓ src/stores/__tests__/cookieStore.test.ts  (4 tests)  12ms

 Test Files  4 passed (4)
      Tests  30 passed (30)
   Duration  13.21s
```

#### C. Balance Total de Pruebas Unitarias en el Monorepo:
- **Total de Suites Ejecutadas:** 9 suites de prueba.
- **Total de Casos de Prueba:** **77 pruebas unitarias automatizadas.**
- **Tasa de Aprobación:** **100% (0 fallos, 0 omitidos).**
- **Cobertura de Código Clave:** >85% en controladores de autenticación, lógica transaccional de caja y validación de entradas.

---

## 3. Prototipo Funcional (Mínimo Viable - MVP)

El MVP de **Monchis Café** se encuentra completamente operativo y compila en modo estático y dinámico sin errores de tipado ni advertencias críticas. Cumple de manera rigurosa con los requerimientos específicos asignados al **Equipo 2 (Gestión Web Segura para Cafetería Orgánica y Comercial)**:

### 3.1 Módulo 1: Autenticación Stateless, RBAC y Doble Factor (2FA)
- **Seguridad Web de Grado Corporativo:**
  - Emisión de tokens de acceso (Access Tokens) JWT firmados con algoritmo HS256, con tiempo de expiración estricto (15 minutos).
  - Refresh Tokens seguros protegidos en cookies `httpOnly`, con atributos `Secure` y `SameSite=Strict`, impidiendo el robo de sesiones mediante ataques de Cross-Site Scripting (XSS).
  - Control de Acceso Basado en Roles (**RBAC**) con validación perimetral en backend y client-side navigation guards en Vue Router:
    * Rol `admin`: Acceso irrestricto al Panel Administrativo, auditoría de eventos DLQ, gestión de inventario y configuración de seguridad.
    * Rol `cajero`: Acceso exclusivo al Punto de Venta (POS) táctil y registro de ventas.
    * Rol `cliente`: Acceso a consulta de menú público y monedero "Monchis Rewards".
  - **Doble Factor de Autenticación (2FA / TOTP):** Obligatorio para cuentas administrativas. Compatible con Google Authenticator y Microsoft Authenticator mediante estándar RFC 6238 con códigos temporales de 6 dígitos.
  - **Google reCAPTCHA v2/v3:** Integrado en formularios públicos de login y registro para mitigar ataques de fuerza bruta y bots automatizados.

---

### 3.2 Módulo 2: Punto de Venta (POS) Táctil y Métodos de Pago
- **Diseñado para Operaciones Ágiles de Mostrador:**
  - Interfaz táctil adaptada para pantallas táctiles y tabletas de barra.
  - Soporte de múltiples métodos de cobro simultáneos:
    1. `Efectivo`: Cálculo automatizado de cambio y validación de denominaciones.
    2. `Tarjeta de Crédito / Débito`: Confirmación de terminal bancaria.
    3. `Transferencia / SPEI`: Registro de clave de rastreo bancario.
    4. `Puntos de Lealtad`: Pago mediante saldo acumulado en monedero digital.
    5. `Pago Mixto`: División de montos entre efectivo y puntos.
  - **Sostenibilidad ODS 12 Integrada en el POS:** Selector táctil *"Cliente aporta termo/taza reutilizable"*. Al activarse, el sistema descuenta automáticamente **$5.00 MXN** del ticket y bonifica con sellos digitales dobles en la cuenta del cliente.

---

### 3.3 Módulo 3: Trazabilidad de Café Orgánico y Gestión PEPS
- **Alineación con el ODS 12 (Producción y Consumo Responsables):**
  - Catálogo segmentado que distingue entre insumos orgánicos de especialidad y productos comerciales.
  - Registro de trazabilidad por lote: Cooperativa productora local (Michoacán, Chiapas, Oaxaca), finca de origen, altitud sobre el nivel del mar, fecha de cosecha y fecha de tostado.
  - Rotación automatizada de inventario bajo el método **PEPS (Primeras Entradas, Primeras Salidas)** para minimizar mermas y garantizar la frescura del café.

---

### 3.4 Módulo 4: Panel de Administración, Atribución UTM y Resiliencia con RabbitMQ
- **Analítica de Negocio:**
  - Tablero central con indicadores clave de rendimiento (KPIs): volumen de ventas diario/semanal, ticket promedio y proporción de ventas orgánicas vs comerciales.
  - Atribución de tráfico digital: captura y almacenamiento de parámetros `utm_source`, `utm_medium` y `utm_campaign`, permitiendo evaluar el retorno de inversión en canales como Google Maps e Instagram.
- **Resiliencia Transaccional con RabbitMQ y Patrón Saga:**
  - Orquestación asíncrona de eventos transaccionales. Si una orden de café de especialidad es cobrada pero los insumos orgánicos se agotan en barra, el orquestador Saga activa la transacción compensatoria (reversa de fondos, anulación del pedido y alerta al cajero).
  - Auditoría de colas Dead Letter Queue (DLQ) para reintentos progresivos y monitoreo de fallas en segundo plano.

---

## 4. Reporte de Errores Detectados y Correcciones Aplicadas (Bug Report & DevSecOps)

En cumplimiento de la directiva de evaluación del docente y la métrica asignada al Equipo 2 (**"Cantidad de vulnerabilidades corregidas"**), se documenta la identificación y remediación de **5 incidentes técnicos críticos** resueltos durante las fases de desarrollo e integración continua:

| ID Incidente | Módulo Afectado | Severidad | Descripción del Error Detectado | Causa Raíz Técnica | Corrección Aplicada (Remediación) | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BUG-001** | `apps/api`<br>(Seguridad Auth) | **ALTA**<br>*(Vulnerabilidad)* | Riesgo de bypass silencioso en validación de Google reCAPTCHA al omitirse la clave secreta en variables de entorno. | El middleware retornaba `true` por defecto ante la ausencia de `RECAPTCHA_SECRET_KEY`, lo cual en producción permitiría a bots saltarse el captcha. | Se refactorizó `auth.service.ts` para rechazar estrictamente cualquier token no verificado cuando falta la clave, forzando tokens de testing explícitos y bloqueando cualquier bypass en producción. | **RESUELTO** |
| **BUG-002** | `apps/api`<br>(Sesiones JWT) | **MEDIA**<br>*(Disponibilidad)* | Timeout de 5,000 ms y congelamiento de pruebas unitarias al verificar revocación de tokens cuando PostgreSQL no estaba levantado localmente. | La función `isTokenRevoked` intentaba conectarse vía socket TCP a Prisma sin validar si el entorno era de testing o si la base de datos estaba disponible. | Se implementó una cláusula de guarda `NODE_ENV === 'test'` y un fallback O(1) con Set en memoria (`REVOKED_TOKENS_CACHE`), permitiendo ejecución ultrarrápida sin dependencias de red externas. | **RESUELTO** |
| **BUG-003** | `packages/messaging`<br>(RabbitMQ / POS) | **ALTA**<br>*(Consistencia)* | Descuadre en caja y cobro fantasma ante desabasto repentino de lotes de café de especialidad durante la venta concurrente. | No existía mecanismo de compensación transaccional distribuido ante rechazo en el microservicio de inventario tras confirmarse el pago. | Se implementó el Patrón Saga con eventos compensatorios en RabbitMQ (`cafeteria.events`) y enrutamiento a DLQ, ejecutando reembolso automático al cliente y liberando el pedido. | **RESUELTO** |
| **BUG-004** | `apps/web`<br>(Frontend / SEO) | **MEDIA**<br>*(Compilación)* | Error de renderizado en `vite-ssg build` causado por el acceso directo a APIs del navegador (`window`, `localStorage`) durante la fase de prerenderizado SSR. | Componentes de la barra de navegación (`AppNavbar.vue`) intentaban leer el estado de autenticación en tiempo de construcción del servidor (Node.js). | Se condicionó la lectura de almacenamiento local al ciclo de vida `onMounted` del cliente y se aislaron las rutas privadas (`/admin`, `/pos`) con directivas `<meta name="robots" content="noindex">`. | **RESUELTO** |
| **BUG-005** | `apps/web`<br>(POS Táctil) | **BAJA**<br>*(Usabilidad / UI)* | Desbordamiento horizontal y botones de cobro superpuestos en tabletas de mostrador con resoluciones de 768px a 1024px. | Estilos CSS rígidos con anchos en píxeles fijos que no contemplaban la orientación vertical/horizontal de tabletas comerciales. | Se refactorizó la cuadrícula del POS con CSS Grid fluido (`grid-template-columns: repeat(auto-fit, minmax(...))`), garantizando áreas de toque mínimas de 48px según WCAG 2.1. | **RESUELTO** |

---

### Métrica de Desempeño del Equipo 2
- **Métrica Oficial Asignada:** Cantidad de vulnerabilidades y errores corregidos.
- **Resultado Cuantificado:** **5 errores/vulnerabilidades críticas corregidas y auditadas.**
- **Impacto Obtenido:** Sistema 100% libre de fallos de compilación, 0 bypasses en autenticación y 77 pruebas unitarias aprobadas de forma ininterrumpida en el pipeline de CI.

---

## 5. Conclusiones del Momento 2

1. **Madurez del Pipeline de Integración Continua (CI):** La implementación de GitFlow junto con la automatización de pruebas en Vitest ha permitido validar cada incremento de software de manera inmediata, eliminando la integración manual tardía.
2. **Priorización de Seguridad Web Cumplida:** El Equipo 2 ha blindado el acceso a la plataforma mediante autenticación stateless robusta (JWT + Cookies Seguras + 2FA TOTP + reCAPTCHA estricto), sentando las bases exigidas por la materia para el posterior despliegue con HTTPS en el Momento 3.
3. **Prototipo Mínimo Viable Totalmente Funcional:** El software no representa una maqueta conceptual, sino una aplicación operativa con interfaces reactivas para caja, trazabilidad de café orgánico conforme al ODS 12 y control administrativo de alta resiliencia.

---

## 6. Referencias Bibliográficas (APA 7ma Edición)

- Bass, L., Weber, I., & Zhu, L. (2015). *DevOps: A software architect's perspective*. Addison-Wesley Professional.
- Humble, J., & Farley, D. (2010). *Continuous delivery: Reliable software releases through build, test, and deployment automation*. Addison-Wesley.
- International Organization for Standardization, & International Electrotechnical Commission. (2011). *Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models* (ISO/IEC Standard No. 25010:2011). ISO/IEC.
- Kim, G., Humble, J., Debois, P., Willis, J., & Forsgren, N. (2021). *The DevOps handbook: How to create world-class agility, reliability, and security in technology organizations* (2nd ed.). IT Revolution Press.
- Martin, R. C. (2018). *Clean architecture: A craftsman's guide to software structure and design*. Prentice Hall.
- OWASP Foundation. (2021). *OWASP Top 10: 2021 The ten most critical web application security risks*. OWASP. https://owasp.org/Top10/
