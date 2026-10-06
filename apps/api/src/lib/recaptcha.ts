// ==============================================================================
// Monchis Café — Verificador de Google reCAPTCHA (apps/api/src/lib/recaptcha.ts)
// ==============================================================================

export interface RecaptchaVerifyResponse {
  success: boolean;
  score?: number;
  action?: string;
  challenge_ts?: string;
  hostname?: string;
  'error-codes'?: string[];
}

export async function verifyGoogleRecaptcha(token: string): Promise<boolean> {
  // Tokens vacíos o ausentes siempre deben ser rechazados
  if (!token || token.trim() === '') {
    return false;
  }

  const isProduction = process.env.NODE_ENV === 'production';
  const isTestOrDev = process.env.NODE_ENV === 'test' || process.env.NODE_ENV === 'development';
  const isTestToken = token === 'test-valid-recaptcha-token';

  // Permitir token de prueba explícito ÚNICAMENTE fuera de producción (tests y desarrollo controlado)
  if (isTestOrDev && isTestToken) {
    return true;
  }

  // En producción, rechazar tajantemente el token dummy de prueba
  if (isProduction && isTestToken) {
    console.warn('⚠️ [reCAPTCHA] Intento de utilizar token de prueba dummy en ambiente de producción.');
    return false;
  }

  const secretKey = process.env.RECAPTCHA_SECRET_KEY;

  if (!secretKey) {
    if (isProduction) {
      console.error('❌ [reCAPTCHA] CRÍTICO: RECAPTCHA_SECRET_KEY no configurada en producción.');
    } else {
      console.warn(
        "⚠️ [reCAPTCHA] RECAPTCHA_SECRET_KEY no configurada. Token rechazado para evitar bypass silencioso. Use 'test-valid-recaptcha-token' en pruebas locales."
      );
    }
    return false;
  }

  try {
    const url = `https://www.google.com/recaptcha/api/siteverify?secret=${encodeURIComponent(
      secretKey
    )}&response=${encodeURIComponent(token)}`;

    const response = await fetch(url, { method: 'POST' });
    const data: RecaptchaVerifyResponse = await response.json();

    if (!data.success) {
      console.warn('⚠️ [reCAPTCHA] Verificación fallida de Google:', data['error-codes']);
      return false;
    }

    // Para reCAPTCHA v3, validar umbral de score (ej. >= 0.5)
    if (typeof data.score === 'number' && data.score < 0.5) {
      console.warn(`⚠️ [reCAPTCHA] Score bajo detectado (${data.score}) - Posible Bot`);
      return false;
    }

    return true;
  } catch (error) {
    console.error('❌ [reCAPTCHA] Error al contactar API de Google reCAPTCHA:', error);
    return false;
  }
}
