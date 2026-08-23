# Monchis Café — Requerimientos Técnicos y de Infraestructura

Este documento especifica la arquitectura técnica, la estrategia de desarrollo TDD por fases, los estándares de testing multicapa, el sistema de diseño y la infraestructura del sistema **Monchis Café**.

---

## 1. Arquitectura y Stack Tecnológico

### 1.1 Estructura Monorepo (`pnpm workspaces` + `Turborepo`)
```
/proyecto-raiz
├── apps/
│   ├── web/                 # Frontend: Vue 3 + Vite + vite-ssg + Pinia + Vue Router
│   └── api/                 # Backend: Next.js (API Routes / Route Handlers)
├── packages/
│   ├── database/            # Prisma ORM, migraciones y seeders
│   ├── shared-types/        # DTOs y tipos TypeScript compartidos
│   ├── config/              # Tokens de diseño CSS pastel, ESLint y TSConfig
│   └── messaging/           # Cliente RabbitMQ, Saga Orchestrator y DLQ
├── infra/
│   ├── docker/              # Dockerfiles para web, api, rabbitmq y nginx
│   ├── terraform/           # IaC para provisión en GCP
│   └── docker-compose.yml   # Orquestador local completo
├── tests/
│   ├── e2e/                 # Playwright (Multi-viewport, regresión visual)
│   ├── security/            # Scripts de pruebas de seguridad automatizadas (OWASP)
│   └── accessibility/       # Lighthouse CI + axe-core
├── docs/                    # Documentación técnica, mockups y diagramas
├── obsidian/                # Vault de conocimiento y bitácora del agente
└── requirements/            # Requerimientos funcionales y técnicos
```

### 1.2 Frontend (`apps/web`)
- **Framework & Build:** Vue 3 con Vite y `vite-ssg` para prerenderizado estático de rutas públicas (`/`, `/nosotros`, `/menu`, `/contacto`).
- **Gestión de Estado:** Pinia (manejo de access token en memoria, carrito de venta y monedero de lealtad).
- **SEO & Head Management:** `@vueuse/head` / `unhead` para meta tags OpenGraph, Twitter Cards y Schema.org `LocalBusiness` / `CoffeeShop`.
- **Diseño & Animación:** Tokens CSS en `packages/config`, `@vueuse/motion` para micro-animaciones declarativas y `GSAP + ScrollTrigger` para transiciones de imágenes al scroll respetando `prefers-reduced-motion`.
- **Consumo de API:** Cliente HTTP (Axios / Fetch) con interceptores para inyección de token `Bearer` y renovación automática por cookie `httpOnly`.

### 1.3 Backend (`apps/api`)
- **Framework:** Next.js (utilizado estrictamente como backend API / Route Handlers, sin renderizado de vistas de negocio).
- **Validación de Datos:** Zod para esquema estricto de inputs y sanitización en cada endpoint.
- **Manejo de Errores:** Middleware centralizado para captura de excepciones y formatos JSON estandarizados.

### 1.4 Base de Datos y ORM (`packages/database`)
- **Motor:** PostgreSQL (Versión 15+).
- **ORM:** Prisma para consultas tipadas, migraciones versionadas y protección nativa contra inyección SQL.
- **Transacciones ACID:** Bloques transaccionales (`prisma.$transaction`) para operaciones críticas locales.

### 1.5 Mensajería y Eventos Asíncronos (`packages/messaging`)
- **Broker:** RabbitMQ (AMQP 5672, Management UI 15672).
- **Exchanges & Queues:** Topic Exchange `cafeteria.events`, colas de eventos por servicio.
- **Reintentos Progresivos con Retraso (Delayed Queues):** Estrategia de reintentos progresivos (10s, 60s, 300s).
- **Dead Letter Queue (DLQ):** Captura de eventos no procesables tras agotar reintentos, con alerta SMTP al administrador.
- **Patrón Saga (Compensación / Reversas):** Transacciones compensatorias automáticas para cancelar ventas y reembolsar cobros ante falta de insumos orgánicos.

---

## 2. Seguridad de la Información y Autenticación Stateless

### 2.1 Autenticación Stateless
- **Access Token:** JWT de vida corta (10–15 minutos) almacenado en memoria en el frontend Vue.
- **Refresh Token:** Token rotativo de larga duración (7 días) almacenado en cookie `httpOnly + Secure + SameSite=Strict`.
- **Claims en Token:** `sub`, `email`, `role` (`admin`, `cajero`, `cliente`) para autorización inmediata en backend sin consultar la base de datos en cada petición.
- **Revocación:** Mecanismo de blacklist en Redis / base de datos para cierre de sesión global.

### 2.2 Integración de Google reCAPTCHA
- Verificación obligatoria de token `g-recaptcha-response` en los endpoints de Login, Registro y Transacciones de alto impacto.
- Validación del token en backend contra el endpoint oficial `https://www.google.com/recaptcha/api/siteverify`.

### 2.3 Medidas contra Vulnerabilidades Web (OWASP Top 10)
- **SQL Injection (SQLi):** Consultas parametrizadas obligatorias vía Prisma.
- **Cross-Site Scripting (XSS):** Sanitización estricta en backend y escape automático en Vue 3 (prohibido el uso inseguro de `v-html`).
- **Insecure Direct Object References (IDOR):** Comprobación en cada servicio de que el recurso pertenece al usuario solicitante.
- **Cabeceras HTTP de Seguridad:** `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security`.
- **Rate Limiting:** Control de tasa de peticiones con Redis en rutas de login y refresh para mitigar fuerza bruta.

---

## 3. Estrategia de Testing Multicapa y Metodología TDD

| Nivel de Prueba | Herramienta | Objetivo y Alcance | Ejecución |
|---|---|---|---|
| **Unitarias** | Vitest | Lógica de negocio, utilidades, stores de Pinia, servicios aislados | Pre-commit / CI |
| **API e Integración** | Supertest + Prisma (Test DB) | Endpoints REST, validaciones Zod, autenticación JWT, reCAPTCHA | Cada PR |
| **Base de Datos** | Vitest + Docker PostgreSQL | Constraints de BD, transacciones ACID, integridad referencial | Cada PR |
| **Viewport / Multi-resolución** | Playwright | Detección de overflow, texto cortado, botones ocultos y scroll horizontal en 360px, 768px, 1024px, 1440px+ | Cada PR a `main` |
| **Regresión Visual** | Playwright Screenshot Diff | Comparación visual pixel por pixel contra capturas baseline por breakpoint | Cada PR a `main` |
| **Validación de CSS / Breakpoints** | Playwright / Vitest DOM | Verificación programática de activación de media queries y estilos esperados | Cada PR a `main` |
| **Accesibilidad y Performance** | Lighthouse CI + axe-core | Puntuación >90 en accesibilidad (tamaño táctil, ARIA, contraste) y >85 en rendimiento | Cada PR a `main` |
| **Seguridad SAST** | eslint-plugin-security, npm audit | Detección estática de dependencias vulnerables y patrones inseguros | En cada commit |
| **Seguridad DAST** | OWASP ZAP / Custom Security Scripts | Simulación activa de ataques XSS, SQLi, CSRF y auditoría de cabeceras HTTP | Pre-release / Staging |

---

## 4. Sistema de Diseño (UI/UX) y Tokens CSS

```css
:root {
  --color-primary: #F3C9C9;         /* Rosa suave */
  --color-primary-dark: #D98C7F;    /* Rosa terracota */
  --color-secondary: #C9A88B;       /* Café con leche */
  --color-secondary-dark: #8C6B52;  /* Café tostado */
  --color-bg-base: #FAF3ED;         /* Crema cálido */
  --color-bg-surface: #FFFDFB;      /* Blanco cálido */
  --color-text-main: #4A3B32;       /* Café oscuro cálido */
  --color-text-muted: #8A7A6D;      /* Café grisáceo */
  --color-success: #B7D9B1;         /* Verde pastel */
  --color-error: #E39A9A;           /* Rosa-rojo suave */
  
  --font-heading: 'Poppins', 'Fraunces', serif;
  --font-body: 'Nunito', 'Inter', sans-serif;
}
```

---

## 5. Infraestructura y Despliegue (`infra/`)

- **Docker Compose Local:**
  - `web` (Vue 3 en puerto 3000)
  - `api` (Next.js en puerto 8080)
  - `postgres` (PostgreSQL 15 en puerto 5432)
  - `rabbitmq` (RabbitMQ 3 con management en 5672 / 15672)
  - `redis` (Redis 7 en puerto 6379)
  - `nginx-gateway` (Proxy inverso en puerto 80)
- **Infraestructura Cloud (GCP):**
  - Cloud Run para backend API y frontend web.
  - Cloud SQL (PostgreSQL administrado).
  - Cloud Memorystore (Redis administrado).
  - Cloud AMQP / RabbitMQ administrado.
  - Google Secret Manager para gestión segura de variables de entorno.
- **Variables de Entorno:** Cero credenciales en código fuente (`.env.example` versionado, `.env` ignorado por Git).
