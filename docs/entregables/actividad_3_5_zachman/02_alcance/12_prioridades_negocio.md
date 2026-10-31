# Nivel 2: ALCANCE — Foco: POR QUÉ
## Prioridades de Negocio — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En cualquier proyecto de desarrollo de software y de inversión empresarial, los recursos económicos, el tiempo y la capacidad del equipo de trabajo son finitos; por lo tanto, pretender construir todas las funcionalidades imaginables al mismo tiempo es el camino más directo al retraso y al fracaso presupuestal (Sapag Chain, 2011). Como explican Wiegers y Beatty (2013), priorizar los requerimientos consiste en evaluar el valor que cada funcionalidad aporta al negocio frente al costo, la complejidad técnica y el riesgo que implica desarrollarla, decidiendo qué se debe construir de manera obligatoria y qué puede esperar para etapas posteriores.

Dentro de la Matriz de Zachman (1987), la celda **Alcance - Por qué** analiza las *Prioridades de Negocio* desde la perspectiva del dueño de la empresa (*Business Priorities / Owner's View*). En este nivel conceptual aplicamos el método formal de priorización **MoSCoW** (Clegg & Barker, 1994), clasificando cada requerimiento en cuatro categorías rigurosas: *Must Have* (Imprescindible), *Should Have* (Importante), *Could Have* (Deseable) y *Won't Have* (Fuera de alcance temporal). Para Monchis Café, esta jerarquía garantiza que lo que sostiene las ventas y la seguridad de la caja esté listo antes que los adornos estéticos o funciones secundarias.

---

### 2. Clasificación MoSCoW de Requerimientos de Negocio

La siguiente tabla clasifica los requerimientos funcionales del sistema conforme a su impacto directo en la operación de la cafetería:

```
+---------------------------------------------------------------------------------------+
|                                  MÉTODO MoSCoW                                        |
+---------------------------------------------------------------------------------------+
| M (Must Have):    Esenciales para abrir la caja y operar (Innegociables).            |
| S (Should Have):  Críticos para el control de inventario y seguridad avanzada.        |
| C (Could Have):   Diferenciadores de marketing y analítica ejecutiva.                 |
| W (Won't Have):   Funcionalidades complejas reservadas para versiones futuras.        |
+---------------------------------------------------------------------------------------+
```

---

| Categoría MoSCoW | Código RF | Requerimiento Funcional | Justificación Estratégica del Negocio |
| :--- | :--- | :--- | :--- |
| **MUST HAVE**<br>*(Obligatorio para Operar)* | **RF-01** | Gestión de Catálogo y Precios Oficiales | Sin catálogo con precios blindados en el servidor, es imposible cobrar en mostrador. |
| **MUST HAVE** | **RF-03** | Registro Ágil de Ventas en Mostrador (POS) | Es el núcleo del negocio; si la terminal no registra ventas con rapidez, se forman filas. |
| **MUST HAVE** | **RF-04** | Cobro Multipago (Efectivo, Tarjeta, SPEI) | Los clientes exigen diversas formas de pago; perder una venta por no cobrar es inadmisible. |
| **MUST HAVE** | **RF-09** | Corte de Turno y Arqueo Diario de Caja | Garantiza el control estricto del dinero físico frente al sistema, evitando pérdidas. |
| **MUST HAVE** | **RF-10** | Autenticación Stateless y Google reCAPTCHA| Protege la plataforma contra bots y accesos no autorizados a las cuentas de empleados. |
| **SHOULD HAVE**<br>*(Altamente Importante)* | **RF-02** | Registro y Trazabilidad de Lotes de Café | Respalda la propuesta de café orgánico campesino frente a la competencia. |
| **SHOULD HAVE** | **RF-05** | Bonificación Ecológica por Termo (ODS 12) | Eje central de sustentabilidad ambiental que ahorra costos en vasos de polipapel. |
| **SHOULD HAVE** | **RF-06** | Programa Monchis Rewards (8 Sellos) | Motor de retención de clientes; incentiva el consumo recurrente en la sucursal. |
| **SHOULD HAVE** | **RF-07** | Control de Inventario con Rotación PEPS | Impide que el café tostado o la repostería se quede rezagada y caduque en bodega. |
| **SHOULD HAVE** | **RF-11** | Doble Factor de Autenticación (2FA Admin) | Blindaje de alta seguridad para la cuenta del dueño frente a intentos de intrusión. |
| **COULD HAVE**<br>*(Deseable / Valor Agregado)*| **RF-08** | Motor de Alertas Sanitarias por Correo SMTP | Apoyo preventivo automático ante lotes por vencer; existe control visual manual. |
| **COULD HAVE** | **RF-12** | Atribución de Campañas (Google Maps/Instagram)| Ayuda a tomar decisiones de marketing digital, aunque no interrumpe el cobro en mostrador. |
| **COULD HAVE** | **RF-13** | Exportación de Reportes en PDF y Excel | Facilita la contabilidad semanal del negocio mediante descargas en un clic. |
| **COULD HAVE** | **RF-15** | Atajos de Teclado (F2) y Lector de Códigos | Acelera la atención en mostrador, complementando la interacción táctil en pantalla. |
| **WON'T HAVE**<br>*(Fuera de Alcance v1.0)* | **W-01** | Pasarela de Pago Online con Envíos a Domicilio| Requiere logística de reparto y comisiones altas; se evaluará para la versión 2.0. |
| **WON'T HAVE** | **W-02** | Facturación Electrónica Automática CFDI 4.0 | Por ahora se maneja mediante tickets de control interno y emisión manual en portal SAT. |

---

### 3. Matriz de Valor vs. Complejidad de Implementación

Para guiar los sprints de desarrollo bajo metodología ágil, se contrastó el valor que cada requerimiento aporta a la cafetería contra el esfuerzo técnico de implementación:

```
ALTO VALOR  | [RF-03: POS Mostrador]        [RF-04: Multipago]
            | [RF-01: Catálogo Precios]     [RF-06: Monchis Rewards]
            | [RF-09: Corte de Caja Z]      [RF-05: Bono Ecológico ODS 12]
            | [RF-10: Autenticación JWT]    [RF-07: Rotación PEPS]
            |-------------------------------------------------------------
            | [RF-15: Atajos y Escáner]     [RF-02: Lotes Trazabilidad]
BAJO VALOR  | [RF-13: Exportes Excel/PDF]   [RF-11: 2FA Administrador]
            |                               [RF-12: Atribución UTM Maps]
            |                               [RF-08: Alertas SMTP]
            +-------------------------------------------------------------
                                BAJA COMPLEJIDAD             ALTA COMPLEJIDAD
```

---

### 4. Justificación Práctica en el Proyecto

Aplicar el método MoSCoW desde la perspectiva del dueño de la empresa es lo que permite entregar un Producto Mínimo Viable (MVP) funcional en el menor tiempo posible. Como señala Sapag Chain (2011), invertir recursos en funciones complejas que no aportan al flujo de caja inmediato puede poner en riesgo la viabilidad financiera de todo el proyecto. Al concentrar el primer esfuerzo en los requerimientos *Must Have*, garantizamos que la cafetería pueda abrir sus puertas, cobrar con seguridad y controlar el efectivo, dejando las optimizaciones de marketing y alertas automáticas como capas complementarias que enriquecen el sistema sin entorpecer su arranque.

---

### 5. Referencias Bibliográficas

1. **Clegg, D., & Barker, R. (1994).** *Case Method Fast-Track: A Rad Approach*. Addison-Wesley.
2. **Sapag Chain, N. (2011).** *Proyectos de inversión: Formulación y evaluación* (2.ª ed.). Pearson Prentice Hall.
3. **Wiegers, K. E., & Beatty, J. (2013).** *Software Requirements* (3.ª ed.). Microsoft Press.
4. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

