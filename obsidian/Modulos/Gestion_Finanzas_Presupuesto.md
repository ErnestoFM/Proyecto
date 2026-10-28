# Gestión de Finanzas y Presupuesto del Proyecto — Monchis Café

#finanzas #presupuesto #gestion_costos #nomina #roi #estrategia_venta #monchis_cafe #navarro_salcedo

Documento técnico que consolida el modelo financiero, la estructura de costos operativos, mano de obra calificada conforme a la legislación fiscal mexicana (2026), amortización de activos y la estrategia de venta comercial para la plataforma web y sistema de punto de venta (POS) **Monchis Café**.

---

## 1. Ficha Técnica y Métricas Clave

| Variable Financiera | Valor Proyectado (MXN) | Base Metodológica |
|:---|:---:|:---|
| **Costo Base Total (CTB)** | **$573,160.08** | Nómina + Gastos Fijos + Nube + Amortización + Financiamiento |
| **Fondo de Contingencia (10%)** | **$57,316.01** | Reserva del 10% sobre el Costo Base Total para mitigación de riesgos |
| **Costo Total del Proyecto (CTP)** | **$630,476.09** | Inversión neta requerida por la empresa desarrolladora (4 meses) |
| **Margen Deseado sobre Ventas** | **30.0%** | Margen real sobre precio facturado: $P = CTP / (1 - 0.30)$ |
| **Precio de Venta sin IVA (Cotización)** | **$900,680.12** | Cotización formal del contrato de desarrollo de software |
| **IVA Trasladado (16%)** | **$144,108.82** | Impuesto de ley trasladado al cliente final |
| **Facturación Total con IVA** | **$1,044,788.94** | Importe bruto total convenido con el cliente |
| **Utilidad Bruta Proyectada** | **$270,204.04** | Ganancia neta empresarial previa a ISR corporativo anual |
| **Punto de Equilibrio** | **1 Solución** | 1 contrato llave en mano absorbe el 100% de los costos operativos |

---

## 2. Estructura Presupuestal por Rubros

### 2.1 Mano de Obra y Nómina Calificada (73.81% del CTP)
- **Equipo Técnico:** 4 perfiles asignados por 16 semanas (2,560 horas de ingeniería acumuladas en 8 sprints quincenales).
  1. *Líder de Proyecto / Scrum Master & DevOps:* $36,000.00 MXN bruto/mes (Costo empresa: $46,800.00 MXN/mes con 30% carga patronal).
  2. *Desarrolladora Frontend Core (Vue 3 / UI/UX):* $20,000.00 MXN bruto/mes (Costo empresa: $26,000.00 MXN/mes).
  3. *Desarrollador Backend Core (Next.js / RabbitMQ):* $20,000.00 MXN bruto/mes (Costo empresa: $26,000.00 MXN/mes).
  4. *Especialista en QA & Ciberseguridad:* $13,500.00 MXN bruto/mes (Costo empresa: $17,550.00 MXN/mes).
- **Consolidado de Nómina:** Sueldos brutos de $89,500.00 MXN/mes ($358,000.00 MXN en 4 meses, en perfecta correspondencia con [[Aspectos_Legales_Contrato_Informatico]]).
- **Carga Patronal Estimada (30%):** $26,850.00 MXN/mes ($107,400.00 MXN en 4 meses).
- **Costo Total Nómina Empresa:** **$465,400.00 MXN**.

### 2.2 Gastos Fijos de Operación (9.52% del CTP)
- Renta oficina / coworking colaborativo ($6,000/mes), electricidad ($1,200/mes), fibra simétrica 500 Mbps con IP fija ($1,500/mes), despacho contable y timbrado fiscal ($2,500/mes), herramientas compartidas SaaS ($1,800/mes) y mantenimiento ($2,000/mes).
- **Total Gastos Fijos (4 meses):** **$60,000.00 MXN**.

### 2.3 Costos Directos del Proyecto (4.25% del CTP)
- Infraestructura serverless en Google Cloud Platform (Cloud Run, Cloud SQL PostgreSQL, Redis Memorystore): $7,200.00 MXN.
- Broker RabbitMQ administrado en CloudAMQP para Patrón Saga y Dead Letter Queue (DLQ): $2,200.00 MXN.
- Licencias colaborativas GitHub Team y monitoreo Sentry: $2,400.00 MXN.
- Dominio web oficial .com.mx y certificado SSL Wildcard TLS 1.3: $950.00 MXN.
- Pruebas multi-resolución en dispositivos móviles de laboratorio: $3,000.00 MXN.
- Auditoría externa de pentesting ético sobre pasarela y JWT: $4,500.00 MXN.
- Viáticos a cafetería en La Piedad para validación en barra: $3,000.00 MXN.
- Materiales de prueba (papel térmico 80mm ecológico libre de BPA): $850.00 MXN.
- Escaneos automatizados de código estático SAST / OWASP: $1,200.00 MXN.
- Manuales operativos de barra y señalética Monchis Rewards: $1,500.00 MXN.
- **Total Costos Directos:** **$26,800.00 MXN**.

### 2.4 Inversión Inicial y Depreciación Devengada (3.11% del CTP)
- 4 Laptops de alto desempeño ($88,000 MXN, vida útil 36 meses) → Imputación en 4 meses: $9,777.78 MXN.
- Mobiliario ergonómico ($18,000 MXN, vida útil 60 meses) → Imputación: $1,200.00 MXN.
- Equipo de red Gigabit y Wi-Fi 6 ($8,500 MXN, vida útil 36 meses) → Imputación: $944.44 MXN.
- Licencias IDEs y herramientas de modelado ($12,800 MXN, vida útil 24 meses) → Imputación: $2,133.33 MXN.
- Capacitación técnica en RabbitMQ y Playwright ($12,000 MXN, vida útil 12 meses) → Imputación: $4,000.00 MXN.
- Kit POS de pruebas de mostrador ($9,500 MXN, vida útil 24 meses) → Imputación: $1,583.33 MXN.
- **Inversión Bruta Adquirida:** $148,800.00 MXN | **Depreciación Asignada al Proyecto:** **$19,638.89 MXN**.

### 2.5 Costo de Financiamiento Puente (0.21% del CTP)
- Línea de crédito de capital de trabajo por $40,000.00 MXN al 18% anual a 24 meses. Interés en 4 meses: **$1,321.19 MXN**.

---

## 3. Estrategia Comercial de Venta y Retorno de Inversión

### 3.1 Modelo de Fijación de Precios (Margin Pricing)
Se evita la erosión del margen aplicando la fórmula financiera sobre ventas facturadas sin impuestos:
$$Precio = \frac{\$630,476.09}{1 - 0.30} = \mathbf{\$900,680.12 \text{ MXN}}$$
Aportando una utilidad neta de **$270,204.04 MXN (30.0%)**.

### 3.2 Modelo de Negocio Híbrido
1. **Contrato Llave en Mano ($900,680.12 MXN + IVA):** Entrega definitiva del sistema con despliegue en GCP, manuales y capacitación.
2. **Póliza de Soporte, Mantenimiento Evolutivo y SLA ($18,500.00 MXN + IVA/mes):** Disponibilidad 99.5%, soporte crítico < 2 horas y parches de seguridad (ARR de $222,000.00 MXN con 55% de margen).

### 3.3 Payback Period para Monchis Café
- Beneficio operativo mensual: **$79,000.00 MXN/mes** ($14.5k ahorro mermas café orgánico + $38.5k incremento ventas Monchis Rewards + $9.2k conciliación de caja + $16.8k nuevos clientes por SEO).
- **Período de Recuperación:** $900,680.12 / $79,000.00 = **11.4 meses**.

---

- Plantilla Oficial en Excel (Archivo Separado del Proyecto): `Actividad_4_Gestion_Finanzas_MonchisCafe.xlsx` (disponible también como `ERNESTO HATUEY FIERRO MELENDEZ - ACTIVIDAD 4 GESTION DE FINANZAS.xlsx`)
- Entregable Académico PDF: `docs/entregables/Actividad_4_Gestion_Finanzas_MonchisCafe.pdf`
- Documento Word Editable: `docs/entregables/Actividad_4_Gestion_Finanzas_MonchisCafe.docx`
- Reporte Maestro Markdown: `docs/entregables/Actividad_4_Gestion_Finanzas_MonchisCafe.md`
- Notas Relacionadas: [[Aspectos_Legales_Contrato_Informatico]], [[Estrategia_Servicios_TI]], [[Planificacion_Sostenibilidad_ODS]].
