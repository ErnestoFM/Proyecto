# Módulo de Autenticación Stateless y Google reCAPTCHA

#modulo #seguridad #jwt #recaptcha #rbac

## Resumen
Gestiona el acceso seguro y la protección anti-bots para **Monchis Café**.

## Características
- **JWT Stateless:** Access Token de 15 minutos en memoria y Refresh Token de 7 días en cookie `httpOnly`.
- **Google reCAPTCHA v2/v3:** Validación de tokens en frontend y backend (`/recaptcha/api/siteverify`).
- **RBAC:** Roles `ADMIN` (con 2FA obligatorio), `CAJERO` y `CLIENTE`.

## Enlaces Relacionados
- [[Arquitectura/Monorepo_Vue_Nextjs_RabbitMQ]]
- [[Modulos/Sistema_Diseno_Pastel_SEO]]
