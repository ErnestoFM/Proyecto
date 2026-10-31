# Nivel 3: ALTO NIVEL — Foco: QUÉ
## Listado de Casos de Uso del Sistema — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En la ingeniería de software orientada a objetos y el modelado con UML, un caso de uso representa una unidad coherente de funcionalidad observable que el sistema ejecuta en interacción con uno o más actores para entregar un resultado de valor cuantificable (Jacobson, 1992). Como señala Cockburn (2000) en su obra clásica, los casos de uso son la herramienta fundamental para tender un puente entre lo que el negocio necesita y lo que los arquitectos deben diseñar; permiten organizar los requerimientos funcionales en historias completas de interacción, describiendo cómo el usuario y la computadora colaboran paso a paso para cumplir una tarea.

Dentro de la Matriz de Zachman (1987), la celda **Alto Nivel - Qué** se sitúa en la perspectiva del diseñador del sistema (*System Model / Designer's View*). En este nivel lógico, dejamos atrás las descripciones puramente comerciales y estructuramos formalmente el catálogo consolidado de **Casos de Uso (CU)**. Cada caso de uso agrupa requerimientos específicos, define con precisión los actores que lo disparan y establece las precondiciones y postcondiciones que garantizan la integridad de los datos en la cafetería (Pressman & Maxim, 2021).

---

### 2. Catálogo Consolidado de Casos de Uso (CU-01 a CU-12)

El sistema **Monchis Café** se estructura a nivel lógico en 12 casos de uso principales:

```
+---------------------------------------------------------------------------------------+
|                       CATÁLOGO DE CASOS DE USO — MONCHIS CAFÉ                         |
+---------------------------------------------------------------------------------------+
| CU-01: Iniciar Sesión con Google reCAPTCHA     | CU-07: Registrar Lote Campesino (PEPS)|
| CU-02: Autenticar Administrador con 2FA (TOTP) | CU-08: Ejecutar Arqueo y Corte de Caja|
| CU-03: Registrar Nueva Venta en Mostrador (POS)| CU-09: Consultar Analítica y UTM Maps |
| CU-04: Procesar Cobro Multipago en Caja        | CU-10: Exportar Reportes (PDF / Excel)|
| CU-05: Aplicar Bonificación Ecológica (ODS 12) | CU-11: Despachar Alertas Sanitarias   |
| CU-06: Canjear Bebida de Monchis Rewards       | CU-12: Orquestar Reversa Saga (Compens)|
+---------------------------------------------------------------------------------------+
```

---

| Identificador | Nombre del Caso de Uso | Actores Involucrados | Requerimientos Asociados | Descripción Sintética |
| :--- | :--- | :--- | :--- | :--- |
| **CU-01** | **Iniciar Sesión con Google reCAPTCHA** | Cajero, Administrador, Google reCAPTCHA | RF-10 | El usuario envía sus credenciales junto con el token anti-bot; el sistema valida con Google y genera tokens JWT stateless. |
| **CU-02** | **Autenticar Administrador con 2FA** | Administrador | RF-11 | Tras validar contraseña, el sistema solicita y comprueba el código TOTP de 6 dígitos antes de conceder permisos administrativos. |
| **CU-03** | **Registrar Nueva Venta en Mostrador** | Cajero | RF-01, RF-03, RF-15 | El cajero escanea productos con el lector de código de barras o teclado (`F2`), calculando precios oficiales del servidor. |
| **CU-04** | **Procesar Cobro Multipago en Caja** | Cajero, Cliente, Pasarela Bancaria | RF-04 | Cobro en Efectivo (con cambio automático), Tarjeta bancaria (con voucher) o Transferencia SPEI (con clave de rastreo). |
| **CU-05** | **Aplicar Bonificación Ecológica (ODS 12)**| Cajero, Cliente | RF-05 | Al presentar termo o taza personal, se aplica un descuento de \$5.00 MXN o sellos dobles en lealtad para reducir desechos. |
| **CU-06** | **Canjear Bebida de Monchis Rewards** | Cajero, Cliente | RF-06 | Al acumular 7 sellos digitales en el programa, el sistema bonifica el 8vo café de especialidad a costo cero (\$0.00). |
| **CU-07** | **Registrar Lote Campesino con Trazabilidad**| Administrador, Proveedor | RF-02, RF-07 | Captura de nuevo grano de café (finca, altura, fecha de tueste y caducidad) ingresándolo a la cola de rotación PEPS. |
| **CU-08** | **Ejecutar Arqueo y Corte de Caja (Reporte Z)**| Cajero, Administrador | RF-09 | Conteo ciego de efectivo físico al fin de turno, comparación con ventas registradas y emisión del corte consolidado Z. |
| **CU-09** | **Consultar Analítica y Atribución UTM** | Administrador | RF-12 | Visualización de ingresos totales, ticket promedio y porcentaje de clientes referidos por Google Maps o Instagram. |
| **CU-10** | **Exportar Reportes Financieros** | Administrador | RF-13 | Descarga en un clic de resúmenes de venta y mermas en formatos CSV (Excel) y PDF formal maquetado. |
| **CU-11** | **Despachar Alertas Sanitarias Preventivas**| Sistema, Servidor SMTP | RF-08 | Rutina automática diaria que envía correo electrónico a gerencia si un lote orgánico tiene menos de 15 días de vida útil. |
| **CU-12** | **Orquestar Reversa Transaccional (Saga)** | Sistema, RabbitMQ | RF-14 | En caso de desabasto inesperado durante la preparación, compensa la transacción reembolsando el cobro y registrando en DLQ. |

---

### 3. Justificación Práctica en el Proyecto

Organizar el comportamiento del sistema mediante un catálogo formal de casos de uso evita dispersiones entre los desarrolladores. Como explica Larman (2004), los casos de uso proporcionan la base sobre la cual se diseñan los diagramas de clases, las tablas de base de datos y las pruebas de integración automatizadas. En Monchis Café, tener delimitado qué hace cada caso de uso garantiza que funcionalidades complejas (como la reversa transaccional ante falta de grano o el bono ecológico) tengan un alcance preciso y no interfieran con la rapidez del cobro en el mostrador.

---

### 4. Referencias Bibliográficas

1. **Cockburn, A. (2000).** *Writing Effective Use Cases*. Addison-Wesley Professional.
2. **Jacobson, I. (1992).** *Object-Oriented Software Engineering: A Use Case Driven Approach*. ACM Press / Addison-Wesley.
3. **Larman, C. (2004).** *Applying UML and Patterns: An Introduction to Object-Oriented Analysis and Design and Iterative Development* (3.ª ed.). Prentice Hall.
4. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
5. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

