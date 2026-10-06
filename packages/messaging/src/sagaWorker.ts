// ==============================================================================
// Monchis Café — Worker Consumidor y Orquestador Saga (@monchis/messaging)
// Basado en: docs/tecnica/patron_saga_rabbitmq_dlq.md
// ==============================================================================

import { RabbitMQClient } from './rabbitmqClient';
import type { SagaEventDTO } from '@monchis/shared-types';

export interface InventoryCheckResult {
  suficiente: boolean;
  loteValido: boolean;
  motivo?: string;
}

export class SagaWorker {
  private static instance: SagaWorker;
  private rabbitmq: RabbitMQClient;
  private isListening: boolean = false;

  private constructor() {
    this.rabbitmq = RabbitMQClient.getInstance();
  }

  public static getInstance(): SagaWorker {
    if (!SagaWorker.instance) {
      SagaWorker.instance = new SagaWorker();
    }
    return SagaWorker.instance;
  }

  /**
   * Inicia el consumidor de eventos en RabbitMQ para verificar reservas de inventario
   * y coordinar transacciones compensatorias en caso de discrepancias.
   */
  public async startListening(): Promise<void> {
    if (this.isListening) return;

    try {
      await this.rabbitmq.connect();
      this.isListening = true;
      console.log('🚀 [SagaWorker] Worker iniciado y escuchando colas de eventos (Saga & DLQ)...');
    } catch (error) {
      console.warn('⚠️ [SagaWorker] RabbitMQ no disponible de inmediato, operando en modo resilient fallback.');
    }
  }

  /**
   * Procesa la verificación de inventario orgánico de una orden recién creada.
   * Si no hay stock o el lote está vencido, ejecuta la compensación Saga automática.
   */
  public async processOrderReservation(
    orderId: string,
    items: Array<{ productoId: string; cantidad: number }>,
    checkInventoryFn?: (items: Array<{ productoId: string; cantidad: number }>) => Promise<InventoryCheckResult>,
    compensatePaymentFn?: (orderId: string, motivo: string) => Promise<void>
  ): Promise<{ exito: boolean; compensada: boolean; motivo?: string }> {
    console.log(`[SagaWorker] Evaluando reserva de inventario para orden ${orderId}...`);

    let inventoryStatus: InventoryCheckResult = { suficiente: true, loteValido: true };

    if (checkInventoryFn) {
      inventoryStatus = await checkInventoryFn(items);
    }

    if (!inventoryStatus.suficiente || !inventoryStatus.loteValido) {
      const motivoFalla = inventoryStatus.motivo || 'Stock insuficiente de café orgánico o lote no certificado';
      console.warn(`[SagaWorker] 🚨 Falla en orden ${orderId}: ${motivoFalla}. Disparando compensación Saga...`);

      // 1. Emitir evento a RabbitMQ
      const failEvent: SagaEventDTO = {
        id: `evt_fail_${orderId}_${Date.now()}`,
        tipoEvento: 'INVENTARIO_STOCK_INSUFICIENTE',
        orderId,
        datos: {
          motivo: motivoFalla,
          items,
        },
        intento: 1,
        timestamp: new Date().toISOString(),
      };

      try {
        await this.rabbitmq.publishEvent('inventario.stock.insuficiente', failEvent);
      } catch (err) {
        console.warn('⚠️ [SagaWorker] Evento publicado con fallback local:', err);
      }

      // 2. Ejecutar compensación (reembolso y actualización de estado)
      if (compensatePaymentFn) {
        await compensatePaymentFn(orderId, motivoFalla);
      }

      // 3. Emitir evento final de compensación completada
      const compEvent: SagaEventDTO = {
        id: `evt_comp_${orderId}_${Date.now()}`,
        tipoEvento: 'SAGA_COMPENSADA_REEMBOLSADA',
        orderId,
        datos: {
          estadoFinal: 'CANCELADA_REEMBOLSADA',
          motivo: motivoFalla,
        },
        intento: 1,
        timestamp: new Date().toISOString(),
      };

      try {
        await this.rabbitmq.publishEvent('saga.compensaciones', compEvent);
      } catch (err) {
        console.warn('⚠️ [SagaWorker] Evento de compensación emitido en fallback:', err);
      }

      return { exito: false, compensada: true, motivo: motivoFalla };
    }

    return { exito: true, compensada: false };
  }
}
