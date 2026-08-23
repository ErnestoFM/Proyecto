// ==============================================================================
// Monchis Café — Middleware de Autorización RBAC (apps/api/src/middleware/authMiddleware.ts)
// ==============================================================================

import { NextRequest, NextResponse } from 'next/server';
import { verifyAccessToken } from '@/lib/jwt';
import { JwtPayloadDTO, UserRole } from '@monchis/shared-types';

export interface AuthenticatedRequest extends NextRequest {
  user?: JwtPayloadDTO;
}

export function requireAuth(allowedRoles?: UserRole[]) {
  return async (
    request: NextRequest,
    handler: (req: NextRequest, user: JwtPayloadDTO) => Promise<NextResponse>
  ): Promise<NextResponse> => {
    const authHeader = request.headers.get('authorization');

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json(
        { error: 'Acceso no autorizado. Se requiere encabezado Authorization: Bearer <token>' },
        { status: 401 }
      );
    }

    const token = authHeader.substring(7);

    try {
      const decodedUser = verifyAccessToken(token);

      // Verificación de Roles RBAC
      if (allowedRoles && allowedRoles.length > 0 && !allowedRoles.includes(decodedUser.rol)) {
        return NextResponse.json(
          {
            error: `Acceso denegado. Se requiere uno de los siguientes roles: ${allowedRoles.join(
              ', '
            )}`,
          },
          { status: 403 }
        );
      }

      return await handler(request, decodedUser);
    } catch (error: any) {
      if (error.name === 'TokenExpiredError') {
        return NextResponse.json(
          { error: 'El token de acceso ha expirado. Por favor solicite renovación (/api/auth/refresh).' },
          { status: 401 }
        );
      }
      return NextResponse.json({ error: 'Token de acceso inválido.' }, { status: 401 });
    }
  };
}
