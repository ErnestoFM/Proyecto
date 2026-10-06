// ==============================================================================
// Monchis Café — Servicio JWT Stateless (apps/api/src/lib/jwt.ts)
// ==============================================================================

import jwt from 'jsonwebtoken';
import { JwtPayloadDTO, UserRole } from '@monchis/shared-types';

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

export function signAccessToken(payload: { userId: string; email: string; rol: UserRole }): string {
  const jwtPayload: JwtPayloadDTO = {
    sub: payload.userId,
    email: payload.email,
    rol: payload.rol,
  };
  return jwt.sign(jwtPayload, getAccessSecret(), {
    expiresIn: (process.env.JWT_ACCESS_EXPIRES as any) || '15m',
    algorithm: 'HS256',
  });
}

export function signRefreshToken(payload: { userId: string; email: string; rol: UserRole }): string {
  const jwtPayload: JwtPayloadDTO = {
    sub: payload.userId,
    email: payload.email,
    rol: payload.rol,
  };
  return jwt.sign(jwtPayload, getRefreshSecret(), {
    expiresIn: (process.env.JWT_REFRESH_EXPIRES as any) || '7d',
    algorithm: 'HS256',
  });
}

export function verifyAccessToken(token: string): JwtPayloadDTO {
  return jwt.verify(token, getAccessSecret(), { algorithms: ['HS256'] }) as JwtPayloadDTO;
}

export function verifyRefreshToken(token: string): JwtPayloadDTO {
  return jwt.verify(token, getRefreshSecret(), { algorithms: ['HS256'] }) as JwtPayloadDTO;
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
