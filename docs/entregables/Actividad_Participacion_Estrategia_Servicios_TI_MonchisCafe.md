# UNIVERSIDAD DE GUADALAJARA
## CENTRO UNIVERSITARIO DE TONALÁ (CUTonalá)
### DIVISIÓN DE INGENIERÍAS E INNOVACIÓN TECNOLÓGICA
### LICENCIATURA EN INGENIERÍA EN COMPUTACIÓN

---

# ACTIVIDAD PARTICIPACIÓN: DISEÑO DE ESTRATEGIA DE SERVICIOS TI
### Cátedra: Gestión de Servicios Informáticos

* **Docente:** Dr. Gabriel Navarro Salcedo  
* **Proyecto Final:** Monchis Café — Plataforma Web y Sistema de Gestión para Cafetería de Especialidad  
* **Estudiante:** Ernesto Hatuey Fierro Medina (Código: 215487963)  
* **Rol:** Desarrollador y Gestor de Servicios TI  
* **Fecha de Entrega:** 17 de octubre de 2026  
* **Ciclo Escolar:** 2026-B  

---

# ÍNDICE GENERAL

1. Introducción y Marco de Gestión de Servicios TI
2. Desarrollo de la Estrategia de Servicios TI
   * 2.1. ¿Qué servicios debemos ofrecer? (Portafolio y Catálogo de Servicios)
   * 2.2. ¿Cuál es su valor? (Definición de Valor: Utilidad y Garantía)
   * 2.3. ¿Cuáles son los resultados esperados? (Metas Cualitativas y Cuantitativas)
   * 2.4. ¿Cuáles son nuestros clientes potenciales? (Segmentación y Perfiles de Mercado)
   * 2.5. ¿Qué servicios son prioritarios? (Matriz de Priorización Estratégica)
   * 2.6. ¿Qué inversiones son necesarias? (Presupuesto y Análisis de Costo Total de Propiedad)
   * 2.7. ¿Qué servicios existen en el mercado que representen competencia directa? (Benchmarking)
   * 2.8. ¿Cómo podemos diferenciarnos de la competencia? (Propuesta de Valor)
3. Articulación de la Estrategia en las Fases del Ciclo de Vida del Servicio TI (ITIL)
   * 3.1. Estrategia del Servicio (Service Strategy)
   * 3.2. Diseño del Servicio (Service Design)
   * 3.3. Transición del Servicio (Service Transition)
   * 3.4. Operación del Servicio (Service Operation)
   * 3.5. Mejora Continua del Servicio (Continual Service Improvement)
4. Conclusiones Generales
5. Referencias Bibliográficas

---

# 1. INTRODUCCIÓN Y MARCO DE GESTIÓN DE SERVICIOS TI

En las organizaciones contemporáneas, las tecnologías de información constituyen el medio fundamental para habilitar operaciones y generar valor. La Gestión de Servicios de Tecnologías de la Información (ITSM) define un marco para alinear la infraestructura y el software con las metas del negocio. La norma internacional ISO/IEC 20000-1 establece los requisitos de un sistema de gestión de servicios (International Organization for Standardization & International Electrotechnical Commission [ISO/IEC], 2018). Por su parte, la biblioteca ITIL en su edición 2011 estructura este enfoque a través de un ciclo de vida de cinco fases: Estrategia, Diseño, Transición, Operación y Mejora Continua del Servicio (Cabinet Office, 2011a–e). Es pertinente señalar que ITIL 4 evolucionó este modelo hacia el Sistema de Valor del Servicio (AXELOS, 2019); no obstante, para fines analíticos de este documento se adopta la estructura clásica por fases de ITIL 2011.

Este trabajo presenta la estrategia de servicios TI para Monchis Café. El proyecto corresponde a un escenario académico que modela una cafetería orientada al café de especialidad y al consumo sustentable. El sistema no se concibe como un software aislado, sino como un conjunto de servicios tecnológicos coordinados. Cada servicio busca facilitar la atención en mostrador, registrar la procedencia del grano y respaldar la sostenibilidad según los Objetivos de Desarrollo Sostenible (Organización de las Naciones Unidas [ONU], 2015). Dado que el establecimiento se encuentra en fase de desarrollo y no cuenta con métricas históricas de ventas ni tiempos de cobro en producción, los valores aquí expuestos se formulan como hipótesis técnicas y metas operativas preliminares.

---

# 2. DESARROLLO DE LA ESTRATEGIA DE SERVICIOS TI

A continuación se da respuesta a las ocho preguntas directrices para la formulación de la estrategia de servicios.

---

## 2.1. ¿QUÉ SERVICIOS DEBEMOS OFRECER?

Siguiendo el marco de catálogo de servicios de ITIL (Cabinet Office, 2011b) y la tipología de servicios (Cabinet Office, 2011d), la oferta se organiza en tres niveles: servicios principales (Core), servicios habilitadores (Enabling) y servicios de realce o soporte (Enhancing / Support). Esta división permite distinguir los componentes que interactúan con el usuario de aquellos que operan en segundo plano para garantizar la seguridad, resiliencia y continuidad operativa.

### Tabla 1. Catálogo de Servicios TI para Monchis Café

| Nivel de Servicio | Nombre del Servicio | Descripción Funcional Breve | Componente Técnico Base |
| :--- | :--- | :--- | :--- |
| **Principal (Core)** | Punto de Venta en Barra (POS) | Registro rápido de comandas, cobro mixto (efectivo, tarjeta bancaria y SPEI) y emisión de comprobantes. | Aplicación web en Vue 3, API en Node.js y lectores térmicos. |
| **Principal (Core)** | Trazabilidad de Café y Control PEPS | Registro de lotes de café (finca, altitud, tueste y caducidad) con rotación de primeras entradas y primeras salidas. | Modelos de datos en PostgreSQL mediante Prisma ORM y códigos QR. |
| **Principal (Core)** | Fidelización "Monchis Rewards" | Registro digital de consumos para otorgar bebidas de cortesía por acumulación (una bebida de cortesía al acumular 10 consumos registrados) y bonificaciones por uso de recipientes reusables. | Módulo de cliente en aplicación web y persistencia de saldos en base de datos. |
| **Habilitador (Enabling)** | Plataforma Cloud y Mensajería | Comunicación asíncrona de eventos de venta e inventario; transporte de mensajes para transacciones compensatorias. | Servidor en Google Cloud Platform (Compute Engine e2-medium, 4 GB RAM) y broker RabbitMQ. |
| **Habilitador (Enabling)** | Persistencia Transaccional | Almacenamiento relacional de compras, catálogo de insumos y auditoría de cambios de inventario. | Base de datos relacional PostgreSQL con restricciones de integridad referencial. |
| **Habilitador (Enabling)** | Seguridad de Acceso y Autenticación | Control de sesiones mediante tokens web, validación de formularios y segregación de perfiles por rol. | JSON Web Tokens (JWT) en cookies seguras, Google reCAPTCHA v3 y control RBAC alineado con los controles de acceso de ISO/IEC 27001 (ISO/IEC, 2022). |
| **Soporte (Support / Enhancing)** | Mesa de Ayuda Técnica | Atención y diagnóstico de fallas en terminales de cobro, lectores de códigos e impresoras. | Canal de reporte técnico con atención en sitio y asistencia remota para el personal. |
| **Soporte (Support / Enhancing)** | Continuidad y Respaldos | Copias periódicas de seguridad de la base de datos y procedimiento documentado de restauración. | Tareas programadas de volcado de datos con almacenamiento externo en la nube. |
| **Soporte (Support / Enhancing)** | Monitoreo de Disponibilidad | Supervisión de rutas de verificación (/api/health) y estado de colas de mensajería pendientes. | Scripts de sondeo de estado con notificaciones de alerta técnica vía SMTP. |

*Criterios de selección:*
- El **Punto de Venta** es el servicio crítico para el negocio. Su diseño responde a la necesidad de no retrasar la fila de pedidos matutinos.
- La **Trazabilidad de Café** materializa la propuesta de valor del negocio. Permite verificar ante el cliente que el grano proviene de cooperativas regionales.
- La **Fidelización** estimula la retención de comensales frecuentes (Reichheld & Sasser, 1990) y apoya la reducción de vasos desechables (ONU, 2015, ODS 12).
- La **Plataforma Cloud y Mensajería** aísla tareas asíncronas pesadas. Cuando ocurre un pedido simultáneo y se detecta agotamiento de insumo, el orquestador de la Saga ejecuta transacciones compensatorias mientras RabbitMQ transporta los mensajes correspondientes. La selección de la máquina virtual e2-medium (4 GB de RAM) responde a los requerimientos oficiales de RabbitMQ para producción (RabbitMQ, 2026), garantizando margen suficiente para el runtime de Erlang y la API de Node.js.
- La **Persistencia** y la **Seguridad de Acceso** protegen la información transaccional y los datos personales alineados con los controles de ISO/IEC 27001 (ISO/IEC, 2022) y conforme a la legislación aplicable (Cámara de Diputados del H. Congreso de la Unión, 2025).
- La **Mesa de Ayuda**, los **Respaldos** y el **Monitoreo** conforman la red de protección operativa que previene interrupciones prolongadas en las jornadas de venta.

---

## 2.2. ¿CUÁL ES SU VALOR?

En el marco ITIL, el valor se define como el conjunto de beneficios percibidos por el cliente al alcanzar sus objetivos. Este valor se compone de dos elementos indispensables: la Utilidad (*Fit for Purpose*, adecuación para el propósito) y la Garantía (*Fit for Use*, adecuación para el uso) (Cabinet Office, 2011d). Ningún servicio genera valor real si ofrece utilidad sin garantía, o si cuenta con garantías técnicas pero carece de utilidad práctica para el negocio.

### Tabla 2. Desglose de Valor: Utilidad frente a Garantía

| Dimensión de Valor | Concepto ITIL | Aplicación Concreta en Monchis Café | Beneficio Operativo Esperado |
| :--- | :--- | :--- | :--- |
| **Utilidad** (*Fit for Purpose*) | Qué hace el servicio; eliminación de restricciones operativas. | Captura táctil de pedidos con cálculo inmediato de cambio y cobro integrado. | Reduce tiempos de espera en mostrador y simplifica el registro de comandas para los baristas. |
| **Utilidad** (*Fit for Purpose*) | Soporte al desempeño del negocio. | Control estricto de rotación PEPS (primeras entradas, primeras salidas) de café en grano. | Se propone como meta evitar que los lotes de café de especialidad pierdan frescura o caduquen en bodega. |
| **Utilidad** (*Fit for Purpose*) | Fidelización y sustentabilidad activa. | Registro digital de visitas y bonificación fija por traer termo reutilizable. | Estimula la recompra regular y apoya el consumo responsable de acuerdo con el ODS 12 (ONU, 2015). |
| **Garantía** (*Fit for Use*) | Disponibilidad del servicio. | Arquitectura contenerizada sobre máquina virtual con respaldos diarios. | Meta de disponibilidad de 99.5 % durante el horario de atención comercial (lunes a sábado). |
| **Garantía** (*Fit for Use*) | Capacidad y desempeño. | Peticiones optimizadas en monorepo web y separación de colas de mensajes. | Tiempo de respuesta en pantalla ≤ 450 ms (P95) en red local bajo carga típica del POS. |
| **Garantía** (*Fit for Use*) | Continuidad operativa. | Respaldos diarios programados de la base de datos relacional. | Objetivo de Tiempo de Recuperación (RTO) ≤ 45 minutos; Objetivo de Punto de Recuperación (RPO) ≤ 24 horas, delimitando el volumen máximo de datos transaccionales en riesgo. |
| **Garantía** (*Fit for Use*) | Seguridad de la información. | Autenticación stateless con JWT, cookies seguras httpOnly y roles RBAC alineado con los controles de acceso de ISO/IEC 27001 (ISO/IEC, 2022). | Previene modificaciones no autorizadas en precios, cortes de caja o datos personales de clientes (Cámara de Diputados del H. Congreso de la Unión, 2025). |

*Aportes esperados a la operación:*  
El valor de la utilidad se refleja en la fluidez del mostrador. Se establece como supuesto operativo de partida un tiempo estimado de cobro actual de 120 segundos, proyectando reducirlo a ≤ 75 segundos con la interfaz táctil. Esto habilitaría un incremento potencial de hasta 60 % en la capacidad teórica de despacho en horas de mayor afluencia. En cuanto a la continuidad, es indispensable diferenciar entre RTO y RPO: el RTO define el tiempo máximo para restaurar el servicio tras una caída (≤ 45 minutos), mientras que el RPO delimita la antigüedad máxima de los datos que se perderían ante un fallo crítico (≤ 24 horas mediante copias diarias).

---

## 2.3. ¿CUÁLES SON LOS RESULTADOS ESPERADOS?

Para que la estrategia sea verificable conforme a los principios de mejora continua (Cabinet Office, 2011a), se definen metas cuantitativas y cualitativas vinculadas a Factores Críticos de Éxito (CSF) e Indicadores Clave de Desempeño (KPI). Puesto que el proyecto se encuentra en etapa de diseño académico, estos valores representan metas operativas formuladas por el autor y sujetas a validación empírica en pruebas de campo.

### Tabla 3. Matriz de Resultados y Metas Operativas Propuestas

| Dimensión de Servicio | Factor Crítico de Éxito (CSF) | Indicador Clave de Desempeño (KPI) | Meta Cuantitativa Propuesta | Meta Cualitativa Esperada |
| :--- | :--- | :--- | :--- | :--- |
| **Atención en Barra** | Agilidad en el registro de la orden. | Tiempo promedio de captura y cobro por pedido en mostrador. | Meta: ≤ 75 segundos por cliente en pedidos estándar. | Sensación de fluidez en el servicio; disminución del estrés para el cajero. |
| **Desempeño Técnico** | Rapidez de respuesta de la aplicación web. | Latencia de respuesta en endpoints del POS (percentil 95). | Meta: ≤ 450 ms (P95) en red local bajo carga típica del POS. | Interacción táctil ágil sin bloqueos perceptibles en la pantalla. |
| **Disponibilidad** | Continuidad durante el horario de servicio. | Porcentaje de tiempo operativo en horario comercial (08:00 a 20:00). | Meta: ≥ 99.5 % mensual (≈ 94 minutos máximos de interrupción tolerados al mes). | Confianza del personal de que la terminal responderá en turnos clave. |
| **Fiabilidad Transaccional** | Consistencia entre inventario y ventas. | Tasa de órdenes con discrepancia no compensada tras corte mensual. | Meta: < 0.1 % de transacciones del periodo evaluado. | Disminución de quejas por cobro de bebidas con ingredientes agotados. |
| **Fidelización** | Participación en el programa de lealtad. | Proporción de clientes frecuentes registrados en Monchis Rewards. | Meta: ≥ 30 % de comensales recurrentes en 3 meses. | Vínculo de identidad con el establecimiento y sentido de trato preferencial. |
| **Sostenibilidad** | Reducción de envases de un solo uso (ODS 12). | Porcentaje de cafés servidos en taza de loza o termo del cliente. | Meta inicial: ≥ 20 % del total de bebidas preparadas. | Percepción de Monchis Café como un proyecto con responsabilidad ambiental. |
| **Soporte Técnico** | Restablecimiento ante fallas de hardware local. | Tiempo medio de reparación ante incidentes en mostrador (MTTR). | Meta: ≤ 45 minutos en promedio durante el horario comercial. | Respuesta organizada ante atascos de impresión o pérdida de red, coherente con el RTO ≤ 45 min definido en continuidad. |

*Traducción de disponibilidad operativa:*  
La meta de 99.5 % de disponibilidad en horario comercial (lunes a sábado de 08:00 a 20:00, 12 horas diarias por 26 días laborables al mes = 312 horas comerciales) se traduce en un margen máximo de indisponibilidad tolerada de aproximadamente 94 minutos al mes:  
$$\text{Minutos tolerados} = (1 - 0.995) \times 312 \text{ h} \times 60 \text{ min/h} = 0.005 \times 18{,}720 \text{ min} = 93.6 \approx 94 \text{ min/mes}$$  
Considerando un MTTR ≤ 45 minutos, este indicador tolera como máximo dos incidentes de severidad alta durante el mes sin incumplir el nivel de servicio acordado.

---

## 2.4. ¿CUÁLES SON NUESTROS CLIENTES POTENCIALES?

La estrategia de servicios distingue a los usuarios finales y a los beneficiarios directos del sistema en cuatro segmentos principales, formulados como hipótesis del autor sujetas a confirmación comercial:

1. **Comensales de café de especialidad y profesionales independientes (Clientes externos):**  
   Personas con interés en el café artesanal, estudiantes universitarios y trabajadores remotos. Se formula la hipótesis de que el grupo principal de usuarios oscilará entre los 20 y los 50 años de edad. Demandan métodos de pago flexibles (tarjeta física o digital, transferencias bancarias), rapidez en la entrega del ticket y acceso transparente a la ficha del café (origen, cooperativa y fecha de tueste) mediante lectura de código QR.
2. **Aliados y proveedores: cooperativas cafetaleras y productores locales (Socios de la cadena de suministro):**  
   Pequeños productores y organizaciones agrícolas regionales que suministran café en grano sustentable. Requieren que el sistema preserve los datos de origen de su grano para evitar que su identidad de marca se diluya en mezclas genéricas.
3. **Personal operativo de barra y administración (Clientes internos):**  
   Baristas y personal de caja responsables de tomar órdenes y preparar bebidas. Precisan una interfaz limpia, botones de gran tamaño para evitar errores de selección, confirmaciones visuales claras de cobro y cuadres de turno automatizados.
4. **Pequeñas cafeterías independientes (Potencial de transferencia tecnológica):**  
   Micronegocios del ramo de alimentos y bebidas de una o dos sucursales en ciudades intermedias que podrían estar limitados por las cuotas o la rigidez de sistemas comerciales cerrados. Buscan una solución tecnológica modular y accesible que no imponga comisiones excesivas ni módulos innecesarios para su escala de operación.

---

## 2.5. ¿QUÉ SERVICIOS SON PRIORITARIOS?

Para ordenar el desarrollo e implantación de los servicios, se elaboró una matriz de priorización cuantitativa. Cada servicio propuesto se evaluó en una escala de 1 a 5 en cuatro criterios ponderados: **Impacto en el Negocio** (peso 35 %), **Urgencia Operativa** (peso 25 %), **Viabilidad Técnica** (peso 25 %) y **Menor Riesgo** (peso 15 %, donde 5 representa menor riesgo percibido y 1 riesgo alto).

Fórmula de ponderación: Puntaje Total = (Impacto × 0.35) + (Urgencia × 0.25) + (Viabilidad × 0.25) + (Menor Riesgo × 0.15)

**Umbrales de clasificación estratégica:**
- **P1 (Crítica):** Puntaje Total ≥ 4.50
- **P2 (Alta):** Puntaje Total de 3.90 a 4.49
- **P3 (Media):** Puntaje Total de 3.75 a 3.89
- **P4 (Soporte):** Puntaje Total < 3.75

### Tabla 4. Matriz de Priorización Cuantitativa de Servicios TI
*(Filas ordenadas de mayor a menor puntaje ponderado)*

| Servicio Evaluado | Impacto (1–5) | Urgencia (1–5) | Viabilidad (1–5) | Menor Riesgo (1–5) | Puntaje Total | Cálculo Ponderado Detallado | Nivel de Prioridad | Fase / Sprints / Semanas |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :---: | :---: |
| **Punto de Venta en Barra (POS)** | 5.0 | 5.0 | 4.5 | 4.0 | **4.73** | $(5.0 	imes 0.35) + (5.0 	imes 0.25) + (4.5 	imes 0.25) + (4.0 	imes 0.15) = 1.75 + 1.25 + 1.125 + 0.60 = 4.725$ | **P1 (Crítica)** | Fase 1 / Sprints 1–2 / Sem. 1–4 |
| **Persistencia Transaccional** | 5.0 | 5.0 | 4.5 | 3.5 | **4.65** | $(5.0 	imes 0.35) + (5.0 	imes 0.25) + (4.5 	imes 0.25) + (3.5 	imes 0.15) = 1.75 + 1.25 + 1.125 + 0.525 = 4.650$ | **P1 (Crítica)** | Fase 1 / Sprints 1–2 / Sem. 1–3 |
| **Seguridad de Acceso y Autenticación** | 5.0 | 4.5 | 4.5 | 4.0 | **4.60** | $(5.0 	imes 0.35) + (4.5 	imes 0.25) + (4.5 	imes 0.25) + (4.0 	imes 0.15) = 1.75 + 1.125 + 1.125 + 0.60 = 4.600$ | **P1 (Crítica)** | Fase 1 / Sprints 1–2 / Sem. 2–4 |
| **Trazabilidad de Café y Control PEPS** | 4.5 | 4.0 | 4.0 | 3.5 | **4.10** | $(4.5 	imes 0.35) + (4.0 	imes 0.25) + (4.0 	imes 0.25) + (3.5 	imes 0.15) = 1.575 + 1.00 + 1.00 + 0.525 = 4.100$ | **P2 (Alta)** | Fase 2 / Sprints 3–4 / Sem. 5–8 |
| **Fidelización "Monchis Rewards"** | 4.0 | 3.0 | 4.5 | 4.5 | **3.95** | $(4.0 	imes 0.35) + (3.0 	imes 0.25) + (4.5 	imes 0.25) + (4.5 	imes 0.15) = 1.40 + 0.75 + 1.125 + 0.675 = 3.950$ | **P2 (Alta)** | Fase 2 / Sprints 3–4 / Sem. 7–8* |
| **Plataforma Cloud y Mensajería** | 4.0 | 4.0 | 4.0 | 3.5 | **3.93** | $(4.0 	imes 0.35) + (4.0 	imes 0.25) + (4.0 	imes 0.25) + (3.5 	imes 0.15) = 1.40 + 1.00 + 1.00 + 0.525 = 3.925$ | **P2 (Alta)** | Fase 2 / Sprints 3–4 / Sem. 5–7 |
| **Continuidad y Respaldos** | 4.0 | 3.5 | 4.0 | 4.0 | **3.88** | $(4.0 	imes 0.35) + (3.5 	imes 0.25) + (4.0 	imes 0.25) + (4.0 	imes 0.15) = 1.40 + 0.875 + 1.00 + 0.60 = 3.875$ | **P3 (Media)** | Fase 3 / Sprints 5–6 / Sem. 9–11 |
| **Mesa de Ayuda Técnica** | 3.5 | 4.0 | 4.0 | 4.0 | **3.83** | $(3.5 	imes 0.35) + (4.0 	imes 0.25) + (4.0 	imes 0.25) + (4.0 	imes 0.15) = 1.225 + 1.00 + 1.00 + 0.60 = 3.825$ | **P3 (Media)** | Fase 3 / Sprints 5–6 / Sem. 10–12 |
| **Monitoreo de Disponibilidad** | 3.5 | 3.5 | 4.0 | 4.0 | **3.70** | $(3.5 	imes 0.35) + (3.5 	imes 0.25) + (4.0 	imes 0.25) + (4.0 	imes 0.15) = 1.225 + 0.875 + 1.00 + 0.60 = 3.700$ | **P4 (Soporte)** | Fase 4 / Sprints 7–8 / Sem. 13–16 |

*Dependencias técnicas del orden de despliegue:*  
Aunque el módulo de Fidelización (3.95) obtiene un puntaje cuantitativo ligeramente superior a Plataforma Cloud y Mensajería (3.93), el programa Rewards requiere que la mensajería asíncrona y la orquestación de transacciones de la Saga se encuentren previamente operativas para registrar bonificaciones sin inconsistencias. Por tal motivo, la Plataforma Cloud se implementa con antelación dentro de la Fase 2. Del mismo modo, la Persistencia Transaccional (4.65) se programa en la Fase 1 (Semanas 1–3) por constituir la base de datos relacional requerida por el Punto de Venta, mientras que Continuidad y Respaldos (3.88) se ubica en la Fase 3 una vez estabilizada la persistencia de datos.

*Criterio de puntajes extremos:*  
El Punto de Venta en Barra obtuvo el puntaje más alto (4.73, P1) debido a que sin él resulta imposible procesar cobros y operar comercialmente. Por el contrario, el Monitoreo de Disponibilidad obtuvo la calificación más baja (3.70, P4) por constituir una disciplina de maduración técnica transversal cuya configuración fina se consolida de manera incremental tras el despliegue de los servicios sustantivos.

*Estructura del calendario en 16 semanas y 8 sprints:*  
El cronograma de 16 semanas se organiza en 8 sprints de dos semanas de duración:
- **Fase 1 (Sprints 1–2, Semanas 1–4):** Servicios críticos P1 (Persistencia Transaccional, POS en Barra y Seguridad de Acceso y Autenticación).
- **Fase 2 (Sprints 3–4, Semanas 5–8):** Servicios P2 (Plataforma Cloud y Mensajería, Trazabilidad de Café y Control PEPS, y Fidelización "Monchis Rewards").
- **Fase 3 (Sprints 5–6, Semanas 9–12):** Servicios P3 (Continuidad y Respaldos, y Mesa de Ayuda Técnica).
- **Fase 4 (Sprints 7–8, Semanas 13–16):** Pruebas integrales en sitio, capacitación formal, Monitoreo de Disponibilidad (P4) y protocolos de contingencia.

---

## 2.6. ¿QUÉ INVERSIONES SON NECESARIAS?

La infraestructura tecnológica para habilitar los servicios requiere recursos financieros divididos en inversión inicial de capital (CAPEX) y costos de operación recurrente (OPEX). El presupuesto considera dos estaciones de trabajo (caja y preparación de comandas) para la operación en producción.

### Tabla 5. Presupuesto Detallado de Inversión Inicial (CAPEX) y Operación Mensual (OPEX)
*(Precios estimados a octubre de 2026; tipo de cambio de referencia: $20.00 MXN/USD)*

| Rubro de Inversión | Descripción del Bien o Servicio | Tipo | Costo Inicial (CAPEX) | Costo Mensual (OPEX) | Justificación Técnica y Fuentes de Consulta |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Hardware de Barra** | 2 tabletas Samsung Galaxy Tab A9+ (11.0", 8 GB RAM) con base fija de seguridad | CAPEX | $11,600 MXN* | $0 MXN | Terminales táctiles de mostrador para caja y comanderas de baristas: 2 tabletas de ~$4,200 MXN* c/u ($8,400 MXN*) + 2 bases metálicas de mostrador de ~$1,600 MXN* c/u ($3,200 MXN*). Fichas en retailers México (Walmart/Mercado Libre), octubre de 2026. |
| **Periféricos de Cobro** | 2 impresoras térmicas de 80 mm (USB/Ethernet) y 2 lectores ópticos de códigos 2D con base | CAPEX | $7,400 MXN* | $0 MXN | Emisión de tickets y escaneo de códigos QR de lotes: ~$2,200 MXN* por impresora + ~$1,500 MXN* por lector. Precios de mercado de cómputo en México, octubre de 2026. |
| **Infraestructura Cloud** | Máquina virtual Google Compute Engine e2-medium (2 vCPU compartidas, 4 GB RAM, 20 GB SSD) | OPEX | $0 MXN | $600 MXN* (~$30 USD/mes) | Aloja la API y RabbitMQ. La guía oficial de RabbitMQ recomienda un mínimo de 4 GiB de RAM por nodo para producción (RabbitMQ, 2026). La instancia e2-medium se adopta como configuración mínima para carga piloto (dos estaciones, un solo nodo, sin clúster), limitando la memoria de RabbitMQ y supervisando su consumo junto a la API. Calculadora oficial GCP (Google Cloud, 2026). |
| **Base de Datos Cloud** | Instancia PostgreSQL administrada Cloud SQL (nivel db-f1-micro, vCPU compartida, 0.6 GB RAM, 10 GB SSD) | OPEX | $0 MXN | $450 MXN* (~$22.50 USD/mes) | Almacenamiento transaccional ACID de ventas, inventarios y auditoría con respaldos diarios automáticos en la región us-central1 (Iowa). Tarifa oficial Cloud SQL (Google Cloud, 2026). |
| **Red y Dominio** | Registro y renovación anual de dominio .com.mx y servicios DNS/TLS en Cloudflare | CAPEX/OPEX | $680 MXN* (año 1) | $0 MXN | Nombre de red y certificados HTTPS (Cloudflare plan gratuito $0 MXN). Renovación anual en Akky / NIC México (~$680 MXN/año; renovaciones de años 2 y 3 incorporadas en el TCO). |
| **Mensajería Transaccional** | Servicio de pasarela SMTP transaccional para notificaciones y alertas | OPEX | $0 MXN | $200 MXN* (~$10 USD/mes) | Envío de alertas automatizadas del orquestador y comprobantes digitales mediante plan transaccional básico de referencia (como SendGrid Essentials o Amazon SES). |
| **Capacitación Operativa** | Talleres prácticos para personal de barra sobre el POS y contingencias | CAPEX | $3,000 MXN* | $0 MXN | Instrucción operativa en apertura de caja, captura de comandas y sustitución de rollos térmicos. |
| **Soporte y Mantenimiento** | Soporte técnico Nivel 1/2, parches y mantenimiento preventivo | OPEX | $0 MXN | $0 MXN (interno)* | El soporte técnico Nivel 1/2 y el mantenimiento preventivo son cubiertos internamente por el desarrollador y equipo sin costo adicional en el esquema propuesto. En un entorno comercial externo, una póliza técnica mensual equivalente se estima como referencia en ~$3,600 MXN/mes*. |
| **Fondo de Contingencia** | Reserva para reemplazo urgente de periféricos o enlace móvil 4G de respaldo | CAPEX | $3,500 MXN* | $0 MXN | Mitigación ante averías mecánicas o interrupciones locales en el enlace a internet. |
| **TOTALES** | **Inversión Inicial y Gasto Operativo Mensual** | — | **$26,180 MXN** | **$1,250 MXN / mes** | **Presupuesto base estimado a precios de mercado de octubre de 2026.** |

*\* Valor estimado de referencia; sujeto a verificación mediante cotización formal.*

*Resumen de operaciones financieras:*  
- **CAPEX total inicial:** $\$11{,}600 	ext{ (tabletas)} + \$7{,}400 	ext{ (periféricos)} + \$680 	ext{ (dominio año 1)} + \$3{,}000 	ext{ (capacitación)} + \$3{,}500 	ext{ (contingencia)} = \mathbf{\$26{,}180 	ext{ MXN}}$.  
- **OPEX mensual regular:** $\$600 	ext{ (Compute Engine e2-medium)} + \$450 	ext{ (Cloud SQL)} + \$200 	ext{ (SMTP)} + \$0 	ext{ (soporte interno)} = \mathbf{\$1{,}250 	ext{ MXN/mes}}$.

### Análisis Comparativo de Costo Total de Propiedad (TCO a 3 Años)

Para evaluar la viabilidad financiera, se proyecta el Costo Total de Propiedad a un horizonte de 36 meses. El cálculo incluye el CAPEX inicial, 36 mensualidades de OPEX y la renovación anual del dominio para los años 2 y 3 ($680 MXN cada año):

$$\text{TCO Monchis Café (3 años)} = \text{CAPEX} + (36 \times \text{OPEX mensual}) + (2 \times \text{Renovación dominio})$$
$$\text{TCO Monchis Café} = \$26{,}180 + (36 \times \$1{,}250) + (\$680 \times 2) = \$26{,}180 + \$45{,}000 + \$1{,}360 = \mathbf{\$72{,}540 \text{ MXN}}$$

*Declaración sobre el esfuerzo de desarrollo y soporte externo:*  
El cálculo anterior excluye deliberadamente el costo del esfuerzo humano de desarrollo de software por tratarse de un proyecto académico formativo no facturado al cliente. Si se cotizara comercialmente el desarrollo inicial (estimado en 680 horas equivalentes a una célula de 2 desarrolladores a medio tiempo durante 16 semanas × $320 MXN/h* = $217,600 MXN*), el TCO total ascendería a $290,140 MXN. Asimismo, si se contratara una póliza de soporte externo estimada en $3,600 MXN/mes* ($129,600 MXN en 36 meses), el TCO operativo comercial alcanzaría los $202,140 MXN (o $419,740 MXN incluyendo desarrollo inicial).

### Tabla 6. Comparativa de Costo Total de Propiedad a 3 Años (2 Estaciones, 36 Meses)
*(Cifras en pesos mexicanos MXN; precios vigentes en 2026 consultados en fuentes oficiales; tipo de cambio: $20.00 MXN/USD)*

| Concepto de Costo | Soft Restaurant 12 Pro (National Soft, 2026) | Loyverse POS (Loyverse, 2026) | Monchis Café (Desarrollo Propio) |
| :--- | :--- | :--- | :--- |
| **Hardware inicial (2 estaciones)** | $23,000 MXN* (1 terminal/PC Windows para caja + 1 tableta comandera Android + 2 impresoras y lectores) | $19,000 MXN* (2 tabletas Android + 2 impresoras y 2 lectores 2D) | $19,000 MXN* (2 tabletas Android + 2 impresoras y 2 lectores 2D incluidos en CAPEX) |
| **Licenciamiento / Suscripción / Cloud** | $45,900 MXN* ($1,099 + IVA = $1,274.84 MXN/mes redondeado a $1,275 MXN/mes por sucursal × 36 meses) | $32,400 MXN (Inventario Avanzado $25 USD + Gestión de 4 Empleados $20 USD = $45 USD/mes = $900 MXN/mes × 36 meses) | $0 MXN de licencia privativa ($45,000 MXN de servicios cloud en 36 meses a $1,250 MXN/mes) |
| **Soporte y Capacitación** | Soporte de marca incluido en suscripción; capacitación e implementación inicial estimada en ~$6,500 MXN* | Soporte básico en línea por chat incluido ($0 MXN) o póliza técnica local externa estimada en $54,000 MXN* ($1,500 MXN/mes* × 36 meses) | $0 MXN en soporte (asumido internamente por el desarrollador/equipo) + $3,000 MXN* de capacitación inicial en CAPEX |
| **Dominio y Contingencia** | N/A (plataforma hospedada por el proveedor) | N/A (plataforma hospedada por el proveedor) | $5,540 MXN ($680 año 1 en CAPEX + $1,360 renovaciones años 2 y 3 + $3,500 de fondo de contingencia en CAPEX) |
| **TCO Estimado a 3 Años** | **~$75,400 MXN*** | **$51,400 a $105,400 MXN*** (según soporte técnico externo) | **$72,540 MXN** (con soporte interno y desarrollo académico excluido) |

*\* Valor estimado de referencia; sujeto a verificación mediante cotización formal. Las comisiones por adquirencia bancaria se consideran idénticas e independientes del software en las tres opciones.*

*Conclusión del análisis financiero:*  
Con soporte técnico cubierto internamente y sin facturar horas de desarrollo de software, Monchis Café resulta altamente competitivo en términos financieros brutos ($72,540 MXN frente a ~$75,400 MXN de Soft Restaurant 12 Pro y $51,400 a $105,400 MXN de Loyverse POS). Su valor de negocio radica en tres ventajas estratégicas:
1. **Alineación funcional exacta:** Incorporación nativa de trazabilidad de lotes por cooperativa campesina, rotación PEPS estricta y compensación automática de ventas agotadas mediante la Saga.
2. **Soberanía y propiedad de datos:** Monchis Café mantiene el control directo sobre sus bases de datos transaccionales y de clientes, eliminando dependencias de plataformas privativas cerradas.
3. **Sostenibilidad integrada:** La vinculación con el ODS 12 y los incentivos por consumo responsable se integran directamente en la lógica del sistema.

---

## 2.7. ¿QUÉ SERVICIOS EXISTEN EN EL MERCADO QUE REPRESENTEN COMPETENCIA DIRECTA?

En el mercado mexicano coexisten diversas alternativas de software para el sector de alimentos y bebidas. Para establecer un marco de comparación realista, se seleccionaron dos opciones comerciales de punto de venta comercializadas activamente en México en 2026 frente a la propuesta propia:

1. **Soft Restaurant 12 (National Soft, 2026):** Solución con amplia trayectoria en el mercado mexicano para restaurantes y cafeterías medianas. En 2026 opera bajo suscripción mensual con soporte y actualizaciones continuas: Plan Lite ($799 MXN + IVA/mes), Plan Pro ($1,099 MXN + IVA/mes) y SR Cloud (desde $699 MXN + IVA/mes por estación) (National Soft, 2026). Requiere conexión continua para sincronización de ventas en la nube, aunque cuenta con almacenamiento local en caso de cortes temporales.
2. **Loyverse POS (Loyverse, 2026):** Aplicación móvil en la nube utilizada con frecuencia por pequeñas cafeterías en México. Ofrece una aplicación base gratuita ($0 MXN); cobra $25 USD/mes (~$500 MXN) por tienda para el módulo de Inventario Avanzado y $5 USD/mes (~$100 MXN) por colaborador para el módulo de Gestión de Empleados (Loyverse, 2026). Su documentación oficial señala que el modo sin conexión permite registrar ventas e imprimir comandas en local, pero suspende temporalmente los reembolsos, el alta de nuevos clientes y la validación de inventario negativo hasta restablecer la conexión a internet.

### Tabla 7. Cuadro Comparativo de Soluciones de Punto de Venta en México

| Parámetro Comparativo | Soft Restaurant 12 (National Soft, 2026) | Loyverse POS (Loyverse, 2026) | Propuesta "Monchis Café" (Estrategia Propia) |
| :--- | :--- | :--- | :--- |
| **Esquema de Precios** | Suscripción mensual: Lite $799 + IVA; Pro $1,099 + IVA; SR Cloud desde $699 + IVA/mes por sucursal. | Base gratuita; Inventario Avanzado $25 USD/mes/tienda; Gestión de Empleados $5 USD/mes/empleado ($20 USD para 4 colaboradores). | CAPEX $26,180 MXN + OPEX $1,250 MXN/mes (servidores cloud, base de datos administrada y SMTP; soporte interno). |
| **Trazabilidad de Café Orgánico** | No documenta en su catálogo oficial módulos de altitud, fincas ni perfil de tueste. | Maneja inventario general de insumos; no registra datos agrícolas ni rotación PEPS por lote. | **Propuesta:** Registro nativo de cooperativa, finca, altitud, fecha de tostado, PEPS y código QR al cliente. |
| **Modo Sin Conexión** | Permite operar en disco local; requiere internet para sincronizar SR Cloud y facturación. | Registra ventas y turnos offline; suspende reembolsos, nuevos clientes y alertas de stock negativo. | **Propuesta:** Modo degradado de mostrador con notas de contingencia para captura continua. |
| **Resiliencia de Transacciones** | Arquitectura cliente-servidor tradicional sobre base de datos relacional local o remota. | Dependiente de conexión a la nube; sin orquestación de transacciones distribuidas. | **Propuesta:** Orquestador de la Saga con transacciones compensatorias transportadas por RabbitMQ. |
| **Sostenibilidad y Lealtad** | Módulos de lealtad comercial tradicionales disponibles como complemento de pago. | Sistema básico de puntos y descuentos configurable en panel web. | **Propuesta:** Sellos digitales y bonificación fija por taza o termo reusable (ODS 12). |
| **Presencia y Soporte Local** | Soporte técnico de marca incluido en suscripción y red de distribuidores autorizados. | Soporte en línea mediante chat y foros comunitarios en español. | **Propuesta:** Mesa de ayuda estructurada con acuerdos internos de nivel de servicio (SLA/SLO propuestos). |

*Nota aclaratoria sobre Monchis Café:* Las capacidades señaladas como "Propuesta" corresponden a especificaciones de diseño técnico formuladas en este proyecto que aún no han sido validadas en operación continua en producción.

---

## 2.8. ¿CÓMO PODEMOS DIFERENCIARNOS DE LA COMPETENCIA?

La propuesta de Monchis Café no busca competir en volumen generalista de funcionalidades frente a sistemas masivos, sino concentrarse en resolver las necesidades específicas de una cafetería de especialidad mediante cuatro factores diferenciadores:

1. **Especialización en la cadena de valor del café sustentable (ODS 12):**  
   Los sistemas convencionales manejan el café como un insumo estandarizado. Monchis Café incorpora en su modelo de datos los atributos del café de especialidad: nombre de la finca, cooperativa campesina proveedora, fecha de cosecha y días de reposo pos-tueste. Al asociar estos datos a un código QR impreso en el recibo o visible en pantalla, el cliente puede corroborar el origen de su bebida. Asimismo, la bonificación por recipiente reutilizable premia directamente conductas de menor impacto ambiental.
2. **Consistencia transaccional mediante Patrón Saga:**  
   En momentos de alta concurrencia en mostrador, es factible que un comensal pague una bebida mientras el último lote del grano seleccionado se agota en otra terminal. En lugar de generar discrepancias contables o fricciones en barra, el orquestador de la Saga ejecuta de inmediato una compensación controlada, informando con precisión al cajero para que reoriente la orden o emita la reversa sin contratiempos.
3. **Independencia operativa y soberanía de los datos:**  
   Al operar sobre una base de datos propia en la nube, el establecimiento no queda sujeto a comisiones transaccionales obligatorias de software privativo ni a incrementos imprevistos en suscripciones mensuales. Monchis Café mantiene un control directo sobre la base de datos de ventas, consumos y perfiles de comensales.
4. **Soporte técnico cercano y preventivo:**  
   La asistencia técnica para el personal de mostrador se estructura con acuerdos internos de nivel de servicio (SLA/SLO propuestos) y protocolos documentados de contingencia física, reduciendo la incertidumbre ante averías mecánicas o problemas de red en horas pico de venta.

---

# 3. ARTICULACIÓN DE LA ESTRATEGIA EN LAS FASES DEL CICLO DE VIDA DEL SERVICIO TI (ITIL)

La gestión de servicios requiere que cada etapa del ciclo de vida esté articulada con las demás. A continuación se describe cómo intervienen las cinco fases establecidas por ITIL 2011 (Cabinet Office, 2011a–e) en el proyecto Monchis Café:

### 3.1. Estrategia del Servicio (*Service Strategy*)
Esta fase define los lineamientos para que la tecnología genere valor genuino para el negocio (Cabinet Office, 2011d). En Monchis Café se definen:
- **Gestión del Portafolio:** Se clasifica el catálogo de servicios activos (POS, Trazabilidad, Lealtad) frente a los servicios que permanecerán en el flujo de desarrollo futuro (pedidos móviles anticipados).
- **Gestión Financiera de TI:** Se proyecta la estructura de costos (CAPEX y OPEX a tres años) y se evalúa el TCO frente a alternativas comerciales para asegurar la viabilidad económica del proyecto.
- **Gestión de la Demanda:** Se analiza la demanda para anticipar los picos de mostrador en turnos matutinos (08:30 a 11:00) y vespertinos (17:00 a 19:30).

### 3.2. Diseño del Servicio (*Service Design*)
Esta fase traduce los requisitos estratégicos en especificaciones técnicas, arquitecturas y acuerdos formales (Cabinet Office, 2011b):
- **Gestión de Niveles de Servicio (SLM):** Se definen los acuerdos internos de nivel de servicio (SLA/SLO propuestos) para fijar una disponibilidad operativa del 99.5 % durante el horario comercial y tiempos de atención técnica según la severidad del incidente.
- **Gestión de la Capacidad:** Se dimensionan los requerimientos de cómputo en la máquina virtual e2-medium (4 GB RAM) de Google Cloud y la concurrencia admisible en RabbitMQ para asegurar que la latencia en transacciones de mostrador no exceda ≤ 450 ms (P95) en red local.
- **Gestión de Proveedores:** Se establecen criterios de evaluación para proveedores críticos de infraestructura en la nube (GCP) y pasarelas de pago, supervisando sus compromisos de tiempo en línea y comisiones.
- **Gestión de Seguridad de la Información:** Se incorporan lineamientos alineados con los controles de ISO/IEC 27001 (ISO/IEC, 2022), incluyendo autenticación stateless mediante JWT en cookies protegidas, validación anti-bot y esquemas RBAC.
- **Gestión de la Continuidad del Servicio de TI (ITSCM):** Se establecen los parámetros de continuidad operativa: un Objetivo de Tiempo de Recuperación (RTO) ≤ 45 minutos y un Objetivo de Punto de Recuperación (RPO) ≤ 24 horas, respaldados por copias diarias automatizadas de la base de datos relacional y un plan de acción local con notas manuales de contingencia.

### 3.3. Transición del Servicio (*Service Transition*)
Esta fase garantiza que los servicios nuevos o modificados se liberen en el entorno operativo sin causar interrupciones inesperadas (Cabinet Office, 2011e):
- **Gestión de Cambios (*Change Enablement*):** Cada actualización del código en el monorepo se somete a revisión técnica mediante pull requests y pruebas de integración antes de incorporarse a la rama principal.
- **Gestión de Liberación y Despliegue:** Se emplean flujos automatizados de integración continua (CI) que construyen contenedores estandarizados y ejecutan pruebas de regresión antes de desplegar versiones estables en producción (Bass et al., 2015; Kim et al., 2016).
- **Validación y Pruebas del Servicio:** Se aplican pruebas unitarias y de integración sobre los endpoints del POS y sobre la lógica de reversas de la Saga para asegurar su funcionamiento correcto previo a la salida a producción.
- **Gestión del Conocimiento y Capacitación:** Se elabora un manual operativo y se imparten talleres prácticos a los cajeros y baristas para familiarizarlos con el manejo del software y la resolución de incidentes menores.

### 3.4. Operación del Servicio (*Service Operation*)
Esta fase coordina las actividades cotidianas para mantener la estabilidad de los servicios y atender las solicitudes de los usuarios (Cabinet Office, 2011c):
- **Gestión de Incidentes:** Se implementa un protocolo escalonado de atención. El Nivel 0 corresponde al personal de mostrador (verificación de cables, reinicio de aplicación y cambio de papel térmico); el Nivel 1 atiende problemas de enlace o caídas de sesión vía remota; el Nivel 2 involucra al equipo de ingeniería para corregir excepciones no contempladas.
- **Gestión de Problemas:** Cuando se detectan fallas recurrentes (por ejemplo, desconexiones intermitentes de la impresora térmica o saturación en colas de mensajes), se realiza un análisis de causa raíz para implementar soluciones definitivas y evitar la repetición del incidente.
- **Gestión de Accesos:** Se administran las credenciales de los empleados conforme al esquema RBAC. Se asignan perfiles diferenciados para cajeros, baristas y gerentes, revocando permisos cuando un colaborador concluye su relación de trabajo.
- **Gestión de Eventos y Monitoreo:** Se vigila el estado de los servicios a través del endpoint `/api/health` y se canalizan mensajes atascados a la Dead Letter Queue (DLQ), generando alertas técnicas por correo electrónico ante saturación anormal.

### 3.5. Mejora Continua del Servicio (*Continual Service Improvement*)
Esta fase mantiene el alineamiento del servicio con las necesidades cambiantes del negocio a lo largo del tiempo (Cabinet Office, 2011a):
- **Ciclo Plan-Do-Check-Act (PDCA):** Se evalúan trimestralmente las métricas operativas frente a las metas planteadas en la Tabla 3.
- **Medición de Desempeño y Satisfacción:** Se registran tiempos reales de cobro en barra para verificar el cumplimiento de la meta de ≤ 75 segundos por comensal y se recaban opiniones del personal para identificar pantallas confusas o flujos de cobro lentos.
- **Optimización de Recursos y Costos:** Se revisa periódicamente el consumo de recursos en la nube con el fin de ajustar las capacidades contratadas y mantener el gasto operativo dentro de los límites presupuestados.

---

# 4. CONCLUSIONES GENERALES

El diseño de esta estrategia de servicios tecnológicos para Monchis Café permitió comprender que la ingeniería informática en un negocio gastronómico trasciende la construcción de interfaces o la configuración de bases de datos. La gestión de servicios bajo el marco de ITIL 2011 aportó una estructura metódica para conectar las decisiones de arquitectura de software —como la orquestación de transacciones con RabbitMQ sobre una máquina virtual e2-medium y la autenticación basada en tokens— con los requerimientos operativos de la barra, la certidumbre de los inventarios y la atención ágil a los comensales.

No obstante, es indispensable señalar los límites y riesgos inherentes a esta propuesta. Las cifras de tiempo de atención (≤ 75 segundos), disponibilidad (99.5 %, equivalente a un máximo de 94 minutos de indisponibilidad tolerada al mes) y costos de mantenimiento corresponden a estimaciones y metas teóricas formuladas en un contexto académico que aún deben contrastarse en un entorno de venta real con comensales en vivo. Con el soporte técnico asumido internamente por el propio equipo y sin contabilizar el costo de desarrollo por tratarse de un proyecto académico, el Costo Total de Propiedad a 3 años de Monchis Café ($72,540 MXN) resulta competitivo frente a las opciones comerciales analizadas (Loyverse POS entre $51,400 y $105,400 MXN*, y Soft Restaurant 12 Pro en ~$75,400 MXN*). Sin embargo, es necesario añadir con claridad que, si se incorporara el costo comercial del desarrollo inicial ($217,600 MXN* estimados) o una póliza de soporte externo ($3,600 MXN/mes*), el desarrollo a la medida superaría el costo de los paquetes comerciales empaquetados. Por consiguiente, su justificación principal radica en la trazabilidad nativa del café de especialidad, la consistencia mediante Patrón Saga y el control directo sobre los datos. El paso inmediato consistirá en validar los supuestos de RTO (≤ 45 min), RPO (≤ 24 h) y latencia (≤ 450 ms P95) mediante pruebas piloto de estrés en la terminal táctil y ejercicios de simulación con baristas antes de autorizar cualquier despliegue definitivo.

---

# 5. REFERENCIAS BIBLIOGRÁFICAS

* AXELOS. (2019). *ITIL foundation: ITIL 4 edition*. The Stationery Office.
* Bass, L., Weber, I., & Zhu, L. (2015). *DevOps: A software architect's perspective*. Addison-Wesley.
* Cabinet Office. (2011a). *ITIL continual service improvement* (2011 ed.). The Stationery Office.
* Cabinet Office. (2011b). *ITIL service design* (2011 ed.). The Stationery Office.
* Cabinet Office. (2011c). *ITIL service operation* (2011 ed.). The Stationery Office.
* Cabinet Office. (2011d). *ITIL service strategy* (2011 ed.). The Stationery Office.
* Cabinet Office. (2011e). *ITIL service transition* (2011 ed.). The Stationery Office.
* Cámara de Diputados del H. Congreso de la Unión. (2025). *Ley Federal de Protección de Datos Personales en Posesión de los Particulares* (publicada el 20 de marzo de 2025; abroga la ley de 2010). Diario Oficial de la Federación. Consultado el 17 de octubre de 2026, de https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf
* Google Cloud. (2026). *Calculadora de precios oficial de Google Cloud: Compute Engine y Cloud SQL*. Alphabet Inc. Consultado el 17 de octubre de 2026, de https://cloud.google.com/products/calculator
* International Organization for Standardization, & International Electrotechnical Commission. (2018). *Information technology — Service management — Part 1: Service management system requirements* (ISO/IEC Standard No. 20000-1:2018). ISO/IEC. https://www.iso.org/standard/70636.html
* International Organization for Standardization, & International Electrotechnical Commission. (2022). *Information security, cybersecurity and privacy protection — Information security management systems — Requirements* (ISO/IEC Standard No. 27001:2022). ISO/IEC. https://www.iso.org/standard/82875.html
* Kim, G., Humble, J., Debois, P., & Willis, J. (2016). *The DevOps handbook: How to create world-class agility, reliability, and security in technology organizations*. IT Revolution Press.
* Loyverse. (2026). *Planes y precios de punto de venta y gestión de inventario para cafeterías*. Loyverse, Inc. Consultado el 17 de octubre de 2026, de https://loyverse.com/es/pricing
* National Soft. (2026). *Soft Restaurant 12: Soluciones integrales para restaurantes y cafeterías*. National Soft de México S.A. de C.V. Consultado el 17 de octubre de 2026, de https://www.nationalsoft.com.mx y https://softrestaurant.com
* Organización de las Naciones Unidas. (2015). *Transformar nuestro mundo: la Agenda 2030 para el Desarrollo Sostenible* (Resolución A/RES/70/1). ONU. https://undocs.org/es/A/RES/70/1
* RabbitMQ. (2026). *Production checklist and hardware guidelines for RabbitMQ*. VMware / Broadcom. Consultado el 17 de octubre de 2026, de https://www.rabbitmq.com/docs/production-checklist
* Reichheld, F. F., & Sasser, W. E. (1990). Zero defections: Quality comes to services. *Harvard Business Review*, 68(5), 105–111.
