# Nivel 4: DETALLE — Foco: QUÉ
## Diagrama de Casos de Uso, Prototipos de Interfaz y Modelo de Dominio — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En la fase de detalle de la ingeniería de software, las abstracciones lógicas deben aterrizarse en artefactos técnicos concretos que sirvan como guía directa para la codificación y la construcción de la base de datos (Pressman & Maxim, 2021). Como señalan Fowler (2003) y Larman (2004), la dimensión de los datos y la estructura requiere tres representaciones complementarias: el **Diagrama de Casos de Uso UML** (que resume la interacción de los actores con las fronteras del sistema), el **Modelo de Dominio** (que captura las entidades conceptuales, sus atributos y sus multiplicidades relacionales) y los **Prototipos de Interfaz de Usuario (UI/UX)** (que materializan la ergonomía visual y la experiencia de uso conforme a estándares de usabilidad) (Nielsen, 1994).

Dentro de la Matriz de Zachman (1987), la celda **Detalle - Qué** se sitúa en la perspectiva del constructor (*Technology Model / Builder's View*). En este nivel resolvemos la pregunta técnica: *¿Cómo se estructuran los datos, las clases y las pantallas que el programador implementa físicamente en el código?* Para **Monchis Café**, este documento integra el diagrama UML global, los wireframes reales del punto de venta y el modelo entidad-relación de las tablas de la base de datos en PostgreSQL.

---

### 2. Diagrama Global de Casos de Uso UML

El siguiente diagrama formal modela la interacción entre los actores del sistema y los doce casos de uso principales:

```
                  SISTEMA WEB Y PUNTO DE VENTA — MONCHIS CAFÉ
  +-----------------------------------------------------------------------------+
  |                                                                             |
  |  +-----------------------------------------------------------------------+  |
  |  | (CU-01: Iniciar Sesión con Google reCAPTCHA)                          |  |
  |  +-----------------------------------------------------------------------+  |
  |             ^                                            ^                  |
  |             |                                            |                  |
  |             | <<include>> (Solo Admin)                   | (Anti-bot)       |
  |             v                                            v                  |
  |  +---------------------------+         +-------------------------------+    |
  |  | (CU-02: Autenticar 2FA)   |         | <<Actor Sistema>>             |    |
  |  +---------------------------+         | Google reCAPTCHA Cloud        |    |
  |                                        +-------------------------------+    |
  |                                                                             |
  |  +-----------------------------------------------------------------------+  |
  |  | (CU-03: Registrar Venta en Mostrador POS)                             |  |
  |  +-----------------------------------------------------------------------+  |
  |        |                     ^                             ^                |
  |        | <<extend>>          | <<include>>                 | Requiere       |
  |        v (Trae termo)        v                             | Stock          |
  |  +-------------------+  +-------------------------+  +--------------------+ |
  |  |(CU-05: Bono ODS12)|  |(CU-04: Cobro Multipago) |  |(CU-07: Lote PEPS)  | |
  |  +-------------------+  +-------------------------+  +--------------------+ |
  |                               |            |                                |
  |               (Tiene 7 sellos)|            | (Falta grano)                  |
  |               <<extend>>      v            v <<extend>>                     |
  |                 +--------------------+  +----------------------+            |
  |                 |(CU-06: 8vo Gratis) |  |(CU-12: Reversa Saga) |            |
  |                 +--------------------+  +----------------------+            |
  |                                                     |                       |
  |                                                     v (Auditoría DLQ)       |
  |  +-------------------------------------+  +-------------------------------+ |
  |  | (CU-08: Corte de Caja Diario Z)     |  | <<Actor Sistema>>             | |
  |  | (CU-09: Analítica y UTM Maps)       |  | Broker RabbitMQ & Servidor    | |
  |  | (CU-10: Exportar Reportes PDF/Excel)|  | SMTP de Correo Electrónico   | |
  |  | (CU-11: Alertas Sanitarias PEPS)    |  +-------------------------------+ |
  |  +-------------------------------------+                                    |
  +-----------------------------------------------------------------------------+
         ^                        ^                               ^
         |                        |                               |
    [ CAJERO ]            [ ADMINISTRADOR ]                  [ CLIENTE ]
```

---

### 3. Modelo de Dominio (Diagrama de Clases / Entidades)

El modelo de dominio representa la estructura lógica de los datos de Monchis Café, implementados mediante **Prisma ORM** sobre **PostgreSQL 15**:

```
+--------------------+        +---------------------+        +--------------------+
|       User         |        |       Order         |        |     OrderItem      |
+--------------------+        +---------------------+        +--------------------+
| id: String (UUID)  | 1    * | id: String (UUID)   | 1    * | id: String (UUID)  |
| nombre: String     |------->| numeroOrden: String |------->| ordenId: String    |
| email: String      |        | usuarioId: String   |        | productoId: String |
| passwordHash: Str  |        | cajeroId: String    |        | cantidad: Int      |
| rol: UserRole      |        | subtotal: Decimal   |        | precioUnit: Decimal|
| sellosRewards: Int |        | descuento: Decimal  |        | subtotal: Decimal  |
| puntosPesa: Int    |        | total: Decimal      |        +--------------------+
| twoFactorSecret:Str|        | metodoPago: Metodo  |                  | *
| activo: Boolean    |        | estado: EstadoOrden |                  |
+--------------------+        | termoReusable: Bool |                  | 1
                              | fechaCreacion: Date |        +--------------------+
                              +---------------------+        |      Product       |
                                      | 1                    +--------------------+
                                      |                      | id: String (UUID)  |
                                      v 1                    | nombre: String     |
                              +---------------------+        | categoria: CatTipo |
                              |     Attribution     |        | precio: Decimal    |
                              +---------------------+        | codigoBarras: Str  |
                              | id: String (UUID)   |        | stockActual: Int   |
                              | ordenId: String     |        | esOrganico: Bool   |
                              | utmSource: String   |        | activo: Boolean    |
                              | utmMedium: String   |        +--------------------+
                              | utmCampaign: String |                  | 1
                              +---------------------+                  |
                                                                       v *
+--------------------+        +---------------------+        +--------------------+
|    RevokedToken    |        |    SagaStateLog     |        |       Batch        |
+--------------------+        +---------------------+        +--------------------+
| jti: String (UUID) |        | id: String (UUID)   |        | id: String (UUID)  |
| tokenHash: String  |        | correlationId: Str  |        | productoId: String |
| expiraEn: DateTime |        | ordenId: String     |        | numeroLote: String |
| revocadoEn: DateTime|       | evento: String      |        | cooperativa: String|
+--------------------+        | estado: SagaEstado  |        | fincaOrigen: String|
                              | payload: Json       |        | fechaTueste: Date  |
                              | reintentos: Int     |        | fechaCaducidad:Date|
                              +---------------------+        | stockInicial: Int  |
                                                             | stockDisponible:Int|
                                                             +--------------------+
```

---

### 4. Prototipos de Interfaz de Usuario (UI/UX)

La interfaz gráfica sigue una filosofía de diseño cálido pastel, optimizada para terminales táctiles de mostrador con botones amplios ($\ge 48\text{ px}$) y accesibilidad WCAG 2.1 AA:

#### 4.1 Pantalla Principal de Punto de Venta (`/pos`)
```
+---------------------------------------------------------------------------------------+
|  [☕ MonchisCafé]    Inicio   Menú   Rewards   Nosotros      | 👤 Cajero: Turno [Salir]|
+---------------------------------------------------------------------------------------+
|  Punto de Venta — Mostrador                   [Lector 1D/2D: Activo] [F2: Cobrar]     |
|                                                                                       |
|  [TODOS]   [🌿 Café Orgánico]   [🥐 Repostería y Otros]      |  ORDEN ACTUAL          |
|  +--------------------+  +--------------------+            |  --------------------  |
|  | 🌿 Orgánico Stock:80|  | 🌿 Orgánico Stock:95|            |  1x Café de Olla $48.00|
|  | Café de Olla Chiapas|  | Cold Brew Sierra   |            |  1x Galleta Avena $25.00|
|  | $48.00  [+ Agregar] |  | $65.00  [+ Agregar] |            |  --------------------  |
|  +--------------------+  +--------------------+            |  Subtotal:      $73.00 |
|  +--------------------+  +--------------------+            |  [X] Trae termo (-$5)  |
|  | 🌿 Orgánico Stock:50|  | 🍞 Comercial Stock:30|          |  Descuento:     -$5.00 |
|  | Latte Lavanda Miel |  | Panqué Artesanal   |            |  TOTAL:         $68.00 |
|  | $72.00  [+ Agregar] |  | $35.00  [+ Agregar] |            |  --------------------  |
|  +--------------------+  +--------------------+            |  MÉTODO DE PAGO:       |
|                                                            |  [EFECTIVO]  [TARJETA] |
|                                                            |  [SPEI]      [REWARDS] |
|                                                            |  [  COBRAR ORDEN (F2) ]|
+---------------------------------------------------------------------------------------+
```

#### 4.2 Pantalla de Inicio de Sesión y Blindaje Web (`/login`)
```
+---------------------------------------------------------------------------------------+
|                                    [ ☕ MonchisCafé ]                                  |
|                               Bienvenido de Vuelta al Sistema                         |
|                                                                                       |
|                     Correo Electrónico:                                               |
|                     [  cajero@monchiscafe.com                               ]         |
|                                                                                       |
|                     Contraseña:                                                       |
|                     [  ••••••••••••••••                                     ]         |
|                                                                                       |
|                     +-----------------------------------------------+                 |
|                     | [X] No soy un robot       [ Google reCAPTCHA ]|                 |
|                     +-----------------------------------------------+                 |
|                                                                                       |
|                     [           INICIAR SESIÓN SEGURA               ]                 |
|                                                                                       |
|                     ¿Olvidaste tu contraseña? Contacta al Administrador.              |
+---------------------------------------------------------------------------------------+
```

---

### 5. Justificación Práctica en el Proyecto

Aterrizar el sistema en este nivel de detalle técnico es lo que permite que la fase de programación sea ágil y libre de errores conceptuales. Como señala Nielsen (1994), una interfaz de punto de venta bien prototipada reduce drásticamente los errores del usuario humano cuando atiende bajo presión en horas pico. Al combinar el diagrama UML formal, el modelo de datos relacional y las pantallas visuales, el equipo de desarrollo cuenta con el plano exacto para codificar los componentes de Vue 3 y los esquemas de Prisma sin tener que adivinar nada.

---

### 6. Referencias Bibliográficas

1. **Fowler, M. (2003).** *Patterns of Enterprise Application Architecture*. Addison-Wesley.
2. **Larman, C. (2004).** *Applying UML and Patterns: An Introduction to Object-Oriented Analysis and Design and Iterative Development* (3.ª ed.). Prentice Hall.
3. **Nielsen, J. (1994).** *Usability Engineering*. Morgan Kaufmann / Academic Press.
4. **Object Management Group. (2017).** *OMG Unified Modeling Language (OMG UML), Version 2.5.1*. OMG Document Number: formal/2017-12-05. https://www.omg.org/spec/UML/2.5.1/
5. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
6. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

