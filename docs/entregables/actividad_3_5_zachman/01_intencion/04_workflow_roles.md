# Nivel 1: INTENCIÓN — Foco: QUIÉN
## Workflow (Roles y Actividades) — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En la gestión de proyectos y la teoría de organizaciones, un flujo de trabajo (*workflow*) describe la secuencia ordenada de actividades humanas y procesos operativos necesarios para transformar insumos en productos terminados con valor para el cliente (Gido & Clements, 2012). Cuando no existe claridad sobre quién es responsable de qué tarea, el trabajo se duplica o, peor aún, se omiten pasos críticos como la verificación sanitaria de los alimentos o el control del efectivo en caja.

En la Matriz de Zachman (1987), la celda **Intención - Quién** define la estructura organizacional inicial desde la visión del planificador. En esta etapa macro no hablamos todavía de tablas de base de datos de usuarios ni de contraseñas con hash criptográfico; lo que se establece formalmente son los perfiles humanos que intervienen en el modelo de negocio, sus atribuciones y la forma en que colaboran día a día (Pressman & Maxim, 2021). Según las directrices del Project Management Institute (2017), una de las mejores herramientas para evitar vacíos de poder y malentendidos operativos es la asignación explícita de responsabilidades mediante matrices RACI.

---

### 2. Definición de Roles del Negocio

Para la operación de **Monchis Café**, se identifican cuatro roles humanos fundamentales:

```
+---------------------------------------------------------------------------------------+
|                             ROLES Y RESPONSABILIDADES                                 |
+---------------------------------------------------------------------------------------+
| 1. Administrador (Gerente)  | Máxima autoridad operativa. Controla precios, audita   |
|                             | cajas, registra lotes y analiza métricas de negocio.    |
+-----------------------------+---------------------------------------------------------+
| 2. Cajero (Barista Mostrador)| Operador en mostrador. Registra ventas en el POS, cobra |
|                             | multipago, aplica el bono ecológico y entrega cambio.   |
+-----------------------------+---------------------------------------------------------+
| 3. Cliente (Consumidor)     | Usuario final. Realiza pedidos, acumula sellos en       |
|                             | Monchis Rewards y promueve el consumo sustentable.      |
+-----------------------------+---------------------------------------------------------+
| 4. Proveedor Campesino      | Cooperativas locales (Michoacán, Oaxaca y Chiapas).     |
|                             | Suministra café de especialidad con ficha técnica.      |
+---------------------------------------------------------------------------------------+
```

---

### 3. Flujo de Trabajo Operativo (Workflow Macro)

El siguiente flujo describe cómo interactúan los cuatro roles a lo largo de una jornada típica de trabajo en la cafetería:

```
[PROVEEDOR] Entrega Lote de Café Orgánico con Ficha Técnica
     |
     v
[ADMINISTRADOR] Inspecciona Calidad, Registra Lote PEPS y Autoriza Pago
     |
     v
[CAJERO] Abre Turno en POS con Fondo Inicial de Caja
     |
     v
[CLIENTE] Llega a Mostrador con Termo Reusable y Elige Café de Especialidad
     |
     v
[CAJERO] Escanea Productos, Aplica Bono Ecológico (-$5.00) y Cobra (Efectivo/Tarjeta/SPEI)
     |
     v
[CLIENTE] Recibe Bebida Preparada, Ticket y Acumula Sello Digital en "Monchis Rewards"
     |
     v
[CAJERO] Realiza Corte de Caja al Fin del Turno (Efectivo Físico vs Sistema)
     |
     v
[ADMINISTRADOR] Audita Corte Z, Revisa Mermas y Recibe Alertas de Caducidad PEPS
```

---

### 4. Matriz de Responsabilidades (RACI)

Para formalizar la relación entre los roles y las tareas clave del negocio, aplicamos el estándar RACI conforme al PMI (2017):
* **R (Responsible):** El rol que ejecuta la actividad directamente.
* **A (Accountable):** El rol que responde en última instancia por el éxito o fracaso de la tarea (solo uno por actividad).
* **C (Consulted):** El rol que aporta información o insumos necesarios antes de la ejecución.
* **I (Informed):** El rol que es notificado una vez concluida la actividad.

| Actividad de Negocio | Proveedor | Administrador | Cajero | Cliente |
| :--- | :---: | :---: | :---: | :---: |
| **Abastecimiento y recepción de grano de café** | **R** | **A** | **I** | — |
| **Alta de lotes y fechas de caducidad en el sistema** | **C** | **A / R** | **I** | — |
| **Apertura de turno e ingreso de fondo de caja** | — | **A** | **R** | — |
| **Toma de orden y venta en mostrador (POS)** | — | **I** | **R** | **C** |
| **Validación y aplicación de Bonificación Ecológica** | — | **I** | **R** | **C** |
| **Cobro en Efectivo, Tarjeta o Transferencia SPEI** | — | **I** | **R** | **C** |
| **Asignación de sellos y cortesía en Monchis Rewards**| — | **I** | **R** | **A** |
| **Corte de caja diario y arqueo de valores** | — | **A** | **R** | — |
| **Gestión de mermas y retiro de café vencido** | — | **A** | **R** | — |
| **Revisión de analítica semanal y campañas UTM** | — | **A / R** | **I** | — |

---

### 5. Justificación Práctica en el Proyecto

Definir los roles y el workflow de trabajo desde esta etapa inicial evita confusiones clásicas en la cafetería, como que un cajero intente modificar precios de catálogo sin autorización, o que el administrador pretenda cobrar ventas sin registrarse en el sistema. Como señala Sapag Chain (2011), la viabilidad de gestión y administrativa de un proyecto depende de qué tan claras estén las líneas de autoridad. Al tener este mapa de roles, el desarrollo del sistema puede modelar con precisión los permisos de seguridad y las pantallas que cada empleado verá al entrar a trabajar.

---

### 6. Referencias Bibliográficas

1. **Gido, J., & Clements, J. P. (2012).** *Administración exitosa de proyectos* (5.ª ed.). Cengage Learning.
2. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
3. **Project Management Institute. (2017).** *A Guide to the Project Management Body of Knowledge (PMBOK Guide)* (6.ª ed.). Project Management Institute.
4. **Sapag Chain, N. (2011).** *Proyectos de inversión: Formulación y evaluación* (2.ª ed.). Pearson Prentice Hall.
5. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

