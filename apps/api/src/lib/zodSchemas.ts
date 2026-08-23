// ==============================================================================
// Monchis Café — Esquemas de Validación Zod (apps/api/src/lib/zodSchemas.ts)
// ==============================================================================

import { z } from 'zod';

export const LoginSchema = z.object({
  email: z.string().email('Formato de correo electrónico inválido').trim(),
  password: z.string().min(6, 'La contraseña debe tener al menos 6 caracteres'),
  recaptchaToken: z.string().min(1, 'Token de verificación reCAPTCHA requerido'),
});

export const RegisterSchema = z.object({
  nombre: z.string().min(2, 'El nombre debe tener al menos 2 caracteres').trim(),
  email: z.string().email('Formato de correo electrónico inválido').trim(),
  password: z.string().min(8, 'La contraseña debe tener al menos 8 caracteres'),
  rol: z.enum(['ADMIN', 'CAJERO', 'CLIENTE']).default('CLIENTE'),
  recaptchaToken: z.string().min(1, 'Token de verificación reCAPTCHA requerido'),
  utmSource: z.string().optional(),
  utmMedium: z.string().optional(),
  utmCampaign: z.string().optional(),
});

export const CreateOrderSchema = z.object({
  clienteId: z.string().uuid().optional(),
  metodoPago: z.enum(['EFECTIVO', 'TARJETA', 'TRANSFERENCIA', 'PUNTOS', 'MIXTO']),
  referenciaPago: z.string().trim().optional(),
  montoEfectivo: z.number().nonnegative().optional(),
  puntosUsados: z.number().int().nonnegative().optional(),
  traeTermoReutilizable: z.boolean().default(false),
  utmSource: z.string().optional(),
  utmCampaign: z.string().optional(),
  items: z
    .array(
      z.object({
        productoId: z.string().uuid('ID de producto inválido'),
        cantidad: z.number().int().positive('La cantidad debe ser mayor a 0'),
        precioUnitario: z.number().positive('El precio debe ser positivo'),
      })
    )
    .min(1, 'La orden debe contener al menos un producto'),
});
