# Nivel 1: INTENCIÓN — Foco: CUÁNDO
## Listado de Eventos de Negocio — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En el análisis de requerimientos y la ingeniería de software moderna, un evento representa un suceso significativo en un momento específico en el tiempo que altera el estado del negocio o exige una respuesta inmediata por parte del sistema (Fowler, 2002). Nada en un negocio ocurre al azar; los procesos no se ejecutan continuamente sin motivo, sino que son "despertados" por estímulos internos o externos, como la llegada de un cliente al mostrador, la recepción de un pedido o el cambio de horario al finalizar la jornada (Pressman & Maxim, 2021).

Dentro de la Matriz de Zachman (1987), la celda **Intención - Cuándo** captura la dimensión temporal del negocio desde el punto de vista del planificador. En esta etapa contextual no diseñamos cronogramas detallados de Gantt con fechas de entrega de software ni diagramas de secuencia técnica con milisegundos de latencia; lo que se formaliza es el *Listado de Eventos de Negocio* que disparan las operaciones cotidianas de la cafetería (ISO/IEC/IEEE 29148, 2018). Si el equipo de desarrollo no entiende con exactitud cuándo y por qué ocurre cada acción en la cafetería, el sistema terminará siendo rígido y desincronizado con el ritmo real del mostrador.

---

### 2. Catálogo de Eventos de Negocio en Monchis Café

A continuación se detallan los diez eventos clave que estructuran la dinámica temporal de la cafetería, clasificados por su tipo de disparador (*Trigger*):

```
+---------------------------------------------------------------------------------------+
|                               TIPOS DE DISPARADORES                                   |
+---------------------------------------------------------------------------------------+
| * Temporales (Cron / Horario):  Apertura de turno, cierre de caja, alerta diaria PEPS.|
| * Transaccionales (Mostrador):  Cobro en POS, lectura de código de barras, pago SPEI. |
| * Excepcionales (Seguridad):    Ruptura de stock en preparación, intentos de intrusión.|
| * Ecológicos / Fidelización:    Presentación de termo, acumulación de 7 sellos.       |
+---------------------------------------------------------------------------------------+
```

---

| Código | Evento de Negocio | Tipo de Disparador | Condición de Activación | Acción / Respuesta del Sistema |
| :--- | :--- | :--- | :--- | :--- |
| **EVT-01** | **Apertura de Turno** | Temporal / Operativo | Inicio de jornada laboral del cajero (07:00 AM). | Registro del fondo fijo de caja inicial y desbloqueo de la terminal POS para ventas. |
| **EVT-02** | **Llegada de Café Campesino** | Externo (Proveedor) | Entrega física de costales o bolsas de café en cafetería. | Captura del número de lote, finca de origen, altitud, costo y fecha de tostado en el sistema. |
| **EVT-03** | **Solicitud de Pedido** | Operativo (Cliente) | El cliente se presenta en mostrador y solicita bebidas o alimentos. | Apertura de una orden activa en el POS y reserva temporal de existencias en mostrador. |
| **EVT-04** | **Presentación de Termo Reusable** | Ecológico (ODS 12) | El cliente muestra su recipiente o termo personal antes del cobro. | El cajero activa la casilla "Bono Ecológico", aplicando -$5.00 MXN o sellos dobles. |
| **EVT-05** | **Confirmación de Cobro** | Financiero / Transaccional | El cajero valida el ingreso de efectivo, voucher de tarjeta o clave SPEI. | Emisión de ticket fiscal/simplificado, descuento formal de stock e incremento de venta en caja. |
| **EVT-06** | **Ruptura de Insumo en Preparación** | Excepcional / Falla | Se agota inesperadamente el grano del lote orgánico mientras se preparaba la bebida. | Cancelación de orden, emisión automática de reembolso compensatorio y notificación a gerencia. |
| **EVT-07** | **Detección de Lote Próximo a Vencer** | Temporal (Automático) | Evaluación diaria a las 06:00 AM sobre lotes con menos de 15 días de vida útil óptima. | Envío de correo electrónico SMTP al Administrador con aviso de remate prioritario PEPS. |
| **EVT-08** | **Acumulación del 7mo Sello** | Fidelización | El cliente registra su séptima compra de café preparado en "Monchis Rewards". | El sistema marca automáticamente la 8va bebida como "Cortesía sin costo ($0.00)". |
| **EVT-09** | **Cierre de Turno y Arqueo** | Temporal / Operativo | Fin de jornada del cajero (15:00 o 22:00 horas). | Bloqueo de la terminal POS, solicitud del desglose de efectivo y generación del corte diario Z. |
| **EVT-10** | **Ráfaga de Accesos Fallidos** | Seguridad / Auditoría | 5 intentos erróneos consecutivos de inicio de sesión desde la misma dirección IP. | Bloqueo temporal del formulario por 15 minutos, registro en log y activación de alerta de seguridad. |

---

### 3. Ciclo Temporal de una Venta en Mostrador

Para ilustrar cómo se encadenan estos eventos en el tiempo, el ciclo estándar de una compra se describe como sigue:

```
[EVT-01: Caja Abierta]
         |
         v
[EVT-03: Cliente pide Latte Chiapas]
         |
         +-----> (¿Trae Termo?) ---> [EVT-04: Aplica Bono Ecológico -$5.00]
         |
         v
[EVT-05: Cliente Paga con Tarjeta]
         |
         v
[EVT-08: Acumula Sello #7] ---> [Bebida #8 Gratis Activada]
         |
         v
[Actualización de Inventario PEPS en Base de Datos]
```

---

### 4. Justificación Práctica en el Proyecto

Identificar los eventos de negocio desde el nivel de Intención es lo que permite que el software se programe pensando en la reactividad. Como señala Sommerville (2011), los sistemas que dan soporte a operaciones comerciales críticas deben ser dirigidos por eventos para no perder transacciones. Si un cajero está cobrando y de pronto se derrama el café o no hay grano, el sistema debe saber responder al evento de cancelación sin dejar la caja descuadrada. Del mismo modo, automatizar la revisión diaria de caducidad (EVT-07) garantiza que ninguna bolsa de café de especialidad se quede olvidada en la bodega, protegiendo la inversión del negocio y la frescura para el cliente.

---

### 5. Referencias Bibliográficas

1. **Fowler, M. (2002).** *Patterns of Enterprise Application Architecture*. Addison-Wesley.
2. **ISO/IEC/IEEE. (2018).** *ISO/IEC/IEEE 29148:2018 Systems and software engineering — Life cycle processes — Requirements engineering*. IEEE.
3. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
4. **Sommerville, I. (2011).** *Ingeniería del software* (9.ª ed.). Addison-Wesley / Pearson Educación.
5. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

