# Gestión Web Segura para Cafetería Orgánica y Comercial

## Características del Proyecto Final

### Problemática Detectada
La cafetería “inserta nombre del proyecto” es un negocio familiar ubicado en una zona rural. Aunque ofrece café orgánico de gran calidad, no lo produce directamente, sino que depende de distintos proveedores regionales. Además, vende productos complementarios comprados en tiendas mayoristas como Sam’s y Costco (galletas, leche vegetal, postres, etc.).

**Actualmente:**
- No existe un control digital de inventario ni de pedidos.
- No se lleva seguimiento de proveedores ni entregas.
- No hay trazabilidad de productos orgánicos (origen, lote, fecha).
- El control de caja y ventas es manual, lo que limita la transparencia.
- No se gestiona la seguridad de los datos personales ni de pagos electrónicos.
- La fidelización del cliente es nula (no hay registros ni promociones digitales).
- Se ignoran posibles alertas sanitarias o trazabilidad de productos orgánicos.

### Objetivo General
Diseñar y desarrollar una aplicación web segura que permita la gestión integral de productos, proveedores, inventario, pedidos y ventas de la cafetería, incorporando mecanismos de seguridad informática, usabilidad, y alineación con los ODS, además de facilitar la trazabilidad de productos orgánicos mediante buenas prácticas de desarrollo web.

### ODS Asociados
- **ODS 8: Trabajo decente y crecimiento económico:** Optimiza procesos operativos y administrativos.
- **ODS 9: Industria, innovación e infraestructura:** Digitalización en zonas rurales.
- **ODS 12: Producción y consumo responsables:** Gestión y trazabilidad de productos.
- **ODS 16: Paz, justicia e instituciones sólidas:** Protección de datos y gestión ética de la información.

---

## Componentes del Sistema Web

### Panel para el Administrador (dueño o encargado)
- Gestión de productos (orgánicos y comerciales).
- Registro de proveedores y fechas de compra.
- Visualización de inventarios (mínimos, expiraciones).
- Reportes semanales en PDF y Excel.
- Control de usuarios con distintos niveles de acceso.

### Módulo de Ventas
- Registro de ventas diario (manual o con lector de códigos).
- Control de caja (ingresos por día).
- Emisión de tickets digitales o físicos.

### Módulo de Trazabilidad
- Registro del lote, proveedor y origen del café orgánico.
- Alerta en caso de vencimientos o anomalías.

### Módulo de Clientes
- Registro básico (nombre, correo).
- Histórico de compras.
- Sistema de recompensas o promociones.

### Seguridad de la Información
- Autenticación con doble factor para el administrador.
- Cifrado de datos sensibles (contraseñas, datos de clientes).
- Control de sesiones y logs de actividad.
- Roles de usuario definidos.
- Copias de seguridad periódicas.

---

## Tecnologías sugeridas
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap, Vue.js o React.
- **Backend:** Node.js + Express o Django.
- **Base de Datos:** PostgreSQL o MySQL (con cifrado).
- **Seguridad:** JWT, bcrypt, HTTPS, control de sesiones.
- **Otras herramientas:** Trello (Scrum), GitHub, Figma, Canva.
- **APIs externas:** Notificaciones por correo (SendGrid), autenticación (Auth0).

---

## Funcionalidades adicionales sugeridas (elige al menos 5)
1. Registro de productos por tipo (orgánico o comercial).
2. Control de caducidad con alertas.
3. Generación de reportes de compras y ventas.
4. Módulo de fidelización de clientes.
5. Panel de control con métricas de negocio.
6. Trazabilidad de lotes y productos con alertas sanitarias.
7. Gestión de pedidos a proveedores con historial.
8. Backup automático de la base de datos.
9. Control de permisos y roles (seguridad web).
10. Exportación de información a formatos PDF/Excel.

---

## Plan de Acción

### Fase de Diseño
- Mockups con Figma.
- Modelo entidad-relación (MER).
- Diagrama de casos de uso y arquitectura general.

### Fase de Desarrollo
- Backend seguro con Express/Django.
- Frontend responsivo con React o Vue.
- Implementar roles y permisos desde el backend.
- Protección de rutas, cifrado de contraseñas, validaciones de inputs.

### Fase de Integración
- Conexión entre módulos.
- Carga segura de archivos.
- Integración con correo electrónico.

### Fase de Pruebas
- Pruebas de funcionalidades básicas.
- Pruebas de seguridad (sesiones, datos).
- Simulación de ataques comunes (XSS, SQLi, etc.).

### Fase de Lanzamiento
- Despliegue en servidor local o en hosting (Heroku, Vercel).
- Manual de usuario y documentación técnica.
- Video demostrativo del sistema.

---

## RÚBRICA DE EVALUACIÓN – PROYECTO INTEGRADOR

- **Nombre del Proyecto:** Plataforma Web Segura para Cafetería de Café Orgánico
- **Modalidad:** Programación Web + Seguridad de la Información
- **ODS Relacionados:**
  - ODS 12: Producción y consumo responsables
  - ODS 8: Trabajo decente y crecimiento económico
  - ODS 9: Industria, innovación e infraestructura

| Criterio | Excelente (10 pts) | Satisfactorio (8 pts) | Regular (6 pts) | Insuficiente (≤5 pts) | Ponderación |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Documentación Técnica** | El proyecto incluye todos los apartados: análisis, requerimientos, modelos, diseño, pruebas y plan de mejora. Redacción impecable. | Incluye la mayoría de los apartados requeridos. Redacción clara. | Faltan secciones importantes o hay errores de redacción. | Documentación incompleta o muy pobre. | 15% |
| **2. Diseño Web y Experiencia de Usuario (UX/UI)** | Interfaz atractiva, intuitiva y accesible. Incluye mockups, wireframes y estructura clara. | Interfaz funcional con buena organización. Puede mejorar la estética o accesibilidad. | Interfaz poco clara, con diseño básico o confuso. | Interfaz deficiente o ausente. | 10% |
| **3. Seguridad de la Información** | Integra medidas como cifrado, roles de usuario, autenticación segura y protección de datos. | Se aplican algunas medidas de seguridad básicas (login, HTTPS, sesiones). | Se mencionan medidas pero no se implementan o son débiles. | No se considera la seguridad en la solución. | 10% |
| **4. Funcionalidad del Sistema Web** | El sistema registra pedidos, controla inventario, gestiona proveedores y genera reportes. Todo operativo. | Funciona la mayoría de los módulos, aunque con detalles mínimos por corregir. | Funciona solo una parte del sistema; fallan procesos clave. | El sistema no ejecuta correctamente las funciones básicas. | 15% |
| **5. Relación con los ODS y Sustentabilidad** | Claramente se integran soluciones a problemáticas relacionadas con los ODS seleccionados. | La solución hace mención a los ODS pero sin acciones claras. | Referencia vaga a los ODS, sin aplicación práctica. | No se relaciona el proyecto con ningún ODS. | 10% |
| **6. Innovación y uso de tecnologías** | Se hace uso avanzado de tecnologías web modernas (frameworks, APIs, bases de datos, cloud, etc.). | Se usa una tecnología adecuada para el contexto. | Uso limitado de tecnología, sin aprovechar su potencial. | Uso inadecuado o inexistente de herramientas tecnológicas. | 10% |
| **7. Presentación final y entrega** | Presentación clara, estructurada y convincente. Entrega de ZIP funcional, manual técnico y de usuario. | Presentación correcta, aunque poco clara en algunos apartados. Entrega con detalles menores. | Presentación confusa o incompleta. Fallos en entrega. | Presentación deficiente o sin entregables. | 15% |
| **8. Presentación del proyecto en EXPODIT** | Exposición profesional, dominio del tema, tiempos adecuados y respuesta precisa a preguntas técnicas. | Presentación adecuada pero con áreas de mejora en exposición o dominio del tema. | Presentación con fallas importantes, poco dominio o sin claridad. | Sin presentación o con errores graves. | 15% |

---

## Documentación
- **Visualización de la presentación:** [Proyecto Integrador en el Desarrollo de Software](https://docs.google.com/presentation/d/1qjuHkkxNJTr4Qt2Ci-aMF44tRKtypyPXrkCJI0NYucE/edit?usp=sharing)

### Notas adicionales sobre metodologías:
- **Metodologías ágiles (Scrum, Kanban, etc.):** deben aplicarse cuando el equipo está compuesto por 4 personas. La documentación debe incluir:
  - Roles del equipo (Scrum Master, Product Owner, etc.).
  - Backlog de producto.
  - Sprint planning y retrospectivas.
  - Tareas en un tablero ágil (Jira, Trello, etc.).
  - Entregas incrementales (MVP).
- **Metodología tradicional (Cascada, espiral, etc.):** puede ser aplicada si el equipo tiene menos de 4 personas. Debe incluir:
  - Diagrama de Gantt o cronograma.
  - Fases de desarrollo bien definidas.
  - Documentación detallada en cada etapa (análisis, diseño, implementación, pruebas).

### Criterios adicionales
- **Penalizaciones:** Por entregas tardías o incumplimiento de requisitos específicos.
- **Bonificaciones:** Por incluir funcionalidades adicionales no requeridas o destacar en la calidad de implementación.
