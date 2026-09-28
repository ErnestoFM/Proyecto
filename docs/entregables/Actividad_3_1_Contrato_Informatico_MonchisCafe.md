# CONTRATO DE PRESTACIÓN DE SERVICIOS PROFESIONALES DE DESARROLLO DE SOFTWARE Y OBRA INFORMÁTICA A PRECIO ALZADO

CONTRATO MIXTO DE PRESTACIÓN DE SERVICIOS PROFESIONALES DE INGENIERÍA DE SOFTWARE Y OBRA INFORMÁTICA A PRECIO ALZADO QUE CELEBRAN, POR UNA PARTE, LA EMPRESA **"SOLUCIONES DIGITALES FIERRO & ASOCIADOS S.A.S. DE C.V."**, A QUIEN EN LO SUCESIVO SE LE DENOMINARÁ COMO **"EL PRESTADOR"**, REPRESENTADA EN ESTE ACTO POR EL **C. ERNESTO FIERRO MORENO**, EN SU CARÁCTER DE ADMINISTRADOR ÚNICO Y DIRECTOR DE PROYECTO; Y POR LA OTRA PARTE, LA EMPRESA MERCANTIL **"MONCHIS CAFÉ S. DE R.L. DE C.V."**, A QUIEN EN LO SUCESIVO SE LE DENOMINARÁ COMO **"EL CLIENTE"**, REPRESENTADA EN ESTE ACTO POR SU GERENTE GENERAL, EL **C. CARLOS ALBERTO MONTEMAYOR SILVA**; SUJETÁNDOSE AMBAS PARTES AL TENOR DE LAS SIGUIENTES DECLARACIONES Y CLÁUSULAS:

---

## DECLARACIONES

### I. DECLARA "EL PRESTADOR", POR CONDUCTO DE SU REPRESENTANTE LEGAL:

**A.** Que es una sociedad mercantil legalmente constituida conforme a la Ley General de Sociedades Mercantiles, bajo la modalidad de Sociedad por Acciones Simplificada de Capital Variable, mediante contrato social formalizado a través del Sistema Electrónico de Constitución de la Secretaría de Economía con fecha 15 de agosto de 2024, con Boleta de Inscripción en el Registro Público de Comercio número **N-2024081599**, con folio mercantil electrónico activo.

**B.** Que cuenta con Registro Federal de Contribuyentes activo clave **SDF240815AB1**, encontrándose al corriente de sus obligaciones fiscales y de seguridad social.

**C.** Que su representante, el **C. Ernesto Fierro Moreno**, acredita su personalidad y facultades de administración en términos de la Cláusula Vigésima de los estatutos constitutivos, manifestando bajo protesta de decir verdad que dichas facultades no le han sido revocadas, modificadas ni limitadas en forma alguna.

**D.** Que respecto a las obras de software y aportaciones intelectuales que desarrolle su equipo técnico (integrado por **Ernesto Fierro Moreno, Jazmín Díaz, Héctor Hernández y Oswaldo Millán**), **"EL PRESTADOR"** se compromete y obliga a formalizar por escrito los respectivos contratos de prestación de servicios y obra por encargo con cesión expresa de derechos patrimoniales conforme al artículo 83 de la Ley Federal del Derecho de Autor, garantizando a **"EL CLIENTE"** la legítima e ininterrumpida cadena de titularidad previa a la suscripción del Acta de Recepción Definitiva.

**E.** Que dispone de la capacidad técnica, experiencia, herramientas computacionales, personal calificado e infraestructura requerida para desarrollar y poner en operación la plataforma de software objeto de este contrato.

**F.** Que señala como domicilio legal el ubicado en **Calle Hidalgo #245, Colonia Centro, Código Postal 59300, en la Ciudad de La Piedad de Cabadas, Estado de Michoacán**, y correo electrónico corporativo `proyectos@fierroasociados.dev`.

---

### II. DECLARA "EL CLIENTE", POR CONDUCTO DE SU REPRESENTANTE LEGAL:

**A.** Que es una persona moral legalmente constituida bajo las leyes mexicanas según consta en la Escritura Pública Número **4,892**, otorgada ante la fe del Notario Público Número 102 del Estado de Michoacán, Lic. Roberto Mendoza Valdés, inscrita en el Registro Público de Comercio de La Piedad, Michoacán, bajo el Folio Mercantil Electrónico **83921-1**.

**B.** Que cuenta con Registro Federal de Contribuyentes activo clave **MCA220410XX8**, con solvencia económica y capacidad financiera plena para celebrar este contrato y solventar las obligaciones contraídas.

**C.** Que su Gerente General, el **C. Carlos Alberto Montemayor Silva**, cuenta con facultades plenas de administración para celebrar este acto, las cuales no le han sido suspendidas, limitadas ni revocadas a la fecha de suscripción.

**D.** Que tiene interés formal en contratar el desarrollo, configuración, despliegue y puesta en marcha de la plataforma tecnológica integral **"Monchis Café"**, con el propósito de optimizar sus operaciones en barra, digitalizar la trazabilidad de café orgánico y automatizar sus programas de fidelización comercial.

**E.** Que señala como domicilio legal el ubicado en **Avenida Las Palmas #108, Fraccionamiento Los Laureles, Código Postal 59310, en la Ciudad de La Piedad, Michoacán**, y correo electrónico `administracion@monchiscafe.com.mx`.

---

### III. DECLARAN AMBAS PARTES:

**ÚNICA.** Que se reconocen recíprocamente la capacidad jurídica y personalidad con que comparecen a la suscripción del presente instrumento, manifestando que es su libre y espontánea voluntad obligarse al tenor de las siguientes:

---

## CLÁUSULAS

### CLÁUSULA PRIMERA. OBJETO DEL CONTRATO
**"EL PRESTADOR"** se obliga a prestar a favor de **"EL CLIENTE"**, y este último se obliga a recibir conforme a los criterios objetivos de aceptación establecidos en la Cláusula Novena y en el **Anexo "A" (SOW)**, los servicios profesionales de ingeniería de software y la obra informática consistente en el diseño, desarrollo, pruebas, configuración de infraestructura y despliegue productivo de la plataforma web integral denominada **"MONCHIS CAFÉ"** (en adelante, **"EL SISTEMA"**).

---

### CLÁUSULA SEGUNDA. ALCANCE, ESPECIFICACIONES TÉCNICAS Y PROCESAMIENTO DE PAGOS
**"EL SISTEMA"** se desarrollará bajo una arquitectura de **Monorepo gestionado con Turborepo y pnpm workspaces**, integrando los siguientes módulos funcionales:
1. **Autenticación Stateless y Seguridad:** JSON Web Tokens (JWT) rotativos con Refresh Token en cookies seguras `httpOnly`, `Secure` y `SameSite=Strict`; Google reCAPTCHA v2/v3 anti-bots; Control de Acceso Basado en Roles (RBAC) con roles `admin`, `cajero` y `cliente`, y autenticación de doble factor (2FA) para cuentas administrativas.
2. **Punto de Venta Táctil (POS) y Pasarela de Pagos:** Interfaz optimizada para tabletas de barra; cobro simultáneo en efectivo (cálculo automatizado de cambio), SPEI (registro de clave de rastreo) y puntos de lealtad. Para pagos con tarjeta de crédito o débito, el sistema se integrará con pasarelas de pago y terminales adquirentes bancarias comerciales (Stripe, Clip o Mercado Pago). Se estipula expresamente que **"EL CLIENTE" es el único responsable de contratar la cuenta mercantil o pasarela correspondiente, de someterse a sus términos de afiliación y de absorber el 100% de las comisiones bancarias y de procesamiento por transacción**. **"EL PRESTADOR"** responde únicamente de la integración técnica de software vía APIs y Webhooks. Integración con lectores de código 1D/2D e impresoras térmicas de tickets estándar de 80 mm conforme a los requerimientos del Anexo "A".
3. **Broker Asíncrono RabbitMQ y Patrón Saga:** Transacciones distribuidas bajo Topic Exchange `cafeteria.events`; orquestación de transacciones compensatorias automáticas ante desabasto de insumos orgánicos y enrutamiento hacia Dead Letter Queue (DLQ) con alertas por correo electrónico (SMTP).
4. **Trazabilidad y Sostenibilidad (ODS 12):** Catálogo segmentado de café orgánico de especialidad regional y comercial; registro por cooperativa de origen, finca, altitud, fecha de tueste y rotación PEPS (Primeras Entradas, Primeras Salidas).
5. **Programa de Fidelización "Monchis Rewards":** Monedero digital, sellos para bebidas preparadas (8va bebida gratis tras 7 compras acumuladas) y bonificación ecológica directa de $5.00 MXN por consumo en taza o termo reutilizable.
6. **Dashboard y Atribución UTM:** Captura de parámetros `utm_source`, `utm_medium` y `utm_campaign` (discriminando visitas originadas en Google Maps vs Instagram) y reportes en PDF y hojas de cálculo Excel (.xlsx).
7. **Diseño y SEO:** Prerenderizado estático en tiempo de construcción (`vite-ssg`), datos estructurados Schema.org (`LocalBusiness` / `CoffeeShop`) y diseño UI/UX pastel.

---

### CLÁUSULA TERCERA. METODOLOGÍA DE DESARROLLO Y SPRINTS
El proyecto se ejecutará bajo la metodología ágil **SCRUM** complementada con la práctica de **Desarrollo Guiado por Pruebas (Test-Driven Development - TDD)**, estructurado en **8 Sprints quincenales**. Al término de cada Sprint, se celebrará una sesión de revisión y demostración (*Sprint Review*) en el entorno de pruebas (*Staging*) para validar el incremento de software funcional entregado.

---

### CLÁUSULA CUARTA. VIGENCIA, CRONOGRAMA DE EJECUCIÓN Y SUBSISTENCIA
1. La vigencia del cronograma de desarrollo del presente contrato será de **16 semanas naturales** (equivalentes a 112 días calendario), comprendidas formalmente del **31 de Agosto de 2026** al **20 de Diciembre de 2026**, conforme al cronograma de hitos estipulado en el **Anexo "B"**. Cualquier prórroga requerirá un Convenio Modificatorio gestionado mediante el procedimiento de control de cambios de la Cláusula Décima.
2. **Cláusula de Subsistencia:** Las partes reconocen expresamente que la suscripción del Acta Definitiva, el finiquito de los saldos devengados pendientes, la Garantía Técnica y SLA (Cláusula Décima Primera), las obligaciones de Confidencialidad y Secreto Industrial (Cláusula Décima Tercera) y el régimen de Propiedad Intelectual y Licenciamiento (Cláusula Décima Segunda) **subsistirán y sobrevivirán en pleno vigor con posterioridad a la culminación del cronograma de desarrollo o terminación de la vigencia del contrato**.

---

### CLÁUSULA QUINTA. CONTRAPRESTACIÓN Y HONORARIOS
**"EL CLIENTE"** se obliga a pagar a **"EL PRESTADOR"** por concepto de honorarios profesionales y obra de desarrollo la cantidad total fija y cerrada de **$358,000.00 MXN (Trescientos cincuenta y ocho mil pesos 00/100 M.N.)**, más el 16% de Impuesto al Valor Agregado (IVA) correspondiente a **$57,280.00 MXN**, resultando un importe total bruto de **$415,280.00 MXN (Cuatrocientos quince mil doscientos ochenta pesos 00/100 M.N.)**.  
Dicho importe retribuye exclusivamente la mano de obra calificada de ingeniería. La infraestructura de nube y el equipamiento físico de mostrador corren por cuenta directa de **"EL CLIENTE"** conforme al **Anexo "C"**.

---

### CLÁUSULA SEXTA. CONDICIONES Y CALENDARIO DE PAGO
La contraprestación se liquidará contra la suscripción de las **Actas de Entrega-Recepción Parcial y Definitiva**, conforme al siguiente calendario de hitos técnicos:

| Hito / Sprint | Entregable Técnico | Importe Neto (MXN) | 16% IVA (MXN) | Total Bruto (MXN) |
|---|---|---|---|---|
| **Hito 1 (Sprint 1)** | Setup Monorepo, Docker Compose y Prisma ORM | $24,000.00 | $3,840.00 | $27,840.00 |
| **Hito 2 (Sprint 2)** | Backend Core, JWT Stateless, RBAC y reCAPTCHA | $30,000.00 | $4,800.00 | $34,800.00 |
| **Hito 3 (Sprint 3)** | Broker RabbitMQ, Patrón Saga y DLQ | $30,000.00 | $4,800.00 | $34,800.00 |
| **Hito 4 (Sprint 4)** | Frontend Vue 3, Tokens Pastel y SEO `vite-ssg` | $30,000.00 | $4,800.00 | $34,800.00 |
| **Hito 5 (Sprint 5)** | POS Táctil de Barra, Lector QR y Pagos Mixtos | $50,000.00 | $8,000.00 | $58,000.00 |
| **Hito 6 (Sprint 6)** | Trazabilidad Café ODS 12 y Monchis Rewards | $40,000.00 | $6,400.00 | $46,400.00 |
| **Hito 7 (Sprint 7)** | Dashboard Admin, Atribución UTM y Reportes | $30,000.00 | $4,800.00 | $34,800.00 |
| **Hito 8 (Sprint 8)** | Testing Multicapa (Vitest/Playwright) y SAST | $54,000.00 | $8,640.00 | $62,640.00 |
| **Hito 9 (Cierre)** | Despliegue GCP (Terraform), Manuales y Release | $70,000.00 | $11,200.00 | $81,200.00 |
| **TOTALES** | **Mano de Obra de Ingeniería de Software** | **$358,000.00** | **$57,280.00** | **$415,280.00** |

**Condición de Exigibilidad:** Cada importe será exigible **dentro de los 5 (cinco) días hábiles posteriores a la suscripción del Acta de Entrega-Recepción del Hito respectivo, o bien, dentro de los 5 (cinco) días hábiles posteriores al vencimiento del plazo de revisión estipulado en la Cláusula Novena si "EL CLIENTE" no hubiese emitido observaciones justificadas por escrito (aprobación tácita por afirmativa ficta)**, previa entrega del CFDI correspondiente.

---

### CLÁUSULA SÉPTIMA. OBLIGACIONES DE "EL PRESTADOR"
1. Desarrollar **"EL SISTEMA"** conforme a las especificaciones contenidas en el Anexo "A" y las buenas prácticas de la industria.
2. **Cero Hardcoding:** No escribir credenciales, contraseñas, secretos de JWT ni claves de API en el código fuente, gestionándolas a través de variables de entorno protegidas (`.env`).
3. Someter los módulos a pruebas de aseguramiento de calidad según los criterios estipulados en la Cláusula Novena.
4. Entregar el código fuente íntegro en repositorio Git y la documentación técnica de despliegue con Terraform.

---

### CLÁUSULA OCTAVA. OBLIGACIONES DE "EL CLIENTE"
1. Designar a un enlace técnico para evaluar las entregas y emitir validaciones en un lapso no mayor a 5 (cinco) días hábiles.
2. Entregar oportunamente catálogos de precios, recetas, padrón de proveedores y material de identidad visual.
3. Proveer y financiar el hardware de mostrador y las suscripciones de infraestructura de nube (GCP y CloudAMQP).
4. Pagar puntualmente las facturas dentro de los plazos estipulados en la Cláusula Sexta.

---

### CLÁUSULA NOVENA. PROCEDIMIENTO DE PRUEBAS Y CRITERIOS OBJETIVOS DE ACEPTACIÓN
La recepción de cada hito se formalizará mediante un **Acta de Entrega-Recepción**. Para su aprobación técnica, los entregables deberán satisfacer los siguientes criterios objetivos modulados por fase:
1. **Hitos de Arquitectura, Backend e Infraestructura (Hitos 1, 2 y 3):** Cobertura de pruebas unitarias y de integración backend (`pnpm test:unit`) mayor o igual al 80% sobre la lógica implementada, esquemas de datos validados estrictamente con Zod y compilación exitosa sin errores de tipado o migración en Prisma ORM.
2. **Hitos de Frontend y Componentes Visuales (Hitos 4, 5 y 6):** Pruebas unitarias de componentes en Vitest aprobadas, renderizado responsivo conforme al sistema de diseño pastel y validación funcional en el entorno de Staging de las interfaces correspondientes a cada hito.
3. **Hito de Testing Integral (Hito 8) y Acta Definitiva (Hito 9):** Aprobación del 100% de la suite completa de pruebas E2E automatizadas con Playwright simulando los flujos integrales de venta en mostrador, canje de sellos Monchis Rewards y transacciones compensatorias Saga en resoluciones de 360px, 768px y 1024px; acompañado del reporte de análisis estático (SAST) libre de vulnerabilidades catalogadas como Críticas o Altas según la escala CVSS/OWASP.  
**"EL CLIENTE"** dispondrá de 5 (cinco) días hábiles para emitir observaciones justificadas. Si transcurrido dicho plazo **"EL CLIENTE"** no emite observaciones justificadas por escrito ni suscribe el Acta, operará la afirmativa ficta, teniéndose el hito por técnicamente recibido y aprobado de pleno derecho para todos los efectos legales, comenzando a correr a partir de ese momento el plazo de pago estipulado en la Cláusula Sexta.

---

### CLÁUSULA DÉCIMA. PROCEDIMIENTO DE CONTROL DE CAMBIOS
Cualquier solicitud de modificación funcional que altere el alcance del **Anexo "A"** deberá someterse a una **Solicitud de Cambio (Change Request)**. **"EL PRESTADOR"** evaluará el impacto técnico en horas y costo, emitiendo una cotización en un plazo de 3 (tres) días hábiles. Ningún cambio se incorporará al desarrollo sin la aprobación firmada de la adenda económica y de cronograma respectiva.

---

### CLÁUSULA DÉCIMA PRIMERA. GARANTÍA TÉCNICA Y NIVELES DE SERVICIO (SLA)
**"EL PRESTADOR"** otorga una **Garantía Técnica de 90 (noventa) días naturales** contados a partir del día siguiente a la firma del Acta de Recepción Definitiva, obligándose a corregir sin costo defectos de código (*bugs*), errores transaccionales de la Saga o fallas de lógica imputables al software entregado.
- **Ventana de Cobertura de Soporte:** Lunes a Sábado de 07:00 a 20:00 horas (horario del centro de México).
- **Incidentes Críticos (POS inoperativo o caída del backend):** Tiempo de respuesta < 2 horas; resolución < 12 horas hábiles dentro de la ventana de soporte.
- **Incidentes Mayores (Fallas parciales en reportes o panel admin):** Tiempo de respuesta < 8 horas; resolución < 48 horas hábiles.
- **Incidentes Menores (Ajustes visuales):** Tiempo de respuesta < 24 horas; resolución en el siguiente ciclo semanal de mantenimiento.

---

### CLÁUSULA DÉCIMA SEGUNDA. PROPIEDAD INTELECTUAL, CESIÓN TEMPORAL Y LICENCIAMIENTO RESIDUAL
Conforme a los artículos 13 frac. XI, 30, 33, 83 y 101 a 114 de la **Ley Federal del Derecho de Autor (LFDA)**:
1. **Derechos Morales:** Corresponden de forma inalienable, perpetua e imprescriptible a los desarrolladores físicos autores del código fuente.
2. **Cesión de Derechos Patrimoniales:** **"EL PRESTADOR"** cede a título **oneroso, exclusivo y temporal por un período determinado de 10 (diez) años**, prorrogable mediante acuerdo expreso y por escrito entre las partes, la totalidad de los derechos patrimoniales sobre **"EL SISTEMA"** a favor de **"EL CLIENTE"**, supeditada a la liquidación total de los honorarios pactados.
3. **Ámbito Territorial y Modalidades de Explotación:** La cesión patrimonial se concede para el ámbito territorial de los Estados Unidos Mexicanos (con acceso transfronterizo derivado de servicios cloud), facultando a **"EL CLIENTE"** para la explotación, reproducción, operación, ejecución y uso exclusivo en sus establecimientos comerciales, puntos de venta físicos, plataformas web y canales digitales.
4. **Régimen al Vencimiento de los 10 Años (Año 11):** Concluido el plazo de 10 (diez) años, si las partes no convinieren por escrito una prórroga de la cesión exclusiva, **"EL CLIENTE" conservará en todo momento una licencia definitiva, no exclusiva, intransferible y libre de regalías (royalty-free)** para continuar utilizando, ejecutando y operando **"EL SISTEMA"** en sus sucursales comerciales presentes y futuras, garantizando la continuidad ininterrumpida de su operación de negocio.
5. **Software Libre y de Terceros:** Se excluyen de la cesión las librerías de código abierto y dependencias del ecosistema (Vue.js, Next.js, Prisma, Tailwind CSS bajo licencias MIT/Apache 2.0, y RabbitMQ bajo licencia Mozilla Public License 2.0 - MPL 2.0). **"EL PRESTADOR"** garantiza no incorporar componentes bajo licencias copyleft restrictivas (como GPLv3 o AGPL) que impongan la obligación de liberar el código privativo de **"EL CLIENTE"**.

---

### CLÁUSULA DÉCIMA TERCERA. CONFIDENCIALIDAD Y SECRETO INDUSTRIAL
Las partes se obligan a guardar la más estricta reserva respecto a información comercial, recetas de café, padrón de proveedores, código fuente, esquemas de bases de datos y arquitectura tecnológica. Esta obligación subsistirá durante la vigencia del contrato y por **5 (cinco) años adicionales** a su conclusión, al amparo de la Ley Federal de Protección a la Propiedad Industrial.

---

### CLÁUSULA DÉCIMA CUARTA. PROTECCIÓN DE DATOS PERSONALES Y CIBERSEGURIDAD
De conformidad con la **Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP)**:
1. **"EL CLIENTE"** reviste el carácter de *Responsable* y **"EL PRESTADOR"** el de *Encargado* del tratamiento de los datos personales recabados de clientes y personal operativo. **"EL CLIENTE"** se obliga a contar con su **Aviso de Privacidad Integral** debidamente publicado en la plataforma y puesto a disposición de los titulares previo al tratamiento de datos.
2. **Infraestructura y Alojamiento:** Las partes reconocen que la infraestructura en la nube de Google Cloud Platform y el broker CloudAMQP son servicios contratados directamente por **"EL CLIENTE"** (Responsable) conforme a la Cláusula Octava, siendo utilizados por **"EL PRESTADOR"** para la implementación técnica de la plataforma.
3. **Almacenamiento Seguro de Credenciales:** Las contraseñas de usuarios se gestionarán exclusivamente mediante **funciones criptográficas de dispersión unidireccional con salting (bcrypt)**.
4. **Prohibición de Almacenamiento Financiero:** Queda prohibido almacenar números de tarjetas de crédito/débito, códigos CVV o NIP en el sistema, procesándose los pagos mediante pasarelas certificadas bajo PCI-DSS.
5. **Notificación Contractual de Brechas:** En caso de que **"EL PRESTADOR"** detecte vulneraciones de seguridad que comprometan datos personales almacenados en la plataforma, notificará a **"EL CLIENTE"** dentro de un plazo máximo de **24 horas**, a fin de que este último adopte las medidas correctivas y proceda a informar de manera inmediata a los titulares afectados en términos del artículo 19 de la LFPDPPP.
6. **Destino, Devolución o Destrucción de Datos:** A la conclusión de los servicios o terminación del presente contrato, **"EL PRESTADOR"** devolverá a **"EL CLIENTE"** todas las bases de datos y respaldos que contengan datos personales, o bien procederá a su borrado seguro y destrucción digital irreversible, emitiendo constancia formal por escrito, salvo aquellos datos que deban conservarse por mandato legal o fiscal aplicable.

---

### CLÁUSULA DÉCIMA QUINTA. INEXISTENCIA DE SUBORDINACIÓN LABORAL Y EXCLUSIÓN DE REPSE
Las partes convienen que la relación que las une es de estricta naturaleza civil y mercantil independiente. **"EL PRESTADOR"** ejecuta los servicios con sus propios medios técnicos, computacionales y metodológicos, sin poner a disposición personal subordinado en los establecimientos de **"EL CLIENTE"**.  
Por lo anterior, **no resulta legalmente exigible la inscripción en el Padrón Público de Contratistas de Servicios Especializados (REPSE)** en términos de los artículos 12 al 15 de la Ley Federal del Trabajo. Las sesiones transitorias de inducción técnica y capacitación en mostrador estipuladas en el Hito 9 poseen naturaleza estrictamente formativa y de entrega de obra, no constituyendo intermediación ni subcontratación de personal.

---

### CLÁUSULA DÉCIMA SEXTA. PENAS CONVENCIONALES Y TOPE DE RESPONSABILIDAD
1. **Mora de Pago:** En caso de retraso injustificado en el pago de los hitos por parte de **"EL CLIENTE"**, se generará un interés moratorio del 1.5% mensual sobre los saldos vencidos.
2. **Mora de Entrega:** Si **"EL PRESTADOR"** incurre en retraso injustificado atribuible exclusivamente a su gestión, se aplicará una pena del 0.5% semanal sobre el valor neto del hito demorado, hasta un tope máximo acumulado del 10% del hito.
3. **Tope de Responsabilidad:** La responsabilidad total acumulada de **"EL PRESTADOR"** por daños y perjuicios derivados del contrato estará contractualmente limitada al 100% del monto efectivamente cobrado bajo el presente instrumento, excluyendo pérdidas consecuenciales, lucro cesante o pérdidas comerciales del establecimiento.

---

### CLÁUSULA DÉCIMA SÉPTIMA. TERMINACIÓN ANTICIPADA ORDINARIA
1. **"EL CLIENTE"** podrá dar por terminado anticipadamente el contrato notificando por escrito a **"EL PRESTADOR"** con al menos **15 (quince) días naturales de anticipación**, obligándose a liquidar los hitos terminados, los trabajos en proceso a prorrata y una compensación del 5% del remanente no devengado por gastos de desmovilización técnica.
2. A fin de garantizar la estabilidad y culminación del desarrollo, **"EL PRESTADOR"** no gozará de terminación voluntaria unilateral ordinaria, debiendo apegarse al procedimiento de rescisión de la Cláusula Décima Octava ante causas justificadas de incumplimiento.
3. **Transmisión de Derechos Parcial:** Si el contrato concluye anticipadamente, los derechos patrimoniales sobre los módulos terminados y efectivamente liquidados se transmitirán a **"EL CLIENTE"**; los módulos no liquidados permanecerán bajo titularidad del equipo desarrollador.

---

### CLÁUSULA DÉCIMA OCTAVA. RESCISIÓN POR INCUMPLIMIENTO SUSTANCIAL
Cualquiera de las partes podrá rescindir de pleno derecho el presente contrato ante el incumplimiento sustancial de las obligaciones pactadas:
- Serán causas imputables a **"EL PRESTADOR"**: suspender injustificadamente las actividades por más de 10 días hábiles continuos o desatender de forma reiterada los criterios de aceptación técnica.
- Serán causas imputables a **"EL CLIENTE"**: incurrir en mora de pago por más de 15 días naturales o no entregar los insumos y accesos indispensables para el desarrollo.  
La parte afectada notificará por escrito a la incumplida, otorgando un plazo de **5 (cinco) días hábiles** para subsanar la falta. De persistir el incumplimiento, operará la rescisión inmediata.

---

### CLÁUSULA DÉCIMA NOVENA. CASO FORTUITO O FUERZA MAYOR
Ninguna parte responderá por retrasos derivados de causas de fuerza mayor o caso fortuito (contingencias sanitarias, catástrofes naturales, cortes prolongados de telecomunicaciones o fallas globales de infraestructura en GCP ajenas al control de las partes), suspendiéndose los plazos contractuales mientras subsista la eventualidad.

---

### CLÁUSULA VIGÉSIMA. DOMICILIOS Y NOTIFICACIONES
Toda notificación formal entre las partes se practicará por escrito en los domicilios consignados en las Declaraciones o vía correo electrónico con acuse formal de recibo a `proyectos@fierroasociados.dev` y `administracion@monchiscafe.com.mx`.

---

### CLÁUSULA VIGÉSIMA PRIMERA. INTEGRIDAD CONTRACTUAL Y ANEXOS
El presente contrato y sus Anexos "A", "B" y "C" constituyen el acuerdo íntegro y definitivo entre las partes respecto a su objeto, dejando sin efecto cualquier comunicación, minuta o cotización previa.

---

### CLÁUSULA VIGÉSIMA SEGUNDA. JURISDICCIÓN Y LEGISLACIÓN APLICABLE
El presente contrato se rige por las disposiciones mercantiles del **Código de Comercio**, la **Ley Federal del Derecho de Autor**, supletoriamente el **Código Civil Federal**, y para cualquier litigio que se suscite con motivo de su interpretación o cumplimiento, las partes se someten expresamente a la competencia de los **Tribunales de la Ciudad de La Piedad de Cabadas, Estado de Michoacán**, renunciando al fuero que pudiera corresponderles por razón de sus domicilios presentes o futuros.

---

## SUSCRIPCIÓN Y FIRMAS FORMALES

LEÍDO EL PRESENTE CONTRATO Y SUS ANEXOS POR AMBAS PARTES Y ENTERADAS DE SU VALOR Y FUERZA LEGAL, LO RATIFICAN Y FIRMAN POR DUPLICADO EJEMPLAR AL MARGEN Y AL CALCE, EN LA CIUDAD DE LA PIEDAD DE CABADAS, ESTADO DE MICHOACÁN, A LOS **31 DÍAS DEL MES DE AGOSTO DEL AÑO 2026**.

<br><br><br>

```
                  POR "EL PRESTADOR":                                         POR "EL CLIENTE":
         SOLUCIONES DIGITALES FIERRO & ASOCIADOS S.A.S. DE C.V.             MONCHIS CAFÉ S. DE R.L. DE C.V.



       _______________________________________________            _______________________________________________
                 C. ERNESTO FIERRO MORENO                               C. CARLOS ALBERTO MONTEMAYOR SILVA
              Administrador Único y Director                                      Gerente General
```

<br><br>

---

## ANEXO "A": ESPECIFICACIONES TÉCNICAS, REQUERIMIENTOS FUNCIONALES (SOW) Y HARDWARE

1. **Arquitectura del Software:** Monorepo con Turborepo y pnpm workspaces; Frontend en Vue 3 con Vite y Tailwind CSS; Backend en Next.js con API Routes y Prisma ORM conectado a PostgreSQL en Cloud SQL.
2. **Asincronía y Resiliencia:** Broker RabbitMQ Topic Exchange `cafeteria.events`, Patrón Saga con transacciones compensatorias de reversa en cobro/inventario y colas Dead Letter Queue (DLQ).
3. **Seguridad Stateless:** Tokens JWT rotativos en cookies seguras `httpOnly`, Google reCAPTCHA v2/v3 en login y registro, 2FA para administradores y control de acceso basado en roles (RBAC).
4. **Punto de Venta e Insumos:** Terminal táctil con cobro mixto (efectivo, tarjeta, SPEI, Monchis Rewards) y trazabilidad estricta de café de especialidad regional bajo ODS 12.
5. **Marketing y Atribución:** Captura y reporte de conversiones por parámetros `utm_source`, `utm_medium` y `utm_campaign` (Google Maps vs Instagram).
6. **Especificaciones Mínimas de Hardware y Periféricos Compatibles:**
   - *Terminal POS Barra:* Tableta táctil con sistema operativo Android 10.0 o superior (o iPadOS 15+), pantalla mínima de 10 pulgadas, memoria RAM de al menos 3 GB y navegador web Google Chrome o Safari actualizado.
   - *Impresora de Tickets Térmicos:* Impresora estándar de 80 mm con velocidad mínima de 200 mm/s, emulación de comandos estándar ESC/POS y conectividad vía USB o interfaz de red Ethernet/Wi-Fi.
   - *Lector Óptico de Códigos:* Escáner láser o generador de imágenes 1D/2D (compatible con lectura de códigos de barras tradicionales y códigos QR de pantalla de teléfono móvil), con interfaz de emulación de teclado USB HID (Plug & Play).

---

## ANEXO "B": CRONOGRAMA DE EJECUCIÓN TEMPORAL POR SPRINTS (GANTT DE 16 SEMANAS)

*Horizonte de 16 semanas naturales (112 días calendario): del 31 de Agosto de 2026 al 20 de Diciembre de 2026.*

- **Sprint 1 (Semana 1 y 2 / 31 Ago – 13 Sep):** Setup Monorepo, Docker Compose y Modelo Prisma BD.
- **Sprint 2 (Semana 3 y 4 / 14 Sep – 27 Sep):** Backend Core, JWT Stateless, RBAC y Google reCAPTCHA.
- **Sprint 3 (Semana 5 y 6 / 28 Sep – 11 Oct):** Broker RabbitMQ, Patrón Saga y Dead Letter Queue (DLQ).
- **Sprint 4 (Semana 7 y 8 / 12 Oct – 25 Oct):** Frontend Vue 3, Tokens Pastel y SEO con `vite-ssg`.
- **Sprint 5 (Semana 9 y 10 / 26 Oct – 08 Nov):** Punto de Venta (POS) Táctil, Lector QR y Pagos Mixtos.
- **Sprint 6 (Semana 11 y 12 / 09 Nov – 22 Nov):** Trazabilidad Café Orgánico ODS 12 y Monchis Rewards.
- **Sprint 7 (Semana 13 y 14 / 23 Nov – 06 Dic):** Dashboard Administrativo, Atribución UTM y Reportes en PDF/Excel.
- **Sprint 8 (Semana 15 y 16 / 07 Dic – 20 Dic):** Testing Multicapa (Vitest/Playwright), Auditoría SAST, Despliegue en GCP con Terraform, Capacitación en Barra y Entrega Definitiva.

---

## ANEXO "C": DESGLOSE DEL PRESUPUESTO MAESTRO DE DESARROLLO E INFRAESTRUCTURA

*(Valores expresados en Pesos Mexicanos MXN, subtotales netos antes de IVA)*

1. **Mano de Obra y Desarrollo de Software (Objeto de este Contrato):** **$358,000.00 MXN neto** ($415,280.00 MXN con 16% de IVA).
2. **Equipamiento Físico en Barra (Adquisición directa por EL CLIENTE):** Terminal táctil ($6,500.00), Impresora de tickets ($1,800.00), Escáner 2D ($1,200.00) = **$9,500.00 MXN**.
3. **Servicios Cloud y Licencias (4 meses a cargo directo de EL CLIENTE):** Google Cloud Platform ($7,200.00), CloudAMQP RabbitMQ ($2,200.00), Dominio y SSL ($950.00), DevOps ($2,400.00) = **$12,750.00 MXN**.
4. **Fondo de Reserva y Contingencia Operativa (10%):** **$38,025.00 MXN**.
- **Presupuesto Integral del Proyecto Monchis Café (Subtotal Neto antes de IVA):** **$418,275.00 MXN**.
