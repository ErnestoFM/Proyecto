# Patrón Saga, Transacciones de Reversa y Dead Letter Queue (DLQ)

#arquitectura #saga #rabbitmq #dlq #transacciones

## Resumen
Para operaciones de venta distribuida en **Monchis Café**, el sistema implementa el **Patrón Saga** soportado por **RabbitMQ**.

## Componentes Clave
1. **Exchange Topic:** `cafeteria.events`.
2. **Reintentos Progresivos con Retardo:** 10 segundos, 60 segundos y 300 segundos para solventar fallas transitorias de red o base de datos.
3. **Dead Letter Queue (`dead_letter_queue`):** Captura mensajes fallidos tras 4 intentos y genera alertas por correo electrónico SMTP.
4. **Transacción de Reversa (Compensación):** En caso de agotamiento de stock orgánico durante una orden cobrada, el orquestador Saga reembolsa el dinero automáticamente y marca la venta como `CANCELADA_REEMBOLSADA`.

## Enlaces Relacionados
- [[Arquitectura/Monorepo_Vue_Nextjs_RabbitMQ]]
- [[Modulos/Autenticacion_Stateless_reCAPTCHA]]
