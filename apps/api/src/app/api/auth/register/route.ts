import { NextRequest, NextResponse } from 'next/server';
import { RegisterSchema } from '@/lib/zodSchemas';
import { verifyGoogleRecaptcha } from '@/lib/recaptcha';
import { hashPassword } from '@/lib/password';
import { signAccessToken, signRefreshToken } from '@/lib/jwt';
import { prisma } from '@/lib/prisma';
import { UserDTO } from '@monchis/shared-types';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const parseResult = RegisterSchema.safeParse(body);

    if (!parseResult.success) {
      return NextResponse.json(
        { error: 'Datos de registro inválidos', detalles: parseResult.error.flatten() },
        { status: 400 }
      );
    }

    const { nombre, email, password, rol, recaptchaToken, utmSource, utmMedium, utmCampaign } =
      parseResult.data;

    // 1. Verificación de Google reCAPTCHA
    const isCaptchaValid = await verifyGoogleRecaptcha(recaptchaToken);
    if (!isCaptchaValid) {
      return NextResponse.json(
        { error: 'Verificación de seguridad reCAPTCHA fallida. Acceso denegado.' },
        { status: 403 }
      );
    }

    // 2. Verificar existencia previa
    const existingUser = await prisma.user.findUnique({
      where: { email: email.toLowerCase() },
    });

    if (existingUser) {
      return NextResponse.json(
        { error: 'El correo electrónico ya se encuentra registrado.' },
        { status: 409 }
      );
    }

    // 3. Hashing de contraseña
    const passwordHash = await hashPassword(password);

    // 4. Creación del usuario y registro de atribución (transacción)
    const newUser = await prisma.$transaction(async (tx) => {
      const user = await tx.user.create({
        data: {
          nombre,
          email: email.toLowerCase(),
          passwordHash,
          rol,
          puntosFidelidad: utmSource ? 50 : 0, // Bono de bienvenida si proviene de campaña
        },
      });

      if (utmSource) {
        await tx.attribution.create({
          data: {
            userId: user.id,
            utmSource,
            utmMedium,
            utmCampaign,
            ipAddress: request.headers.get('x-forwarded-for') || undefined,
            userAgent: request.headers.get('user-agent') || undefined,
          },
        });
      }

      return user;
    });

    // 5. Emisión de Tokens JWT Stateless
    const tokenPayload = {
      userId: newUser.id,
      email: newUser.email,
      rol: newUser.rol,
    };

    const accessToken = signAccessToken(tokenPayload);
    const refreshToken = signRefreshToken(tokenPayload);

    const userDTO: UserDTO = {
      id: newUser.id,
      email: newUser.email,
      nombre: newUser.nombre,
      rol: newUser.rol,
      puntosFidelidad: newUser.puntosFidelidad,
      sellosAcumulados: newUser.sellosAcumulados,
      creadoEn: newUser.createdAt.toISOString(),
    };

    const response = NextResponse.json(
      {
        mensaje: 'Registro completado exitosamente',
        accessToken,
        usuario: userDTO,
      },
      { status: 201 }
    );

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
    console.error('❌ [Register API] Error en registro:', error);
    return NextResponse.json(
      { error: 'Error interno del servidor durante el registro' },
      { status: 500 }
    );
  }
}
