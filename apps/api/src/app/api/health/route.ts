import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    status: 'UP',
    servicio: 'Monchis Café API',
    timestamp: new Date().toISOString(),
  });
}
