// ==============================================================================
// Monchis Café — Tipos TypeScript Compartidos (@monchis/shared-types)
// ==============================================================================

export type UserRole = 'ADMIN' | 'CAJERO' | 'CLIENTE';

export interface UserDTO {
  id: string;
  email: string;
  nombre: string;
  rol: UserRole;
  puntosFidelidad: number;
  sellosAcumulados: number;
  creadoEn: string;
}

export interface JwtPayloadDTO {
  sub: string;
  email: string;
  rol: UserRole;
  iat?: number;
  exp?: number;
}

export type ProductType = 'ORGANICO' | 'COMERCIAL';

export interface ProductDTO {
  id: string;
  nombre: string;
  descripcion?: string;
  tipo: ProductType;
  precio: number;
  stockActual: number;
  stockMinimo: number;
  imagenUrl?: string;
  activo: boolean;
}

export interface BatchDTO {
  id: string;
  productoId: string;
  numeroLote: string;
  proveedorRegional: string;
  fincaOrigen?: string;
  fechaCosechaTostado: string;
  fechaCaducidad: string;
  cantidadKilos: number;
  alertasSanitarias?: string;
}

export type PaymentMethod = 'EFECTIVO' | 'TARJETA' | 'TRANSFERENCIA' | 'PUNTOS' | 'MIXTO';

export type OrderStatus = 'PENDIENTE' | 'PROCESANDO' | 'COMPLETADA' | 'CANCELADA_REEMBOLSADA';

export interface OrderItemDTO {
  productoId: string;
  cantidad: number;
  precioUnitario: number;
  subtotal: number;
}

export interface CreateOrderRequestDTO {
  clienteId?: string;
  items: OrderItemDTO[];
  metodoPago: PaymentMethod;
  referenciaPago?: string; // Para transferencias / SPEI
  montoEfectivo?: number;
  puntosUsados?: number;
  traeTermoReutilizable?: boolean;
  utmSource?: string;
  utmCampaign?: string;
}

export interface OrderDTO {
  id: string;
  total: number;
  descuento: number;
  metodoPago: PaymentMethod;
  estado: OrderStatus;
  referenciaPago?: string;
  clienteId?: string;
  cajeroId: string;
  items: OrderItemDTO[];
  creadoEn: string;
}

export interface AttributionTrafficDTO {
  source: string; // 'google_maps', 'instagram', 'direct'
  medium?: string;
  campaign?: string;
  totalVisitas: number;
  totalVentas: number;
  montoGenerado: number;
}

export interface SagaEventDTO<T = any> {
  id: string;
  tipoEvento: string;
  orderId: string;
  datos: T;
  intento: number;
  timestamp: string;
}
