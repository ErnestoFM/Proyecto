// ==============================================================================
// Monchis Café — Pruebas Unitarias y de Seguridad (apps/api/tests/auth.test.ts)
// ==============================================================================

import { describe, it, expect, vi } from 'vitest';
import {
  signAccessToken,
  signRefreshToken,
  verifyAccessToken,
  verifyRefreshToken,
  revokeToken,
  isTokenRevoked,
  verifyAccessTokenAsync,
} from '../src/lib/jwt';
import { hashPassword, comparePassword } from '../src/lib/password';
import { LoginSchema, RegisterSchema } from '../src/lib/zodSchemas';
import { verifyGoogleRecaptcha } from '../src/lib/recaptcha';

describe('🔒 Módulo de Autenticación Stateless y Seguridad (TDD)', () => {
  describe('1. Pruebas de Firma y Verificación JWT Stateless', () => {
    const mockUser = {
      userId: 'uuid-1234-5678',
      email: 'admin@monchiscafe.com',
      rol: 'ADMIN' as const,
    };

    it('Debe firmar y verificar un Access Token correctamente', () => {
      const token = signAccessToken(mockUser);
      expect(token).toBeDefined();
      expect(typeof token).toBe('string');

      const decoded = verifyAccessToken(token);
      expect(decoded.sub).toBe(mockUser.userId);
      expect(decoded.email).toBe(mockUser.email);
      expect(decoded.rol).toBe(mockUser.rol);
    });

    it('Debe firmar y verificar un Refresh Token correctamente', () => {
      const token = signRefreshToken(mockUser);
      expect(token).toBeDefined();

      const decoded = verifyRefreshToken(token);
      expect(decoded.sub).toBe(mockUser.userId);
      expect(decoded.email).toBe(mockUser.email);
    });

    it('Debe rechazar un token manipulado o con firma inválida', () => {
      const token = signAccessToken(mockUser);
      const tamperedToken = token.slice(0, -5) + 'xxxxx';

      expect(() => verifyAccessToken(tamperedToken)).toThrow();
    });
  });

  describe('2. Pruebas de Hashing de Contraseñas (bcrypt)', () => {
    const rawPassword = 'PasswordSeguro2026!';

    it('Debe generar un hash seguro diferente al texto plano', async () => {
      const hash = await hashPassword(rawPassword);
      expect(hash).not.toBe(rawPassword);
      expect(hash.startsWith('$2')).toBe(true); // Prefijo bcrypt
    });

    it('Debe validar correctamente la contraseña correcta', async () => {
      const hash = await hashPassword(rawPassword);
      const isValid = await comparePassword(rawPassword, hash);
      expect(isValid).toBe(true);
    });

    it('Debe rechazar contraseñas incorrectas', async () => {
      const hash = await hashPassword(rawPassword);
      const isValid = await comparePassword('PasswordIncorrecto', hash);
      expect(isValid).toBe(false);
    });
  });

  describe('3. Pruebas de Validación de Entradas y Prevención de Inyecciones (Zod)', () => {
    it('Debe aceptar entradas válidas en LoginSchema', () => {
      const validData = {
        email: 'cajero@monchiscafe.com',
        password: 'Password123!',
        recaptchaToken: 'token-recaptcha-valido',
      };

      const result = LoginSchema.safeParse(validData);
      expect(result.success).toBe(true);
    });

    it('Debe rechazar payloads de Inyección SQL en el campo email', () => {
      const sqlInjectionPayload = {
        email: "' OR 1=1 --",
        password: 'Password123!',
        recaptchaToken: 'token-recaptcha-valido',
      };

      const result = LoginSchema.safeParse(sqlInjectionPayload);
      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.flatten().fieldErrors.email).toBeDefined();
      }
    });

    it('Debe rechazar contraseñas débiles o vacías en RegisterSchema', () => {
      const invalidData = {
        nombre: 'C',
        email: 'email-invalido',
        password: '123',
        rol: 'CLIENTE',
        recaptchaToken: '',
      };

      const result = RegisterSchema.safeParse(invalidData);
      expect(result.success).toBe(false);
    });
  });

  describe('4. Pruebas de Verificación Google reCAPTCHA', () => {
    it('Debe validar tokens de prueba en ambiente de test', async () => {
      const isValid = await verifyGoogleRecaptcha('test-valid-recaptcha-token');
      expect(isValid).toBe(true);
    });

    it('Debe rechazar tokens vacíos o sólo espacios', async () => {
      const isValidEmpty = await verifyGoogleRecaptcha('');
      const isValidWhitespace = await verifyGoogleRecaptcha('   ');
      expect(isValidEmpty).toBe(false);
      expect(isValidWhitespace).toBe(false);
    });

    it('Debe rechazar tokens aleatorios sin clave secreta (sin bypass silencioso)', async () => {
      const originalSecret = process.env.RECAPTCHA_SECRET_KEY;
      delete process.env.RECAPTCHA_SECRET_KEY;

      const isValid = await verifyGoogleRecaptcha('token-aleatorio-no-autorizado');
      expect(isValid).toBe(false);

      if (originalSecret) process.env.RECAPTCHA_SECRET_KEY = originalSecret;
    });

    it('Debe rechazar tokens dummy en entorno de producción', async () => {
      const originalEnv = process.env.NODE_ENV;
      (process.env as any).NODE_ENV = 'production';

      const isValid = await verifyGoogleRecaptcha('test-valid-recaptcha-token');
      expect(isValid).toBe(false);

      (process.env as any).NODE_ENV = originalEnv;
    });
  });

  describe('5. Pruebas de Revocación Activa y Blacklist de Tokens (Logout Real)', () => {
    const mockUser = {
      userId: 'uuid-admin-blacklisted',
      email: 'admin.revoked@monchiscafe.com',
      rol: 'ADMIN' as const,
    };

    it('Debe incluir un identificador único jti en el token firmado', () => {
      const token = signAccessToken(mockUser);
      const decoded = verifyAccessToken(token);

      expect(decoded.jti).toBeDefined();
      expect(typeof decoded.jti).toBe('string');
      expect(decoded.jti!.length).toBeGreaterThan(10);
    });

    it('Debe revocar un token y detectar que está en la blacklist', async () => {
      const token = signAccessToken(mockUser);
      const decoded = verifyAccessToken(token);

      // Inicialmente no debe estar revocado
      expect(await isTokenRevoked(token, decoded.jti)).toBe(false);

      // Revocar el token
      await revokeToken(token, 'Cierre de sesión de prueba');

      // Debe figurar como revocado tanto por token como por jti
      expect(await isTokenRevoked(token, decoded.jti)).toBe(true);
      expect(await isTokenRevoked(token)).toBe(true);
      expect(await isTokenRevoked(decoded.jti!)).toBe(true);
    });

    it('Debe rechazar la verificación de un token revocado lanzando TokenRevokedError', async () => {
      const token = signAccessToken(mockUser);
      await revokeToken(token, 'Prueba de rechazo');

      // verifyAccessToken síncrono debe lanzar error
      expect(() => verifyAccessToken(token)).toThrow(/Token revocado/);

      // verifyAccessTokenAsync asíncrono debe rechazar la promesa
      await expect(verifyAccessTokenAsync(token)).rejects.toThrow(/Token revocado/);
    });

    it('Debe revocar un Refresh Token e impedir su verificación', async () => {
      const refreshToken = signRefreshToken(mockUser);
      const decoded = verifyRefreshToken(refreshToken);

      expect(await isTokenRevoked(refreshToken, decoded.jti)).toBe(false);

      await revokeToken(refreshToken, 'Prueba de revocación de Refresh Token');

      expect(await isTokenRevoked(refreshToken, decoded.jti)).toBe(true);
      expect(() => verifyRefreshToken(refreshToken)).toThrow(/Refresh token revocado/);
    });
  });
});

