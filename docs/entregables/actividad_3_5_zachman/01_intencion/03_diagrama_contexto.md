# Nivel 1: INTENCIÓN — Foco: DÓNDE
## Diagrama de Contexto — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En el análisis estructurado de sistemas, el diagrama de contexto representa el nivel más alto de abstracción en el modelado de datos y flujos de información (Yourdon, 1989). Conocido formalmente como el *Diagrama de Flujo de Datos de Nivel 0* (DFD Nivel 0), su propósito fundamental es delimitar las fronteras del sistema, tratándolo como una sola burbuja o "caja negra" que interactúa únicamente con el mundo exterior a través de entidades externas y flujos de entrada y salida (Pressman & Maxim, 2021).

Dentro de la Matriz de Zachman (1987), la celda **Intención - Dónde** aborda la dimensión geográfica y de ubicación desde el punto de vista del planificador. No se trata en este momento de especificar direcciones IP, configuraciones de Nginx o puertos de red en servidores cloud; lo que el arquitecto debe definir en este nivel es la relación física y lógica del negocio: *¿Dónde interactúa el sistema con los actores humanos y con los servicios externos que complementan la operación de la cafetería?* (Sommerville, 2011).

---

### 2. Diagrama de Contexto del Sistema

A continuación se presenta la interacción entre el núcleo de **Monchis Café** y los actores y servicios que forman su entorno operativo:

```
                                  +------------------------------------+
                                  |     Cooperativas Campesinas        |
                                  |     y Proveedores de Café          |
                                  +------------------------------------+
                                             |              ^
                           Entrega de Lotes  |              | Orden de
                           y Fichas Técnicas |              | Compra
                                             v              |
+---------------------+           +------------------------------------+           +----------------------+
|       CLIENTE       | --------> |                                    | --------> |     ADMINISTRADOR    |
| (Web / Mostrador)   | Solicitud |                                    | Métricas  |    (Dueño / Gerente) |
|                     | de Pedido |                                    | de Venta  +----------------------+
|                     | <-------- |                                    | <--------
|                     | Ticket /  |      SISTEMA INFORMÁTICO           | Parámetros Catálogo,
|                     | Sellos    |                                    | Lotes y Cortes de Caja
+---------------------+           |          MONCHIS CAFÉ              |
                                  |                                    |
+---------------------+           |                                    | --------> +----------------------+
|       CAJERO        | --------> |                                    | Alertas   |    Servicio SMTP     |
| (Terminal POS)      | Ventas y  |                                    | Sanitarias|  (Correo Electrónico)|
|                     | Arqueo    |                                    | y DLQ     +----------------------+
|                     | <-------- |                                    |
|                     | Confirm.  |                                    | <-------> +----------------------+
+---------------------+           +------------------------------------+ Peticiones|    Servicios Web     |
                                             |              ^            HTTP/Auth |   Externos de Google |
                             Transacciones   |              | Autoriz.             | (reCAPTCHA / Maps)   |
                             Tarjeta / SPEI  v              | y Claves             +----------------------+
                                  +------------------------------------+
                                  |   Pasarela Bancaria y SPEI (SAT)   |
                                  +------------------------------------+
```

---

### 3. Descripción de Entidades Externas y Flujos

Para comprender con exactitud qué información entra y sale del sistema, se describen los límites de cada entidad:

| Entidad Externa | Tipo | Flujo de Entrada (Hacia el Sistema) | Flujo de Salida (Desde el Sistema) |
| :--- | :--- | :--- | :--- |
| **Cliente** | Humano / Usuario | Selección de café/alimentos, solicitud de registro a Rewards, presentación de termo reusable y pago. | Ticket digital de compra, estado de sellos acumulados y café de cortesía. |
| **Cajero** | Humano / Operador | Apertura de turno, escaneo de códigos de barra, cobro en mostrador y declaración de efectivo para arqueo. | Notificación de cambio a devolver, estatus de orden y reporte de corte diario. |
| **Administrador** | Humano / Gerente | Registro de nuevos lotes de café, actualización de precios, gestión de promociones y revisión de caja. | Tablero de analítica en tiempo real, reportes ejecutivos en PDF/Excel y auditoría de eventos. |
| **Cooperativas y Proveedores** | Externo / Negocio | Fichas técnicas de café (origen, altitud, tipo de tostado, fecha de tueste y caducidad). | Órdenes de compra oficiales y confirmación de pago por transferencias. |
| **Pasarela Bancaria / SPEI** | Sistema Externo | Códigos de autorización de tarjeta bancaria y confirmación de recepción de transferencias con clave de rastreo. | Solicitudes de cargo por cobro y montos transaccionales para acreditación en cuenta fiscal. |
| **Servicio de Correo (SMTP)** | Servicio Cloud | Confirmaciones de entrega de correos electrónicos. | Alertas automáticas de caducidad (<15 días) al administrador, alertas críticas DLQ y tickets de compra a clientes. |
| **Google Cloud Services** | Servicio Cloud | Puntuación y validación de tokens anti-bot (reCAPTCHA) y geolocalización de la cafetería en Google Maps. | Peticiones seguras con claves API para validación de tráfico y credenciales. |

---

### 4. Justificación Práctica en el Proyecto

El diagrama de contexto es indispensable porque nos permite ver a Monchis Café no como una isla aislada, sino como parte de un ecosistema real. Como bien explican Gido y Clements (2012), uno de los errores más graves en los proyectos de software es asumir que el sistema lo resolverá todo por su cuenta, ignorando cómo se conecta con los bancos, los clientes y los proveedores de grano. Al trazar estas fronteras, el equipo sabe exactamente qué interfaces deben construirse y qué dependencias externas se tienen que vigilar para que no se caiga el servicio en plena hora pico de la cafetería.

---

### 5. Referencias Bibliográficas

1. **Gido, J., & Clements, J. P. (2012).** *Administración exitosa de proyectos* (5.ª ed.). Cengage Learning.
2. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
3. **Sommerville, I. (2011).** *Ingeniería del software* (9.ª ed.). Addison-Wesley / Pearson Educación.
4. **Yourdon, E. (1989).** *Modern Structured Analysis*. Prentice Hall.
5. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

