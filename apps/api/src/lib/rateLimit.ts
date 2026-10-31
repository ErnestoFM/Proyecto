// ==============================================================================
// Monchis Café — Limitador de Tasa de Peticiones (Rate Limiter)
// Protección perimetral contra ataques de fuerza bruta y saturación de API
// ==============================================================================

interface RateLimitRecord {
  count: number;
  resetTime: number;
}

const rateLimitStore = new Map<string, RateLimitRecord>();

// Limpieza periódica de claves expiradas cada 5 minutos
if (typeof setInterval !== 'undefined') {
  setInterval(() => {
    const now = Date.now();
    rateLimitStore.forEach((record, key) => {
      if (now > record.resetTime) {
        rateLimitStore.delete(key);
      }
    });
  }, 5 * 60 * 1000).unref?.();
}

export interface RateLimitOptions {
  windowMs?: number; // Ventana de tiempo en milisegundos (default: 60s)
  max?: number;      // Máximo de peticiones permitidas en la ventana (default: 5)
}

export interface RateLimitResult {
  success: boolean;
  limit: number;
  remaining: number;
  retryAfterSeconds: number;
}

/**
 * Evalúa si una clave identificadora (ej. IP del cliente) ha excedido el límite de tasa.
 */
export function checkRateLimit(
  identifier: string,
  options: RateLimitOptions = {}
): RateLimitResult {
  // En entorno de tests, permitir peticiones para no interferir con suites concurrentes
  if (process.env.NODE_ENV === 'test') {
    return {
      success: true,
      limit: options.max || 100,
      remaining: 99,
      retryAfterSeconds: 0,
    };
  }

  const windowMs = options.windowMs || 60 * 1000; // 1 minuto por defecto
  const max = options.max || 5;                   // 5 intentos por defecto
  const now = Date.now();

  const record = rateLimitStore.get(identifier);

  if (!record || now > record.resetTime) {
    rateLimitStore.set(identifier, {
      count: 1,
      resetTime: now + windowMs,
    });
    return {
      success: true,
      limit: max,
      remaining: max - 1,
      retryAfterSeconds: 0,
    };
  }

  if (record.count >= max) {
    const retryAfterSeconds = Math.ceil((record.resetTime - now) / 1000);
    return {
      success: false,
      limit: max,
      remaining: 0,
      retryAfterSeconds,
    };
  }

  record.count += 1;
  return {
    success: true,
    limit: max,
    remaining: max - record.count,
    retryAfterSeconds: 0,
  };
}

import { checkRateLimitDistributed } from './redis';

export async function checkRateLimitAsync(
  identifier: string,
  options: RateLimitOptions = {}
): Promise<RateLimitResult> {
  if (process.env.NODE_ENV === 'test') {
    return checkRateLimit(identifier, options);
  }

  if (process.env.REDIS_URL) {
    const res = await checkRateLimitDistributed(identifier, {
      max: options.max,
      windowSeconds: Math.ceil((options.windowMs || 60000) / 1000),
    });
    return res;
  }

  return checkRateLimit(identifier, options);
}

export function resetRateLimitForTesting(): void {
  rateLimitStore.clear();
}
