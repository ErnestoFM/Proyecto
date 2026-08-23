// ==============================================================================
// Monchis Café — Servicio de Fidelización y Rewards
// ==============================================================================

export interface LoyaltyCalculationResult {
  sellosGanados: number;
  nuevosSellosTotal: number;
  cafesGratisDisponibles: number;
  puntosGanados: number;
  nuevosPuntosTotal: number;
  puntosUtilizados: number;
  descuentoPuntosAplicado: number;
}

export class LoyaltyService {
  /** Cada 8 sellos otorgan un café gratis */
  static readonly SELLOS_PARA_CAFE_GRATIS = 8;

  /** 5% de cashback en puntos sobre el monto pagado */
  static readonly TASA_CASHBACK_PUNTOS = 0.05;

  /**
   * Calcula los sellos ganados en una orden.
   * Regla de Negocio:
   * - 1 sello por cada café o producto orgánico.
   * - Si el cliente trae su termo reutilizable, se otorga 1 sello extra ecológico.
   */
  static calcularSellosGanados(cantidadCafes: number, traeTermo: boolean): number {
    if (cantidadCafes <= 0) return 0;
    const sellosBase = cantidadCafes;
    const sellosEco = traeTermo ? 1 : 0;
    return sellosBase + sellosEco;
  }

  /**
   * Calcula los puntos de cashback generados en función del monto pagado neto (después de descuentos).
   */
  static calcularPuntosCashback(montoNetoPagado: number): number {
    if (montoNetoPagado <= 0) return 0;
    return Math.floor(montoNetoPagado * this.TASA_CASHBACK_PUNTOS);
  }

  /**
   * Procesa la actualización completa de recompensas para un cliente.
   */
  static procesarRecompensas(params: {
    sellosActuales: number;
    puntosActuales: number;
    cantidadCafes: number;
    montoNetoPagado: number;
    puntosAUsa: number;
    traeTermo: boolean;
  }): LoyaltyCalculationResult {
    const { sellosActuales, puntosActuales, cantidadCafes, montoNetoPagado, puntosAUsa, traeTermo } = params;

    // 1. Validar y aplicar puntos usados
    const puntosValidosUso = Math.min(Math.max(0, puntosAUsa), puntosActuales, Math.floor(montoNetoPagado));
    const descuentoPuntos = puntosValidosUso; // 1 punto = $1 MXN
    const saldoPuntosTrasUso = puntosActuales - puntosValidosUso;

    // 2. Calcular nuevos puntos ganados sobre el monto efectivamente pagado en dinero
    const montoEfectivo = Math.max(0, montoNetoPagado - descuentoPuntos);
    const puntosGanados = this.calcularPuntosCashback(montoEfectivo);
    const nuevosPuntosTotal = saldoPuntosTrasUso + puntosGanados;

    // 3. Calcular sellos
    const sellosGanados = this.calcularSellosGanados(cantidadCafes, traeTermo);
    const sellosTotales = sellosActuales + sellosGanados;
    const cafesGratis = Math.floor(sellosTotales / this.SELLOS_PARA_CAFE_GRATIS);
    const sellosRestantes = sellosTotales % this.SELLOS_PARA_CAFE_GRATIS;

    return {
      sellosGanados,
      nuevosSellosTotal: sellosRestantes,
      cafesGratisDisponibles: cafesGratis,
      puntosGanados,
      nuevosPuntosTotal,
      puntosUtilizados: puntosValidosUso,
      descuentoPuntosAplicado: descuentoPuntos,
    };
  }
}
