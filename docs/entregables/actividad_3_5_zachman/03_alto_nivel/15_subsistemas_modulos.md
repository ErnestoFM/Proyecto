# Nivel 3: ALTO NIVEL — Foco: DÓNDE
## Arquitectura de Subsistemas y Módulos — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En la arquitectura de software, la descomposición modular consiste en dividir un sistema complejo en subsistemas y módulos desacoplados con responsabilidades únicas y bien delimitadas (*Single Responsibility Principle*) (Bass et al., 2012). Como advierte Fowler (2002), cuando los sistemas empresariales se construyen como un monolito desordenado ("bola de lodo"), cualquier cambio pequeño en una pantalla de cobro termina rompiendo el módulo de inventarios o corrompiendo la base de datos. Para evitar esto, la ingeniería moderna recurre al diseño por capas y al uso de arquitecturas de Monorepo estructuradas en paquetes independientes (Sommerville, 2011).

Dentro de la Matriz de Zachman (1987), la celda **Alto Nivel - Dónde** define la distribución lógica de componentes (*System Architecture / Designer's View*). En este nivel del diseñador, respondemos a la pregunta: *¿Dónde reside cada función y cómo se comunican los subsistemas entre sí?* Para **Monchis Café**, adoptamos una arquitectura de **Monorepo** administrada con `pnpm workspaces` y `Turborepo`, separando con total claridad las aplicaciones de cara al usuario (`apps/`) de las bibliotecas de lógica compartida, persistencia y mensajería (`packages/`).

---

### 2. Mapa Arquitectónico de Subsistemas y Módulos

La siguiente estructura ilustra cómo se descomponen y relacionan los subsistemas del proyecto:

```
+=======================================================================================+
|                             MONOREPO ROOT (Turborepo)                                 |
+=======================================================================================+
|                               APLICACIONES (apps/)                                    |
|  +-------------------------------------+   +---------------------------------------+  |
|  |     SUBSISTEMA 1: apps/web          |   |       SUBSISTEMA 2: apps/api          |  |
|  |  (Frontend Vue 3 + Vite + vite-ssg) |   |    (Backend RESTful API Stateless)    |  |
|  |                                     |   |                                       |  |
|  |  * Mod. POS Mostrador (views/pos)   |   |  * Mod. Órdenes POS (api/pos/orders)  |  |
|  |  * Mod. Rewards (views/rewards)     |   |  * Mod. Lotes PEPS (api/inventory)    |  |
|  |  * Mod. Admin y Analítica (views)   |   |  * Mod. Analítica UTM (api/admin)     |  |
|  |  * Mod. Auth y Perfil (Pinia store) |   |  * Mod. Auth Stateless (JWT/reCAPTCHA)|  |
|  |  * Mod. Catálogo Público SEO (SSG)  |   |  * Mod. Alertas SMTP (EmailService)   |  |
|  +-------------------------------------+   +---------------------------------------+  |
|                     |                                          |                      |
|                     +--------------------+---------------------+                      |
|                                          |                                            |
|                                          v                                            |
|                               PAQUETES (packages/)                                    |
|  +---------------------------------------------------------------------------------+  |
|  | SUBSISTEMA 3: packages/database (Prisma ORM + PostgreSQL 15)                    |  |
|  |  * Tablas: User, Product, Batch, Order, OrderItem, Attribution, SagaStateLog. |  |
|  +---------------------------------------------------------------------------------+  |
|  | SUBSISTEMA 4: packages/messaging (RabbitMQ + Patrón Saga + DLQ)                |  |
|  |  * RabbitMQClient, SagaWorker (Reversas transaccionales) y colas diferidas.    |  |
|  +---------------------------------------------------------------------------------+  |
|  | SUBSISTEMA 5: packages/shared-types (Contratos DTO y Tipos TypeScript)         |  |
|  +---------------------------------------------------------------------------------+  |
+=======================================================================================+
```

---

### 3. Descripción Detallada de Subsistemas

#### 3.1 Subsistema 1: Frontend Web y POS de Mostrador (`apps/web`)
* **Responsabilidad:** Proveer la interfaz gráfica tanto para los clientes en internet como para el personal que cobra en mostrador.
* **Módulos Internos:**
  - *Módulo POS (`src/views/pos/`):* Terminal de cobro rápido con cálculo reactivo de subtotales, bonificación ecológica y atajos de teclado (`F2`, `Esc`).
  - *Módulo Monchis Rewards (`src/views/rewards/`):* Visualización de la tarjeta de 8 sellos digitales e incentivos ecológicos.
  - *Módulo Administrativo (`src/views/admin/`):* Tablero con analítica de ventas, trazabilidad de lotes y exportación en Excel/PDF.
  - *Módulo de Autenticación (`src/views/auth/` y `stores/authStore.ts`):* Control de sesiones con token en memoria y validación reCAPTCHA.
  - *Módulo Prerenderizado SEO (`vite-ssg`):* Generación de HTML estático en tiempo de compilación para la landing page (`/`), menú y contacto.

#### 3.2 Subsistema 2: Core API Gateway y Servicios de Negocio (`apps/api`)
* **Responsabilidad:** Exponer endpoints RESTful seguros, validar datos con esquemas Zod y ejecutar las reglas de negocio de la cafetería.
* **Módulos Internos:**
  - *Módulo de Transacciones POS (`src/app/api/pos/orders/`):* Procesamiento atómico de órdenes, decremento de inventario y cálculo de cambio.
  - *Módulo de Inventario y Lotes (`src/app/api/inventory/batches/`):* Registro y consulta de lotes de café campesino bajo rotación PEPS.
  - *Módulo de Seguridad Stateless (`src/lib/jwt.ts` y `src/lib/recaptcha.ts`):* Emisión de JWT, rotación de cookies y verificación anti-bot con Google.
  - *Módulo de Autenticación 2FA (`src/lib/totp.ts`):* Generación y validación de códigos de segundo factor para Administrador.
  - *Módulo de Alertas Sanitarias (`src/lib/emailService.ts`):* Despacho de notificaciones preventivas de caducidad por correo SMTP.

#### 3.3 Subsistema 3: Capa de Persistencia y Acceso a Datos (`packages/database`)
* **Responsabilidad:** Garantizar la integridad referencial y transaccional ACID de la información comercial en PostgreSQL 15 mediante Prisma ORM.
* **Modelos Centrales:**
  - `User`: Credenciales, rol RBAC (`ADMIN`, `CAJERO`, `CLIENTE`), sellos Rewards y secreto 2FA.
  - `Product`: Catálogo oficial con precio unitario blindado y categoría (Orgánico vs Comercial).
  - `Batch`: Lotes de café de especialidad con finca de origen, altitud, fechas de tueste y caducidad.
  - `Order` y `OrderItem`: Registro inmutable de transacciones, desglose de IVA y método de pago.
  - `Attribution`: Persistencia de canales UTM de adquisición (Google Maps, Instagram).
  - `RevokedToken`: Blacklist persistente para invalidación inmediata de sesiones cerradas.

#### 3.4 Subsistema 4: Mensajería Asíncrona y Orquestación Saga (`packages/messaging`)
* **Responsabilidad:** Manejar eventos desacoplados y garantizar la consistencia eventual entre el cobro y el inventario.
* **Componentes:**
  - `RabbitMQClient`: Gestión de conexiones AMQP y declaración de Exchanges (`cafeteria.events`).
  - `SagaWorker`: Consumidor que escucha rupturas de stock y orquesta la transacción compensatoria (reversa) y reembolso al cliente.
  - `DeadLetterQueue (orders.dlq)`: Cola de aislamiento para eventos con fallas reiteradas con alerta crítica por correo electrónico.

---

### 4. Justificación Práctica en el Proyecto

Dividir el software en subsistemas independientes nos permite garantizar lo que en arquitectura se conoce como alta cohesión y bajo acoplamiento (Bass et al., 2012). En Monchis Café, esto significa que si la conexión a internet externa falla temporalmente o si la pasarela bancaria tarda en responder, la interfaz del POS no se queda congelada; puede continuar operando con su caché local y reintentar de forma asíncrona a través de las colas de RabbitMQ. Del mismo modo, el dueño puede consultar la analítica sin riesgo de alentar la terminal donde el barista está cobrando.

---

### 5. Referencias Bibliográficas

1. **Bass, L., Clements, P., & Kazman, R. (2012).** *Software Architecture in Practice* (3.ª ed.). Addison-Wesley.
2. **Fowler, M. (2002).** *Patterns of Enterprise Application Architecture*. Addison-Wesley.
3. **Sommerville, I. (2011).** *Ingeniería del software* (9.ª ed.). Addison-Wesley / Pearson Educación.
4. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

