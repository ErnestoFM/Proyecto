// ==============================================================================
// Monchis Café — Cliente de Mensajería RabbitMQ (@monchis/messaging)
// ==============================================================================

import amqplib, { Channel, Connection } from 'amqplib';
import { SagaEventDTO } from '@monchis/shared-types';

export class RabbitMQClient {
  private static instance: RabbitMQClient;
  private connection: Connection | null = null;
  private channel: Channel | null = null;
  private exchangeName: string = process.env.RABBITMQ_EXCHANGE || 'cafeteria.events';
  private dlxExchangeName: string = process.env.RABBITMQ_DLX_EXCHANGE || 'cafeteria.dlx';
  private dlqName: string = process.env.RABBITMQ_DLQ_NAME || 'dead_letter_queue';
  private retryDelays: number[] = [10000, 60000, 300000]; // 10s, 1m, 5m

  private constructor() {}

  public static getInstance(): RabbitMQClient {
    if (!RabbitMQClient.instance) {
      RabbitMQClient.instance = new RabbitMQClient();
    }
    return RabbitMQClient.instance;
  }

  public async connect(): Promise<void> {
    if (this.connection && this.channel) return;

    const url = process.env.RABBITMQ_URL || 'amqp://guest:guest@localhost:5672';
    try {
      this.connection = await amqplib.connect(url);
      this.channel = await this.connection.createChannel();

      // Declarar Exchanges
      await this.channel.assertExchange(this.exchangeName, 'topic', { durable: true });
      await this.channel.assertExchange(this.dlxExchangeName, 'direct', { durable: true });

      // Declarar Dead Letter Queue
      await this.channel.assertQueue(this.dlqName, { durable: true });
      await this.channel.bindQueue(this.dlqName, this.dlxExchangeName, 'dlq.#');

      console.log('✅ [RabbitMQ] Conectado exitosamente con soporte DLQ');
    } catch (error) {
      console.error('❌ [RabbitMQ] Error conectando a RabbitMQ:', error);
      throw error;
    }
  }

  public async publishEvent<T>(routingKey: string, event: SagaEventDTO<T>): Promise<boolean> {
    if (!this.channel) {
      await this.connect();
    }
    const messageBuffer = Buffer.from(JSON.stringify(event));
    return this.channel!.publish(this.exchangeName, routingKey, messageBuffer, {
      persistent: true,
      headers: {
        'x-retry-count': event.intento || 0,
        'x-original-routing-key': routingKey,
      },
    });
  }

  public async handleRetryOrDLQ<T>(
    event: SagaEventDTO<T>,
    originalRoutingKey: string,
    errorReason: string
  ): Promise<void> {
    if (!this.channel) await this.connect();

    const currentAttempt = event.intento || 0;
    if (currentAttempt < this.retryDelays.length) {
      const delayMs = this.retryDelays[currentAttempt];
      const nextAttempt = currentAttempt + 1;
      console.warn(
        `⚠️ [RabbitMQ Retry] Reintentando evento ${event.tipoEvento} (Intento ${nextAttempt} en ${delayMs / 1000}s)`
      );

      // Usar cola con TTL para el retraso progresivo
      const retryQueue = `retry.${delayMs}ms.queue`;
      await this.channel!.assertQueue(retryQueue, {
        durable: true,
        deadLetterExchange: this.exchangeName,
        deadLetterRoutingKey: originalRoutingKey,
        messageTtl: delayMs,
      });

      const updatedEvent: SagaEventDTO<T> = {
        ...event,
        intento: nextAttempt,
      };

      this.channel!.sendToQueue(retryQueue, Buffer.from(JSON.stringify(updatedEvent)), {
        persistent: true,
      });
    } else {
      console.error(
        `🚨 [RabbitMQ DLQ] Reintentos agotados para evento ${event.tipoEvento}. Derivando a Dead Letter Queue.`
      );
      const dlqPayload = {
        ...event,
        errorReason,
        failedAt: new Date().toISOString(),
      };
      this.channel!.publish(
        this.dlxExchangeName,
        `dlq.${originalRoutingKey}`,
        Buffer.from(JSON.stringify(dlqPayload)),
        { persistent: true }
      );
    }
  }
}
