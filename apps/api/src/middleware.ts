// ==============================================================================
// Monchis Café — Middleware Global de Seguridad y CORS (Next.js)
// apps/api/src/middleware.ts
// ==============================================================================

import { NextRequest, NextResponse } from 'next/server';

const ALLOWED_ORIGINS = [
  process.env.VITE_APP_URL || 'http://localhost:3000',
  'http://localhost:3000',
  'http://localhost:8080',
  'https://monchiscafe.com',
  'https://monchis-cafe-prod.web.app',
];

export function middleware(request: NextRequest) {
  const origin = request.headers.get('origin') || '';
  const isAllowedOrigin = ALLOWED_ORIGINS.includes(origin) || process.env.NODE_ENV !== 'production';
  const effectiveOrigin = isAllowedOrigin && origin ? origin : ALLOWED_ORIGINS[0];

  // 1. Manejo inmediato de peticiones preflight CORS (OPTIONS)
  if (request.method === 'OPTIONS') {
    const preflightHeaders = new Headers({
      'Access-Control-Allow-Origin': effectiveOrigin,
      'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With, Accept, Origin, Cache-Control',
      'Access-Control-Allow-Credentials': 'true',
      'Access-Control-Max-Age': '86400',
      'Vary': 'Origin',
    });

    return new NextResponse(null, {
      status: 204,
      headers: preflightHeaders,
    });
  }

  // 2. Continuar con el handler correspondiente y añadir cabeceras de respuesta
  const response = NextResponse.next();

  response.headers.set('Access-Control-Allow-Origin', effectiveOrigin);
  response.headers.set('Access-Control-Allow-Credentials', 'true');
  response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS');
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, Accept, Origin');
  response.headers.set('Vary', 'Origin');

  // Cabeceras perimetrales de seguridad OWASP
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  response.headers.set('X-XSS-Protection', '1; mode=block');

  return response;
}

export const config = {
  matcher: '/api/:path*',
};

