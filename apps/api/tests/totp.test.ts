// ==============================================================================
// Pruebas Unitarias TDD — Doble Factor de Autenticación (2FA / TOTP)
// apps/api/tests/totp.test.ts
// ==============================================================================

import { describe, it, expect } from 'vitest';
import { TotpService, base32Encode, base32Decode } from '../src/lib/totp';
import { signTemp2FAToken, verifyTemp2FAToken } from '../src/lib/jwt';

describe('🔐 Módulo 2FA / TOTP — Monchis Café (RFC 6238 & RFC 4226)', () => {
  describe('1. Codificación y Decodificación Base32', () => {
    it('Debe codificar y decodificar correctamente manteniendo la integridad binaria', () => {
      const originalText = 'MonchisCafeSeguro2026';
      const buffer = Buffer.from(originalText, 'utf-8');
      const base32 = base32Encode(buffer);

      expect(typeof base32).toBe('string');
      expect(base32.length).toBeGreaterThan(0);

      const decoded = base32Decode(base32);
      expect(decoded.toString('utf-8')).toBe(originalText);
    });

    it('Debe lanzar error ante caracteres no válidos en Base32', () => {
      expect(() => base32Decode('INVALID189!')).toThrow();
    });
  });

  describe('2. Generación de Secreto y URI otpauth://', () => {
    it('Debe generar secretos Base32 criptográficamente seguros de 32 caracteres', () => {
      const secret = TotpService.generateSecret();
      expect(secret).toBeDefined();
      expect(secret.length).toBe(32);
      expect(/^[A-Z2-7]+$/.test(secret)).toBe(true);
    });

    it('Debe formatear correctamente el URI otpauth para Google Authenticator', () => {
      const secret = 'JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP';
      const email = 'admin@monchiscafe.com';
      const url = TotpService.getOtpAuthUrl(email, secret, 'Monchis Café');

      expect(url).toContain('otpauth://totp/');
      expect(url).toContain(`secret=${secret}`);
      expect(url).toContain('issuer=Monchis');
      expect(url).toContain('digits=6');
      expect(url).toContain('period=30');
    });

    it('Debe generar un Data URL con imagen PNG del código QR', async () => {
      const secret = TotpService.generateSecret();
      const url = TotpService.getOtpAuthUrl('admin@monchiscafe.com', secret);
      const qrDataUrl = await TotpService.generateQRCodeDataUrl(url);

      expect(qrDataUrl).toBeDefined();
      expect(qrDataUrl.startsWith('data:image/png;base64,')).toBe(true);
    });
  });

  describe('3. Generación y Validación de Tokens TOTP (RFC 6238)', () => {
    const testSecret = 'GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ';

    it('Debe generar códigos numéricos de exactamente 6 dígitos', () => {
      const code = TotpService.generateToken(testSecret);
      expect(code).toMatch(/^\d{6}$/);
    });

    it('Debe validar exitosamente el código actual', () => {
      const now = Date.now();
      const code = TotpService.generateToken(testSecret, now);
      const isValid = TotpService.verifyToken(code, testSecret, 1, now);

      expect(isValid).toBe(true);
    });

    it('Debe tolerar desfase de reloj dentro de la ventana de ±1 paso (±30s)', () => {
      const now = Date.now();
      // Token generado 25 segundos en el pasado
      const pastToken = TotpService.generateToken(testSecret, now - 25000);
      expect(TotpService.verifyToken(pastToken, testSecret, 1, now)).toBe(true);

      // Token generado 25 segundos en el futuro
      const futureToken = TotpService.generateToken(testSecret, now + 25000);
      expect(TotpService.verifyToken(futureToken, testSecret, 1, now)).toBe(true);
    });

    it('Debe rechazar códigos fuera de la ventana de tolerancia (> 90s)', () => {
      const now = Date.now();
      const expiredToken = TotpService.generateToken(testSecret, now - 120000); // 2 minutos atrás
      expect(TotpService.verifyToken(expiredToken, testSecret, 1, now)).toBe(false);
    });

    it('Debe rechazar códigos con formato incorrecto o caracteres inválidos', () => {
      expect(TotpService.verifyToken('12345', testSecret)).toBe(false);
      expect(TotpService.verifyToken('abcdef', testSecret)).toBe(false);
      expect(TotpService.verifyToken('', testSecret)).toBe(false);
    });
  });

  describe('4. Token Temporal de Autenticación 2FA (signTemp2FAToken)', () => {
    const mockUser = {
      userId: 'admin-uuid-1234',
      email: 'admin@monchiscafe.com',
      rol: 'ADMIN' as const,
    };

    it('Debe firmar un token temporal con flag is2FA y verificarlo', () => {
      const tempToken = signTemp2FAToken(mockUser);
      expect(tempToken).toBeDefined();

      const decoded = verifyTemp2FAToken(tempToken);
      expect(decoded.sub).toBe(mockUser.userId);
      expect(decoded.email).toBe(mockUser.email);
      expect(decoded.is2FA).toBe(true);
    });
  });
});
