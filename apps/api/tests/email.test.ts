// ==============================================================================
// Monchis Café — Pruebas Unitarias del Servicio de Notificaciones SMTP (TDD)
// Archivo: apps/api/tests/email.test.ts
// ==============================================================================

import { describe, it, expect, beforeEach } from 'vitest';
import {
  EmailService,
  getSentEmailsLogForTesting,
  clearSentEmailsLogForTesting,
} from '../src/lib/emailService';

describe('📧 Servicio de Notificaciones por Correo SMTP (Req 2.2 & 2.3)', () => {
  beforeEach(() => {
    clearSentEmailsLogForTesting();
  });

  describe('1. Alerta Crítica de Dead Letter Queue (DLQ)', () => {
    it('Debe emitir un correo de alerta DLQ al administrador con formato y detalles del fallo', async () => {
      const payload = {
        orderId: 'ord_test_dlq_999',
        motivo: 'Insumo de café orgánico agotado tras 3 reintentos en cola',
        intentos: 3,
        sagaId: 'saga_ord_test_dlq_999',
        timestamp: '2026-10-06T18:00:00.000Z',
      };

      const result = await EmailService.sendDLQAlert(payload);
      expect(result.success).toBe(true);

      const logs = getSentEmailsLogForTesting();
      expect(logs.length).toBe(1);

      const email = logs[0];
      expect(email.subject).toContain('🚨 [ALERTA CRÍTICA DLQ]');
      expect(email.subject).toContain(payload.orderId);
      expect(email.html).toContain('ord_test_dlq_999');
      expect(email.html).toContain('3 intentos');
      expect(email.html).toContain('Insumo de café orgánico agotado');
      expect(email.html).toContain('Dead Letter Queue');
    });
  });

  describe('2. Alerta de Caducidad de Lotes Orgánicos', () => {
    it('Debe emitir alerta preventiva ante caducidad próxima de lote de café', async () => {
      const payload = {
        numeroLote: 'MC-CHP-2026-X1',
        productoNombre: 'Mezcla Orgánica Chiapas 500g',
        fincaOrigen: 'Finca Santa Rosa, Chiapas',
        fechaCaducidad: '2026-10-15',
        diasRestantes: 9,
      };

      const result = await EmailService.sendBatchExpiryAlert(payload);
      expect(result.success).toBe(true);

      const logs = getSentEmailsLogForTesting();
      expect(logs.length).toBe(1);

      const email = logs[0];
      expect(email.subject).toContain('⚠️ [CADUCIDAD PREVENTIVA]');
      expect(email.subject).toContain(payload.numeroLote);
      expect(email.html).toContain('MC-CHP-2026-X1');
      expect(email.html).toContain('Finca Santa Rosa, Chiapas');
      expect(email.html).toContain('9 días');
    });

    it('Debe marcar alerta como URGENTE si los días restantes son 5 o menos', async () => {
      const payload = {
        numeroLote: 'MC-VER-2026-CRITICO',
        productoNombre: 'Expreso Veracruzano Tueste Obscuro',
        fechaCaducidad: '2026-10-08',
        diasRestantes: 2,
      };

      const result = await EmailService.sendBatchExpiryAlert(payload);
      expect(result.success).toBe(true);

      const logs = getSentEmailsLogForTesting();
      expect(logs[0].subject).toContain('⚠️ [CADUCIDAD URGENTE]');
      expect(logs[0].html).toContain('2 días');
    });
  });

  describe('3. Alerta de Stock Mínimo de Inventario', () => {
    it('Debe enviar notificación de inventario bajo ante cruce de umbral', async () => {
      const payload = {
        productoId: 'prod_1',
        productoNombre: 'Café Orgánico de Altura 1kg',
        stockActual: 3,
        stockMinimo: 10,
      };

      const result = await EmailService.sendLowStockAlert(payload);
      expect(result.success).toBe(true);

      const logs = getSentEmailsLogForTesting();
      expect(logs.length).toBe(1);

      const email = logs[0];
      expect(email.subject).toContain('📦 [INVENTARIO BAJO]');
      expect(email.subject).toContain('Café Orgánico de Altura 1kg');
      expect(email.html).toContain('3 unidades');
      expect(email.html).toContain('10 unidades');
    });
  });

  describe('4. Comprobante / Recibo de Compra para el Cliente', () => {
    it('Debe generar y enviar recibo con desglose de productos y beneficios de fidelidad', async () => {
      const payload = {
        clienteEmail: 'cliente.feliz@gmail.com',
        ordenId: 'ord_pos_abc_123',
        total: 135.5,
        metodoPago: 'TARJETA',
        items: [
          { nombre: 'Café Americano Chiapas', cantidad: 2, subtotal: 96.0 },
          { nombre: 'Galleta de Avena Orgánica', cantidad: 1, subtotal: 39.5 },
        ],
        puntosGanados: 13,
        sellosAcumulados: 5,
      };

      const result = await EmailService.sendOrderReceipt(payload);
      expect(result.success).toBe(true);

      const logs = getSentEmailsLogForTesting();
      expect(logs.length).toBe(1);

      const email = logs[0];
      expect(email.to).toBe('cliente.feliz@gmail.com');
      expect(email.subject).toContain('Comprobante de Compra #ord_pos_');
      expect(email.html).toContain('$135.50 MXN');
      expect(email.html).toContain('Café Americano Chiapas');
      expect(email.html).toContain('Sellos activos:');
      expect(email.html).toContain('+13 pts');
    });
  });
});
