# Nivel 1: INTENCIÓN — Foco: POR QUÉ
## Visión y Objetivos del Proyecto — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

Todo proyecto de inversión y de ingeniería surge como respuesta a una necesidad insatisfecha, un problema operativo o una oportunidad estratégica en el mercado (Baca Urbina, 2013). Como señala el Project Management Institute (2017), el *Business Case* (o justificación del proyecto) es el documento que responde a la pregunta de por qué se deben destinar recursos económicos, tiempo y talento a una iniciativa; sin una visión clara, el proyecto carece de rumbo y es imposible evaluar si tuvo éxito o si fue un gasto innecesario.

En la Matriz de Zachman (1987), la celda **Intención - Por qué** representa la columna vertebral de la motivación empresarial. En este nivel del planificador, definimos la misión, la visión a largo plazo y los objetivos estratégicos que justifican la existencia del software (Kaplan & Norton, 1996). Para que los objetivos no se queden en buenas intenciones o discursos vacíos, la teoría administrativa exige estructurarlos bajo el modelo **SMART** (Específicos, Medibles, Alcanzables, Relevantes y con Límite de Tiempo) (Doran, 1981). En Monchis Café, el "Por qué" no es solo vender café, sino transformar una cafetería familiar en un negocio digitalizado, rentable, transparente y comprometido con la sustentabilidad ambiental.

---

### 2. Misión y Visión de Monchis Café

```
+---------------------------------------------------------------------------------------+
|                                  MISIÓN Y VISIÓN                                      |
+---------------------------------------------------------------------------------------+
| MISIÓN:                                                                               |
| Ofrecer una experiencia de café de especialidad orgánico y alimentos de alta calidad, |
| conectando de forma directa a cooperativas campesinas locales con consumidores        |
| urbanos, mediante un servicio ágil, transparente y con incentivos activos para la     |
| reducción de desechos plásticos y el cuidado del medio ambiente.                      |
+---------------------------------------------------------------------------------------+
| VISIÓN:                                                                               |
| Ser la cafetería de especialidad de referencia en la región por su modelo de comercio |
| justo, calidad en taza y vanguardia tecnológica, demostrando que una pequeña empresa  |
| familiar puede operar con estándares modernos de seguridad web, control de inventario |
| y compromiso ecológico comprobable.                                                   |
+---------------------------------------------------------------------------------------+
```

---

### 3. Objetivos del Proyecto (Metodología SMART)

#### 3.1 Objetivo General
Desarrollar e implementar la plataforma web integral y el sistema de Punto de Venta (POS) seguro para **Monchis Café** en un periodo de cuatro meses, automatizando el control de cobros multipago, la trazabilidad de lotes orgánicos y la fidelización con incentivos ecológicos, logrando una reducción del 95% en discrepancias de caja y un incremento del 20% en clientes recurrentes.

#### 3.2 Objetivos Específicos (Criterios SMART)

1. **Digitalización y Precisión en Caja (SMART):**
   * *Específico:* Automatizar el cobro en mostrador mediante una terminal táctil con soporte para efectivo, tarjetas bancarias y transferencias SPEI.
   * *Medible:* Reducir el tiempo de atención por cliente a menos de 45 segundos y disminuir los errores de arqueo al cierre de turno a un margen inferior al 0.5% del total diario.
   * *Alcanzable:* Utilizando un catálogo visual rápido con atajos de teclado (`F2`) y lectura de códigos de barras.
   * *Relevante:* Evita fugas de dinero y filas innecesarias en horas pico.
   * *Tiempo:* Operativo al finalizar el segundo mes de desarrollo.

2. **Control de Inventarios y Cero Mermas (SMART):**
   * *Específico:* Implementar la política de rotación **PEPS** para granos de café y perecederos con alertas preventivas por correo electrónico (SMTP).
   * *Medible:* Disminuir el desperdicio de café tostado por caducidad en un 90% durante los primeros seis meses de operación.
   * *Alcanzable:* El sistema emite alertas automáticas cuando un lote tiene menos de 15 días de vida útil óptima.
   * *Relevante:* Protege el margen de ganancia y asegura frescura total al cliente.
   * *Tiempo:* Desplegado en el tercer mes del proyecto.

3. **Fidelización y Consumo Sostenible (SMART):**
   * *Específico:* Operar el programa "Monchis Rewards" con la tarjeta digital de 8 sellos y la Bonificación Ecológica por recipiente reusable.
   * *Medible:* Lograr que al menos el 35% de las ventas diarias de café preparado se sirvan en termos o tazas traídas por el cliente, evitando más de 500 vasos desechables al mes.
   * *Alcanzable:* Bonificación automática de \$5.00 MXN en caja o sellos dobles.
   * *Relevante:* Diferencia a la cafetería de la competencia mediante un valor ecológico tangible.
   * *Tiempo:* Integrado desde el lanzamiento del MVP.

4. **Seguridad de la Información y Blindaje Web (SMART):**
   * *Específico:* Proteger la plataforma contra intrusiones, fraude en pedidos y ataques automatizados de bots.
   * *Medible:* Cero vulnerabilidades críticas abiertas en producción, 100% de formularios con Google reCAPTCHA y 2FA activo en cuentas administradoras.
   * *Alcanzable:* Mediante arquitectura stateless con JWT, cookies seguras `httpOnly` y middleware de validación Zod.
   * *Relevante:* Garantiza la confidencialidad de datos de clientes y la integridad del dinero en caja.
   * *Tiempo:* Verificado y auditado en la etapa de pre-despliegue.

---

### 4. Alineación con los Objetivos de Desarrollo Sostenible (ODS)

El proyecto no fue concebido únicamente como un ejercicio de código; está alineado de manera explícita con las metas de la **Agenda 2030 de la Organización de las Naciones Unidas (ONU, 2015)**:

* **ODS 12: Producción y Consumo Responsables (Eje Central del Proyecto):**
  - *Meta 12.2 (Uso eficiente de recursos):* Apoyo directo a cooperativas campesinas que cultivan café bajo sombra sin agroquímicos agresivos.
  - *Meta 12.3 (Reducción de mermas y desperdicios):* Control riguroso de caducidades mediante rotación PEPS.
  - *Meta 12.5 (Disminución sustancial de generación de desechos):* Incentivo económico y de fidelización por uso de termos y tazas personales en mostrador.
* **ODS 8: Trabajo Decente y Crecimiento Económico:**
  - Facilitación del trabajo del cajero y barista con interfaces intuitivas, reduciendo el estrés en mostrador y garantizando cuentas claras en las jornadas laborales.
* **ODS 9: Industria, Innovación e Infraestructura:**
  - Modernización tecnológica de una pequeña empresa tradicional mediante arquitectura desacoplada en la nube (Cloud Run) y eventos asíncronos.

---

### 5. Justificación Práctica en el Proyecto

Tener definidos la visión y los objetivos desde la celda de Intención es lo que le da sentido a cada línea de código que escribimos. Como advierte Sapag Chain (2011), cuando un proyecto no tiene claro su propósito económico y social, termina dispersando esfuerzos en detalles irrelevantes. Saber que nuestra meta es reducir mermas, proteger el dinero de la caja y premiar a los clientes ecológicos nos marca la pauta de cuáles historias de usuario deben priorizarse y cómo debe medirse el impacto real de la plataforma una vez en producción.

---

### 6. Referencias Bibliográficas

1. **Baca Urbina, G. (2013).** *Evaluación de proyectos* (7.ª ed.). McGraw-Hill Interamericana.
2. **Doran, G. T. (1981).** There's a S.M.A.R.T. way to write management's goals and objectives. *Management Review*, 70(11), 35–36.
3. **Kaplan, R. S., & Norton, D. P. (1996).** *The Balanced Scorecard: Translating Strategy into Action*. Harvard Business School Press.
4. **Organización de las Naciones Unidas. (2015).** *Transformar nuestro mundo: la Agenda 2030 para el Desarrollo Sostenible*. ONU. https://sdgs.un.org/es/goals
5. **Project Management Institute. (2017).** *A Guide to the Project Management Body of Knowledge (PMBOK Guide)* (6.ª ed.). Project Management Institute.
6. **Sapag Chain, N. (2011).** *Proyectos de inversión: Formulación y evaluación* (2.ª ed.). Pearson Prentice Hall.
7. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

