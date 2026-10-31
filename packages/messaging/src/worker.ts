// ==============================================================================
// Monchis Café — Worker Consumidor Desacoplado de RabbitMQ y Saga
// packages/messaging/src/worker.ts
// ==============================================================================

import { RabbitMQClient } from './rabbitmqClient';
import { SagaWorker } from './sagaWorker';

async function bootstrapWorker() {
  console.log('==========================================================');
  console.log('🚀 [Worker] Iniciando Daemon Consumidor de Eventos AMQP');
  console.log('==========================================================');

  const client = RabbitMQClient.getInstance();
  const worker = SagaWorker.getInstance();

  try {
    await client.connect();
    await worker.startListening();
    console.log('✅ [Worker] Daemon activo. Escuchando cafeteria.events y Dead Letter Queue.');
  } catch (error: any) {
    console.error('❌ [Worker] Error fatal al conectar con RabbitMQ:', error.message);
    if (process.env.NODE_ENV === 'production') {
      process.exit(1);
    }
  }

  // Manejo de señales de terminación limpia
  const gracefulShutdown = () => {
    console.log('\n🛑 [Worker] Recibida señal de terminación. Cerrando conexiones AMQP...');
    process.exit(0);
  };

  process.on('SIGINT', gracefulShutdown);
  process.on('SIGTERM', gracefulShutdown);
}

if (require.main === module || process.env.RUN_WORKER === 'true') {
  bootstrapWorker();
}

export { bootstrapWorker };
