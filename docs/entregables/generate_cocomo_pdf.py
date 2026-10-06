import os
import subprocess
import shutil

def generate_improved_deliverables():
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Actividad 2.1 - Modelo COCOMO Básico - Salud Integral</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

        @page {
            size: letter;
            margin: 12mm 14mm 12mm 14mm;
            @top-right {
                content: "Ingeniería de Software · Modelo COCOMO Básico";
                font-family: 'Inter', sans-serif;
                font-size: 7.5pt;
                color: #64748B;
            }
            @bottom-left {
                content: "Clínica Universitaria 'Salud Integral' · Ernesto Fierro";
                font-family: 'Inter', sans-serif;
                font-size: 7.5pt;
                color: #64748B;
            }
            @bottom-right {
                content: "Página " counter(page);
                font-family: 'Inter', sans-serif;
                font-size: 7.5pt;
                font-weight: 700;
                color: #1E293B;
            }
        }

        @page:first {
            @top-right { content: none; }
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 8.5pt;
            line-height: 1.39;
            color: #1E293B;
            background-color: #FFFFFF;
            margin: 0;
            padding: 0;
            text-align: justify;
        }

        .avoid-break {
            break-inside: avoid;
            page-break-inside: avoid;
        }

        /* --- ENCABEZADO Y PORTADA --- */
        .header-badge-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
        }

        .badge-academic {
            background: linear-gradient(135deg, #1B365D, #0F172A);
            color: #FFFFFF;
            font-size: 7.5pt;
            font-weight: 700;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            padding: 3px 10px;
            border-radius: 4px;
        }

        .date-badge {
            font-size: 7.8pt;
            font-weight: 600;
            color: #64748B;
        }

        .doc-title {
            font-size: 15.5pt;
            font-weight: 800;
            line-height: 1.15;
            color: #0F172A;
            margin: 0 0 3px 0;
            letter-spacing: -0.3px;
        }

        .doc-subtitle {
            font-size: 9.8pt;
            font-weight: 600;
            color: #008080;
            margin: 0 0 7px 0;
        }

        .header-line {
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, #1B365D 0%, #008080 50%, #0EA5E9 100%);
            border-radius: 2px;
            margin-bottom: 8px;
        }

        /* METADATOS COMPACTOS */
        .meta-card {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-left: 4px solid #1B365D;
            border-radius: 4px;
            padding: 6px 10px;
            margin-bottom: 8px;
            display: grid;
            grid-template-columns: 1.2fr 1fr;
            gap: 3px 14px;
            font-size: 8.2pt;
            break-inside: avoid;
            page-break-inside: avoid;
        }

        .meta-item {
            display: flex;
        }
        .meta-item strong {
            width: 105px;
            color: #334155;
            font-weight: 700;
        }
        .meta-item span {
            color: #0F172A;
        }

        /* ENCABEZADOS DE SECCIÓN */
        h1 {
            color: #0F172A;
            font-size: 10.4pt;
            font-weight: 800;
            border-bottom: 1.5px solid #CBD5E1;
            padding-bottom: 2px;
            margin-top: 9px;
            margin-bottom: 5px;
            letter-spacing: -0.2px;
            text-transform: uppercase;
            page-break-after: avoid;
            break-after: avoid;
        }

        h2 {
            color: #1B365D;
            font-size: 9.2pt;
            font-weight: 700;
            margin-top: 7px;
            margin-bottom: 3px;
            page-break-after: avoid;
            break-after: avoid;
        }

        p {
            margin-top: 0;
            margin-bottom: 5px;
        }

        ul, ol {
            margin-top: 2px;
            margin-bottom: 5px;
            padding-left: 17px;
        }

        li {
            margin-bottom: 2.5px;
        }

        b, strong {
            font-weight: 700;
            color: #0F172A;
        }

        /* RECUADROS CALLOUT */
        .callout {
            border: 1px solid #E2E8F0;
            border-radius: 4px;
            padding: 6px 9px;
            margin: 5px 0;
            font-size: 8.3pt;
            break-inside: avoid;
            page-break-inside: avoid;
        }

        .callout-title {
            font-weight: 800;
            font-size: 8.5pt;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            margin-bottom: 3px;
        }

        .callout-primary {
            background-color: #F8FAFC;
            border-left: 4px solid #1B365D;
        }
        .callout-primary .callout-title { color: #1B365D; }

        .callout-success {
            background-color: #F0FDF4;
            border-color: #BBF7D0;
            border-left: 4px solid #16A34A;
        }
        .callout-success .callout-title { color: #166534; }

        .callout-warning {
            background-color: #FEF2F2;
            border-color: #FECACA;
            border-left: 4px solid #DC2626;
        }
        .callout-warning .callout-title { color: #991B1B; }

        .callout-info {
            background-color: #F0F9FF;
            border-color: #BAE6FD;
            border-left: 4px solid #0284C7;
        }
        .callout-info .callout-title { color: #0369A1; }

        /* FÓRMULAS MATEMÁTICAS */
        .formula-box {
            background-color: #F1F5F9;
            border: 1px solid #CBD5E1;
            border-radius: 4px;
            padding: 5px 9px;
            margin: 4px 0;
            font-family: 'JetBrains Mono', monospace;
            font-size: 8.1pt;
            line-height: 1.45;
            color: #0F172A;
            break-inside: avoid;
            page-break-inside: avoid;
        }

        .formula-highlight {
            font-weight: 700;
            color: #1B365D;
            background: #E2E8F0;
            padding: 1px 4px;
            border-radius: 3px;
        }

        /* TABLAS ESTILIZADAS */
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 8pt;
            margin: 5px 0;
            break-inside: avoid;
            page-break-inside: avoid;
        }

        th {
            background-color: #1B365D;
            color: #FFFFFF;
            font-weight: 700;
            text-align: center;
            padding: 4px 6px;
            border: 1px solid #CBD5E1;
        }

        td {
            padding: 3.5px 6px;
            border: 1px solid #CBD5E1;
            vertical-align: middle;
        }

        tr:nth-child(even) td {
            background-color: #F8FAFC;
        }

        .highlight-row td {
            background-color: #EBF3FA !important;
            font-weight: 600;
            color: #1B365D;
        }

        .text-center { text-align: center; }
        .text-right { text-align: right; }
        .text-left { text-align: left; }

        .tag-status {
            display: inline-block;
            padding: 1px 5px;
            border-radius: 3px;
            font-size: 7pt;
            font-weight: 700;
            text-transform: uppercase;
        }
        .tag-success { background-color: #DCFCE7; color: #166534; }
        .tag-warning { background-color: #FEF3C7; color: #92400E; }
        .tag-danger { background-color: #FEE2E2; color: #991B1B; }

    </style>
</head>
<body>

    <!-- ================= SECCIÓN 1 ================= -->
    <div class="header-badge-row">
        <span class="badge-academic">Ingeniería de Software · Actividad 2.1</span>
        <span class="date-badge">29 de Septiembre de 2026</span>
    </div>
    <h1 class="doc-title">MODELO COCOMO BÁSICO</h1>
    <div class="doc-subtitle">Estimación de Esfuerzo, Tiempo de Desarrollo y Personal para el Sistema "Salud Integral"</div>
    <div class="header-line"></div>

    <div class="meta-card">
        <div class="meta-item"><strong>Materia:</strong> <span>Administración de Proyectos / Ing. de Software</span></div>
        <div class="meta-item"><strong>Estudiante:</strong> <span>Ernesto Fierro</span></div>
        <div class="meta-item"><strong>Docente:</strong> <span>Dr. Gabriel Navarro Salcedo</span></div>
        <div class="meta-item"><strong>Ponderación:</strong> <span>2 Puntos (2 % de la Evaluación Total)</span></div>
    </div>

    <div class="callout callout-info">
        <div class="callout-title">Resumen Ejecutivo de Resultados del Caso Asignado</div>
        Para el desarrollo del sistema web de la <b>Clínica Universitaria "Salud Integral"</b> (estimado en <b>18 KLOC</b>, desarrollado por un equipo universitario con <b>experiencia media</b> bajo el modo Semiacoplado/Medio), el modelo COCOMO Básico proyecta un <b>esfuerzo de 76.39 persona-mes</b>, una duración óptima de <b>11.40 meses</b> y un equipo de <b>6 a 7 desarrolladores a tiempo completo</b>. Si el cliente pretendiera comprimir la entrega a <b>3 meses</b> (como en el ejemplo pedagógico de clase), se requeriría teóricamente un equipo de <b>26 programadores</b>; no obstante, esto resulta <b>técnicamente inviable</b> debido a la <b>Falacia del Hombre-Mes</b> y la sobrecarga comunicativa cuadrática (los canales crecen un 1,328% de 21 a 325) y porque se transgrede el límite de compresión de Boehm (zona imposible). Se fundamenta matemáticamente una estrategia ágil por fases con un MVP en 3 meses (~3.5 KLOC con 4 desarrolladores).
    </div>

    <h1>1. Análisis del Caso de Estudio: Clínica Universitaria "Salud Integral"</h1>
    <p>
        La Clínica Universitaria "Salud Integral" atiende consultas de medicina general y diversas especialidades médicas. En la actualidad, su gestión descansa enteramente en hojas de cálculo (Excel) y expedientes físicos en papel. Dicha dinámica genera tiempos excesivos de espera para los pacientes, ausentismo (<i>no-show</i>) no controlado, desorganización en los expedientes y dificultades graves para generar reportes clínicos y estadísticos.
    </p>
    <p>
        Ante esta situación, la dirección institucional requiere el desarrollo y despliegue de una <b>aplicación web centralizada</b> con diseño responsivo (accesible desde computadoras de escritorio y tablets) para automatizar la operación integral de la clínica.
    </p>

    <h2>1.1. Alcance Técnico, Dimensionamiento y Restricciones</h2>
    <ul>
        <li><b>Módulos Funcionales (7 módulos):</b> Pacientes, Citas Médicas, Expediente Clínico Básico, Usuarios y Roles, Reportes Mensuales, Importación de Datos y Notificaciones Automáticas.</li>
        <li><b>Volumen de Interfaces:</b> Aproximadamente 20 pantallas y formularios operativos.</li>
        <li><b>Modelo de Datos:</b> 10 entidades estructurales relacionales (<i>Paciente, Médico, Especialidad, Cita, NotaConsulta, SignosVitales, Receta, Usuario, Rol, ArchivoAdjunto</i>).</li>
        <li><b>Integración Externa:</b> Consumo de una API REST universitaria preexistente para envío masivo de correos y mensajes SMS de recordatorio.</li>
        <li><b>Migración de Datos Históricos:</b> Script de extracción, saneamiento básico y carga (ETL) de 2,000 registros heredados desde archivos Excel.</li>
        <li><b>Perfil del Equipo:</b> El caso estipula explícitamente: <i>"se asume un equipo de desarrollo universitario con experiencia media"</i>.</li>
    </ul>

    <h2>1.2. Parámetros de Tamaño del Software (KLOC)</h2>
    <ul>
        <li><b>Código Nuevo Total:</b> 18,000 líneas de código fuente (<b>18 KLOC</b>), estimadas por el coordinador técnico con base en proyectos precedentes.</li>
        <li><b>Reutilización de Código:</b> 0% (se asume código 100% nuevo conforme a las premisas del caso).</li>
        <li><b>Lenguaje de Programación:</b> No condicionado; en COCOMO Básico la variable explicativa es el total de KLOC.</li>
    </ul>

    <!-- ================= SECCIÓN 2 ================= -->
    <h1>2. Formulación Matemática del Modelo COCOMO Básico</h1>
    <p>
        El <b>Modelo Constructivo de Costos (COCOMO)</b> en su versión básica (Boehm, 1981) relaciona el tamaño del código fuente en miles de líneas (KLOC) con el esfuerzo y tiempo mediante ecuaciones de potencia ajustadas empíricamente:
    </p>

    <div class="callout callout-primary">
        <div class="callout-title">Ecuaciones del Modelo COCOMO Básico (Presentación de la Cátedra)</div>
        <div class="formula-box">
            <div><b>1. Esfuerzo Aplicado (Personas-Mes):</b> <span class="formula-highlight">PM = A · (KLOC)<sup>B</sup></span></div>
            <div><b>2. Tiempo de Desarrollo (Meses de Calendario):</b> <span class="formula-highlight">TDEV = C · (PM)<sup>D</sup></span> <i>(notado como TDVE en las diapositivas de clase)</i></div>
            <div><b>3. Número de Personas Necesarias:</b> <span class="formula-highlight">NP = PM / TDEV</span></div>
        </div>
    </div>

    <h2>2.1. Coeficientes Oficiales de Calibración COCOMO</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 32%;">Tipo de Proyecto</th>
                <th style="width: 17%;">A</th>
                <th style="width: 17%;">B</th>
                <th style="width: 17%;">C</th>
                <th style="width: 17%;">D</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>Orgánico</b></td>
                <td class="text-center">2.40</td>
                <td class="text-center">1.05</td>
                <td class="text-center">2.50</td>
                <td class="text-center">0.38</td>
            </tr>
            <tr class="highlight-row">
                <td><b>Medio (Semiacoplado) [Caso Asignado]</b></td>
                <td class="text-center"><b>3.00</b></td>
                <td class="text-center"><b>1.12</b></td>
                <td class="text-center"><b>2.50</b></td>
                <td class="text-center"><b>0.35</b></td>
            </tr>
            <tr>
                <td><b>Embebido</b></td>
                <td class="text-center">3.60</td>
                <td class="text-center">1.20</td>
                <td class="text-center">2.50</td>
                <td class="text-center">0.32</td>
            </tr>
        </tbody>
    </table>

    <h2>2.2. Justificación Técnica del Modo de Desarrollo Seleccionado</h2>
    <p>
        La clasificación correcta del proyecto corresponde con rigor al <b>Modo Medio (Semiacoplado)</b> debido a:
    </p>
    <ul>
        <li><b>Experiencia del Equipo:</b> El caso indica de forma literal <i>"se asume un equipo de desarrollo universitario con experiencia media"</i>. En la taxonomía formal de Boehm, los proyectos desarrollados por equipos con experiencia mixta o intermedia pertenecen inequívocamente al modo Semiacoplado.</li>
        <li><b>Complejidad de Integraciones y Migración:</b> La interacción con una API universitaria externa para recordatorios y la migración de 2,000 registros de Excel con 10 entidades y 20 interfaces implican un nivel de restricciones superior al de un sistema orgánico básico aislado.</li>
    </ul>
    <p style="font-size: 8.1pt; color: #475569;">
        <i>Nota metodológica: Se presenta adicionalmente el Modo Orgánico como un análisis de sensibilidad comparativo frente a un escenario hipotético de máxima estabilidad y autonomía técnica.</i>
    </p>

    <!-- ================= SECCIÓN 3 ================= -->
    <h1>3. Desarrollo y Cálculo Matemático Paso a Paso</h1>

    <h2>3.1. Caso Principal: Modo Medio / Semiacoplado (A = 3.00, B = 1.12, C = 2.50, D = 0.35 | KLOC = 18)</h2>
    <div class="callout callout-success">
        <div class="callout-title">Cálculo Detallado - Modo Medio</div>
        <div class="formula-box">
            <div><b>Paso 1: Cálculo del Esfuerzo (PM)</b></div>
            <div>&nbsp;&nbsp;PM = 3.00 · (18)<sup>1.12</sup></div>
            <div>&nbsp;&nbsp;18<sup>1.12</sup> = e<sup>(1.12 · ln(18))</sup> = e<sup>(1.12 · 2.89037)</sup> = e<sup>3.23722</sup> ≈ <b>25.4627</b></div>
            <div>&nbsp;&nbsp;PM = 3.00 · 25.4627 = <span class="formula-highlight">76.3882 ≈ 76.39 Personas-Mes</span></div>
            <div style="margin-top: 3px;"><b>Paso 2: Cálculo del Tiempo de Desarrollo Estimado (TDEV)</b></div>
            <div>&nbsp;&nbsp;TDEV = 2.50 · (76.3882)<sup>0.35</sup></div>
            <div>&nbsp;&nbsp;(76.3882)<sup>0.35</sup> = e<sup>(0.35 · ln(76.3882))</sup> = e<sup>(0.35 · 4.33583)</sup> = e<sup>1.51754</sup> ≈ <b>4.5610</b></div>
            <div>&nbsp;&nbsp;TDEV = 2.50 · 4.5610 = <span class="formula-highlight">11.4025 ≈ 11.40 Meses</span></div>
            <div style="margin-top: 3px;"><b>Paso 3: Cálculo del Número Óptimo de Personas (NP)</b></div>
            <div>&nbsp;&nbsp;NP = PM / TDEV = 76.3882 / 11.4025 = <span class="formula-highlight">6.6993 ≈ 6.70 Desarrolladores</span></div>
            <div>&nbsp;&nbsp;<b>Equipo Óptimo Recomendado:</b> <b>6 a 7 desarrolladores</b> a tiempo completo (redondeo operativo a <b>7 personas</b>).</div>
        </div>
    </div>

    <h2>3.2. Escenario Comparativo: Modo Orgánico (A = 2.40, B = 1.05, C = 2.50, D = 0.38 | KLOC = 18)</h2>
    <div class="callout callout-info">
        <div class="callout-title">Cálculo Detallado - Modo Orgánico (Análisis de Sensibilidad)</div>
        <div class="formula-box">
            <div>• <b>PM:</b> 2.40 · (18)<sup>1.05</sup> = 2.40 · 20.7987 = <span class="formula-highlight">49.9169 ≈ 49.92 Personas-Mes</span></div>
            <div>• <b>TDEV:</b> 2.50 · (49.9169)<sup>0.38</sup> = 2.50 · 4.4191 = <span class="formula-highlight">11.0478 ≈ 11.05 Meses</span></div>
            <div>• <b>NP:</b> 49.9169 / 11.0478 = <span class="formula-highlight">4.5183 ≈ 4.52 Desarrolladores</span> (Equipo óptimo: <b>4 a 5 desarrolladores</b>).</div>
        </div>
    </div>

    <h2>3.3. Matriz Resumen de Resultados COCOMO</h2>
    <table>
        <thead>
            <tr>
                <th>Modo de Proyecto</th>
                <th>Tamaño</th>
                <th>Esfuerzo (PM)</th>
                <th>Tiempo (TDEV)</th>
                <th>Personal (NP)</th>
                <th>Equipo Recomendado</th>
            </tr>
        </thead>
        <tbody>
            <tr class="highlight-row">
                <td><b>Medio (Semiacoplado) [Caso Base]</b></td>
                <td class="text-center">18 KLOC</td>
                <td class="text-center"><b>76.39 PM</b></td>
                <td class="text-center"><b>11.40 Meses</b></td>
                <td class="text-center"><b>6.70</b></td>
                <td class="text-center"><b>6 a 7 Desarrolladores</b></td>
            </tr>
            <tr>
                <td><b>Orgánico [Comparativo]</b></td>
                <td class="text-center">18 KLOC</td>
                <td class="text-center">49.92 PM</td>
                <td class="text-center">11.05 Meses</td>
                <td class="text-center">4.52</td>
                <td class="text-center">4 a 5 Desarrolladores</td>
            </tr>
        </tbody>
    </table>

    <!-- ================= SECCIÓN 4 ================= -->
    <h1>4. Interpretación Técnica de Viabilidad Respecto al Tiempo del Cliente</h1>
    <p>
        Siguiendo fielmente la estructura del ejemplo de la empresa COTECNO proporcionado en las instrucciones de la actividad, se realiza el análisis de viabilidad técnica contrastando la duración nominal empírica arrojada por COCOMO (<b>11.40 meses</b>) frente a los requerimientos temporales habituales de clientes y directivos:
    </p>

    <h2>4.1. Escenario A: Entrega Solicitada en 3 Meses (Directamente Análogo al Ejemplo Docente)</h2>
    <p>
        Si la dirección de la Clínica Universitaria "Salud Integral" solicita la entrega total en un plazo de <b>3 meses</b>:
    </p>
    <ul>
        <li><b>Personal requerido (Modo Medio):</b> NP = PM / Plazo = 76.39 / 3 = <b>25.46 desarrolladores</b>. Para cubrir la totalidad del esfuerzo sin déficit de horas (25 × 3 = 75 PM < 76.39 PM), se requieren matemáticamente <b>26 desarrolladores a tiempo completo</b> (26 × 3 = 78 PM).</li>
        <li><b>Personal requerido (Modo Orgánico):</b> NP = PM / Plazo = 49.92 / 3 = <b>16.64 desarrolladores</b> (~<b>17 desarrolladores</b> a tiempo completo).</li>
        <li><b>Evaluación de Viabilidad Técnica:</b> <span class="tag-status tag-danger">TÉCNICAMENTE INVIABLE</span>. De acuerdo con los postulados empíricos de Boehm, no es posible comprimir un cronograma de desarrollo de software a menos del <b>75% de su tiempo nominal</b>. Comprimir a 3 meses equivale a forzarlo al <b>26.3%</b> del tiempo nominal (una reducción del 73.7%), lo que sitúa al proyecto de lleno en la "Zona Imposible" y conduce al colapso organizacional.</li>
    </ul>

    <h2>4.2. Escenario B: Entrega Semestral Universitaria en 6 Meses</h2>
    <p>
        Si el cliente plantea ajustar la entrega a la conclusión de un ciclo escolar o semestre universitario (<b>6 meses</b>):
    </p>
    <ul>
        <li><b>Personal requerido (Modo Medio):</b> NP = PM / Plazo = 76.39 / 6 = <b>12.73 desarrolladores</b> (~<b>13 desarrolladores</b> a tiempo completo).</li>
        <li><b>Evaluación de Viabilidad Técnica:</b> <span class="tag-status tag-danger">INVIABLE BAJO ALCANCE TOTAL (ZONA IMPOSIBLE)</span>. Seis meses representa una compresión al <b>52.6%</b> del tiempo nominal (11.40 meses), manteniéndose significativamente por debajo del umbral mínimo del 75% (8.55 meses). Intentar entregar el 100% del alcance en 6 meses duplicando la plantilla (de 7 a 13) es inviable según COCOMO, a menos que se aplique una reducción formal del alcance del software.</li>
    </ul>

    <h2>4.3. Análisis Financiero de Honorarios Salariales del Equipo</h2>
    <p>
        Tomando exactamente como referencia el costo mensual promedio de <b>$10,100.00 MXN</b> por desarrollador estipulado en el ejemplo de la actividad, se proyecta la nómina salarial para cada alternativa:
    </p>

    <table>
        <thead>
            <tr>
                <th>Escenario de Plazo</th>
                <th>Desarrolladores</th>
                <th>Duración</th>
                <th>Costo Mensual</th>
                <th>Total Honorarios (MXN)</th>
                <th>Factibilidad Técnica</th>
            </tr>
        </thead>
        <tbody>
            <tr class="highlight-row">
                <td><b>Nominal Óptimo COCOMO</b></td>
                <td class="text-center">7 desarrolladores</td>
                <td class="text-center">11.40 Meses</td>
                <td class="text-right">$70,700.00</td>
                <td class="text-right"><b>$805,980.00 MXN</b></td>
                <td class="text-center"><span class="tag-status tag-success">Óptimo</span></td>
            </tr>
            <tr>
                <td><b>Semestre Universitario</b></td>
                <td class="text-center">13 desarrolladores</td>
                <td class="text-center">6.00 Meses</td>
                <td class="text-right">$131,300.00</td>
                <td class="text-right"><b>$787,800.00 MXN</b></td>
                <td class="text-center"><span class="tag-status tag-danger">Zona Imposible</span></td>
            </tr>
            <tr>
                <td><b>Acelerado (3 Meses - Ejemplo)</b></td>
                <td class="text-center">26 desarrolladores</td>
                <td class="text-center">3.00 Meses</td>
                <td class="text-right">$262,600.00</td>
                <td class="text-right"><b>$787,800.00 MXN</b></td>
                <td class="text-center"><span class="tag-status tag-danger">Inviable Total</span></td>
            </tr>
        </tbody>
    </table>
    <p style="font-size: 8pt; color: #475569;">
        <i>Nota analítica:</i> El costo laboral nominal estricto derivado de COCOMO es de 76.39 PM × $10,100 = <b>$771,538.82 MXN</b>. Las ligeras variaciones en los totales de la tabla obedecen al redondeo a números enteros discretos de personal (26 personas en 3 meses = $787,800 MXN; 7 personas en 11.4 meses = $805,980 MXN). Cualitativamente, pagar a 26 desarrolladores en un plazo tan comprimido genera un desperdicio económico severo, pues la mayor parte del tiempo pagado se consume en fricciones de coordinación y retrabajo.
    </p>

    <!-- ================= SECCIÓN 5 ================= -->
    <h1>5. Reflexión Técnica: ¿Cómo Cambia el Proyecto al Modificar el Personal?</h1>
    <p>
        Existe una creencia equivocada en clientes no técnicos que asume que el esfuerzo (Personas-Mes) se puede fraccionar arbitrariamente dividiendo entre el número de desarrolladores (la falacia del "Hombre-Mes"). La ingeniería de software demuestra que alterar el número de desarrolladores transforma drásticamente la dinámica del proyecto por las siguientes causas:
    </p>

    <h2>5.1. El Mito del Hombre-Mes y el Crecimiento Cuadrático de Canales de Comunicación</h2>
    <p>
        Frederick Brooks (1975) demostró que las personas y los meses no son magnitudes intercambiables: asignar 26 desarrolladores no reduce proporcionalmente el tiempo. Los canales de comunicación bilateral crecen de forma estrictamente <b>cuadrática</b> mediante la fórmula combinatoria:
    </p>

    <div class="callout callout-warning">
        <div class="callout-title">Crecimiento Cuadrático de Canales de Comunicación: C = [ N · (N - 1) ] / 2</div>
        <div class="formula-box">
            <div>• <b>Equipo Nominal (N = 7):</b> C = (7 · 6) / 2 = <span class="formula-highlight">21 canales</span> de comunicación.</div>
            <div>• <b>Equipo Semestral (N = 13):</b> C = (13 · 12) / 2 = <span class="formula-highlight">78 canales (+271%)</span>.</div>
            <div>• <b>Equipo Forzado a 3 Meses (N = 26):</b> C = (26 · 25) / 2 = <span class="formula-highlight">325 canales (+1,448%)</span> <i>(o 300 canales para N = 25)</i>.</div>
        </div>
        <div style="font-size: 8.1pt; color: #991B1B; margin-top: 3px;">
            Al saltar de 21 a 325 canales, la jornada laboral se satura en reuniones de sincronización, resolución de conflictos de integración en Git y debates arquitectónicos. Si el proyecto empieza a demorarse e intentan sumar más personal, se activa la temida <b>Ley de Brooks</b>: <i>"Añadir personal a un proyecto de software retrasado solo lo retrasa más"</i>.
        </div>
    </div>

    <h2>5.2. Curva de Aprendizaje y Costo de Onboarding en Equipos Universitarios</h2>
    <p>
        El caso señala que el equipo tiene <b>"experiencia media"</b>. De acuerdo con la literatura de ingeniería de software sobre asimilación técnica (Pressman & Maxim, 2020; Sommerville, 2016), en proyectos urgentes con equipos no sénior, el periodo de inducción y acoplamiento (<i>ramp-up</i>) consume entre el 30% y el 50% de la ventana temporal disponible:
    </p>
    <ul>
        <li>Los desarrolladores más capacitados que diseñaron la base de datos relacional y la seguridad RBAC deben detener su trabajo de programación para capacitar y supervisar a los nuevos integrantes.</li>
        <li>La productividad grupal sufre una caída inmediata (el denominado <i>valle de productividad</i> o curva en J).</li>
    </ul>

    <h2>5.3. El Límite Infranqueable de Compresión (The Impossible Region de Boehm)</h2>
    <p>
        Los estudios empíricos de Boehm demostraron que ningún proyecto de software puede comprimirse a menos del <b>75% del tiempo nominal de desarrollo</b> (<i>TDEV<sub>mín</sub> ≈ 0.75 · TDEV</i>), sin importar los recursos que se inyecten:
    </p>
    <ul>
        <li><b>Límite mínimo de compresión para Modo Medio:</b> TDEV<sub>mín</sub> = 0.75 · 11.40 Meses = <b>8.55 Meses</b>.</li>
        <li><b>Límite mínimo de compresión para Modo Orgánico:</b> TDEV<sub>mín</sub> = 0.75 · 11.05 Meses = <b>8.29 Meses</b>.</li>
    </ul>
    <p>
        Cualquier intento de forzar la entrega en 3 o 6 meses traspasa la frontera hacia la "Zona Imposible", produciendo sistemas con código frágil, pruebas omitidas y graves riesgos de seguridad en el manejo de expedientes clínicos.
    </p>

    <h2>5.4. Dependencias Secuenciales y Ley de Amdahl</h2>
    <p>
        El software posee dependencias de precedencia ineludibles: no es posible paralelizar el desarrollo de las 20 pantallas si el esquema de base de datos de las 10 entidades no está normalizado y probado; y no se puede implementar el expediente clínico sin tener antes la autenticación y el registro de pacientes. Como establece la <b>Ley de Amdahl</b>, la velocidad de ejecución está limitada por la fracción estrictamente secuencial de las tareas.
    </p>

    <!-- ================= SECCIÓN 6 ================= -->
    <h1>6. Conclusiones Técnicas y Recomendaciones de Gestión</h1>
    <ol style="margin-bottom: 6px;">
        <li>
            <b>Validez del Modelo Cuantitativo:</b> Para un tamaño de 18 KLOC con un equipo universitario de experiencia media, el modelo COCOMO Básico proyecta de forma certera un esfuerzo de <b>76.39 persona-mes</b>, una duración óptima de <b>11.40 meses</b> y una dotación de <b>6 a 7 desarrolladores</b> a tiempo completo.
        </li>
        <li>
            <b>Rechazo al Enfoque de Fuerza Bruta:</b> Aceptar una entrega en 3 meses contratando a 26 desarrolladores es un error metodológico crítico. La sobrecarga cuadrática de 325 canales de comunicación y la curva de aprendizaje paralizarán el avance.
        </li>
        <li>
            <b>Propuesta de Solución: Estrategia por Fases (MVP Ágil con Respaldo Matemático COCOMO):</b> Si la clínica universitaria necesita obligatoriamente resultados en 3 meses, la solución profesional de ingeniería es <b>reducir el alcance inicial</b> manteniendo un equipo estable de <b>4 desarrolladores</b>:
            <ul>
                <li><b>Respaldo matemático de capacidad en 3 meses:</b> Un equipo de 4 personas trabajando 3 meses genera $PM_{MVP} = 4 \times 3 = 12 \text{ PM}$. Invirtiendo la fórmula de COCOMO Semiacoplado ($PM = 3.00 \cdot KLOC^{1.12}$), se obtiene:  
                $$KLOC_{MVP} = (12 / 3.00)^{1 / 1.12} = 4^{0.8928} \approx \mathbf{3.45 \text{ KLOC}}$$  
                Esto valida que en 3 meses es matemáticamente viable construir un MVP con ~3.5 KLOC (~20% del sistema).</li>
                <li><b>Fase 1 (MVP en 3 Meses | ~3.5 KLOC | 4 desarrolladores):</b> Módulos de Pacientes, Citas Médicas (registro, reprogramación, cancelación, lista de espera), Usuarios/Roles (autenticación básica) y migración de los 2,000 registros de Excel. Resuelve de inmediato los tiempos de espera y el desorden de agendas en mostrador.</li>
                <li><b>Fase 2 (Plataforma Integral en Meses 4 a 9 | ~14.5 KLOC | 4 a 5 desarrolladores):</b> Expediente clínico digital completo (signos vitales, recetas, antecedentes, adjuntos), consumo de la API de recordatorios por SMS/correo (resolviendo de fondo el ausentismo o <i>no-show</i>) y el módulo de <b>Reportes Mensuales y Gerenciales</b> (productividad médica y exportación a PDF/CSV).</li>
            </ul>
        </li>
        <li>
            <b>Utilidad Estratégica de COCOMO:</b> Este modelo matemático dota al líder técnico de un fundamento objetivo y científico para negociar con los directivos institucionales, demostrando que la calidad del software médico y la seguridad de los pacientes no pueden comprometerse por plazos comerciales arbitrarios.
        </li>
    </ol>

    <!-- ================= SECCIÓN 7 ================= -->
    <h1>7. Referencias Bibliográficas</h1>
    <ul style="font-size: 7.7pt; color: #475569; margin-bottom: 0;">
        <li>Boehm, B. W. (1981). <i>Software Engineering Economics</i>. Englewood Cliffs, NJ: Prentice-Hall.</li>
        <li>Brooks, F. P. (1975). <i>The Mythical Man-Month: Essays on Software Engineering</i>. Reading, MA: Addison-Wesley.</li>
        <li>Navarro Salcedo, G. (2026). <i>Ecuaciones y Coeficientes del Modelo COCOMO Básico</i>. Presentación de la Cátedra de Ingeniería de Software.</li>
        <li>Pressman, R. S., & Maxim, B. R. (2020). <i>Software Engineering: A Practitioner's Approach</i> (9th ed.). McGraw-Hill Education.</li>
        <li>Sommerville, I. (2016). <i>Software Engineering</i> (10th ed.). Pearson Education.</li>
    </ul>

</body>
</html>
"""

    html_path = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_2_1_Modelo_COCOMO_Basico_Salud_Integral.html"
    pdf_path = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_2_1_Modelo_COCOMO_Basico_Salud_Integral.pdf"
    downloads_pdf = r"C:\Users\erfierro\Downloads\Actividad_2_1_Modelo_COCOMO_Basico_Salud_Integral.pdf"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("HTML generado exitosamente en:", html_path)

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]

    print("Ejecutando Chrome headless...")
    subprocess.run(cmd, check=True)

    if os.path.exists(pdf_path):
        print("PDF generado exitosamente en:", pdf_path)
        shutil.copy2(pdf_path, downloads_pdf)
        print("Copia creada exitosamente en Downloads:", downloads_pdf)
    else:
        print("Error: No se pudo generar el archivo PDF.")

if __name__ == "__main__":
    generate_improved_deliverables()
