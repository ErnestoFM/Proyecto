import { NextRequest, NextResponse } from 'next/server';
import { LoginSchema } from '@/lib/zodSchemas';
import { verifyGoogleRecaptcha } from '@/lib/recaptcha';
import { comparePassword } from '@/lib/password';
import { signAccessToken, signRefreshToken } from '@/lib/jwt';
import { prisma } from '@/lib/prisma';
import { UserDTO } from '@monchis/shared-types';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const parseResult = LoginSchema.safeParse(body);

    if (!parseResult.success) {
      return NextResponse.json(
        { error: 'Datos de entrada inválidos', detalles: parseResult.error.flatten() },
        { status: 400 }
      );
    }

    const { email, password, recaptchaToken } = parseResult.data;

    // 1. Verificación de Google reCAPTCHA
    const isCaptchaValid = await verifyGoogleRecaptcha(recaptchaToken);
    if (!isCaptchaValid) {
      return NextResponse.json(
        { error: 'Verificación de seguridad reCAPTCHA fallida. Acceso denegado.' },
        { status: 403 }
      );
    }

    // 2. Búsqueda de Usuario en Base de Datos
    const user = await prisma.user.findUnique({
      where: { email: email.toLowerCase() },
    });

    if (!user) {
      return NextResponse.json(
        { error: 'Credenciales inválidas (usuario o contraseña incorrectos).' },
        { status: 401 }
      );
    }

    // 3. Verificación de Contraseña (bcrypt)
    const isPasswordValid = await comparePassword(password, user.passwordHash);
    if (!isPasswordValid) {
      return NextResponse.json(
        { error: 'Credenciales inválidas (usuario o contraseña incorrectos).' },
        { status: 401 }
      );
    }

    // 4. Emisión de Tokens JWT Stateless
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
    };

    // 5. Respuesta con Access Token en Body y Refresh Token en Cookie httpOnly
    const response = NextResponse.json({
      mensaje: 'Inicio de sesión exitoso',
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
      maxAge: 7 * 24 * 60 * 60, // 7 días en segundos
    });

    return response;
  } catch (error: any) {
    console.error('❌ [Auth API] Error en login:', error);
    return NextResponse.json(
      { error: 'Error interno del servidor durante la autenticación' },
      { status: 500 }
    );
  }
}
