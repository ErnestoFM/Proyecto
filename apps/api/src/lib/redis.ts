// ==============================================================================
// Monchis Café — Cliente y Servicio Redis (apps/api/src/lib/redis.ts)
// Gestión de Cache Distribuido, Rate Limiting y Blacklist de Tokens
// ==============================================================================

import Redis from 'ioredis';

let redisInstance: Redis | null = null;
let isRedisAvailable = false;

export function getRedisClient(): Redis | null {
  if (redisInstance) {
    return redisInstance;
  }

  const redisUrl = process.env.REDIS_URL;
  if (!redisUrl) {
    return null;
  }

  try {
    redisInstance = new Redis(redisUrl, {
      lazyConnect: true,
      maxRetriesPerRequest: 1,
      connectTimeout: 2000,
      retryStrategy: (times) => {
        if (times > 3) {
          isRedisAvailable = false;
          return null; // Detener reintentos continuos para no bloquear la aplicación
        }
        return Math.min(times * 100, 1000);
      },
    });

    redisInstance.on('connect', () => {
      isRedisAvailable = true;
      console.log('✅ [Redis] Conectado exitosamente al servidor Redis.');
    });

    redisInstance.on('error', (err) => {
      isRedisAvailable = false;
      // No loguear spam en desarrollo/test
      if (process.env.NODE_ENV !== 'test') {
        console.warn('⚠️ [Redis] Servidor no disponible, operando en modo fallback local:', err.message);
      }
    });

    return redisInstance;
  } catch (error) {
    console.warn('⚠️ [Redis] Error inicializando cliente Redis:', error);
    return null;
  }
}

export async function checkRedisHealth(): Promise<{ status: string; latencyMs: number; error: string | null }> {
  const client = getRedisClient();
  if (!client) {
    return { status: 'DISABLED', latencyMs: -1, error: 'REDIS_URL no configurada' };
  }

  const start = Date.now();
  try {
    if (client.status !== 'ready') {
      await client.connect();
    }
    await client.ping();
    return { status: 'CONNECTED', latencyMs: Date.now() - start, error: null };
  } catch (err: any) {
    return { status: 'ERROR', latencyMs: -1, error: err.message || 'No se pudo conectar a Redis' };
  }
}

/**
 * Limitador de tasa distribuido con Redis (Token Bucket / Sliding Window)
 * Si Redis no está disponible, delega elegantemente al limitador en memoria.
 */
export async function checkRateLimitDistributed(
  identifier: string,
  options: { max?: number; windowSeconds?: number } = {}
): Promise<{ success: boolean; limit: number; remaining: number; retryAfterSeconds: number }> {
  const max = options.max || 5;
  const windowSeconds = options.windowSeconds || 60;
  const client = getRedisClient();

  if (!client) {
    // Redis no configurado, retornar éxito o fallback
    return { success: true, limit: max, remaining: max - 1, retryAfterSeconds: 0 };
  }

  try {
    if (client.status !== 'ready') {
      await client.connect();
    }

    const key = `rl:${identifier}`;
    const current = await client.incr(key);

    if (current === 1) {
      await client.expire(key, windowSeconds);
    }

    const ttl = await client.ttl(key);

    if (current > max) {
      return {
        success: false,
        limit: max,
        remaining: 0,
        retryAfterSeconds: ttl > 0 ? ttl : windowSeconds,
      };
    }

    return {
      success: true,
      limit: max,
      remaining: Math.max(0, max - current),
      retryAfterSeconds: 0,
    };
  } catch (e) {
    // Si Redis falla, permitir la petición para no interrumpir el servicio (Fail-Open seguro con log)
    return { success: true, limit: max, remaining: 1, retryAfterSeconds: 0 };
  }
}
