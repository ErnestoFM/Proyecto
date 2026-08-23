// ==============================================================================
// Monchis Café — Procesador de Pagos y Validación de Pago Mixto
// ==============================================================================

import type { PaymentMethod } from '@monchis/shared-types';

export interface PaymentBreakdown {
  montoEfectivo?: number;
  montoTarjeta?: number;
  montoTransferencia?: number;
  montoPuntos?: number;
  referenciaTransferencia?: string;
  montoRecibidoEfectivo?: number; // Para calcular cambio
}

export interface PaymentValidationResult {
  esValido: boolean;
  error?: string;
  cambioEfectivo?: number;
  desglose: {
    efectivo: number;
    tarjeta: number;
    transferencia: number;
    puntos: number;
  };
}

export class PaymentProcessor {
  /**
   * Valida un esquema de pago (único o mixto) contra el monto total a liquidar.
   */
  static validarPago(params: {
    totalOrden: number;
    metodoPago: PaymentMethod;
    desglose?: PaymentBreakdown;
    puntosDisponiblesUsuario?: number;
  }): PaymentValidationResult {
    const { totalOrden, metodoPago, desglose = {}, puntosDisponiblesUsuario = 0 } = params;

    if (totalOrden < 0) {
      return { esValido: false, error: 'El total de la orden no puede ser negativo', desglose: { efectivo: 0, tarjeta: 0, transferencia: 0, puntos: 0 } };
    }

    if (totalOrden === 0) {
      return {
        esValido: true,
        desglose: { efectivo: 0, tarjeta: 0, transferencia: 0, puntos: 0 },
        cambioEfectivo: 0,
      };
    }

    let efectivo = 0;
    let tarjeta = 0;
    let transferencia = 0;
    let puntos = 0;
    let cambioEfectivo = 0;

    switch (metodoPago) {
      case 'EFECTIVO': {
        const recibido = desglose.montoRecibidoEfectivo ?? totalOrden;
        if (recibido < totalOrden) {
          return {
            esValido: false,
            error: `Monto recibido ($${recibido}) es menor al total ($${totalOrden})`,
            desglose: { efectivo: 0, tarjeta: 0, transferencia: 0, puntos: 0 },
          };
        }
        efectivo = totalOrden;
        cambioEfectivo = Number((recibido - totalOrden).toFixed(2));
        break;
      }

      case 'TARJETA': {
        tarjeta = totalOrden;
        break;
      }

      case 'TRANSFERENCIA': {
        if (!desglose.referenciaTransferencia || desglose.referenciaTransferencia.trim().length < 4) {
          return {
            esValido: false,
            error: 'La transferencia bancaria requiere una referencia de pago o SPEI válida (mínimo 4 caracteres)',
            desglose: { efectivo: 0, tarjeta: 0, transferencia: 0, puntos: 0 },
          };
        }
        transferencia = totalOrden;
        break;
      }

      case 'PUNTOS': {
        if (puntosDisponiblesUsuario < totalOrden) {
          return {
            esValido: false,
            error: `Puntos insuficientes: Se requieren ${totalOrden} puntos y el usuario tiene ${puntosDisponiblesUsuario}`,
            desglose: { efectivo: 0, tarjeta: 0, transferencia: 0, puntos: 0 },
          };
        }
        puntos = totalOrden;
        break;
      }

      case 'MIXTO': {
        efectivo = Math.max(0, desglose.montoEfectivo || 0);
        tarjeta = Math.max(0, desglose.montoTarjeta || 0);
        transferencia = Math.max(0, desglose.montoTransferencia || 0);
        puntos = Math.max(0, desglose.montoPuntos || 0);

        if (transferencia > 0 && (!desglose.referenciaTransferencia || desglose.referenciaTransferencia.trim().length < 4)) {
          return {
            esValido: false,
            error: 'La fracción pagada con transferencia requiere su respectiva clave de rastreo / referencia',
            desglose: { efectivo: 0, tarjeta: 0, transferencia: 0, puntos: 0 },
          };
        }

        if (puntos > puntosDisponiblesUsuario) {
          return {
            esValido: false,
            error: `Puntos insuficientes: Se intentó usar ${puntos} puntos pero solo hay ${puntosDisponiblesUsuario} disponibles`,
            desglose: { efectivo: 0, tarjeta: 0, transferencia: 0, puntos: 0 },
          };
        }

        const sumaPagos = Number((efectivo + tarjeta + transferencia + puntos).toFixed(2));
        if (sumaPagos !== Number(totalOrden.toFixed(2))) {
          return {
            esValido: false,
            error: `La suma de montos ($${sumaPagos}) no coincide con el total de la orden ($${totalOrden})`,
            desglose: { efectivo, tarjeta, transferencia, puntos },
          };
        }

        if (desglose.montoRecibidoEfectivo && desglose.montoRecibidoEfectivo > efectivo) {
          cambioEfectivo = Number((desglose.montoRecibidoEfectivo - efectivo).toFixed(2));
        }
        break;
      }

      default:
        return { esValido: false, error: 'Método de pago no reconocido', desglose: { efectivo: 0, tarjeta: 0, transferencia: 0, puntos: 0 } };
    }

    return {
      esValido: true,
      cambioEfectivo,
      desglose: { efectivo, tarjeta, transferencia, puntos },
    };
  }
}
