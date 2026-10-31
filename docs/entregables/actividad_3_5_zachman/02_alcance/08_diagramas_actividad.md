# Nivel 2: ALCANCE — Foco: CÓMO
## Diagramas de Actividad UML — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En el estándar de modelado UML (Unified Modeling Language), el diagrama de actividad se utiliza para representar de forma gráfica los flujos de control y de datos que ocurren a lo largo de un proceso de negocio o de un caso de uso (Object Management Group [OMG], 2017). A diferencia de un simple diagrama de flujo tradicional, el diagrama de actividad de UML incorpora elementos formales como nodos iniciales y finales, bifurcaciones de decisión (*decision nodes*), barras de sincronización (*fork/join*) y, muy especialmente, carriles de responsabilidad o particiones (*swimlanes*) (Booch et al., 2005).

Dentro de la Matriz de Zachman (1987), la celda **Alcance - Cómo** modela los procesos de negocio en detalle (*Business Process Model*). En este nivel conceptual, ya no nos limitamos a listar los nombres de los procesos como hicimos en la fila de Intención; aquí desglosamos paso a paso cómo se ejecutan las actividades, qué decisiones se toman en el camino y qué actor o componente del sistema es responsable de cada acción (Pressman & Maxim, 2021). Para Monchis Café, dos procesos son el corazón operativo del negocio: el cobro ágil en mostrador con incentivos ecológicos y la recepción de café campesino con control de caducidad PEPS.

---

### 2. Diagrama de Actividad 1: Venta en Mostrador y Bono Ecológico (DA-01)

Este diagrama modela el flujo completo desde que el cliente se acerca a la barra de café hasta que sale con su bebida, su ticket y sus sellos de lealtad acumulados:

```
+-------------------+--------------------+----------------------+-----------------------+
|      CLIENTE      |       CAJERO       |     SISTEMA POS      |   PASARELA BANCARIA   |
+-------------------+--------------------+----------------------+-----------------------+
|         O (Inicio)|                    |                      |                       |
|         |         |                    |                      |                       |
|  Pide café o      |                    |                      |                       |
|  alimento         |                    |                      |                       |
|         |-------->| Recibe pedido y    |                      |                       |
|                   | escanea producto   |                      |                       |
|                   |         |--------->| Agrega item a orden  |                       |
|                   |                    | y calcula subtotal   |                       |
|  ¿Presenta termo  |                    |         |            |                       |
|   reutilizable?   |                    |         |            |                       |
|    /         \    |                    |         |            |                       |
|  (SÍ)        (NO) |                    |         |            |                       |
|   |            |  |                    |         |            |                       |
|   v            v  |                    |         |            |                       |
| Muestra      Pide | Activa casilla de  | Aplica -$5.00 MXN o  |                       |
| termo        vaso | "Bono Ecológico"   | doble sello ODS 12   |                       |
|   |            |  |         |--------->|         |            |                       |
|   +-----+------+  |                    |         v            |                       |
|         |         |                    | Despliega Total      |                       |
|  Selecciona forma |                    |         |            |                       |
|  de pago          |                    |         |            |                       |
|    /    |    \    |                    |         |            |                       |
|[Efectivo][Tarjeta][SPEI]               |         |            |                       |
|    |    |    |    |                    |         |            |                       |
|    v    |    |    | Recibe dinero y    | Calcula cambio y     |                       |
| Entrega |    |    | digita monto       | valida monto         |                       |
| dinero  |    |    |         |--------->|         |            |                       |
|         v    |    |                    |         |            |                       |
|       Desliza|    | Solicita cobro en  | Envía petición       | Procesa transacción   |
|       tarjeta|    | terminal física    | de cargo ------------| y emite autorización  |
|              v    |                    |                      |         |             |
|          Transfiere| Solicita clave de | Registra clave de    |         |             |
|          por SPEI | rastreo bancaria   | rastreo bancaria     |         |             |
|              |    |         |--------->|         |            |         |             |
|              +----+---------+----------+---------+------------+---------+             |
|                                                  | <--------------------+             |
|                                                  v                                    |
|                                        Genera orden 'PAGADA',                         |
|                                        decrementa stock PEPS                          |
|                                        y suma sellos Rewards                          |
|                                                  |                                    |
|                   | Entrega bebida,    |<--------+                                    |
|                   | cambio y ticket    |                                              |
| Recibe producto,  |<--------|          |                                              |
| cambio y ticket   |                    |                                              |
|         |         |                    |                                              |
|       (Fin)       |                    |                                              |
+-------------------+--------------------+----------------------+-----------------------+
```

---

### 3. Diagrama de Actividad 2: Abastecimiento de Café y Alerta PEPS (DA-02)

Este diagrama representa cómo se garantiza la frescura del café orgánico y se previene el desperdicio de materia prima (Meta 12.3 de los ODS):

```
+--------------------+---------------------+---------------------+----------------------+
| PROVEEDOR CAMPESINO|    ADMINISTRADOR    | SISTEMA MONCHIS CAFÉ|    SERVICIO SMTP     |
+--------------------+---------------------+---------------------+----------------------+
|         O (Inicio) |                     |                     |                      |
|         |          |                     |                     |                      |
| Entrega costales   |                     |                     |                      |
| de café orgánico y |                     |                     |                      |
| ficha de tueste    |                     |                     |                      |
|         |--------->| Inspecciona calidad |                     |                      |
|                    | física del grano    |                     |                      |
|                    | y humedad           |                     |                      |
|                    |     /         \     |                     |                      |
|                    |  [Aceptado] [Rechazado]                   |                      |
|                    |     |            |  |                     |                      |
|                    |     v            v  |                     |                      |
|                    | Registra lote  Devuelve costal            |                      |
|                    | en sistema     al proveedor               |                      |
|                    | (Finca, Altura,     |                     |                      |
|                    |  Tueste, Caduc)   (Fin)                   |                      |
|                    |     |-------------->| Almacena Lote con   |                      |
|                    |                     | estado 'DISPONIBLE' |                      |
|                    |                     | en cola PEPS        |                      |
|                    |                     |         |           |                      |
|                    |                     | (Evaluación diaria) |                      |
|                    |                     |         |           |                      |
|                    |                     | ¿Caducidad <15 días?|                      |
|                    |                     |     /        \      |                      |
|                    |                     |  (SÍ)        (NO)   |                      |
|                    |                     |   |            |    |                      |
|                    |                     |   v            v    |                      |
|                    |                     | Genera alerta  Mantener                    |
|                    |                     | de caducidad   rotación                    |
|                    |                     | preventiva     normal                      |
|                    |                     |   |---------------->| Envía correo a       |
|                    | Recibe correo con   |<--------------------| bandeja de gerencia  |
|                    | aviso de lote por   |                     |                      |
|                    | vencer y ordena     |                     |                      |
|                    | rotación prioritaria|                     |                      |
|                    |         |           |                     |                      |
|                    |       (Fin)         |                     |                      |
+--------------------+---------------------+---------------------+----------------------+
```

---

### 4. Justificación Práctica en el Proyecto

Los diagramas de actividad con carriles (*swimlanes*) son una herramienta clave para el equipo porque hacen visibles las responsabilidades cruzadas. Como señalan Booch et al. (2005), muchas fallas en los sistemas ocurren en las transiciones de una persona a otra o en los puntos de decisión. En Monchis Café, modelar visualmente el bono ecológico garantiza que el cajero sepa en qué momento exacto preguntar por el termo antes de cobrar; de igual forma, el flujo de abastecimiento asegura que ningún grano de café entre a la bodega sin que el sistema registre su fecha de caducidad para el control automático de mermas.

---

### 5. Referencias Bibliográficas

1. **Booch, G., Rumbaugh, J., & Jacobson, I. (2005).** *The Unified Modeling Language User Guide* (2.ª ed.). Addison-Wesley.
2. **Object Management Group. (2017).** *OMG Unified Modeling Language (OMG UML), Version 2.5.1*. OMG Document Number: formal/2017-12-05. https://www.omg.org/spec/UML/2.5.1/
3. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
4. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

