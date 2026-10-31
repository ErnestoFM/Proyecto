// ==============================================================================
// Monchis Café — Endpoint GET /api/health (Sonda de Salud Liveness & Readiness)
// Evaluación real de base de datos PostgreSQL, latencia y observabilidad SRE
// ==============================================================================

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { checkRedisHealth } from '@/lib/redis';

export const dynamic = 'force-dynamic';

export async function GET() {
  const startTime = Date.now();
  let dbStatus = 'DISCONNECTED';
  let dbLatencyMs = -1;
  let dbError: string | null = null;

  try {
    const dbStart = Date.now();
    await prisma.$queryRaw`SELECT 1`;
    dbLatencyMs = Date.now() - dbStart;
    dbStatus = 'CONNECTED';
  } catch (error: any) {
    dbStatus = 'ERROR';
    dbError = error.message || 'Error de conexión a PostgreSQL';
  }

  // Comprobación real de salud de Redis
  const redisHealth = await checkRedisHealth();

  const memory = process.memoryUsage();
  const uptimeSeconds = Math.floor(process.uptime());

  const isHealthy = dbStatus === 'CONNECTED';
  const statusCode = isHealthy ? 200 : 503;

  return NextResponse.json(
    {
      status: isHealthy ? 'UP' : 'DEGRADED',
      servicio: 'Monchis Café API',
      version: '1.0.0',
      timestamp: new Date().toISOString(),
      uptimeSegundos: uptimeSeconds,
      duracionTotalMs: Date.now() - startTime,
      componentes: {
        baseDatos: {
          motor: 'PostgreSQL (Prisma)',
          estado: dbStatus,
          latenciaMs: dbLatencyMs,
          error: dbError,
        },
        redis: {
          motor: 'Redis 7 (ioredis)',
          estado: redisHealth.status,
          latenciaMs: redisHealth.latencyMs,
          error: redisHealth.error,
        },
        memoria: {
          rssMb: (memory.rss / (1024 * 1024)).toFixed(2),
          heapUsedMb: (memory.heapUsed / (1024 * 1024)).toFixed(2),
          heapTotalMb: (memory.heapTotal / (1024 * 1024)).toFixed(2),
        },
      },
    },
    { status: statusCode }
  );
}
