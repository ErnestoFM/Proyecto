# Auditoría de Pendientes, Deuda Técnica y Buenas Prácticas

#pendientes #deuda_tecnica #seguridad #auditoria #prisma #rabbitmq #monchis_cafe

Nota contextualizada en el Vault de Obsidian que resume el estado de completitud técnica del proyecto frente a los requerimientos funcionales y técnicos.

---

## 📌 Resumen de Estado del Sistema

| Dimensión | Estado Actual | Observaciones |
|---|:---:|---|
| **Frontend UI / UX** | ✅ 90% | Vistas públicas, POS y Admin maquetados con diseño pastel y responsive. Faltan exportes y lectura de periféricos. |
| **Lógica de Negocio (TDD)** | ✅ 95% | Reglas de lealtad, puntos, sellos, bonos eco y cobros mixtos con 55 tests unitarios aprobados. |
| **Persistencia (PostgreSQL / Prisma)** | ⚠️ 20% | Esquema Prisma modelado al 100%, pero no conectado en vivo. Las órdenes, lotes y productos operan en memoria (arrays). |
| **Mensajería (RabbitMQ Saga / DLQ)** | ⚠️ 35% | Cliente y eventos estructurados, pero sin worker consumidor activo para procesar las reversas. Inconsistencia de nombre de Exchange. |
| **Seguridad de la Información** | ⚠️ 60% | Hashing bcrypt y tokens JWT implementados, pero con secretos de fallback quemados en código fuente y cálculo de precios confiado al cliente en POS. |
| **Integraciones Externas** | ❌ 10% | Sin servicio SMTP de correo, sin 2FA TOTP para admin y reCAPTCHA en modo permisivo si no hay credenciales en `.env`. |

---

## 🔍 Detalle de Hallazgos y Tareas por Resolver

### 1. Seguridad Crítica
- **Secretos JWT en código:** `apps/api/src/lib/jwt.ts` tiene cadenas por defecto para `JWT_ACCESS_SECRET`. Deben eliminarse y forzar lectura de `.env`.
- **Manipulación de precios en POS:** `apps/api/src/app/api/pos/orders/route.ts` confía en `item.precioUnitario` enviado desde el cliente en lugar de verificarlo contra la base de datos.
- **Blacklist de tokens revocados:** `RevokedToken` no se consulta activamente en el middleware al validar `verifyAccessToken`.

### 2. Persistencia y Eliminación de Mocks
- **Órdenes no guardadas:** Al cobrar en `/pos`, el backend no ejecuta `prisma.order.create()`. La venta no descuenta stock ni actualiza puntos del usuario en PostgreSQL.
- **Catálogo de productos estático:** `apps/api/src/app/api/products/route.ts` usa `CATALOGO_PRODUCTOS` fijo en memoria. Debe migrar a `prisma.product.findMany()`.
- **Lotes en memoria:** `apps/api/src/app/api/inventory/batches/route.ts` usa un array `LOTES_MEMORIA`. Al reiniciar el proceso se pierde el inventario.
- **Analítica simulada:** `apps/api/src/app/api/admin/analytics/route.ts` calcula sobre datos fijos en lugar de consultar `Order` y `Attribution`.

### 3. Módulos Faltantes según Requerimientos
- **2FA (Doble Factor):** Exigido para el Administrador; no existen rutas ni vistas para generar/validar TOTP con Google Authenticator.
- **Worker Consumidor de RabbitMQ:** El Patrón Saga requiere un proceso en background escuchando la cola de eventos para ejecutar transacciones compensatorias.
- **Notificaciones SMTP:** Requeridas para alertas de caducidad en lotes y eventos caídos en DLQ.
- **Exportación de Reportes:** Requerida en Excel y PDF en el panel administrativo.

### 4. Corrección de Scripts y Configuración
- En `package.json` raíz, `pnpm test` falla porque `@monchis/database` y `@monchis/messaging` no tienen archivos de test. Agregar `--passWithNoTests` o tests unitarios a dichos paquetes.
- Unificar nombre del exchange de RabbitMQ (`cafeteria.events` en el cliente vs. `monchis.events` en la ruta de órdenes).

---

## 🔗 Referencias Cruzadas (Wikilinks)
- [[Index|Índice Principal del Vault]]
- [[Arquitectura/Index|Arquitectura y Patrón Saga]]
- [[Modulos/Autenticacion_Stateless_reCAPTCHA|Módulo de Autenticación Stateless]]
- [[Contexto/Index|Contexto del Negocio]]
- Archivo raíz: `PENDIENTES.md`
