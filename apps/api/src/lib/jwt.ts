// ==============================================================================
// Monchis Café — Servicio JWT Stateless (apps/api/src/lib/jwt.ts)
// ==============================================================================

import crypto from 'crypto';
import jwt from 'jsonwebtoken';
import { JwtPayloadDTO, UserRole } from '@monchis/shared-types';
import { prisma } from './prisma';

// Cache en memoria para revocación inmediata O(1) de tokens
const REVOKED_TOKENS_CACHE = new Set<string>();

export function _clearRevokedTokensCacheForTesting(): void {
  REVOKED_TOKENS_CACHE.clear();
}

function getSecret(envKey: string, devDefault: string): string {
  const secret = process.env[envKey];
  if (secret && secret.trim().length >= 32) {
    return secret;
  }
  if (process.env.NODE_ENV === 'production') {
    throw new Error(`[Seguridad Crítica] La variable de entorno obligatoria ${envKey} no está configurada o tiene menos de 32 caracteres.`);
  }
  // En desarrollo/test, alertar sobre la ausencia de la variable
  if (process.env.NODE_ENV !== 'test') {
    console.warn(`⚠️ [JWT] Advertencia de Seguridad: ${envKey} no está definida en .env. Usando clave de desarrollo temporal.`);
  }
  return devDefault;
}

const getAccessSecret = () => getSecret('JWT_ACCESS_SECRET', 'dev_only_ephemeral_jwt_access_secret_key_32_chars');
const getRefreshSecret = () => getSecret('JWT_REFRESH_SECRET', 'dev_only_ephemeral_jwt_refresh_secret_key_32_chars');

export function signAccessToken(payload: { userId: string; email: string; rol: UserRole; jti?: string }): string {
  const jwtPayload: JwtPayloadDTO = {
    sub: payload.userId,
    email: payload.email,
    rol: payload.rol,
    jti: payload.jti || crypto.randomUUID(),
  };
  return jwt.sign(jwtPayload, getAccessSecret(), {
    expiresIn: (process.env.JWT_ACCESS_EXPIRES as any) || '15m',
    algorithm: 'HS256',
  });
}

export function signRefreshToken(payload: { userId: string; email: string; rol: UserRole; jti?: string }): string {
  const jwtPayload: JwtPayloadDTO = {
    sub: payload.userId,
    email: payload.email,
    rol: payload.rol,
    jti: payload.jti || crypto.randomUUID(),
  };
  return jwt.sign(jwtPayload, getRefreshSecret(), {
    expiresIn: (process.env.JWT_REFRESH_EXPIRES as any) || '7d',
    algorithm: 'HS256',
  });
}

/**
 * Registra un token o su JTI en la lista negra (en memoria y en la base de datos PostgreSQL).
 */
export async function revokeToken(
  token: string,
  motivo: string = 'Cierre de sesión de usuario'
): Promise<void> {
  let jti: string | undefined;
  let expiraEn = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000); // 7 días por defecto

  try {
    const decoded = jwt.decode(token) as (JwtPayloadDTO & { exp?: number; jti?: string }) | null;
    if (decoded) {
      if (decoded.jti) jti = decoded.jti;
      if (decoded.exp) expiraEn = new Date(decoded.exp * 1000);
    }
  } catch {
    // Si no es un JWT decodificable estándar, se usa el token en crudo
  }

  const primaryKey = jti || token;
  REVOKED_TOKENS_CACHE.add(token);
  if (jti) REVOKED_TOKENS_CACHE.add(jti);

  if (!process.env.DATABASE_URL) {
    return;
  }

  try {
    await prisma.revokedToken.upsert({
      where: { tokenJti: primaryKey },
      create: {
        tokenJti: primaryKey,
        expiraEn,
        motivo,
      },
      update: {
        motivo,
      },
    });
  } catch (error) {
    // Fallback seguro en memoria si PostgreSQL está offline o en entorno de tests
    console.warn('⚠️ [JWT] Token revocado en memoria. No se pudo persistir en PostgreSQL:', error);
  }
}

/**
 * Verifica si un token o su identificador (JTI) se encuentra en la lista de revocación.
 */
export async function isTokenRevoked(token: string, jti?: string): Promise<boolean> {
  // 1. Verificación en memoria (Ultra-rápido O(1))
  if (REVOKED_TOKENS_CACHE.has(token) || (jti && REVOKED_TOKENS_CACHE.has(jti))) {
    return true;
  }

  // Si no hay DATABASE_URL configurada, omitimos la consulta a Prisma
  if (!process.env.DATABASE_URL) {
    return false;
  }

  // 2. Verificación en la tabla RevokedToken de la base de datos
  try {
    const searchTargets = [token];
    if (jti) searchTargets.push(jti);

    const revokedRecord = await prisma.revokedToken.findFirst({
      where: {
        tokenJti: {
          in: searchTargets,
        },
      },
    });

    if (revokedRecord) {
      REVOKED_TOKENS_CACHE.add(revokedRecord.tokenJti);
      return true;
    }
  } catch {
    // Si la base de datos está offline, confiamos en la lista en memoria
  }

  return false;
}

export function verifyAccessToken(token: string): JwtPayloadDTO {
  const decoded = jwt.verify(token, getAccessSecret(), { algorithms: ['HS256'] }) as JwtPayloadDTO;
  
  if (REVOKED_TOKENS_CACHE.has(token) || (decoded.jti && REVOKED_TOKENS_CACHE.has(decoded.jti))) {
    const error = new Error('Token revocado. La sesión ha sido cerrada.');
    error.name = 'TokenRevokedError';
    throw error;
  }

  return decoded;
}

export async function verifyAccessTokenAsync(token: string): Promise<JwtPayloadDTO> {
  const decoded = verifyAccessToken(token);

  const revoked = await isTokenRevoked(token, decoded.jti);
  if (revoked) {
    const error = new Error('Token revocado. La sesión ha sido cerrada.');
    error.name = 'TokenRevokedError';
    throw error;
  }

  return decoded;
}

export function verifyRefreshToken(token: string): JwtPayloadDTO {
  const decoded = jwt.verify(token, getRefreshSecret(), { algorithms: ['HS256'] }) as JwtPayloadDTO;

  if (REVOKED_TOKENS_CACHE.has(token) || (decoded.jti && REVOKED_TOKENS_CACHE.has(decoded.jti))) {
    const error = new Error('Refresh token revocado. La sesión ha sido cerrada.');
    error.name = 'TokenRevokedError';
    throw error;
  }

  return decoded;
}

export interface Temp2FAPayload {
  sub: string;
  email: string;
  rol: UserRole;
  is2FA: boolean;
}

export function signTemp2FAToken(payload: { userId: string; email: string; rol: UserRole }): string {
  const jwtPayload: Temp2FAPayload = {
    sub: payload.userId,
    email: payload.email,
    rol: payload.rol,
    is2FA: true,
  };
  return jwt.sign(jwtPayload, getAccessSecret(), {
    expiresIn: '5m',
    algorithm: 'HS256',
  });
}

export function verifyTemp2FAToken(token: string): Temp2FAPayload {
  const decoded = jwt.verify(token, getAccessSecret(), { algorithms: ['HS256'] }) as Temp2FAPayload;
  if (!decoded.is2FA) {
    throw new Error('Token inválido para verificación de segundo factor');
  }
  return decoded;
}
