# Especificación Técnica: Patrón Saga, RabbitMQ y Dead Letter Queue (DLQ)

## 1. Visión General
En **Monchis Café**, las operaciones de venta involucran múltiples pasos coordinados: cobro, reserva de inventario de café orgánico y emisión de tickets. Para garantizar la consistencia sin recurrir a bloqueos pesados de base de datos bidireccionales, se utiliza el **Patrón Saga (Choreography/Orchestration)** sobre **RabbitMQ**.

---

## 2. Topología de RabbitMQ

### 2.1 Exchanges
* `cafeteria.events` (Tipo: `topic`, Durable: `true`): Canal principal para eventos de negocio.
* `cafeteria.dlx` (Tipo: `direct`, Durable: `true`): Dead Letter Exchange para enrutar mensajes fallidos.

### 2.2 Colas Principales
* `pos.ventas.iniciadas`: Consumida por el servicio de ventas.
* `inventario.reservas`: Consumida por el servicio de inventario y trazabilidad.
* `saga.compensaciones`: Consumida por el orquestador de compensaciones.
* `dead_letter_queue`: Cola final para auditoría y alertas.

---

## 3. Flujo de Reintentos Progresivos con Retardo

```
Intento 1: Ejecución Inmediata
    │ (Falla de red / timeout)
    ▼
Intento 2: Retraso de 10s (retry.10000ms.queue)
    │ (Falla persistente)
    ▼
Intento 3: Retraso de 60s (retry.60000ms.queue)
    │ (Falla persistente)
    ▼
Intento 4: Retraso de 300s (retry.300000ms.queue)
    │ (Reintentos Agotados)
    ▼
Dead Letter Queue (DLQ) ──► Notificación por Correo SMTP al Administrador
```

---

## 4. Transacciones Compensatorias (Reversa)

Cuando un insumo de café orgánico no cuenta con stock suficiente tras haberse efectuado el cobro:
1. El microservicio emite `inventario.stock.insuficiente`.
2. El `SagaCoordinator` intercepta el evento y ejecuta la pila LIFO de compensación.
3. Se realiza el reembolso del método de pago (Efectivo/Tarjeta/Transferencia).
4. Se actualiza el registro en `SagaStateLog` con estado `CANCELADA_REEMBOLSADA`.
