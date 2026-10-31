# Nivel 3: ALTO NIVEL — Foco: CUÁNDO
## Precedencia de Casos de Uso — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En el análisis de requerimientos con UML, los casos de uso no se ejecutan de manera aislada ni en cualquier orden arbitrario; existen dependencias lógicas, condiciones de precedencia y secuencias temporales estrictas que determinan cuándo un caso de uso puede comenzar y qué otro debe haber terminado con éxito previamente (Pressman & Maxim, 2021). Como señala Larman (2004), establecer la precedencia entre casos de uso permite al equipo de arquitectura definir la máquina de estados del negocio y modelar las relaciones formales de UML como `<<include>>` (inclusión obligatoria de un subflujo) y `<<extend>>` (extensión condicional ante eventos específicos).

Dentro de la Matriz de Zachman (1987), la celda **Alto Nivel - Cuándo** captura la dimensión temporal lógica (*System Timing / Designer's View*). En este nivel no hablamos de fechas de calendario ni de semanas de un diagrama de Gantt; lo que se formaliza es el *orden de precedencia y ejecución de los casos de uso*: *¿Qué caso de uso debe completarse primero para que otro pueda dispararse?* (Object Management Group [OMG], 2017). Si un programador no programa estas restricciones en el backend, un usuario podría intentar cobrar una venta sin haber abierto la caja o intentar consultar reportes sin haber iniciado sesión.

---

### 2. Tipos de Relaciones y Precedencia en Monchis Café

Para organizar la secuencia lógica de los 12 casos de uso del sistema, se definen tres tipos de reglas de precedencia:

```
+---------------------------------------------------------------------------------------+
|                          REGLAS LÓGICAS DE PRECEDENCIA                                |
+---------------------------------------------------------------------------------------+
| 1. Precedencia Obligatoria (-->):  CU-A debe completarse antes de iniciar CU-B.        |
| 2. Inclusión (<<include>>):        CU-B se ejecuta siempre como parte interna de CU-A.|
| 3. Extensión (<<extend>>):         CU-B solo se ejecuta si se cumple una condición.   |
+---------------------------------------------------------------------------------------+
```

---

### 3. Matriz de Precedencia y Dependencias Lógicas

| Caso de Uso | Nombre del Caso de Uso | Casos de Uso Predecesores Obligatorios | Relación UML con otros Casos de Uso | Condición de Activación / Disparo |
| :--- | :--- | :--- | :--- | :--- |
| **CU-01** | Iniciar Sesión con Google reCAPTCHA | Ninguno (Punto de entrada) | — | Disparo por usuario en `/login`. |
| **CU-02** | Autenticar Administrador con 2FA | **CU-01** (con rol 'ADMIN') | `<<include>>` desde CU-01 para Admin | Credenciales válidas de usuario administrador. |
| **CU-07** | Registrar Lote Campesino (PEPS) | **CU-01 + CU-02** | Habilita stock para CU-03 | Administrador autenticado con sesión 2FA. |
| **CU-03** | Registrar Venta en Mostrador (POS)| **CU-01** (con rol 'CAJERO') | Requiere lote activo de CU-07 | Cajero autenticado con turno abierto. |
| **CU-05** | Aplicar Bonificación Ecológica | **CU-03** (en edición de orden) | `<<extend>>` sobre CU-03 | El cliente presenta termo o taza reusable. |
| **CU-04** | Procesar Cobro Multipago en Caja | **CU-03** (orden lista para cobro) | `<<include>>` de CU-03 | Cajero presiona cobro rápido [F2]. |
| **CU-06** | Canjear Bebida Monchis Rewards | **CU-04** (al calcular total) | `<<extend>>` sobre CU-04 | El cliente acumula 7 sellos verificados. |
| **CU-12** | Orquestar Reversa Saga | **CU-04** (orden cobrada) | `<<extend>>` excepcional sobre CU-04 | Ruptura física de stock de café en barra. |
| **CU-08** | Ejecutar Arqueo y Corte de Caja Z | **CU-04** (al fin de turno) | Consolida ventas de CU-04 | Finalización de jornada laboral en POS. |
| **CU-09** | Consultar Analítica y UTM Maps | **CU-01 + CU-02** | Lee datos generados por CU-04 | Administrador autenticado en `/admin`. |
| **CU-10** | Exportar Reportes (PDF/Excel) | **CU-09** | `<<extend>>` sobre CU-09 | Clic en botones de exportación en panel. |
| **CU-11** | Despachar Alertas Sanitarias | Ninguno (Cron temporal diario) | Lee lotes registrados en CU-07 | Disparo automático a las 06:30 AM. |

---

### 4. Grafo Dirigido de Precedencia Lógica

El siguiente flujo ilustra el encadenamiento secuencial y las bifurcaciones lógicas entre los casos de uso:

```
[CU-01: Login reCAPTCHA]
        |
        +---- (Si es ADMIN) ----> [CU-02: 2FA TOTP]
        |                                 |
        |                                 +-----> [CU-07: Registro Lote PEPS]
        |                                 |                 | (Alimenta Stock)
        |                                 |                 v
        |                                 +-----> [CU-09: Analítica UTM]
        |                                                   |
        |                                                   v
        |                                         [CU-10: Exportar PDF/Excel]
        |
        +---- (Si es CAJERO) ---> [CU-03: Venta en Mostrador POS] <---+
                                          |                           |
                  (¿Trae Termo?) --------+---- <<extend>> ---------> [CU-05: Bono Ecológico]
                                          |
                                          v
                                  [CU-04: Cobro Multipago]
                                          |
                  (¿Tiene 7 sellos?) ----+---- <<extend>> ---------> [CU-06: 8vo Café Gratis]
                  (¿Falta de grano?) ----+---- <<extend>> ---------> [CU-12: Reversa Saga]
                                          |
                                          v
                                  [CU-08: Corte de Caja Diario Z]

[Cron Job 06:30 AM] ------------> [CU-11: Alertas Sanitarias SMTP]
```

---

### 5. Justificación Práctica en el Proyecto

Mapear la precedencia de los casos de uso es lo que le permite al desarrollador implementar correctamente los *Navigation Guards* en Vue Router y los middlewares de seguridad en la API de Next.js. Como señalan Pressman y Maxim (2021), un sistema que no controla el orden de ejecución es vulnerable a condiciones de carrera (*race conditions*) y a inconsistencias en la base de datos. En Monchis Café, garantizar que no se pueda cobrar (CU-04) si no hay una orden abierta con precios validados (CU-03), o que el bono ecológico (CU-05) solo pueda aplicarse antes de emitir el cobro final, es lo que blinda la integridad financiera de la cafetería.

---

### 6. Referencias Bibliográficas

1. **Larman, C. (2004).** *Applying UML and Patterns: An Introduction to Object-Oriented Analysis and Design and Iterative Development* (3.ª ed.). Prentice Hall.
2. **Object Management Group. (2017).** *OMG Unified Modeling Language (OMG UML), Version 2.5.1*. OMG Document Number: formal/2017-12-05. https://www.omg.org/spec/UML/2.5.1/
3. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
4. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

