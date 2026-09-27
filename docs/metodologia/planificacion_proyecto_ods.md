# Planificación de un Proyecto de Desarrollo de Software Enfocado a los Objetivos de Desarrollo Sostenible (ODS)

**Proyecto:** Monchis Café — Plataforma Web Segura para Cafetería Orgánica y Comercial  
**Materia:** Unidad 1. Administración de Proyectos  
**Docente:** Dr. Gabriel Navarro Salcedo  
**Equipo de Proyecto:** Ernesto Fierro (Líder de Proyecto / Arquitecto de Software) y Equipo de Desarrollo  
**Fecha:** 31 de Agosto de 2026  
**Versión:** 1.0 (Documento Definitivo de Planificación Estratégica y Operativa)

---

## 1. Definición del Sistema a Desarrollar

### 1.1 Selección y Fundamentación de los ODS Base
El proyecto **Monchis Café** asume un compromiso formal con la Agenda 2030 de la Organización de las Naciones Unidas (ONU), integrando la sostenibilidad no como un añadido superficial, sino como un eje rector embebido en las decisiones arquitectónicas, de procesos y de lógica de negocio del software. Los cuatro ODS seleccionados como pilares son:

```
                  ┌─────────────────────────────────────────────────────────────┐
                  │                 MONCHIS CAFÉ & AGENDA 2030                  │
                  └──────────────────────────────┬──────────────────────────────┘
                                                 │
        ┌───────────────────────┬────────────────┴────────────────┬───────────────────────┐
        ▼                       ▼                                 ▼                       ▼
┌───────────────┐       ┌───────────────┐                 ┌───────────────┐       ┌───────────────┐
│     ODS 8     │       │     ODS 9     │                 │    ODS 12     │       │    ODS 16     │
│Trabajo Decente│       │ Industria,    │                 │ Producción y  │       │Paz, Justicia e│
│ y Crecimiento │       │ Innovación e  │                 │    Consumo    │       │ Instituciones │
│   Económico   │       │Infraestructura│                 │ Responsables  │       │    Sólidas    │
└───────────────┘       └───────────────┘                 └───────────────┘       └───────────────┘
```

1. **ODS 8: Trabajo Decente y Crecimiento Económico (Metas 8.2 y 8.3):**
   - *Fundamentación:* Fortalece la viabilidad económica de las micro, pequeñas y medianas empresas (MIPYMES) cafetaleras y el comercio regional de especialidad. La plataforma digitaliza integralmente las ventas, reduce discrepancias de caja y formaliza los canales comerciales de caficultores artesanales.
2. **ODS 9: Industria, Innovación e Infraestructura (Metas 9.4 y 9.c):**
   - *Fundamentación:* Moderniza la infraestructura tecnológica con una arquitectura escalable en monorepo (`pnpm workspaces` + `Turborepo`), microservicios orientados a eventos con RabbitMQ y contenedorización Docker bajo estándares de eficiencia de recursos computacionales (*Green Software Engineering*).
3. **ODS 12: Producción y Consumo Responsables (Metas 12.2, 12.5 y 12.8):**
   - *Fundamentación:* Implementa trazabilidad de lotes orgánicos (finca, altitud, fecha de tueste y caducidad), control de mermas para mitigar el desperdicio de insumos, y un motor de fidelización ecológico ("Monchis Rewards") que incentiva el uso de termos y tazas reutilizables mediante descuentos y sellos digitales, disminuyendo el desecho de plásticos de un solo uso.
4. **ODS 16: Paz, Justicia e Instituciones Sólidas (Metas 16.5 y 16.6):**
   - *Fundamentación:* Garantiza transacciones transparentes, rendición de cuentas financieras sin alteraciones, protección estricta de datos personales bajo esquemas *stateless* (JWT, reCAPTCHA v2/v3, RBAC) y auditoría inmutable de transacciones y reversas financieras (Patrón Saga).

---

### 1.2 Descripción Detallada del Sistema
**Monchis Café** es una plataforma web integral, distribuida y segura diseñada para la administración y comercialización omnicanal de una cafetería de especialidad orgánica y productos comerciales complementarios.

- **Propósito:** Cerrar la brecha tecnológica y de sostenibilidad en el sector de alimentos y bebidas artesanal mediante una solución de software de alto rendimiento que unifique el punto de venta táctil (POS), la fidelización ecológica de clientes, el seguimiento de la cadena de suministro de café regional y la analítica de marketing con total transparencia contable y resiliencia ante fallos.
- **Público Objetivo:**
  - *Consumidores Finales (Clientes locales y visitantes):* Amantes del café de especialidad y consumidores eco-conscientes interesados en conocer el origen de su bebida y beneficiarse de incentivos por consumo responsable.
  - *Personal de Servicio (Baristas y Cajeros):* Operadores que precisan un sistema POS ágil, intuitivo, con cálculo automático de cambios, soporte de pagos mixtos y mitigación de errores humanos.
  - *Productores y Cooperativas Cafetaleras Regionales (Chiapas, Veracruz, Oaxaca):* Proveedores de café de altura que acceden a una plataforma que visibiliza su labor, garantiza comercio justo y registra digitalmente sus lotes.
  - *Administradores y Socios de la MIPYME:* Responsables que requieren supervisión en tiempo real de ingresos, mermas, alertas de caducidad, auditoría transaccional y métricas de adquisición de clientes.
- **Contribución Concreta al Cumplimiento de los ODS:**
  - *Mitigación de Residuos:* El sistema descuenta automáticamente la huella de desecho al bonificar a los usuarios que presentan envases reutilizables y parametriza el control de inventario según la fecha de tueste y vida útil para evitar caducidad en anaquel.
  - *Eficiencia Operativa:* Sustituye registros en papel por auditorías electrónicas sincronizadas mediante colas asíncronas con tolerancia a caídas de red.
  - *Ciberseguridad y Privacidad Ciudadana:* Protege la identidad de los consumidores mediante autenticación sin estado, eliminando brechas de seguridad comunes en sistemas comerciales tradicionales.

---

## 2. Alcance y Prioridades del Sistema

### 2.1 Límites del Sistema (In-Scope vs. Out-of-Scope)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                             ALCANCE DEL SISTEMA                                 │
├────────────────────────────────────────┬────────────────────────────────────────┤
│        DENTRO DEL ALCANCE (IN-SCOPE)   │      FUERA DEL ALCANCE (OUT-OF-SCOPE)  │
├────────────────────────────────────────┼────────────────────────────────────────┤
│ • Arquitectura Monorepo TypeScript     │ • Hardware POS propietario embebido    │
│   (Frontend Vue 3 + Backend Next.js)   │   (lectores de banda magnética bespoke)│
│ • Punto de Venta (POS) web táctil      │ • Flotilla propia de reparto/delivery  │
│ • Pagos mixtos (Efectivo, Tarjeta,     │   de última milla en fase 1            │
│   SPEI con referencia, Puntos)         │ • Módulo de contabilidad fiscal oficial│
│ • Patrón Saga con RabbitMQ y Reversas  │   (timbrado de facturas SAT México v4) │
│ • Módulo Monchis Rewards con bono eco  │ • Pasarela con criptoactivos           │
│ • Trazabilidad de lotes orgánicos      │ • Sensores IoT de tolvas en tiempo real│
│ • Panel Admin con analítica de tráfico │ • Soporte nativo para iOS/Android      │
│   (Google Maps, Instagram, Directo)    │   (en fase 1 se opera como PWA/Web)    │
│ • Prerenderizado SEO con `vite-ssg`    │                                        │
│ • Autenticación stateless JWT + Captcha│                                        │
└────────────────────────────────────────┴────────────────────────────────────────┘
```

### 2.2 Prioridades del Desarrollo (Método MoSCoW Alineado a ODS)

| Clasificación | Módulo / Requerimiento | Alineación ODS | Justificación |
|---|---|---|---|
| **Must Have** (Indispensable) | Autenticación Stateless (JWT con rotación, RBAC, reCAPTCHA v2/v3). | ODS 16 | Sin seguridad robusta no se pueden procesar transacciones ni proteger la privacidad de los usuarios. |
| **Must Have** (Indispensable) | Punto de Venta (POS) ágil con soporte de efectivo, tarjeta y cálculo de cambio. | ODS 8 | Constituye el núcleo de ingresos y operatividad de la cafetería. |
| **Must Have** (Indispensable) | Trazabilidad de Lotes de Café Orgánico y Gestión de Inventario con caducidades. | ODS 12 | Asegura el control de calidad, comercio justo con fincas y combate al desperdicio. |
| **Must Have** (Indispensable) | Orquestación Saga con RabbitMQ para Reversas Transaccionales automáticas. | ODS 9, 16 | Evita pérdidas financieras por inconsistencias de inventario tras cobros fallidos. |
| **Should Have** (Importante) | Programa "Monchis Rewards" (sellos digitales, monedero cashback y bono ecológico). | ODS 12 | Conductor clave de fidelización y reducción sistemática de vasos desechables. |
| **Should Have** (Importante) | Panel de Administración con Atribución de Canales UTM (Google Maps, Instagram). | ODS 8, 9 | Proporciona analítica de datos para toma de decisiones informada del negocio. |
| **Should Have** (Importante) | SEO optimizado con prerenderizado estático (`vite-ssg`) y Schema.org. | ODS 8, 9 | Aumenta el alcance orgánico de la cafetería y atrae turismo responsable. |
| **Could Have** (Deseable) | Alertas automáticas de stock bajo y DLQ vía servidor de correo SMTP. | ODS 9 | Añade proactividad al mantenimiento operativo sin interrumpir el flujo central. |
| **Could Have** (Deseable) | Exportación de reportes semanales en formatos estructurados PDF y Excel. | ODS 8, 16 | Facilita revisiones contables periódicas para auditorías internas. |
| **Won't Have** (Postergado) | Facturación electrónica directa con el SAT de México (CFDI 4.0). | ODS 8 | Se contempla para la Fase 2 del ciclo de vida tras validar la adopción del POS. |
| **Won't Have** (Postergado) | Integración con flotillas de repartidores de terceros vía API (Uber Eats). | ODS 8 | Se excluye para priorizar el modelo de consumo en sitio y *pick-up* sostenible. |

---

## 3. Objetivos Generales y Específicos

### 3.1 Objetivo General
Diseñar, planificar e implementar una plataforma web de alto rendimiento y arquitectura modular para **Monchis Café** antes de finalizar el ciclo operativo 2026, que integre punto de venta táctil, trazabilidad de café orgánico y comercio justo, resiliencia transaccional con RabbitMQ Saga y fidelización ecológica, alineada plenamente a los ODS 8, 9, 12 y 16, garantizando una cobertura de pruebas mínima del 85% bajo metodología TDD.

### 3.2 Objetivos Específicos por Fases de Desarrollo

```
FASE 1: Planificación y Arquitectura ──► FASE 2: Backend Core & Seguridad ──► FASE 3: Frontend Core & SEO
                                                                                         │
FASE 6: QA Multicapa & Seguridad    ◄── FASE 5: Panel Admin & Analítica  ◄── FASE 4: POS & Trazabilidad
        │
        ▼
FASE 7: Despliegue Cloud & Monitoreo
```

- **Fase 1: Análisis, Modelado de Datos y Arquitectura Base**
  - Configurar el espacio de trabajo monorepo con `pnpm` y `Turborepo`, estableciendo paquetes compartidos (`packages/database`, `packages/messaging`, `packages/config`).
  - Modelar la base de datos relacional en PostgreSQL mediante Prisma ORM para entidades de usuarios, productos, lotes, ventas, pagos y recompensas.
  - Documentar la arquitectura de referencia, diagramas C4 y especificaciones funcionales en Obsidian.
- **Fase 2: Backend Core, Seguridad y Mensajería Asíncrona**
  - Desarrollar endpoints en Next.js Route Handlers con validación tipada mediante Zod.
  - Implementar autenticación stateless JWT con Access Tokens de 15 minutos en memoria y Refresh Tokens rotativos en cookies `httpOnly + Secure + SameSite=Strict`.
  - Integrar Google reCAPTCHA v2/v3 para mitigar abusos por bots en rutas de autenticación.
  - Configurar RabbitMQ Topic Exchange (`cafeteria.events`) con colas de retardo y Dead Letter Queue (DLQ).
- **Fase 3: Frontend Core, Sistema de Diseño y SEO Prerenderizado**
  - Construir la interfaz de usuario en Vue 3 con Vite, Pinia y Vue Router.
  - Implementar el sistema de diseño cálido pastel con tokens CSS y micro-animaciones declarativas respetando `prefers-reduced-motion`.
  - Configurar `vite-ssg` para prerenderizado estático de páginas públicas (`/`, `/menu`, `/nosotros`, `/contacto`) y metadatos Schema.org `LocalBusiness`.
- **Fase 4: Lógica de Negocio, POS Sostenible y Patrón Saga**
  - Implementar el módulo de Trazabilidad de Café Orgánico con fincas de origen, notas de cata y fechas de tueste/caducidad.
  - Diseñar el POS táctil con soporte de pagos mixtos (Efectivo, Tarjeta, SPEI y Puntos Monchis).
  - Programar la orquestación del Patrón Saga: emisión automática de compensaciones/reversas en caso de discrepancias de inventario.
  - Integrar las reglas de negocio de "Monchis Rewards": sellos digitales por bebida, bono ecológico por uso de termo y cashback en puntos.
- **Fase 5: Panel Administrativo y Atribución de Marketing Digital**
  - Desarrollar el panel de control para administradores con métricas de ventas y salud de inventario.
  - Implementar el motor de atribución de tráfico capturando parámetros UTM (`utm_source`, `utm_medium`, `utm_campaign`) para comparar conversiones desde Google Maps e Instagram.
  - Habilitar la supervisión y reintento de mensajes fallidos en la Dead Letter Queue.
- **Fase 6: Calidad de Software, Testing Multicapa y Seguridad**
  - Ejecutar pruebas unitarias de stores y lógica con Vitest con cobertura >85%.
  - Realizar pruebas E2E y de regresión visual en múltiples viewports (360px móvil, 768px tablet, 1280px desktop) con Playwright.
  - Auditar la accesibilidad web (WCAG 2.1 AA con axe-core y Lighthouse CI con puntaje >90).
  - Validar defensas contra OWASP Top 10 (XSS, SQLi, CSRF, CSP y rate limiting).
- **Fase 7: Despliegue en la Nube, IaC y Cierre de Proyecto**
  - Automatizar la provisión de infraestructura en Google Cloud Platform (Cloud Run, Cloud SQL, Memorystore Redis) mediante Terraform.
  - Empaquetar servicios en contenedores Docker y orquestar despliegues continuos mediante GitHub Actions.
  - Entregar manuales de usuario y bitácoras finales de lecciones aprendidas.

---

## 4. Determinación de Recursos y Estimación Presupuestal

### 4.1 Clasificación de Recursos

1. **Recursos Humanos:**
   - *Líder de Proyecto / Scrum Master (1 persona):* Coordinación de sprints, gestión de riesgos, comunicación con stakeholders y supervisión de cronograma.
   - *Arquitecto de Software & DevOps Engineer (1 persona):* Diseño del monorepo, topología de RabbitMQ, IaC con Terraform y despliegues CI/CD.
   - *Desarrollador Full-Stack Backend (1 persona):* Lógica de Next.js API, Prisma ORM, JWT stateless, Saga orchestrator y validaciones Zod.
   - *Desarrollador Full-Stack Frontend & UI/UX (1 persona):* Interfaz en Vue 3, Pinia, integración de POS, sistema de diseño pastel y `vite-ssg`.
   - *Especialista en QA & Ciberseguridad (1 persona):* Pruebas automatizadas Playwright, Vitest, escaneo OWASP y auditorías de accesibilidad.
2. **Recursos Tecnológicos:**
   - *Lenguajes y Frameworks:* TypeScript, Vue 3, Next.js, Vite, Node.js.
   - *Persistencia y Mensajería:* PostgreSQL 15, Redis 7, RabbitMQ 3.
   - *Herramientas Cloud:* Google Cloud Platform (Cloud Run, Cloud SQL, Cloud Memorystore, Secret Manager).
   - *Herramientas de Desarrollo y QA:* Turborepo, Vitest, Playwright, Docker Desktop, GitHub Enterprise / Pro, Obsidian.
3. **Recursos Materiales:**
   - 2 Estaciones de trabajo de desarrollo (Laptops Core i7 / Apple Silicon, 32GB RAM).
   - 1 Terminal táctil de punto de venta (Tablet Android de 10.5" con soporte ergonómico para mostrador).
   - 1 Impresora térmica de tickets (58mm/80mm USB/Bluetooth/Red) para comprobantes ecológicos de papel reciclado.
   - 1 Lector de código de barras bidimensional (1D/2D QR) USB.
4. **Recursos Financieros:**
   - Asignación de fondos para honorarios profesionales, consumo de servicios de nube, dominios, certificados y contingencias.

---

### 4.2 Estimación de Costos y Tiempos (Duración: 16 semanas / 4 meses)

| Categoría de Recurso | Descripción Detallada | Tiempo de Uso / Dedicación | Costo Unitario (MXN) | Costo Total (MXN) | Costo Total (USD aprox.) |
|---|---|---|---|---|---|
| **R. Humano** | Líder de Proyecto / Scrum Master | 16 semanas (Part-time 20h/sem) | $12,000 / mes | $48,000 | $2,667 |
| **R. Humano** | Arquitecto de Software & DevOps | 16 semanas (Full-time 40h/sem) | $24,000 / mes | $96,000 | $5,333 |
| **R. Humano** | Desarrollador Backend Core | 16 semanas (Full-time 40h/sem) | $20,000 / mes | $80,000 | $4,444 |
| **R. Humano** | Desarrollador Frontend & UI/UX | 16 semanas (Full-time 40h/sem) | $20,000 / mes | $80,000 | $4,444 |
| **R. Humano** | Ingeniero de QA y Ciberseguridad | 12 semanas (Full-time 40h/sem) | $18,000 / mes | $54,000 | $3,000 |
| **R. Tecnológico** | Google Cloud Platform (Cloud Run + Cloud SQL + Redis) | 4 meses (Entornos Dev + Staging + Prod) | $1,800 / mes | $7,200 | $400 |
| **R. Tecnológico** | CloudAMQP (Instancia administrada de RabbitMQ) | 4 meses | $550 / mes | $2,200 | $122 |
| **R. Tecnológico** | Dominio Web (`.com` / `.mx`) y Certificados SSL | Anual | Pago único | $950 | $53 |
| **R. Tecnológico** | Licencias de software y repositorio (GitHub Team, Obsidian Sync) | 4 meses | $600 / mes | $2,400 | $133 |
| **R. Material** | Terminal de Mostrador (Tablet 10.5" + Base POS fija) | Compra de activo fijo | Pago único | $6,500 | $361 |
| **R. Material** | Impresora térmica de tickets reciclados 80mm | Compra de activo fijo | Pago único | $1,800 | $100 |
| **R. Material** | Lector de código de barras y códigos QR 2D | Compra de activo fijo | Pago único | $1,200 | $67 |
| **R. Financiero** | Fondo de Contingencia Operativa y Riesgos (10%) | Disponible durante el proyecto | N/A | $38,025 | $2,112 |
| **TOTAL ESTIMADO** | **Inversión Integral del Proyecto** | **16 semanas** | — | **$418,275 MXN** | **$23,237 USD** |

---

## 5. Asignación de Roles y Responsabilidades

### 5.1 Definición de Roles del Equipo y Alineación con ODS

```
                            ┌─────────────────────────────────────────┐
                            │    LÍDER DE PROYECTO & SCRUM MASTER     │
                            │    (Ernesto Fierro) [Alineación ODS 8]  │
                            └────────────────────┬────────────────────┘
                                                 │
         ┌───────────────────────────────────────┼───────────────────────────────────────┐
         ▼                                       ▼                                       ▼
┌─────────────────────────┐             ┌─────────────────────────┐             ┌─────────────────────────┐
│  ARQUITECTO SOFTWARE &  │             │   DESARROLLADORES DE    │             │   INGENIERO DE QA &     │
│     DEVOPS ENGINEER     │             │     SOFTWARE FULL-STACK │             │      CIBERSEGURIDAD     │
│   [Alineación ODS 9]    │             │   [Alineación ODS 12]   │             │   [Alineación ODS 16]   │
└─────────────────────────┘             └─────────────────────────┘             └─────────────────────────┘
```

1. **Líder de Proyecto / Scrum Master:**
   - *Responsabilidades:* Facilitar ceremonias ágiles (Daily, Planning, Review, Retrospective), remover impedimentos, controlar el presupuesto, gestionar el alcance MoSCoW y verificar el cumplimiento de los estándares ODS en los entregables.
   - *Alineación ODS:* ODS 8 (garantiza condiciones laborales sostenibles, ritmo de trabajo saludable y entrega de valor económico real a la MIPYME).
2. **Arquitecto de Software & DevOps Engineer:**
   - *Responsabilidades:* Modelar la arquitectura monorepo, configurar pipelines de CI/CD en GitHub Actions, automatizar la infraestructura en GCP con Terraform, administrar RabbitMQ y velar por el bajo consumo de recursos de cómputo (*Green Computing*).
   - *Alineación ODS:* ODS 9 (promueve infraestructura tecnológica industrial moderna, limpia y resiliente).
3. **Desarrollador Full-Stack (Backend & Datos):**
   - *Responsabilidades:* Implementar servicios REST en Next.js API, migración de esquema en Prisma, gestión de transacciones ACID, orquestación del Patrón Saga con reversas automáticas y lógica de trazabilidad de lotes orgánicos.
   - *Alineación ODS:* ODS 12 (codifica la lógica que previene mermas y valida el origen de los lotes de café de comercio justo).
4. **Desarrollador Full-Stack (Frontend & UI/UX):**
   - *Responsabilidades:* Diseñar e implementar las vistas en Vue 3, stores de Pinia, flujo del POS táctil con pagos mixtos, motor de sellos y bonificaciones de Monchis Rewards, accesibilidad WCAG y prerenderizado SEO (`vite-ssg`).
   - *Alineación ODS:* ODS 12 (construye la experiencia de usuario que incentiva el uso de termos y visibiliza el impacto ecológico del consumidor).
5. **Ingeniero de QA y Ciberseguridad:**
   - *Responsabilidades:* Diseñar y ejecutar suites de pruebas automatizadas en Vitest y Playwright, realizar auditorías de seguridad DAST/SAST según directrices OWASP Top 10, verificar la autenticación stateless JWT y medir la accesibilidad con axe-core y Lighthouse.
   - *Alineación ODS:* ODS 16 (asegura la protección de datos, la integridad de las transacciones y la rendición de cuentas del sistema).

---

### 5.2 Matriz RACI del Proyecto
*(R = Responsable de la ejecución, A = Aprobador/Accountable, C = Consultado, I = Informado)*

| Fase / Actividad Principal | Líder de Proyecto | Arquitecto / DevOps | Dev Backend | Dev Frontend | QA & Seguridad |
|---|:---:|:---:|:---:|:---:|:---:|
| 1. Definición de Requerimientos y ODS | **A** | C | C | C | I |
| 2. Diseño de Arquitectura Monorepo y BD | A | **R** | C | C | I |
| 3. Infraestructura Docker e IaC Terraform | I | **R / A** | C | I | I |
| 4. Backend Core y Stateless Auth (JWT + reCAPTCHA) | I | A | **R** | C | C |
| 5. Mensajería RabbitMQ, Saga y Reversas | I | A | **R** | I | C |
| 6. Frontend Core, UI/UX Pastel y SEO Prerender | I | C | I | **R / A** | C |
| 7. Módulo POS, Pagos Mixtos y Monchis Rewards | A | C | R | **R** | C |
| 8. Dashboard Administrativo y Atribución UTM | A | I | R | **R** | I |
| 9. Testing Multicapa (Vitest, Playwright, OWASP) | I | I | C | C | **R / A** |
| 10. Despliegue en Staging / Producción en GCP | A | **R** | I | I | C |
| 11. Capacitación al Personal y Cierre Operativo | **R / A** | I | I | C | I |

---

## 6. Elaboración del Plan Operativo

### 6.1 Objetivos Operativos de Corto Plazo (Sprints de 2 semanas)
El desarrollo se estructura en un ciclo de 16 semanas dividido en 8 Sprints quincenales bajo el marco ágil Scrum con integración de prácticas TDD (Test-Driven Development):

- **Sprint 1 (Semanas 1-2): Cimientos e Infraestructura Base:** Establecer el monorepo funcional con Turborepo, dependencias compartidas, esquemas Prisma para entidades base y contenedorización Docker Compose local.
- **Sprint 2 (Semanas 3-4): Seguridad Stateless y Autenticación:** Entregar el sistema de autenticación JWT (Access/Refresh rotativos), roles RBAC y protección de formularios con Google reCAPTCHA v2/v3.
- **Sprint 3 (Semanas 5-6): Broker de Mensajería y Patrón Saga:** Configurar el exchange de RabbitMQ, colas de retardo y el orquestador de transacciones compensatorias para fallos de stock.
- **Sprint 4 (Semanas 7-8): Frontend Core y Sistema de Diseño Pastel:** Desplegar la estructura Vue 3, integración con Pinia, prerenderizado estático `vite-ssg` para rutas públicas y catálogo con SEO Schema.org.
- **Sprint 5 (Semanas 9-10): Punto de Venta (POS) y Pagos Mixtos:** Implementar la interfaz táctil del cajero con registro de ventas por código de barras, cobro mixto (efectivo con cálculo de cambio, tarjeta, SPEI y puntos).
- **Sprint 6 (Semanas 11-12): Trazabilidad de Lotes y Monchis Rewards:** Habilitar el registro de café orgánico por finca y fecha de tueste, y programar el motor de fidelización con bono por uso de termo y sellos digitales.
- **Sprint 7 (Semanas 13-14): Analítica de Tráfico y QA Multicapa:** Entregar el panel administrativo con atribución UTM (Google Maps vs Instagram), auditoría DLQ y batería de pruebas Playwright en 3 viewports.
- **Sprint 8 (Semanas 15-16): Despliegue Cloud en GCP y Puesta en Marcha:** Ejecutar aprovisionamiento IaC con Terraform, pruebas de penetración OWASP, validación de carga y liberación del sistema a producción.

---

### 6.2 Plan de Acciones, Cronograma y Métricas de Seguimiento

```
Semana:  01  02  03  04  05  06  07  08  09  10  11  12  13  14  15  16
Sprint: ├──S1──┤├──S2──┤├──S3──┤├──S4──┤├──S5──┤├──S6──┤├──S7──┤├──S8──┤
Fase 1: [======]
Fase 2:         [======][======]
Fase 3:                 [======][======]
Fase 4:                         [======][======]
Fase 5:                                 [======][======]
Fase 6:                                         [==============][======]
Fase 7:                                                 [======][======]
```

| ID | Acción Operativa Clave | Plazo | Entregable Verificable | Responsable | Métricas de Seguimiento (KPI) |
|---|---|---|---|---|---|
| **ACT-01** | Inicialización de Monorepo y Docker Compose | Sem 1-2 | Repositorio con build exitoso y contenedores levantados (`postgres`, `rabbitmq`, `redis`). | DevOps | Tiempo de compilación < 45s; 0 errores en `turbo run build`. |
| **ACT-02** | Implementación de JWT Stateless y reCAPTCHA | Sem 3-4 | Endpoints `/api/auth/*` con tests de cookies y rechazo de bots. | Dev Backend | 100% de tests unitarios de auth aprobados; tasa de rechazo de bots simulados = 100%. |
| **ACT-03** | Configuración de RabbitMQ Saga y DLQ | Sem 5-6 | Package `packages/messaging` con orquestador y simulación de reversa. | Dev Backend / DevOps | Tiempo de emisión de compensación < 500ms; mensajes muertos redirigidos a DLQ = 100%. |
| **ACT-04** | Creación de Vistas Públicas y Prerender SEO | Sem 7-8 | Rutas públicas compiladas con `vite-ssg` e inspeccionadas con Google Rich Results. | Dev Frontend | Puntaje Lighthouse SEO = 100/100; tiempo de carga FCP < 1.2 segundos. |
| **ACT-05** | Desarrollo del POS Táctil y Pagos Mixtos | Sem 9-10 | Vista `/pos` interactiva con agregación de productos y cálculo exacto de cambio. | Dev Frontend | Tiempo promedio por registro de venta < 15 segundos; precisión de cambio = 100.00%. |
| **ACT-06** | Módulo de Trazabilidad y Fidelización Eco | Sem 11-12 | Registro de fincas de café y cálculo de bono ecológico en carrito de venta. | Dev Backend / Frontend | 100% de lotes asociados a origen regional; incremento de adopción de sellos digitales. |
| **ACT-07** | Dashboard Admin y Atribución de Tráfico | Sem 13-14 | Panel `/admin` con desglose de ventas por canal UTM y visualización de inventario. | Dev Frontend / Backend | Detección correcta de `utm_source` (Maps / IG) en el 100% de visitas etiquetadas. |
| **ACT-08** | Testing Multicapa y Auditoría de Seguridad | Sem 13-15 | Reporte de pruebas Playwright en 3 resoluciones y escaneo DAST sin vulnerabilidades altas. | QA & Seguridad | Coberura de código >85%; 0 vulnerabilidades críticas OWASP; Accesibilidad Lighthouse >90. |
| **ACT-09** | Provisión GCP con Terraform y Despliegue | Sem 15-16 | Sistema en producción en Cloud Run conectado a Cloud SQL y dominio oficial. | DevOps / Arquitecto | Uptime de servicios >99.5%; latencia de respuesta p95 < 250ms. |

---

## 7. Desarrollo del Plan Estratégico

### 7.1 Mapa Estratégico de la Organización (Cuadro de Mando Integral / Balanced Scorecard)

El mapa estratégico de **Monchis Café** traduce la misión de sostenibilidad y excelencia técnica en una cadena de causa y efecto equilibrada a través de cuatro perspectivas fundamentales:

```
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│                      PERSPECTIVA FINANCIERA Y DE IMPACTO SOSTENIBLE (ODS)                 │
│  • Maximizar la rentabilidad de la cafetería reduciendo pérdidas por mermas y errores POS.│
│  • Incrementar el margen del café de especialidad apoyando el comercio justo regional.    │
│  • Reducir costos de insumos desechables mediante el incentivo de termos reutilizables.   │
└─────────────────────────────────────────────▲─────────────────────────────────────────────┘
                                              │ genera
┌─────────────────────────────────────────────┴─────────────────────────────────────────────┐
│                            PERSPECTIVA DE CLIENTES Y COMUNIDAD                            │
│  • Brindar una experiencia de compra ágil, segura y libre de fricciones en el mostrador.  │
│  • Empoderar al consumidor conociendo la historia y trazabilidad de su café orgánico.    │
│  • Fomentar la lealtad comunitaria mediante beneficios tangibles por hábitos ecológicos.  │
└─────────────────────────────────────────────▲─────────────────────────────────────────────┘
                                              │ impulsa
┌─────────────────────────────────────────────┴─────────────────────────────────────────────┐
│                         PERSPECTIVA DE PROCESOS INTERNOS Y GREEN IT                       │
│  • Garantizar resiliencia transaccional y cero inconsistencias de caja con RabbitMQ Saga. │
│  • Automatizar la rotación de stock por caducidad (PEPS - Primeras Entradas, Salidas).    │
│  • Optimizar la huella de carbono digital mediante prerenderizado y arquitectura serverless.│
└─────────────────────────────────────────────▲─────────────────────────────────────────────┘
                                              │ se fundamenta en
┌─────────────────────────────────────────────┴─────────────────────────────────────────────┐
│                       PERSPECTIVA DE APRENDIZAJE, INNOVACIÓN Y EQUIPO                     │
│  • Adoptar metodología TDD y testing automatizado multicapa para minimizar deuda técnica. │
│  • Capacitar continuamente al equipo en estándares de ciberseguridad y privacidad.        │
│  • Fomentar una cultura ágil de mejora continua y documentación viva en Obsidian.          │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 7.2 Análisis FODA (Fortalezas, Oportunidades, Debilidades, Amenazas)

```
                       ┌───────────────────────┬───────────────────────┐
                       │   FACTORES INTERNOS   │   FACTORES EXTERNOS   │
┌──────────────────────┼───────────────────────┼───────────────────────┤
│                      │      FORTALEZAS       │     OPORTUNIDADES     │
│   ASPECTOS           │ • Arquitectura moderna│ • Creciente demanda de│
│   POSITIVOS          │ • Trazabilidad ODS 12 │   café sustentable    │
│                      │ • Seguridad stateless │ • Vacío digital en el │
│                      │ • Saga resiliente     │   sector artesanal    │
├──────────────────────┼───────────────────────┼───────────────────────┤
│                      │      DEBILIDADES      │       AMENAZAS        │
│   ASPECTOS           │ • Curva de aprendizaje│ • Conectividad móvil  │
│   NEGATIVOS          │ • Equipo compacto     │   inestable en zona   │
│                      │ • Dependencia inicial │ • Resistencia inicial │
│                      │   de configuración    │   al cambio operativo │
└──────────────────────┴───────────────────────┴───────────────────────┘
```

- **Fortalezas (Internas):**
  - **F1:** Arquitectura técnica desacoplada y escalable (Monorepo con Turborepo, Vue 3 y Next.js API).
  - **F2:** Mecanismo nativo de reversas automáticas (Patrón Saga sobre RabbitMQ) que erradica inconsistencias contables e inventarios fantasma.
  - **F3:** Propuesta de valor alineada a ODS (trazabilidad de café regional y programa ecológico de fidelización).
  - **F4:** Seguridad robusta por diseño (autenticación stateless JWT, reCAPTCHA y defensas OWASP).
  - **F5:** Excelente rendimiento y SEO con prerenderizado `vite-ssg` para posicionamiento local.
- **Debilidades (Internas):**
  - **D1:** Mayor complejidad en la configuración inicial de infraestructura distribuida (Docker, RabbitMQ, Redis) frente a un monolito tradicional.
  - **D2:** Curva de aprendizaje del personal de mostrador respecto a la lectura de códigos de barra y métodos de pago mixtos.
  - **D3:** Equipo de desarrollo compacto, demandando rigurosa disciplina en la priorización para evitar sobrecarga.
- **Oportunidades (Externas):**
  - **O1:** Creciente tendencia de consumidores que priorizan productos con certificación de comercio justo y empaque ecológico.
  - **O2:** Carencia de soluciones de software accesibles y modernas adaptadas a cafeterías artesanales en zonas suburbanas/rurales.
  - **O3:** Canales de marketing digital geolocalizados de bajo costo (atribución directa desde Google Maps e Instagram).
  - **O4:** Acceso a fondos o reconocimientos de emprendimiento verde y sustentabilidad empresarial.
- **Amenazas (Externas):**
  - **A1:** Inestabilidad de la conexión a internet en la zona de operación de la cafetería.
  - **A2:** Competencia de grandes cadenas comerciales que cuentan con aplicaciones móviles masivas y programas de lealtad agresivos.
  - **A3:** Incremento en los costos de materias primas e inflación en el grano de café de altura.
  - **A4:** Ciberataques automatizados y fraude transaccional frecuente en plataformas web comerciales.

---

### 7.3 Matriz de Cruces Estratégicos

| Cuadrante Estratégico | Estrategia Formulada | Justificación y Acciones |
|---|---|---|
| **Estrategias FO** *(Maxi-Maxi: Usar Fortalezas para aprovechar Oportunidades)* | **E-FO1:** Lanzar campañas de marketing geolocalizado en Instagram y Google Maps destacando la trazabilidad de fincas regionales y la bonificación por termo, midiendo la conversión con el panel administrativo (F3, F5 + O1, O3). | Aprovechar la capacidad técnica de atribución UTM y prerenderizado SEO para captar clientes eco-conscientes en el radio geográfico de la cafetería. |
| **Estrategias DO** *(Mini-Maxi: Superar Debilidades aprovechando Oportunidades)* | **E-DO1:** Diseñar interfaces intuitivas y tutoriales interactivos en el POS para que el personal domine la operativa en menos de 2 horas, posicionando a la MIPYME como líder en digitalización artesanal (D2 + O2). | La simplicidad de la UI pastel y reactiva reduce la curva de aprendizaje del personal sin experiencia tecnológica previa. |
| **Estrategias FA** *(Maxi-Mini: Usar Fortalezas para neutralizar Amenazas)* | **E-FA1:** Proteger la plataforma contra ataques de denegación de servicio y fraude mediante rate limiting en Redis, reCAPTCHA v2/v3 y tokens stateless que no comprometen la base de datos (F4 + A4). | Blindar el negocio frente a vulnerabilidades web sin incurrir en licencias costosas de WAFs comerciales propietarios. |
| **Estrategias DA** *(Mini-Mini: Minimizar Debilidades y eludir Amenazas)* | **E-DA1:** Incorporar soporte para transacciones en cola local (almacenamiento en caché del navegador/Pinia) para que caídas momentáneas de internet no bloqueen el cobro en caja (D1 + A1). | Garantizar la continuidad del negocio en mostrador aun cuando la conectividad del proveedor de internet rural fluctúe. |

---

## 8. Análisis de Tendencias, Objetivos, Pruebas y Resultados Esperados

### 8.1 Tendencias Tecnológicas y de Desarrollo de Software
La concepción técnica de **Monchis Café** se apoya en cinco tendencias de vanguardia de la ingeniería de software moderna:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        TENDENCIAS TECNOLÓGICAS INCORPORADAS                            │
├──────────────────────────┬──────────────────────────┬──────────────────────────────────┤
│ Green Software Eng.      │ Event-Driven Architecture│ Stateless Auth & Zero Trust      │
│ • Menor consumo de CPU   │ • Desacoplamiento        │ • Cero sesiones en servidor      │
│ • Prerenderizado SSG     │ • Patrón Saga y DLQ      │ • JWT rotativo + reCAPTCHA       │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ Monorepo Architecture    │ Multi-Viewport & Visual  │ Local SEO & Structured Data      │
│ • Turborepo + pnpm       │ • Pruebas pixel-diff     │ • JSON-LD Schema.org             │
│ • Código compartido      │ • Playwright automatizado│ • Atribución UTM granular        │
└──────────────────────────┴──────────────────────────┴──────────────────────────────────┘
```

1. **Green Software Engineering (Ingeniería de Software Verde):**
   - *Fundamento:* La computación global genera una proporción significativa de las emisiones de carbono. Monchis Café adopta la reducción de cómputo innecesario mediante prerenderizado estático (`vite-ssg`): las páginas públicas se compilan a HTML plano durante el build, evitando renderizados en el servidor en cada petición y minimizando el consumo de energía en los centros de datos de la nube.
2. **Arquitecturas Orientadas a Eventos (EDA) y Patrón Saga:**
   - *Fundamento:* Sustituir el bloqueo transaccional distribuido de dos fases (2PC) por orquestación mediante colas de mensajería con RabbitMQ. Si un insumo se agota mientras el cliente realiza el pago, el orquestador Saga gatilla de forma asíncrona la reversa del cobro, garantizando la consistencia eventual sin congelar recursos del sistema.
3. **Seguridad Stateless y Principios de Zero Trust:**
   - *Fundamento:* Eliminación de sesiones tradicionales en memoria de servidor que consumen recursos continuos. La combinación de Access Tokens en memoria del navegador y Refresh Tokens protegidos en cookies seguras (`httpOnly`, `SameSite=Strict`), junto con reCAPTCHA en backend, provee autenticación de baja latencia inmune a ataques CSRF y robo por XSS.
4. **Monorepos Modulares de Alto Rendimiento:**
   - *Fundamento:* Uso de `Turborepo` con `pnpm` para gestionar múltiples aplicaciones (`apps/web`, `apps/api`) y paquetes compartidos (`database`, `messaging`, `config`) en un solo repositorio unificado, logrando tiempos de compilación incrementales con caché inteligente.
5. **Testing Multicapa Automatizado y Regresión Visual:**
   - *Fundamento:* La garantía de calidad ya no depende de pruebas manuales tardías, sino de pipelines continuos que validan desde la unidad de código hasta la apariencia visual píxel por píxel en pantallas de smartphone, tablet y escritorio.

---

### 8.2 Objetivos de Pruebas y Estrategia de Calidad (Testing Multicapa)

El aseguramiento de calidad se rige por la **Pirámide de Pruebas** adaptada a sistemas transaccionales con requerimientos de alta disponibilidad y diseño responsive:

```
                                 /\
                                /  \     Pruebas E2E & Regresión Visual
                               /    \    (Playwright: 3 viewports, Pixel-diff)
                              /------\
                             /        \   Pruebas de Seguridad & Accesibilidad
                            /          \  (OWASP DAST, Lighthouse CI, axe-core)
                           /------------\
                          /              \ Pruebas de Integración y API
                         /                \ (Supertest, Prisma Test DB, RabbitMQ)
                        /------------------\
                       /                    \ Pruebas Unitarias de Lógica y Stores
                      /                      \ (Vitest: Pinia stores, utilidades, Zod)
                     /------------------------\
```

| Nivel de Prueba | Herramienta | Objetivo Específico de Calidad | Criterio de Aceptación / Éxito |
|---|---|---|---|
| **Unitarias** | Vitest | Validar aisladamente la lógica de negocio (cálculo de cambio, reglas de cashback, sellos digitales y esquemas Zod). | Cobertura de sentencias y ramas > 85%; ejecución en < 10 segundos en local. |
| **Integración de API** | Supertest + Test DB | Probar endpoints REST, ciclo de vida de tokens JWT, transacciones ACID de Prisma y manejo de errores 4xx/5xx. | 100% de rutas críticas probadas con respuestas HTTP estandarizadas. |
| **Mensajería y Eventos** | Mock RabbitMQ / In-Memory Bus | Verificar que eventos `order.created`, `order.cancelled` y reversas Saga emitan las compensaciones esperadas. | Compensación ejecutada en 100% de escenarios simulados de stock agotado. |
| **Viewport / Multi-resolución** | Playwright | Asegurar adaptabilidad en 3 viewports clave: Móvil (360px–375px), Tablet (768px) y Desktop (1280px–1440px). | 0 desbordamientos horizontales de texto; botones táctiles con tamaño mínimo de 48x48px. |
| **Regresión Visual** | Playwright Screenshot Diff | Detectar cambios accidentales en la interfaz gráfica comparando capturas con un baseline establecido. | Discrepancia visual inferior al 0.5% en componentes centrales del POS y Landing. |
| **Accesibilidad (a11y)** | Lighthouse CI + axe-core | Garantizar navegación universal para personas con debilidad visual o motriz según WCAG 2.1 nivel AA. | Puntuación de accesibilidad Lighthouse ≥ 90/100; 0 violaciones graves en axe-core. |
| **Seguridad Web (SAST/DAST)** | eslint-plugin-security + OWASP Scripts | Identificar vulnerabilidades de inyección SQL, Cross-Site Scripting (XSS), omisión de reCAPTCHA y fallas de cabeceras. | 0 vulnerabilidades catalogadas como Altas o Críticas según el OWASP Top 10. |

---

### 8.3 Resultados Esperados e Impacto en los ODS

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                      RESULTADOS ESPERADOS E IMPACTO CUANTIFICABLE                      │
├──────────────────────┬──────────────────────────────────┬──────────────────────────────┤
│ Dimensión / ODS      │ Indicador Clave de Desempeño    │ Meta Cuantificable al Cierre │
├──────────────────────┼──────────────────────────────────┼──────────────────────────────┤
│ **ODS 8: Crecimiento │ • Reducción en tiempo de cobro   │ • De 2.5 min a < 30 seg      │
│ y Formalización**    │ • Discrepancia en arqueo de caja │ • Cero descuadres contables  │
│                      │ • Formalización de proveedores   │ • 100% compras registradas   │
├──────────────────────┼──────────────────────────────────┼──────────────────────────────┤
│ **ODS 9: Innovación  │ • Resiliencia en transacciones   │ • 99.9% consistencia eventual│
│ e Infraestructura**  │ • Disponibilidad de la nube      │ • Uptime > 99.5%             │
│                      │ • Eficiencia de carga y SEO      │ • Lighthouse Performance >85 │
├──────────────────────┼──────────────────────────────────┼──────────────────────────────┤
│ **ODS 12: Producción │ • Desvío de vasos desechables    │ • Reducción del 35% en 6 m   │
│ y Consumo Resp.**    │ • Pérdida de café por caducidad  │ • Merma inferior al 1.5%     │
│                      │ • Café con origen trazable       │ • 100% lotes orgánicos audit.│
├──────────────────────┼──────────────────────────────────┼──────────────────────────────┤
│ **ODS 16: Confianza  │ • Fugas de datos e intrusiones   │ • 0 brechas de seguridad     │
│ y Ciberseguridad**   │ • Transparencia transaccional    │ • Auditoría inmutable en BD  │
│                      │ • Cumplimiento de privacidad     │ • Aviso y cookies conformes  │
└──────────────────────┴──────────────────────────────────┴──────────────────────────────┘
```

1. **Impacto en ODS 8 (Trabajo Decente y Crecimiento Económico):**
   - Agilización del 80% en los tiempos de atención en barra durante horas pico, reduciendo el estrés laboral de los baristas.
   - Eliminación total de faltantes y sobrantes de caja gracias al registro digital de ventas mixtas y cálculo automatizado de vueltos.
   - Incremento del 25% en ingresos de cooperativas cafetaleras asociadas al recibir pedidos previsibles basados en la rotación del inventario.
2. **Impacto en ODS 9 (Industria, Innovación e Infraestructura):**
   - Implementación de un modelo de software transferible y replicable para otras MIPYMES gastronómicas sustentables.
   - Arquitectura en contenedores que reduce la huella de cómputo y el gasto en servidores hasta en un 40% respecto a arquitecturas basadas en máquinas virtuales dedicadas.
3. **Impacto en ODS 12 (Producción y Consumo Responsables):**
   - Ahorro proyectado de al menos 4,500 vasos y tapas desechables semestrales derivado de los incentivos del programa Monchis Rewards.
   - Disminución de mermas de café tostado a menos del 1.5% anual gracias a la política automatizada de primeras entradas, primeras salidas (PEPS) con alertas de caducidad.
   - Difusión de la cultura de consumo responsable mediante códigos QR en tickets y cartas digitales que muestran la biografía de la finca productora.
4. **Impacto en ODS 16 (Paz, Justicia e Instituciones Sólidas):**
   - Implementación de un modelo ético de software que respeta de manera integral los derechos digitales y la privacidad de los usuarios, sin recolectar datos innecesarios ni vender perfiles de consumo.
   - Trazabilidad y auditoría completa de eventos financieros para prevenir cualquier forma de desvío de recursos o fraude interno.

---

## 9. Referencias Bibliográficas (Formato IEEE)

1. United Nations, "Transforming our world: the 2030 Agenda for Sustainable Development," General Assembly, Resolution A/RES/70/1, Oct. 2015.
2. C. Becker *et al.*, "Sustainability Design in Software Engineering: Designing Externalities," in *Proc. 37th IEEE/ACM International Conference on Software Engineering (ICSE)*, Florence, Italy, 2015, pp. 467–476.
3. M. Fowler, "Saga Pattern: Sagas in Distributed Architectures," *MartinFowler.com*, Jan. 2019. [En línea]. Disponible en: https://martinfowler.com
4. Green Software Foundation, "Software Carbon Intensity (SCI) Specification v1.0," *Green Software Foundation Standards*, Dec. 2022.
5. OWASP Foundation, "OWASP Top 10: 2021 - The Ten Most Critical Web Application Security Risks," *Open Web Application Security Project*, 2021. [En línea]. Disponible en: https://owasp.org/Top10/
6. D. Jackson, "Software Requirements and System Architecture: Aligning Agile Practices with the UN Sustainable Development Goals," *IEEE Software*, vol. 39, no. 4, pp. 54–61, Jul.–Aug. 2022.
7. W3C, "Web Content Accessibility Guidelines (WCAG) 2.1," W3C Recommendation, World Wide Web Consortium, Jun. 2018. [En línea]. Disponible en: https://www.w3.org/TR/WCAG21/
8. E. Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Boston, MA, USA: Addison-Wesley, 2003.
9. I. Sommerville, *Software Engineering*, 10th ed., Boston, MA, USA: Pearson, 2015.
10. E. Gamma, R. Helm, R. Johnson, and J. Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software*, Reading, MA, USA: Addison-Wesley, 1994.

---

*Documento elaborado para la acreditación académica de la Unidad 1 — Administración de Proyectos, diseñado bajo los lineamientos pedagógicos del Dr. Gabriel Navarro Salcedo.*
