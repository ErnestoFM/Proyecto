# Módulo: Planificación DevOps — Momento 1 (Equipo 2)

#devops #planificacion #momento1 #equipo2 #seguridad #ods12 #scrum #ci_cd

Nota técnica y estratégica que documenta la fase de **Planificación DevOps (Momento 1)** para el proyecto **"Gestión Web Segura para Cafetería Orgánica y Comercial"** ([[Contexto/Index|Monchis Café]]), en cumplimiento de las directrices académicas del **Dr. Gabriel Navarro Salcedo** para la cátedra de **Productos Integradores de Desarrollo de Software** (Universidad de Guadalajara / CUTonalá).

---

## 1. Definición del Proyecto y ODS Asociado

- **Nombre Oficial:** Gestión Web Segura para Cafetería Orgánica y Comercial
- **Identificador de Equipo:** Equipo 2
- **Solución Técnica:** Monchis Café (Monorepo con Vue 3 + Node.js API + PostgreSQL + RabbitMQ Saga)
- **Eje Rector Sostenible:** **ODS 12 — Producción y Consumo Responsables**
  - *Meta 12.2:* Priorización de café orgánico de especialidad cultivado bajo sombra sin pesticidas sintéticos por cooperativas campesinas locales (Michoacán, Chiapas y Oaxaca).
  - *Meta 12.5:* **Bonificación Ecológica** automatizada en el Punto de Venta (POS): descuento directo de $5.00 MXN y sellos digitales dobles en "Monchis Rewards" para clientes que aporten su taza o termo reutilizable, eliminando el desecho masivo de vasos de polipapel.
  - *Meta 12.3:* Minimización de mermas de alimentos perecederos mediante algoritmo de rotación de inventarios **PEPS (Primeras Entradas, Primeras Salidas)** y alertas por correo SMTP.
  - *ODS Complementarios:* **ODS 8 (Trabajo Decente y Crecimiento Económico)** y **ODS 9 (Industria, Innovación e Infraestructura)**.

---

## 2. Estructura de Roles del Equipo DevOps

El equipo de 4 ingenieros elimina la brecha tradicional entre desarrollo y operaciones mediante una distribución balanceada de responsabilidades:

1. **Scrum Master (Ernesto Hatuey Fierro Medina):**
   - Facilitación ágil (Daily Standups de 15 min, Sprint Planning, Reviews y Retrospectivas semanales).
   - Administración del tablero Kanban en Trello, límites WIP y verificación estricta del *Definition of Done (DoD)*.
2. **Ops / DevOps Lead (Ernesto Hatuey Fierro Medina):**
   - Contenedorización inmutable mediante `Dockerfile` multi-stage y orquestación con `docker-compose.yml`.
   - Implementación de pipelines de Integración Continua (CI) en Jenkins y GitHub Actions.
   - Automatización de Despliegue Continuo (CD) con HTTPS forzado (Frontend en Vercel y Backend en Nginx Reverse Proxy con TLS).
   - Observabilidad: logs estructurados con Winston/Morgan y sondeo recurrente del endpoint `/health`.
3. **Dev Backend Core (Héctor Hernández):**
   - API RESTful en Node.js y TypeScript con validaciones Zod.
   - Modelado de base de datos relacional y migraciones en PostgreSQL mediante Prisma ORM.
   - Seguridad: autenticación stateless JWT, Refresh Tokens en cookies `httpOnly`, hashing `bcrypt` (salt 12) y middleware RBAC (`admin`, `cajero`, `cliente`).
   - Broker RabbitMQ con patrón Saga para reversas transaccionales ante desabasto de inventario orgánico.
4. **Dev Frontend Core (Jazmín Díaz):**
   - SPA reactiva en Vue 3 con Vite y gestión de estado con Pinia.
   - Punto de Venta (POS) táctil para mostrador con cobro ágil multipago.
   - Catálogo segmentado (orgánicos vs comerciales) con visualización de trazabilidad ODS 12.
   - Navigation Guards en Vue Router basados en los claims del token JWT y Google reCAPTCHA v2/v3.
5. **QA & Security Engineer (Oswaldo Millán):**
   - Pruebas unitarias y de integración con Vitest y Supertest.
   - Pruebas E2E automatizadas con Playwright simulando navegación y validación de permisos RBAC.
   - Escaneo estático SAST con `npm audit` y Snyk Open Source.
   - Seguimiento y reporte oficial de la métrica del Equipo 2: **"Cantidad de vulnerabilidades corregidas"**.

---

## 3. Plan de Trabajo en 4 Semanas (4 Momentos)

```
[Semana 1: Momento 1] -> [Semana 2: Momento 2] -> [Semana 3: Momento 3] -> [Semana 4: Momento 4]
Planificación & Setup -> Desarrollo & CI        -> Despliegue & Monitoreo -> Retroalimentación & Cierre
(28 Oct - 03 Nov)        (04 Nov - 10 Nov)         (11 Nov - 17 Nov)         (18 Nov - 24 Nov)
```

- **Semana 1 (Momento 1: Planificación - Entrega: 3 nov):**
  - T1.1 Alcance, arquitectura técnica y justificación ODS 12.
  - T1.2 Repositorio GitHub con ramas protegidas (`main`, `develop`) y Conventional Commits.
  - T1.3 Tablero Kanban en Trello con columnas DevOps y políticas WIP.
  - T1.4 Matriz RBAC, esquemas Prisma y directrices de seguridad web.
  - T1.5 Diagrama de flujo del proceso DevOps y entregable: `Proyecto_Equipo2_Momento1_Planificacion.pdf`.
- **Semana 2 (Momento 2: Desarrollo e Integración Continua - Entrega: 10 nov):**
  - T2.1 API Node.js con autenticación JWT, RBAC y CRUD en PostgreSQL.
  - T2.2 Frontend Vue 3: interfaz POS, catálogo orgánico y navegación por roles.
  - T2.3 `Dockerfile` multi-stage y `docker-compose.yml` local.
  - T2.4 Pipeline CI en Jenkins / GitHub Actions (Linting + SAST Snyk + Tests Vitest).
  - T2.5 Pruebas unitarias automáticas y reporte de errores corregidos (`Proyecto_Equipo2_Momento2_Integracion.pdf`).
- **Semana 3 (Momento 3: Despliegue y Monitoreo - Entrega: 17 nov):**
  - T3.1 Despliegue del Frontend en Vercel con HTTPS automático forzado.
  - T3.2 Despliegue del Backend API y PostgreSQL en contenedor cloud con Nginx TLS.
  - T3.3 Cabeceras HTTP de seguridad con Helmet (CSP, HSTS, CORS restrictivo).
  - T3.4 Observabilidad con logs Winston y endpoint `/health`.
  - T3.5 Escaneo de vulnerabilidades y cuantificación de la métrica clave (`Proyecto_Equipo2_Momento3_Despliegue.pdf`).
- **Semana 4 (Momento 4: Retroalimentación y Cierre - Entrega: 24 nov):**
  - T4.1 Métricas DevOps (Lead Time, frecuencia de despliegues, MTTR y cobertura de tests).
  - T4.2 Retrospectiva formal del equipo y evaluación de la Toolchain.
  - T4.3 Auditoría final del tablero Trello completado.
  - T4.4 Plan de mejora continua (GitOps, Kubernetes, DAST continuo).
  - T4.5 Documento de reflexión y cierre (`Proyecto_Equipo2_Momento4_Reflexion.pdf`).

---

## 4. Cadena de Herramientas DevOps (Toolchain Oficial)

| Categoría | Herramienta | Rol y Justificación Técnica |
| :--- | :--- | :--- |
| **Planificación Ágil** | **Trello & GitHub Projects** | Tablero Kanban con límites WIP, asignación de tareas y checklists DoD. |
| **Control de Versiones** | **GitHub (GitFlow)** | Ramas `main` y `develop` protegidas, Pull Requests obligatorios y Conventional Commits. |
| **Integración Continua** | **Jenkins & GitHub Actions** | Automatización de compilaciones, linting, análisis SAST y pruebas unitarias paralelas. |
| **Contenedorización** | **Docker & Docker Compose** | Imágenes multi-stage ligeras en Alpine y orquestación local con paridad garantizada. |
| **Base de Datos** | **PostgreSQL 15 & Prisma** | Transacciones ACID para cobros de caja y prevención nativa de inyecciones SQL. |
| **DevSecOps** | **Snyk, npm audit, Helmet, reCAPTCHA** | Detección de CVEs, cabeceras de blindaje HTTP y protección contra bots en formularios. |
| **Testing Automatizado** | **Vitest, Supertest, Playwright** | Pruebas unitarias ultrarrápidas, integración de endpoints y suites E2E multi-rol. |
| **Despliegue CD** | **Vercel & Nginx TLS** | Aprovisionamiento de SSL/HTTPS forzado en Frontend y Backend conforme al Momento 3. |
| **Observabilidad** | **Winston Logger & `/health`** | Logging estructurado JSON y sondeo continuo de latencia y estado del servidor. |

---

## 5. Entregables Generados

- [`Proyecto_Equipo2_Momento1_Planificacion.pdf`](file:///d:/ernestofm/Proyecto/docs/entregables/Proyecto_Equipo2_Momento1_Planificacion.pdf) (Compilado con Chrome Headless, 13 páginas, portada institucional y diagramas).
- [`Proyecto_MonchisCafe_Momento1_Planificacion.pdf`](file:///d:/ernestofm/Proyecto/docs/entregables/Proyecto_MonchisCafe_Momento1_Planificacion.pdf) (Copia por nombre de proyecto).
- [`Proyecto_Equipo2_Momento1_Planificacion.docx`](file:///d:/ernestofm/Proyecto/docs/entregables/Proyecto_Equipo2_Momento1_Planificacion.docx) (Documento Word editable en formato institucional).
- [`Proyecto_Equipo2_Momento1_Planificacion.md`](file:///d:/ernestofm/Proyecto/docs/entregables/Proyecto_Equipo2_Momento1_Planificacion.md) (Especificación técnica completa en Markdown).
- Copias en `C:\Users\erfierro\Downloads\` preparadas para su entrega inmediata en plataforma educativa.
