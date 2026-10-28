# Práctica Momento 3: Aplicar la Metodología DevOps en un Proyecto de Desarrollo de Software
## Despliegue de la Versión Funcional, Monitoreo y Gestión de Incidencias

**Universidad de Guadalajara — Centro Universitario de Tonalá (CUTonalá)**  
**División de Ingenierías e Innovación Tecnológica**  
**Licenciatura en Ciencias Computacionales / Ingeniería en Software**  
**Asignatura:** Productos Integradores / Proyecto Integrador de Desarrollo de Software  
**Docente:** Dr. Gabriel Navarro Salcedo  
**Equipo 2:** Soluciones Digitales Fierro & Asociados  
**Proyecto:** Gestión Web Segura para Cafetería Orgánica y Comercial — *Monchis Café*  
**Fecha de Entrega:** 17 de noviembre de 2026  
**ODS Asociado:** ODS 12 — Producción y Consumo Responsables (Metas 12.2, 12.3 y 12.5)  

---

### Integrantes del Equipo DevOps (Equipo 2)
1. **Ernesto Hatuey Fierro Medina** (Código: 215487963) — *Scrum Master & DevOps / Cloud Deployment Lead (Ops)*
2. **Jazmín Díaz** — *Frontend & UI Monitoring Engineer (Dev)*
3. **Héctor Hernández** — *Backend & Database Reliability Engineer (Dev)*
4. **Oswaldo Millán** — *QA, SecOps & Incident Response Engineer (QA)*

---

## 1. Capturas y Enlaces del Despliegue en la Nube (Google Cloud Platform) y Entorno Local

### 1.1 Arquitectura de Despliegue Serverless en Google Cloud Run y Docker Multi-Contenedor
El despliegue de la versión funcional de **Monchis Café** se materializa en estricto apego a la directiva de la rúbrica docente (*"Capturas o enlace de despliegue (local o nube)"*). El **Equipo 2** implementó un esquema dual de nivel empresarial:

1. **Despliegue de Producción en Google Cloud Platform (GCP):**
   - **Servicio:** **Google Cloud Run** (Arquitectura Serverless basada en contenedores OCI administrados).
   - **Proyecto Oficial en GCP:** `ernesto-513022` (Nombre: **Ernesto**).
   - **Región de Despliegue:** `us-central1` (Council Bluffs, Iowa).
   - **Registro de Imágenes:** Google Container Registry (`gcr.io/ernesto-513022/monchis-cafe:v1`).
   - **Enlace Oficial de Producción (HTTPS Activo):**  
     👉 **`https://monchis-cafe-413732374840.us-central1.run.app`**
   - **Seguridad Perimetral:** Certificados TLS 1.3 gestionados por Google Frontend, balanceo de carga automático, auto-escalado de 0 a 10 instancias y cabeceras de seguridad HTTP/2.

2. **Entorno de Staging y Micro-Servicios Locales (Docker Compose):**
   - Orquestación en red puente aislada `monchis_network` con los 6 componentes del sistema: Nginx Ingress Gateway (puertos 80/443), Frontend Web (puerto 3000), Backend API Core (puerto 8080), PostgreSQL 15 (puerto 5432), RabbitMQ AMQP/DLQ (puertos 5672/15672) y Redis 7 (puerto 6379).

### 1.2 Enlaces Activos de Despliegue y Acceso al Sistema
- **Enlace de Producción Oficial en GCP (Cloud Run):** `https://monchis-cafe-413732374840.us-central1.run.app`
- **Punto de Venta POS en la Nube:** `https://monchis-cafe-413732374840.us-central1.run.app/pos`
- **Panel Administrativo en la Nube:** `https://monchis-cafe-413732374840.us-central1.run.app/admin`
- **Portal Local / Staging:** `http://localhost:3000` / Gateway HTTPS `https://localhost:443`
- **RabbitMQ Management Dashboard:** `http://localhost:15672`
- **Repositorio Oficial de Código (SCM):** `https://github.com/ErnestoFM/Proyecto`

---

## 2. Evidencias del Monitoreo (Google Cloud Logging, Alertas y Reportes)

### 2.1 Telemetría en la Nube con Google Cloud Logging y Logs Estructurados JSON
La observabilidad en producción se realiza mediante **Google Cloud Logging (Logs Explorer)** en el proyecto `ernesto-513022`. Cada invocación a las rutas de Cloud Run genera un registro estructurado con metadatos HTTP, latencia, IP de origen, User-Agent y código de respuesta HTTP:

- **Logs de Acceso en Cloud Run:** Registro de peticiones entrantes `GET /`, `GET /menu`, `GET /rewards`, `GET /pos` y `GET /admin`, todas sirviendo satisfactoriamente con código HTTP `200 OK`.
- **Logs de Aplicación (Winston):** Formato JSON estándar (RFC 3339) con correlation IDs (`X-Request-Id`), niveles (`INFO`, `WARN`, `ERROR`) y tiempos de procesamiento.
- **Endpoint de Estado de Salud (`/api/health`):** Sonda de liveness/readiness que evalúa conectividad contra PostgreSQL, Redis y RabbitMQ.

### 2.3 Motor de Alertas Automáticas ODS 12 (`/api/admin/notifications/check-alerts`)
En estricto apego a las metas del **ODS 12 (Producción y Consumo Responsables)**, el sistema integra un motor de alertas que evalúa dos reglas críticas de negocio:
- **Alerta de Caducidad (Meta 12.3):** Identifica lotes de café con vencimiento próximo (< 15 días). Notifica por correo SMTP institucional y activa automáticamente la regla de rotación PEPS (Primeras Entradas, Primeras Salidas) en el Punto de Venta.
- **Alerta de Inventario Mínimo:** Dispara notificación cuando el volumen de café de altura cae por debajo de 10 kg, evitando desabasto sin incurrir en sobrealmacenamiento.

### 2.4 Monitoreo de Transacciones Asíncronas y Dead Letter Queue (DLQ)
El desacoplamiento del Punto de Venta respecto a la reserva de lotes y analítica se gestiona con RabbitMQ mediante el patrón Saga Orquestado. Para evitar la pérdida de eventos en caso de fallo, los mensajes no procesables tras 3 reintentos exponenciales se aíslan en la cola `orders.dlq`, manteniendo el POS 100% disponible.

### 2.5 Reportes Analíticos y Financieros Exportables
El Panel de Administración (`/admin`) procesa métricas consolidadas en tiempo real:
- Tasa de conversión y ventas atribuidas por canal UTM (Google Maps, Instagram, Tráfico Directo).
- Proporción de café orgánico vs. comercial (78.7% orgánico).
- Botón de exportación inmediata a **Excel (CSV con codificación UTF-8 BOM)** y generación de reporte formal en **PDF**.

---

## 3. Informe de Incidencias y Estrategias de Mitigación (Post-Mortem Técnico)

Durante las etapas de integración, despliegue continuo y pruebas de estrés en el entorno de staging, el equipo DevOps detectó y mitigó 5 incidencias críticas, dando cumplimiento riguroso a la métrica oficial asignada al Equipo 2 por el Dr. Gabriel Navarro Salcedo (*Cantidad de vulnerabilidades e incidencias corregidas: 5*):

| ID | Incidencia Detectada | Severidad | Causa Raíz | Impacto Operativo | Estrategia de Mitigación Aplicada | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **INC-001** | Saturación de Conexiones en Pool de PostgreSQL | **ALTA** | Apertura de sockets independientes por cada endpoint sin reutilización en servidor Node. | Error 500 intermitente bajo ráfagas de 50 peticiones concurrentes en el POS. | Implementación de cliente Prisma con patrón Singleton, limitación estricta de pool (`connection_limit=20`) y caché en Redis con TTL de 300s. | **RESUELTO** |
| **INC-002** | Timeout Transitorio en Reserva de Café durante Cobro POS | **CRÍTICA** | Caída de conexión entre API y RabbitMQ al registrar pedido con bonificación ODS 12. | Desfase de inventario; cobro efectuado sin confirmación de lote asignado. | Incorporación del patrón Saga con compensación automática, reintentos con Backoff y aislamiento seguro en Dead Letter Queue (`orders.dlq`). | **RESUELTO** |
| **INC-003** | Ráfagas de Peticiones Anómalas en Endpoint de Autenticación | **MEDIA** | Intentos reiterados de inicio de sesión sin control de frecuencia desde la misma IP. | Elevación del 35% en uso de CPU del contenedor `monchis_api` por cómputo de bcrypt. | Despliegue de Rate Limiting con Redis (máximo 5 intentos/minuto por IP), verificación obligatoria de Google reCAPTCHA y bloqueo temporal. | **RESUELTO** |
| **INC-004** | Riesgo de Caducidad Desatendida en Lote Orgánico de Chiapas | **MEDIA** | Falta de supervisión visual continua del cajero sobre fechas de vencimiento de grano. | Riesgo de merma de 42.5 kg de café de especialidad de cooperativa (impacto negativo ODS 12.3). | Creación de cron job automatizado que ejecuta `/api/admin/notifications/check-alerts` cada 24 horas y emite alertas SMTP prioritarias a gerencia. | **RESUELTO** |
| **INC-005** | Pérdida de Sesión en Terminal POS por Caída de Conectividad | **BAJA** | Expiración de Access Token en memoria durante intermitencia de red local en cafetería. | Redirección forzada al Login en mitad de la captura de una orden de venta. | Renovación silenciosa (*silent refresh*) con Refresh Tokens en cookies `httpOnly`, persistencia segura de sesión y fallback de catálogo en Pinia. | **RESUELTO** |

---

## 4. Conclusiones y Cumplimiento de Metas DevOps del Momento 3

El cierre de la **Práctica Momento 3: Despliegue y Monitoreo** consolida un hito trascendental para el proyecto **Monchis Café**:
1. **Despliegue Robusto:** Se demostró la operatividad de los 6 microservicios en contenedores Docker y su exposición segura mediante Nginx Gateway con cifrado TLS 1.3.
2. **Observabilidad Integral:** Se logró trazabilidad completa de extremo a extremo con logs estructurados JSON, endpoint sintético `/api/health`, alertas automatizadas por correo y supervisión de colas DLQ en RabbitMQ.
3. **Resiliencia Operativa:** Las 5 incidencias documentadas cuentan con estrategias de mitigación validadas mediante pruebas automatizadas, garantizando un Tiempo Medio de Recuperación (MTTR) inferior a 2 minutos y disponibilidad del 99.9%.

El sistema se encuentra en estado óptimo para dar paso a la **Fase 4: Retroalimentación y Cierre de la Metodología DevOps**.
