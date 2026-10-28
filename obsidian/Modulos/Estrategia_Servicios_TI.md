# Estrategia de Servicios TI — Monchis Café

#servicios_ti #itil #itsm #estrategia_servicio #catalogo_servicios #iso20000 #participacion #navarro_salcedo

Este documento sintetiza la **Estrategia Integral de Servicios TI** para la plataforma **Monchis Café**, diseñada para la **Actividad PARTICIPACIÓN: Gestión de Servicios Informáticos** evaluada por el **Dr. Gabriel Navarro Salcedo** (Universidad de Guadalajara / CUTonalá).

---

## 1. El Ciclo de Vida del Servicio TI (ITIL 2011) Aplicado

A diferencia de ITIL 4 que organiza los servicios en el Sistema de Valor del Servicio (AXELOS, 2019), este trabajo aplica didácticamente el ciclo de vida clásico de cinco fases de **ITIL 2011** (Cabinet Office, 2011a–e):

1. **Estrategia del Servicio (*Service Strategy*):** Portafolio de servicios activos y en desarrollo, análisis de Costo Total de Propiedad (TCO base a 3 años = $72,540 MXN) y análisis de la demanda para anticipar picos de mostrador (Cabinet Office, 2011d).
2. **Diseño del Servicio (*Service Design*):** Acuerdos internos de nivel de servicio (SLA/SLO propuestos: 99.5 % de disponibilidad en horario comercial ≈ 94 min/mes tolerados), dimensionamiento de capacidad en VM Compute Engine `e2-medium` (4 GB RAM para soportar RabbitMQ según guías oficiales en entorno piloto) con latencia $\le 450$ ms (P95), Cloud SQL PostgreSQL `db-f1-micro` en `us-central1`, seguridad de acceso RBAC/JWT alineada con ISO/IEC 27001 (ISO/IEC, 2022) y gestión de la continuidad del servicio de TI (ITSCM) con RTO $\le 45$ min y RPO $\le 24$ h (Cabinet Office, 2011b).
3. **Transición del Servicio (*Service Transition*):** Integración continua en GitHub Actions, pruebas automatizadas de endpoints y transacciones compensatorias Saga (DevOps: Bass et al., 2015; Kim et al., 2016), control de cambios por pull requests y talleres prácticos de capacitación (Cabinet Office, 2011e).
4. **Operación del Servicio (*Service Operation*):** Mesa de ayuda estructurada (propuesta) escalonada (Nivel 0 en barra, Nivel 1 soporte interno por desarrollador, Nivel 2 ingeniería), gestión de incidentes con MTTR $\le 45$ min, gestión de problemas mediante análisis de causa raíz, y gestión de accesos RBAC (Cabinet Office, 2011c).
5. **Mejora Continua del Servicio (*Continual Service Improvement*):** Ciclo Deming (PDCA) con revisiones trimestrales de indicadores de atención frente a la meta de $\le 75$ segundos y encuestas cualitativas de satisfacción (Cabinet Office, 2011a).

---

## 2. Catálogo de Servicios TI (9 Servicios)

| Nivel | Servicio | Descripción Funcional | Componente Base |
| :--- | :--- | :--- | :--- |
| **Principal (Core)** | Punto de Venta en Barra (POS) | Registro rápido de comandas, cobro mixto (efectivo, tarjeta, SPEI) y emisión de tickets térmicos. | Vue 3 SPA, API Node.js y lectores térmicos 80 mm. |
| **Principal (Core)** | Trazabilidad de Café y Control PEPS | Registro de lotes por cooperativa campesina, altitud y rotación de primeras entradas y primeras salidas. | Modelos PostgreSQL con Prisma ORM y códigos QR. |
| **Principal (Core)** | Fidelización "Monchis Rewards" | Registro digital de consumos para otorgar bebidas de cortesía por acumulación (una bebida al acumular 10 consumos) y bonificaciones por recipientes reusables. | Módulo de cliente en web y saldos en base de datos. |
| **Habilitador (Enabling)** | Plataforma Cloud y Mensajería | Transporte de eventos asíncronos de venta y soporte para transacciones compensatorias. | VM Compute Engine `e2-medium` (4 GB RAM) en GCP y broker RabbitMQ. |
| **Habilitador (Enabling)** | Persistencia Transaccional | Almacenamiento relacional de ventas, compras e historial de movimientos de insumos con integridad ACID. | PostgreSQL en Cloud SQL (`db-f1-micro`) en `us-central1`. |
| **Habilitador (Enabling)** | Seguridad de Acceso y Autenticación | Control de sesiones con JWT, cookies seguras httpOnly, Google reCAPTCHA y roles RBAC alineado con ISO/IEC 27001 y LFPDPPP. | Middlewares de autenticación en backend API. |
| **Soporte (Enhancing)** | Mesa de Ayuda Técnica | Atención escalonada para resolver incidencias de hardware o red en mostrador. | Soporte interno en sitio y asistencia remota para baristas. |
| **Soporte (Enhancing)** | Continuidad y Respaldos | Respaldos diarios de base de datos con tiempo de recuperación (RTO) $\le 45$ min y RPO $\le 24$ h. | Tareas programadas en Cloud SQL y almacenamiento en Cloud Storage. |
| **Soporte (Enhancing)** | Monitoreo de Disponibilidad | Sondeo periódico de rutas (/api/health) y alertas SMTP ante mensajes en colas de error. | Scripts de telemetría y servicio SMTP transaccional. |

---

## 3. Matriz de Priorización de Servicios (9 Servicios Completos)

| Prioridad | Servicio | Imp (35%) | Urg (25%) | Viab (25%) | Riesgo (15%) | Total | Fase de Implementación |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **P1** | Punto de Venta en Barra (POS) | 5.0 | 5.0 | 4.5 | 4.0 | **4.73** | Fase 1 / Sprints 1–2 / Semanas 1–4 |
| **P1** | Persistencia Transaccional | 5.0 | 5.0 | 4.5 | 3.5 | **4.65** | Fase 1 / Sprints 1–2 / Semanas 1–3 |
| **P1** | Seguridad de Acceso y Autenticación | 5.0 | 4.5 | 4.5 | 4.0 | **4.60** | Fase 1 / Sprints 1–2 / Semanas 2–4 |
| **P2** | Trazabilidad de Café y Control PEPS | 4.5 | 4.0 | 4.0 | 3.5 | **4.10** | Fase 2 / Sprints 3–4 / Semanas 5–8 |
| **P2** | Fidelización "Monchis Rewards" | 4.0 | 3.0 | 4.5 | 4.5 | **3.95** | Fase 2 / Sprints 3–4 / Semanas 7–8 |
| **P2** | Plataforma Cloud y Mensajería | 4.0 | 4.0 | 4.0 | 3.5 | **3.93** | Fase 2 / Sprints 3–4 / Semanas 5–7 |
| **P3** | Continuidad y Respaldos | 4.0 | 3.5 | 4.0 | 4.0 | **3.88** | Fase 3 / Sprints 5–6 / Semanas 9–11 |
| **P3** | Mesa de Ayuda Técnica | 3.5 | 4.0 | 4.0 | 4.0 | **3.83** | Fase 3 / Sprints 5–6 / Semanas 10–12 |
| **P4** | Monitoreo de Disponibilidad | 3.5 | 3.5 | 4.0 | 4.0 | **3.70** | Fase 4 / Sprints 7–8 / Semanas 13–16 |

Fórmula: Puntaje Total = (Impacto en Negocio × 0.35) + (Urgencia Operativa × 0.25) + (Viabilidad Técnica × 0.25) + (Riesgo Mitigado × 0.15)

---

## 4. Presupuesto y Costo Total de Propiedad (TCO a 3 Años)

- **CAPEX Inicial:** **$26,180 MXN**
  - 2 tabletas Samsung Galaxy Tab A9+ 11.0" 8GB RAM: $8,400 MXN* + 2 bases de mostrador: $3,200 MXN* = $11,600 MXN*.
  - 2 impresoras térmicas 80 mm y 2 lectores 2D: $7,400 MXN*.
  - Dominio .com.mx (año 1 vía Akky): $680 MXN (Cloudflare DNS/TLS gratuito).
  - Taller de capacitación inicial: $3,000 MXN*.
  - Fondo de contingencia operativa: $3,500 MXN*.
- **OPEX Mensual:** **$1,250 MXN / mes**
  - Compute Engine `e2-medium` (4 GB RAM): $600 MXN/mes (~$30 USD).
  - Cloud SQL PostgreSQL `db-f1-micro`: $450 MXN/mes (~$22.50 USD).
  - Servicio SMTP transaccional: $200 MXN/mes (~$10 USD).
  - Soporte técnico Nivel 1/2 y mantenimiento: $0 MXN (asumido internamente; referencia externa ~$3,600 MXN/mes*).
- **TCO Proyectado a 3 Años (36 Meses):**
  $$\text{TCO} = \$26{,}180 + (36 \times \$1{,}250) + (\$680 \times 2) = \$26{,}180 + \$45{,}000 + \$1{,}360 = \mathbf{\$72{,}540 \text{ MXN}}$$
- **Nota sobre Esfuerzo de Desarrollo:** Excluido del TCO base por ser proyecto académico. Si se cotizara comercialmente (680 horas equivalentes a 2 desarrolladores medio tiempo durante 16 semanas × $320 MXN/h* = $217,600 MXN*), el TCO ascendería a $290,140 MXN (o $419,740 MXN sumando soporte externo).

---

## 5. Comparativa Competitiva en México (2026)

| Factor Clave | Soft Restaurant 12 Pro (National Soft, 2026) | Loyverse POS (Loyverse, 2026) | Monchis Café (Desarrollo Propio) |
| :--- | :--- | :--- | :--- |
| **TCO a 3 Años (2 Estaciones)** | **~$75,400 MXN\*** ($23,000 hardware + $45,900 suscripción + $6,500 implementación) | **$51,400 a $105,400 MXN\*** ($19,000 hardware + $32,400 suscripción 4 empleados + $0 a $54,000 soporte) | **$72,540 MXN** (soporte interno y desarrollo académico excluidos) |
| **Trazabilidad de Café de Especialidad** | Genérica; no contempla parcelas campesinas ni altitud. | Insumos generales; sin registro agronómico ni cooperativas. | **Propuesta:** Finca, cooperativa, altitud, perfil de tueste, rotación PEPS y código QR. |
| **Modo Offline** | Operación local en Windows; sincroniza con SR Cloud. | Ventas y turnos locales; bloquea reembolsos, clientes y stock negativo. | **Propuesta:** Modo degradado con almacenamiento temporal y notas de contingencia. |
| **Resiliencia Transaccional** | Arquitectura cliente-servidor clásica. | Dependiente de nube; sin transacciones distribuidas. | **Propuesta:** Orquestador Saga y transacciones compensatorias sobre RabbitMQ. |
| **Sostenibilidad (ODS 12)** | Módulos comerciales tradicionales sin enfoque ambiental. | Sistema de lealtad estándar por puntos. | **Propuesta:** Bonificación fija en caja por uso de termo reutilizable (ODS 12). |
| **Soporte Técnico y Nivel de Servicio** | Soporte de marca incluido en suscripción. | Chat en línea ($0) o póliza externa local (~$1,500/mes\*). | **Propuesta:** Acuerdos internos propuestos (SLA/SLO: MTTR ≤ 45 min, disp. 99.5%). |

---

## 🔗 Enlaces Relacionados
- [[Bitacora/2026-10-17|Bitácora de Trabajo - 2026-10-17]]
- [[Modulos/Aspectos_Legales_Contrato_Informatico|Contrato Informático y Marco LFPDPPP]]
- [[Modulos/Autenticacion_Stateless_reCAPTCHA|Módulo de Seguridad y Autenticación]]
- [[Modulos/Planificacion_Sostenibilidad_ODS|Planificación y Alineación ODS]]
- [[Modulos/Sistema_Diseno_Pastel_SEO|Diseño UI/UX y SEO vite-ssg]]
- Entregable oficial en PDF: [`docs/entregables/Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.pdf`](file:///d:/ernestofm/Proyecto/docs/entregables/Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.pdf)
- Entregable editable en Word: [`docs/entregables/Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.docx`](file:///d:/ernestofm/Proyecto/docs/entregables/Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.docx)
