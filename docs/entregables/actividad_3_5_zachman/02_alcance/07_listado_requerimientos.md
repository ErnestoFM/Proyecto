# Nivel 2: ALCANCE — Foco: QUÉ
## Listado de Requerimientos del Sistema — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En la ingeniería de requerimientos, un requerimiento representa una condición, capacidad o restricción que el sistema informático debe cumplir para resolver un problema operativo o satisfacer un objetivo del negocio (ISO/IEC/IEEE 29148, 2018). Como explican Sommerville (2011) y Pressman y Maxim (2021), no se puede empezar a escribir código o armar bases de datos si antes no se tienen redactados los requerimientos de manera comprensible para el cliente y suficientemente rigurosa para los programadores. Si un requerimiento está incompleto o redactado con ambigüedades, el costo de corregir ese error en etapas avanzadas de producción llega a multiplicarse hasta por cien (Boehm, 1981).

Dentro de la Matriz de Zachman (1987), la celda **Alcance - Qué** corresponde al modelo de negocio (*Business Model / Owner's View*). En este nivel, el dueño del negocio y los analistas traducen las características generales de la cafetería en un catálogo estructurado de **Requerimientos Funcionales (RF)**. Cada requerimiento debe tener un identificador unívoco, un verbo en infinitivo que exprese la acción, el actor que lo utiliza y el criterio de éxito que permite verificar si realmente se cumplió (Wiegers & Beatty, 2013).

---

### 2. Catálogo de Requerimientos Funcionales (RF)

A continuación se listan los 15 Requerimientos Funcionales principales que rigen la operación de **Monchis Café**, clasificados por módulo operativo:

```
+---------------------------------------------------------------------------------------+
|                       REQUERIMIENTOS FUNCIONALES (RF-01 A RF-15)                      |
+---------------------------------------------------------------------------------------+
| Módulo A: Catálogo y Trazabilidad    | RF-01 (Catálogo)      | RF-02 (Lotes Orgánicos)|
| Módulo B: Punto de Venta (POS)       | RF-03 (Venta Mostrador)| RF-04 (Multipago)      |
| Módulo C: Sostenibilidad y Lealtad   | RF-05 (Bono Ecológico) | RF-06 (Monchis Rewards)|
| Módulo D: Inventarios y Alertas      | RF-07 (Rotación PEPS)  | RF-08 (Alertas SMTP)   |
| Módulo E: Operación y Arqueo de Caja | RF-09 (Corte Diario Z) | RF-15 (Atajos y Escáner)|
| Módulo F: Seguridad e Identidad      | RF-10 (JWT / reCAPTCHA)| RF-11 (2FA Administrador)|
| Módulo G: Analítica y Resiliencia    | RF-12 (Atribución UTM) | RF-13 (Reportes Excel) |
|                                      | RF-14 (Reversas Saga)  |                        |
+---------------------------------------------------------------------------------------+
```

---

| Identificador | Nombre del Requerimiento | Actor Principal | Descripción Detallada | Criterio de Verificación / Salida |
| :--- | :--- | :--- | :--- | :--- |
| **RF-01** | **Gestión de Catálogo Segmentado** | Administrador | El sistema debe permitir dar de alta, modificar y desactivar productos clasificándolos en *Línea Orgánica* (café de especialidad) o *Línea Comercial* (repostería/bebidas frías). | Producto visible en el POS con foto, precio unitario oficial y badge correspondiente. |
| **RF-02** | **Trazabilidad de Lotes de Café** | Administrador | El sistema debe registrar cada lote de café recibido asociando cooperativa campesina, finca de origen, altitud (msnm), fecha de tueste y caducidad sugerida. | Ficha de lote almacenada en base de datos con código único de trazabilidad. |
| **RF-03** | **Registro de Venta en Mostrador** | Cajero | El sistema debe proporcionar una interfaz táctil rápida para seleccionar productos, especificar cantidades y calcular subtotal, IVA y total de forma automática. | Carrito de venta actualizado con tiempo de respuesta inferior a 100 ms. |
| **RF-04** | **Cobro Multipago en Caja** | Cajero / Cliente | El sistema debe admitir cobros en Efectivo (calculando el cambio exacto), Tarjeta bancaria (con captura de voucher) y Transferencia SPEI (con clave de rastreo). | Transacción registrada en estado `PAGADA` y emisión de ticket digital/impreso. |
| **RF-05** | **Aplicación de Bonificación Ecológica** | Cajero / Cliente | Al activar la casilla de "Bono Ecológico", el sistema debe aplicar un descuento directo de \$5.00 MXN o sellos dobles si el cliente presenta su propio termo o taza. | Descuento reflejado en el ticket y cálculo de métrica de ahorro de vasos (ODS 12). |
| **RF-06** | **Gestión de Monchis Rewards** | Cliente / Cajero | El sistema debe acumular 1 sello digital por cada café preparado; al llegar a 7 sellos, debe marcar automáticamente el 8vo café como cortesía ($0.00). | Contador de sellos actualizado en la cuenta del cliente y alerta de café gratis. |
| **RF-07** | **Control de Inventario PEPS** | Sistema / Cajero | Cada venta de café en grano o bebidas preparadas debe descontar automáticamente las existencias del lote con fecha de entrada más antigua en bodega. | Stock decrementado en base de datos sin permitir existencias negativas. |
| **RF-08** | **Motor de Alertas Sanitarias SMTP**| Sistema / Admin | El sistema debe evaluar diariamente las fechas de caducidad y emitir correos de alerta preventiva al administrador si un lote tiene menos de 15 días de vida óptima. | Correo electrónico recibido en la bandeja del administrador con detalle del lote. |
| **RF-09** | **Corte de Turno y Arqueo de Caja** | Cajero / Admin | Al terminar el turno, el sistema debe solicitar al cajero el conteo de efectivo físico y compararlo con el total registrado, generando el reporte Z de corte. | Reporte Z generado con desglose de ventas por método de pago y cálculo de sobrante/faltante. |
| **RF-10** | **Autenticación Stateless y reCAPTCHA**| Todos los Roles | El acceso al sistema debe verificarse mediante tokens JWT en memoria, cookies seguras `httpOnly` y validación obligatoria de Google reCAPTCHA v2/v3 en login. | Acceso permitido solo con credenciales válidas y bloqueo inmediato a bots o tokens dummy. |
| **RF-11** | **Doble Factor de Autenticación (2FA)**| Administrador | El sistema debe exigir un código TOTP de 6 dígitos (Google Authenticator) para confirmar el inicio de sesión de cuentas con perfil de Administrador. | Sesión autorizada únicamente tras validar el código temporal de 30 segundos. |
| **RF-12** | **Atribución de Tráfico y Campañas** | Administrador | El sistema debe capturar parámetros `utm_source` y `utm_campaign` en registros y compras web para medir si los clientes provienen de Google Maps o Instagram. | Métricas de conversión visibles en el panel administrativo clasificadas por canal. |
| **RF-13** | **Exportación de Reportes Financieros**| Administrador | El sistema debe permitir descargar los resúmenes de ventas, corte de caja y mermas en formatos CSV (compatible con Excel) y PDF maquetado para impresión. | Archivo `.xlsx` o `.pdf` descargado con datos consolidados de la cafetería. |
| **RF-14** | **Transacciones Compensatorias (Saga)**| Sistema | Si se cobra una orden pero el grano del lote orgánico se agota durante la preparación, el sistema debe orquestar automáticamente la reversa y reembolso. | Orden marcada como `CANCELADA_REEMBOLSADA` y notificación automática a gerencia. |
| **RF-15** | **Atajos de Mostrador y Lector Óptico**| Cajero | El sistema debe escuchar eventos globales de teclado: `F2` para cobrar directo, `Esc` para vaciar la orden y lectura automática de códigos de barras (7501001-7501005). | Producto agregado al carrito al instante al pasar el lector de código de barras. |

---

### 3. Justificación Práctica en el Proyecto

Contar con este catálogo detallado de requerimientos funcionales nos evita lo que en el ambiente de desarrollo llamamos "construir a ciegas". Como bien advierten Pressman y Maxim (2021), cuando un programador no tiene una especificación concreta con entradas, procesos y salidas medibles, termina inventando el flujo de la aplicación según su criterio personal, lo que después choca de frente con la realidad del cajero o con las normas fiscales del negocio. Con esta lista aprobada por el dueño, el equipo de desarrollo puede asociar cada funcionalidad con pruebas unitarias automáticas (TDD) y verificar que el software haga exactamente lo que Monchis Café necesita para operar.

---

### 4. Referencias Bibliográficas

1. **Boehm, B. W. (1981).** *Software Engineering Economics*. Prentice-Hall.
2. **ISO/IEC/IEEE. (2018).** *ISO/IEC/IEEE 29148:2018 Systems and software engineering — Life cycle processes — Requirements engineering*. IEEE.
3. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
4. **Sommerville, I. (2011).** *Ingeniería del software* (9.ª ed.). Addison-Wesley / Pearson Educación.
5. **Wiegers, K. E., & Beatty, J. (2013).** *Software Requirements* (3.ª ed.). Microsoft Press.
6. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

