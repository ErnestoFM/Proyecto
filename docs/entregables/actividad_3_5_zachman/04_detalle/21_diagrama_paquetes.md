# Nivel 4: DETALLE — Foco: DÓNDE
## Diagrama de Paquetes — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En el estándar de modelado UML, el diagrama de paquetes se utiliza para agrupar elementos del diseño (clases, interfaces, componentes o módulos) en unidades de software de mayor nivel, mostrando las dependencias lógicas y físicas existentes entre ellos (Object Management Group [OMG], 2017). Como explica Robert C. Martin (2002) en sus principios de arquitectura ágil de paquetes, una estructura modular saludable debe regirse por el **Principio de Dependencias Acíclicas** (*Acyclic Dependencies Principle - ADP*), el cual establece que la estructura de dependencias entre paquetes no debe contener ciclos cerrados. Si el paquete A depende de B, y B depende de C, bajo ninguna circunstancia C debe volver a depender de A.

Dentro de la Matriz de Zachman (1987), la celda **Detalle - Dónde** corresponde a la vista del constructor (*Technology Network & Package Model / Builder's View*). En este nivel del código físico, formalizamos la distribución de paquetes administrados mediante `pnpm workspaces` y `Turborepo` en el repositorio de **Monchis Café**. Cada paquete tiene su propio archivo de configuración (`package.json`), su ciclo de compilación independiente y contratos tipados en TypeScript que evitan el acoplamiento desordenado.

---

### 2. Diagrama de Paquetes UML del Monorepo

El siguiente diagrama modela la organización de paquetes del proyecto y el flujo estrictamente unidireccional de sus dependencias:

```
+=======================================================================================+
|                            MONOREPO: monchis-cafe                                     |
+=======================================================================================+
|                                                                                       |
|   +---------------------------------------+   +------------------------------------+  |
|   |         package: @monchis/web         |   |       package: @monchis/api        |  |
|   |    (Frontend Vue 3 SPA / vite-ssg)    |   |     (Backend Next.js REST API)     |  |
|   |                                       |   |                                    |  |
|   |   - views/ (pos, admin, rewards, auth)|   |   - app/api/ (orders, batches)     |  |
|   |   - stores/ (posStore, authStore)     |   |   - lib/ (jwt, recaptcha, totp)    |  |
|   |   - components/ (Navbar, Modales)     |   |   - middleware/ (authMiddleware)   |  |
|   +---------------------------------------+   +------------------------------------+  |
|             |                  |                         |               |            |
|             |                  |                         |               |            |
|             | <<import>>       | <<import>>              | <<import>>    | <<import>> |
|             v                  +------------+    +-------+               v            |
|   +--------------------+                    |    |           +---------------------+  |
|   | package:           |                    v    v           | package:            |  |
|   | @monchis/config    |               +-------------------+ | @monchis/messaging  |  |
|   |                    |               | package:          | |                     |  |
|   | - tokens.css       |               | @monchis/         | | - RabbitMQClient    |  |
|   | - eslint-config    |               | shared-types      | | - SagaWorker        |  |
|   | - tsconfig.base    |               |                   | | - DLQ & Retries     |  |
|   +--------------------+               | - DTOs & Enums    | +---------------------+  |
|                                        | - Interfaces      |              |           |
|                                        +-------------------+              |           |
|                                                  ^                        |           |
|                                                  | <<import>>             | <<import>>|
|                                                  |                        v           |
|                                        +-------------------------------------------+  |
|                                        |       package: @monchis/database          |  |
|                                        |      (Prisma ORM + PostgreSQL 15)         |  |
|                                        |                                           |  |
|                                        |   - prisma/schema.prisma                  |  |
|                                        |   - migrations/ (Historial versionado)    |  |
|                                        |   - seed.ts (Poblado de datos maestros)   |  |
|                                        +-------------------------------------------+  |
|                                                                                       |
+=======================================================================================+
```

---

### 3. Matriz de Responsabilidades y Dependencias entre Paquetes

| Paquete | Tipo de Artefacto | Responsabilidad Técnica | Dependencias Permitidas (Hacia Adentro) |
| :--- | :--- | :--- | :--- |
| **`@monchis/web`** | Aplicación Cliente (Vue 3) | Renderizado de interfaces de mostrador, navegación en cliente, gestión de estado con Pinia y llamadas HTTP a la API. | `@monchis/shared-types`<br>`@monchis/config` |
| **`@monchis/api`** | Aplicación Servidor (Node.js) | Exposición de Route Handlers RESTful, validación con Zod, middleware RBAC, despacho de eventos y orquestación. | `@monchis/shared-types`<br>`@monchis/database`<br>`@monchis/messaging` |
| **`@monchis/database`** | Biblioteca de Persistencia | Definición del esquema relacional en Prisma, migraciones versionadas y consultas transaccionales hacia PostgreSQL. | `@monchis/shared-types` |
| **`@monchis/messaging`** | Biblioteca de Eventos | Cliente AMQP para conexión con RabbitMQ, publicación en Topic Exchanges, consumidor Saga y aislamiento en DLQ. | `@monchis/shared-types`<br>`@monchis/database` |
| **`@monchis/shared-types`** | Biblioteca de Tipos | Contratos de interfaces TypeScript, DTOs de petición/respuesta y enumeraciones (`UserRole`, `EstadoOrden`, `MetodoPago`). | **Ninguna** (Paquete hoja totalmente desacoplado). |
| **`@monchis/config`** | Biblioteca de Estilos y Reglas | Definición de variables y tokens de diseño CSS pastel, reglas de linter y configuración base de TypeScript. | **Ninguna** (Paquete hoja independiente). |

---

### 4. Justificación Práctica en el Proyecto

Organizar el proyecto en paquetes bajo el principio de dependencias acíclicas (ADP) es lo que garantiza que el desarrollo no se vuelva un laberinto con el paso de los meses. Como señala Martin (2002), cuando los paquetes comparten contratos tipados sin depender circularmente entre sí, es posible compilar y probar componentes de manera aislada con herramientas como Turborepo. En Monchis Café, si modificamos una regla de tipos en `@monchis/shared-types` (como agregar un nuevo campo al DTO de la orden), el compilador de TypeScript detecta automáticamente en qué pantallas de la web y en qué endpoints de la API debe ajustarse el código, evitando que errores de tipado o discrepancias de nombres se cuelen a producción.

---

### 5. Referencias Bibliográficas

1. **Martin, R. C. (2002).** *Agile Software Development, Principles, Patterns, and Practices*. Prentice Hall.
2. **Object Management Group. (2017).** *OMG Unified Modeling Language (OMG UML), Version 2.5.1*. OMG Document Number: formal/2017-12-05. https://www.omg.org/spec/UML/2.5.1/
3. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
4. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

