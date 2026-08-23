// ==============================================================================
// Monchis Café — Coordinador Saga y Transacciones Compensatorias (@monchis/messaging)
// ==============================================================================

import { RabbitMQClient } from './rabbitmqClient';
import { SagaEventDTO } from '@monchis/shared-types';

export interface SagaStep {
  nombre: string;
  ejecutar: () => Promise<boolean>;
  compensar: () => Promise<void>;
}

export class SagaCoordinator {
  private sagaId: string;
  private orderId: string;
  private executedSteps: string[] = [];
  private compensations: Array<() => Promise<void>> = [];
  private rabbitmq: RabbitMQClient;

  constructor(orderId: string) {
    this.orderId = orderId;
    this.sagaId = `saga_${orderId}_${Date.now()}`;
    this.rabbitmq = RabbitMQClient.getInstance();
  }

  public async executeStep(step: SagaStep): Promise<boolean> {
    try {
      console.log(`[Saga ${this.sagaId}] Ejecutando paso: ${step.nombre}`);
      const success = await step.ejecutar();

      if (success) {
        this.executedSteps.push(step.nombre);
        this.compensations.unshift(step.compensar); // Pila LIFO para compensación
        return true;
      } else {
        console.warn(`[Saga ${this.sagaId}] Paso falló: ${step.nombre}. Iniciando reversa...`);
        await this.rollback(`Fallo en paso ${step.nombre}`);
        return false;
      }
    } catch (error: any) {
      console.error(`[Saga ${this.sagaId}] Excepción en paso ${step.nombre}:`, error);
      await this.rollback(error.message || 'Excepción no controlada en paso');
      return false;
    }
  }

  public async rollback(reason: string): Promise<void> {
    console.warn(`[Saga ${this.sagaId}] 🔄 EJECUTANDO TRANSACCIONES COMPENSATORIAS (REVERSA)...`);
    for (const compensate of this.compensations) {
      try {
        await compensate();
      } catch (compError) {
        console.error(`[Saga ${this.sagaId}] Error en compensación:`, compError);
      }
    }

    // Publicar evento de saga fallida a RabbitMQ
    const failureEvent: SagaEventDTO = {
      id: `fail_${this.sagaId}`,
      tipoEvento: 'SAGA_COMPENSADA_REEMBOLSADA',
      orderId: this.orderId,
      datos: {
        sagaId: this.sagaId,
        motivo: reason,
        pasosRevertidos: this.executedSteps,
      },
      intento: 1,
      timestamp: new Date().toISOString(),
    };

    await this.rabbitmq.publishEvent('saga.compensar.venta', failureEvent);
  }
}
