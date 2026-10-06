// ==============================================================================
// Monchis Café — Endpoint POST /api/auth/2fa/verify (Verificación TOTP en Login)
// ==============================================================================

import { NextRequest, NextResponse } from 'next/server';
import { Verify2FASchema } from '@/lib/zodSchemas';
import { verifyTemp2FAToken, signAccessToken, signRefreshToken } from '@/lib/jwt';
import { TotpService } from '@/lib/totp';
import { prisma } from '@/lib/prisma';
import type { UserDTO } from '@monchis/shared-types';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const parseResult = Verify2FASchema.safeParse(body);

    if (!parseResult.success) {
      return NextResponse.json(
        { error: 'Datos de verificación 2FA inválidos', detalles: parseResult.error.flatten() },
        { status: 400 }
      );
    }

    const { tempToken, totpCode } = parseResult.data;

    // 1. Verificar firma y validez del token temporal
    let payload;
    try {
      payload = verifyTemp2FAToken(tempToken);
    } catch (tokenErr) {
      return NextResponse.json(
        { error: 'El token temporal de autenticación ha expirado o es inválido. Vuelva a iniciar sesión.' },
        { status: 401 }
      );
    }

    // 2. Obtener usuario de la base de datos
    const user = await prisma.user.findUnique({
      where: { id: payload.sub },
    });

    if (!user || !user.dosFactoresActivo || !user.dosFactoresSecret) {
      return NextResponse.json(
        { error: 'El usuario no tiene una configuración válida de 2FA.' },
        { status: 400 }
      );
    }

    // 3. Validar código TOTP de 6 dígitos
    const isValidTotp = TotpService.verifyToken(totpCode, user.dosFactoresSecret);
    if (!isValidTotp) {
      return NextResponse.json(
        { error: 'Código 2FA / TOTP incorrecto o expirado. Verifique su aplicación autenticadora.' },
        { status: 401 }
      );
    }

    // 4. Emitir tokens definitivos
    const tokenPayload = {
      userId: user.id,
      email: user.email,
      rol: user.rol,
    };

    const accessToken = signAccessToken(tokenPayload);
    const refreshToken = signRefreshToken(tokenPayload);

    const userDTO: UserDTO = {
      id: user.id,
      email: user.email,
      nombre: user.nombre,
      rol: user.rol,
      puntosFidelidad: user.puntosFidelidad,
      sellosAcumulados: user.sellosAcumulados,
      creadoEn: user.createdAt.toISOString(),
      dosFactoresActivo: true,
    };

    const response = NextResponse.json({
      mensaje: 'Autenticación de doble factor completada exitosamente',
      accessToken,
      usuario: userDTO,
    });

    response.cookies.set({
      name: 'monchis_refresh_token',
      value: refreshToken,
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      path: '/api/auth',
      maxAge: 7 * 24 * 60 * 60,
    });

    return response;
  } catch (error: any) {
    console.error('❌ [Auth 2FA] Error en verificación 2FA:', error);
    return NextResponse.json(
      { error: 'Error interno del servidor durante la verificación de doble factor' },
      { status: 500 }
    );
  }
}
