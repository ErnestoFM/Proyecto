# Nivel 2: ALCANCE — Foco: DÓNDE
## Ambiente Operativo y Requerimientos No Funcionales — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

Los requerimientos no funcionales (RNF), conocidos formalmente en la arquitectura de software como atributos de calidad, definen las restricciones de rendimiento, seguridad, confiabilidad y ambiente operativo bajo las cuales el sistema debe trabajar (Bass et al., 2012). No se trata de qué hace el software (eso lo resuelven los requerimientos funcionales), sino de *cómo se comporta y bajo qué condiciones técnicas lo hace* (ISO/IEC 25010, 2011). Un sistema de punto de venta puede registrar ventas de manera impecable, pero si tarda dos minutos en imprimir un ticket o se cae cuando hay diez clientes formados, el negocio colapsa en la práctica.

Dentro de la Matriz de Zachman (1987), la celda **Alcance - Dónde** establece el ambiente operativo y los requerimientos no funcionales desde la perspectiva del dueño del negocio (*Business Model / Owner's View*). En este nivel no nos quedamos en la teoría abstracta; definimos las condiciones físicas de las terminales de mostrador, la infraestructura de servidores donde se hospeda el sistema y los estándares mínimos de seguridad que blindan la información del negocio frente a fraudes y caídas de red (Pressman & Maxim, 2021).

---

### 2. Definición del Ambiente Operativo

El sistema **Monchis Café** está diseñado bajo un modelo híbrido y desacoplado que garantiza disponibilidad tanto en la nube para la administración y clientes, como en red local para la terminal de mostrador:

```
+---------------------------------------------------------------------------------------+
|                                AMBIENTES OPERATIVOS                                   |
+---------------------------------------------------------------------------------------+
| 1. Ambiente Cloud (Producción):     Google Cloud Run (Serverless OCI) en us-central1, |
|                                     certificados TLS 1.3 gestionados por Google.      |
+-------------------------------------+-------------------------------------------------+
| 2. Ambiente Local (Staging / POS):  Docker Compose orquestando 6 contenedores         |
|                                     (Nginx, Web Vue 3, API Node, Postgres, RabbitMQ). |
+-------------------------------------+-------------------------------------------------+
| 3. Hardware de Mostrador:           Terminal táctil / PC con Windows o Linux,          |
|                                     lector óptico USB/HID 1D/2D e impresora térmica.   |
+-------------------------------------+-------------------------------------------------+
| 4. Dispositivos del Cliente:        Navegadores web modernos (Chrome, Safari, Edge)   |
|                                     en smartphones iOS y Android para Monchis Rewards.|
+---------------------------------------------------------------------------------------+
```

---

### 3. Matriz de Requerimientos No Funcionales (Estándar ISO/IEC 25010)

Para clasificar los atributos de calidad de forma rigurosa y verificable, adoptamos las directrices de la norma internacional **ISO/IEC 25010 (SQuaRE)**:

| Categoría ISO/IEC | Código | Nombre del RNF | Métrica y Criterio de Aceptación |
| :--- | :--- | :--- | :--- |
| **Eficiencia de Desempeño** | **RNF-01** | **Latencia en Punto de Venta** | El tiempo de respuesta al escanear un producto o agregar un ítem al carrito en el POS debe ser inferior a **100 milisegundos**. El tiempo de procesamiento total de cobro no debe exceder de **500 milisegundos**. |
| **Seguridad de la Información** | **RNF-02** | **Cifrado y Autenticación Stateless** | Todas las comunicaciones deben forzar **HTTPS con TLS 1.3**. El acceso se gestiona mediante tokens JWT en memoria (expiración de 15 min) y Refresh Tokens rotativos en cookies `httpOnly + Secure + SameSite=Strict`. Las contraseñas se almacenan con hash `bcrypt` (factor de costo 12). |
| **Seguridad Anti-Fraude** | **RNF-03** | **Protección contra Bots y Brute Force** | Los formularios públicos (login y registro) deben validar obligatoriamente tokens de **Google reCAPTCHA v2/v3**. El sistema debe bloquear temporalmente por 15 minutos cualquier IP que acumule 5 intentos fallidos consecutivos de acceso. |
| **Fiabilidad y Disponibilidad** | **RNF-04** | **Disponibilidad de Servicio (SLA)** | El sistema debe ofrecer una disponibilidad del **99.5%** durante el horario comercial de la cafetería (07:00 a 22:00 horas). En caso de intermitencia de red externa, el POS debe operar en modo de degradación controlada mediante almacenamiento local (*Pinia persist*). |
| **Usabilidad y Ergonomía** | **RNF-05** | **Interfaz de Mostrador Táctil** | Los botones de cobro y catálogo en la pantalla del POS deben tener un tamaño táctil mínimo de **48x48 píxeles** con paleta pastel de alto contraste (relación mínima 4.5:1), cumpliendo con el estándar de accesibilidad **WCAG 2.1 nivel AA**. |
| **Mantenibilidad y Modularidad** | **RNF-06** | **Arquitectura Monorepo Tipada** | El código debe mantenerse desacoplado en un Monorepo con `pnpm workspaces` y `Turborepo`, compartiendo contratos TypeScript (`@monchis/shared-types`) y manteniendo una cobertura de pruebas unitarias superior al **80%** en componentes críticos. |
| **Compatibilidad** | **RNF-07** | **Integración con Periféricos HID** | El sistema debe recibir entradas de escáneres de código de barras estándar (USB/Bluetooth) emulando teclado humano (HID) sin requerir controladores privativos. |

---

### 4. Justificación Práctica en el Proyecto

Los requerimientos no funcionales son los que salvan a un proyecto de fracasar en el mundo real. Como señalan Bass, Clements y Kazman (2012), si la arquitectura no contempla los atributos de calidad desde el principio, es prácticamente imposible "parcharlos" al final cuando el sistema ya está programado. En Monchis Café, garantizar que el POS responda en menos de medio segundo y que la sesión no se pierda si parpadea el internet de la cafetería es lo que asegura que el cliente no se desespere en la fila y que los baristas puedan concentrarse en preparar un excelente café.

---

### 5. Referencias Bibliográficas

1. **Bass, L., Clements, P., & Kazman, R. (2012).** *Software Architecture in Practice* (3.ª ed.). Addison-Wesley.
2. **ISO/IEC. (2011).** *ISO/IEC 25010:2011 Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models*. International Organization for Standardization.
3. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
4. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

