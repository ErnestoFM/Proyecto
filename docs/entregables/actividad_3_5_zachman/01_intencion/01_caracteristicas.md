# Nivel 1: INTENCIÓN — Foco: QUÉ
## Características del Sistema — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En la ingeniería de software y la gestión de proyectos, definir las características de un sistema no es simplemente hacer una lista de deseos o describir pantallas bonitas. Como señalan Pressman y Maxim (2021), las características representan el conjunto de propiedades funcionales y capacidades observables que el software debe ofrecer para satisfacer las necesidades del cliente. Si no se delimitan con claridad desde el primer momento, caemos en lo que en gestión se conoce como corrupción del alcance (*scope creep*), donde se agregan funciones al vapor sin planeación ni presupuesto (Project Management Institute, 2017).

Desde la perspectiva de la Matriz de Zachman (1987), la celda **Intención - Qué** (Nivel Contextual / Planificador) responde a la pregunta más básica del negocio: *¿Qué cosas materiales, datos y capacidades existen en el entorno que el sistema debe gestionar?* Para Sommerville (2011), esta etapa marca la frontera entre lo que el negocio realmente necesita operar y lo que queda fuera de la solución. En una cafetería que combina la venta de café orgánico de especialidad con repostería comercial, el sistema debe ser capaz de modelar tanto la calidez del servicio como la rigurosidad del control de inventarios y la seguridad en los cobros.

---

### 2. Características Principales de Monchis Café

A partir de los requerimientos y el modelo de negocio de Monchis Café, el sistema se estructura en torno a las siguientes características esenciales:

```
+----------------------------------------------------------------------------------+
|                     CARACTERÍSTICAS NÚCLEO — MONCHIS CAFÉ                        |
+----------------------------------------------------------------------------------+
| 1. Catálogo Segmentado      | Distinción clara entre café de especialidad         |
|    y Trazabilidad           | bajo sombra y productos comerciales.                |
+-----------------------------+----------------------------------------------------+
| 2. Punto de Venta (POS)     | Venta ágil de mostrador, atajos de teclado (F2),   |
|    Multipago en Mostrador   | soporte para lector de código de barras 1D/2D.     |
+-----------------------------+----------------------------------------------------+
| 3. Monchis Rewards          | Tarjeta digital de 8 sellos y bonificación         |
|    y Enfoque ODS 12         | ecológica ($5.00 MXN) por uso de termo reusable.   |
+-----------------------------+----------------------------------------------------+
| 4. Control de Inventarios   | Algoritmo PEPS (Primeras Entradas, Primeras Salidas)|
|    y Alertas Sanitarias     | con alertas preventivas por correo SMTP.           |
+-----------------------------+----------------------------------------------------+
| 5. Autenticación Stateless  | Seguridad basada en JWT en memoria, cookies        |
|    y Protección Web         | httpOnly, Google reCAPTCHA y 2FA para Admin.       |
+-----------------------------+----------------------------------------------------+
| 6. Analítica y Atribución   | Registro de canales de adquisición (Google Maps,   |
|    de Tráfico Digital       | Instagram y directo) con exportación en PDF/Excel. |
+----------------------------------------------------------------------------------+
```

#### 2.1 Catálogo Segmentado y Trazabilidad de Origen
El sistema clasifica el catálogo en dos categorías operativas:
* **Línea Orgánica:** Granos de café arábica cultivados bajo sombra por cooperativas campesinas de Michoacán, Oaxaca y Chiapas. Cada producto incluye información de su finca, altitud (msnm), notas de cata y fecha de tostado.
* **Línea Comercial:** Bebidas frías embotelladas, leches vegetales y repostería de consumo masivo con control convencional de existencias.

#### 2.2 Punto de Venta (POS) Ágil y Flexible
Diseñado para la atención física rápida en el mostrador:
* Soporte para múltiples formas de pago: **Efectivo** (con cálculo automático del cambio), **Tarjeta de Crédito/Débito**, **Transferencia/SPEI** (con captura obligatoria de la clave de rastreo bancaria) y **Pago Mixto**.
* Interfaz reactiva adaptada para pantallas táctiles y teclado rápido (atajos `F2` para cobrar y `Esc` para limpiar el carrito).
* Integración fluida con lectores de códigos de barras USB/HID para lectura directa del empaque del café.

#### 2.3 Programa de Fidelización "Monchis Rewards" y Bono Ecológico (ODS 12)
Fomentamos el consumo consciente alineado con la Meta 12.5 de los Objetivos de Desarrollo Sostenible (reducción de desechos):
* **Bonificación Ecológica:** Descuento directo de \$5.00 MXN o sellos dobles cuando el cliente presenta su propio termo o taza reutilizable en caja, desincentivando el uso de vasos desechables de un solo uso.
* **Tarjeta Digital de Sellos:** Acumulación automática de 1 sello por cada bebida preparada; al llegar a 7 sellos, el sistema otorga el 8vo café de cortesía.

#### 2.4 Control de Inventario PEPS y Alertas Sanitarias
Para evitar mermas en alimentos perecederos y granos tostados (ODS 12, Meta 12.3):
* El inventario opera estrictamente bajo el método **PEPS (Primeras Entradas, Primeras Salidas)**, asegurando que los lotes con fecha de tueste o elaboración más antigua salgan primero.
* Disparo automático de alertas preventivas vía correo electrónico (SMTP) cuando un lote orgánico tiene menos de 15 días antes de perder sus propiedades óptimas.

#### 2.5 Seguridad Web Robusta y Control de Acceso (RBAC)
* Arquitectura de autenticación desacoplada (*stateless*) mediante tokens JWT (Access Token de 15 minutos en memoria y Refresh Token rotativo en cookie segura `httpOnly`).
* Verificación obligatoria de **Google reCAPTCHA v2/v3** en formularios de acceso para mitigar ataques automatizados de bots.
* Doble Factor de Autenticación (**2FA / TOTP**) obligatorio para el rol de Administrador.

---

### 3. Justificación Práctica en el Proyecto

Tener bien definidas estas características desde la fase inicial nos evita malentendidos entre lo que espera el dueño de la cafetería y lo que los desarrolladores construyen. Como bien explica Sapag Chain (2011), un proyecto de inversión debe responder a una necesidad real del mercado; en nuestro caso, Monchis Café no solo necesitaba un software para cobrar café, sino una herramienta integral que resolviera el desorden en inventarios, premiara a los clientes ecológicos y mantuviera las cuentas claras sin fugas de dinero en caja.

---

### 4. Referencias Bibliográficas

1. **Project Management Institute. (2017).** *A Guide to the Project Management Body of Knowledge (PMBOK Guide)* (6.ª ed.). Project Management Institute.
2. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
3. **Sapag Chain, N. (2011).** *Proyectos de inversión: Formulación y evaluación* (2.ª ed.). Pearson Prentice Hall.
4. **Sommerville, I. (2011).** *Ingeniería del software* (9.ª ed.). Addison-Wesley / Pearson Educación.
5. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

