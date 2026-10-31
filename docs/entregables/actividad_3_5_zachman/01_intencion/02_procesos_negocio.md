# Nivel 1: INTENCIÓN — Foco: CÓMO
## Listado de Procesos de Negocio — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

Un proceso de negocio no es simplemente una lista de pasos en un manual de procedimientos; como lo definen Dumas et al. (2018), representa un conjunto coordinado de actividades y tareas que involucran personas, recursos y sistemas informáticos para entregar un producto o servicio de valor a un cliente. Cuando una empresa opera sin tener claros sus procesos, cada empleado trabaja a su manera, lo que genera cuellos de botella, pérdidas de materia prima y errores en el dinero que entra a caja.

Dentro de la Matriz de Zachman (1987), la celda **Intención - Cómo** se enfoca en el *Listado de Procesos de Negocio*. En este primer nivel (la visión del planificador), no nos metemos todavía a diseñar algoritmos, funciones de programación ni diagramas de base de datos detallados. Lo que se busca aquí es identificar las funciones macro que hacen posible la operación diaria de la empresa (Pressman & Maxim, 2021). Para una cafetería como Monchis Café, el "Cómo" inicial consiste en entender el ciclo completo: desde que compramos los costales de café a los productores de la sierra hasta que servimos una taza caliente en mostrador y hacemos el corte del día.

---

### 2. Catálogo de Procesos Macro de Negocio

Para garantizar una operación eficiente y trazable, el funcionamiento de **Monchis Café** se divide en seis procesos esenciales:

```
[Proceso 1: Abastecimiento]  -->  [Proceso 2: Venta y Cobro POS]  -->  [Proceso 3: Fidelización ODS 12]
            |                                    |                                    |
            v                                    v                                    v
[Proceso 4: Control PEPS]   <--  [Proceso 5: Cierre y Caja]      <--  [Proceso 6: Analítica y Seguridad]
```

---

#### PN-01: Abastecimiento y Recepción de Café Orgánico y Perecederos
* **Objetivo:** Adquirir granos de café de alta calidad directamente de cooperativas campesinas locales (Michoacán, Oaxaca, Chiapas) y repostería comercial, asegurando frescura y trazabilidad de origen.
* **Actividades Principales:**
  1. Solicitud de pedido al proveedor con especificación de tipo de grano, altura y fecha de tueste.
  2. Recepción física en cafetería con revisión sanitaria de empaques y humedad.
  3. Registro en el sistema del lote recibido: número de lote, fecha de entrada, fecha de caducidad sugerida y costo unitario.
  4. Almacenamiento en bodega aplicando la regla de etiquetado PEPS.

#### PN-02: Venta en Mostrador y Cobro Multipago (Punto de Venta)
* **Objetivo:** Atender con rapidez al cliente en el mostrador, registrar su pedido de bebidas y alimentos, y procesar el cobro bajo diversas formas de pago.
* **Actividades Principales:**
  1. Toma del pedido mediante la pantalla táctil del POS o lectura de código de barras 1D/2D del producto.
  2. Selección del método de pago elegido por el cliente:
     - *Efectivo:* Ingreso de monto recibido y entrega inmediata de cambio calculado.
     - *Tarjeta:* Cobro en terminal y verificación de autorización bancaria.
     - *Transferencia / SPEI:* Captura de la clave de rastreo bancaria para comprobación de abono.
  3. Descuento automático de stock de los insumos o productos vendidos.
  4. Impresión o envío digital del ticket de venta al cliente.

#### PN-03: Fidelización de Clientes y Bonificación Ecológica (ODS 12)
* **Objetivo:** Fomentar el retorno continuo de los clientes y reducir el desperdicio ambiental de vasos desechables (Meta 12.5 de los ODS).
* **Actividades Principales:**
  1. Identificación del cliente mediante su número telefónico, correo o código QR de "Monchis Rewards".
  2. Verificación en mostrador: si el cliente presenta su propio termo o taza reutilizable, el cajero activa la casilla de **Bono Ecológico**, aplicando \$5.00 MXN de descuento directo o sellos dobles.
  3. Asignación automática de sellos digitales (1 por bebida). Al llegar a 7 sellos, el sistema marca el 8vo café como cortesía sin costo.

#### PN-04: Control de Inventario PEPS, Alertas de Caducidad y Mermas
* **Objetivo:** Minimizar la pérdida de café y alimentos perecederos garantizando que el producto más antiguo se consuma primero (Meta 12.3 de los ODS).
* **Actividades Principales:**
  1. Ejecución automática de revisiones diarias de inventario.
  2. Emisión de alertas por correo electrónico al administrador cuando un lote de café orgánico tenga menos de 15 días de vida útil óptima.
  3. En caso de caducidad inevitable o merma física (derrame, grano en mal estado), el cajero/administrador registra la baja formal indicando la causa para auditoría.

#### PN-05: Cierre de Turno y Arqueo de Caja
* **Objetivo:** Conciliar los ingresos reales recibidos en la jornada contra las ventas registradas por el sistema informático.
* **Actividades Principales:**
  1. Bloqueo de terminal al terminar el turno del cajero.
  2. Conteo físico de efectivo y cotejo de vouchers de terminal y comprobantes de transferencias SPEI.
  3. Generación del reporte de corte de caja (*Reporte Z*) identificando si hubo sobrantes o faltantes.
  4. Validación y firma de conformidad por parte del Administrador.

#### PN-06: Gestión de Seguridad, Roles y Análisis de Tráfico
* **Objetivo:** Proteger el acceso al sistema mediante perfiles bien definidos y analizar de dónde vienen los clientes para tomar mejores decisiones comerciales.
* **Actividades Principales:**
  1. Control de accesos mediante perfiles de usuario (`Administrador`, `Cajero`, `Cliente`).
  2. Registro de parámetros de marketing digital (`utm_source`, `utm_medium`) para saber si una venta vino recomendada por Google Maps o por campañas de Instagram.
  3. Exportación de métricas semanales en PDF y Excel para la toma de decisiones.

---

### 3. Justificación Práctica en el Proyecto

Al tener los procesos de negocio claramente definidos, evitamos que el software termine haciendo cosas que no corresponden a la realidad del mostrador. Tal como señala Baca Urbina (2013), un sistema de información en un proyecto de inversión debe servir para simplificar el trabajo operativo y reducir los costos de administración. Con este catálogo de procesos, el equipo de desarrollo tiene la certeza de qué módulos programar y qué datos deben fluir entre la caja, la bodega y la gerencia.

---

### 4. Referencias Bibliográficas

1. **Baca Urbina, G. (2013).** *Evaluación de proyectos* (7.ª ed.). McGraw-Hill Interamericana.
2. **Dumas, M., La Rosa, M., Mendling, J., & Reijers, H. A. (2018).** *Fundamentals of Business Process Management* (2.ª ed.). Springer. https://doi.org/10.1007/978-3-662-56509-4
3. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
4. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

