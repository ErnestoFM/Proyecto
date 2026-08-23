# Casos de Uso e Historias de Usuario (TDD) — Monchis Café

Este documento define los casos de uso fundamentales en formato **User Story** con criterios de aceptación estructurados en **Given / When / Then** para guiar el desarrollo guiado por pruebas (TDD).

---

## 1. Módulo de Autenticación y Seguridad

### US-01: Inicio de Sesión Stateless con Google reCAPTCHA
* **Como** Usuario (Administrador / Cajero / Cliente),
* **Quiero** autenticarme en la plataforma ingresando mis credenciales y resolviendo la validación anti-bot de Google reCAPTCHA,
* **Para** acceder de forma segura a mis funciones según mi rol.

#### Criterios de Aceptación (Gherkin):
```gherkin
Scenario: Inicio de sesión exitoso de administrador con reCAPTCHA válido
  Given que el usuario envía email válido, contraseña correcta y un token reCAPTCHA válido
  When el backend valida el token con la API de Google y comprueba el hash bcrypt
  Then el servidor responde HTTP 200 con un Access Token JWT de 15 minutos en el body
  And establece una cookie httpOnly con el Refresh Token de 7 días.

Scenario: Rechazo de inicio de sesión por bot o reCAPTCHA inválido
  Given que se envía un intento de login con token reCAPTCHA expirado o ausente
  When el backend consulta https://www.google.com/recaptcha/api/siteverify
  Then el servidor retorna HTTP 403 Forbidden con el mensaje "Verificación de seguridad fallida".
```

---

## 2. Módulo de Punto de Venta (POS) y Pagos

### US-02: Cobro de Venta con Múltiples Métodos de Pago
* **Como** Cajero de Monchis Café,
* **Quiero** registrar una orden en el POS cobrando en Efectivo, Tarjeta o Transferencia/SPEI,
* **Para** emitir el ticket de venta y cuadrar el corte de caja.

#### Criterios de Aceptación:
```gherkin
Scenario: Cobro con Transferencia / SPEI
  Given que el cliente solicita pagar una orden de $150 MXN mediante transferencia
  When el cajero selecciona el método 'TRANSFERENCIA' e ingresa la clave de rastreo bancaria
  Then la orden se guarda en estado 'PROCESANDO'
  And el sistema asocia la clave de rastreo a la transacción para auditoría de caja.
```

---

## 3. Módulo de Transacciones Distribuidas (Saga de Reversa)

### US-03: Reversa Automática por Falta de Insumos Orgánicos
* **Como** Sistema de Monchis Café,
* **Quiero** cancelar automáticamente una venta y reembolsar el cobro si el insumo de café orgánico se agotó,
* **Para** evitar discrepancias y mantener la satisfacción del cliente.

#### Criterios de Aceptación:
```gherkin
Scenario: Activación de Transacción Compensatoria (Reversa)
  Given que una orden de café de especialidad fue cobrada
  When el servicio de inventario detecta que el lote orgánico no tiene stock disponible
  Then RabbitMQ emite el evento 'inventario.stock.insuficiente'
  And el Saga Coordinator ejecuta la compensación: reembolsa el dinero y marca la orden como 'CANCELADA_REEMBOLSADA'.
```

---

## 4. Módulo de Atribución y Fidelización (Monchis Rewards)

### US-04: Captura de Origen de Tráfico (Instagram / Google Maps)
* **Como** Administrador de Monchis Café,
* **Quiero** conocer qué porcentaje de compras proviene de Google Maps o campañas de Instagram,
* **Para** optimizar la inversión en marketing local.

#### Criterios de Aceptación:
```gherkin
Scenario: Atribución de cliente proveniente de Google Maps
  Given que un cliente visita la landing con el parámetro '?utm_source=google_maps'
  When el cliente se registra o realiza una compra
  Then el sistema guarda el registro de atribución vinculado al usuario y la orden
  And el panel de administración actualiza el gráfico de canales de tráfico.
```
