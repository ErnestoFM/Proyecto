import { NextRequest, NextResponse } from 'next/server';
import { revokeToken } from '@/lib/jwt';

export async function POST(request: NextRequest) {
  // 1. Revocar Access Token si viene en el encabezado Authorization
  const authHeader = request.headers.get('authorization');
  if (authHeader && authHeader.startsWith('Bearer ')) {
    const accessToken = authHeader.substring(7).trim();
    if (accessToken) {
      await revokeToken(accessToken, 'Cierre de sesión de usuario (Access Token)');
    }
  }

  // 2. Revocar Refresh Token si existe en la cookie HTTP-Only
  const refreshTokenCookie = request.cookies.get('monchis_refresh_token');
  if (refreshTokenCookie?.value) {
    await revokeToken(refreshTokenCookie.value, 'Cierre de sesión de usuario (Refresh Token)');
  }

  const response = NextResponse.json({
    mensaje: 'Sesión cerrada exitosamente. Tokens revocados.',
  });

  // 3. Expirar la cookie de refresh token inmediatamente
  response.cookies.set({
    name: 'monchis_refresh_token',
    value: '',
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    path: '/api/auth',
    maxAge: 0,
  });

  return response;
}
