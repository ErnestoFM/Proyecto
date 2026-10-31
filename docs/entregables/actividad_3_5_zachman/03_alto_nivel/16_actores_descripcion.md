# Nivel 3: ALTO NIVEL — Foco: QUIÉN
## Descripción de Actores del Sistema — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En el modelado con UML y el análisis de casos de uso, un actor no es necesariamente una persona con nombre y apellido; representa un rol idealizado que una entidad externa (humana, de hardware o de software) asume al interactuar directamente con las fronteras del sistema informático (Cockburn, 2000; Object Management Group [OMG], 2017). Como explican Pressman y Maxim (2021), es indispensable clasificar a los actores en **actores primarios** (aquellos que inician un caso de uso para cumplir un objetivo de valor directo) y **actores secundarios** (aquellos que brindan servicios complementarios, autorizaciones o almacenamiento externo para que el caso de uso pueda completarse con éxito).

Dentro de la Matriz de Zachman (1987), la celda **Alto Nivel - Quién** define los *Actores del Sistema* desde la perspectiva lógica del diseñador (*System Model / Designer's View*). En este nivel traducimos los roles comerciales que definimos en el nivel de Alcance en entidades formales del modelo de análisis. Para **Monchis Café**, los actores no solo son el barista o el dueño del negocio; también se modelan como actores del sistema a los servicios cloud externos (como la API de Google reCAPTCHA o el servidor SMTP de correo) y a los componentes internos automatizados que actúan como agentes autónomos (como el consumidor de eventos RabbitMQ).

---

### 2. Catálogo Formal de Actores del Sistema

El ecosistema de **Monchis Café** involucra ocho actores estructurados en tres categorías:

```
+=======================================================================================+
|                               ACTORES DE MONCHIS CAFÉ                                 |
+=======================================================================================+
| 1. ACTORES HUMANOS PRIMARIOS (Iniciadores de Casos de Uso):                           |
|    * ACT-01: Cajero de Mostrador (Barista)                                            |
|    * ACT-02: Administrador (Dueño / Gerente General)                                  |
|    * ACT-03: Cliente Consumidor (Monchis Rewards)                                     |
+---------------------------------------------------------------------------------------+
| 2. ACTORES HUMANOS SECUNDARIOS (Soporte Operativo):                                   |
|    * ACT-04: Proveedor Campesino (Cooperativas de Especialidad)                       |
+---------------------------------------------------------------------------------------+
| 3. ACTORES DE SISTEMA Y SERVICIOS EXTERNOS (Automatizados):                           |
|    * ACT-05: Servicio Cloud Google reCAPTCHA                                          |
|    * ACT-06: Pasarela Bancaria y Red SPEI (SAT)                                       |
|    * ACT-07: Servidor de Correo Electrónico SMTP                                      |
|    * ACT-08: Orquestador de Eventos RabbitMQ (Saga Worker)                            |
+=======================================================================================+
```

---

### 3. Fichas Descriptivas por Actor

| Identificador | Nombre del Actor | Tipo de Actor | Rol y Responsabilidad en el Sistema | Casos de Uso que Inicia / Participa |
| :--- | :--- | :--- | :--- | :--- |
| **ACT-01** | **Cajero de Mostrador** | Humano / Primario | Barista responsable de la venta rápida en la barra. Opera la terminal POS, escanea productos, aplica el bono ecológico (-$5.00), procesa cobros y realiza el arqueo al cierre de turno. | CU-01, CU-03, CU-04, CU-05, CU-06, CU-08. |
| **ACT-02** | **Administrador** | Humano / Primario | Dueño o gerente con control total del negocio. Gestiona catálogo y precios, registra lotes de café con trazabilidad, audita cortes Z, revisa analítica de tráfico UTM y descarga reportes. | CU-01, CU-02, CU-07, CU-08, CU-09, CU-10. |
| **ACT-03** | **Cliente Consumidor** | Humano / Primario | Usuario que consulta el menú web, compra bebidas en mostrador, presenta su termo reusable y acumula sellos digitales en Monchis Rewards. | CU-03, CU-04, CU-05, CU-06. |
| **ACT-04** | **Proveedor Campesino** | Humano / Secundario | Representante de cooperativas de Michoacán, Oaxaca o Chiapas. Entrega café con ficha de altura y tueste y recibe órdenes de compra. | CU-07. |
| **ACT-05** | **Google reCAPTCHA** | Sistema / Externo | Servicio de verificación anti-bot de Google que valida los tokens criptográficos enviados en el formulario de login y registro. | Participa en CU-01. |
| **ACT-06** | **Pasarela Bancaria / SPEI**| Sistema / Externo | Entidad financiera que procesa cobros con tarjetas bancarias y autoriza transacciones interbancarias mediante clave de rastreo. | Participa en CU-04. |
| **ACT-07** | **Servidor SMTP** | Sistema / Externo | Servicio de mensajería electrónica que despacha alertas de caducidad de lotes (<15 días) y avisos de eventos críticos en DLQ a gerencia. | Participa en CU-11, CU-12. |
| **ACT-08** | **Orquestador RabbitMQ** | Sistema / Interno | Componente autónomo (`SagaWorker`) que escucha colas AMQP para ejecutar reversas transaccionales y compensaciones ante roturas de stock. | Inicia y coordina CU-12. |

---

### 4. Matriz de Interacción Actor vs. Caso de Uso

La siguiente matriz cruza a cada actor con los doce casos de uso del sistema, indicando si actúa como iniciador principal (**P**) o como participante secundario (**S**):

| Caso de Uso | ACT-01 (Cajero) | ACT-02 (Admin) | ACT-03 (Cliente) | ACT-04 (Proveedor) | ACT-05 (reCAPTCHA) | ACT-06 (Banco) | ACT-07 (SMTP) | ACT-08 (RabbitMQ) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **CU-01: Iniciar Sesión** | **P** | **P** | **P** | — | **S** | — | — | — |
| **CU-02: 2FA Administrador** | — | **P** | — | — | — | — | — | — |
| **CU-03: Venta en Mostrador** | **P** | — | **S** | — | — | — | — | — |
| **CU-04: Cobro Multipago** | **P** | — | **S** | — | — | **S** | — | — |
| **CU-05: Bono Ecológico** | **P** | — | **S** | — | — | — | — | — |
| **CU-06: Monchis Rewards** | **P** | — | **S** | — | — | — | — | — |
| **CU-07: Registro Lote PEPS**| — | **P** | — | **S** | — | — | — | — |
| **CU-08: Corte de Caja Z** | **P** | **P** | — | — | — | — | — | — |
| **CU-09: Analítica UTM** | — | **P** | — | — | — | — | — | — |
| **CU-10: Exportar Reportes** | — | **P** | — | — | — | — | — | — |
| **CU-11: Alertas Sanitarias**| — | **S** | — | — | — | — | **S** | — |
| **CU-12: Reversa Saga** | **S** | **S** | **S** | — | — | — | **S** | **P** |

---

### 5. Justificación Práctica en el Proyecto

Modelar con exactitud a los actores en este nivel lógico evita un error común en la programación: creer que todos los casos de uso son iniciados por humanos sentados frente al teclado. Como advierte Cockburn (2000), los sistemas modernos orientados a eventos tienen casos de uso iniciados por temporizadores (*cron jobs*) o por colas de mensajería asíncrona. En Monchis Café, reconocer al `Orquestador RabbitMQ (ACT-08)` como actor formal nos permite programar las reversas de stock y los reembolsos sin depender de que un empleado tenga que hacer clic manual, protegiendo las cuentas del negocio incluso si el barista se distrae en barra.

---

### 6. Referencias Bibliográficas

1. **Cockburn, A. (2000).** *Writing Effective Use Cases*. Addison-Wesley Professional.
2. **Object Management Group. (2017).** *OMG Unified Modeling Language (OMG UML), Version 2.5.1*. OMG Document Number: formal/2017-12-05. https://www.omg.org/spec/UML/2.5.1/
3. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
4. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

