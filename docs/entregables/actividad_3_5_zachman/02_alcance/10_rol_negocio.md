# Nivel 2: ALCANCE — Foco: QUIÉN
## Roles de Negocio — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En la ingeniería de requerimientos, el análisis de los roles de negocio consiste en caracterizar de forma detallada a los usuarios y actores clave (*stakeholders*) que interactúan con los procesos de la empresa (Cockburn, 2000). Como señalan Pressman y Maxim (2021), un error muy común en el desarrollo de software es pensar en el "usuario" como un ente genérico; en la práctica, no tiene las mismas necesidades, conocimientos técnicos ni nivel de estrés un barista que tiene diez clientes esperando su café en la mañana, que el dueño del negocio revisando los estados financieros en su computadora por la noche.

Dentro de la Matriz de Zachman (1987), la celda **Alcance - Quién** define los *Roles de Negocio* desde la perspectiva del dueño (*Business Model / Owner's View*). En este nivel conceptual profundizamos en la caracterización operativa de cada perfil: sus objetivos diarios, las decisiones de negocio que toma, las restricciones de acceso que debe respetar y los riesgos operativos que el software le ayuda a mitigar (Sommerville, 2011).

---

### 2. Fichas de Caracterización de Roles de Negocio

Para **Monchis Café** se formalizan cuatro perfiles de negocio:

```
+---------------------------------------------------------------------------------------+
|                                ROLES DE NEGOCIO                                       |
+---------------------------------------------------------------------------------------+
| 1. Administrador General  | Dueño / Gerente. Estrategia, precios, compras y auditoría.|
| 2. Cajero de Turno        | Barista Mostrador. Ventas ágiles, arqueo y bono ecológico.|
| 3. Cliente Consumidor     | Comprador final. Café de calidad, sellos y termo reusable.|
| 4. Proveedor Campesino    | Cooperativas locales. Grano de especialidad trazable.     |
+---------------------------------------------------------------------------------------+
```

---

#### 2.1 Perfil de Negocio: Administrador General (Dueño / Gerente)
* **Descripción del Rol:** Persona responsable de la rentabilidad, administración general y cumplimiento fiscal de la cafetería. Es quien toma las decisiones de compra de grano y supervisa el desempeño de los empleados.
* **Nivel Técnico:** Medio (manejo fluido de correo, hojas de cálculo de Excel y aplicaciones web de oficina).
* **Objetivos Clave:**
  - Garantizar que las cuentas de caja cuadren al 100% todos los días sin faltantes inexplicables.
  - Monitorear la rotación del café orgánico para evitar pérdidas económicas por caducidad (Meta 12.3 de los ODS).
  - Medir la efectividad de las campañas digitales (tráfico proveniente de Google Maps e Instagram).
* **Responsabilidades y Permisos:**
  - Alta, modificación y desactivación de productos y precios oficiales.
  - Registro de lotes de café con cooperativas campesinas.
  - Auditoría y cierre definitivo del corte de caja diario (*Reporte Z*).
  - Gestión de usuarios y credenciales de acceso (con autenticación 2FA obligatoria).
* **Riesgo Mitigado:** Fugas de dinero por ventas no registradas y compras innecesarias de insumos.

---

#### 2.2 Perfil de Negocio: Cajero de Turno (Barista en Mostrador)
* **Descripción del Rol:** Empleado responsable de la atención al cliente en el mostrador, la toma de pedidos, el cobro multipago y la preparación de bebidas en barra.
* **Nivel Técnico:** Básico a Intermedio (experiencia con pantallas táctiles, teclados rápidos y terminales de cobro bancario).
* **Objetivos Clave:**
  - Atender a cada cliente con la máxima rapidez (menos de 45 segundos por transacción).
  - Cobrar con exactitud sin equivocarse en el cambio en efectivo ni en los comprobantes de tarjeta/SPEI.
  - Preguntar activamente por el termo o taza personal para promover la Bonificación Ecológica (Meta 12.5 de los ODS).
* **Responsabilidades y Permisos:**
  - Apertura de turno registrando el fondo inicial de caja.
  - Registro ágil de ventas en el POS mediante teclado (`F2`, `Esc`) o lector de código de barras.
  - Selección de métodos de pago y entrega de ticket digital o impreso.
  - Conteo de valores y arqueo ciego al terminar su jornada laboral.
* **Restricciones:** No puede modificar precios de catálogo ni alterar el stock de almacén sin autorización de gerencia.

---

#### 2.3 Perfil de Negocio: Cliente Consumidor (Final)
* **Descripción del Rol:** Personas de la comunidad que asisten a la cafetería en busca de café de especialidad orgánico de cooperativa, repostería artesanal o un espacio cálido de trabajo.
* **Nivel Técnico:** Variable (cualquier usuario con smartphone).
* **Objetivos Clave:**
  - Adquirir café de alta calidad a un precio justo y con rapidez de servicio.
  - Conocer el origen del café que consume (finca campesina, altura y tostado).
  - Obtener beneficios directos por cuidar el medio ambiente mediante su termo personal.
* **Interacción con el Sistema:**
  - Consulta del menú digital y credenciales ecológicas de los productos.
  - Registro en el programa "Monchis Rewards" para acumular sellos de lealtad (8vo café gratis).
  - Presentación de termo reusable para acceder al descuento directo de \$5.00 MXN en caja.

---

#### 2.4 Perfil de Negocio: Proveedor Campesino (Cooperativas de Especialidad)
* **Descripción del Rol:** Productores y cooperativas campesinas de Michoacán, Oaxaca y Chiapas que cultivan café arábica bajo sombra de forma sustentable.
* **Nivel Técnico:** Básico (interacción mediante comprobantes físicos y comunicaciones comerciales).
* **Objetivos Clave:**
  - Vender sus cosechas de café bajo condiciones de comercio justo sin intermediarios especuladores.
  - Demostrar la autenticidad y calidad de su grano mediante fichas de cata y fechas de beneficio.
* **Interacción con el Sistema:**
  - Entrega física de los bultos de café con su documentación técnica (origen, altitud, tipo de proceso y fecha de tueste).
  - Emisión de facturas y recepción de pagos mediante transferencias bancarias registradas en la cafetería.

---

### 3. Justificación Práctica en el Proyecto

Analizar los roles desde la perspectiva del negocio es lo que permite que el diseño de las interfaces de usuario (UI/UX) sea humanizado y coherente con las capacidades reales de la gente. Como señalan Pressman y Maxim (2021), forzar a un barista a navegar menús complicados mientras tiene la barra llena de pedidos es la receta perfecta para el caos. Al entender que el cajero necesita botones grandes, atajos rápidos de teclado y validaciones automáticas de cambio, logramos un software que no le estorba, sino que lo apoya en su trabajo diario.

---

### 4. Referencias Bibliográficas

1. **Cockburn, A. (2000).** *Writing Effective Use Cases*. Addison-Wesley Professional.
2. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
3. **Sommerville, I. (2011).** *Ingeniería del software* (9.ª ed.). Addison-Wesley / Pearson Educación.
4. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

