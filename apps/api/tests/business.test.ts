// ==============================================================================
// Pruebas Unitarias TDD — Módulos de Negocio Core (Fase 4)
// LoyaltyService & PaymentProcessor
// ==============================================================================

import { describe, it, expect } from 'vitest';
import { LoyaltyService } from '../src/lib/loyalty';
import { PaymentProcessor } from '../src/lib/paymentProcessor';

describe('☕ Módulos de Negocio Core — Monchis Café (TDD)', () => {
  // ============================================================================
  // 1. Fidelización & Monchis Rewards
  // ============================================================================
  describe('🎁 1. LoyaltyService (Sellos, Recompensas y Cashback)', () => {
    it('Debe otorgar 1 sello por café comprado sin termo', () => {
      const sellos = LoyaltyService.calcularSellosGanados(3, false);
      expect(sellos).toBe(3);
    });

    it('Debe otorgar 1 sello extra ecológico si el cliente trae termo reutilizable', () => {
      const sellos = LoyaltyService.calcularSellosGanados(2, true);
      expect(sellos).toBe(3); // 2 cafes + 1 bono eco
    });

    it('Debe calcular 5% de cashback en puntos sobre monto neto', () => {
      const puntos = LoyaltyService.calcularPuntosCashback(200);
      expect(puntos).toBe(10); // 200 * 0.05 = 10 puntos
    });

    it('Debe otorgar un café gratis al alcanzar 8 sellos y mantener el remanente', () => {
      const resultado = LoyaltyService.procesarRecompensas({
        sellosActuales: 6,
        puntosActuales: 20,
        cantidadCafes: 3, // 6 + 3 = 9 sellos -> 1 café gratis, 1 sello restante
        montoNetoPagado: 150,
        puntosAUsa: 0,
        traeTermo: false,
      });

      expect(resultado.cafesGratisDisponibles).toBe(1);
      expect(resultado.nuevosSellosTotal).toBe(1);
      expect(resultado.puntosGanados).toBe(7); // floor(150 * 0.05)
      expect(resultado.nuevosPuntosTotal).toBe(27);
    });

    it('Debe permitir redimir puntos como descuento directo ($1 MXN por punto)', () => {
      const resultado = LoyaltyService.procesarRecompensas({
        sellosActuales: 2,
        puntosActuales: 50,
        cantidadCafes: 1,
        montoNetoPagado: 100,
        puntosAUsa: 30, // Usa 30 puntos -> $30 de descuento
        traeTermo: false,
      });

      expect(resultado.puntosUtilizados).toBe(30);
      expect(resultado.descuentoPuntosAplicado).toBe(30);
      // Saldo restante: 50 - 30 = 20. Nuevo monto pagado: 70 -> Puntos ganados: floor(70*0.05)=3 -> Total: 23
      expect(resultado.nuevosPuntosTotal).toBe(23);
    });
  });

  // ============================================================================
  // 2. Procesador de Pagos y Validación de Pago Mixto
  // ============================================================================
  describe('💳 2. PaymentProcessor (Pagos Simples, Transferencias y Pagos Mixtos)', () => {
    it('Debe procesar pago en efectivo y calcular cambio correctamente', () => {
      const res = PaymentProcessor.validarPago({
        totalOrden: 150,
        metodoPago: 'EFECTIVO',
        desglose: { montoRecibidoEfectivo: 200 },
      });

      expect(res.esValido).toBe(true);
      expect(res.cambioEfectivo).toBe(50);
      expect(res.desglose.efectivo).toBe(150);
    });

    it('Debe rechazar pago en efectivo si el monto recibido es menor al total', () => {
      const res = PaymentProcessor.validarPago({
        totalOrden: 100,
        metodoPago: 'EFECTIVO',
        desglose: { montoRecibidoEfectivo: 80 },
      });

      expect(res.esValido).toBe(false);
      expect(res.error).toContain('menor al total');
    });

    it('Debe requerir clave de rastreo / referencia para transferencias / SPEI', () => {
      // Sin referencia -> Rechazado
      const sinRef = PaymentProcessor.validarPago({
        totalOrden: 120,
        metodoPago: 'TRANSFERENCIA',
        desglose: {},
      });
      expect(sinRef.esValido).toBe(false);
      expect(sinRef.error).toContain('referencia de pago');

      // Con referencia válida -> Aprobado
      const conRef = PaymentProcessor.validarPago({
        totalOrden: 120,
        metodoPago: 'TRANSFERENCIA',
        desglose: { referenciaTransferencia: 'SPEI-9847291' },
      });
      expect(conRef.esValido).toBe(true);
      expect(conRef.desglose.transferencia).toBe(120);
    });

    it('Debe validar pagos mixtos (Efectivo + Tarjeta + Transferencia + Puntos)', () => {
      const total = 350;
      const res = PaymentProcessor.validarPago({
        totalOrden: total,
        metodoPago: 'MIXTO',
        desglose: {
          montoEfectivo: 100,
          montoTarjeta: 150,
          montoTransferencia: 50,
          referenciaTransferencia: 'REF-1234',
          montoPuntos: 50,
        },
        puntosDisponiblesUsuario: 60,
      });

      expect(res.esValido).toBe(true);
      expect(res.desglose.efectivo).toBe(100);
      expect(res.desglose.tarjeta).toBe(150);
      expect(res.desglose.transferencia).toBe(50);
      expect(res.desglose.puntos).toBe(50);
    });

    it('Debe rechazar pago mixto si la suma de montos no coincide con el total', () => {
      const res = PaymentProcessor.validarPago({
        totalOrden: 200,
        metodoPago: 'MIXTO',
        desglose: {
          montoEfectivo: 50,
          montoTarjeta: 100, // Total suma 150 en lugar de 200
        },
      });

      expect(res.esValido).toBe(false);
      expect(res.error).toContain('no coincide con el total');
    });

    it('Debe rechazar pago con puntos si el usuario no tiene saldo suficiente', () => {
      const res = PaymentProcessor.validarPago({
        totalOrden: 100,
        metodoPago: 'PUNTOS',
        puntosDisponiblesUsuario: 40,
      });

      expect(res.esValido).toBe(false);
      expect(res.error).toContain('Puntos insuficientes');
    });
  });
});
