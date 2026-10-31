# Nivel 2: ALCANCE — Foco: CUÁNDO
## Cronograma de Negocio — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

El cronograma es la consecuencia directa de una planificación seria y realista de un proyecto; le demuestra tanto al inversionista como al equipo operativo qué se va a hacer, en qué fechas específicas se va a entregar y por qué se decidió esa secuencia de trabajo (Kerzner, 2022). Como define con precisión el Project Management Institute (2017), la gestión del cronograma incluye los procesos indispensables para administrar y garantizar la finalización de los compromisos a tiempo. Sin un cronograma que ordene el trabajo por fases, cualquier proyecto corre el riesgo de caer en retrasos interminables y costos no contemplados que devoran el presupuesto (Gido & Clements, 2012).

En la Matriz de Zachman (1987), la celda **Alcance - Cuándo** modela la dimensión temporal desde el punto de vista del dueño del negocio (*Business Schedule / Owner's View*). En este nivel conceptual se definen dos planos temporales fundamentales para la cafetería: por un lado, las **fases de implantación del sistema** para que el personal adopte el software sin paralizar las ventas; y por el otro, los **ciclos operativos diarios y semanales** bajo los cuales abre el mostrador, se corta la caja y se renuevan los pedidos de café orgánico con las cooperativas campesinas.

---

### 2. Fases de Implantación y Despliegue del Sistema

La puesta en marcha de **Monchis Café** se estructura en cuatro fases progresivas de 4 semanas cada una (16 semanas en total), asegurando una adopción gradual por parte del equipo de baristas y la gerencia:

```
[Fase 1: Preparación y Datos] -> [Fase 2: Piloto Mostrador POS] -> [Fase 3: Rewards y ODS 12] -> [Fase 4: Estabilización]
      (Semanas 1 - 4)                  (Semanas 5 - 8)                  (Semanas 9 - 12)             (Semanas 13 - 16)
```

---

| Fase del Negocio | Duración | Actividades Clave de la Fase | Hito de Cierre y Entregable |
| :--- | :---: | :--- | :--- |
| **Fase 1: Preparación, Alta de Catálogo y Datos Maestros** | Semanas 1 a 4 | - Registro de cooperativas de Michoacán, Oaxaca y Chiapas.<br>- Carga inicial del catálogo de café de especialidad y precios oficiales.<br>- Adquisición y configuración de hardware de mostrador (terminal táctil, escáner USB e impresora térmica). | **Hito 1 (Fin Sem 4):** Base de datos inicial poblada y hardware de mostrador validado. |
| **Fase 2: Puesta en Marcha del POS y Cobro Multipago** | Semanas 5 a 8 | - Capacitación presencial de cajeros y baristas en el uso del POS.<br>- Operación en mostrador con cobros en efectivo, tarjeta y SPEI.<br>- Validación de la precisión en el arqueo diario de caja y cálculo de cambio. | **Hito 2 (Fin Sem 8):** Primer corte de caja semanal con 0% de discrepancias en mostrador. |
| **Fase 3: Activación de Monchis Rewards y Alertas PEPS** | Semanas 9 a 12 | - Lanzamiento formal de la Bonificación Ecológica (\$5.00 MXN de descuento por termo).<br>- Registro de clientes al programa de 8 sellos digitales.<br>- Puesta en marcha del motor de alertas por correo SMTP para caducidades de grano (<15 días). | **Hito 3 (Fin Sem 12):** Primeros 100 clientes registrados y 35% de café servido en recipientes reusables. |
| **Fase 4: Analítica de Tráfico, Auditoría y Operación Estable** | Semanas 13 a 16 | - Medición de campañas digitales (atribución Google Maps vs Instagram).<br>- Generación de reportes ejecutivos semanales en PDF y Excel.<br>- Auditoría de seguridad web, cierre de turnos y entrega definitiva a gerencia. | **Hito 4 (Fin Sem 16):** Operación en producción estable con sistema en la nube (Cloud Run). |

---

### 3. Ciclo Temporal y Ventanas Operativas de la Cafetería

Además de las fases del proyecto, el cronograma de negocio rige la rutina diaria y semanal del mostrador para garantizar orden y seguridad en el manejo del dinero:

```
06:30 AM  ----->  Revisión automática de caducidad PEPS por el sistema (Cron Job).
07:00 AM  ----->  Apertura de turno matutino: Cajero ingresa fondo fijo en POS ($1,000 MXN).
07:00-14:30 --->  Operación continua: Venta en mostrador, lector de código de barras y Rewards.
14:30 PM  ----->  Cambio de turno: Arqueo de caja del turno matutino y relevo de cajero.
14:30-22:00 --->  Operación del turno vespertino.
22:00 PM  ----->  Cierre de caja final del día: Conteo físico de efectivo y vouchers.
22:15 PM  ----->  Generación del Reporte Z consolidado y validación del Administrador.
LUNES 09:00 --->  Revisión semanal de inventarios y envío de órdenes de compra a cooperativas.
DOMINGO 23:00 ->  Generación automática del reporte semanal de ventas y campañas en Excel/PDF.
```

---

### 4. Justificación Práctica en el Proyecto

Como destacan Gido y Clements (2012), el cronograma es la herramienta de comunicación por excelencia hacia clientes y directivos porque aterriza las promesas en fechas concretas y compromisos medibles. En Monchis Café, estructurar la adopción en cuatro fases nos evitó el error común de querer encender todo de golpe (lo que en desarrollo se conoce como *big bang*), permitiendo que los cajeros dominaran primero el cobro rápido antes de introducir la fidelización y las alertas de mermas. De este modo, la cafetería mantuvo su servicio impecable mientras el sistema se integraba de forma natural a la rutina del negocio.

---

### 5. Referencias Bibliográficas

1. **Gido, J., & Clements, J. P. (2012).** *Administración exitosa de proyectos* (5.ª ed.). Cengage Learning.
2. **Kerzner, H. (2022).** *Project Management: A Systems Approach to Planning, Scheduling, and Controlling* (13.ª ed.). John Wiley & Sons.
3. **Project Management Institute. (2017).** *A Guide to the Project Management Body of Knowledge (PMBOK Guide)* (6.ª ed.). Project Management Institute.
4. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

