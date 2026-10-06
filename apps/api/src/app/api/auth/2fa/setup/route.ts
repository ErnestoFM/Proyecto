// ==============================================================================
// Monchis Café — Endpoint GET /api/auth/2fa/setup (Configuración y Código QR TOTP)
// ==============================================================================

import { NextRequest, NextResponse } from 'next/server';
import { verifyAccessTokenAsync } from '@/lib/jwt';
import { TotpService } from '@/lib/totp';
import { prisma } from '@/lib/prisma';

export async function GET(request: NextRequest) {
  try {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json({ error: 'No autorizado: Token ausente' }, { status: 401 });
    }

    let payload;
    try {
      payload = await verifyAccessTokenAsync(authHeader.split(' ')[1]);
    } catch (err: any) {
      if (err.name === 'TokenRevokedError') {
        return NextResponse.json({ error: 'Token revocado o sesión cerrada' }, { status: 401 });
      }
      return NextResponse.json({ error: 'Token inválido o expirado' }, { status: 401 });
    }

    // El requerimiento exige 2FA para el rol Administrador
    if (payload.rol !== 'ADMIN') {
      return NextResponse.json(
        { error: 'Acceso restringido: La configuración de 2FA está reservada a administradores' },
        { status: 403 }
      );
    }

    const user = await prisma.user.findUnique({
      where: { id: payload.sub },
    });

    if (!user) {
      return NextResponse.json({ error: 'Usuario no encontrado' }, { status: 404 });
    }

    // Generar un nuevo secreto en formato Base32
    const secret = TotpService.generateSecret();
    const otpAuthUrl = TotpService.getOtpAuthUrl(user.email, secret, 'Monchis Café');
    const qrCodeDataUrl = await TotpService.generateQRCodeDataUrl(otpAuthUrl);

    return NextResponse.json({
      secret,
      otpAuthUrl,
      qrCodeDataUrl,
      dosFactoresActivo: user.dosFactoresActivo,
      mensaje: 'Escanee el código QR con Google Authenticator o ingrese la clave manualmente',
    });
  } catch (error: any) {
    console.error('❌ [Auth 2FA Setup] Error al generar configuración 2FA:', error);
    return NextResponse.json(
      { error: 'Error interno del servidor al generar configuración 2FA' },
      { status: 500 }
    );
  }
}
