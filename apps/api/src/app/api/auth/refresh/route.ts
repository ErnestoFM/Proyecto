import { NextRequest, NextResponse } from 'next/server';
import { verifyRefreshToken, signAccessToken, signRefreshToken } from '@/lib/jwt';
import { prisma } from '@/lib/prisma';

export async function POST(request: NextRequest) {
  try {
    const refreshTokenCookie = request.cookies.get('monchis_refresh_token');

    if (!refreshTokenCookie || !refreshTokenCookie.value) {
      return NextResponse.json(
        { error: 'No se encontró cookie de refresh token' },
        { status: 401 }
      );
    }

    // 1. Verificación del Refresh Token
    let decoded;
    try {
      decoded = verifyRefreshToken(refreshTokenCookie.value);
    } catch (err) {
      return NextResponse.json(
        { error: 'Refresh token inválido o expirado' },
        { status: 401 }
      );
    }

    // 2. Comprobar que el usuario aún existe y está activo
    const user = await prisma.user.findUnique({
      where: { id: decoded.sub },
    });

    if (!user) {
      return NextResponse.json(
        { error: 'Usuario no encontrado' },
        { status: 401 }
      );
    }

    // 3. Rotación de Tokens (Emisión de nuevo par)
    const tokenPayload = {
      userId: user.id,
      email: user.email,
      rol: user.rol,
    };

    const newAccessToken = signAccessToken(tokenPayload);
    const newRefreshToken = signRefreshToken(tokenPayload);

    const response = NextResponse.json({
      mensaje: 'Tokens renovados exitosamente',
      accessToken: newAccessToken,
    });

    response.cookies.set({
      name: 'monchis_refresh_token',
      value: newRefreshToken,
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      path: '/api/auth',
      maxAge: 7 * 24 * 60 * 60,
    });

    return response;
  } catch (error: any) {
    console.error('❌ [Refresh API] Error renovando token:', error);
    return NextResponse.json(
      { error: 'Error interno del servidor durante la renovación de sesión' },
      { status: 500 }
    );
  }
}
