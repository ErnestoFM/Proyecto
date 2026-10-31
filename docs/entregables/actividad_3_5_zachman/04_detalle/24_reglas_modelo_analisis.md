# Nivel 4: DETALLE — Foco: POR QUÉ
## Reglas de Negocio en el Modelo de Análisis y Código — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En el desarrollo de software profesional y el diseño guiado por el dominio (*Domain-Driven Design* - DDD), las reglas de negocio no pueden quedarse como conceptos abstractos flotando en un documento de análisis; deben materializarse formalmente en invariantes del dominio, validadores de esquemas, restricciones de base de datos relacionales (*constraints*) y middlewares de control (Evans, 2003). Como explica Martin Fowler (2002), cuando las reglas de negocio se dispersan o se duplican sin orden en la interfaz gráfica, el sistema se vuelve frágil y vulnerable; cualquier atacante que burle el navegador puede enviar peticiones manipuladas directamente a la API si el backend no valida las reglas con puño de hierro.

Dentro de la Matriz de Zachman (1987), la celda **Detalle - Por qué** cierra la arquitectura en la perspectiva del constructor (*Rule Enforcement & Implementation Model / Builder's View*). En este nivel técnico se detalla el **mapeo exacto** de cómo cada una de las ocho reglas de negocio de **Monchis Café** está implementada en el código fuente TypeScript, en los esquemas de **Prisma ORM / PostgreSQL**, en las colas de **RabbitMQ** y en las pruebas unitarias automatizadas (**Vitest**) que verifican su cumplimiento en cada despliegue.

---

### 2. Matriz de Trazabilidad: Regla de Negocio ➔ Código y Base de Datos

La siguiente tabla resume cómo se implementa y se prueba técnicamente cada regla en el monorepo:

| Regla de Negocio | Entidad / Módulo Responsable | Implementación Técnica y Restricción | Prueba Automática Asociada (TDD) |
| :--- | :--- | :--- | :--- |
| **RN-01: Precios de Servidor** | `apps/api/src/app/api/pos/orders/route.ts` | El backend extrae los `productoId` y consulta `prisma.product.findUnique()`. Sobreescribe cualquier precio enviado en el JSON del cliente. | `tests/business.test.ts` (Prueba de rechazo de precios manipulados). |
| **RN-02: Rotación PEPS** | `packages/database/prisma/schema.prisma` | Consulta ordenada: `prisma.batch.findFirst({ where: { stockDisponible: { gt: 0 } }, orderBy: { fechaIngreso: 'asc' } })`. | `tests/business.test.ts` (Prueba de decremento sobre el lote más antiguo). |
| **RN-03: Bono Ecológico** | `apps/api/src/app/api/pos/orders/route.ts` | Si `termoReusable === true`, aplica deducción estricta de `$5.00` en `descuento` y registra la métrica en la tabla `Order`. | `tests/business.test.ts` (Prueba de cálculo reactivo de bono ecológico). |
| **RN-04: Monchis Rewards** | `apps/api/src/app/api/pos/orders/route.ts` | Evaluación atómica: `const gratis = user.sellosRewards % 8 === 7`. Bonifica bebida a `$0.00` y actualiza contador en `User`. | `tests/business.test.ts` (Prueba de otorgamiento de 8vo café de cortesía). |
| **RN-05: 2FA Administrador**| `apps/api/src/lib/totp.ts` | Servicio criptográfico RFC 6238 que valida código de 6 dígitos con ventana de $\pm 30\text{ s}$ mediante `otplib`. | `tests/totp.test.ts` (11 pruebas de generación, verificación y revocación). |
| **RN-06: Reversa Saga** | `packages/messaging/src/sagaWorker.ts` | Consumer AMQP que escucha `inventario.stock.insuficiente`. Ejecuta reversa a `CANCELADA_REEMBOLSADA` y DLQ tras 3 fallos. | `tests/admin.test.ts` (Prueba de auditoría de eventos en `orders.dlq`). |
| **RN-07: Rate Limiting** | `apps/api/src/lib/recaptcha.ts` | Verificación en backend contra API de Google y contador en memoria por IP. Bloqueo HTTP 429 tras 5 intentos erróneos. | `tests/auth.test.ts` (Prueba de bloqueo anti-fuerza bruta y anti-bypass). |
| **RN-08: Arqueo Ciego** | `apps/api/src/app/api/admin/cash-cut/route.ts` | El endpoint exige `montoDeclarado`. Solo tras registrar el valor físico en BD, calcula y retorna `diferencia = declarado - teorico`. | `tests/admin.test.ts` (Prueba de cálculo de sobrante/faltante en corte Z). |

---

### 3. Evidencia de Implementación en Código Fuente

A continuación se presentan fragmentos reales del código que demuestran la aplicación rigurosa de las reglas en la arquitectura:

#### 3.1 Blindaje de Precios Oficiales (RN-01):
```typescript
// Fragmento de apps/api/src/app/api/pos/orders/route.ts
// Blindaje contra manipulación de precios desde el cliente
const productIds = body.items.map((i: any) => i.productoId);
const dbProducts = await prisma.product.findMany({
  where: { id: { in: productIds }, activo: true }
});

let subtotalCalculado = 0;
const orderItemsData = body.items.map((item: any) => {
  const prod = dbProducts.find((p) => p.id === item.productoId);
  if (!prod) throw new Error(`Producto no encontrado o inactivo: ${item.productoId}`);
  
  // PRECIO OFICIAL OBLIGATORIO DEL SERVIDOR (Cero confianza en el cliente)
  const precioUnitarioOficial = Number(prod.precio);
  const subtotalItem = precioUnitarioOficial * item.cantidad;
  subtotalCalculado += subtotalItem;

  return {
    productoId: prod.id,
    cantidad: item.cantidad,
    precioUnitario: precioUnitarioOficial,
    subtotal: subtotalItem
  };
});
```

#### 3.2 Rotación de Inventarios PEPS en Base de Datos (RN-02):
```prisma
// Fragmento de packages/database/prisma/schema.prisma
model Batch {
  id              String      @id @default(uuid())
  productoId      String
  numeroLote      String      @unique
  cooperativa     String
  fincaOrigen     String
  fechaIngreso    DateTime    @default(now())
  fechaCaducidad  DateTime
  stockDisponible Int
  producto        Product     @relation(fields: [productoId], references: [id])

  @@index([productoId, fechaIngreso]) // Optimización para ordenamiento PEPS
}
```

#### 3.3 Validación de Tokens Anti-Bot sin Bypass en Producción (RN-07):
```typescript
// Fragmento de apps/api/src/lib/recaptcha.ts
export async function verifyGoogleRecaptcha(token: string): Promise<boolean> {
  if (!token || token.trim() === '') return false;

  const isProduction = process.env.NODE_ENV === 'production';
  const isTestToken = token === 'test-valid-recaptcha-token';

  // En producción se rechaza tajantemente cualquier token dummy de prueba
  if (isProduction && isTestToken) {
    console.warn('⚠️ [reCAPTCHA] Intento de usar token dummy en ambiente de producción.');
    return false;
  }

  const secretKey = process.env.RECAPTCHA_SECRET_KEY;
  if (!secretKey) {
    if (isProduction) throw new Error('[Seguridad Crítica] RECAPTCHA_SECRET_KEY no configurada.');
    return false;
  }
  // Validación contra Google API
  const res = await fetch(`https://www.google.com/recaptcha/api/siteverify?secret=${secretKey}&response=${token}`, { method: 'POST' });
  const data = await res.json();
  return data.success === true;
}
```

---

### 4. Justificación Práctica en el Proyecto

Asegurar que cada regla de negocio tenga un reflejo directo en la base de datos y en las pruebas unitarias (TDD) es la máxima garantía de calidad de software. Como destaca Evans (2003), cuando el código habla el mismo lenguaje que las reglas del negocio, el software se vuelve predecible, auditable y resistente a errores. En Monchis Café, contar con 77 pruebas unitarias automáticas pasando en verde en cada commit confirma que, sin importar qué cambios se hagan en la interfaz o qué barista opere el punto de venta, las reglas de precio, rotación PEPS, bono ecológico y seguridad de la caja se cumplirán siempre de forma implacable.

---

### 5. Referencias Bibliográficas

1. **Evans, E. (2003).** *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley Professional.
2. **Fowler, M. (2002).** *Patterns of Enterprise Application Architecture*. Addison-Wesley.
3. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
4. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

