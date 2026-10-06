import os
import subprocess
import shutil
import math

def generate_activity_2_3_deliverable():
    # Parámetros Base de Monchis Café
    kloc = 22.5
    labor_rate_hourly = 358000.0 / 2720.0  # 131.617647... MXN/hr
    cost_per_pm = labor_rate_hourly * 160.0 # 21058.823529... MXN/PM (160 hrs/mes)

    # 1. COCOMO Básico (Semiacoplado)
    a_bas = 3.00
    b_bas = 1.12
    c_bas = 2.50
    d_bas = 0.35

    kloc_pow_b = kloc ** b_bas # 32.6922
    pm_bas = a_bas * kloc_pow_b # 98.0767
    pm_bas_pow_d = pm_bas ** d_bas # 4.9779
    tdev_bas = c_bas * pm_bas_pow_d # 12.4448 meses
    np_bas = pm_bas / tdev_bas # 7.8809 personas
    prod_bas = (kloc * 1000.0) / pm_bas # 229.41 LOC/PM
    cost_bas = pm_bas * cost_per_pm # 2,065,379.11 MXN

    # 2. COCOMO Intermedio (Semiacoplado)
    drivers = [
        ("RELY", "Fiabilidad requerida del software", "Alta", 1.15, "Manejo de pedidos, cobros POS y persistencia de transacciones."),
        ("DATA", "Tamaño de la base de datos", "Nominal", 1.00, "Base de datos relacional PostgreSQL con volumen comercial moderado."),
        ("CPLX", "Complejidad del software", "Alta", 1.15, "Patrón Saga distribuido con RabbitMQ, transacciones y JWT."),
        ("TIME", "Restricción de tiempo de ejecución", "Nominal", 1.00, "Aplicación transaccional web sin restricciones de tiempo real estricto."),
        ("STOR", "Restricción de memoria principal", "Nominal", 1.00, "Memoria holgada en instancias Cloud Run y contenedores Docker."),
        ("VIRT", "Volatilidad de la máquina virtual", "Baja", 0.87, "Entorno estandarizado en contenedores Docker y Node.js LTS."),
        ("TURN", "Tiempo de respuesta de la máquina", "Nominal", 1.00, "Entorno de desarrollo ágil con HMR interactivo en Vite."),
        ("ACAP", "Capacidad de los analistas", "Alta", 0.86, "Equipo con dominio completo de la arquitectura y requerimientos."),
        ("AEXP", "Experiencia en la aplicación", "Nominal", 1.00, "Experiencia media en comercio electrónico y puntos de venta."),
        ("PCAP", "Capacidad de los programadores", "Alta", 0.86, "Dominio sólido de TypeScript, Vue 3, Next.js y Prisma."),
        ("VEXP", "Experiencia en la máquina virtual", "Nominal", 1.00, "Familiaridad estándar en Linux, GCP y Docker."),
        ("LEXP", "Experiencia en lenguajes de prog.", "Alta", 0.95, "Especialización en TypeScript y JavaScript full-stack."),
        ("MODP", "Prácticas modernas de programación", "Muy Alta", 0.82, "Arquitectura monorepo Turborepo, TDD, linting y CI/CD."),
        ("TOOL", "Uso de herramientas de desarrollo", "Alta", 0.91, "Herramientas avanzadas: Prisma Studio, Playwright, Vitest."),
        ("SCED", "Plazo de desarrollo requerido", "Nominal*", 1.00, "Se mantiene nominal (1.00) para aislar tecnología y equipo (ver análisis).")
    ]

    eaf = 1.0
    for d in drivers:
        eaf *= d[3]

    pm_int = eaf * pm_bas # 59.1638 PM
    pm_int_pow_d = pm_int ** d_bas # 4.1708
    tdev_int = c_bas * pm_int_pow_d # 10.4270 meses
    np_int = pm_int / tdev_int # 5.6741 personas
    prod_int = (kloc * 1000.0) / pm_int # 380.30 LOC/PM
    cost_int = pm_int * cost_per_pm # 1,245,920.89 MXN

    # 3. Presupuesto Inicial (WBS)
    labor_hours_wbs = 2720
    pm_wbs = labor_hours_wbs / 160.0 # 17.0 PM
    tdev_wbs = 4.0 # 16 semanas = 4 meses
    np_wbs = pm_wbs / tdev_wbs # 4.25 desarrolladores equivalentes
    cost_labor_wbs = 358000.00
    cost_hw_wbs = 9500.00
    cost_cloud_wbs = 12750.00
    cost_risk_wbs = 38025.00
    cost_total_wbs = 418275.00
    prod_wbs = (kloc * 1000.0) / pm_wbs # 1323.53 LOC/PM

    # Cifras consistentes unificadas
    cost_bas_str = f"${cost_bas:,.2f} MXN"
    cost_int_str = f"${cost_int:,.2f} MXN"

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Actividad 2.3 - Tabla Comparativa de Estimación del Proyecto - Monchis Café</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        @page {{
            size: letter;
            margin: 11mm 13mm 11mm 13mm;
            @top-right {{
                content: "Actividad 2.3 · Métodos de Estimación de Software";
                font-family: 'Inter', sans-serif;
                font-size: 7.5pt;
                color: #64748B;
            }}
            @bottom-left {{
                content: "Monchis Café · Dr. Gabriel Navarro Salcedo · Ernesto Fierro";
                font-family: 'Inter', sans-serif;
                font-size: 7.5pt;
                color: #64748B;
            }}
            @bottom-right {{
                content: "Página " counter(page);
                font-family: 'Inter', sans-serif;
                font-size: 7.5pt;
                font-weight: 700;
                color: #1E293B;
            }}
        }}

        @page:first {{
            @top-right {{ content: none; }}
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 8.3pt;
            line-height: 1.36;
            color: #1E293B;
            background-color: #FFFFFF;
            margin: 0;
            padding: 0;
            text-align: justify;
        }}

        .avoid-break {{
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .page-break {{
            page-break-before: always;
        }}

        /* Encabezado Institucional */
        .inst-header {{
            border-bottom: 2px solid #1E3A8A;
            padding-bottom: 6px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}

        .inst-titles h2 {{
            font-size: 10.5pt;
            font-weight: 800;
            color: #1E3A8A;
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .inst-titles h3 {{
            font-size: 8.8pt;
            font-weight: 600;
            color: #475569;
            margin: 2px 0 0 0;
        }}

        .doc-badge {{
            background-color: #F1F5F9;
            border: 1px solid #CBD5E1;
            padding: 3px 8px;
            border-radius: 4px;
            text-align: right;
            font-size: 7.5pt;
            color: #475569;
            font-weight: 600;
        }}

        .doc-title {{
            font-size: 13pt;
            font-weight: 800;
            color: #0F172A;
            margin: 8px 0 3px 0;
            line-height: 1.2;
            letter-spacing: -0.2px;
        }}

        .doc-subtitle {{
            font-size: 9pt;
            font-weight: 500;
            color: #2563EB;
            margin: 0 0 8px 0;
        }}

        /* Bloque de Metadatos */
        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 5px;
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 4px;
            padding: 6px 9px;
            margin-bottom: 10px;
        }}

        .meta-item {{
            font-size: 7.7pt;
        }}

        .meta-item strong {{
            color: #334155;
            font-weight: 700;
            display: block;
        }}

        .meta-item span {{
            color: #0F172A;
        }}

        /* Tipografía de Secciones */
        h1 {{
            font-size: 9.8pt;
            font-weight: 800;
            color: #1E3A8A;
            border-left: 3.5px solid #2563EB;
            padding-left: 6px;
            margin: 10px 0 4px 0;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}

        h2 {{
            font-size: 8.6pt;
            font-weight: 700;
            color: #0F172A;
            margin: 7px 0 3px 0;
        }}

        h3 {{
            font-size: 8.2pt;
            font-weight: 700;
            color: #1E3A8A;
            margin: 5px 0 2px 0;
        }}

        p {{
            margin: 0 0 4.5px 0;
        }}

        ul, ol {{
            margin: 0 0 5px 0;
            padding-left: 16px;
        }}

        li {{
            margin-bottom: 2px;
        }}

        /* Cajas de Texto y Notas Técnicas */
        .callout {{
            border: 1px solid #CBD5E1;
            border-left: 3.5px solid #1E3A8A;
            background-color: #F8FAFC;
            border-radius: 4px;
            padding: 6px 9px;
            margin: 6px 0;
            font-size: 7.9pt;
            line-height: 1.36;
            color: #1E293B;
        }}

        .callout-title {{
            font-weight: 700;
            font-size: 8.1pt;
            color: #1E3A8A;
            margin-bottom: 3px;
        }}

        /* Fórmulas Matemáticas Académicas */
        .formula-card {{
            background-color: #F8FAFC;
            color: #0F172A;
            border: 1px solid #CBD5E1;
            border-left: 3.5px solid #1E3A8A;
            border-radius: 4px;
            padding: 7px 11px;
            margin: 6px 0;
            font-size: 7.9pt;
            line-height: 1.42;
        }}

        .formula-title {{
            color: #1E3A8A;
            font-weight: 700;
            font-size: 8.1pt;
            margin-bottom: 3px;
            text-transform: uppercase;
            font-family: 'Inter', sans-serif;
        }}

        .formula-hl {{
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            color: #1E3A8A;
        }}

        /* Tablas */
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 7.3pt;
            margin: 4px 0;
        }}

        th {{
            background-color: #1E3A8A;
            color: #FFFFFF;
            font-weight: 700;
            text-align: left;
            padding: 3px 5px;
            border: 1px solid #0F2D6B;
            font-size: 7.3pt;
        }}

        th.text-center, td.text-center {{
            text-align: center;
        }}

        th.text-right, td.text-right {{
            text-align: right;
        }}

        td {{
            padding: 2.8px 4.5px;
            border: 1px solid #CBD5E1;
            color: #1E293B;
            vertical-align: middle;
        }}

        tr:nth-child(even) td {{
            background-color: #F8FAFC;
        }}

        tr.highlight-total td {{
            background-color: #EEF2F6;
            font-weight: 700;
            color: #0F172A;
            border-top: 1.5px solid #1E3A8A;
            border-bottom: 2px solid #1E3A8A;
        }}

        /* Tabla Comparativa Destacada */
        .comp-table {{
            margin-top: 2px;
            margin-bottom: 4px;
        }}

        .comp-table th {{
            background-color: #1E3A8A;
            font-size: 7.3pt;
            padding: 3.5px 5px;
        }}

        .comp-table td {{
            font-size: 6.8pt;
            line-height: 1.18;
            padding: 2px 4px;
        }}

        .calc-steps {{
            background-color: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-radius: 4px;
            padding: 5px 9px;
            margin: 5px 0;
            font-family: 'JetBrains Mono', monospace;
            font-size: 7.5pt;
            line-height: 1.36;
            color: #1E293B;
        }}
    </style>
</head>
<body>

    <!-- ================= ENCABEZADO INSTITUCIONAL ================= -->
    <div class="inst-header">
        <div class="inst-titles">
            <h2>Universidad de Guadalajara</h2>
            <h3>Administración de Proyectos de Software · Cátedra Dr. Gabriel Navarro Salcedo</h3>
        </div>
        <div class="doc-badge">
            Actividad 2.3 · Ciclo 2026-B
        </div>
    </div>

    <div class="doc-title">Actividad 2.3: Tabla Comparativa de Estimación del Proyecto</div>
    <div class="doc-subtitle">Evaluación Técnica: Presupuesto Inicial (WBS / Bottom-Up), COCOMO Básico y COCOMO Intermedio</div>

    <!-- ================= METADATOS ================= -->
    <div class="meta-grid">
        <div class="meta-item"><strong>Proyecto:</strong> <span>Monchis Café Web POS</span></div>
        <div class="meta-item"><strong>Alumno:</strong> <span>Ernesto Fierro Meléndez</span></div>
        <div class="meta-item"><strong>Docente:</strong> <span>Dr. Gabriel Navarro Salcedo</span></div>
        <div class="meta-item"><strong>Ponderación:</strong> <span>2 Puntos (2 % Total)</span></div>
        <div class="meta-item"><strong>Tamaño Software:</strong> <span>22.5 KLOC (22,500 SLOC)</span></div>
        <div class="meta-item"><strong>Modo COCOMO:</strong> <span>Semiacoplado (Semidetached)</span></div>
        <div class="meta-item"><strong>Horizonte Planeado:</strong> <span>16 Semanas (4.0 Meses)</span></div>
        <div class="meta-item"><strong>Fecha de Emisión:</strong> <span>Octubre de 2026</span></div>
    </div>

    <!-- ================= RESUMEN EJECUTIVO ================= -->
    <div class="callout avoid-break">
        <div class="callout-title">Objetivo General de la Actividad</div>
        Evaluar y contrastar tres metodologías de estimación aplicadas al proyecto <b>Monchis Café — Plataforma Web para Cafetería Orgánica y Comercial</b>: 
        (1) la estimación analítica por <b>Presupuesto Inicial (WBS / Bottom-Up)</b> basada en la plantilla oficial de Smartsheet (Smartsheet Inc., 2023), 
        (2) el modelo paramétrico <b>COCOMO Básico (Boehm, 1981; Navarro Salcedo, 2026)</b>, y 
        (3) el modelo <b>COCOMO Intermedio (15 Conductores de Costo)</b>. El análisis busca fundamentar matemáticamente la selección del método más idóneo para la gestión presupuestal y de ingeniería del sistema.
    </div>

    <!-- ================= SECCIÓN 1 ================= -->
    <h1>1. Contextualización del Proyecto: Monchis Café</h1>
    <p>
        <b>Monchis Café</b> es una plataforma web de comercio electrónico y Punto de Venta (POS) diseñada para una cafetería orgánica de especialidad, orientada a la sostenibilidad comercial (comercio justo y reducción de residuos). El sistema opera sobre una arquitectura distribuida desacoplada estructurada en un monorepo:
    </p>
    <ul>
        <li><b>Frontend Web y POS Táctil:</b> Desarrollado en Vue 3 con Pinia, prerenderizado estático mediante <code>vite-ssg</code>, catálogo comercial, módulo de personalización de bebidas y panel táctil de barra.</li>
        <li><b>Backend y Capa Transaccional:</b> API modular desarrollada en Next.js y Node.js, autenticación stateless mediante JWT rotativo en cookies <code>httpOnly</code> seguras, autorización RBAC y persistencia relacional con PostgreSQL vía Prisma ORM.</li>
        <li><b>Orquestación Distribuida y Resiliencia:</b> Manejo asíncrono de pedidos y cobros mediante el Patrón Saga Orquestado respaldado en RabbitMQ (topic exchange <code>cafeteria.events</code> y colas de reintento Dead Letter Queue - DLQ).</li>
        <li><b>Módulo de Trazabilidad y Fidelización:</b> Pasaporte digital QR de fincas cafetaleras y gestión de recompensas con bono por vaso reutilizable (-$5 MXN).</li>
    </ul>

    <h2>1.1. Estimación y Justificación del Tamaño del Software (22.5 KLOC)</h2>
    <p>
        El volumen total de desarrollo nuevo se dimensionó en <b>22,500 líneas de código fuente (22.5 KLOC)</b>. Esta estimación la realizó el equipo aplicando la técnica de descomposición por módulos y analogía con proyectos web previos, siguiendo los principios de estimación basados en líneas de código descritos en la literatura de ingeniería de software (Pressman & Maxim, 2020):
    </p>
    <ul>
        <li><b>Frontend (Vue 3, Pinia, vite-ssg): ~8.5 KLOC.</b> Se calculó a partir de ~25 vistas y componentes interactivos (panel táctil de mostrador POS, personalizador de bebidas con leches y siropes, catálogo, carrito, resumen de caja y store global de estado en Pinia).</li>
        <li><b>Backend y Servicios (Next.js, TypeScript): ~7.0 KLOC.</b> Dimensionado sobre ~18 endpoints REST (gestión de órdenes, cobros, catálogo, inventario y autenticación), middleware de tokens JWT stateless y esquemas de validación con Zod.</li>
        <li><b>Persistencia y Mensajería (Prisma ORM, RabbitMQ): ~3.5 KLOC.</b> Incluye esquema relacional de PostgreSQL, migraciones de base de datos, productores/consumidores de eventos y lógica de compensación de fallos en colas DLQ del Patrón Saga.</li>
        <li><b>Pruebas Automatizadas y DevOps: ~3.5 KLOC.</b> Pruebas unitarias con Vitest, pruebas de integración y flujos e2e de compra con Playwright, Dockerfiles multicapa y configuración de pipelines de CI/CD.</li>
    </ul>

    <!-- ================= SECCIÓN 2 ================= -->
    <h1>2. Método 1: Presupuesto Inicial (WBS / Bottom-Up)</h1>
    <p>
        El presupuesto formal del proyecto se diseñó utilizando la plantilla oficial de propuesta de presupuesto de proyectos de Smartsheet (Smartsheet Inc., 2023; <code>docs/presupuesto/Presupuesto_Monchis_Cafe.xlsx</code>), siguiendo los lineamientos de descomposición jerárquica de trabajo del Project Management Institute (PMI, 2019). El presupuesto se desglosa en 4 categorías WBS:
    </p>

    <!-- Tabla WBS Resumen -->
    <table>
        <thead>
            <tr>
                <th style="width: 10%;">WBS</th>
                <th style="width: 32%;">Categoría / Paquete de Trabajo</th>
                <th style="width: 38%;">Descripción Operativa y Alcance</th>
                <th style="width: 20%;" class="text-right">Monto Total (MXN)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>1.0</b></td>
                <td><b>Recursos Humanos (Mano de Obra / Labor)</b></td>
                <td>5 roles técnicos (Scrum Master, DevOps, Backend, Frontend, QA/Seguridad) cubriendo 9 tareas WBS y 2,720 horas planeadas de desarrollo.</td>
                <td class="text-right"><b>$358,000.00 MXN</b></td>
            </tr>
            <tr>
                <td><b>2.0</b></td>
                <td><b>Equipamiento y Hardware Mostrador</b></td>
                <td>Terminal táctil mostrador Android 10.5" ($6,500), Impresora térmica de tickets 80mm ($1,800) y Lector de códigos 1D/2D QR ($1,200).</td>
                <td class="text-right"><b>$9,500.00 MXN</b></td>
            </tr>
            <tr>
                <td><b>3.0</b></td>
                <td><b>Infraestructura Cloud y Licenciamiento</b></td>
                <td>Google Cloud Platform Cloud Run/SQL/Redis ($7,200), CloudAMQP RabbitMQ ($2,200), Dominio SSL TLS 1.3 ($950) y GitHub ($2,400) por 4 meses.</td>
                <td class="text-right"><b>$12,750.00 MXN</b></td>
            </tr>
            <tr>
                <td><b>4.0</b></td>
                <td><b>Fondo de Contingencia y Mitigación (10%)</b></td>
                <td>Reserva del 10% sobre costos directos para imprevistos técnicos, fluctuación cambiaria y picos imprevistos de cómputo en la nube.</td>
                <td class="text-right"><b>$38,025.00 MXN</b></td>
            </tr>
            <tr class="highlight-total">
                <td colspan="3" class="text-right"><b>PRESUPUESTO TOTAL INICIAL:</b></td>
                <td class="text-right"><b>$418,275.00 MXN</b></td>
            </tr>
        </tbody>
    </table>

    <div class="callout avoid-break">
        <div class="callout-title">Métricas de Ingeniería del Presupuesto Inicial</div>
        <b>• Duración Planificada:</b> 16 Semanas (4.0 meses de calendario en 8 sprints quincenales).<br>
        <b>• Esfuerzo Equivalente en Persona-Mes:</b> PM = 2,720 horas / 160 hrs/mes = <b>{pm_wbs:.2f} PM</b>.<br>
        <b>• Personal Promedio Asignado:</b> NP = 17.0 PM / 4.0 meses = <b>{np_wbs:.2f} personas a tiempo completo</b>.<br>
        <b>• Costo Promedio por Hora / Persona-Mes:</b> Tarifa Horaria = $131.62 MXN/hr &rarr; Costo/PM = 160 hrs &times; $131.62 = <b>${cost_per_pm:,.2f} MXN/PM</b>.<br>
        <b>• Productividad Implícita:</b> Prod = 22,500 LOC / 17.0 PM = <b>{prod_wbs:,.2f} LOC / Persona-Mes</b> (~66 LOC por día laboral por desarrollador).<br>
        <span style="color:#B45309; font-size:7.4pt;"><b>Nota de riesgo:</b> Esta productividad implícita es alcanzable mediante el uso de librerías modernas y generadores de código, pero constituye un plan agresivo. Si el alcance final supera las 22.5 KLOC o se presentan bloqueos en la integración con el hardware POS, el cronograma de 16 semanas enfrentará riesgos significativos de retraso.</span>
    </div>

    <!-- ================= SECCIÓN 3 ================= -->
    <h1>3. Método 2: Estimación por COCOMO Básico (Boehm, 1981)</h1>
    <p>
        El modelo COCOMO Básico estima el esfuerzo y el calendario como funciones de potencia exclusivas del volumen de código en miles de líneas (KLOC; Boehm, 1981). Para Monchis Café (22.5 KLOC, arquitectura distribuida y equipo con experiencia intermedia), la clasificación corresponde al <b>Modo Semiacoplado (Semidetached)</b> (Navarro Salcedo, 2026):
    </p>

    <div class="formula-card avoid-break">
        <div class="formula-title">Ecuaciones del Modelo COCOMO Básico — Modo Semiacoplado (Navarro Salcedo, 2026)</div>
        <div>Coeficientes: <span class="formula-hl">A = 3.00,  B = 1.12,  C = 2.50,  D = 0.35</span></div>
        <div>1. Esfuerzo Nominal: <span class="formula-hl">PM = A · (KLOC)<sup>B</sup></span></div>
        <div>2. Tiempo de Desarrollo: <span class="formula-hl">TDEV = C · (PM)<sup>D</sup></span></div>
        <div>3. Personal Promedio Requerido: <span class="formula-hl">NP = PM / TDEV</span></div>
        <div>4. Costo Estimado de Desarrollo: <span class="formula-hl">Costo = PM · (Tarifa Promedio PM)</span></div>
    </div>

    <h2>3.1. Desarrollo Matemático Paso a Paso</h2>
    <div class="calc-steps avoid-break">
        <b>Paso 1: Cálculo del Esfuerzo Nominal (PM)</b><br>
        &bull; KLOC = 22.5<br>
        &bull; Exponenciación: (22.5)<sup>1.12</sup> = exp(1.12 · ln(22.5)) = exp(1.12 · 3.113515) = exp(3.487137) = <b>{kloc_pow_b:.4f}</b><br>
        &bull; PM = 3.00 &times; {kloc_pow_b:.4f} = <b>{pm_bas:.4f} PM &approx; {pm_bas:.2f} Personas-Mes</b><br><br>

        <b>Paso 2: Cálculo del Tiempo de Desarrollo (TDEV)</b><br>
        &bull; Base de esfuerzo: ({pm_bas:.2f})<sup>0.35</sup> = exp(0.35 · ln({pm_bas:.4f})) = exp(0.35 · 4.5857) = exp(1.6050) = <b>{pm_bas_pow_d:.4f}</b><br>
        &bull; TDEV = 2.50 &times; {pm_bas_pow_d:.4f} = <b>{tdev_bas:.4f} meses &approx; {tdev_bas:.2f} Meses de Calendario</b><br><br>

        <b>Paso 3: Personal Promedio y Productividad</b><br>
        &bull; Personal promedio (NP) = PM / TDEV = {pm_bas:.4f} / {tdev_bas:.4f} = <b>{np_bas:.2f} Personas a tiempo completo</b><br>
        &bull; Productividad nominal = 22,500 LOC / {pm_bas:.2f} PM = <b>{prod_bas:.2f} LOC / Persona-Mes</b><br><br>

        <b>Paso 4: Valorización Económica (Tarifa base: ${cost_per_pm:,.2f} MXN/PM)</b><br>
        &bull; Costo de Mano de Obra = {pm_bas:.4f} PM &times; ${cost_per_pm:,.2f} = <b>{cost_bas_str}</b>
    </div>

    <div class="callout avoid-break">
        <div class="callout-title">Evaluación Crítica del Modelo Básico</div>
        El modelo COCOMO Básico proyecta <b>98.08 personas-mes</b> y <b>12.44 meses</b> con un costo de mano de obra de <b>{cost_bas_str}</b>. Este modelo asume la tecnología de desarrollo procedimental de 1981 sin frameworks web ni componentes reutilizables, lo que provoca una sobreestimación sustancial del esfuerzo para un sistema web actual. Además, requerir casi 8 desarrolladores a tiempo completo en un proyecto de 22.5 KLOC incrementaría la sobrecarga de comunicación interna según advierte la ley de Brooks (1975).
    </div>

    <!-- ================= SECCIÓN 4 ================= -->
    <h1>4. Método 3: Estimación por COCOMO Intermedio</h1>
    <p>
        El modelo COCOMO Intermedio corrige la rigidez del modelo básico al incorporar el <b>Factor de Ajuste de Esfuerzo (EAF - Effort Adjustment Factor)</b>, calculado como el producto de los 15 conductores de coste (<i>Cost Drivers</i>) de Boehm (1981), agrupados en atributos del producto, de la computadora, del personal y del proyecto:
    </p>

    <!-- Tabla de los 15 Cost Drivers de Boehm -->
    <table class="avoid-break">
        <thead>
            <tr>
                <th style="width: 14%;">Categoría</th>
                <th style="width: 28%;">Conductor de Costo (Cost Driver)</th>
                <th style="width: 14%;" class="text-center">Nivel Asignado</th>
                <th style="width: 12%;" class="text-center">Multiplicador</th>
                <th style="width: 32%;">Justificación Técnica del Proyecto</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>Producto</b></td>
                <td>RELY — Fiabilidad requerida del software</td>
                <td class="text-center">Alta</td>
                <td class="text-center"><b>1.15</b></td>
                <td>Manejo de pedidos, cobros POS y persistencia de transacciones.</td>
            </tr>
            <tr>
                <td><b>Producto</b></td>
                <td>DATA — Tamaño de la base de datos</td>
                <td class="text-center">Nominal</td>
                <td class="text-center">1.00</td>
                <td>Base de datos relacional PostgreSQL con volumen comercial moderado.</td>
            </tr>
            <tr>
                <td><b>Producto</b></td>
                <td>CPLX — Complejidad del software</td>
                <td class="text-center">Alta</td>
                <td class="text-center"><b>1.15</b></td>
                <td>Patrón Saga distribuido con RabbitMQ, transacciones y JWT.</td>
            </tr>
            <tr>
                <td><b>Plataforma</b></td>
                <td>TIME — Restricción de tiempo de ejecución</td>
                <td class="text-center">Nominal</td>
                <td class="text-center">1.00</td>
                <td>Aplicación transaccional web sin restricciones de tiempo real estricto.</td>
            </tr>
            <tr>
                <td><b>Plataforma</b></td>
                <td>STOR — Restricción de memoria principal</td>
                <td class="text-center">Nominal</td>
                <td class="text-center">1.00</td>
                <td>Memoria holgada en instancias Cloud Run y contenedores Docker.</td>
            </tr>
            <tr>
                <td><b>Plataforma</b></td>
                <td>VIRT — Volatilidad de la máquina virtual</td>
                <td class="text-center">Baja</td>
                <td class="text-center"><b>0.87</b></td>
                <td>Entorno estandarizado en contenedores Docker y Node.js LTS.</td>
            </tr>
            <tr>
                <td><b>Plataforma</b></td>
                <td>TURN — Tiempo de respuesta de la máquina</td>
                <td class="text-center">Nominal</td>
                <td class="text-center">1.00</td>
                <td>Entorno de desarrollo ágil con HMR interactivo en Vite.</td>
            </tr>
            <tr>
                <td><b>Personal</b></td>
                <td>ACAP — Capacidad de los analistas</td>
                <td class="text-center">Alta</td>
                <td class="text-center"><b>0.86</b></td>
                <td>Equipo con dominio completo de la arquitectura y requerimientos.</td>
            </tr>
            <tr>
                <td><b>Personal</b></td>
                <td>AEXP — Experiencia en la aplicación</td>
                <td class="text-center">Nominal</td>
                <td class="text-center">1.00</td>
                <td>Experiencia media en comercio electrónico y puntos de venta.</td>
            </tr>
            <tr>
                <td><b>Personal</b></td>
                <td>PCAP — Capacidad de los programadores</td>
                <td class="text-center">Alta</td>
                <td class="text-center"><b>0.86</b></td>
                <td>Dominio sólido de TypeScript, Vue 3, Next.js y Prisma.</td>
            </tr>
            <tr>
                <td><b>Personal</b></td>
                <td>VEXP — Experiencia en la máquina virtual</td>
                <td class="text-center">Nominal</td>
                <td class="text-center">1.00</td>
                <td>Familiaridad estándar en Linux, GCP y Docker.</td>
            </tr>
            <tr>
                <td><b>Personal</b></td>
                <td>LEXP — Experiencia en lenguajes de prog.</td>
                <td class="text-center">Alta</td>
                <td class="text-center"><b>0.95</b></td>
                <td>Especialización en TypeScript y JavaScript full-stack.</td>
            </tr>
            <tr>
                <td><b>Proyecto</b></td>
                <td>MODP — Prácticas modernas de programación</td>
                <td class="text-center">Muy Alta</td>
                <td class="text-center"><b>0.82</b></td>
                <td>Arquitectura monorepo Turborepo, TDD, linting y CI/CD.</td>
            </tr>
            <tr>
                <td><b>Proyecto</b></td>
                <td>TOOL — Uso de herramientas de desarrollo</td>
                <td class="text-center">Alta</td>
                <td class="text-center"><b>0.91</b></td>
                <td>Herramientas avanzadas: Prisma Studio, Playwright, Vitest.</td>
            </tr>
            <tr>
                <td><b>Proyecto</b></td>
                <td>SCED — Plazo de desarrollo requerido</td>
                <td class="text-center">Nominal*</td>
                <td class="text-center">1.00</td>
                <td>Se evalúa nominal (1.00) para aislar tecnología y equipo (ver nota).</td>
            </tr>
            <tr class="highlight-total">
                <td colspan="3"><b>PRODUCTO DE LOS 15 FACTORES (EAF):</b></td>
                <td class="text-center"><b>{eaf:.4f}</b></td>
                <td><b>EAF Neto: {eaf:.4f} (Ahorro del {(1.0-eaf)*100:.1f}% frente al nominal)</b></td>
            </tr>
        </tbody>
    </table>

    <div class="calc-steps avoid-break">
        <b>Cálculo Aritmético del Factor EAF:</b><br>
        EAF = 1.15 &times; 1.00 &times; 1.15 &times; 1.00 &times; 1.00 &times; 0.87 &times; 1.00 &times; 0.86 &times; 1.00 &times; 0.86 &times; 1.00 &times; 0.95 &times; 0.82 &times; 0.91 &times; 1.00 = <b>{eaf:.4f}</b><br><br>

        <b>Cálculo del Esfuerzo Ajustado (PM_ajustado):</b><br>
        &bull; PM_ajustado = EAF &times; PM_nominal = {eaf:.4f} &times; {pm_bas:.4f} = <b>{pm_int:.4f} PM &approx; {pm_int:.2f} Personas-Mes</b> (Reducción de {pm_bas - pm_int:.2f} PM)<br><br>

        <b>Cálculo del Tiempo de Desarrollo Ajustado (TDEV_ajustado):</b><br>
        &bull; Base de esfuerzo: ({pm_int:.2f})<sup>0.35</sup> = <b>{pm_int_pow_d:.4f}</b><br>
        &bull; TDEV_ajustado = 2.50 &times; {pm_int_pow_d:.4f} = <b>{tdev_int:.4f} meses &approx; {tdev_int:.2f} Meses de Calendario</b><br><br>

        <b>Personal Promedio y Costo Valorizado:</b><br>
        &bull; Personal promedio (NP) = {pm_int:.4f} / {tdev_int:.4f} = <b>{np_int:.2f} Personas a tiempo completo</b><br>
        &bull; Productividad ajustada = 22,500 LOC / {pm_int:.2f} PM = <b>{prod_int:.2f} LOC / Persona-Mes</b> (Aumento de {((prod_int/prod_bas)-1)*100:.1f}% en productividad)<br>
        &bull; Costo de Mano de Obra = {pm_int:.4f} PM &times; ${cost_per_pm:,.2f} = <b>{cost_int_str}</b>
    </div>

    <p style="font-size:7.4pt; color:#475569; margin-top:2px;">
        *<b>Análisis sobre el factor SCED:</b> COCOMO 81 estima un plazo nominal de 10.43 meses. Desarrollar el sistema en 4 meses (16 semanas) representaría una compresión severa (~38% del plazo nominal). En las tablas de Boehm (1981), comprimir por debajo del 75% se cataloga como inviable en modelos en cascada. Se mantiene SCED nominal (1.00) en el cálculo principal para aislar el beneficio exclusivo de las herramientas y el equipo; si se aplicara el multiplicador estricto de compresión máxima (SCED = Muy Bajo, 1.23), el EAF subiría a <b>0.7420</b> y el esfuerzo a <b>72.77 PM</b> (~$1,532,482 MXN).
    </p>

    <!-- ================= SECCIÓN 5: TABLA COMPARATIVA ================= -->
    <div class="page-break"></div>
    <h1>5. Tabla Comparativa de las Tres Estimaciones</h1>
    <p>
        A continuación se contrastan formalmente las tres metodologías de estimación aplicadas al proyecto Monchis Café, integrando métricas de ingeniería de software, dimensiones de costo, factores de sensibilidad y aplicabilidad práctica:
    </p>

    <table class="comp-table avoid-break">
        <thead>
            <tr>
                <th style="width: 22%;">Criterio / Dimensión Evaluada</th>
                <th style="width: 26%; text-align: center;">1. Presupuesto Inicial (WBS)</th>
                <th style="width: 26%; text-align: center;">2. COCOMO Básico (Boehm, 1981)</th>
                <th style="width: 26%; text-align: center;">3. COCOMO Intermedio (Boehm, 1981)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>Filosofía y Enfoque</b></td>
                <td>Bottom-Up (Ascendente): Descomposición analítica en tareas, entregables y asignación de horas/recursos (PMI, 2019).</td>
                <td>Paramétrico Macroscópico: Modelo empírico basado exclusivamente en líneas de código (KLOC; Boehm, 1981).</td>
                <td>Paramétrico Calibrado: Modelo empírico modificado por 15 conductores de coste contextuales (EAF; Boehm, 1981).</td>
            </tr>
            <tr>
                <td><b>Variable Primaria de Entrada</b></td>
                <td>Horas por rol técnico, equipamiento de mostrador, nube y reserva de contingencia.</td>
                <td>Tamaño del software en KLOC (22.5 KLOC) y modo de desarrollo (Semiacoplado).</td>
                <td>Tamaño (22.5 KLOC), modo Semiacoplado y vector de 15 multiplicadores EAF = 0.6032.</td>
            </tr>
            <tr>
                <td><b>Esfuerzo Estimado (PM)</b></td>
                <td><b>17.00 Personas-Mes</b><br>(2,720 horas de desarrollo planeadas).</td>
                <td><b>98.08 Personas-Mes</b><br>(Sobreestimación de +476.9% vs WBS).</td>
                <td><b>59.16 Personas-Mes</b><br>(Ahorro del 39.7% frente al básico).</td>
            </tr>
            <tr>
                <td><b>Plazo de Calendario (TDEV)</b></td>
                <td><b>4.00 Meses</b> (16 Semanas / 8 sprints quincenales estructurados).</td>
                <td><b>12.44 Meses</b><br>(~54 semanas de calendario).</td>
                <td><b>10.43 Meses</b><br>(~45 semanas de calendario).</td>
            </tr>
            <tr>
                <td><b>Personal Promedio (NP)</b></td>
                <td><b>4.25 Personas</b> (Equipo planeado: 5 roles técnicos a dedicación parcial/completa).</td>
                <td><b>7.88 Personas</b><br>(Riesgo de sobrecarga comunicativa; Brooks, 1975).</td>
                <td><b>5.67 Personas</b><br>(Equipo mediano estructurado).</td>
            </tr>
            <tr>
                <td><b>Productividad Proyectada</b></td>
                <td><b>1,323.53 LOC / PM</b><br>(Alta productividad con riesgo de optimismo).</td>
                <td><b>229.41 LOC / PM</b><br>(Típica de desarrollo procedimental C/Fortran).</td>
                <td><b>380.30 LOC / PM</b><br>(Incremento del 65.8% vs básico).</td>
            </tr>
            <tr>
                <td><b>Costo Mano de Obra (Labor)</b></td>
                <td><b>$358,000.00 MXN</b> (Tarifas propuestas por el equipo: $112.50 a $175.00 MXN/hr).</td>
                <td><b>{cost_bas_str}</b> (Valorizado a tarifa calculada de $21,058.82 MXN/PM).</td>
                <td><b>{cost_int_str}</b> (Valorizado a tarifa calculada de $21,058.82 MXN/PM).</td>
            </tr>
            <tr>
                <td><b>Costos de Hardware / POS</b></td>
                <td><b>$9,500.00 MXN</b> (Tablet mostrador, impresora térmica y escáner QR).</td>
                <td><b>$0.00</b> (Ignora hardware; solo modela líneas de código).</td>
                <td><b>$0.00</b> (Ignora hardware; solo modela líneas de código).</td>
            </tr>
            <tr>
                <td><b>Infraestructura Cloud / SaaS</b></td>
                <td><b>$12,750.00 MXN</b> (GCP Cloud Run, SQL, RabbitMQ CloudAMQP, SSL, GitHub).</td>
                <td><b>$0.00</b> (Ignora servidores, licencias y costos en la nube).</td>
                <td><b>$0.00</b> (Ignora servidores, licencias y costos en la nube).</td>
            </tr>
            <tr>
                <td><b>Reserva de Contingencia</b></td>
                <td><b>$38,025.00 MXN</b> (Fondo explícito del 10% sobre costos directos).</td>
                <td><b>$0.00</b> (No contempla rubro financiero para imprevistos).</td>
                <td><b>$0.00</b> (No contempla rubro financiero para imprevistos).</td>
            </tr>
            <tr class="highlight-total">
                <td><b>INVERSIÓN TOTAL PROYECTADA</b></td>
                <td><b>$418,275.00 MXN</b><br><span style="font-size:6.9pt; color:#1E40AF;">(Mano de obra, hardware, nube y contingencia)</span></td>
                <td><b>{cost_bas_str}</b><br><span style="font-size:6.9pt; color:#991B1B;">(Solo mano de obra estimada)</span></td>
                <td><b>{cost_int_str}</b><br><span style="font-size:6.9pt; color:#166534;">(Solo mano de obra estimada)</span></td>
            </tr>
            <tr>
                <td><b>Sensibilidad a Tecnología Moderna</b></td>
                <td>Alta: El desglose de horas refleja el uso de TypeScript, ORMs y componentes de UI.</td>
                <td>Nula: Trata una línea de TypeScript igual a una línea de ensamblador o Pascal de 1981.</td>
                <td>Moderada: Modula el impacto mediante MODP (0.82), TOOL (0.91), PCAP (0.86) y ACAP (0.86).</td>
            </tr>
            <tr>
                <td><b>Sensibilidad a Complejidad</b></td>
                <td>Específica por tarea (ej. 480 hrs en pruebas y seguridad; 400 hrs en POS).</td>
                <td>Solo reflejada en el exponente B = 1.12 del modo semiacoplado.</td>
                <td>Ponderada explícitamente en RELY (1.15) y CPLX (1.15), compensada por MODP.</td>
            </tr>
            <tr>
                <td><b>Principales Ventajas</b></td>
                <td>
                    &bull; Control financiero integral.<br>
                    &bull; Incluye hardware, nube y riesgos.<br>
                    &bull; Base contractual para el cliente.
                </td>
                <td>
                    &bull; Rápido de calcular.<br>
                    &bull; Solo requiere estimar KLOC.<br>
                    &bull; Referencia histórica macroscópica.
                </td>
                <td>
                    &bull; Calibra el perfil técnico del equipo.<br>
                    &bull; Premia buenas prácticas modernas.<br>
                    &bull; Reduce drásticamente la sobreestimación.
                </td>
            </tr>
            <tr>
                <td><b>Principales Limitaciones</b></td>
                <td>
                    &bull; Vulnerable a sesgos de optimismo.<br>
                    &bull; Requiere WBS detallado previo.<br>
                    &bull; No provee fórmulas de compresión.
                </td>
                <td>
                    &bull; Sobrestima severamente en web.<br>
                    &bull; Ignora tecnología y herramientas.<br>
                    &bull; Desconectado de presupuestos reales.
                </td>
                <td>
                    &bull; Sigue omitiendo hardware y nube.<br>
                    &bull; Calibrado en proyectos de 1981.<br>
                    &bull; Requiere evaluar 15 coeficientes.
                </td>
            </tr>
        </tbody>
    </table>

    <!-- ================= SECCIÓN 6 ================= -->
    <div class="page-break"></div>
    <h1>6. Análisis Técnico Comparativo y Conclusiones</h1>

    <h2>6.1. Justificación de las Discrepancias entre Modelos (1981 vs. 2026)</h2>
    <p>
        Al contrastar el <b>Presupuesto Inicial ($418,275 MXN | 17 PM)</b> con los modelos <b>COCOMO Básico ({cost_bas_str} | 98.08 PM)</b> e <b>Intermedio ({cost_int_str} | 59.16 PM)</b>, se observa una diferencia considerable: el esfuerzo del modelo básico representa casi seis veces el esfuerzo planeado en el presupuesto (+477%), mientras que el modelo intermedio es casi 3.5 veces el esfuerzo presupuestado (59.16 vs. 17.00 PM, un +248%). Esta divergencia obedece a razones metodológicas y tecnológicas claras:
    </p>
    <ul>
        <li><b>La Base Empírica de COCOMO 81:</b> Barry Boehm calibró el modelo original en 1981 a partir de 63 proyectos tradicionales desarrollados en FORTRAN, COBOL y ensamblador (Boehm, 1981). En esa época, programar 22.5 KLOC exigía escribir desde cero drivers de comunicación, interfaces de usuario en modo texto y persistencia manual, lo que explica las 98 personas-mes.</li>
        <li><b>El Apalancamiento del Ecosistema Moderno:</b> En Monchis Café, una línea de código en TypeScript moderno posee una densidad funcional mucho mayor: se utilizan componentes reactivos de Vue 3, esquemas automáticos con Prisma ORM y servicios en la nube. Esto permite proyectar una productividad de 1,323 LOC/PM en 16 semanas. Sin embargo, esta alta productividad asume un flujo continuo sin bloqueos mayores; si surgen imprevistos en la integración de periféricos o el código crece, el cronograma corre el riesgo de desfasarse.</li>
        <li><b>El Ajuste de COCOMO Intermedio (EAF = 0.6032):</b> Al aplicar los 15 conductores, el esfuerzo baja de 98 a 59 personas-mes. Lo que más influye en esa reducción son las prácticas modernas (<code>MODP = 0.82</code>) y la capacidad del equipo (<code>ACAP = 0.86</code> y <code>PCAP = 0.86</code>). Aun así, el resultado sigue triplicando el presupuesto inicial, y los 10.4 meses estimados quedan lejos de las 16 semanas que planeamos.</li>
    </ul>

    <h2>6.2. Conclusión: ¿Cuál Método es Más Adecuado para el Proyecto?</h2>
    
    <div class="callout avoid-break" style="padding: 5px 8px; margin: 4px 0;">
        <div class="callout-title">Recomendación y Selección Metodológica</div>
        Para el desarrollo y gestión de <b>Monchis Café</b>, se concluye técnicamente que:
        <ol style="margin-bottom: 2px; padding-left: 15px;">
            <li><b>El Presupuesto Inicial (WBS / Bottom-Up) es el Método Más Adecuado para la Viabilidad Financiera y Contractual:</b><br>
            Es el único de los tres métodos que proporciona una visión integral del negocio: incluye los $9,500 MXN de hardware POS sin los cuales la cafetería no puede cobrar ni operar en mostrador, los $12,750 MXN de infraestructura Cloud para alojar la base de datos y RabbitMQ, y el fondo de reserva del 10% ($38,025 MXN) para contingencias. Los modelos COCOMO no contemplan estos costos directos, pues están formulados únicamente para estimar el esfuerzo de desarrollo.</li>
            <li><b>COCOMO Intermedio es un Marco de Referencia Paramétrico Superior al Básico, pero Requiere Calibración Moderna:</b><br>
            COCOMO Intermedio supera al básico porque modula el esfuerzo en función del perfil técnico y las herramientas. No obstante, no debe tomarse como un presupuesto vinculante para el cliente, sino como un modelo de contraste macroscópico que alerta al equipo sobre el riesgo de sobrecarga comunicativa (Brooks, 1975) si se pretende resolver un retraso sumando desarrolladores al final. Para proyectos contemporáneos, la disciplina recurre a evoluciones como <b>COCOMO II</b> (Boehm et al., 2000), diseñado para desarrollo moderno basado en componentes y reutilización de software.</li>
        </ol>
    </div>

    <h2>6.3. Reflexión Personal sobre el Proceso de Estimación</h2>
    <p>
        Durante la elaboración de esta actividad, se tomaron decisiones de estimación basadas en el contexto del proyecto y la consulta de mercado:
    </p>
    <ul style="margin-bottom: 4px; padding-left: 15px;">
        <li><b>Definición de Tarifas Horarias:</b> Para determinar las tarifas horarias ($112.50 a $175.00 MXN/hr, promedio $131.62 MXN/hr o ~$21,058.82 MXN/PM), revisamos vacantes recientes en portales de empleo de tecnología para desarrolladores junior e independientes en la Zona Metropolitana de Guadalajara (como Computrabajo y Glassdoor en 2026), ajustándolas a esquemas de contratación por honorarios para proyectos de microempresas.</li>
        <li><b>Módulos de Mayor Incertidumbre:</b> Lo que más costó dimensionar fue la orquestación distribuida del Patrón Saga con RabbitMQ y la sincronización con los periféricos locales del mostrador (impresora térmica de tickets y escáner QR). Es fácil estimar un formulario web estándar, pero coordinar colas asíncronas de cobro y contingencias de desconexión en barra física introduce incertidumbres difíciles de prever solo con líneas de código.</li>
        <li><b>Aprendizaje Principal:</b> Lo que más me llamó la atención al comparar los tres métodos fue la brecha abismal con COCOMO Básico (~100 personas-mes frente a 17 en el plan). Esto evidencia cuánto ha evolucionado la productividad con los frameworks web modernos. Sin embargo, ver que COCOMO Intermedio aún arroja 10 meses y casi 6 personas me hizo ver que nuestro plan de 16 semanas con 1,323 LOC/PM es muy exigente: la WBS es indispensable para cotizar con el cliente, pero los modelos paramétricos son una alerta necesaria contra el exceso de optimismo en los tiempos de entrega.</li>
    </ul>

    <!-- ================= SECCIÓN 7: REFERENCIAS ================= -->
    <div class="avoid-break" style="margin-top: 5px;">
        <h1 style="margin: 6px 0 3px 0;">7. Referencias Bibliográficas (Normas APA 7)</h1>
        <ul style="font-size: 7.1pt; line-height: 1.30; color: #475569; margin-bottom: 0; padding-left: 15px;">
            <li>Boehm, B. W. (1981). <i>Software engineering economics</i>. Prentice-Hall.</li>
            <li>Boehm, B., Abts, C., Brown, A. W., Chulani, S., Clark, B. K., Horowitz, E., Madachy, R., Reifer, D., & Steece, B. (2000). <i>Software cost estimation with COCOMO II</i>. Prentice Hall.</li>
            <li>Brooks, F. P. (1975). <i>The mythical man-month: Essays on software engineering</i>. Addison-Wesley.</li>
            <li>Navarro Salcedo, G. (2026). <i>Material de apoyo y notas de cátedra sobre los modelos COCOMO básico e intermedio</i> [Material didáctico de clase]. Departamento de Ciencias Computacionales, Universidad de Guadalajara.</li>
            <li>Pressman, R. S., & Maxim, B. R. (2020). <i>Software engineering: A practitioner's approach</i> (9.ª ed.). McGraw-Hill Education.</li>
            <li>Project Management Institute. (2019). <i>Practice standard for work breakdown structures</i> (3.ª ed.). Project Management Institute.</li>
            <li>Smartsheet Inc. (2023). <i>Plantilla de propuesta de presupuesto de proyectos</i> [Plantilla de hoja de cálculo]. Smartsheet. https://es.smartsheet.com/content/project-budget-templates</li>
        </ul>
    </div>

</body>
</html>
"""

    html_path = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_2_3_Tabla_Comparativa_Estimacion_MonchisCafe.html"
    pdf_path = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_2_3_Tabla_Comparativa_Estimacion_MonchisCafe.pdf"
    downloads_pdf = r"C:\Users\erfierro\Downloads\Actividad_2_3_Tabla_Comparativa_Estimacion_MonchisCafe.pdf"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML generado exitosamente en: {html_path}")

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]

    print("Compilando a PDF con Google Chrome Headless...")
    subprocess.run(cmd, check=True)

    if os.path.exists(pdf_path):
        size = os.path.getsize(pdf_path)
        print(f"PDF generado exitosamente en: {pdf_path} ({size:,} bytes)")
        shutil.copy2(pdf_path, downloads_pdf)
        print(f"Copia creada exitosamente en Downloads: {downloads_pdf}")
    else:
        print("Error: No se pudo generar el archivo PDF.")

if __name__ == "__main__":
    generate_activity_2_3_deliverable()
