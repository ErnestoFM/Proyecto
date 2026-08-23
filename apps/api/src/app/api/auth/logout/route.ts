import { NextResponse } from 'next/server';

export async function POST() {
  const response = NextResponse.json({
    mensaje: 'Sesión cerrada exitosamente',
  });

  // Expira la cookie de refresh token inmediatamente
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
