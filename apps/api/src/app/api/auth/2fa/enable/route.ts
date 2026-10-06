// ==============================================================================
// Monchis Café — Endpoint POST /api/auth/2fa/enable (Activar 2FA para Administrador)
// ==============================================================================

import { NextRequest, NextResponse } from 'next/server';
import { verifyAccessToken } from '@/lib/jwt';
import { Enable2FASchema } from '@/lib/zodSchemas';
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
      payload = verifyAccessToken(authHeader.split(' ')[1]);
    } catch {
      return NextResponse.json({ error: 'Token inválido o expirado' }, { status: 401 });
    }

    if (payload.rol !== 'ADMIN') {
      return NextResponse.json(
        { error: 'Acceso restringido a administradores' },
        { status: 403 }
      );
    }

    const body = await request.json();
    const parseResult = Enable2FASchema.safeParse(body);

    if (!parseResult.success) {
      return NextResponse.json(
        { error: 'Datos de activación inválidos', detalles: parseResult.error.flatten() },
        { status: 400 }
      );
    }

    const { secret, totpCode } = parseResult.data;

    // Verificar que el código ingresado coincida con el secreto antes de guardarlo
    const isValid = TotpService.verifyToken(totpCode, secret);
    if (!isValid) {
      return NextResponse.json(
        { error: 'Código 2FA incorrecto. Asegúrese de que la hora de su dispositivo esté sincronizada.' },
        { status: 400 }
      );
    }

    // Persistir estado de 2FA en la base de datos
    await prisma.user.update({
      where: { id: payload.sub },
      data: {
        dosFactoresActivo: true,
        dosFactoresSecret: secret,
      },
    });

    return NextResponse.json({
      mensaje: 'Doble factor de autenticación (2FA / TOTP) activado exitosamente.',
      dosFactoresActivo: true,
    });
  } catch (error: any) {
    console.error('❌ [Auth 2FA Enable] Error al activar 2FA:', error);
    return NextResponse.json(
      { error: 'Error interno del servidor al activar 2FA' },
      { status: 500 }
    );
  }
}
