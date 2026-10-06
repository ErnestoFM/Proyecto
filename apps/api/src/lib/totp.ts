// ==============================================================================
// Monchis Café — Servicio TOTP / 2FA (RFC 6238 & RFC 4226)
// ==============================================================================

import crypto from 'crypto';
import QRCode from 'qrcode';

const BASE32_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';

/**
 * Codifica un Buffer a Base32 (RFC 4648 sin padding).
 */
export function base32Encode(buffer: Buffer): string {
  let bits = 0;
  let value = 0;
  let output = '';

  for (let i = 0; i < buffer.length; i++) {
    value = (value << 8) | buffer[i];
    bits += 8;

    while (bits >= 5) {
      output += BASE32_ALPHABET[(value >>> (bits - 5)) & 31];
      bits -= 5;
    }
  }

  if (bits > 0) {
    output += BASE32_ALPHABET[(value << (5 - bits)) & 31];
  }

  return output;
}

/**
 * Decodifica una cadena Base32 a Buffer.
 */
export function base32Decode(base32: string): Buffer {
  const cleaned = base32.toUpperCase().replace(/=+$/, '').replace(/\s+/g, '');
  let bits = 0;
  let value = 0;
  const bytes: number[] = [];

  for (let i = 0; i < cleaned.length; i++) {
    const idx = BASE32_ALPHABET.indexOf(cleaned[i]);
    if (idx === -1) {
      throw new Error(`Carácter Base32 no válido: ${cleaned[i]}`);
    }
    value = (value << 5) | idx;
    bits += 5;

    if (bits >= 8) {
      bytes.push((value >>> (bits - 8)) & 0xff);
      bits -= 8;
    }
  }

  return Buffer.from(bytes);
}

export class TotpService {
  /**
   * Genera un secreto aleatorio criptográficamente seguro en formato Base32 (20 bytes / 160 bits).
   */
  static generateSecret(): string {
    const randomBuffer = crypto.randomBytes(20);
    return base32Encode(randomBuffer);
  }

  /**
   * Construye el URI estándar otpauth:// compatible con Google Authenticator, Authy, etc.
   */
  static getOtpAuthUrl(email: string, secret: string, issuer = 'Monchis Café'): string {
    const label = `${issuer}:${email}`;
    const params = new URLSearchParams({
      secret,
      issuer,
      algorithm: 'SHA1',
      digits: '6',
      period: '30',
    });
    return `otpauth://totp/${encodeURIComponent(label)}?${params.toString()}`;
  }

  /**
   * Genera un código QR en Data URI (PNG Base64).
   */
  static async generateQRCodeDataUrl(otpAuthUrl: string): Promise<string> {
    return QRCode.toDataURL(otpAuthUrl, {
      errorCorrectionLevel: 'M',
      margin: 2,
      width: 256,
      color: {
        dark: '#4A3B32', // Tono café cálido de Monchis Café
        light: '#FFFFFF',
      },
    });
  }

  /**
   * Genera un código QR en formato SVG vectorial.
   */
  static async generateQRCodeSvg(otpAuthUrl: string): Promise<string> {
    return QRCode.toString(otpAuthUrl, {
      type: 'svg',
      errorCorrectionLevel: 'M',
      margin: 2,
      color: {
        dark: '#4A3B32',
        light: '#FFFFFF',
      },
    });
  }

  /**
   * Calcula el código TOTP actual de 6 dígitos para un secreto y timestamp dado (RFC 6238).
   */
  static generateToken(secret: string, timestamp = Date.now(), timeStepSec = 30): string {
    const counter = Math.floor(timestamp / (timeStepSec * 1000));
    const buffer = Buffer.alloc(8);
    buffer.writeBigInt64BE(BigInt(counter), 0);

    const key = base32Decode(secret);
    const hmac = crypto.createHmac('sha1', key).update(buffer).digest();

    const offset = hmac[hmac.length - 1] & 0x0f;
    const binary =
      ((hmac[offset] & 0x7f) << 24) |
      ((hmac[offset + 1] & 0xff) << 16) |
      ((hmac[offset + 2] & 0xff) << 8) |
      (hmac[offset + 3] & 0xff);

    const otp = (binary % 1_000_000).toString().padStart(6, '0');
    return otp;
  }

  /**
   * Valida un código TOTP de 6 dígitos considerando una ventana de tolerancia de ±1 paso (±30s).
   */
  static verifyToken(
    token: string,
    secret: string,
    window = 1,
    timestamp = Date.now(),
    timeStepSec = 30
  ): boolean {
    if (!token || !/^\d{6}$/.test(token.trim())) {
      return false;
    }

    const cleanToken = token.trim();

    try {
      for (let errorWindow = -window; errorWindow <= window; errorWindow++) {
        const checkTime = timestamp + errorWindow * timeStepSec * 1000;
        const generated = this.generateToken(secret, checkTime, timeStepSec);
        if (crypto.timingSafeEqual(Buffer.from(cleanToken), Buffer.from(generated))) {
          return true;
        }
      }
    } catch {
      return false;
    }

    return false;
  }
}
