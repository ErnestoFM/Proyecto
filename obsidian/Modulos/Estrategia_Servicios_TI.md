# Estrategia de Servicios TI — Monchis Café

#servicios_ti #itil #itsm #estrategia_servicio #catalogo_servicios #iso20000 #participacion #navarro_salcedo

Este documento sintetiza la **Estrategia Integral de Servicios TI** para la plataforma **Monchis Café**, diseñada para la **Actividad PARTICIPACIÓN: Gestión de Servicios Informáticos** evaluada por el **Dr. Gabriel Navarro Salcedo** (Universidad de Guadalajara / CUTonalá).

---

## 1. El Ciclo de Vida del Servicio TI (ITIL) Aplicado

```
                    ┌────────────────────────────────────────────────────────┐
                    │       CICLO DE VIDA DE LOS SERVICIOS TI (ITIL)         │
                    └────────────────────────────────────────────────────────┘
                                                 │
         ┌───────────────────────────────────────┼──────────────────────────────────────┐
         ▼                                       ▼                                      ▼
┌─────────────────────────────┐   ┌─────────────────────────────┐   ┌─────────────────────────────┐
│    1. SERVICE STRATEGY      │   │     2. SERVICE DESIGN       │   │    3. SERVICE TRANSITION    │
│  • Catálogo de Servicios    │   │  • SLAs (99.9% uptime)      │   │  • CI/CD GitHub Actions     │
│  • Utilidad y Garantía      │   │  • Seguridad Stateless JWT  │   │  • TDD (Vitest, Playwright) │
│  • Finanzas: CAPEX/OPEX     │   │  • Capacidad y Continuidad  │   │  • Gestión del Cambio       │
└─────────────────────────────┘   └─────────────────────────────┘   └─────────────────────────────┘
                                                 │
                                 ┌───────────────┴───────────────┐
                                 ▼                               ▼
                  ┌─────────────────────────────┐ ┌─────────────────────────────┐
                  │    4. SERVICE OPERATION     │ │ 5. CONTINUAL SERVICE IMPROV.│
                  │  • Mesa de Ayuda N0/N1/N2   │ │  • Ciclo Deming (PDCA)      │
                  │  • MTTR < 60 min            │ │  • KPIs de caja y latencia  │
                  │  • Telemetría y Dead Letter │ │  • Encuestas de satisfacción│
                  └─────────────────────────────┘ └─────────────────────────────┘
```

---

## 2. Catálogo de Servicios TI

1. **Servicios Core (Principales):**
   - **Punto de Venta Táctil (POS) Multimodal:** Cobro en efectivo, tarjeta (Stripe/Clip/Mercado Pago) y SPEI.
   - **Trazabilidad de Café Orgánico y Gestión PEPS:** Registro por cooperativa, finca, altitud, fecha de tueste y rotación PEPS.
   - **Programa de Fidelización y Monedero Digital ("Monchis Rewards"):** Sellos digitales (8.ª gratis tras 7 compras), cashback y bonificación de $5.00 MXN por termo/taza reusable ([[Planificacion_Sostenibilidad_ODS|Alineación ODS 12]]).
2. **Servicios Habilitadores (Enabling):**
   - **Plataforma Cloud y Broker Asíncrono:** RabbitMQ + Patrón Saga (reversas automáticas ante desabasto de insumos orgánicos).
   - **Almacenamiento Seguro Transaccional:** PostgreSQL con Prisma ORM e integridad referencial.
   - **Seguridad Perimetral y Autenticación Stateless:** JWT rotativos, Google reCAPTCHA v2/v3 y 2FA administrativo ([[Autenticacion_Stateless_reCAPTCHA]]).
3. **Servicios de Soporte (Support):**
   - **Mesa de Ayuda (Service Desk):** Soporte escalonado Nivel 0 (cajero), Nivel 1 (remoto < 15 min), Nivel 2 (ingeniería).
   - **Continuidad y Copias de Seguridad:** Respaldo diario en la nube con RTO < 60 minutos.
   - **Monitoreo Proactivo y Telemetría:** Monitoreo de `/api/health` y alertas SMTP por colas muertas (DLQ).

---

## 3. Generación de Valor: Utilidad vs. Garantía

- **Utilidad (*Fit for Purpose*):**
  - Reducción del tiempo de atención en barra de **2.5 min a < 45 s**.
  - Aumento de capacidad de atención en horas pico hasta un **60 %**.
  - Cierre de caja automatizado en 1 clic (ahorro de 40–60 min/día).
  - Reducción de mermas de café de especialidad en un **85 %**.
- **Garantía (*Fit for Use*):**
  - Disponibilidad contractual de **99.9 %** de uptime.
  - Consistencia transaccional del **100 %** (cero cobros no compensados).
  - Tiempo Medio de Recuperación ante Incidentes (MTTR) **$\le 60$ minutos**.

---

## 4. Presupuesto de Inversión y Operación

- **Inversión Inicial en Activos (CAPEX):** **$28,480 MXN** (Tabletas industriales, impresoras térmicas, lectores ópticos, capacitación y fondo de contingencia).
- **Gasto Operativo Mensual (OPEX):** **$4,850 MXN / mes** (Cloud GCP, base de datos PostgreSQL administrada, correo SMTP transaccional y soporte técnico mensual N1/N2).
- **Ahorro Anual Proyectado:** **>$36,000 MXN** frente a soluciones privativas como Soft Restaurant o Toast POS.

---

## 5. Diferenciación Competitiva Única

| Factor Clave | Soft Restaurant | Toast / Square | Monchis Café |
| :--- | :--- | :--- | :--- |
| **Trazabilidad Orgánica** | Genérica | Inexistente | **Nativa: Lote, finca, altitud y QR al comensal** |
| **Resiliencia Transaccional** | Rígida / Bloqueos | Dependiente de nube | **Patrón Saga (RabbitMQ) con reversas inmediatas** |
| **Sostenibilidad** | Nula | Puntos de tarjeta | **Bonificación por termo reusable (ODS 12)** |
| **SEO y Marketing Integrado** | Nula | Básica en web cerrada | **Prerenderizado vite-ssg + Atribución UTM (Maps vs IG)** |
| **Costos Recurrentes** | Licencia costosa | $69–$165 USD/mes | **Infraestructura ligera ($4,850 MXN/mes total)** |

---

## 🔗 Enlaces Relacionados
- [[Bitacora/2026-10-13|Bitácora de Trabajo - 2026-10-13]]
- [[Modulos/Aspectos_Legales_Contrato_Informatico|Contrato Informático y SLAs]]
- [[Modulos/Autenticacion_Stateless_reCAPTCHA|Módulo de Seguridad y Autenticación]]
- [[Modulos/Planificacion_Sostenibilidad_ODS|Planificación y Alineación ODS]]
- [[Modulos/Sistema_Diseno_Pastel_SEO|Diseño UI/UX y SEO vite-ssg]]
- Entregable oficial en PDF: [`docs/entregables/Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.pdf`](file:///d:/ernestofm/Proyecto/docs/entregables/Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.pdf)
- Entregable editable en Word: [`docs/entregables/Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.docx`](file:///d:/ernestofm/Proyecto/docs/entregables/Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.docx)
