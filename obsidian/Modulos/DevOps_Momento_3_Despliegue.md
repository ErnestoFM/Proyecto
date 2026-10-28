# Módulo: Despliegue y Monitoreo — Momento 3 (Equipo 2)

#devops #despliegue #monitoreo #observabilidad #momento3 #equipo2 #docker #nginx #winston #sre #postmortem #ods12 #monchis_cafe

Nota técnica y estratégica que documenta la fase de **Despliegue de la Versión Funcional, Monitoreo y Gestión de Incidencias (Momento 3)** para el proyecto **"Gestión Web Segura para Cafetería Orgánica y Comercial"** ([[Contexto/Index|Monchis Café]]), en cumplimiento de las directrices académicas del **Dr. Gabriel Navarro Salcedo** para la cátedra de **Productos Integradores de Desarrollo de Software** (Universidad de Guadalajara / CUTonalá).

---

## 1. Topología de Despliegue en Google Cloud Platform (Cloud Run) y Docker Compose

El despliegue operativo de la versión funcional de **Monchis Café** se materializa en la nube y en entorno local:

- **Despliegue en la Nube (Google Cloud Platform):**
  - **Servicio:** Google Cloud Run (Serverless OCI Containers).
  - **Proyecto Oficial GCP:** `ernesto-513022` (Nombre: **Ernesto**).
  - **Región:** `us-central1` (Iowa).
  - **Imagen en Registro:** `gcr.io/ernesto-513022/monchis-cafe:v1` (Cloud Build).
  - **URL de Producción Activa:** `https://monchis-cafe-413732374840.us-central1.run.app`
  - **Seguridad:** Certificados TLS 1.3 administrados por Google Frontend y auto-escalado de 0 a 10 instancias.

- **Despliegue Local de Staging (Docker Compose):**
  - Orquestación en red puente `monchis_network` con los 6 servicios desacoplados: Nginx Gateway (80/443), Frontend Web (3000), Backend API Core (8080), PostgreSQL 15 (5432), RabbitMQ AMQP/DLQ (5672/15672) y Redis 7 (6379).

---

## 2. Pilares de Observabilidad y Monitoreo (SRE)

1. **Google Cloud Logging (Logs Explorer en la Nube):**
   - Telemetría de producción en el proyecto `ernesto-513022` con registro de peticiones HTTP en tiempo real (`GET /`, `/menu`, `/rewards`, `/pos`, `/admin`) sirviendo con código 200 OK y latencia en ms.
2. **Logs Estructurados JSON (Winston):**
   - Formato RFC 3339 con severidades (`INFO`, `WARN`, `ERROR`), request correlation IDs (`X-Request-Id`) y sanitización.
3. **Endpoint Sintético de Salud (`/api/health`):**
   - Retorna estado operativo `UP` evaluando latencia de PostgreSQL (1.8 ms), estado de Redis y canales activos en RabbitMQ.
4. **Motor de Alertas Automáticas ODS 12 (`/api/admin/notifications/check-alerts`):**
   - Detección preventiva de lotes de café con caducidad próxima (< 15 días, Meta 12.3) con alertas SMTP a gerencia y rotación PEPS forzada en POS.
5. **Auditoría de Mensajería Asíncrona y Dead Letter Queue (DLQ):**
   - Supervisión continua de la cola `orders.dlq` en RabbitMQ garantizando 0 transacciones perdidas en el flujo Saga.
6. **Reportes Operativos y Analíticos:**
   - Visualización y exportación de métricas de ventas y conversión UTM en formato CSV (compatible con Excel) y versión formal PDF desde `http://localhost:3000/admin`.

---

## 3. Matriz de Incidencias Técnicas y Mitigación (Post-Mortem)

En estricto cumplimiento con la métrica oficial asignada al Equipo 2 (*Cantidad de vulnerabilidades e incidencias corregidas: 5*):

| ID | Incidencia | Severidad | Causa Raíz | Mitigación Aplicada | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **INC-001** | Saturación de Conexiones Pool PostgreSQL | **ALTA** | Apertura de sockets independientes sin reutilización bajo tráfico concurrente en el POS. | Patrón Singleton en `prisma.ts`, `connection_limit=20` y capa de caché en Redis (TTL 300s). | **RESUELTO** |
| **INC-002** | Timeout Transaccional en Reserva POS | **CRÍTICA** | Cierre transitorio de canal AMQP durante confirmación de orden con descuento ODS 12. | Patrón Saga con compensación automática de stock y aislamiento en Dead Letter Queue (`orders.dlq`). | **RESUELTO** |
| **INC-003** | Ráfagas de Fuerza Bruta en Login | **MEDIA** | Múltiples solicitudes fallidas consecutivas desde una misma IP sin limitador de frecuencia. | Rate Limiting con Redis (máx. 5 req/min por IP), verificación obligatoria de Google reCAPTCHA y bloqueo progresivo. | **RESUELTO** |
| **INC-004** | Riesgo de Caducidad en Lote de Chiapas | **MEDIA** | Falta de visibilidad preventiva del cajero sobre vencimiento de 42.5 kg de café orgánico. | Cron job diario invocando `/api/admin/notifications/check-alerts` con alertas SMTP y política PEPS obligatoria en POS. | **RESUELTO** |
| **INC-005** | Pérdida de Sesión POS por Intermitencia | **BAJA** | Expiración de token JWT en memoria durante fallas temporales de red local. | Renovación silenciosa (*silent refresh*) con Refresh Tokens en cookies `httpOnly` y persistencia de carrito en Pinia. | **RESUELTO** |

---

## 4. Entregables Oficiales Generados

- **Documento PDF Oficial:** [`docs/entregables/Proyecto_Equipo2_Momento3_Despliegue.pdf`](file:///d:/ernestofm/Proyecto/docs/entregables/Proyecto_Equipo2_Momento3_Despliegue.pdf)
- **Copia Alternativa en PDF:** [`docs/entregables/Proyecto_MonchisCafe_Momento3_Despliegue.pdf`](file:///d:/ernestofm/Proyecto/docs/entregables/Proyecto_MonchisCafe_Momento3_Despliegue.pdf)
- **Documento Word Estilizado (.docx):** [`docs/entregables/Proyecto_Equipo2_Momento3_Despliegue.docx`](file:///d:/ernestofm/Proyecto/docs/entregables/Proyecto_Equipo2_Momento3_Despliegue.docx)
- **Documento Maestro Markdown:** [`docs/entregables/Proyecto_Equipo2_Momento3_Despliegue.md`](file:///d:/ernestofm/Proyecto/docs/entregables/Proyecto_Equipo2_Momento3_Despliegue.md)
- **Plantilla HTML para Compilación:** [`docs/entregables/Proyecto_Equipo2_Momento3_Despliegue.html`](file:///d:/ernestofm/Proyecto/docs/entregables/Proyecto_Equipo2_Momento3_Despliegue.html)
- **Script Compilador Automatizado:** [`docs/entregables/generate_momento3_devops_deliverables.py`](file:///d:/ernestofm/Proyecto/docs/entregables/generate_momento3_devops_deliverables.py)
- **Copias para Entrega Inmediata:** `C:\Users\erfierro\Downloads\Proyecto_Equipo2_Momento3_Despliegue.pdf` y `.docx`.

