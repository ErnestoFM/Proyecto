# Nivel 3: ALTO NIVEL — Foco: CÓMO
## Especificación de Casos de Uso Principales — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

Una simple lista de nombres de casos de uso no es suficiente para que un equipo de desarrollo programe sin ambigüedades; se requiere una especificación formal y estructurada conocida en la ingeniería de software como plantilla de caso de uso detallada (*fully dressed use case*) (Cockburn, 2000). Como señalan Larman (2004) y Pressman y Maxim (2021), especificar un caso de uso implica redactar de forma minuciosa el flujo básico o "camino feliz" (*main success scenario*), las precondiciones necesarias antes de arrancar, las postcondiciones que garantizan el éxito y todos los flujos alternativos o excepciones que pueden presentarse cuando algo sale mal.

Dentro de la Matriz de Zachman (1987), la celda **Alto Nivel - Cómo** aborda la especificación lógica del comportamiento del sistema (*Logical Process Model / Designer's View*). En este nivel traducimos las intenciones del negocio en secuencias formales de interacción. A continuación se presentan las especificaciones detalladas de los tres casos de uso más críticos para la operación de **Monchis Café**: la autenticación segura, la venta en mostrador con bono ecológico y la reversa transaccional compensatoria.

---

### 2. Especificación Formal de Casos de Uso Principales

#### Ficha 1: CU-01 — Iniciar Sesión con Google reCAPTCHA y JWT Stateless
* **Identificador:** CU-01
* **Nombre:** Iniciar Sesión con Google reCAPTCHA y JWT Stateless
* **Actor Principal:** Empleado (Cajero / Administrador)
* **Actores Secundarios:** Servicio Cloud de Google reCAPTCHA
* **Precondición:** El usuario debe estar registrado activamente en la base de datos y tener conectividad de red.
* **Postcondición:** Se entrega un Access Token JWT de 15 minutos en memoria, se establece la cookie `httpOnly` con el Refresh Token de 7 días y se redirige a la pantalla correspondiente según el rol (`/pos` o `/admin`).
* **Disparador:** El empleado ingresa sus credenciales en el formulario web de acceso.

```
FLUJO PRINCIPAL (Camino Feliz):
1. El usuario accede a la pantalla de login (/login) e ingresa su correo electrónico y contraseña.
2. El widget de Google reCAPTCHA v2/v3 genera un token criptográfico de verificación anti-bot en el cliente.
3. El usuario presiona el botón "Iniciar Sesión".
4. El frontend envía la petición POST a /api/auth/login con email, password y g-recaptcha-response.
5. El backend valida el token con la API oficial de Google (https://www.google.com/recaptcha/api/siteverify).
6. Google responde con éxito (success: true, score >= 0.5).
7. El backend busca el usuario en PostgreSQL y comprueba la contraseña mediante hash bcrypt (costo 12).
8. Si las credenciales son correctas y el rol es 'CAJERO', genera los tokens JWT stateless (Access Token con jti único).
9. El backend inyecta la cookie httpOnly + Secure + SameSite=Strict con el Refresh Token y retorna HTTP 200.
10. El frontend almacena el Access Token en Pinia y redirige al cajero a la terminal de ventas (/pos).

FLUJOS ALTERNATIVOS Y EXCEPCIONES:
* 5a. Token de reCAPTCHA inválido o ausente:
  - El backend rechaza la petición con HTTP 403 Forbidden ("Verificación de seguridad anti-bot fallida").
* 7a. Contraseña incorrecta o usuario inactivo:
  - El sistema incrementa el contador de intentos fallidos en Redis y retorna HTTP 401 ("Credenciales inválidas").
  - Si se acumulan 5 intentos fallidos en menos de 15 minutos, bloquea temporalmente la IP (RN-07).
* 8a. El usuario tiene rol 'ADMIN':
  - Se suspende la emisión del token final y el sistema desvía al flujo de CU-02 (Desafío de Segundo Factor 2FA).
```

---

#### Ficha 2: CU-03 / CU-04 — Venta en Mostrador, Bono Ecológico y Cobro Multipago
* **Identificador:** CU-03 / CU-04
* **Nombre:** Registrar Venta en Mostrador, Aplicar Bono Ecológico y Procesar Cobro Multipago
* **Actor Principal:** Cajero de Turno (Barista)
* **Actores Secundarios:** Cliente, Pasarela Bancaria
* **Precondición:** El cajero debe tener sesión iniciada en `/pos` y la caja debe estar abierta con fondo inicial.
* **Postcondición:** La orden se almacena en PostgreSQL en estado `PAGADA`, se decrementa el stock de café aplicando rotación PEPS, se suman sellos en Monchis Rewards y se imprime/envía el ticket.
* **Disparador:** Un cliente solicita bebidas o alimentos en la barra de atención.

```
FLUJO PRINCIPAL (Camino Feliz):
1. El cajero agrega productos a la orden mediante lectura óptica de código de barras o teclado táctil.
2. El sistema consulta los precios oficiales del catálogo en el servidor y calcula subtotal e IVA.
3. El cajero verifica si el cliente trae termo o taza personal y presiona la tecla o botón "Bono Ecológico".
4. El sistema aplica el descuento de $5.00 MXN en el total o duplica los sellos asignados (ODS 12).
5. El cliente indica el método de pago deseado:
   - Si es Efectivo: El cajero digita el monto recibido y el sistema calcula y despliega el cambio exacto.
   - Si es Tarjeta: El cajero solicita cobro en la terminal bancaria e ingresa el código de autorización.
   - Si es Transferencia/SPEI: El cajero ingresa la clave de rastreo bancaria provista por el cliente.
6. El cajero presiona la tecla de cobro rápido [F2].
7. El backend procesa la transacción atómica (prisma.$transaction):
   a) Crea el registro Order y sus OrderItems.
   b) Decrementa las existencias del lote orgánico más antiguo (PEPS).
   c) Si el cliente está registrado en Rewards, añade 1 sello digital.
8. La orden pasa al estado 'PAGADA'.
9. El sistema emite el ticket de compra y limpia automáticamente la pantalla para el siguiente cliente.

FLUJOS ALTERNATIVOS Y EXCEPCIONES:
* 5a. El cliente cuenta con 7 sellos en Monchis Rewards:
  - El sistema activa CU-06 y descuenta el 100% del costo de la bebida preparada ($0.00 cortesía).
* 7a. Interrupción de red externa durante el cobro:
  - El sistema activa el almacenamiento local seguro en memoria del navegador y encola la sincronización.
```

---

#### Ficha 3: CU-12 — Orquestar Reversa Transaccional Compensatoria (Saga)
* **Identificador:** CU-12
* **Nombre:** Orquestar Reversa Transaccional Compensatoria (Patrón Saga ante Ruptura de Stock)
* **Actor Principal:** Sistema Informático (Worker RabbitMQ)
* **Actores Secundarios:** Cajero, Administrador
* **Precondición:** Se registró una orden en estado `PAGADA` pero el barista detecta en barra que el grano orgánico del lote asignado se agotó físicamente o presentó contaminación antes de servir.
* **Postcondición:** La orden pasa al estado `CANCELADA_REEMBOLSADA`, se reintegra el dinero al cliente, se anula la suma de sellos y se genera un registro de auditoría en la cola de eventos.
* **Disparador:** Notificación de inconsistencia de inventario en mostrador.

```
FLUJO PRINCIPAL (Transacción Compensatoria):
1. El cajero o el sistema reporta la imposibilidad de surtir la orden cobrada por agotamiento del insumo orgánico.
2. El backend emite un evento asíncrono 'inventario.stock.insuficiente' al exchange de RabbitMQ (cafeteria.events).
3. El componente SagaWorker intercepta el evento y ejecuta la transacción compensatoria (Reversa):
   a) Modifica el estado de la orden de 'PAGADA' a 'CANCELADA_REEMBOLSADA'.
   b) Genera un comprobante de devolución de dinero en efectivo o cancelación de cargo en tarjeta.
   c) Revoca los puntos o sellos de fidelización que se habían asignado preventivamente.
   d) Restituye cualquier insumo complementario no afectado en la orden.
4. El sistema registra el evento en la tabla SagaStateLog y emite una notificación al Administrador.
5. El cajero entrega el reembolso físico al cliente ofreciendo una disculpa y el ticket cancelado.

FLUJOS ALTERNATIVOS Y EXCEPCIONES:
* 3a. El broker de mensajería no puede confirmar la compensación tras 3 intentos (10s, 60s, 300s):
  - El evento es desviado a la Dead Letter Queue (orders.dlq) y el servicio SMTP envía una alerta de error crítico a gerencia.
```

---

### 3. Justificación Práctica en el Proyecto

Redactar casos de uso con este nivel de rigurosidad evita que los desarrolladores asuman cosas que nadie les pidió o que olviden los escenarios de error. Como bien señala Cockburn (2000), el 80% de los errores en producción ocurren en los flujos alternativos y en el manejo de excepciones, no en el camino feliz. Saber con exactitud qué pasa cuando falla una tarjeta, qué hacer si el cliente presenta termo o cómo devolver el dinero si se acaba el grano es lo que convierte a Monchis Café en un software confiable y profesional listo para operar en mostrador.

---

### 4. Referencias Bibliográficas

1. **Cockburn, A. (2000).** *Writing Effective Use Cases*. Addison-Wesley Professional.
2. **Larman, C. (2004).** *Applying UML and Patterns: An Introduction to Object-Oriented Analysis and Design and Iterative Development* (3.ª ed.). Prentice Hall.
3. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
4. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

