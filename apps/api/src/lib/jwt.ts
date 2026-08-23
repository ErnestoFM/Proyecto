// ==============================================================================
// Monchis Café — Servicio JWT Stateless (apps/api/src/lib/jwt.ts)
// ==============================================================================

import jwt from 'jsonwebtoken';
import { JwtPayloadDTO, UserRole } from '@monchis/shared-types';

const ACCESS_SECRET = process.env.JWT_ACCESS_SECRET || 'monchis_cafe_jwt_super_secret_access_key_32_characters_min';
const REFRESH_SECRET = process.env.JWT_REFRESH_SECRET || 'monchis_cafe_jwt_super_secret_refresh_key_32_characters_min';

export function signAccessToken(payload: { userId: string; email: string; rol: UserRole }): string {
  const jwtPayload: JwtPayloadDTO = {
    sub: payload.userId,
    email: payload.email,
    rol: payload.rol,
  };
  return jwt.sign(jwtPayload, ACCESS_SECRET, {
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
  return jwt.sign(jwtPayload, REFRESH_SECRET, {
    expiresIn: (process.env.JWT_REFRESH_EXPIRES as any) || '7d',
    algorithm: 'HS256',
  });
}

export function verifyAccessToken(token: string): JwtPayloadDTO {
  return jwt.verify(token, ACCESS_SECRET, { algorithms: ['HS256'] }) as JwtPayloadDTO;
}

export function verifyRefreshToken(token: string): JwtPayloadDTO {
  return jwt.verify(token, REFRESH_SECRET, { algorithms: ['HS256'] }) as JwtPayloadDTO;
}
