# Arquitectura Monorepo — Monchis Café

#arquitectura #monorepo #vue3 #nextjs #rabbitmq #prisma

## Resumen
Monchis Café utiliza una arquitectura Monorepo administrada con `pnpm workspaces` y `Turborepo`.

## Estructura de Aplicaciones y Paquetes
- `apps/web`: Frontend Vue 3 + Vite + `vite-ssg` para prerenderizado SEO de páginas públicas.
- `apps/api`: Backend Next.js API Routes (Stateless REST API).
- `packages/database`: Modelos de datos PostgreSQL administrados con [[Modulos/Database_Prisma|Prisma ORM]].
- `packages/messaging`: Cliente de mensajería [[Arquitectura/Patron_Saga_DLQ|RabbitMQ y Coordinador Saga]].
- `packages/config`: Tokens CSS para el [[Modulos/Sistema_Diseno_Pastel_SEO|Sistema de Diseño Pastel]].
- `packages/shared-types`: DTOs e interfaces TypeScript compartidas.

## Enlaces Relacionados
- [[Arquitectura/Patron_Saga_DLQ]]
- [[Modulos/Autenticacion_Stateless_reCAPTCHA]]
- [[Modulos/Sistema_Diseno_Pastel_SEO]]
