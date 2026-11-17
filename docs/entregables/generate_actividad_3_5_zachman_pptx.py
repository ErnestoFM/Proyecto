import os
import shutil
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_PPTX_PATH = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_3_5_Matriz_Zachman_Equipo2.pptx"
DOWNLOADS_PPTX_PATH = r"C:\Users\erfierro\Downloads\Actividad_3_5_Matriz_Zachman_Equipo2.pptx"

# 24 Google Drive links verified HTTP 200
DOCS_LINKS = {
    # Fila 1: INTENCIÓN
    "c01": ("Características", "https://drive.google.com/file/d/1JN_dtu5lZ1W7tbtIF0IKflDZPmsfYhf3/view?usp=sharing", "Catálogo segmentado, POS multipago, Rewards ODS 12 y seguridad stateless."),
    "c02": ("Procesos de Negocio", "https://drive.google.com/file/d/1vcsIoEWRk4YHCevhiRMAXfcy3Bx66GEu/view?usp=sharing", "PN-01 a PN-06: Abastecimiento, venta mostrador, sellos Rewards y corte."),
    "c03": ("Diagramas de Contexto", "https://drive.google.com/file/d/1LzBN-nL0tG-zNTOaP2HoctF0gQJVmdd1/view?usp=sharing", "DFD Nivel 0 con entidades: Cliente, Cajero, Cooperativas, SPEI y Google."),
    "c04": ("Workflow (Roles y Act)", "https://drive.google.com/file/d/1Wzye6_ptLYnj-maWlK4KD0UG6N26zPra/view?usp=sharing", "Flujo operativo entre roles humanos y Matriz RACI para 10 tareas clave."),
    "c05": ("Listado de Eventos", "https://drive.google.com/file/d/1TfmMaKqq7NDDG6rJWS3F_GMakRlu5WEJ/view?usp=sharing", "10 eventos de negocio (EVT-01..10): Apertura, termo reusable, cobro y corte Z."),
    "c06": ("Visión y Objetivos", "https://drive.google.com/file/d/1Ip5KtpyCUPkLIxO7MxxnFKhMVXtaz9CH/view?usp=sharing", "Misión, visión, 4 objetivos SMART y alineación estratégica con ODS 12."),

    # Fila 2: ALCANCE
    "c07": ("Listado Requerimientos", "https://drive.google.com/file/d/16W6lQikUgddAJ_KBMcXtxEKs69DheEdR/view?usp=sharing", "15 Requerimientos Funcionales (RF-01..15) con actores y criterios de éxito."),
    "c08": ("Diagramas Actividad", "https://drive.google.com/file/d/1Peu-KbIO6gYiDaw4GL4FjdYuPUxfrs_t/view?usp=sharing", "DA-01 Venta con Bono Ecológico y DA-02 Abastecimiento de Café con PEPS."),
    "c09": ("Ambiente y RNF", "https://drive.google.com/file/d/1tDRRXX3a6l6XLnXlf6dz8XU0syW5gYpv/view?usp=sharing", "GCP Cloud Run, Docker y 7 RNF bajo la norma internacional ISO/IEC 25010."),
    "c10": ("Rol de Negocio", "https://drive.google.com/file/d/1laKg-ZQjPQ6wK8LZf7HKQ8F1w1OdXUZ_/view?usp=sharing", "Fichas de caracterización: Admin, Cajero de Turno, Cliente y Productor."),
    "c11": ("Cronograma Negocio", "https://drive.google.com/file/d/182RflhJkU9rRvR4cFmB2hGIaat-XJhpo/view?usp=sharing", "4 fases en 16 semanas, hitos críticos y ciclo de turnos diarios en tienda."),
    "c12": ("Prioridades Negocio", "https://drive.google.com/file/d/1j68qAoV3ERWpcu55pOt0arTVubQW8Oz9/view?usp=sharing", "Jerarquización MoSCoW (Must, Should, Could, Won't) y matriz valor-esfuerzo."),

    # Fila 3: ALTO NIVEL
    "c13": ("Listado Casos de Uso", "https://drive.google.com/file/d/1YreuU-wXv48jbjeqUQ8p9L3GmDx7d9d1/view?usp=sharing", "Catálogo de 12 Casos de Uso (CU-01..12) cruzados con requerimientos funcionales."),
    "c14": ("Especificación CU", "https://drive.google.com/file/d/1_cDRjedF6fy1GsQmVd-IndjlCYP70CCp/view?usp=sharing", "Plantillas Cockburn para CU-01 (Auth), CU-03/04 (POS) y CU-12 (Saga/Reversas)."),
    "c15": ("Subsistemas y Módulos", "https://drive.google.com/file/d/1WRVpfAYHLaH3OTnbtSHMcCC6eMhOT7Kr/view?usp=sharing", "Monorepo desacoplado: apps/web, apps/api, packages/database y packages/messaging."),
    "c16": ("Actores Descripción", "https://drive.google.com/file/d/14TNzrFVrvmTok-ft1q7ZJsq6ybI2MD6l/view?usp=sharing", "Caracterización de 8 actores (humanos y servicios) y matriz cruzada."),
    "c17": ("Precedencia de CU", "https://drive.google.com/file/d/1oc3S5ZsxEnefU3D5VnziqO1WboquZ0bU/view?usp=sharing", "Reglas de precedencia, dependencias <<include>>, extensiones y grafo acíclico."),
    "c18": ("Reglas de Negocio", "https://drive.google.com/file/d/1lQZliiNeIBKsRtnwZq_AQzI9-VYM0f3v/view?usp=sharing", "8 reglas de negocio (RN-01..08) clasificadas por criticidad P1, P2 y P3."),

    # Fila 4: DETALLE
    "c19": ("Diagramas CU, UI y Dominio", "https://drive.google.com/file/d/16cuwd5f5ozDXF5XtztKYo6OVAfNaArkI/view?usp=sharing", "Diagrama UML global, wireframes de pantallas POS/Login y MER relacional."),
    "c20": ("Navegación y Rutas", "https://drive.google.com/file/d/1s87hXYzVU8eJpM2mPCoOuFC8T_gYCnNE/view?usp=sharing", "Grafo en Vue Router 4, guardianes de ruta (beforeEach) y atajos F2/Esc."),
    "c21": ("Diagrama de Paquetes", "https://drive.google.com/file/d/1-eevSj942qa2g61nRMKnW1KZKvfrB1xj/view?usp=sharing", "Arquitectura de paquetes @monchis/* bajo Principio de Aciclicidad (ADP)."),
    "c22": ("Permisos RBAC", "https://drive.google.com/file/d/1rBP2enmghjbUN1aGE1FfZixubyQ2EwVC/view?usp=sharing", "Matriz CRUD de permisos por endpoint de API y rutas web (Menor Privilegio)."),
    "c23": ("Diagrama de Estados", "https://drive.google.com/file/d/1WoA5Sw573CwePZ04SNnRf51O8x21sjmx/view?usp=sharing", "Autómatas finitos de Orden de Venta (Order) y Lote de Café (Batch)."),
    "c24": ("Reglas en Modelo Análisis", "https://drive.google.com/file/d/1u_WlrnJiJo7AeiG091-n-Gpevaq5MJ9y/view?usp=sharing", "Trazabilidad de 8 reglas a código TypeScript, Prisma y tests Vitest.")
}

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Paleta de colores
    NAVY = RGBColor(26, 54, 93)      # #1A365D Primario UDG
    BLUE_ACCENT = RGBColor(43, 108, 176) # #2B6CB0
    ORANGE = RGBColor(192, 86, 33)   # #C05621 Naranja institucional
    ORANGE_HEADER = RGBColor(237, 137, 54) # #ED8936
    DARK_TEXT = RGBColor(45, 55, 72) # #2D3748
    MUTED = RGBColor(113, 128, 150)  # #718096
    WHITE = RGBColor(255, 255, 255)
    LIGHT_BG = RGBColor(247, 250, 252) # #F7FAFC
    LINK_BLUE = RGBColor(29, 78, 216) # #1D4ED8 Azul interactivo

    # Helper para encabezado estándar
    def add_header(slide, title_text, subtitle_text):
        hdr_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.133), Inches(0.85))
        tf = hdr_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = "UNIVERSIDAD DE GUADALAJARA  •  CENTRO UNIVERSITARIO DE TONALÁ"
        p0.font.name = "Arial"
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = ORANGE

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.name = "Arial"
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = NAVY
        p1.space_before = Pt(2)

        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.name = "Arial"
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = MUTED
            p2.space_before = Pt(1)

    # =========================================================================
    # SLIDE 1: PORTADA INSTITUCIONAL
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)

    # Barra superior decorativa
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.2))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = ORANGE
    top_bar.line.fill.background()

    # Barra inferior decorativa
    bot_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.3), Inches(13.333), Inches(0.2))
    bot_bar.fill.solid()
    bot_bar.fill.fore_color.rgb = NAVY
    bot_bar.line.fill.background()

    # Escudo UDG
    escudo_path = r"d:\ernestofm\Proyecto\docs\entregables\img\escudo_udg_oficial.png"
    if os.path.exists(escudo_path):
        s1.shapes.add_picture(escudo_path, Inches(1.0), Inches(1.6), height=Inches(3.8))

    # Bloque de Títulos Portada
    tb_portada = s1.shapes.add_textbox(Inches(4.2), Inches(1.2), Inches(8.3), Inches(5.2))
    tf1 = tb_portada.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "UNIVERSIDAD DE GUADALAJARA"
    p.font.name = "Arial"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p = tf1.add_paragraph()
    p.text = "Centro Universitario de Tonalá (CUTonalá) — División de Ingenierías"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    p.space_after = Pt(14)

    p = tf1.add_paragraph()
    p.text = "Actividad 3.5. Matriz de Zachman Aplicada a Requerimientos"
    p.font.name = "Arial"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = ORANGE
    p.space_before = Pt(8)

    p = tf1.add_paragraph()
    p.text = "Mapeo Arquitectónico Conceptual y Lógico con 24 Entregables Verificados"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(18)

    # Cuadro datos autor / docente
    p = tf1.add_paragraph()
    p.text = "INFORMACIÓN DEL PROYECTO Y AUTOR:"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_before = Pt(6)

    p = tf1.add_paragraph()
    p.text = "• Proyecto Integrador: Monchis Café — Cafetería Orgánica y Comercial (Equipo 2)"
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.color.rgb = DARK_TEXT

    p = tf1.add_paragraph()
    p.text = "• Autor: Ernesto Hatuey Fierro Meléndez  |  Código de Estudiante: 223977036"
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT

    p = tf1.add_paragraph()
    p.text = "• Docente Titular: Dr. Gabriel Navarro Salcedo  |  Materia: Proyecto Integrador"
    p.font.name = "Arial"
    p.font.size = Pt(10.5)
    p.font.color.rgb = DARK_TEXT

    p = tf1.add_paragraph()
    p.text = "• Fecha de Emisión: Noviembre 2026  |  Tonalá, Jalisco, México"
    p.font.name = "Arial"
    p.font.size = Pt(9.5)
    p.font.color.rgb = MUTED
    p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 2: MATRIZ DE ZACHMAN COMPLETA INTERACTIVA (4x6 CON LINKS)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Actividad 3.5. Matriz de Zachman Aplicada a Requerimientos (Equipo 2)",
               "Mapeo de 4 Niveles Arquitectónicos × 6 Interrogantes Fundamentales — Haz clic en cualquier botón [🔗 Abrir Documento] para ver el entregable en Google Drive")

    # Tabla 5 filas (1 encabezado + 4 niveles) y 7 columnas (Nivel + 6 interrogantes)
    rows_count = 5
    cols_count = 7
    left = Inches(0.5)
    top = Inches(1.3)
    width = Inches(12.333)
    height = Inches(5.8)

    tbl_shape = s2.shapes.add_table(rows_count, cols_count, left, top, width, height)
    tbl = tbl_shape.table

    # Anchos de columna
    tbl.columns[0].width = Inches(1.2)   # Nivel
    tbl.columns[1].width = Inches(1.85)  # QUÉ
    tbl.columns[2].width = Inches(1.85)  # CÓMO
    tbl.columns[3].width = Inches(1.85)  # DÓNDE
    tbl.columns[4].width = Inches(1.85)  # QUIÉN
    tbl.columns[5].width = Inches(1.85)  # CUÁNDO
    tbl.columns[6].width = Inches(1.88)  # POR QUÉ

    # Encabezados de Columna
    col_headers = [
        "NIVEL",
        "¿QUÉ?\n(Datos)",
        "¿CÓMO?\n(Funciones)",
        "¿DÓNDE?\n(Red / Ubicación)",
        "¿QUIÉN?\n(Personas / Roles)",
        "¿CUÁNDO?\n(Tiempo / Eventos)",
        "¿POR QUÉ?\n(Motivación)"
    ]

    for c_idx, h_text in enumerate(col_headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = ORANGE_HEADER
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = h_text
        p.font.name = "Arial"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = WHITE

    # Definición de Celdas de la Matriz (4 niveles)
    matrix_data = [
        # Fila 1: INTENCIÓN (Contextual)
        ("INTENCIÓN\n(Contextual)", ["c01", "c02", "c03", "c04", "c05", "c06"]),
        # Fila 2: ALCANCE (Conceptual)
        ("ALCANCE\n(Conceptual)", ["c07", "c08", "c09", "c10", "c11", "c12"]),
        # Fila 3: ALTO NIVEL (Lógico)
        ("ALTO NIVEL\n(Lógico)", ["c13", "c14", "c15", "c16", "c17", "c18"]),
        # Fila 4: DETALLE (Tecnológico)
        ("DETALLE\n(Tecnológico)", ["c19", "c20", "c21", "c22", "c23", "c24"]),
    ]

    for r_idx, (level_name, cell_keys) in enumerate(matrix_data, start=1):
        # Celda de Nivel (Columna 0)
        lvl_cell = tbl.cell(r_idx, 0)
        lvl_cell.fill.solid()
        lvl_cell.fill.fore_color.rgb = NAVY
        lvl_cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = lvl_cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = level_name
        p.font.name = "Arial"
        p.font.size = Pt(8)
        p.font.bold = True
        p.font.color.rgb = WHITE

        # Celdas de Contenido (Columnas 1 a 6)
        for c_idx, key in enumerate(cell_keys, start=1):
            title, url, desc = DOCS_LINKS[key]
            content_cell = tbl.cell(r_idx, c_idx)
            content_cell.fill.solid()
            # Alternar color suave de fondo
            if r_idx % 2 == 1:
                content_cell.fill.fore_color.rgb = WHITE
            else:
                content_cell.fill.fore_color.rgb = LIGHT_BG

            content_cell.vertical_anchor = MSO_ANCHOR.TOP
            tf = content_cell.text_frame
            tf.word_wrap = True
            tf.margin_top = Inches(0.04)
            tf.margin_bottom = Inches(0.04)
            tf.margin_left = Inches(0.05)
            tf.margin_right = Inches(0.05)

            # Párrafo 1: Título del artefacto
            p_title = tf.paragraphs[0]
            p_title.text = title
            p_title.font.name = "Arial"
            p_title.font.size = Pt(7.5)
            p_title.font.bold = True
            p_title.font.color.rgb = NAVY
            p_title.space_after = Pt(1)

            # Párrafo 2: Botón interactivo con hipervínculo clickeable
            p_btn = tf.add_paragraph()
            p_btn.space_before = Pt(1)
            p_btn.space_after = Pt(2)
            run_btn = p_btn.add_run()
            run_btn.text = "🔗 Abrir en Drive"
            run_btn.font.name = "Arial"
            run_btn.font.size = Pt(7)
            run_btn.font.bold = True
            run_btn.font.underline = True
            run_btn.font.color.rgb = LINK_BLUE
            run_btn.hyperlink.address = url

            # Párrafo 3: Breve descripción de los requerimientos
            p_desc = tf.add_paragraph()
            p_desc.text = desc
            p_desc.font.name = "Arial"
            p_desc.font.size = Pt(6.5)
            p_desc.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 3: JUSTIFICACIÓN METODOLÓGICA Y REFERENCIAS APA 7
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Justificación Metodológica, Rigor de Arquitectura y Referencias APA 7",
               "Fundamentación teórica del marco de Zachman aplicado a la ingeniería de software y trazabilidad con ISO/IEC 25010 y ODS 12")

    # Columna Izquierda: Justificación Metodológica (2 tarjetas)
    box_left = s3.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.8))
    tf_l = box_left.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "1. Estructura Bidimensional del Marco de Zachman"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p = tf_l.add_paragraph()
    p.text = ("El marco de Zachman (1987) proporciona una ontología formal para organizar artefactos de software "
              "sin imponer una metodología rígida. Al cruzar las 6 preguntas universales (Qué, Cómo, Dónde, Quién, Cuándo, Por Qué) "
              "con los niveles de abstracción (Intención, Alcance, Alto Nivel y Detalle), se garantiza que ningún requerimiento "
              "carezca de soporte arquitectónico, técnico o de justificación de negocio.")
    p.font.name = "Arial"
    p.font.size = Pt(8.5)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(8)

    p = tf_l.add_paragraph()
    p.text = "2. Trazabilidad Completa y Cohesión de Ingeniería"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p = tf_l.add_paragraph()
    p.text = ("Cada una de las 24 celdas contiene un documento formal respaldado por diagramas UML 2.5, especificaciones "
              "formales Cockburn, modelos relacionales y código ejecutable. La columna 'Por Qué' garantiza la trazabilidad "
              "hacia las metas ODS 12 (Producción y Consumo Responsables) de la Agenda 2030, y la columna 'Dónde' asegura "
              "el cumplimiento de métricas de calidad ISO/IEC 25010 (latencia < 200 ms, alta disponibilidad en GCP Cloud Run).")
    p.font.name = "Arial"
    p.font.size = Pt(8.5)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(8)

    p = tf_l.add_paragraph()
    p.text = "3. Acceso Público Inmediato a Entregables"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p = tf_l.add_paragraph()
    p.text = ("Todos los archivos .docx fueron compilados formalmente y alojados en Google Drive con acceso público "
              "de lectura para evaluación institucional por pares y por el docente titular Dr. Gabriel Navarro Salcedo.")
    p.font.name = "Arial"
    p.font.size = Pt(8.5)
    p.font.color.rgb = DARK_TEXT

    # Columna Derecha: Referencias Bibliográficas APA 7
    box_right = s3.shapes.add_textbox(Inches(6.8), Inches(1.3), Inches(5.9), Inches(5.8))
    tf_r = box_right.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Referencias Bibliográficas (Norma APA 7.ª Edición)"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ORANGE
    p.space_after = Pt(6)

    references = [
        "1. Bass, L., Clements, P., & Kazman, R. (2012). Software Architecture in Practice (3rd ed.). Addison-Wesley.",
        "2. Cockburn, A. (2000). Writing Effective Use Cases. Addison-Wesley Professional.",
        "3. Evans, E. (2003). Domain-Driven Design: Tackling Complexity in the Heart of Software. Addison-Wesley.",
        "4. Ferraiolo, D. F., et al. (2001). Proposed NIST standard for role-based access control. ACM TISSEC, 4(3), 224–274.",
        "5. Fowler, M. (2002). Patterns of Enterprise Application Architecture. Addison-Wesley.",
        "6. ISO/IEC/IEEE. (2018). ISO/IEC/IEEE 29148:2018 Systems and software engineering — Requirements engineering.",
        "7. Martin, R. C. (2002). Agile Software Development, Principles, Patterns, and Practices. Prentice Hall.",
        "8. Pressman, R. S., & Maxim, B. R. (2021). Ingeniería de software: un enfoque práctico (9.ª ed.). McGraw-Hill.",
        "9. Sommerville, I. (2011). Ingeniería del software (9.ª ed.). Addison-Wesley / Pearson Educación.",
        "10. Zachman, J. A. (1987). A framework for information systems architecture. IBM Systems Journal, 26(3), 276–292."
    ]

    for ref in references:
        p = tf_r.add_paragraph()
        p.text = ref
        p.font.name = "Arial"
        p.font.size = Pt(7.8)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 4: DIRECTORIO DIRECTO DE LOS 24 ENLACES GOOGLE DRIVE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Directorio Centralizado de Enlaces a los 24 Entregables de la Matriz",
               "Índice directo de acceso a cada documento Word (.docx) almacenado en la nube institucional de Google Drive")

    # 4 columnas de 6 enlaces cada una (una por nivel arquitectónico)
    col_w = Inches(2.9)
    col_y = Inches(1.3)
    levels = [
        ("Nivel 1: INTENCIÓN", ["c01", "c02", "c03", "c04", "c05", "c06"], Inches(0.6), ORANGE),
        ("Nivel 2: ALCANCE", ["c07", "c08", "c09", "c10", "c11", "c12"], Inches(3.7), BLUE_ACCENT),
        ("Nivel 3: ALTO NIVEL", ["c13", "c14", "c15", "c16", "c17", "c18"], Inches(6.8), NAVY),
        ("Nivel 4: DETALLE", ["c19", "c20", "c21", "c22", "c23", "c24"], Inches(9.9), ORANGE),
    ]

    for lvl_title, keys, col_x, col_color in levels:
        box = s4.shapes.add_textbox(col_x, col_y, col_w, Inches(5.8))
        tf = box.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = lvl_title
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col_color
        p.space_after = Pt(6)

        for k in keys:
            title, url, _ = DOCS_LINKS[k]
            p_item = tf.add_paragraph()
            p_item.space_before = Pt(3)
            p_item.space_after = Pt(3)

            run_bullet = p_item.add_run()
            run_bullet.text = f"{k.upper()}: {title}\n"
            run_bullet.font.name = "Arial"
            run_bullet.font.size = Pt(8)
            run_bullet.font.bold = True
            run_bullet.font.color.rgb = NAVY

            run_link = p_item.add_run()
            run_link.text = "🔗 Abrir en Google Drive"
            run_link.font.name = "Arial"
            run_link.font.size = Pt(7.5)
            run_link.font.bold = True
            run_link.font.underline = True
            run_link.font.color.rgb = LINK_BLUE
            run_link.hyperlink.address = url

    # Guardar archivo
    prs.save(OUTPUT_PPTX_PATH)
    print(f"Presentación generada con éxito en: {OUTPUT_PPTX_PATH}")

    # Copiar a Descargas del usuario
    shutil.copy2(OUTPUT_PPTX_PATH, DOWNLOADS_PPTX_PATH)
    print(f"Copia depositada en Descargas: {DOWNLOADS_PPTX_PATH}")

if __name__ == "__main__":
    create_presentation()
