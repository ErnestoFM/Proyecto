# -*- coding: utf-8 -*-
"""
Generador del Entregable Académico Oficial:
Actividad 4. Gestión de Finanzas
Cátedra: Proyecto Integrador de Desarrollo de Software / Gestión de Finanzas
Docente: Dr. Gabriel Navarro Salcedo
Estudiante: Ernesto Hatuey Fierro Meléndez (Código: 215487963)
Centro Universitario de Tonalá (CUTonalá) - Universidad de Guadalajara
"""

import os
import subprocess
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_deliverables():
    base_dir = r"d:\ernestofm\Proyecto\docs\entregables"
    downloads_dir = r"C:\Users\erfierro\Downloads"
    os.makedirs(base_dir, exist_ok=True)
    
    md_path = os.path.join(base_dir, "Actividad_4_Gestion_Finanzas_MonchisCafe.md")
    docx_path = os.path.join(base_dir, "Actividad_4_Gestion_Finanzas_MonchisCafe.docx")
    html_path = os.path.join(base_dir, "Actividad_4_Gestion_Finanzas_MonchisCafe.html")
    pdf_path = os.path.join(base_dir, "Actividad_4_Gestion_Finanzas_MonchisCafe.pdf")
    
    docx_downloads = os.path.join(downloads_dir, "Actividad_4_Gestion_Finanzas_MonchisCafe.docx")
    pdf_downloads = os.path.join(downloads_dir, "Actividad_4_Gestion_Finanzas_MonchisCafe.pdf")

    # -------------------------------------------------------------
    # 1. CONTENIDO MARKDOWN
    # -------------------------------------------------------------
    md_content = """# ACTIVIDAD 4: GESTIÓN DE FINANZAS
## Proyecto Integrador: Monchis Café — Plataforma Web y POS Seguro para Cafetería Orgánica (Alineada a ODS)

**Cátedra:** Proyecto Integrador de Desarrollo de Software / Gestión de Finanzas  
**Docente:** Dr. Gabriel Navarro Salcedo  
**Estudiante:** Ernesto Hatuey Fierro Meléndez (Código: 215487963)  
**Empresa Desarrolladora:** Soluciones Digitales Fierro & Asociados S.A.S. de C.V.  
**Cliente:** Monchis Café S. de R.L. de C.V. (Representante: Carlos Alberto Montemayor Silva)  
**Fecha de Entrega:** 24 de Octubre de 2026  
**Ponderación:** 4% de la Evaluación Total  

---

## RESUMEN EJECUTIVO Y FICHA TÉCNICA FINANCIERA

| Indicador Financiero Clave | Valor Proyectado (MXN) | Base de Cálculo / Referencia Celda | % s/ Venta | Interpretación y Relevancia Operativa |
|:---|:---:|:---:|:---:|:---|
| **Costo Base Total (CTB)** | **$573,160.08** | Nómina + Gastos Fijos + Nube + Inversión + Préstamo (`'RESUMEN Y COTIZACION'!B11`) | 63.6% | Inversión acumulada de mano de obra y operación de soporte en 4 meses. |
| **Fondo de Contingencia (10%)** | **$57,316.01** | 10% s/ Costo Base Total (`'RESUMEN Y COTIZACION'!B12`) | 6.4% | Reserva para amortiguar variaciones en servicios cloud y ajustes técnicos. |
| **COSTO TOTAL DEL PROYECTO (CTP)** | **$630,476.09** | CTB + Contingencia (`'RESUMEN Y COTIZACION'!B13`) | 70.0% | Inversión neta requerida por la empresa para producir y entregar la solución. |
| **Margen de Utilidad sobre Ventas** | **30.0%** | Parámetro comercial estratégico (`'RESUMEN Y COTIZACION'!B16`) | N/A | Margen comercial sobre el precio de venta sin IVA (no recargo simple o markup). |
| **PRECIO DE VENTA SIN IVA (COTIZACIÓN)** | **$900,680.12** | CTP / (1 - Margen) = $630,476.09 / 0.70 (`'RESUMEN Y COTIZACION'!B17`) | **100.0%** | Precio facturado antes de impuestos. Base contractual de la solución llave en mano. |
| **IVA Trasladado (16%)** | **$144,108.82** | 16% s/ Precio de Venta (`'RESUMEN Y COTIZACION'!B18`) | 16.0% | Impuesto fiscal acreditable para el cliente contra sus débitos tributarios de IVA. |
| **PRECIO TOTAL FACTURADO CON IVA** | **$1,044,788.94** | Precio sin IVA + IVA (`'RESUMEN Y COTIZACION'!B19`) | 116.0% | Monto total formalizado suscrito en la propuesta económica del contrato. |
| **UTILIDAD ANTES DE ISR (PROYECTADA)** | **$270,204.04** | Precio sin IVA - Costo Total (`'RESUMEN Y COTIZACION'!B24`) | **30.0%** | Ganancia comercial de la empresa previa a impuestos anuales e I+D. |
| **ISR Corporativo Estimado (30%)** | **$81,061.21** | 30% s/ Utilidad antes de ISR (LISR art. 9) | 9.0% | Provisión estimada del impuesto sobre la renta empresarial correspondiente. |
| **UTILIDAD ESTIMADA DESPUÉS DE ISR** | **$189,142.83** | Utilidad antes de ISR - ISR Corporativo | **21.0%** | Beneficio neto proyectado disponible para solvencia y reinversión de la empresa. |
| **Punto de Equilibrio (Soluciones)** | **1 Solución** | Costos Fijos / Margen de Contribución (`'RESUMEN Y COTIZACION'!B26`) | N/A | Un único contrato llave en mano absorbe la estructura completa de costos del proyecto. |
| **Punto de Equilibrio en Pesos** | **$602,641.80** | Costos Fijos / Razón de Margen de Contribución | 66.9% | Facturación mínima sin IVA necesaria para cubrir los costos fijos y variables. |
| **Margen de Seguridad Comercial** | **33.1%** | (Precio sin IVA - Punto de Equilibrio) / Precio | N/A | Margen de tolerancia de facturación antes de que el contrato incurra en pérdidas. |

---

## 1. INTRODUCCIÓN Y CONTEXTO DEL PROYECTO

La dirección de proyectos de software en la práctica profesional no concluye con la arquitectura técnica ni con la ejecución de suites de pruebas automatizadas; requiere una planeación financiera rigurosa que asegure la solvencia de la empresa desarrolladora y un retorno de inversión justificado para el cliente.

El presente estudio modela la estructura presupuestal de la plataforma web y sistema de punto de venta (POS) para **"Monchis Café"**, una empresa familiar dedicada a la venta de café orgánico de alta calidad y productos comerciales complementarios en La Piedad, Michoacán y la Zona Metropolitana de Guadalajara.

### 1.1 Alcance Temporal y Equipo Técnico
El desarrollo comprende **16 semanas de trabajo** (4 meses calendario), distribuidas en **8 Sprints quincenales** bajo marco SCRUM con enfoque TDD (Vitest, Playwright E2E y análisis SAST). La ejecución abarca del **31 de Agosto al 20 de Diciembre de 2026**.

El equipo técnico está conformado por cuatro perfiles de ingeniería:
1. **Líder de Proyecto / Scrum Master & DevOps (Ernesto Fierro Moreno):** Gestión de sprints, pipeline CI/CD y despliegue cloud.
2. **Desarrolladora Frontend Core (Vue 3 / UI) (Jazmín Díaz):** Interfaz web reactiva, componentes de diseño pastel y catálogo ODS 12.
3. **Desarrollador Backend Core (Node.js / APIs) (Héctor Hernández):** Lógica de negocio, orquestación RabbitMQ Saga y Prisma ORM.
4. **Especialista en QA, Automatización & Ciberseguridad (Oswaldo Millán):** Pruebas funcionales, suites E2E, seguridad JWT y reCAPTCHA.

> **Nota de Riesgo Operativo:** El proyecto no dispone de perfiles dedicados y exclusivos de DevOps, DBA ni diseñador UX; dichas responsabilidades son asumidas por los cuatro ingenieros de desarrollo. Por tanto, el fondo de contingencia del 10% ($57,316.01 MXN) constituye el único margen disponible para absorber desviaciones técnicas o retrabajos en infraestructura.

---

## 2. LLENADO Y ANÁLISIS DE LA PLANTILLA FINANCIERA (50%)

La modelación financiera se integró a partir de parámetros económicos estandarizados y disposiciones fiscales mexicanas vigentes para el ejercicio 2026:

### 2.1 Hoja PARAMETROS
- **Horizonte de Ejecución:** 4 meses (16 semanas / 8 sprints quincenales).
- **Proyectos a Entregar:** 1 desarrollo a medida (llave en mano).
- **Margen Deseado sobre Ventas:** 30.0% ($Precio = Costo / (1 - 0.30)$).
- **IVA de Facturación:** 16.0% (impuesto trasladado acreditable).
- **Contingencia sobre Costo:** 10.0% sobre el costo base total.
- **Carga Patronal Estimada:** 30.0% sobre el sueldo bruto mensual. Corresponde a una aproximación técnica que integra las cuotas de seguridad social del IMSS, la aportación patronal del 5.0% al INFONAVIT y el Impuesto Sobre Nóminas (ISN) local del 3.0% (tasa vigente tanto en Michoacán como en Jalisco).
- **Jornada Laboral Productiva:** 160 horas al mes por persona (40 horas semanales efectivas).
- **Parámetros Fiscales 2026:** UMA diaria de $117.31 MXN y tope mensual de subsidio al empleo de $11,492.66 MXN (publicados en el DOF).
- **Condiciones de Crédito:** Tasa anual del 18.0% a 24 meses de plazo, con imputación proporcional al proyecto.

> **Nota de Sensibilidad Fiscal:** Por cada 5.0 puntos porcentuales adicionales de carga patronal sobre la nómina ($17,900.00 MXN en sueldos brutos + $1,790.00 MXN de contingencia = $19,690.00 MXN en CTP), el precio de venta sin IVA aumentaría en **$28,128.57 MXN (≈ $28,100 MXN)** para mantener el margen comercial del 30.0%.

### 2.2 Hoja NOMINA y Costo de Mano de Obra
Compuesta por 4 profesionales dedicados durante las 16 semanas (2,560 horas de ingeniería):
1. **Líder de Proyecto / Scrum Master & DevOps:** Sueldo mensual bruto de **$36,000.00 MXN**. Retención ISR mensual: $6,121.08 MXN. Carga patronal estimada (30%): $10,800.00 MXN. Costo mensual empresa: **$46,800.00 MXN** ($292.50 MXN/hora).
2. **Desarrolladora Frontend Core (Vue 3 / UI):** Sueldo mensual bruto de **$20,000.00 MXN**. Retención ISR mensual: $2,604.00 MXN. Carga patronal estimada (30%): $6,000.00 MXN. Costo mensual empresa: **$26,000.00 MXN** ($162.50 MXN/hora).
3. **Desarrollador Backend Core (Node.js / APIs):** Sueldo mensual bruto de **$20,000.00 MXN**. Retención ISR mensual: $2,604.00 MXN. Carga patronal estimada (30%): $6,000.00 MXN. Costo mensual empresa: **$26,000.00 MXN** ($162.50 MXN/hora).
4. **Especialista en QA, Automatización & Ciberseguridad:** Sueldo mensual bruto de **$13,500.00 MXN**. Retención ISR mensual: $1,283.98 MXN. Carga patronal estimada (30%): $4,050.00 MXN. Costo mensual empresa: **$17,550.00 MXN** ($109.69 MXN/hora).

**Consolidado de Nómina:**
- Sueldo bruto mensual total: **$89,500.00 MXN** ($358,000.00 MXN en 4 meses, en correspondencia con el Contrato Informático de la Actividad 3.1).
- Carga patronal estimada mensual (30%): **$26,850.00 MXN** ($107,400.00 MXN en 4 meses).
- **Costo total de nómina para la empresa (4 meses):** **$465,400.00 MXN**.

### 2.3 Hoja GASTOS FIJOS (7 rubros desglosados)
Costos indirectos de operación de la oficina técnica ($15,000.00 MXN/mes):
1. Renta de espacio colaborativo / coworking y sala de juntas: $6,000.00 MXN/mes ($24,000.00 en 4 meses).
2. Electricidad y climatización de estaciones de cómputo: $1,200.00 MXN/mes ($4,800.00 en 4 meses).
3. Enlace simétrico de fibra óptica 500 Mbps con IP fija: $1,500.00 MXN/mes ($6,000.00 en 4 meses).
4. Despacho contable externo y timbrado fiscal ante el SAT: $2,500.00 MXN/mes ($10,000.00 en 4 meses).
5. Herramientas SaaS de colaboración (Google Workspace, Slack Pro, Notion, Figma): $1,800.00 MXN/mes ($7,200.00 en 4 meses).
6. Gestión comercial, demostraciones en sitio y prospección: $1,000.00 MXN/mes ($4,000.00 en 4 meses).
7. Mantenimiento preventivo, artículos de limpieza y papelería: $1,000.00 MXN/mes ($4,000.00 en 4 meses).
- **Total Gastos Fijos (4 meses):** **$60,000.00 MXN**.

### 2.4 Hoja COSTOS DIRECTOS (10 rubros reales)
Servicios en la nube e insumos dedicados exclusivamente a la solución Monchis Café:
1. Google Cloud Platform (Cloud Run, PostgreSQL, Redis): 4 meses x $1,800.00 = **$7,200.00 MXN**.
2. Licencias de repositorios y minutos CI/CD en GitHub Team y Sentry: 4 meses x $600.00 = **$2,400.00 MXN**.
3. Broker de mensajería CloudAMQP RabbitMQ dedicado (Saga y DLQ): 4 meses x $550.00 = **$2,200.00 MXN**.
4. Registro de dominio .com.mx y certificado TLS/SSL Wildcard: 1 anualidad = **$950.00 MXN**.
5. Dispositivos móviles de laboratorio para pruebas táctiles y QR: 2 unidades x $1,500.00 = **$3,000.00 MXN**.
6. Subcontratación de pentesting ético y auditoría de pasarela: 1 servicio = **$4,500.00 MXN**.
7. Viáticos de visitas de campo a la cafetería en La Piedad (pruebas en barra): 6 visitas x $500.00 = **$3,000.00 MXN**.
8. Materiales y consumibles (papel térmico 80mm sin BPA, cables): 1 lote = **$850.00 MXN**.
9. Auditoría de código estático (SAST) y análisis OWASP Top 10: 1 servicio = **$1,200.00 MXN**.
10. Otros / Manuales de mostrador y señalética Monchis Rewards: 1 paquete = **$1,500.00 MXN**.
- **Total Costos Directos:** **$26,800.00 MXN**.

### 2.5 Hoja INVERSION INICIAL y Depreciación
Conforme al principio contable de devengo, se imputa al proyecto únicamente el desgaste proporcional de los activos durante los 4 meses de uso:
- 4 Laptops de alto rendimiento ($22,000 c/u = $88,000 MXN, vida útil 36 meses): **$9,777.78 MXN**.
- Mobiliario ergonómico ($4,500 c/u = $18,000 MXN, vida útil 60 meses): **$1,200.00 MXN**.
- Equipo de red de laboratorio ($8,500 MXN, vida útil 36 meses): **$944.44 MXN**.
- Licencias IDEs y herramientas ($3,200 c/u = $12,800 MXN, vida útil 24 meses): **$2,133.33 MXN**.
- Capacitación técnica en RabbitMQ y Playwright ($12,000 MXN, vida útil 12 meses): **$4,000.00 MXN**.
- Kit POS de mostrador de pruebas ($9,500 MXN, vida útil 24 meses): **$1,583.33 MXN**.
- **Inversión total adquirida:** $148,800.00 MXN | **Depreciación imputada en 4 meses:** **$19,638.89 MXN**.

### 2.6 Hoja PRESTAMO (Costo Financiero y Liquidez)
Se consideró una línea de crédito de capital de trabajo por **$40,000.00 MXN** al 18.0% anual a 24 meses (cuota mensual de $1,996.96 MXN). El interés total del crédito asciende a $7,927.14 MXN. La plantilla imputa el **interés promedio lineal prorrateado a 4 meses ($1,321.19 MXN)**, aun cuando el interés real devengado bajo tabla de amortización francesa en los primeros 4 meses ronda los $2,273 MXN.

> **Justificación Operativa:** La contratación del financiamiento se fundamenta en la necesidad de adquirir de forma anticipada los activos de laboratorio ($148.8k) y depósitos de nube sin esperar los tiempos administrativos y bancarios de dispersión del anticipo por parte del cliente, absorbiendo desfases en la conciliación inicial.

---

## 3. CUADRO JUSTIFICATIVO FINANCIERO (PERTINENCIA 50%)

El siguiente cuadro detalla la pertinencia técnica, operativa y económica de cada partida presupuestal:

| Rubro Presupuestal | Importe (MXN) | % s/ CTP | Clasificación Contable | Criterio Técnico y Justificación Operativa | Impacto en Calidad y Mitigación de Riesgos |
|:---|:---:|:---:|:---:|:---|:---|
| **Nómina y Carga Patronal** | $465,400.00 | 73.81% | Mano de Obra Directa | 4 perfiles técnicos (Scrum Master/DevOps, Frontend, Backend, QA) por 16 semanas (2,560 hrs). Sueldos brutos de $89.5k/mes más estimación del 30% de carga patronal (IMSS, Infonavit 5%, ISN 3%). | Permite el avance de los 8 sprints bajo metodología TDD con cobertura >80% y reduce el riesgo de rotación técnica mediante compensaciones de mercado. |
| **Gastos Fijos Operativos** | $60,000.00 | 9.52% | Costo Indirecto Fijo | Espacio coworking ($6k/mes), energía ($1.2k), fibra simétrica con IP fija ($1.5k), despacho contable ($2.5k), herramientas SaaS ($1.8k), gestión comercial ($1k) y suministros ($1k) ($15,000/mes). | Asegura un entorno estable para integración continua, soporte fiscal para timbrado CFDI 4.0 y herramientas colaborativas de desarrollo. |
| **Costos Directos del Proyecto** | $26,800.00 | 4.25% | Costo Directo Variable | GCP Cloud Run/SQL/Redis ($7.2k), GitHub/Sentry ($2.4k), CloudAMQP RabbitMQ ($2.2k), dominio/SSL ($950), dispositivos de prueba ($3k), pentesting ($4.5k), viáticos ($3k), papel/cables ($850), SAST ($1.2k) y otros ($1.5k). | Sustenta la arquitectura orientada a eventos con RabbitMQ y Patrón Saga, asegura el cumplimiento de seguridad en pagos y valida los periféricos de mostrador. |
| **Inversión Inicial Asignada** | $19,638.89 | 3.11% | Depreciación de Activos | Desgaste proporcional en 4 meses de laptops (36 meses), mobiliario (60 meses), red gigabit (36 meses), licencias IDEs y kit POS ($19,638.89 de $148.8k adquiridos). | Aplica el principio contable de devengo: el contrato absorbe únicamente el desgaste real de los bienes productivos durante el tiempo de ejecución. |
| **Intereses de Financiamiento** | $1,321.19 | 0.21% | Costo Financiero | Crédito de $40,000.00 MXN al 18% anual a 24 meses. Interés promedio prorrateado a 4 meses ($1,321.19 MXN) para anticipar la compra de activos y absorber desfases del anticipo. | Evita demoras en el arranque de actividades técnicas ante posibles retrasos bancarios o administrativos en la primera transferencia del cliente. |
| **Fondo de Contingencia (10%)** | $57,316.01 | 9.09% | Reserva de Riesgos | Reserva del 10% sobre el costo base ($573,160.08 MXN) para absorber fluctuaciones cambiarias en servicios cloud en dólares y retrabajos técnicos menores. | Absorbe desviaciones imprevistas y constituye el único colchón financiero ante la ausencia de roles dedicados de DevOps, DBA o UX en el equipo. |
| **TOTAL COSTO DEL PROYECTO (CTP)** | **$630,476.09** | **100.00%** | **Costo Integral** | **Inversión total consolidada necesaria para diseñar, desarrollar, probar y liberar en producción el software Monchis Café.** | **Base matemática que sustenta una cotización estructurada y viable frente al cliente.** |

---

## 4. ESTRATEGIA COMERCIAL DE VENTA SEGÚN COSTO Y UTILIDAD (35%)

La fijación de precio y la comercialización se estructuran a partir del costo de ingeniería y el rendimiento financiero requerido para la empresa desarrolladora:

### 4.1 Modelo de Fijación de Precios: Margen Comercial vs Recargo (Markup)
El precio de venta se determinó aplicando margen comercial sobre ventas antes de impuestos:

$$\\text{Precio de Venta (sin IVA)} = \\frac{\\text{Costo Total del Proyecto}}{1 - \\text{Margen Deseado}} = \\frac{\\$630,476.09}{1 - 0.30} = \\frac{\\$630,476.09}{0.70} = \\mathbf{\\$900,680.12 \\text{ MXN}}$$

$$\\text{Utilidad antes de ISR} = \\text{Precio de Venta} - \\text{Costo Total} = \\$900,680.12 - \\$630,476.09 = \\mathbf{\\$270,204.04 \\text{ MXN}} \\quad (30.0\\%)$$

$$\\text{Facturación Total con 16\\% de IVA} = \\$900,680.12 \\times 1.16 = \\mathbf{\\$1,044,788.94 \\text{ MXN}}$$

- **Utilidad Estimada Después de ISR (30%):** De conformidad con la tasa corporativa ordinaria del impuesto sobre la renta (artículo 9 de la LISR), el ISR estimado asciende a **$81,061.21 MXN**, resultando una utilidad neta después de impuestos de **$189,142.83 MXN**, representativa del **21.0%** de las ventas facturadas sin IVA. En caso de existir base gravable sujeta a la Participación de los Trabajadores en las Utilidades (PTU), aplicaría la tasa constitucional del 10%.
- **Naturaleza del IVA:** Los $144,108.82 MXN corresponden a un impuesto trasladado que no constituye utilidad para el desarrollador y es acreditable para Monchis Café contra sus débitos de IVA.

### 4.2 Modelo de Negocio Híbrido: Venta Inicial + Ingresos Recurrentes
1. **Contrato de Implementación Llave en Mano ($900,680.12 MXN + IVA):** Comprende arquitectura monorepo, desarrollo frontend en Vue 3 con prerenderizado SEO (`vite-ssg`), backend en Node.js, broker RabbitMQ con Patrón Saga, módulo POS, trazabilidad de café orgánico (ODS 12), pruebas de seguridad, despliegue en GCP mediante Terraform y capacitación presencial a baristas y cajeros.
2. **Póliza de Soporte, Mantenimiento Evolutivo y SLA ($18,500.00 MXN + IVA/mes a partir del Mes 5):**
   - Disponibilidad del 99.5% de la plataforma con monitoreo de microservicios y Dead Letter Queue (DLQ).
   - Tiempo de respuesta a incidentes críticos menor a 2 horas durante el horario operativo del establecimiento.
   - Actualización de dependencias, parches de seguridad y ajustes SEO mensuales.
   - Margen operativo de la póliza: 55%, aportando un ingreso recurrente anual (ARR) de **$222,000.00 MXN**.
3. **Módulo de Franquicias / Nuevas Sucursales:** Licenciamiento de **$45,000.00 MXN** por sucursal adicional más **$3,500.00 MXN/mes** de soporte técnico y mantenimiento por tienda abierta.

### 4.3 Propuesta de Valor y Retorno de Inversión (Payback) para Monchis Café
Los beneficios operativos mensuales estimados para la cafetería se desglosan a continuación:

| Beneficio Operativo Cuantificable | Mecanismo del Sistema | Impacto Mensual Estimado | Beneficio Anual Proyectado |
|:---|:---|:---:|:---:|
| **Reducción de Mermas de Café Orgánico (-22%)** | Control de rotación PEPS, alertas de caducidad y trazabilidad de lotes regionales. | $14,500.00 MXN | $174,000.00 MXN |
| **Incremento en Ventas y Ticket Promedio (+24%)** | Sellos digitales Monchis Rewards y bono termo (-$5.00 MXN reutilizable ODS 12). | $38,500.00 MXN | $462,000.00 MXN |
| **Eliminación de Discrepancias en Caja (-98%)** | Registro ágil de ventas en barra, cálculo de cambio y conciliación de pagos mixtos. | $9,200.00 MXN | $110,400.00 MXN |
| **Captura de Nuevos Clientes por SEO Local** | Prerenderizado `vite-ssg`, Schema.org LocalBusiness y atribución de campañas UTM. | $16,800.00 MXN | $201,600.00 MXN |
| **TOTAL BENEFICIO OPERATIVO BRUTO ESTIMADO** | **Ahorros directos e ingresos adicionales proyectados** | **$79,000.00 MXN** | **$948,000.00 MXN** |

> **Aclaración de Supuestos:** Las cifras de impacto corresponden a supuestos preliminares derivados de parámetros estándar del sector restaurantero y deben validarse con datos históricos de venta, merma y afluencia de la cafetería.

#### Evaluación del Período de Recuperación (Payback Period):
1. **Escenario Bruto (11.4 meses):** Calculado como $\\$900,680.12 / \\$79,000.00 = \\mathbf{11.4 \\text{ meses}}$. Este plazo no considera el pago de la póliza de soporte ni el costo directo de ventas.
2. **Escenario Neto con Póliza SLA (14.9 meses):** A partir del mes 5, se descuenta el costo mensual de la póliza SLA ($18,500.00 MXN). El flujo mensual neto se reduce a $60,500.00 MXN ($79,000.00 - $18,500.00), resultando un plazo de $\\$900,680.12 / \\$60,500.00 = \\mathbf{14.9 \\text{ meses}}$.
3. **Escenario Prudente (15.8 meses sin póliza y 23.5 meses con póliza):**
   - Los ingresos adicionales ($38,500.00 de ticket + $16,800.00 de clientes = $55,300.00 MXN) requieren costo de insumos (grano de café, leche, jarabes). Suponiendo un **60% de margen de contribución**, aportan $33,180.00 MXN netos.
   - Los ahorros directos (mermas $14,500.00 + caja $9,200.00 = $23,700.00 MXN) ingresan al 100%.
   - Beneficio operativo neto mensual prudente: **$56,880.00 MXN**.
   - *Payback prudente sin póliza:* $\\$900,680.12 / \\$56,880.00 = \\mathbf{15.8 \\text{ meses}}$.
   - *Payback prudente con póliza SLA:* $\\$900,680.12 / (\\$56,880.00 - \\$18,500.00) = \\$900,680.12 / \\$38,380.00 = \\mathbf{23.5 \\text{ meses}}$.

### 4.4 Esquema de Cierre y Pagos por Hitos Ágiles
El esquema de cobro se divide en **6 hitos de pago** respaldados mediante entregables verificables en ambiente Staging:
1. **Hito 0 (Firma y Arranque - 20%):** $180,136.02 MXN sin IVA. Firma de contrato, configuración del monorepo, Docker Compose, esquema Prisma ORM y compra de licencias iniciales.
2. **Hito 1 (Sprint 2 - Backend & Seguridad - 15%):** $135,102.02 MXN sin IVA. Backend Core, autenticación JWT stateless, RBAC y validación anti-bot con reCAPTCHA en Staging.
3. **Hito 2 (Sprint 4 - Eventos & Frontend - 15%):** $135,102.02 MXN sin IVA. Broker RabbitMQ CloudAMQP, Patrón Saga y vistas frontend Vue 3 con prerenderizado `vite-ssg`.
4. **Hito 3 (Sprint 6 - POS & Trazabilidad - 15%):** $135,102.02 MXN sin IVA. Punto de Venta táctil operativo, cobro mixto (efectivo/tarjeta/SPEI), escaneo QR y catálogo ODS 12.
5. **Hito 4 (Sprint 8 - Analítica & Testing - 15%):** $135,102.02 MXN sin IVA. Dashboard de ventas con atribución UTM, suites Vitest/Playwright (>80% cobertura) y reporte SAST/OWASP.
6. **Hito 5 (Cierre y Despliegue en GCP - 20%):** $180,136.02 MXN sin IVA. Infraestructura en GCP mediante Terraform, manuales técnicos de usuario y administración, capacitación al personal y Acta de Recepción Definitiva.

### 4.5 Análisis de Sensibilidad y Escenarios de Rentabilidad

| Escenario Comercial | Margen s/ Venta | Precio sin IVA (MXN) | Precio con IVA (16%) | Utilidad antes ISR | Criterio y Táctica de Negociación |
|:---|:---:|:---:|:---:|:---:|:---|
| **Escenario Conservador (Piso Mínimo)** | 20.0% | $788,095.11 | $914,190.33 | $157,619.02 | Representa el piso de negociación comercial que sacrifica margen (del 30% al 20%), no reducción de costos de desarrollo. Asegura el contrato ante restricciones presupuestales del cliente. |
| **Escenario Esperado / Base (Recomendado)** | **30.0%** | **$900,680.12** | **$1,044,788.94** | **$270,204.04** | **Propuesta recomendada.** Preserva el margen del 30.0% necesario para la solvencia de la empresa y amortización equilibrada para el cliente. |
| **Escenario Premium / Valor Agregado** | 35.0% | $969,963.21 | $1,125,157.32 | $339,487.12 | Paquete de valor que integra 6 meses de póliza SLA con 99.5% de disponibilidad (costo asumido de $49,950 MXN) y analítica avanzada. Utilidad ajustada post-SLA: **$289,537.12 MXN** (margen efectivo del 29.9%). |

### 4.6 Punto de Equilibrio y Margen de Seguridad
- **Punto de Equilibrio en Unidades:** 1 Solución a medida.
- **Punto de Equilibrio en Pesos:** **$602,641.80 MXN**. Determina el volumen de facturación sin IVA requerido para absorber los costos fijos ($546,360.08 MXN) considerando la razón de margen de contribución neta (90.66%).
- **Margen de Seguridad Comercial:** **33.1%**. Indica que la cotización base posee una holgura del 33.1% frente al punto de equilibrio en pesos antes de comprometer la cobertura de costos.

---

## 5. CONCLUSIONES Y LÍMITES DEL MODELO

La elaboración de este estudio financiero permitió fundamentar la viabilidad del proyecto integrador Monchis Café a partir de costos reales de ingeniería de software. No obstante, deben reconocerse los supuestos y limitaciones del modelo:

1. **Aproximación de Carga Social:** La tasa global del 30% es una estimación técnica; la prima real de riesgo de trabajo ante el IMSS y las cuotas de cesantía pueden presentar ligeras variaciones al momento de la inscripción patronal formal.
2. **Validación de Beneficios Operativos:** Los ahorros por mermas y los incrementos en ticket de venta son proyecciones que dependerán de la disciplina operativa del personal de barra y de la adopción del programa Monchis Rewards por parte de los clientes.
3. **Riesgos de Infraestructura y Tipo de Cambio:** Los servicios de Google Cloud Platform y CloudAMQP se cotizan en dólares estadounidenses, por lo que el fondo de contingencia del 10% ($57,316.01 MXN) cumple la función prioritaria de absorber fluctuaciones cambiarias e incrementos imprevistos en consumo de cómputo.

---

## 6. REFERENCIAS (FORMATO APA 7ma EDICIÓN)

- Diario Oficial de la Federación. (2025, 27 de diciembre). *Resolución Miscelánea Fiscal para 2026: Anexo 8 (Tarifas aplicables para el cálculo del Impuesto sobre la Renta)*. Secretaría de Hacienda y Crédito Público. https://sidof.segob.gob.mx/notas/docFuente/5777219
- Diario Oficial de la Federación. (2024, 1 de mayo). *Decreto por el que se otorga el subsidio para el empleo para los trabajadores con ingresos mensuales de hasta $11,492.66*. Presidencia de la República. https://sidof.segob.gob.mx/notas/docFuente/5777649
- Instituto Nacional de Estadística y Geografía. (2026). *Valor de la Unidad de Medida y Actualización (UMA) vigente a partir de febrero de 2026*. INEGI. https://www.inegi.org.mx/temas/uma/
- Kerzner, H. (2017). *Project management: A systems approach to planning, scheduling, and controlling* (12th ed.). John Wiley & Sons.
- McConnell, S. (2006). *Software estimation: Demystifying the black art*. Microsoft Press.
- Project Management Institute. (2021). *A guide to the project management body of knowledge (PMBOK guide)* (7th ed.). Project Management Institute.
- Schwaber, K., & Sutherland, J. (2020). *The Scrum guide: The definitive guide to Scrum: The rules of the game*. Scrum.org.
"""

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Documento Markdown guardado en: {md_path}")

    # -------------------------------------------------------------
    # 2. GENERAR DOCUMENTO WORD (.DOCX)
    # -------------------------------------------------------------
    doc = Document()
    
    for sec in doc.sections:
        sec.top_margin = Inches(1)
        sec.bottom_margin = Inches(1)
        sec.left_margin = Inches(1)
        sec.right_margin = Inches(1)
        
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(10.5)
    style_normal.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(6)

    COLOR_NAVY = RGBColor(0x17, 0x36, 0x5D)
    COLOR_BLUE = RGBColor(0x24, 0x4B, 0x7A)
    HEX_HEADER = "17365D"
    HEX_ALT = "F0F4F8"
    HEX_SUCCESS = "E2F0D9"

    def set_cell_shading(cell, color_hex):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Arial'
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = COLOR_NAVY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Arial'
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = COLOR_BLUE
        return p

    # Portada institucional
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(4)
    r = p_title.add_run("ACTIVIDAD 4: GESTIÓN DE FINANZAS")
    r.font.size = Pt(16)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    r2 = p_sub.add_run("Proyecto Integrador: Monchis Café — Plataforma Web y POS Seguro para Cafetería Orgánica")
    r2.font.size = Pt(11)
    r2.font.italic = True
    r2.font.color.rgb = COLOR_BLUE

    tbl_meta = doc.add_table(rows=4, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_rows = [
        ("Cátedra / Materia:", "Gestión de Finanzas / Proyecto Integrador de Software"),
        ("Docente Evaluador:", "Dr. Gabriel Navarro Salcedo"),
        ("Estudiante:", "Ernesto Hatuey Fierro Meléndez (Código: 215487963)"),
        ("Fecha de Entrega:", "24 de Octubre de 2026 | Ponderación: 4% del 100%")
    ]
    for idx, (l, v) in enumerate(meta_rows):
        r_cells = tbl_meta.rows[idx].cells
        r_cells[0].width = Inches(2.2)
        r_cells[1].width = Inches(4.3)
        set_cell_shading(r_cells[0], "D9E2EC")
        set_cell_margins(r_cells[0], top=60, bottom=60, left=100, right=100)
        set_cell_margins(r_cells[1], top=60, bottom=60, left=100, right=100)
        p0 = r_cells[0].paragraphs[0]
        p0.add_run(l).bold = True
        p0.runs[0].font.size = Pt(9.0)
        p1 = r_cells[1].paragraphs[0]
        p1.add_run(v)
        p1.runs[0].font.size = Pt(9.0)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 1. Resumen Ejecutivo
    add_h1("1. Resumen Ejecutivo de Indicadores Financieros")
    doc.add_paragraph(
        "A continuación se presenta el consolidado de las variables económicas del proyecto, "
        "modeladas dinámicamente en la plantilla oficial y vinculadas a la hoja ESTRATEGIA DE VENTA:"
    )

    kpi_doc_data = [
        ("Costo Base Total (CTB)", "$573,160.08 MXN", "63.6%", "Costos empresariales directos, indirectos, nómina y financiamiento."),
        ("Fondo de Contingencia (10%)", "$57,316.01 MXN", "6.4%", "Reserva de mitigación ante riesgos técnicos y variaciones cloud."),
        ("COSTO TOTAL DEL PROYECTO (CTP)", "$630,476.09 MXN", "70.0%", "Inversión neta requerida por la empresa para producir la solución."),
        ("Margen de Utilidad s/ Venta", "30.0%", "N/A", "Rendimiento comercial pactado sobre el precio sin impuestos."),
        ("PRECIO DE VENTA SIN IVA", "$900,680.12 MXN", "100.0%", "Cotización contractual llave en mano: CTP / (1 - Margen)."),
        ("IVA Trasladado (16%)", "$144,108.82 MXN", "16.0%", "Impuesto fiscal trasladado acreditable para el cliente contra sus débitos de IVA."),
        ("PRECIO TOTAL FACTURADO CON IVA", "$1,044,788.94 MXN", "116.0%", "Monto total formalizado convenido en la propuesta económica."),
        ("UTILIDAD ANTES DE ISR", "$270,204.04 MXN", "30.0%", "Ganancia empresarial antes de ISR corporativo anual para solvencia e I+D."),
        ("ISR Corporativo Estimado (30%)", "$81,061.21 MXN", "9.0%", "Provisión estimada del impuesto sobre la renta empresarial (LISR art. 9)."),
        ("UTILIDAD ESTIMADA DESPUÉS DE ISR", "$189,142.83 MXN", "21.0%", "Beneficio neto proyectado disponible tras obligaciones tributarias."),
        ("Punto de Equilibrio (Soluciones)", "1 Solución", "N/A", "Un contrato llave en mano absorbe la estructura de costos operativos."),
        ("Punto de Equilibrio en Pesos", "$602,641.80 MXN", "66.9%", "Facturación mínima sin IVA necesaria para cubrir costos fijos y variables."),
        ("Margen de Seguridad Comercial", "33.1%", "N/A", "Margen de tolerancia frente a contingencias antes de entrar en pérdidas.")
    ]

    tbl_kpi = doc.add_table(rows=len(kpi_doc_data) + 1, cols=4)
    tbl_kpi.alignment = WD_TABLE_ALIGNMENT.CENTER
    kpi_headers = ["Indicador Financiero", "Monto Proyectado", "% s/ Venta", "Interpretación Operativa"]
    for c_idx, h in enumerate(kpi_headers):
        cell = tbl_kpi.rows[0].cells[c_idx]
        set_cell_shading(cell, HEX_HEADER)
        set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8.0)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        if c_idx in [1, 2]: p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    for r_idx, row_data in enumerate(kpi_doc_data, start=1):
        is_hl = "PRECIO DE VENTA" in row_data[0] or "UTILIDAD" in row_data[0]
        bg = HEX_SUCCESS if "DESPUÉS DE ISR" in row_data[0] else (HEX_ALT if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, val in enumerate(row_data):
            cell = tbl_kpi.rows[r_idx].cells[c_idx]
            set_cell_shading(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.0)
            if is_hl: r.font.bold = True
            if c_idx in [1, 2]: p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # 2. Cuadro Justificativo
    add_h1("2. Cuadro Justificativo Financiero (Pertinencia de Costos - 50%)")
    doc.add_paragraph(
        "Desglose analítico que justifica la pertinencia técnica, operativa y económica de cada rubro presupuestal:"
    )

    just_doc_data = [
        ("Nómina y Carga Patronal", "$465,400.00", "73.81%", "4 perfiles (Scrum Master/DevOps, Frontend Vue 3, Backend Node.js, QA) por 16 semanas. Sueldos brutos de $89.5k/mes más estimación del 30% de carga patronal (IMSS, Infonavit 5%, ISN 3%).", "Garantiza 8 sprints bajo TDD (>80% cobertura) y reduce el riesgo de rotación técnica mediante compensaciones de mercado."),
        ("Gastos Fijos de Operación", "$60,000.00", "9.52%", "Coworking ($6k/mes), energía ($1.2k), fibra simétrica ($1.5k), despacho contable ($2.5k), herramientas SaaS ($1.8k), gestión comercial ($1k) y suministros ($1k) ($15k/mes).", "Asegura entorno ininterrumpido para CI/CD, soporte fiscal para timbrado CFDI 4.0 y herramientas de trabajo colaborativo."),
        ("Costos Directos (10 rubros)", "$26,800.00", "4.25%", "GCP ($7.2k), GitHub/Sentry ($2.4k), CloudAMQP RabbitMQ ($2.2k), dominio/SSL ($950), dispositivos ($3k), pentesting ($4.5k), viáticos ($3k), papel/cables ($850), SAST ($1.2k) y otros ($1.5k).", "Sustenta arquitectura orientada a eventos (Saga/DLQ), seguridad de datos de pago y validación física en barra."),
        ("Inversión Inicial Asignada", "$19,638.89", "3.11%", "Depreciación en 4 meses según vida útil fiscal: 4 laptops (36 meses), mobiliario (60 meses), red (36 meses), licencias IDEs y kit POS ($19.6k de $148.8k).", "Aplica devengo contable: el proyecto absorbe únicamente el desgaste real de los activos productivos durante su ejecución."),
        ("Intereses de Financiamiento", "$1,321.19", "0.21%", "Crédito de $40,000.00 MXN al 18% anual a 24 meses. Interés promedio prorrateado a 4 meses ($1,321.19 MXN) para anticipar compra de activos y absorber desfases del anticipo.", "Evita demoras operativas en el arranque derivadas de tiempos de dispersión bancaria de la primera transferencia."),
        ("Fondo de Contingencia (10%)", "$57,316.01", "9.09%", "Reserva estratégica del 10% s/ costo base para fluctuaciones en tarifas cloud en dólares, inflación o retrabajos técnicos menores.", "Absorbe imprevistos y constituye el único colchón financiero ante la ausencia de roles dedicados de DevOps, DBA o UX."),
        ("TOTAL COSTO DEL PROYECTO", "$630,476.09", "100.00%", "Inversión integral necesaria para diseñar, probar y liberar en producción el software Monchis Café.", "Base matemática y analítica sólida que respalda una cotización justa, viable y rentable.")
    ]

    tbl_just = doc.add_table(rows=len(just_doc_data) + 1, cols=5)
    tbl_just.alignment = WD_TABLE_ALIGNMENT.CENTER
    just_headers = ["Rubro Presupuestal", "Importe (MXN)", "% s/ CTP", "Criterio Técnico y Justificación", "Impacto en Calidad y Riesgos"]
    for c_idx, h in enumerate(just_headers):
        cell = tbl_just.rows[0].cells[c_idx]
        set_cell_shading(cell, HEX_HEADER)
        set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8.0)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        if c_idx in [1, 2]: p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    for r_idx, row_data in enumerate(just_doc_data, start=1):
        is_tot = "TOTAL COSTO" in row_data[0]
        bg = "D9E2EC" if is_tot else (HEX_ALT if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, val in enumerate(row_data):
            cell = tbl_just.rows[r_idx].cells[c_idx]
            set_cell_shading(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(7.5)
            if is_tot: r.font.bold = True
            if c_idx in [1, 2]: p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # 3. Estrategia de Venta
    add_h1("3. Estrategia Comercial de Venta según Costo y Utilidad (35%)")
    
    add_h2("3.1 Modelo de Fijación de Precios: Margen Comercial vs Recargo (Markup)")
    doc.add_paragraph(
        "La cotización del software se formuló a partir del margen comercial sobre ventas, garantizando "
        "que el 30.0% del monto facturado antes de impuestos se traduzca en utilidad para la empresa desarrolladora:\n"
        "• Precio de Venta sin IVA = CTP / (1 - Margen) = $630,476.09 / 0.70 = $900,680.12 MXN.\n"
        "• Utilidad antes de ISR Proyectada = $900,680.12 - $630,476.09 = $270,204.04 MXN (Margen real: 30.0%).\n"
        "• Facturación con IVA (16%) = $900,680.12 x 1.16 = $1,044,788.94 MXN.\n"
        "• Utilidad después de ISR (30%): $189,142.83 MXN (21.0% de las ventas). Mención de PTU (10% constitucional)."
    )

    add_h2("3.2 Modelo de Negocio Híbrido: Venta Inicial + Ingresos Recurrentes")
    doc.add_paragraph(
        "1. Venta Inicial Llave en Mano ($900,680.12 MXN + IVA): Licenciamiento y puesta en producción de la plataforma web, POS táctil y microservicios en GCP.\n"
        "2. Póliza de Soporte, Mantenimiento Evolutivo y SLA ($18,500.00 MXN + IVA/mes a partir del Mes 5): Disponibilidad del 99.5%, respuesta a incidentes críticos de caja < 2 horas en horario operativo, monitoreo de RabbitMQ DLQ y parches de seguridad (ARR de $222,000.00 MXN con 55% de margen).\n"
        "3. Licenciamiento por Franquicia / Sucursal ($45,000.00 MXN de cuota única por nueva tienda + $3,500.00 MXN/mes de soporte y mantenimiento por sucursal)."
    )

    add_h2("3.3 Propuesta de Valor y Retorno de Inversión (Payback) para Monchis Café")
    doc.add_paragraph(
        "Los beneficios mensuales estimados corresponden a estimaciones preliminares sujetas a validación con datos reales del negocio:\n"
        "• Reducción de mermas de café orgánico (-22%): Ahorro mensual de $14,500.00 MXN mediante rotación PEPS.\n"
        "• Incremento en ticket promedio (+24%): $38,500.00 MXN mensuales por fidelización Monchis Rewards.\n"
        "• Eliminación de fugas en caja (-98%): Recuperación mensual de $9,200.00 MXN por conciliación automática.\n"
        "• Clientes nuevos por SEO local y Google Maps: $16,800.00 MXN mensuales adicionales.\n"
        "• Beneficio mensual bruto total: $79,000.00 MXN/mes ($948,000.00 MXN al año).\n\n"
        "Evaluación del Período de Recuperación (Payback Period):\n"
        "1. Payback Bruto: $900,680.12 / $79,000.00 = 11.4 meses (sin descontar póliza ni costo de ventas).\n"
        "2. Payback Neto con Póliza SLA: $900,680.12 / ($79,000.00 - $18,500.00) = $900,680.12 / $60,500.00 = 14.9 meses.\n"
        "3. Payback Prudente (60% margen en ventas adicionales, beneficio neto de $56,880.00/mes): Plazo sin póliza: 15.8 meses; plazo neto con póliza ($38,380.00/mes): 23.5 meses."
    )

    add_h2("3.4 Esquema de Cierre y Pagos por 6 Hitos Ágiles")
    doc.add_paragraph(
        "El plan de cobro escalonado asegura certidumbre contra entregables en Staging:\n"
        "• Hito 0 (Firma y Arranque): Anticipo del 20% ($180,136.02 MXN sin IVA). Monorepo, Docker Compose, Prisma y licencias.\n"
        "• Hito 1 (Sprint 2 - Backend & Seguridad): 15% ($135,102.02 MXN). Backend Core, JWT stateless, RBAC y reCAPTCHA.\n"
        "• Hito 2 (Sprint 4 - Eventos RabbitMQ & Frontend Vue 3): 15% ($135,102.02 MXN). Broker CloudAMQP, Patrón Saga y vistas prerenderizadas.\n"
        "• Hito 3 (Sprint 6 - POS mostrador & Trazabilidad ODS 12): 15% ($135,102.02 MXN). POS táctil, pagos mixtos y trazabilidad.\n"
        "• Hito 4 (Sprint 8 - Dashboard analítico & Testing Vitest/Playwright): 15% ($135,102.02 MXN). Dashboard UTM y reporte SAST.\n"
        "• Hito 5 (Cierre y Despliegue GCP con Terraform): Finiquito del 20% ($180,136.02 MXN). Infraestructura productiva y entrega de llaves."
    )

    add_h2("3.5 Análisis de Sensibilidad y Escenarios de Rentabilidad")
    sens_doc_data = [
        ("Conservador (Piso Mínimo)", "20.0%", "$788,095.11", "$914,190.33", "$157,619.02", "Piso de negociación que sacrifica margen comercial, no costos de desarrollo."),
        ("Esperado / Base (Recomendado)", "30.0%", "$900,680.12", "$1,044,788.94", "$270,204.04", "Propuesta base recomendada. Mantiene la rentabilidad del 30% proyectada."),
        ("Premium / Valor Agregado", "35.0%", "$969,963.21", "$1,125,157.32", "$339,487.12", "Paquete con 6 meses de póliza SLA 99.5% ($49,950 MXN costo asumido) y analítica avanzada. Utilidad ajustada post-SLA: $289,537.12 MXN (margen efectivo del 29.9%).")
    ]
    tbl_sens = doc.add_table(rows=len(sens_doc_data) + 1, cols=6)
    tbl_sens.alignment = WD_TABLE_ALIGNMENT.CENTER
    sens_headers = ["Escenario", "Margen", "Precio sin IVA", "Precio con IVA", "Utilidad antes ISR", "Criterio de Negociación"]
    for c_idx, h in enumerate(sens_headers):
        cell = tbl_sens.rows[0].cells[c_idx]
        set_cell_shading(cell, HEX_HEADER)
        set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8.0)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        if c_idx in [1, 2, 3, 4]: p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    for r_idx, row_data in enumerate(sens_doc_data, start=1):
        bg = HEX_SUCCESS if "Esperado" in row_data[0] else (HEX_ALT if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, val in enumerate(row_data):
            cell = tbl_sens.rows[r_idx].cells[c_idx]
            set_cell_shading(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(7.5)
            if "Esperado" in row_data[0]: r.font.bold = True
            if c_idx in [1, 2, 3, 4]: p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # 4. Conclusiones y Referencias
    add_h1("4. Conclusiones y Reconocimiento de Límites del Modelo")
    doc.add_paragraph(
        "El ejercicio presupuestal confirma la complementariedad entre ingeniería de software y gestión financiera. "
        "No obstante, se reconocen los límites del modelo:\n"
        "1. La carga patronal del 30% es una estimación técnica sujeta a primas de riesgo IMSS definitivas.\n"
        "2. Los beneficios de mermas y ventas son supuestos preliminares que requerirán validación con registros históricos reales.\n"
        "3. Las variaciones en tarifas de cómputo en la nube e impacto cambiario USD/MXN se amortiguan mediante la reserva de contingencia del 10% ($57,316.01 MXN)."
    )

    doc.save(docx_path)
    print(f"Documento Word guardado en: {docx_path}")
    shutil.copyfile(docx_path, docx_downloads)
    print(f"Copia de Word en Descargas: {docx_downloads}")

    # -------------------------------------------------------------
    # 3. GENERAR HTML ESTILIZADO Y COMPILAR PDF CON CHROME HEADLESS
    # -------------------------------------------------------------
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Actividad 4: Gestión de Finanzas — Monchis Café</title>
  <style>
    @page {{
      size: letter portrait;
      margin: 1.8cm 1.8cm 1.8cm 1.8cm;
      @bottom-right {{
        content: counter(page);
      }}
    }}
    body {{
      font-family: 'Segoe UI', Arial, sans-serif;
      font-size: 9.5pt;
      line-height: 1.45;
      color: #222222;
      margin: 0;
      padding: 0;
    }}
    h1 {{
      font-size: 13pt;
      color: #17365D;
      border-bottom: 2px solid #17365D;
      padding-bottom: 4px;
      margin-top: 18px;
      margin-bottom: 8px;
      page-break-after: avoid;
    }}
    h2 {{
      font-size: 11pt;
      color: #244B7A;
      margin-top: 12px;
      margin-bottom: 6px;
      page-break-after: avoid;
    }}
    p {{
      margin-top: 0;
      margin-bottom: 8px;
      text-align: justify;
    }}
    .header-box {{
      background: linear-gradient(135deg, #17365D 0%, #244B7A 100%);
      color: #ffffff;
      padding: 16px 20px;
      border-radius: 6px;
      margin-bottom: 14px;
    }}
    .header-box h1 {{
      color: #ffffff;
      border-bottom: none;
      margin: 0 0 4px 0;
      font-size: 15pt;
    }}
    .header-box p {{
      margin: 0;
      color: #D9E2EC;
      font-size: 9.5pt;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 8px;
      margin-bottom: 12px;
      font-size: 8pt;
    }}
    th, td {{
      border: 1px solid #D3D3D3;
      padding: 5px 7px;
      vertical-align: middle;
    }}
    th {{
      background-color: #17365D;
      color: #ffffff;
      font-weight: bold;
      text-align: left;
    }}
    .bg-alt {{
      background-color: #F0F4F8;
    }}
    .bg-success {{
      background-color: #E2F0D9;
      font-weight: bold;
    }}
    .bg-subhead {{
      background-color: #D9E2EC;
      font-weight: bold;
    }}
    .text-right {{
      text-align: right;
    }}
    .text-center {{
      text-align: center;
    }}
    .bold {{
      font-weight: bold;
    }}
    .kpi-card {{
      background: #F8FAFC;
      border-left: 4px solid #17365D;
      padding: 10px 14px;
      margin: 10px 0;
      font-size: 8.5pt;
    }}
    .page-break {{
      page-break-before: always;
    }}
    ul {{
      margin-top: 4px;
      margin-bottom: 8px;
      padding-left: 20px;
    }}
    li {{
      margin-bottom: 3px;
    }}
  </style>
</head>
<body>

  <div class="header-box">
    <h1>ACTIVIDAD 4: GESTIÓN DE FINANZAS</h1>
    <p><b>Proyecto Integrador:</b> Monchis Café — Plataforma Web y POS Seguro para Cafetería Orgánica</p>
    <p><b>Docente:</b> Dr. Gabriel Navarro Salcedo | <b>Estudiante:</b> Ernesto Hatuey Fierro Meléndez (Código: 215487963)</p>
    <p><b>Fecha de Entrega:</b> 24 de Octubre de 2026 | <b>Ponderación:</b> 4% de la Evaluación Total</p>
  </div>

  <h1>1. Resumen Ejecutivo de Indicadores Financieros</h1>
  <p>Consolidado de las variables económicas del proyecto, modeladas dinámicamente en la plantilla oficial y vinculadas a la hoja ESTRATEGIA DE VENTA:</p>

  <table>
    <thead>
      <tr>
        <th>Indicador Financiero Clave</th>
        <th class="text-right">Valor Proyectado</th>
        <th class="text-center">% s/ Venta</th>
        <th>Interpretación y Relevancia Operativa</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="bold">Costo Base Total (CTB)</td>
        <td class="text-right bold">$573,160.08</td>
        <td class="text-center">63.6%</td>
        <td>Costos empresariales directos, indirectos, nómina y costo financiero.</td>
      </tr>
      <tr class="bg-alt">
        <td class="bold">Fondo de Contingencia (10%)</td>
        <td class="text-right bold">$57,316.01</td>
        <td class="text-center">6.4%</td>
        <td>Reserva de mitigación ante riesgos técnicos y variaciones de tarifas cloud.</td>
      </tr>
      <tr>
        <td class="bold">COSTO TOTAL DEL PROYECTO (CTP)</td>
        <td class="text-right bold">$630,476.09</td>
        <td class="text-center bold">70.0%</td>
        <td>Inversión neta requerida por la empresa para producir y entregar la solución.</td>
      </tr>
      <tr class="bg-alt">
        <td class="bold">Margen de Utilidad sobre Ventas</td>
        <td class="text-right bold">30.0%</td>
        <td class="text-center">N/A</td>
        <td>Margen comercial pactado sobre el precio sin impuestos.</td>
      </tr>
      <tr class="bg-subhead">
        <td class="bold">PRECIO DE VENTA SIN IVA (COTIZACIÓN)</td>
        <td class="text-right bold">$900,680.12</td>
        <td class="text-center bold">100.0%</td>
        <td>Cotización base de la solución completa llave en mano: CTP / (1 - Margen).</td>
      </tr>
      <tr>
        <td class="bold">IVA Trasladado (16%)</td>
        <td class="text-right bold">$144,108.82</td>
        <td class="text-center">16.0%</td>
        <td>Impuesto fiscal acreditable para el cliente contra sus débitos de IVA.</td>
      </tr>
      <tr class="bg-subhead">
        <td class="bold">PRECIO TOTAL FACTURADO CON IVA</td>
        <td class="text-right bold">$1,044,788.94</td>
        <td class="text-center bold">116.0%</td>
        <td>Monto total formalizado convenido en la propuesta económica del contrato.</td>
      </tr>
      <tr>
        <td class="bold">UTILIDAD ANTES DE ISR (PROYECTADA)</td>
        <td class="text-right bold">$270,204.04</td>
        <td class="text-center bold">30.0%</td>
        <td>Ganancia empresarial antes de ISR corporativo anual para solvencia e I+D.</td>
      </tr>
      <tr class="bg-alt">
        <td class="bold">ISR Corporativo Estimado (30%)</td>
        <td class="text-right bold">$81,061.21</td>
        <td class="text-center">9.0%</td>
        <td>Provisión estimada del impuesto sobre la renta empresarial (LISR art. 9).</td>
      </tr>
      <tr class="bg-success">
        <td class="bold">UTILIDAD ESTIMADA DESPUÉS DE ISR</td>
        <td class="text-right bold">$189,142.83</td>
        <td class="text-center bold">21.0%</td>
        <td>Beneficio neto proyectado disponible tras obligaciones tributarias.</td>
      </tr>
      <tr>
        <td class="bold">Punto de Equilibrio (Soluciones)</td>
        <td class="text-right bold">1 Solución</td>
        <td class="text-center">N/A</td>
        <td>Un único contrato llave en mano cubre la estructura de costos operativos.</td>
      </tr>
      <tr class="bg-alt">
        <td class="bold">Punto de Equilibrio en Pesos</td>
        <td class="text-right bold">$602,641.80</td>
        <td class="text-center">66.9%</td>
        <td>Facturación mínima sin IVA necesaria para cubrir costos fijos y variables.</td>
      </tr>
      <tr>
        <td class="bold">Margen de Seguridad Comercial</td>
        <td class="text-right bold">33.1%</td>
        <td class="text-center">N/A</td>
        <td>Margen de tolerancia frente a contingencias antes de entrar en pérdidas.</td>
      </tr>
    </tbody>
  </table>

  <h1>2. Cuadro Justificativo Financiero (Pertinencia de Costos - 50%)</h1>
  <p>Desglose analítico que justifica la pertinencia técnica, operativa y económica de cada partida presupuestal:</p>

  <table>
    <thead>
      <tr>
        <th>Rubro Presupuestal</th>
        <th class="text-right">Importe (MXN)</th>
        <th class="text-center">% s/ CTP</th>
        <th>Criterio Técnico y Justificación Operativa</th>
        <th>Impacto en Calidad y Mitigación de Riesgos</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="bold">Nómina y Carga Patronal</td>
        <td class="text-right">$465,400.00</td>
        <td class="text-center">73.81%</td>
        <td>4 perfiles (Scrum Master/DevOps, Frontend Vue 3, Backend Node.js, QA) por 16 semanas. Sueldos brutos de $89.5k/mes más estimación del 30% de carga patronal (IMSS, Infonavit 5%, ISN 3%).</td>
        <td>Garantiza 8 sprints bajo TDD (>80% cobertura) y reduce el riesgo de rotación técnica mediante compensaciones de mercado.</td>
      </tr>
      <tr class="bg-alt">
        <td class="bold">Gastos Fijos de Operación</td>
        <td class="text-right">$60,000.00</td>
        <td class="text-center">9.52%</td>
        <td>Coworking ($6k/mes), energía ($1.2k), fibra simétrica con IP fija ($1.5k), despacho contable ($2.5k), herramientas SaaS ($1.8k), gestión comercial ($1k) y suministros ($1k) ($15k/mes).</td>
        <td>Asegura entorno ininterrumpido para CI/CD, soporte fiscal para timbrado CFDI 4.0 y herramientas de trabajo colaborativo.</td>
      </tr>
      <tr>
        <td class="bold">Costos Directos (10 rubros)</td>
        <td class="text-right">$26,800.00</td>
        <td class="text-center">4.25%</td>
        <td>GCP ($7.2k), GitHub/Sentry ($2.4k), CloudAMQP RabbitMQ ($2.2k), dominio/SSL ($950), dispositivos ($3k), pentesting ($4.5k), viáticos ($3k), papel/cables ($850), SAST ($1.2k) y otros ($1.5k).</td>
        <td>Sustenta arquitectura orientada a eventos (Saga/DLQ), seguridad de datos de pago y validación física en barra.</td>
      </tr>
      <tr class="bg-alt">
        <td class="bold">Inversión Inicial Asignada</td>
        <td class="text-right">$19,638.89</td>
        <td class="text-center">3.11%</td>
        <td>Depreciación en 4 meses según vida útil fiscal: 4 laptops (36 meses), mobiliario (60 meses), red (36 meses), licencias IDEs y kit POS ($19.6k de $148.8k).</td>
        <td>Aplica devengo contable: el proyecto absorbe únicamente el desgaste real de los activos productivos durante su ejecución.</td>
      </tr>
      <tr>
        <td class="bold">Intereses de Financiamiento</td>
        <td class="text-right">$1,321.19</td>
        <td class="text-center">0.21%</td>
        <td>Crédito de $40,000.00 MXN al 18% anual a 24 meses. Interés promedio prorrateado a 4 meses ($1,321.19 MXN) para anticipar compra de activos y absorber desfases del anticipo.</td>
        <td>Evita demoras operativas en el arranque derivadas de tiempos de dispersión bancaria de la primera transferencia.</td>
      </tr>
      <tr class="bg-alt">
        <td class="bold">Fondo de Contingencia (10%)</td>
        <td class="text-right">$57,316.01</td>
        <td class="text-center">9.09%</td>
        <td>Reserva estratégica del 10% s/ costo base para fluctuaciones en tarifas cloud en dólares, inflación o retrabajos técnicos menores.</td>
        <td>Absorbe imprevistos y constituye el único colchón financiero ante la ausencia de roles dedicados de DevOps, DBA o UX.</td>
      </tr>
      <tr class="bg-subhead">
        <td>TOTAL COSTO DEL PROYECTO</td>
        <td class="text-right">$630,476.09</td>
        <td class="text-center">100.00%</td>
        <td colspan="2">Suma integral de factores de costo empresarial necesarios para desarrollar, probar y liberar en producción el software Monchis Café.</td>
      </tr>
    </tbody>
  </table>

  <div class="page-break"></div>

  <h1>3. Estrategia Comercial de Venta según Costo y Utilidad (35%)</h1>

  <h2>3.1 Modelo de Fijación de Precios: Margen Comercial vs Recargo (Markup)</h2>
  <p>
    La cotización comercial se estructuró a partir de la metodología de <b>margen sobre ventas antes de impuestos</b>, evitando la pérdida de rentabilidad derivada de un recargo simple (markup):
  </p>
  <div class="kpi-card">
    <b>Fórmula Financiera de Precio:</b> Precio = CTP / (1 - Margen) = $630,476.09 / (1 - 0.30) = <b>$900,680.12 MXN sin IVA</b><br>
    <b>Utilidad antes de ISR:</b> $900,680.12 - $630,476.09 = <b>$270,204.04 MXN</b> (30.0% real sobre ventas facturadas).<br>
    <b>Facturación Final con 16% de IVA:</b> $900,680.12 x 1.16 = <b>$1,044,788.94 MXN</b> (IVA acreditable para el cliente).<br>
    <b>Utilidad Estimada después de ISR (30%):</b> $270,204.04 - $81,061.21 = <b>$189,142.83 MXN</b> (21.0% neto sobre ventas).
  </div>

  <h2>3.2 Modelo de Negocio Híbrido: Venta Inicial + Ingresos Recurrentes</h2>
  <p>
    <b>1. Venta Inicial Llave en Mano ($900,680.12 MXN + IVA):</b> Licenciamiento y puesta en producción de la plataforma web, POS táctil, broker RabbitMQ y microservicios en GCP.<br>
    <b>2. Póliza de Soporte, Mantenimiento Evolutivo y SLA ($18,500.00 MXN + IVA/mes a partir del Mes 5):</b> Disponibilidad del 99.5%, respuesta a incidentes de caja &lt; 2 horas en horario operativo, monitoreo de RabbitMQ DLQ y parches de seguridad (ARR de $222,000.00 MXN con 55% de margen).<br>
    <b>3. Licenciamiento por Franquicia / Sucursal ($45,000.00 MXN cuota única + $3,500.00 MXN/mes de soporte por sucursal):</b> Permite monetizar el crecimiento de Monchis Café si apertura nuevas tiendas.
  </p>

  <h2>3.3 Propuesta de Valor y Retorno de Inversión (Payback) para Monchis Café</h2>
  <p>
    Los beneficios operativos mensuales estimados corresponden a supuestos preliminares sujetos a validación con datos reales del negocio:
  </p>
  <table>
    <thead>
      <tr>
        <th>Beneficio Operativo Cuantificable</th>
        <th>Mecanismo del Sistema</th>
        <th class="text-right">Impacto Mensual</th>
        <th class="text-right">Beneficio Anual</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="bold">Reducción de Mermas de Café Orgánico (-22%)</td>
        <td>Control de rotación PEPS y trazabilidad de lotes regionales por finca.</td>
        <td class="text-right">$14,500.00</td>
        <td class="text-right">$174,000.00</td>
      </tr>
      <tr class="bg-alt">
        <td class="bold">Incremento en Ventas y Ticket Promedio (+24%)</td>
        <td>Programa Monchis Rewards (sellos digitales y bono termo -$5.00 MXN).</td>
        <td class="text-right">$38,500.00</td>
        <td class="text-right">$462,000.00</td>
      </tr>
      <tr>
        <td class="bold">Eliminación de Discrepancias en Caja (-98%)</td>
        <td>Conciliación automática de cobros mixtos (efectivo, tarjeta, SPEI).</td>
        <td class="text-right">$9,200.00</td>
        <td class="text-right">$110,400.00</td>
      </tr>
      <tr class="bg-alt">
        <td class="bold">Clientes Nuevos por SEO y Google Maps</td>
        <td>Prerenderizado vite-ssg, Schema.org LocalBusiness y atribución UTM.</td>
        <td class="text-right">$16,800.00</td>
        <td class="text-right">$201,600.00</td>
      </tr>
      <tr class="bg-subhead">
        <td colspan="2">TOTAL BENEFICIO OPERATIVO BRUTO ESTIMADO</td>
        <td class="text-right">$79,000.00</td>
        <td class="text-right">$948,000.00</td>
      </tr>
    </tbody>
  </table>

  <div class="kpi-card">
    <b>Evaluación del Período de Recuperación (Payback Period):</b><br>
    1. <b>Payback Bruto:</b> $900,680.12 / $79,000.00 = <b>11.4 meses</b> (sin descontar póliza ni costo de ventas).<br>
    2. <b>Payback Neto con Póliza SLA:</b> $900,680.12 / ($79,000.00 - $18,500.00) = $900,680.12 / $60,500.00 = <b>14.9 meses</b>.<br>
    3. <b>Payback Prudente (60% margen de contribución en ventas adicionales):</b> Beneficio neto de $56,880.00/mes ($33,180 margen ventas + $23,700 ahorros). Plazo sin póliza: <b>15.8 meses</b>; plazo neto con póliza ($38,380.00/mes): <b>23.5 meses</b>.
  </div>

  <h2>3.4 Esquema de Cierre y Financiamiento por 6 Hitos Ágiles</h2>
  <ul>
    <li><b>Hito 0 (Firma y Arranque - 20%):</b> $180,136.02 MXN sin IVA (Setup monorepo, Docker Compose, Prisma y compra inicial de licencias).</li>
    <li><b>Hito 1 (Sprint 2 - Backend & Seguridad - 15%):</b> $135,102.02 MXN (Backend Core, JWT stateless, RBAC y reCAPTCHA en Staging).</li>
    <li><b>Hito 2 (Sprint 4 - Eventos & Frontend - 15%):</b> $135,102.02 MXN (Broker RabbitMQ CloudAMQP, Patrón Saga y vistas Vue 3 prerenderizadas).</li>
    <li><b>Hito 3 (Sprint 6 - POS & Trazabilidad - 15%):</b> $135,102.02 MXN (POS mostrador, pagos mixtos y catálogo de café ODS 12).</li>
    <li><b>Hito 4 (Sprint 8 - Analítica & Testing - 15%):</b> $135,102.02 MXN (Dashboard analítico, atribución UTM y suites Vitest/Playwright).</li>
    <li><b>Hito 5 (Cierre y Despliegue en GCP - 20%):</b> $180,136.02 MXN (Terraform en GCP, manuales de usuario y entrega de llaves).</li>
  </ul>

  <h2>3.5 Análisis de Sensibilidad y Escenarios de Rentabilidad</h2>
  <table>
    <thead>
      <tr>
        <th>Escenario Comercial</th>
        <th class="text-center">Margen</th>
        <th class="text-right">Precio sin IVA</th>
        <th class="text-right">Precio con IVA</th>
        <th class="text-right">Utilidad antes ISR</th>
        <th>Criterio y Táctica de Negociación</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="bold">Conservador (Piso Mínimo)</td>
        <td class="text-center">20.0%</td>
        <td class="text-right">$788,095.11</td>
        <td class="text-right">$914,190.33</td>
        <td class="text-right bold">$157,619.02</td>
        <td>Piso de negociación que sacrifica margen comercial, no costos de desarrollo. Asegura el contrato ante restricciones presupuestales.</td>
      </tr>
      <tr class="bg-success">
        <td class="bold">Esperado / Base (Recomendado)</td>
        <td class="text-center bold">30.0%</td>
        <td class="text-right bold">$900,680.12</td>
        <td class="text-right bold">$1,044,788.94</td>
        <td class="text-right bold">$270,204.04</td>
        <td>Propuesta base óptima. Preserva la rentabilidad del 30.0% necesaria para la viabilidad de la empresa y amortización para el cliente.</td>
      </tr>
      <tr>
        <td class="bold">Premium / Valor Agregado</td>
        <td class="text-center">35.0%</td>
        <td class="text-right">$969,963.21</td>
        <td class="text-right">$1,125,157.32</td>
        <td class="text-right bold">$339,487.12</td>
        <td>Paquete con 6 meses de póliza SLA 99.5% ($49,950 MXN costo asumido) y analítica avanzada. Utilidad ajustada post-SLA: $289,537.12 MXN (margen efectivo del 29.9%).</td>
      </tr>
    </tbody>
  </table>

  <h1>4. Conclusiones y Límites del Modelo</h1>
  <p>
    El ejercicio presupuestal confirma que la ingeniería de software y la gestión financiera son disciplinas complementarias. Al aplicar los tabuladores fiscales de 2026, la carga patronal del 30% y una estrategia de precios basada en margen sobre ventas, el proyecto <b>Monchis Café</b> cuenta con bases financieras sólidas. No obstante, se reconocen los límites y supuestos del modelo: la tasa patronal es una estimación técnica sujeta a primas de riesgo definitivas, los beneficios operativos son proyecciones sujetas a validación empírica con la cafetería, y los riesgos cambiarios en servicios cloud en dólares son amortiguados mediante la reserva estratégica de contingencia del 10%.
  </p>

</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML generado en: {html_path}")

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    print("Compilando PDF con Chrome Headless...")
    subprocess.run(cmd, check=True)
    print(f"PDF generado con éxito en: {pdf_path}")
    
    shutil.copyfile(pdf_path, pdf_downloads)
    print(f"Copia de PDF en Descargas: {pdf_downloads}")
    print("\n¡Todos los entregables de la Actividad 4 han sido actualizados y generados exitosamente!")

if __name__ == "__main__":
    generate_deliverables()
