// ==============================================================================
// Monchis Café — Pruebas Unitarias y de Seguridad (apps/api/tests/auth.test.ts)
// ==============================================================================

import { describe, it, expect, vi } from 'vitest';
import { signAccessToken, signRefreshToken, verifyAccessToken, verifyRefreshToken } from '../src/lib/jwt';
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

    it('Debe rechazar tokens vacíos', async () => {
      const isValid = await verifyGoogleRecaptcha('');
      expect(isValid).toBe(false);
    });
  });
});
