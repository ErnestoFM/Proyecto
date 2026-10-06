// ==============================================================================
// Monchis Café — Endpoint POST /api/auth/2fa/disable (Desactivar 2FA)
// ==============================================================================

import { NextRequest, NextResponse } from 'next/server';
import { verifyAccessTokenAsync } from '@/lib/jwt';
import { Disable2FASchema } from '@/lib/zodSchemas';
import { TotpService } from '@/lib/totp';
import { prisma } from '@/lib/prisma';

export async function POST(request: NextRequest) {
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

    if (payload.rol !== 'ADMIN') {
      return NextResponse.json(
        { error: 'Acceso restringido a administradores' },
        { status: 403 }
      );
    }

    const body = await request.json();
    const parseResult = Disable2FASchema.safeParse(body);

    if (!parseResult.success) {
      return NextResponse.json(
        { error: 'Código 2FA requerido para desactivación', detalles: parseResult.error.flatten() },
        { status: 400 }
      );
    }

    const { totpCode } = parseResult.data;

    const user = await prisma.user.findUnique({
      where: { id: payload.sub },
    });

    if (!user || !user.dosFactoresActivo || !user.dosFactoresSecret) {
      return NextResponse.json(
        { error: 'El doble factor no está activo en esta cuenta.' },
        { status: 400 }
      );
    }

    const isValid = TotpService.verifyToken(totpCode, user.dosFactoresSecret);
    if (!isValid) {
      return NextResponse.json(
        { error: 'Código 2FA incorrecto. No se puede desactivar la protección.' },
        { status: 401 }
      );
    }

    await prisma.user.update({
      where: { id: payload.sub },
      data: {
        dosFactoresActivo: false,
        dosFactoresSecret: null,
      },
    });

    return NextResponse.json({
      mensaje: 'Doble factor de autenticación desactivado.',
      dosFactoresActivo: false,
    });
  } catch (error: any) {
    console.error('❌ [Auth 2FA Disable] Error al desactivar 2FA:', error);
    return NextResponse.json(
      { error: 'Error interno del servidor al desactivar 2FA' },
      { status: 500 }
    );
  }
}
