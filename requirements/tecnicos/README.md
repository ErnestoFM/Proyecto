# Requerimientos Técnicos del Sistema

Este documento especifica los requerimientos técnicos y de infraestructura identificados a partir del análisis del documento de requerimientos funcionales, la rúbrica de evaluación y las pautas del proyecto integrador.

---

## 1. Arquitectura y Stack Tecnológico

### 1.1 Backend
- **Framework:** Node.js (con Express.js) o Python (con Django).
- **Arquitectura:** Patrón en capas (Controladores, Servicios, Repositorios/Modelos) o RESTful API.
- **Manejo de Peticiones:** Endpoints estructurados en formato JSON con middleware para tratamiento centralizado de errores y validación de esquemas (ej. Joi / Zod).

### 1.2 Frontend
- **Tecnología:** React, Vue.js o HTML5/CSS3/JavaScript modular responsivo.
- **Diseño Responsivo:** Compatibilidad con pantallas de escritorio (Administrador) y tabletas/móviles (Punto de Venta/Caja en entorno rural).
- **Consumo de APIs:** Cliente HTTP (Axios o Fetch API) con interceptores para inyección de tokens de autenticación y manejo de sesiones expiradas.

### 1.3 Base de Datos
- **Motor:** PostgreSQL o MySQL (Versión 8.0+).
- **Transacciones ACID:** Garantía de atomicidad e integridad en operaciones críticas (registro de ventas, movimientos de inventario y cierres de caja).
- **Modelado:** Diseño relacional normalizado hasta la Tercera Forma Normal (3FN), con relaciones explícitas entre Productos, Proveedores, Lotes, Ventas y Usuarios.

---

## 2. Manejo de Transacciones y Gestión de Inventario

### 2.1 Transacciones de Ventas y Caja
- **Atomicidad en Ventas:** Cada registro de venta debe descontar en tiempo real el stock en la base de datos dentro de una misma transacción (`BEGIN...COMMIT / ROLLBACK`).
- **Control de Caja:** Tablas específicas para apertura, ingresos diarios, egresos y cierre de caja con validación de saldos esperados vs. reales.

### 2.2 Trazabilidad de Productos Orgánicos
- **Entidad de Lote:** Registro obligatorio de origen (finca/proveedor regional), número de lote, fecha de compra y fecha de caducidad para café orgánico.
- **Índices de Búsqueda:** Creación de índices en la base de datos por `lote`, `fecha_caducidad` y `proveedor_id` para optimizar consultas de trazabilidad.

---

## 3. Seguridad de la Información y Control de Acceso

### 3.1 Autenticación y Autorización
- **Autenticación:** Tokens JWT (JSON Web Tokens) firmados con algoritmos seguros (`HS256` / `RS256`) o manejo de sesiones seguras (`httpOnly`, `Secure`, `SameSite=Strict`).
- **Doble Factor (2FA):** Implementación de autenticación de dos factores (TOTP / Google Authenticator o envío de código por correo) requerida obligatoriamente para el rol **Administrador**.
- **Control de Acceso basado en Roles (RBAC):** Middleware de seguridad para restringir rutas según el rol (Administrador vs. Cajero/Empleado).

### 3.2 Cifrado y Protección de Datos
- **Cifrado de Contraseñas:** Algoritmos de hashing robustos con sal (ej. `bcrypt` con costo 10+ o `argon2`).
- **Cifrado en Transito:** Conexiones cifradas mediante protocolo **HTTPS / TLS 1.3**.
- **Cifrado en Reposo:** Cifrado SSL/TLS activo en la conexión con la base de datos y protección de campos sensibles (datos de clientes y tokens).

### 3.3 Mitigación de Vulnerabilidades Web
- **Inyección SQL:** Uso obligatorio de ORM/Query Builders (Prisma, TypeORM, Sequelize, SQLAlchemy) o consultas preparadas (`parameterized queries`).
- **Cross-Site Scripting (XSS):** Sanitización estricta de datos de entrada y escape automático en las vistas.
- **Seguridad en Encabezados HTTP:** Integración de bibliotecas de seguridad HTTP (ej. `Helmet` en Express) para Content Security Policy (CSP), HSTS y Anti-Clickjacking.
- **Auditoría y Audit Logs:** Registro en base de datos o archivos de log de eventos clave (inicios de sesión, cambios de permisos, borrado de datos, transacciones de alto valor).

---

## 4. Mantenimiento y Respaldo de Base de Datos

- **Copias de Seguridad (Backups):** Script automatizado de respaldo (mediante `pg_dump` o `mysqldump`) ejecutable por tareas cron o utilidades del sistema.
- **Integridad Referencial:** Configuración estricta de claves foráneas (`FOREIGN KEY`) con reglas de restricción (`ON DELETE RESTRICT`) para prevenir pérdidas involuntarias de historial de ventas o lotes.

---

## 5. Integraciones y Servicios Externos

- **Notificaciones por Correo Electrónico:** Integración con servicio SMTP o API externa (SendGrid, Nodemailer o Resend) para alertas de caducidad, anomalías sanitarias y comprobantes digitales.
- **Exportación de Reportes:**
  - **PDF:** Utilidad backend/frontend (ej. `PDFKit`, `Puppeteer` o `jsPDF`) para la generación de reportes semanales y tickets de venta.
  - **Excel:** Generación de hojas de cálculo dinámicas (mediante `xlsx` / `exceljs`) para inventarios y reportes financieros.
- **Soporte de Lectores de Código:** Compatibilidad en el frontend para captura de entradas desde lectores USB/HID de código de barras o cámara web.

---

## 6. Entregables Académicos y de Evaluación (ExpoDIT)

De acuerdo con las indicaciones institucionales y la rúbrica del proyecto integrador, se requieren los siguientes productos técnicos y comunicativos:

1. **Documento Técnico del Proyecto:**
   - Análisis de requerimientos y estudio de factibilidad.
   - Modelo Entidad-Relación (MER) y Diagrama de Casos de Uso.
   - Especificación de arquitectura de software y diagramas de componentes.
   - Plan de pruebas (funcionales y de seguridad) y plan de mejora continua.
2. **Video Pitch (Registro EXPODIT):**
   - Video explicativo (siguiendo las directrices del enlace provisto) que exponga: Problemática rural, Genialidades de la solución, Justificación técnica, Demostración y Relación directa con los **ODS 8, 9, 12 y 16**.
3. **Presentación Ejecutiva (ExpoDIT):**
   - Diapositivas diseñadas en herramienta moderna para la exposición presencial, cubriendo: Problema, Solución, Objetivos, Ventajas, Justificación ODS, Diagrama de Software, Herramientas, Conclusiones y Demostración.
4. **Manuales del Sistema:**
   - **Manual Técnico:** Guía de instalación, configuración de variables de entorno `.env`, despliegue y endpoints de API.
   - **Manual de Usuario:** Guía ilustrada de operación del sistema para administrador y cajero.

---

## 7. Despliegue y Control de Versiones

- **Control de Versiones:** Repositorio en GitHub con estructura modular e historial de commits limpio.
- **Variables de Entorno (`.env`):** Cero credenciales harcodeadas en código fuente.
- **Despliegue (Hosting / Cloud):** Servidor local o PaaS (ej. Render, Vercel, Railway) con base de datos administrada en la nube.
