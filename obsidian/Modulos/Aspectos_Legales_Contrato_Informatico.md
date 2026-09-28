# Aspectos Legales y Contrato Informático — Monchis Café

#legal #contrato #derecho_informatico #lfda #lfpdppp #patrimonial #morales #unidad3

Este documento contextualiza la dimensión jurídica y contractual del software para **Monchis Café**, elaborado para la **Actividad 3.1: Contrato Informático** evaluada por el **Dr. Gabriel Navarro Salcedo**.

---

## 1. Elementos Formales del Contrato

```
                        ┌──────────────────────────────────────────────┐
                        │             CONTRATO INFORMÁTICO             │
                        └──────────────────────┬───────────────────────┘
                                               │
                 ┌─────────────────────────────┴─────────────────────────────┐
                 ▼                                                           ▼
  ┌───────────────────────────────┐                           ┌───────────────────────────────┐
  │    ELEMENTOS DE EXISTENCIA    │                           │     ELEMENTOS DE VALIDEZ      │
  ├───────────────────────────────┤                           ├───────────────────────────────┤
  │ • Consentimiento (expreso y   │                           │ • Capacidad jurídica          │
  │   electrónico CCom art. 89)   │                           │ • Ausencia de vicios          │
  │ • Objeto (directo e indirecto │                           │ • Licitud en objeto y fin     │
  │   de resultado verificable)   │                           │ • Forma escrita / electrónica │
  └───────────────────────────────┘                           └───────────────────────────────┘
```

---

## 2. Marco Normativo Positivo Mexicano Aplicable

- **Código de Comercio (Arts. 75, 89-114):** Calificación mercantil de los actos entre sociedades y profesionistas; plena validez probatoria de mensajes de datos, firma electrónica y contratación digital.
- **Código Civil Federal (Arts. 1792-1859, 2606-2643):** Consentimiento, vicios, prestación de servicios profesionales y contratos de obra a precio alzado.
- **Ley Federal del Derecho de Autor (Arts. 13 frac. XI, 30, 33, 83, 101-114):** Protección del software como obra asimilada a literaria. Los **derechos morales** permanecen inalienables en los desarrolladores físicos; los **derechos patrimoniales** se ceden a título **oneroso y temporal por 10 años** (art. 30 y 33) prorrogables mediante acuerdo escrito a Monchis Café tras la liquidación de los honorarios.
- **Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP):**
  - Principios rectores (arts. 6 al 11) y Aviso de Privacidad puesto a disposición (arts. 15-16).
  - Deber de implementar medidas técnicas y de seguridad (art. 18).
  - Notificación contractual de brechas del Encargado al Responsable en **24 horas**, permitiendo al Responsable informar de inmediato a los titulares afectados (art. 19).
  - Almacenamiento de contraseñas con hashing criptográfico unidireccional `bcrypt` y prohibición de guardar datos de tarjetas de pago (PCI-DSS).
- **Ley Federal del Trabajo (Arts. 12-15):** Exclusión de subcontratación de personal; no exigibilidad de REPSE debido a que se ejecuta con infraestructura y medios propios del prestador sin puesta a disposición de trabajadores.

---

## 3. Cláusulas Clave del Contrato de Monchis Café (22 Cláusulas)

1. **Naturaleza Mixta:** Prestación de servicios profesionales de ingeniería y obra informática a precio alzado.
2. **Objeto:** Plataforma web en Monorepo (Vue 3, Next.js API Routes, Prisma ORM, RabbitMQ Saga, JWT stateless, reCAPTCHA v2/v3).
3. **Plazo y Metodología:** 16 semanas exactas (112 días calendario: del 31 de agosto al 20 de diciembre de 2026), 8 Sprints quincenales bajo Scrum y TDD.
4. **Presupuesto y Hitos:** **$358,000.00 MXN neto** (+ 16% IVA = **$415,280.00 MXN**) por mano de obra calificada, desglosados en 9 hitos exigibles a los 5 días hábiles posteriores a la firma de Actas de Entrega-Recepción.
5. **Garantía y SLA:** 90 días naturales pos-entrega con ventana de servicio de Lunes a Sábado de 07:00 a 20:00 hrs (resolución de fallas críticas en menos de 12 horas hábiles).
6. **Responsabilidad y Sanciones:** Interés moratorio del 1.5% mensual por atraso del cliente, pena del 0.5% semanal por retraso del prestador y tope de responsabilidad limitada al 100% de lo efectivamente cobrado.
7. **Anexos Formales Integrados:** Anexo "A" (SOW), Anexo "B" (Gantt exacto de 16 semanas) y Anexo "C" (Presupuesto Integral de $418,275.00 MXN antes de IVA).

---

## 🔗 Enlaces Relacionados
- [[Bitacora/2026-09-19|Bitácora de Trabajo - 2026-09-19]]
- [[Arquitectura/Index|Arquitectura General del Sistema]]
- [[Contexto/Index|Contexto del Negocio Monchis Café]]
- Documento oficial completo: [`docs/entregables/Actividad_3_1_Contrato_Informatico_MonchisCafe.md`](file:///d:/ernestofm/Proyecto/docs/entregables/Actividad_3_1_Contrato_Informatico_MonchisCafe.md)
