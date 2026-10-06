import os
import sys
import subprocess
import shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, hex_color):
    """Establece color de fondo de una celda en docx."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    """Establece márgenes internos de una celda."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_callout_box(doc, text_paragraphs, border_color="1B365D", bg_color="F0F4F8"):
    """Crea un recuadro de llamada/alerta estilizado tipo callout."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=160)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '24') # 3pt
    left.set(qn('w:space'), '0')
    left.set(qn('w:color'), border_color)
    tcBorders.append(left)
    
    for side in ['top', 'bottom', 'right']:
        node = OxmlElement(f'w:{side}')
        node.set(qn('w:val'), 'none')
        tcBorders.append(node)
        
    tcPr.append(tcBorders)
    
    p_first = cell.paragraphs[0]
    p_first.text = ""
    for i, (title, content, bold_prefix) in enumerate(text_paragraphs):
        p = p_first if i == 0 else cell.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        if title:
            r_title = p.add_run(title)
            r_title.bold = True
            r_title.font.name = "Calibri"
            r_title.font.size = Pt(10)
            r_title.font.color.rgb = RGBColor(27, 54, 93)
        if bold_prefix:
            r_bp = p.add_run(bold_prefix)
            r_bp.bold = True
            r_bp.font.name = "Calibri"
            r_bp.font.size = Pt(9.5)
            r_bp.font.color.rgb = RGBColor(44, 62, 80)
        if content:
            r_c = p.add_run(content)
            r_c.font.name = "Calibri"
            r_c.font.size = Pt(9.5)
            r_c.font.color.rgb = RGBColor(50, 50, 50)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def generate_word():
    doc = Document()
    
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(30)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(18)
        r.font.color.rgb = RGBColor(27, 54, 93)
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(24)
        r = p.add_run(text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 128, 128)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(13)
        r.font.color.rgb = RGBColor(27, 54, 93)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(44, 62, 80)
        return p

    def add_p(text, bold_prefix=""):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(5)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.bold = True
            rb.font.name = "Calibri"
            rb.font.size = Pt(10)
            rb.font.color.rgb = RGBColor(30, 30, 30)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(40, 40, 40)
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.bold = True
            rb.font.name = "Calibri"
            rb.font.size = Pt(10)
            rb.font.color.rgb = RGBColor(30, 30, 30)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(40, 40, 40)
        return p

    # -------------------------------------------------------------
    # PORTADA
    # -------------------------------------------------------------
    add_title("ACTIVIDAD 2.1. MODELO COCOMO BÁSICO\nESTIMACIÓN DE ESFUERZO, TIEMPO Y PERSONAL")
    add_subtitle("CASO DE ESTUDIO: SISTEMA WEB DE GESTIÓN CLÍNICA \"SALUD INTEGRAL\"")

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.line_spacing = 1.3
    p_meta.paragraph_format.space_after = Pt(25)
    meta_runs = [
        ("Materia: ", True), ("Administración de Proyectos / Ingeniería de Software\n", False),
        ("Docente: ", True), ("Dr. Gabriel Navarro Salcedo\n", False),
        ("Estudiante: ", True), ("Ernesto Fierro\n", False),
        ("Fecha de Entrega: ", True), ("29 de Septiembre de 2026\n", False),
        ("Ponderación: ", True), ("2 Puntos (2% de la Evaluación Total)\n", False),
        ("Estado: ", True), ("Solución Técnica y Matemática Completa", False)
    ]
    for m_text, m_bold in meta_runs:
        rm = p_meta.add_run(m_text)
        rm.bold = m_bold
        rm.font.name = "Calibri"
        rm.font.size = Pt(10.5)
        rm.font.color.rgb = RGBColor(60, 70, 85)

    doc.add_page_break()

    # -------------------------------------------------------------
    # SECCIÓN 1: INTRODUCCIÓN Y ANÁLISIS DEL CASO
    # -------------------------------------------------------------
    add_h1("1. Análisis del Caso de Estudio: Clínica Universitaria \"Salud Integral\"")
    add_p(
        "La Clínica Universitaria \"Salud Integral\" atiende consultas de medicina general y especialidad. Actualmente opera "
        "con expedientes en papel y registros manuales en hojas de cálculo (Excel), lo cual genera tiempos de espera elevados, "
        "pérdida de trazabilidad de pacientes y altos índices de inasistencia (no-show). Con el objetivo de modernizar la operación, "
        "la dirección institucional solicitó el desarrollo de una plataforma web (accesible desde computadoras y tablets) para "
        "centralizar la gestión clínica y administrativa."
    )

    add_h2("1.1. Alcance Técnico y Dimensionamiento")
    add_bullet("Pacientes, Citas médicas, Expediente clínico básico, Usuarios y Roles, Reportes mensuales, Importación histórica desde Excel y Notificaciones automáticas.", "• Módulos del Sistema (7 módulos): ")
    add_bullet("Aproximadamente 20 formularios y pantallas operativas interactivas responsivas para tablet y escritorio.", "• Volumen de Interfaces: ")
    add_bullet("10 entidades de datos fundamentales (Paciente, Médico, Especialidad, Cita, NotaConsulta, SignosVitales, Receta, Usuario, Rol, ArchivoAdjunto).", "• Modelo de Entidades: ")
    add_bullet("Consumo de API institucional preexistente para envío automatizado de SMS y correos electrónicos.", "• Integración Externa: ")
    add_bullet("Proceso de extracción, transformación y carga (ETL) de 2,000 registros desde archivos de Excel históricos.", "• Migración de Datos: ")
    add_bullet("Se asume formalmente un equipo de desarrollo universitario con nivel de experiencia media.", "• Perfil del Equipo: ")

    add_h2("1.2. Parámetros de Tamaño de Software (KLOC)")
    add_bullet("18,000 líneas de código fuente (18 KLOC), estimadas por el coordinador técnico con base en proyectos precedentes.", "• Código nuevo total: ")
    add_bullet("0 KLOC (no se contempla reutilización de código; se asume desarrollo 100% nuevo según la especificación).", "• Reutilización de código: ")
    add_bullet("Indiferente para el Modelo Básico (COCOMO Básico opera directamente sobre el volumen en KLOC).", "• Lenguaje de programación: ")

    # -------------------------------------------------------------
    # SECCIÓN 2: FORMULACIÓN MATEMÁTICA Y COEFICIENTES
    # -------------------------------------------------------------
    add_h1("2. Formulación Matemática del Modelo COCOMO Básico")
    add_p(
        "El Modelo Constructivo de Costos (COCOMO 81), propuesto por el Dr. Barry Boehm, es un modelo empírico de estimación algorítmica "
        "que permite proyectar el esfuerzo en personas-mes, el tiempo de entrega y el tamaño del equipo de trabajo en función del tamaño "
        "estimado del código fuente expresado en miles de líneas de código (KLOC)."
    )

    create_callout_box(doc, [
        ("ECUACIONES OFICIALES DEL MODELO COCOMO BÁSICO:", "", ""),
        ("", "PM = A · (KLOC)^B", "1. Esfuerzo Aplicado (Personas-Mes): "),
        ("", "TDEV = C · (PM)^D  (notado como TDVE en las diapositivas de clase)", "2. Tiempo de Desarrollo Cronológico (Meses): "),
        ("", "NP = PM / TDEV", "3. Número Óptimo de Personas Necesarias: ")
    ], border_color="1B365D", bg_color="F2F5F9")

    add_h2("2.1. Tabla Oficial de Coeficientes de Calibración COCOMO")
    add_p("De acuerdo con las diapositivas oficiales de la cátedra proporcionadas por el docente:")

    table_coef = doc.add_table(rows=4, cols=5)
    table_coef.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Tipo de Proyecto", "A", "B", "C", "D"]
    data_coef = [
        ["Orgánico", "2.40", "1.05", "2.50", "0.38"],
        ["Medio (Semiacoplado) [Caso Asignado]", "3.00", "1.12", "2.50", "0.35"],
        ["Embebido", "3.60", "1.20", "2.50", "0.32"]
    ]

    for c_idx, h_text in enumerate(headers):
        cell = table_coef.cell(0, c_idx)
        cell.text = h_text
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row_values in enumerate(data_coef):
        bg = "FFFFFF" if r_idx % 2 == 0 else "F7FAFC"
        if r_idx == 1:
            bg = "EBF3FA"
        for c_idx, val in enumerate(row_values):
            cell = table_coef.cell(r_idx + 1, c_idx)
            cell.text = val
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9)
                if r_idx == 1:
                    r.bold = True
                    r.font.color.rgb = RGBColor(27, 54, 93)

    add_h2("2.2. Justificación Técnica del Modo de Desarrollo")
    add_bullet(
        "El documento del caso señala explícitamente: \"se asume un equipo de desarrollo universitario con experiencia media\". En la taxonomía formal de Boehm, los equipos con niveles intermedios de experiencia corresponden estrictamente al Modo Medio (Semiacoplado).",
        "1. Experiencia del equipo: "
    )
    add_bullet(
        "Con 18 KLOC, 20 interfaces y 10 entidades, el proyecto no es trivial y requiere interactuar con una API universitaria externa para notificaciones y migrar 2,000 registros heredados de Excel.",
        "2. Complejidad de integraciones y datos: "
    )
    add_p(
        "Se presenta adicionalmente el Modo Orgánico como un análisis de sensibilidad comparativo frente a un escenario hipotético de máxima estabilidad y autonomía técnica.",
        bold_prefix="• Nota metodológica: "
    )

    # -------------------------------------------------------------
    # SECCIÓN 3: CÁLCULOS MATEMÁTICOS PASO A PASO
    # -------------------------------------------------------------
    add_h1("3. Desarrollo y Cálculo del Modelo COCOMO Básico")

    add_h2("3.1. Caso Principal: Modo Medio / Semiacoplado (A = 3.00, B = 1.12, C = 2.50, D = 0.35 | KLOC = 18)")
    calc_medio_items = [
        ("PASO 1: CÁLCULO DEL ESFUERZO (PM)", "", ""),
        ("", "PM = 3.00 · (18)^1.12", "Fórmula: "),
        ("", "18^1.12 ≈ 25.4627", "Evaluación exponencial: "),
        ("", "PM = 3.00 · 25.4627 = 76.3882 ≈ 76.39 Personas-Mes", "Resultado: "),
        ("", "", ""),
        ("PASO 2: CÁLCULO DEL TIEMPO ESTIMADO DE DESARROLLO (TDEV)", "", ""),
        ("", "TDEV = 2.50 · (76.3882)^0.35", "Fórmula: "),
        ("", "(76.3882)^0.35 ≈ 4.5610", "Evaluación exponencial: "),
        ("", "TDEV = 2.50 · 4.5610 = 11.4025 ≈ 11.40 Meses", "Resultado: "),
        ("", "", ""),
        ("PASO 3: CÁLCULO DEL NÚMERO ÓPTIMO DE DESARROLLADORES (NP)", "", ""),
        ("", "NP = PM / TDEV = 76.3882 / 11.4025 = 6.6993 ≈ 6.70 Desarrolladores", "Fórmula y resultado: "),
        ("", "Aproximadamente 6 a 7 desarrolladores de tiempo completo (redondeo operativo a 7 personas).", "Equipo óptimo recomendado: ")
    ]
    create_callout_box(doc, calc_medio_items, border_color="008080", bg_color="F0FDF4")

    add_h2("3.2. Escenario Comparativo: Modo Orgánico (Análisis de Sensibilidad)")
    calc_org_items = [
        ("PASO 1: CÁLCULO DEL ESFUERZO (PM)", "", ""),
        ("", "PM = 2.40 · (18)^1.05 = 2.40 · 20.7987 = 49.9169 ≈ 49.92 Personas-Mes", "Resultado: "),
        ("PASO 2: CÁLCULO DEL TIEMPO (TDEV)", "", ""),
        ("", "TDEV = 2.50 · (49.9169)^0.38 = 2.50 · 4.4191 = 11.0478 ≈ 11.05 Meses", "Resultado: "),
        ("PASO 3: CÁLCULO DEL PERSONAL (NP)", "", ""),
        ("", "NP = 49.9169 / 11.0478 = 4.5183 ≈ 4.52 Desarrolladores (Equipo de 4 a 5 desarrolladores).", "Resultado: ")
    ]
    create_callout_box(doc, calc_org_items, border_color="1B365D", bg_color="F8FAFC")

    add_h2("3.3. Matriz Resumen de Resultados COCOMO")
    table_comp = doc.add_table(rows=3, cols=6)
    table_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_c = ["Modo de Proyecto", "Líneas (KLOC)", "Esfuerzo (PM)", "Tiempo (TDEV)", "Personal (NP)", "Equipo Sugerido"]
    data_comp = [
        ["Medio (Semiacoplado) [Caso Base]", "18 KLOC", "76.39 PM", "11.40 Meses", "6.70 Personas", "6 – 7 Desarrolladores"],
        ["Orgánico [Comparativo]", "18 KLOC", "49.92 PM", "11.05 Meses", "4.52 Personas", "4 – 5 Desarrolladores"]
    ]

    for c_idx, h_text in enumerate(headers_c):
        cell = table_comp.cell(0, c_idx)
        cell.text = h_text
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row_values in enumerate(data_comp):
        bg = "EBF3FA" if r_idx == 0 else "FFFFFF"
        for c_idx, val in enumerate(row_values):
            cell = table_comp.cell(r_idx + 1, c_idx)
            cell.text = val
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9)
                if r_idx == 0 and c_idx in [2, 3, 4, 5]:
                    r.bold = True
                    r.font.color.rgb = RGBColor(27, 54, 93)

    # -------------------------------------------------------------
    # SECCIÓN 4: INTERPRETACIÓN Y VIABILIDAD
    # -------------------------------------------------------------
    add_h1("4. Interpretación Técnica de Viabilidad Respecto al Tiempo del Cliente")
    add_p(
        "Siguiendo fielmente la estructura del ejemplo de la empresa COTECNO analizado en clase, contrastamos el tiempo nominal "
        "empírico obtenido mediante COCOMO (11.40 meses) contra los horizontes temporales solicitados por clientes y directivos:"
    )

    add_h2("4.1. Escenario A: Entrega Solicitada en 3 Meses (Directamente Análogo al Ejemplo Docente)")
    add_bullet(
        "NP = PM / Plazo = 76.39 / 3 = 25.46 desarrolladores. Para cubrir la totalidad del esfuerzo sin déficit (25 × 3 = 75 PM < 76.39 PM), se requieren matemáticamente 26 desarrolladores a tiempo completo (26 × 3 = 78 PM).",
        "• Personal Requerido (Modo Medio): "
    )
    add_bullet(
        "NP = 49.92 / 3 = 16.64 desarrolladores (~17 desarrolladores a tiempo completo).",
        "• Personal Requerido (Modo Orgánico): "
    )
    add_bullet(
        "TÉCNICAMENTE INVIABLE. De acuerdo con los postulados empíricos de Boehm, no es posible comprimir un cronograma de desarrollo de software a menos del 75% de su tiempo nominal. Comprimir a 3 meses equivale a forzarlo al 26.3% del tiempo nominal (una reducción del 73.7%), situando al proyecto de lleno en la \"Zona Imposible\" y conduciendo al colapso organizacional.",
        "• Dictamen de Viabilidad Técnica: "
    )

    add_h2("4.2. Escenario B: Entrega Semestral Universitaria en 6 Meses")
    add_bullet(
        "NP = PM / Plazo = 76.39 / 6 = 12.73 desarrolladores (~13 desarrolladores a tiempo completo).",
        "• Personal Requerido (Modo Medio): "
    )
    add_bullet(
        "INVIABLE BAJO ALCANCE TOTAL (ZONA IMPOSIBLE). Seis meses representa una compresión al 52.6% del tiempo nominal (11.40 meses), manteniéndose significativamente por debajo del umbral mínimo del 75% (8.55 meses). Intentar entregar el 100% del alcance en 6 meses duplicando la plantilla es inviable bajo COCOMO, a menos que se aplique una reducción formal del alcance del software.",
        "• Dictamen de Viabilidad Técnica: "
    )

    add_h2("4.3. Análisis Financiero de Honorarios Salariales del Equipo")
    add_p(
        "Tomando como referencia el tabulador de $10,100.00 MXN mensuales por desarrollador estipulado en el ejemplo de la actividad, se proyecta la nómina salarial para cada alternativa:"
    )

    table_cost = doc.add_table(rows=4, cols=6)
    table_cost.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_cost = ["Escenario de Plazo", "Desarrolladores (NP)", "Duración", "Costo Mensual", "Honorarios Totales (MXN)", "Factibilidad Técnica"]
    data_cost = [
        ["Nominal Óptimo COCOMO", "7 desarrolladores", "11.40 Meses", "$70,700.00 MXN", "$805,980.00 MXN", "Óptimo (Recomendado)"],
        ["Semestre Universitario", "13 desarrolladores", "6.00 Meses", "$131,300.00 MXN", "$787,800.00 MXN", "Zona Imposible (Inviable)"],
        ["Acelerado (3 Meses - Ejemplo)", "26 desarrolladores", "3.00 Meses", "$262,600.00 MXN", "$787,800.00 MXN", "Inviable Total (Colapso)"]
    ]

    for c_idx, h_text in enumerate(headers_cost):
        cell = table_cost.cell(0, c_idx)
        cell.text = h_text
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=70, bottom=70, left=70, right=70)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row_values in enumerate(data_cost):
        bg = "FFFFFF" if r_idx % 2 == 0 else "F7FAFC"
        if r_idx == 0:
            bg = "EBF3FA"
        for c_idx, val in enumerate(row_values):
            cell = table_cost.cell(r_idx + 1, c_idx)
            cell.text = val
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [1, 2, 5] else WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [3, 4] else WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(8.5)
                if r_idx == 0 and c_idx in [4, 5]:
                    r.bold = True
                    r.font.color.rgb = RGBColor(27, 54, 93)

    add_p(
        "El costo laboral nominal estricto derivado de COCOMO es de 76.39 PM × $10,100 = $771,538.82 MXN. "
        "Las ligeras diferencias en los totales de la tabla obedecen al redondeo a números enteros discretos de personal (26 personas en 3 meses = $787,800 MXN; 7 personas en 11.4 meses = $805,980 MXN). "
        "Cualitativamente, pagar a 26 desarrolladores en un plazo tan comprimido genera un desperdicio económico severo, pues la mayor parte del tiempo pagado se consume en fricciones de coordinación y retrabajo.",
        bold_prefix="• Nota analítica: "
    )

    # -------------------------------------------------------------
    # SECCIÓN 5: REFLEXIÓN TÉCNICA
    # -------------------------------------------------------------
    add_h1("5. Reflexión Técnica: ¿Cómo Cambia el Proyecto al Modificar el Personal?")
    add_p(
        "Una premisa errónea habitual en clientes no técnicos es asumir que el esfuerzo (Personas-Mes) se puede fraccionar arbitrariamente dividiendo entre el número de desarrolladores (la falacia del \"Hombre-Mes\"). "
        "La ingeniería de software demuestra que alterar el personal transforma críticamente la dinámica del proyecto:"
    )

    add_h2("5.1. El Mito del Hombre-Mes y el Crecimiento Cuadrático de Canales de Comunicación")
    add_p(
        "Frederick Brooks (1975) demostró que las personas y los meses no son magnitudes intercambiables: asignar 26 desarrolladores no reduce proporcionalmente el tiempo. "
        "Los canales de comunicación bilateral crecen de forma estrictamente cuadrática mediante la fórmula combinatoria:"
    )

    create_callout_box(doc, [
        ("CRECIMIENTO CUADRÁTICO DE CANALES DE COMUNICACIÓN: C = [ N · (N - 1) ] / 2", "", ""),
        ("", "C = (7 · 6) / 2 = 21 canales de comunicación.", "• Equipo Nominal (N = 7): "),
        ("", "C = (13 · 12) / 2 = 78 canales (+271% de sobrecarga).", "• Equipo Semestral (N = 13): "),
        ("", "C = (26 · 25) / 2 = 325 canales (+1,448% de sobrecarga) [o 300 canales para N = 25].", "• Equipo Forzado a 3 Meses (N = 26): "),
        ("", "Al saltar de 21 a 325 canales, la jornada laboral se satura en reuniones de sincronización, conflictos de integración en Git y debates arquitectónicos. Si el proyecto se retrasa e intentan sumar personal, se activa la temida Ley de Brooks: \"Añadir personal a un proyecto retrasado solo lo retrasa más\".", "Impacto Operativo: ")
    ], border_color="C0392B", bg_color="FDF2E9")

    add_h2("5.2. Curva de Aprendizaje y Costo de Onboarding en Equipos Universitarios")
    add_p(
        "El caso señala que el equipo tiene \"experiencia media\". De acuerdo con la literatura de ingeniería de software sobre asimilación técnica (Pressman & Maxim, 2020; Sommerville, 2016), "
        "en proyectos urgentes con equipos no sénior, el periodo de inducción y acoplamiento (ramp-up) consume entre el 30% y el 50% de la ventana temporal disponible:"
    )
    add_bullet("Los desarrolladores más capacitados que diseñaron la base de datos relacional y la seguridad RBAC deben detener su trabajo de programación para capacitar a los nuevos integrantes.")
    add_bullet("La productividad grupal sufre una caída inmediata (el denominado valle de productividad o curva en J).")

    add_h2("5.3. El Límite Infranqueable de Compresión (The Impossible Region de Boehm)")
    add_p(
        "Los estudios empíricos de Boehm demostraron que ningún proyecto de software puede comprimirse a menos del 75% del tiempo nominal de desarrollo (TDEV_mín ≈ 0.75 · TDEV):"
    )
    add_bullet("Límite mínimo para Modo Medio: TDEV_mín = 0.75 · 11.40 Meses = 8.55 Meses.", "• ")
    add_bullet("Límite mínimo para Modo Orgánico: TDEV_mín = 0.75 · 11.05 Meses = 8.29 Meses.", "• ")
    add_p(
        "Cualquier intento de forzar la entrega en 3 o 6 meses traspasa la frontera hacia la \"Zona Imposible\", produciendo sistemas con código frágil, pruebas omitidas y graves riesgos de seguridad en expedientes clínicos."
    )

    add_h2("5.4. Dependencias Secuenciales y Ley de Amdahl")
    add_p(
        "El software posee dependencias de precedencia ineludibles: no es posible paralelizar el desarrollo de las 20 pantallas si el esquema de base de datos de las 10 entidades no está normalizado y probado; "
        "y no se puede implementar el expediente clínico sin tener antes la autenticación y el registro de pacientes. Como establece la Ley de Amdahl, la velocidad de ejecución está limitada por la fracción estrictamente secuencial de las tareas."
    )

    # -------------------------------------------------------------
    # SECCIÓN 6: CONCLUSIONES Y RECOMENDACIÓN MVP
    # -------------------------------------------------------------
    add_h1("6. Conclusiones Técnicas y Recomendaciones de Gestión")
    add_bullet(
        "Para un tamaño de 18 KLOC con un equipo universitario de experiencia media, el modelo COCOMO Básico proyecta formalmente 76.39 persona-mes, una duración óptima de 11.40 meses y una dotación de 6 a 7 desarrolladores a tiempo completo.",
        "1. Validez del Modelo Cuantitativo: "
    )
    add_bullet(
        "Aceptar una entrega en 3 meses contratando a 26 desarrolladores es un error metodológico crítico. La sobrecarga cuadrática de 325 canales de comunicación y la curva de aprendizaje paralizarán el avance.",
        "2. Rechazo al Enfoque de Fuerza Bruta: "
    )
    add_bullet(
        "Si la clínica universitaria necesita obligatoriamente resultados en 3 meses, la solución profesional de ingeniería es reducir el alcance inicial manteniendo un equipo estable de 4 desarrolladores:",
        "3. Propuesta de Solución: Estrategia por Fases (MVP Ágil con Respaldo Matemático COCOMO): "
    )
    add_bullet(
        "Un equipo de 4 personas trabajando 3 meses genera PM_MVP = 4 × 3 = 12 PM. Invirtiendo la fórmula de COCOMO Semiacoplado (PM = 3.00 · KLOC^1.12), se obtiene KLOC_MVP = (12 / 3.00)^(1 / 1.12) = 4^0.8928 ≈ 3.45 KLOC. Esto valida que en 3 meses es matemáticamente viable construir un MVP con ~3.5 KLOC (~20% del sistema).",
        "   • Respaldo Matemático de Capacidad en 3 Meses: "
    )
    add_bullet(
        "Módulos de Pacientes, Citas Médicas (registro, reprogramación, cancelación, lista de espera), Usuarios/Roles (autenticación básica) y migración de los 2,000 registros de Excel. Resuelve de inmediato los tiempos de espera y el desorden de agendas en mostrador.",
        "   • Fase 1 (MVP en 3 Meses | ~3.5 KLOC | 4 desarrolladores): "
    )
    add_bullet(
        "Expediente clínico digital completo (signos vitales, recetas, antecedentes, adjuntos), consumo de la API de recordatorios por SMS/correo (resolviendo de fondo el ausentismo o no-show) y el módulo de Reportes Mensuales y Gerenciales (productividad médica y exportación a PDF/CSV).",
        "   • Fase 2 (Plataforma Integral en Meses 4 a 9 | ~14.5 KLOC | 4 a 5 desarrolladores): "
    )
    add_bullet(
        "Este modelo matemático dota al líder técnico de un fundamento objetivo y científico para negociar con los directivos institucionales, demostrando que la calidad del software médico y la seguridad de los pacientes no pueden comprometerse por plazos comerciales arbitrarios.",
        "4. Utilidad Estratégica de COCOMO: "
    )

    # -------------------------------------------------------------
    # SECCIÓN 7: REFERENCIAS BIBLIOGRÁFICAS
    # -------------------------------------------------------------
    add_h1("7. Referencias Bibliográficas")
    add_bullet("Boehm, B. W. (1981). Software Engineering Economics. Prentice-Hall.", "• ")
    add_bullet("Brooks, F. P. (1975). The Mythical Man-Month: Essays on Software Engineering. Addison-Wesley.", "• ")
    add_bullet("Navarro Salcedo, G. (2026). Ecuaciones y Coeficientes del Modelo COCOMO Básico. Presentación de la Cátedra de Ingeniería de Software.", "• ")
    add_bullet("Pressman, R. S., & Maxim, B. R. (2020). Software Engineering: A Practitioner's Approach (9th ed.). McGraw-Hill Education.", "• ")
    add_bullet("Sommerville, I. (2016). Software Engineering (10th ed.). Pearson Education.", "• ")

    output_docx = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_2_1_Modelo_COCOMO_Basico_Salud_Integral.docx"
    doc.save(output_docx)
    print("Documento Word (.docx) actualizado exitosamente en:", output_docx)

if __name__ == "__main__":
    generate_word()
