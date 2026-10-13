# UNIVERSIDAD DE GUADALAJARA
## CENTRO UNIVERSITARIO DE TONALÁ (CUTonalá)
### DIVISIÓN DE INGENIERÍAS E INNOVACIÓN TECNOLÓGICA
### LICENCIATURA EN INGENIERÍA EN COMPUTACIÓN

---

# ACTIVIDAD PARTICIPACIÓN: DISEÑO DE ESTRATEGIA DE SERVICIOS TI
### Gestión de Servicios Informáticos

* **Docente:** Dr. Gabriel Navarro Salcedo  
* **Proyecto Final:** Monchis Café — Plataforma Web Integral y Sistema de Gestión de Servicios para Cafetería Orgánica y Comercial  
* **Equipo de Proyecto:**  
  * Ernesto Hatuey Fierro Medina (Código: 215487963) — *Líder de Proyecto y Arquitecto de Servicios TI*  
  * Jazmín Díaz — *Ingeniera de Requerimientos y Diseño de Servicios*  
  * Héctor Hernández — *Especialista en Infraestructura y Operación de Servicios TI*  
  * Oswaldo Millán — *Especialista en Transición y Aseguramiento de Calidad de Software*  
* **Fecha de Entrega:** 17 de octubre de 2026  
* **Ciclo Escolar:** 2026-B  

---

# ÍNDICE GENERAL

1. [Introducción y Marco de Gestión de Servicios TI](#1-introducción-y-marco-de-gestión-de-servicios-ti)
2. [Desarrollo de la Estrategia de Servicios TI](#2-desarrollo-de-la-estrategia-de-servicios-ti)
   * 2.1. [¿Qué servicios debemos ofrecer? (Portafolio y Catálogo de Servicios)](#21-qué-servicios-debemos-ofrecer)
   * 2.2. [¿Cuál es su valor? (Definición de Valor: Utilidad y Garantía)](#22-cuál-es-su-valor)
   * 2.3. [¿Cuáles son los resultados esperados? (Metas Cualitativas y Cuantitativas)](#23-cuáles-son-los-resultados-esperados)
   * 2.4. [¿Cuáles son nuestros clientes potenciales? (Segmentación y Perfiles de Mercado)](#24-cuáles-son-nuestros-clientes-potenciales)
   * 2.5. [¿Qué servicios son prioritarios? (Matriz de Priorización Estratégica)](#25-qué-servicios-son-prioritarios)
   * 2.6. [¿Qué inversiones son necesarias? (Presupuesto y Recursos Financieros)](#26-qué-inversiones-son-necesarias)
   * 2.7. [¿Qué servicios existen ya en el mercado que puedan representar una competencia directa? (Benchmarking Competitivo)](#27-qué-servicios-existen-ya-en-el-mercado-que-puedan-representar-una-competencia-directa)
   * 2.8. [¿Cómo podemos diferenciarnos de la competencia? (Propuesta de Valor Única)](#28-cómo-podemos-diferenciarnos-de-la-competencia)
3. [Articulación de la Estrategia en las Fases del Ciclo de Vida del Servicio TI (ITIL)](#3-articulación-de-la-estrategia-en-las-fases-del-ciclo-de-vida-del-servicio-ti-itil)
   * 3.1. Estrategia del Servicio (*Service Strategy*)
   * 3.2. Diseño del Servicio (*Service Design*)
   * 3.3. Transición del Servicio (*Service Transition*)
   * 3.4. Operación del Servicio (*Service Operation*)
   * 3.5. Mejora Continua del Servicio (*Continual Service Improvement*)
4. [Conclusiones](#4-conclusiones)
5. [Referencias (Formato APA 7.ª edición)](#5-referencias)

---

# 1. INTRODUCCIÓN Y MARCO DE GESTIÓN DE SERVICIOS TI

En la actualidad, las tecnologías de información han dejado de ser meras herramientas de soporte administrativo para convertirse en el núcleo estratégico que habilita, transforma y potencia los modelos de negocio. Bajo los principios de la Gestión de Servicios de Tecnologías de la Información (ITSM), formalizados en marcos de referencia reconocidos globalmente como **ITIL (Information Technology Infrastructure Library)** y el estándar internacional **ISO/IEC 20000-1:2018**, un servicio de TI se define como un medio para entregar valor a los clientes facilitando los resultados que ellos desean alcanzar, sin que estos deban asumir de forma directa la propiedad de costos y riesgos específicos (AXELOS, 2019; ISO/IEC, 2018).

El presente documento expone la **Estrategia Integral de Servicios TI** diseñada por el equipo de proyecto para **Monchis Café**, una empresa gastronómica especializada en café orgánico de cooperativas regionales y productos comerciales complementarios. La estrategia no se limita a describir un paquete de software aislado; por el contrario, estructura un **ecosistema de servicios gestionados** que articula las cinco fases del ciclo de vida de los servicios TI (Estrategia, Diseño, Transición, Operación y Mejora Continua). Con ello, se garantiza que la inversión tecnológica responda directamente a las necesidades del negocio en barra, a la sostenibilidad ecológica (alineada a los Objetivos de Desarrollo Sostenible de la ONU: ODS 8, 9, 12 y 16) y a una experiencia omnicanal superior para el comensal contemporáneo.

---

# 2. DESARROLLO DE LA ESTRATEGIA DE SERVICIOS TI

A continuación se da respuesta analítica, justificada y fundamentada a las ocho preguntas directrices planteadas para el diseño estratégico de servicios, integrando la realidad técnica y operativa del proyecto Monchis Café.

---

## 2.1. ¿QUÉ SERVICIOS DEBEMOS OFRECER?

Para estructurar la oferta tecnológica, adoptamos la metodología de portafolio y catálogo de servicios de ITIL v3 / ITIL 4, clasificando los servicios en **Servicios Principales (Core)**, **Servicios Habilitadores (Enabling)** y **Servicios de Soporte/Garantía (Support & Enhancing)**. Esta taxonomía permite identificar con claridad qué percibe el cliente final y qué capas de infraestructura y seguridad sustentan la operación ininterrumpida de la cafetería.

```
                    ┌────────────────────────────────────────────────────────┐
                    │               CATÁLOGO DE SERVICIOS TI                 │
                    │                    "MONCHIS CAFÉ"                      │
                    └────────────────────────────────────────────────────────┘
                                                 │
         ┌───────────────────────────────────────┼──────────────────────────────────────┐
         ▼                                       ▼                                      ▼
┌─────────────────────────────┐   ┌─────────────────────────────┐   ┌─────────────────────────────┐
│    SERVICIOS PRINCIPALES    │   │    SERVICIOS HABILITADORES  │   │    SERVICIOS DE SOPORTE     │
│           (CORE)            │   │         (ENABLING)          │   │         (SUPPORT)           │
├─────────────────────────────┤   ├─────────────────────────────┤   ├─────────────────────────────┤
│ 1. Punto de Venta Táctil    │   │ 4. Plataforma Cloud &       │   │ 7. Mesa de Ayuda y Soporte  │
│    (POS) Omnicanal          │   │    Mensajería RabbitMQ      │   │    Técnico en Sitio/Remoto  │
│ 2. Trazabilidad de Café     │   │ 5. Gestión de Datos y       │   │ 8. Continuidad y Copias de  │
│    Orgánico y Lotes         │   │    Almacenamiento Seguro    │   │    Seguridad Automatizadas  │
│ 3. Fidelización y Monedero  │   │ 6. Seguridad Perimetral,    │   │ 9. Monitoreo Proactivo y    │
│    Digital (Monchis Rewards)│   │    Auth Stateless & 2FA     │   │    Alertamiento en Tiempo R.│
└─────────────────────────────┘   └─────────────────────────────┘   └─────────────────────────────┘
```

### A. Servicios Principales (Core Services)
1. **Servicio de Punto de Venta Táctil (POS) Omnicanal y Procesamiento Multimodal de Pagos:**  
   * *Descripción:* Interfaz interactiva de alta velocidad optimizada para tabletas y terminales táctiles de barra (Vue 3 SPA). Facilita el registro inmediato de comandas, cobro mixto (efectivo con cálculo automatizado de cambio, tarjetas mediante pasarelas Stripe/Clip/Mercado Pago, transferencias electrónicas SPEI con captura de clave de rastreo) y emisión automatizada de tickets digitales y físicos (térmicos de 80 mm).
   * *Justificación:* Constituye el motor generador de ingresos de la cafetería. Un fallo o demora en la terminal de cobro degrada inmediatamente la experiencia del cliente y ocasiona pérdidas financieras directas.
2. **Servicio de Trazabilidad Integral de Café Orgánico y Gestión PEPS de Almacén:**  
   * *Descripción:* Registro granular de cada lote de café en grano recibido desde cooperativas productoras (origen geográfico, finca, altitud, perfil de tueste, fecha de tostado y caducidad). Implementa rotación estricta PEPS (Primeras Entradas, Primeras Salidas) y genera códigos QR para que los clientes consulten el origen del café en su taza.
   * *Justificación:* La propuesta de valor de Monchis Café radica en el café de especialidad orgánico y sustentable. Sin trazabilidad digitalizada, existe el riesgo de vender grano envejecido o perder la certificación de procedencia.
3. **Servicio de Fidelización y Monedero Digital ("Monchis Rewards"):**  
   * *Descripción:* Sistema digital de lealtad que recompensa la recurrencia del comensal: tarjeta digital de sellos (8.ª bebida preparada gratuita tras 7 compras acumuladas), monedero de cashback (1 punto por cada $10 MXN de compra) y bonificación ecológica directa de $5.00 MXN al llevar termo o taza reutilizable (alineado al ODS 12).
   * *Justificación:* Retener a un cliente cuesta una fracción de lo que cuesta adquirir uno nuevo. En el rubro de cafeterías de barrio, la fidelización digital gamificada crea barreras contra la competencia directa.

### B. Servicios Habilitadores e Infraestructura (Enabling Services)
4. **Servicio de Plataforma Cloud y Orquestación Asíncrona (RabbitMQ + Patrón Saga):**  
   * *Descripción:* Infraestructura contenerizada bajo Docker y orquestación de transacciones distribuidas. Cuando una venta concurrente se procesa en barra y el inventario de un insumo crítico se agota, el broker ejecuta transacciones compensatorias automáticas (reversas) para cancelar el pedido, reembolsar el pago y liberar recursos sin inconsistencias en base de datos.
   * *Justificación:* Previene el cobro de productos no disponibles y garantiza consistencia transaccional aun durante picos de demanda en horas punta (8:00 a 11:00 hrs).
5. **Servicio de Almacenamiento Seguro y Persistencia Transaccional (PostgreSQL + Prisma):**  
   * *Descripción:* Almacenamiento relacional estructurado con integridad referencial estricta, consultas parametrizadas contra inyecciones SQL y particionamiento lógico de catálogos comerciales frente a insumos orgánicos de especialidad.
   * *Justificación:* Asegura la confidencialidad, no repudio y precisión matemática de los registros contables y fiscales del negocio.
6. **Servicio de Seguridad Perimetral, Autenticación Stateless y Control de Acceso (RBAC):**  
   * *Descripción:* Autenticación basada en JSON Web Tokens (JWT) rotativos con Refresh Token en cookies `httpOnly + Secure + SameSite=Strict`, validación anti-bots con Google reCAPTCHA v2/v3, doble factor de autenticación (2FA) para roles gerenciales y auditoría de accesos.
   * *Justificación:* Protege la caja, los datos personales de clientes (conforme a la Ley Federal de Protección de Datos Personales en Posesión de los Particulares - LFPDPPP) y previene accesos indebidos desde terminales no autorizadas.

### C. Servicios de Soporte y Operación (Support Services)
7. **Servicio de Mesa de Ayuda (Service Desk) y Soporte Técnico Continuo (Nivel 1 y 2):**  
   * *Descripción:* Canal de asistencia técnica remota e inmediata para cajeros y administradores ante incidencias de hardware (impresoras trabadas, desconexión de red) o bloqueos en la plataforma, con tiempos de respuesta bajo acuerdo de nivel de servicio (SLA).
8. **Servicio de Respaldo Automatizado y Recuperación ante Desastres (Disaster Recovery):**  
   * *Descripción:* Respaldos incrementales automatizados diarios y volcados completos semanales cifrados y almacenados en almacenamiento externo seguro (Cloud Storage), con procedimientos validados de restauración en menos de 60 minutos.
9. **Servicio de Monitoreo Proactivo de Salud y Telemetría:**  
   * *Descripción:* Vigilancia continua del estado del servidor, latencia de base de datos, colas muertas de mensajería (Dead Letter Queue) y consumo de memoria, disparando alertas por SMTP a los administradores antes de que un fallo impacte la atención al público.

---

## 2.2. ¿CUÁL ES SU VALOR?

Siguiendo el principio fundamental de ITIL, **el valor no reside en la tecnología misma, sino en la percepción de los resultados habilitados para el cliente**. El valor se compone de dos factores inseparables: **Utilidad (*Fit for Purpose*)** —lo que el servicio hace— y **Garantía (*Fit for Use*)** —cómo se entrega el servicio en términos de disponibilidad, capacidad, continuidad y seguridad— (AXELOS, 2019; Steinberg, 2011).

```
                      ┌────────────────────────────────────────┐
                      │          CREACIÓN DE VALOR TI          │
                      │             (VALOR TOTAL)              │
                      └────────────────────────────────────────┘
                                           │
                ┌──────────────────────────┴──────────────────────────┐
                ▼                                                     ▼
    ┌─────────────────────────┐                           ┌─────────────────────────┐
    │  UTILIDAD DEL SERVICIO  │                           │  GARANTÍA DEL SERVICIO  │
    │   ("Fit for Purpose")   │                           │     ("Fit for Use")     │
    ├─────────────────────────┤                           ├─────────────────────────┤
    │ • Elimina cuellos de    │                           │ • Disponibilidad 99.9%  │
    │   botella en caja.      │                           │ • Transacciones seguras │
    │ • Trazabilidad de café  │                           │   (Stateless JWT + 2FA) │
    │   orgánico certificable.│                           │ • Resiliencia con Saga  │
    │ • Fidelización activa   │                           │   (Reversas automáticas)│
    │   y monetizable.        │                           │ • Recuperación RTO < 1h │
    └─────────────────────────┘                           └─────────────────────────┘
```

### A. Aportes Concretos a la Productividad y Eficiencia Operativa
* **Reducción del Tiempo de Cobro en Barra (Productividad):** La interfaz táctil con pre-cálculo de cambio e integración de lectores ópticos reduce el tiempo promedio de atención por cliente de **2 minutos y medio a menos de 45 segundos**. Esto permite a Monchis Café atender hasta un **60 % más de clientes en horas pico matutinas** con la misma dotación de personal.
* **Automatización del Cierre de Caja:** El cuadre de ingresos en efectivo, tarjeta y SPEI se realiza de manera inmediata al finalizar el turno, eliminando de **40 a 60 minutos diarios de conteo manual** y reduciendo a cero los errores aritméticos de los cajeros.
* **Control Automatizado de Mermas y Caducidad de Café:** El sistema alerta preventivamente sobre lotes de café con más de 20 días de tostado, priorizando su molienda antes de que pierdan sus notas de cata y aromas esenciales. Esto reduce el desperdicio de materia prima costosa en un **85 %**.

### B. Reducción de Costos Operativos y Financieros
* **Ahorro en Comisiones y Licenciamiento Propietario:** Al desplegar un sistema web modular en contenedores en lugar de contratar software cerrado con licencias mensuales por terminal (que típicamente cobran entre $1,500 y $3,000 MXN mensuales por estación de trabajo más comisiones adicionales por módulo), Monchis Café ahorra aproximadamente **$36,000 MXN anuales** en gastos recurrentes de software.
* **Mitigación de Fraudes e Inconsistencias:** La obligatoriedad del doble factor para administradores, el control estricto de accesos RBAC y la auditoría inmutable de transacciones eliminan las pérdidas por cancelaciones sospechosas o descuadres de inventario en mostrador.

### C. Generación de Beneficios Estratégicos y Competitivos
* **Monetización de la Sustentabilidad:** La bonificación por termo reutilizable atrae al segmento joven y profesional con conciencia ambiental, incrementando la lealtad y el valor de vida del cliente (*Customer Lifetime Value*).
* **Inteligencia de Negocio y Atribución Comercial:** El panel analítico captura el origen del cliente a través de parámetros `utm_source` (diferenciando comensales atraídos por la ficha de Google Maps vs. campañas visuales de Instagram). Esto permite a la dirección invertir su presupuesto de marketing únicamente en los canales que generan visitas y ventas reales.

---

## 2.3. ¿CUÁLES SON LOS RESULTADOS ESPERADOS?

Para garantizar que la estrategia sea medible y auditable conforme a la fase de Mejora Continua de ITIL, se establecen metas cualitativas y cuantitativas vinculadas a Factores Críticos de Éxito (CSFs) e Indicadores Clave de Desempeño (KPIs):

### Tabla 1. Matriz de Resultados Esperados (Cualitativos y Cuantitativos)

| Dimensión | Factor Crítico de Éxito (CSF) | Métrica / Indicador Clave (KPI) | Meta Estratégica Cuantitativa | Meta Cualitativa Esperada |
| :--- | :--- | :--- | :--- | :--- |
| **Operación en Barra** | Velocidad y fluidez en el registro de pedidos | Tiempo Medio de Atención en Caja (*Service Time*) | $\le 45$ segundos por transacción | Eliminación de filas estresantes; sensación de servicio moderno y profesional. |
| **Desempeño Técnico** | Rapidez en la respuesta del sistema | Latencia de endpoints en transacciones POS | $\le 400$ ms en el percentil 95 (P95) | Sensación de inmediatez táctil en la pantalla del cajero. |
| **Disponibilidad** | Continuidad operativa durante horario comercial | Tiempo de Actividad (*System Uptime*) | $\ge 99.9$ % (máx. 43 min no planificados/mes) | Confianza total del personal: la caja nunca "se cae" en plena venta. |
| **Fiabilidad Transaccional** | Consistencia en inventarios y cobros concurrentes | Tasa de transacciones inconsistentes | $0.0$ % (100 % gestionadas por Saga/DLQ) | Ausencia de quejas por cobros duplicados o productos agotados. |
| **Fidelización** | Retención recurrente de clientes | Tasa de adopción del programa Monchis Rewards | $\ge 40$ % de los clientes frecuentes registrados | Vínculo afectivo con la marca y sentido de recompensa tangible. |
| **Sostenibilidad** | Reducción de insumos desechables (ODS 12) | Porcentaje de pedidos servidos en termo/taza reusables | $\ge 25$ % del volumen total de bebidas | Reputación de Monchis Café como líder ecológico en la región. |
| **Soporte TI** | Resolución expedita de fallos en producción | Tiempo Medio de Resolución de Incidentes Críticos (*MTTR*) | $\le 60$ minutos | Seguridad del personal de caja de contar con respaldo técnico ágil. |
| **Efectividad Comercial** | Rentabilidad de las campañas digitales | Tasa de conversión de visitas con atribución UTM | $\ge 12$ % de conversión en ventas registradas | Certeza gerencial del retorno de inversión en redes y Google Maps. |

---

## 2.4. ¿CUÁLES SON NUESTROS CLIENTES POTENCIALES?

La estrategia de servicios TI de Monchis Café contempla una segmentación dual: los **beneficiarios directos e indirectos del ecosistema**, identificando quién interactúa con cada componente del servicio:

```
                    ┌────────────────────────────────────────────────────────┐
                    │            SEGMENTACIÓN DE CLIENTES TI                 │
                    └────────────────────────────────────────────────────────┘
                                                 │
         ┌───────────────────────────────────────┴──────────────────────────────────────┐
         ▼                                                                              ▼
┌─────────────────────────────────────────┐                    ┌─────────────────────────────────────────┐
│        SEGMENTO A: CLIENTE FINAL        │                    │      SEGMENTO B: CLIENTE INTERNO /      │
│        (CONSUMIDORES Y COOPERATIVAS)    │                    │      POTENCIALES FRANQUICIATARIOS       │
├─────────────────────────────────────────┤                    ├─────────────────────────────────────────┤
│ • Consumidores de Café de Especialidad  │                    │ • Dueños y Gerencia de Monchis Café     │
│ • Profesionales y Teletrabajadores      │                    │ • Baristas y Personal de Atención       │
│ • Productores y Cooperativas Orgánicas  │                    │ • Cafeterías Independientes Similares   │
│   (Trazabilidad de origen y comercio)   │                    │   (Modelo SaaS marca blanca a futuro)   │
└─────────────────────────────────────────┘                    └─────────────────────────────────────────┘
```

### Segmento 1: Consumidores y Clientes Externos
* **Aficionados al Café de Especialidad (Consumidor Gourmet):**  
  * *Perfil:* Personas de 22 a 55 años, con poder adquisitivo medio-alto, que valoran los orígenes del grano, los métodos de extracción y la pureza orgánica.  
  * *Necesidad TI:* Desean escanear el código QR del ticket para conocer la finca de procedencia, altitud y fecha de tueste; valoran un menú interactivo visual y claro.
* **Nómadas Digitales, Profesionales y Estudiantes Locales:**  
  * *Perfil:* Clientes que acuden a la cafetería a trabajar o socializar.  
  * *Necesidad TI:* Exigen pagos rápidos sin contacto, emisión de factura electrónica sin fricciones y un programa de lealtad en su smartphone que no requiera tarjetas plásticas contaminantes.
* **Productores y Cooperativas Cafetaleras Regionales:**  
  * *Perfil:* Cooperativas de pequeños agricultores del estado y regiones aledañas.  
  * *Necesidad TI:* Requieren visibilidad sobre la venta de sus cosechas y certeza de que su marca de origen es respetada y destacada ante el consumidor final.

### Segmento 2: Clientes Internos y Usuarios Operativos
* **Personal Operativo (Baristas y Cajeros):**  
  * *Necesidad TI:* Una interfaz táctil limpia, rápida, a prueba de equivocaciones táctiles, con cálculo automático de cambio y confirmación instantánea de transacciones.
* **Administración y Gerencia:**  
  * *Necesidad TI:* Reportes consolidados en PDF y Excel, auditoría de flujo de efectivo, trazabilidad de mermas y panel de control del marketing digital.

### Segmento 3: Potencial de Expansión de Mercado (SaaS Gastronómico para Micro y Pequeñas Cafeterías)
* **Perfil:** Microempresas del sector restaurantero y cafeterías de especialidad de 1 a 3 sucursales en ciudades medianas.
* **Dolor de Mercado:** Actualmente están desatendidas por los grandes sistemas ERP (demasiado costosos y burocráticos) y limitadas por las apps básicas de cobro (que no manejan trazabilidad de café orgánico ni patrones de compensación). El sistema Monchis Café representa un modelo altamente comercializable como servicio SaaS para este nicho.

---

## 2.5. ¿QUÉ SERVICIOS SON PRIORITARIOS?

Para definir el orden de implementación y puesta en marcha de los servicios, se aplicó una **Matriz de Priorización de Servicios TI** basada en dos criterios fundamentales: **Impacto en la Continuidad del Negocio (Urgencia/Valor)** y **Factibilidad Técnica y Disponibilidad de Recursos**.

### Tabla 2. Matriz de Priorización Estratégica de Servicios TI

| Nivel de Prioridad | Servicio TI | Justificación de Negocio | Recursos Técnicos Requeridos | Fase de Despliegue |
| :---: | :--- | :--- | :--- | :---: |
| **P1 (Crítica / Inmediata)** | **POS Táctil & Procesamiento de Pagos** | Sin este servicio es imposible abrir la cafetería y registrar cobros legales. Cero tolerancia a retrasos. | Frontend Vue 3, Next.js API, BD PostgreSQL, lectores de códigos e impresoras de tickets. | Fase 1 (Semana 1-3) |
| **P1 (Crítica / Inmediata)** | **Seguridad Stateless & Autenticación RBAC** | Protege las transacciones financieras y restringe el acceso al panel administrativo desde el día uno. | JWT rotativos, Google reCAPTCHA, middlewares de validación Zod. | Fase 1 (Semana 2-4) |
| **P2 (Alta / Esencial)** | **Trazabilidad de Café Orgánico y Control PEPS** | Garantiza la diferenciación de Monchis Café y evita pérdidas económicas por caducidad de lotes. | Modelos relacionales Prisma, catálogo segmentado, módulo de inventario. | Fase 2 (Semana 5-7) |
| **P2 (Alta / Esencial)** | **Infraestructura Resiliente (RabbitMQ Saga)** | Evita inconsistencias graves cuando hay ventas simultáneas en barra y pedidos de insumos. | Docker Compose, Broker RabbitMQ, orquestador Saga y colas de retardo. | Fase 2 (Semana 6-8) |
| **P3 (Media / Diferenciadora)** | **Fidelización "Monchis Rewards" & ODS 12** | Impulsa la recompra y consolida la comunidad de clientes una vez estabilizada la barra. | Lógica de puntos en Pinia/Next.js, algoritmo de sellos digitales y descuentos por termo. | Fase 3 (Semana 9-11) |
| **P3 (Media / Diferenciadora)** | **Panel Analítico & Atribución de Tráfico UTM** | Permite optimizar la inversión de publicidad en Instagram y Google Maps para la gerencia. | Dashboard administrativo, librerías de gráficos, exportación a Excel y PDF. | Fase 3 (Semana 10-12) |
| **P4 (Soporte Continuo)** | **Mesa de Ayuda, Monitoreo y Backup Automatizado** | Mantiene la salud operativa, previene pérdidas de datos catastróficas y brinda soporte. | Scripts de backup en cron, alertas SMTP, telemetría de servidor y canal de soporte. | Fase 4 (Transversal) |

*Argumentación de la priorización:*  
Se priorizan en el primer bloque los servicios transaccionales y de seguridad (P1) porque constituyen el núcleo vital (*Minimum Viable Service*) para operar comercialmente. En el segundo bloque (P2) se ubica la trazabilidad y la resiliencia asíncrona, ya que representan la base de la propuesta de valor del café de especialidad. La fidelización y la analítica avanzada (P3) se activan una vez que el flujo transaccional está completamente depurado, cerrando con las políticas transversales de soporte y continuidad (P4).

---

## 2.6. ¿QUÉ INVERSIONES SON NECESARIAS?

La puesta en marcha y operación sostenible de la estrategia de servicios TI demanda una estructura presupuestal realista y justificada. Se analizan las inversiones en cinco rubros esenciales: **Infraestructura Cloud/Hardware**, **Herramientas de Software y Licencias**, **Personal y Roles Especializados**, **Capacitación Operativa** y **Reserva de Contingencia**.

### Tabla 3. Presupuesto Detallado de Inversión Inicial y Operación Mensual (Valores en MXN)

| Rubro de Inversión | Descripción del Componente | Tipo de Gasto | Inversión Inicial (Setup) | Gasto Operativo Mensual (OPEX) | Justificación Estratégica |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Hardware en Barra** | 2 Tabletas industriales táctiles 10.5" Android para POS con base de soporte de seguridad | CAPEX | $12,500 MXN | $0 MXN | Terminales interactivas duraderas para cajero y barista en barra. |
| **Hardware Periférico** | 2 Impresoras térmicas de tickets USB/Ethernet 80 mm + 2 Lectores de código 1D/2D omnidireccionales | CAPEX | $7,800 MXN | $0 MXN | Emisión instantánea de comandas, recibos fiscales y lectura de códigos de barra. |
| **Infraestructura Cloud** | Servidor Virtual Privado (GCP Compute Engine / Cloud Run) para Backend Next.js y RabbitMQ | OPEX | $0 MXN | $650 MXN | Alojamiento contenerizado de alta disponibilidad y baja latencia. |
| **Base de Datos Cloud** | Instancia administrada PostgreSQL (Cloud SQL o servidor dedicado optimizado) con backups automáticos | OPEX | $0 MXN | $450 MXN | Persistencia transaccional confiable con respaldos diarios cifrados. |
| **Dominio y Red (CDN)** | Dominio comercial `.com.mx`, certificados SSL/TLS y CDN Cloudflare (mitigación DDoS y DNS seguro) | CAPEX / OPEX | $680 MXN (anual) | $0 MXN (plan Pro $400 MXN opt.) | Identidad corporativa, seguridad HTTPS y entrega ultrarrápida del frontend estático. |
| **Servicio SMTP & SMS** | Pasarela de mensajería para alertas transaccionales a administradores y notificaciones DLQ (SendGrid / Brevo) | OPEX | $0 MXN | $250 MXN | Notificaciones críticas del patrón Saga y alertas de caducidad. |
| **Capacitación del Personal** | Talleres prácticos para baristas y cajeros (uso de POS táctil, gestión de mermas, soporte Nivel 0) | CAPEX | $3,500 MXN | $0 MXN | Garantiza que el personal domine la herramienta y brinde una atención ágil sin tropiezos. |
| **Roles de Soporte y Ops** | Servicios profesionales de soporte técnico remoto Nivel 1/2, monitoreo y mantenimiento mensual preventivo | OPEX | $0 MXN | $3,500 MXN | Cobertura técnica ante incidentes imprevistos y aplicación de parches de seguridad. |
| **Fondo de Contingencia TI** | Reserva financiera para refacciones de hardware (cables, fuentes de poder, conectividad 4G de respaldo) | CAPEX | $4,000 MXN | $0 MXN | Amortigua cualquier eventualidad física sin detener la operación de la cafetería. |
| **TOTALES CONSOLIDADOS** | **Inversión Total Inicial y Operación Mensual Estimada** | — | **$28,480 MXN** | **$4,850 MXN / mes** | **Estructura financiera sumamente rentable frente al costo de contratar software privativo.** |

---

## 2.7. ¿QUÉ SERVICIOS EXISTEN YA EN EL MERCADO QUE PUEDAN REPRESENTAR UNA COMPETENCIA DIRECTA?

Para situar la estrategia en el entorno real de mercado, realizamos un **Benchmarking Competitivo** comparando las soluciones tecnológicas gastronómicas predominantes en México frente a la propuesta de Monchis Café:

### Tabla 4. Análisis Comparativo de la Competencia en el Mercado

| Parámetro de Evaluación | Soft Restaurant (Nacional) | Toast POS / Square (Internacional) | Clip Stand / Mercadopago POS | Propuesta "Monchis Café" (Nuestra Estrategia) |
| :--- | :--- | :--- | :--- | :--- |
| **Enfoque de Negocio** | Restaurantes tradicionales y bares de gran escala. | Cadenas medianas de alimentos y bebidas (EE. UU. / Latam). | Comercios minoristas y micro-negocios genéricos. | **Cafeterías de especialidad orgánicas y comercio sostenible.** |
| **Modelo de Precios y Costos** | Licencia tradicional costosa (desde $14,000 MXN) + cobro por póliza de soporte y actualizaciones. | Suscripción mensual elevada ($69–$165 USD/mes) + comisiones obligatorias por transacción. | Terminal barata ($2,000 MXN), pero cobra comisión alta por tarjeta (3.6% + IVA) y software muy limitado. | **Bajo costo operativo mensual ($4,850 MXN infra total), sin rentas de software por asiento ni ataduras bancarias.** |
| **Trazabilidad de Café y Lotes** | Nula o muy genérica (solo maneja inventario simple de insumos). | Nula (inventario general de restaurante sin trazabilidad de origen). | Inexistente (únicamente catálogo de productos con precio). | **Nativa: Registro de cooperativa, finca, altitud, tueste, rotación PEPS y código QR al cliente.** |
| **Resiliencia Transaccional** | Bloqueo de base de datos local o inconsistencias ante caídas de red. | Dependiente 100 % de conectividad a la nube del proveedor. | No maneja transacciones distribuidas ni reversas automáticas. | **Avanzada: Patrón Saga con RabbitMQ, transacciones compensatorias automáticas y DLQ auditada.** |
| **Fidelización y Sustentabilidad** | Requiere módulos de terceros con costo extra. | Programa de puntos básico por tarjeta de crédito. | Inexistente o limitado a monederos genéricos. | **Nativa: Tarjeta digital de sellos, monedero cashback y bonificación ecológica por termo (ODS 12).** |
| **Atribución de Tráfico y SEO** | Ninguna (no conecta con la web ni con campañas de marketing). | Integración básica con pedidos en línea propietarios. | Nula. | **Nativa: Captura de `utm_source` (Google Maps vs Instagram) y frontend prerenderizado SEO (`vite-ssg`).** |
| **Soporte y Flexibilidad** | Burocrático, soporte en horarios de oficina con costo por ticket. | En idioma inglés o soporte remoto internacional despersonalizado. | Soporte genérico por chat o bots automáticos. | **Hiperlocalizado: Mesa de ayuda directa, soporte presencial/remoto ágil y SLAs adaptados a la cafetería.** |

---

## 2.8. ¿CÓMO PODEMOS DIFERENCIARNOS DE LA COMPETENCIA?

Nuestra propuesta se aleja intencionalmente de la comoditización del software genérico de cobro. Construimos una ventaja competitiva sustentable basada en cinco pilares estratégicos:

```
                          PILARESL DE DIFERENCIACIÓN ESTRATÉGICA
                                      "MONCHIS CAFÉ"
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │                                                                                        │
  │  1. ESPECIALIZACIÓN NATIVA EN CAFÉ ORGÁNICO Y SOSTENIBILIDAD (ODS 12)                  │
  │     Trazabilidad de finca a taza con código QR y recompensas por termo reutilizable.   │
  │                                                                                        │
  │  2. ARQUITECTURA DE ALTA RESILIENCIA Y CONSISTENCIA (RABBITMQ + SAGA)                  │
  │     Cero ventas inconsistentes: reversas automáticas ante desabasto de insumos.        │
  │                                                                                        │
  │  3. CONVERGENCIA OMNICANAL: MARKETING DIGITAL, SEO Y ATRIBUCIÓN REAL                   │
  │     Unión de marketing digital (Google Maps / Instagram) con el punto de venta físico. │
  │                                                                                        │
  │  4. ECONOMÍA OPERATIVA Y CERO COSTOS OCULTOS DE LICENCIAMIENTO                         │
  │     Infraestructura modular sin licencias de software prohibitivas por caja.           │
  │                                                                                        │
  │  5. MODELO DE GESTIÓN ITSM CON SOPORTE PERSONALIZADO Y HUMANIZADO                      │
  │     Atención técnica directa, mantenimiento preventivo y SLAs garantizados.            │
  │                                                                                        │
  └────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Especialización Nativa en Café de Especialidad y Sostenibilidad Ecológica:**  
   Mientras los competidores ofrecen inventarios genéricos que tratan un grano de café como si fuera un refresco embotellado, nuestra plataforma modela el ciclo biológico y sensorial del café: días de desgasificación tras el tostado, altitud de cultivo, nombre de la cooperativa campesina y rotación PEPS. Al integrar la bonificación por termo reusable, convertimos el sistema de cobro en un embajador activo de la política ambiental del negocio.
2. **Resiliencia Técnica de Nivel Empresarial con Patrón Saga:**  
   Los sistemas de bajo costo suelen cobrar una orden y luego fallar cuando el barista descubre que el ingrediente se agotó, provocando disputas verbales con el comensal. En Monchis Café, el broker RabbitMQ y el orquestador Saga procesan la transacción con eventos atómicos: si el stock de café de una región falla, el sistema realiza la reversa electrónica en milisegundos, notifica con claridad al cajero y ofrece alternativas al cliente sin fricción.
3. **Conexión Directa entre Marketing Digital (SEO) y Punto de Venta Físico:**  
   Ningún sistema comercial del mercado vincula la campaña que el usuario vio en Instagram o la búsqueda en Google Maps ("café orgánico cerca de mí") con el ticket que se cobra en el mostrador. Monchis Café une ambos mundos: su landing prerenderizada (`vite-ssg`) posiciona a la cafetería en los primeros resultados locales y transfiere los parámetros UTM a la cuenta del cliente para medir qué fotos, promociones o mapas generan ventas reales en mostrador.
4. **Independencia Tecnológica y Menor Costo Total de Propiedad (TCO):**  
   Al operar sobre una arquitectura moderna basada en estándares abiertos y microservicios ligeros en la nube, el negocio no paga rentas perpetuas por licencia ni porcentajes punitivos a monopolios de software restaurantero. El retorno de inversión (ROI) se acelera notablemente.
5. **Cultura de Servicio Humanizada y SLA Hiperlocal:**  
   La mesa de ayuda técnica no es un centro de llamadas anónimo o un chatbot genérico. El equipo de proyecto actúa como socio tecnológico directo de Monchis Café, ofreciendo tiempos de respuesta de menos de 15 minutos ante fallos críticos durante los horarios de mayor afluencia.

---

# 3. ARTICULACIÓN DE LA ESTRATEGIA EN LAS FASES DEL CICLO DE VIDA DEL SERVICIO TI (ITIL)

Para responder rigurosamente al objetivo de la actividad académica, a continuación se demuestra cómo interviene cada una de las **cinco fases del ciclo de vida del servicio TI** en la implementación de la estrategia de Monchis Café:

```
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │                 EL CICLO DE VIDA DE LOS SERVICIOS TI (ITIL / ITSM)                     │
  └────────────────────────────────────────────────────────────────────────────────────────┘
                                              │
              ┌───────────────────────────────┴───────────────────────────────┐
              ▼                                                               ▼
   ┌───────────────────────┐                                       ┌───────────────────────┐
   │ 1. SERVICE STRATEGY   │ ──► Alineación con el negocio,        │ 2. SERVICE DESIGN     │ ──► SLAs, seguridad,
   │    (Estrategia)       │     portafolio, clientes y finanzas.  │    (Diseño)           │     arquitectura, capacidad.
   └───────────────────────┘                                       └───────────────────────┘
              │                                                               │
              └───────────────────────────────┬───────────────────────────────┘
                                              ▼
                                   ┌───────────────────────┐
                                   │ 3. SERVICE TRANSITION │ ──► CI/CD, testing TDD,
                                   │    (Transición)       │     despliegue y capacitación.
                                   └───────────────────────┘
                                              │
              ┌───────────────────────────────┴───────────────────────────────┐
              ▼                                                               ▼
   ┌───────────────────────┐                                       ┌───────────────────────┐
   │ 4. SERVICE OPERATION  │ ──► Mesa de ayuda, incidentes,        │ 5. CONTINUAL SERVICE  │ ──► Métricas, KPIs,
   │    (Operación)        │     monitoreo de colas y eventos.     │    IMPROVEMENT (CSI)  │     optimización continua.
   └───────────────────────┘                                       └───────────────────────┘
```

### 3.1. Fase 1: Estrategia del Servicio (*Service Strategy*)
* **Gestión del Portafolio de Servicios:** Definición clara de servicios en desarrollo (*Pipeline*), servicios en producción (*Service Catalog*) y servicios retirados.
* **Gestión Financiera de TI:** Determinación del presupuesto CAPEX/OPEX, análisis del Costo Total de Propiedad (TCO) y comprobación del Retorno de la Inversión (ROI) proyectado a 6 meses.
* **Gestión de la Demanda:** Análisis de los patrones de consumo en barra para dimensionar los servidores en horas pico matutinas (8:00 a 11:00 hrs) y tardes de fin de semana.

### 3.2. Fase 2: Diseño del Servicio (*Service Design*)
* **Gestión de Niveles de Servicio (SLM):** Formalización de Acuerdos de Nivel de Servicio (SLA) con la gerencia de Monchis Café (disponibilidad $\ge 99.9$ %, resolución de incidentes de caja en menos de 60 minutos).
* **Gestión de la Seguridad de la Información:** Implementación de autenticación stateless mediante JWT en cookies `httpOnly`, validación anti-bot con Google reCAPTCHA, políticas de contraseñas seguras y cifrado en tránsito vía TLS 1.3.
* **Gestión de la Continuidad del Servicio (ITSCM):** Planes de contingencia que incluyen modo de operación fuera de línea en tableta con sincronización posterior y respaldo diario automatizado de base de datos en nube.
* **Gestión de Capacidad y Disponibilidad:** Dimensionamiento de recursos en Docker y RabbitMQ para procesar hasta 50 solicitudes concurrentes por segundo sin degradación.

### 3.3. Fase 3: Transición del Servicio (*Service Transition*)
* **Gestión de Cambios (*Change Enablement*):** Todo cambio en la plataforma pasa por ramas protegidas de Git, revisión obligatoria de código y validación automatizada antes de mergear a producción.
* **Gestión de Liberación e Implementación (DevOps CI/CD):** Pipelines automatizados de GitHub Actions que compilan el monorepo con Turborepo, ejecutan las pruebas unitarias y empaquetan los contenedores Docker listos para despliegue sin caída de servicio (*Zero-Downtime Deployment*).
* **Validación y Pruebas del Servicio (TDD Multicapa):** Baterías de pruebas unitarias con Vitest, pruebas de API con Supertest, pruebas de transacciones distribuidas con RabbitMQ en memoria y pruebas de interfaz con Playwright en múltiples resoluciones (móvil, tableta y escritorio).
* **Gestión del Conocimiento y Capacitación:** Elaboración de manuales interactivos de usuario para el personal de barra y sesiones de inducción antes del lanzamiento en vivo.

### 3.4. Fase 4: Operación del Servicio (*Service Operation*)
* **Gestión de Eventos y Monitoreo:** Vigilancia automática de la salud del sistema a través de endpoints de *Health Check* (`/api/health`), telemetría de RabbitMQ y alertas tempranas por correo SMTP ante eventos canalizados a la Dead Letter Queue (DLQ).
* **Gestión de Incidentes:** Protocolo escalonado para restaurar el servicio en caso de fallo:
  * *Nivel 0 (Autoservicio):* Reinicio de la aplicación en la tableta y verificación de conexión Wi-Fi por parte del cajero.
  * *Nivel 1 (Soporte Inmediato):* Asistencia telefónica o por mensajería en menos de 15 minutos para resolución de atascos lógicos o problemas de periféricos.
  * *Nivel 2 (Ingeniería de Software):* Diagnóstico profundo de base de datos, colas de mensajería o despliegue de parches urgentes (*Hotfix*).
* **Gestión de Problemas:** Análisis de Causa Raíz (RCA) ante incidentes recurrentes para corregir fallos estructurales de código o infraestructura y evitar su repetición.
* **Gestión de Accesos:** Asignación estricta de permisos según el rol de la persona en el establecimiento (`admin`, `cajero`, `cliente`).

### 3.5. Fase 5: Mejora Continua del Servicio (*Continual Service Improvement - CSI*)
* **Ciclo Deming (Plan-Do-Check-Act):** Revisión trimestral de métricas de servicio frente a los objetivos de negocio de Monchis Café.
* **Encuestas de Satisfacción del Usuario:** Recopilación periódica de opiniones de cajeros, administradores y clientes sobre la agilidad de la pantalla táctil y el programa de recompensas.
* **Optimización de Costos y Rendimiento:** Ajuste dinámico de los recursos en la nube en función del tráfico real y refinamiento de consultas de base de datos para preservar tiempos de respuesta menores a 400 milisegundos.

---

# 4. CONCLUSIONES

El diseño de una estrategia de servicios de tecnologías de información para **Monchis Café** demuestra de forma contundente que el valor tecnológico no se genera mediante la simple acumulación de líneas de código o la adopción impulsiva de modas informáticas, sino a través de la **alineación rigurosa de las capacidades de TI con los objetivos estratégicos, financieros y humanos de la organización**.

A lo largo de este análisis estratégico, pudimos articular las cinco fases del ciclo de vida de los servicios TI propuestas por ITIL, transformando los desafíos típicos de un negocio gastronómico independiente (filas lentas en horas pico, descuadres de inventario, pérdida de trazabilidad de insumos orgánicos y altos costos de software comercial) en **oportunidades de diferenciación competitiva sólida y sostenible**:

1. **Viabilidad Técnica y Operativa Comprobada:** Al sustentar la solución sobre una arquitectura moderna basada en Monorepo, contenedores Docker, mensajería asíncrona con RabbitMQ (patrón Saga) y una interfaz táctil rápida en Vue 3, se garantiza una plataforma altamente resiliente, segura y agradable para el usuario, que elimina por completo las inconsistencias transaccionales y protege los ingresos de la cafetería.
2. **Viabilidad Financiera y Retorno de Inversión:** La estructura de inversión presentada ($28,480 MXN en adquisición inicial de hardware e instalación, complementada con un gasto operativo mensual de apenas $4,850 MXN) rompe la dependencia de paquetes de software privativos que asfixian a las micro y pequeñas empresas con suscripciones mensuales elevadas por cada terminal de cobro. El ahorro acumulado y la optimización de mermas garantizan un retorno de inversión en menos de seis meses de operación regular.
3. **Sostenibilidad y Responsabilidad Social (Alineación ODS):** Monchis Café no solo compite en precio y sabor; su tecnología se convierte en el vehículo para cumplir compromisos ambientales y éticos genuinos (ODS 12 y ODS 8). La trazabilidad digital de origen dignifica el trabajo de las cooperativas cafetaleras locales, mientras que la gamificación ecológica estimula activamente la reducción de vasos desechables entre los comensales.
4. **Respaldo al Éxito del Proyecto Integrador:** Para nuestro equipo de ingeniería en computación, este ejercicio estratégico consolida una visión holística de nuestra profesión: no somos únicamente desarrolladores de software, sino **diseñadores y gestores de servicios integrales que generan valor medible para las personas y las empresas**. La estrategia aquí documentada sienta las bases definitivas para la implementación, entrega y trascendencia de Monchis Café como un proyecto de excelencia académica y comercial.

---

# 5. REFERENCIAS (FORMATO APA 7.ª EDICIÓN)

* AXELOS. (2019). *ITIL foundation: ITIL 4 edition*. TSO (The Stationery Office).
* Bass, L., Weber, I., & Zhu, L. (2015). *DevOps: A software architect's perspective*. Addison-Wesley.
* International Organization for Standardization, & International Electrotechnical Commission. (2018). *Information technology — Service management — Part 1: Service management system requirements* (ISO/IEC Standard No. 20000-1:2018). ISO/IEC. https://www.iso.org/standard/70636.html
* International Organization for Standardization, & International Electrotechnical Commission. (2022). *Information security, cybersecurity and privacy protection — Information security management systems — Requirements* (ISO/IEC Standard No. 27001:2022). ISO/IEC. https://www.iso.org/standard/82875.html
* Kerzner, H. (2022). *Project management: A systems approach to planning, scheduling, and controlling* (13th ed.). John Wiley & Sons.
* Kim, G., Humble, J., Debois, P., & Willis, J. (2016). *The DevOps handbook: How to create world-class agility, reliability, and security in technology organizations*. IT Revolution Press.
* Newman, S. (2021). *Building microservices: Designing fine-grained systems* (2nd ed.). O'Reilly Media.
* Steinberg, R. (2011). *ITIL service strategy* (2011 ed.). TSO (The Stationery Office).
* Van Bon, J., de Jong, A., Kolthof, A., Pieper, M., Tjassing, R., van der Veen, A., & Verheijen, T. (2008). *IT service management: An introduction based on ITIL V3*. Van Haren Publishing.
