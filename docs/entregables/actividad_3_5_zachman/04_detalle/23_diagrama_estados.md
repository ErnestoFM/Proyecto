# Nivel 4: DETALLE — Foco: CUÁNDO
## Diagramas de Estados UML — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En la teoría de autómatas finitos y el modelado formal de software, un diagrama de máquina de estados describe los diferentes estados cualitativos por los que atraviesa una entidad u objeto a lo largo de su ciclo de vida como respuesta a eventos discretos, condiciones de guarda y acciones asociadas (Harel, 1987; Object Management Group [OMG], 2017). Como señalan Booch et al. (2005) y Pressman y Maxim (2021), modelar los estados es vital cuando los objetos de negocio tienen un comportamiento dinámico complejo; una orden de compra no puede cancelarse si ya fue entregada, y un lote de café no puede venderse si está marcado como caducado.

Dentro de la Matriz de Zachman (1987), la celda **Detalle - Cuándo** se ubica en la perspectiva del constructor (*State Transition & Timing Model / Builder's View*). En este nivel del código físico, formalizamos las máquinas de estados que controlan la vida útil de los dos elementos más críticos de la base de datos de **Monchis Café**: la **Orden de Venta (`Order`)** y el **Lote de Café Orgánico (`Batch`)**.

---

### 2. Diagrama de Estados 1: Ciclo de Vida de una Orden de Venta

El siguiente autómata modela los estados por los que viaja una orden desde que el cajero abre el carrito en el mostrador hasta que se entrega la bebida o se orquesta una reversa compensatoria:

```
    [*] (Inicio)
     |
     | [Cajero agrega productos al carrito]
     v
+------------------+
|      CREADA      |
+------------------+
     |
     | [Cajero presiona F2 para cobrar]
     v
+------------------+
|     EN_COBRO     | <------------------------------------+
+------------------+                                      | (Reintento)
     |                                                    |
     +---- (Fallo de red / Rechazo banco) ----------------+
     |
     | [Cobro confirmado: Efectivo / Tarjeta / SPEI]
     v
+------------------+
|      PAGADA      |
+------------------+
     |
     +---- (Stock disponible en barra / Bebida servida) ----> +-------------------+
     |                                                        |    COMPLETADA     |
     |                                                        +-------------------+
     |                                                                  |
     | (Insumo orgánico insuficiente / Evento 'inventario.insuficiente')| [Cierre turno]
     v                                                                  v
+-----------------------------+                               +-------------------+
|    CANCELADA_REEMBOLSADA    |                               |     ARCHIVADA     |
| (Compensación Saga / Reversa|                               | (Corte Diario Z)  |
+-----------------------------+                               +-------------------+
     |                                                                  |
     v                                                                  v
    [*] (Fin)                                                          [*] (Fin)
```

---

### 3. Diagrama de Estados 2: Ciclo de Vida de un Lote de Café Orgánico

Para garantizar la rotación PEPS y la frescura del café campesino (Meta 12.3 de los ODS), cada lote transita por los siguientes estados:

```
    [*] (Inicio)
     |
     | [Llega café campesino con ficha de tueste]
     v
+---------------------+
|    RECEPCIONADO     |
+---------------------+
     |
     +---- (Inspección física rechazada: grano húmedo o roto) ----> [*] (Devuelto)
     |
     | [Inspección aprobada por Administrador]
     v
+---------------------+
|   DISPONIBLE_PEPS   | <---+ (Rotación normal de ventas en mostrador)
+---------------------+     |
     |                      |
     | [Evaluación diaria Cron: ¿Fecha caducidad < 15 días?]
     v
+---------------------+
| EN_ALERTA_PREVENTIVA|
| (Alerta SMTP enviada|
+---------------------+
     |
     +---- (Se consume la totalidad del grano en ventas) -------> +-----------------+
     |                                                            |     AGOTADO     |
     |                                                            +-----------------+
     |                                                                     |
     | [Llega fecha límite sin venderse: Retiro sanitario]                 v
     v                                                                    [*] (Fin)
+---------------------+
|  MERMADO_CADUCADO   |
| (Baja registrada)   |
+---------------------+
     |
     v
    [*] (Fin)
```

---

### 4. Tabla Formal de Transiciones de Estado de la Orden

La siguiente tabla resume los eventos, las condiciones de guarda `[guard]` y las acciones ejecutadas durante cada cambio de estado de la orden:

| Estado Origen | Evento Disparador | Condición de Guarda `[guard]` | Acción Ejecutada en el Sistema | Estado Destino |
| :--- | :--- | :--- | :--- | :--- |
| **`[*]` (Nulo)** | `abrirNuevaOrden()` | Cajero autenticado con turno abierto. | Instancia objeto `Order` en memoria con subtotal cero. | **`CREADA`** |
| **`CREADA`** | `iniciarCobro()` | Carrito tiene al menos un producto válido. | Congela precios del catálogo y despliega opciones de pago. | **`EN_COBRO`** |
| **`EN_COBRO`** | `confirmarPago()` | Monto efectivo exacto o voucher autorizado. | Guarda orden atómica en PostgreSQL (`prisma.$transaction`).| **`PAGADA`** |
| **`PAGADA`** | `entregarBebida()` | Insumo verificado físicamente en barra. | Decrementa stock PEPS y asigna sellos Rewards. | **`COMPLETADA`** |
| **`PAGADA`** | `eventoFaltaGrano()`| Grano de café agotado o contaminado en barra. | Orquesta reversa Saga, emite reembolso y alerta gerencia. | **`CANCELADA_REEMBOLSADA`** |
| **`COMPLETADA`**| `ejecutarCorteZ()` | Fin de jornada laboral del cajero. | Consolida montos en reporte Z y cierra el turno. | **`ARCHIVADA`** |

---

### 5. Justificación Práctica en el Proyecto

Modelar las máquinas de estados en la fase de detalle es lo que impide que el software caiga en inconsistencias lógicas graves. Como demuestra Harel (1987), sin una máquina de estados explícita, el código se llena de condicionales booleanos dispersos (`if/else`) propensos a bugs donde una orden puede cobrarse dos veces o donde un producto ya reembolsado aparece todavía como vendido. En Monchis Café, garantizar que una orden solo pase a `PAGADA` si hay una confirmación bancaria o de efectivo, y que transite automáticamente a `CANCELADA_REEMBOLSADA` ante cualquier falla de insumos, es lo que blinda la coherencia operativa del negocio.

---

### 6. Referencias Bibliográficas

1. **Booch, G., Rumbaugh, J., & Jacobson, I. (2005).** *The Unified Modeling Language User Guide* (2.ª ed.). Addison-Wesley.
2. **Harel, D. (1987).** Statecharts: A visual formalism for complex systems. *Science of Computer Programming*, 8(3), 231–274. https://doi.org/10.1016/0167-6423(87)90035-9
3. **Object Management Group. (2017).** *OMG Unified Modeling Language (OMG UML), Version 2.5.1*. OMG Document Number: formal/2017-12-05. https://www.omg.org/spec/UML/2.5.1/
4. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
5. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

