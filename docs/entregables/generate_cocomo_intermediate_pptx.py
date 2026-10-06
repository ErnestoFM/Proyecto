import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # PALETA DE COLORES OFICIAL: MONCHIS CAFÉ (Alineada al sitio web y tokens)
    # =========================================================================
    ESPRESSO = RGBColor(74, 59, 50)        # #4A3B32 Café oscuro cálido principal (texto principal)
    ESPRESSO_DARK = RGBColor(52, 36, 28)   # #34241C Espresso profundo
    TERRACOTTA = RGBColor(201, 117, 103)   # #C97567 Rosa terracota institucional (Acento de marca)
    ROSE_ACCENT = RGBColor(217, 140, 127)  # #D98C7F Rosa cálido de interacción
    MUTED = RGBColor(138, 122, 109)        # #8A7A6D Café grisáceo secundario
    BG_BASE = RGBColor(250, 243, 237)      # #FAF3ED Crema cálido de fondo
    SURFACE = RGBColor(255, 253, 251)      # #FFFDFB Blanco cálido de superficie para tarjetas
    WHITE = RGBColor(255, 255, 255)        # Blanco puro
    CARD_BORDER = RGBColor(232, 220, 212)  # #E8DCD4 Borde cálido sutil

    # Acentos funcionales Monchis Café
    PINK_LIGHT = RGBColor(243, 217, 211)   # #F3D9D3 Rosa suave highlight (callouts / insignias)
    SAGE_BG = RGBColor(238, 241, 233)      # #EEF1E9 Verde salvia pastel (tarjeta de resultado oficial)
    SAGE_TEXT = RGBColor(95, 115, 85)      # #5F7355 Verde orgánico oscuro (título de éxito)
    SAGE_BORDER = RGBColor(124, 148, 115)  # #7C9473 Borde verde salvia institucional

    # Resaltado inequívoco para celdas objetivo de la matriz consolidada
    SAGE_TARGET_BG = RGBColor(220, 238, 222)   # #DCEEDE Verde suave distintivo para celda resaltada
    SAGE_TARGET_TEXT = RGBColor(27, 94, 32)    # #1B5E20 Verde bosque profundo para contraste óptimo

    AMBER_BG = RGBColor(254, 243, 225)     # #FEF3E1 Alerta/Nota técnica cálida
    AMBER_TEXT = RGBColor(140, 90, 40)     # #8C5A28 Café ámbar texto
    AMBER_BORDER = RGBColor(230, 200, 170) # #E6C8AA Borde ámbar cálido

    TABLE_ROW_ALT = RGBColor(247, 242, 238)# #F7F2EE Fila zebra cálida

    def add_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_BASE
        bg.line.fill.background()
        return bg

    def create_card(slide, left, top, width, height, bg_rgb=SURFACE, border_rgb=CARD_BORDER, border_width=1):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_rgb
        shape.line.color.rgb = border_rgb
        shape.line.width = Pt(border_width)
        return shape

    def add_header(slide, title_text, category="ACTIVIDAD 2.2 · MODELO COCOMO INTERMEDIO · ADMINISTRACIÓN DE PROYECTOS"):
        # Categoría superior (Breadcrumb corporativo Monchis Café)
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.3))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        p_c = tf_c.paragraphs[0]
        p_c.text = category.upper()
        p_c.font.name = "Calibri"
        p_c.font.size = Pt(10.5)
        p_c.font.bold = True
        p_c.font.color.rgb = TERRACOTTA

        # Título principal de la diapositiva en tipografía Cambria institucional
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.733), Inches(0.65))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Cambria"
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = ESPRESSO

        # Línea separadora decorativa con color Terracota de la marca
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.32), Inches(11.733), Inches(0.035))
        line.fill.solid()
        line.fill.fore_color.rgb = TERRACOTTA
        line.line.fill.background()

    def add_footer(slide, slide_num, total_slides=11):
        # Línea divisoria inferior suave
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.fill.background()

        # Texto del pie izquierdo
        box_l = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(9.0), Inches(0.3))
        tf_l = box_l.text_frame
        tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
        p_l = tf_l.paragraphs[0]
        p_l.text = "Actividad 2.2: Problemas COCOMO Intermedio · Ernesto Fierro · Dr. Gabriel Navarro Salcedo"
        p_l.font.name = "Calibri"
        p_l.font.size = Pt(9.5)
        p_l.font.color.rgb = MUTED

        # Texto del pie derecho con paginación
        box_r = slide.shapes.add_textbox(Inches(10.0), Inches(7.05), Inches(2.533), Inches(0.3))
        tf_r = box_r.text_frame
        tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
        p_r = tf_r.paragraphs[0]
        p_r.text = f"Diapositiva {slide_num} de {total_slides}"
        p_r.alignment = PP_ALIGN.RIGHT
        p_r.font.name = "Calibri"
        p_r.font.size = Pt(9.5)
        p_r.font.color.rgb = MUTED

    def set_speaker_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # Ruta del logo de la marca
    logo_path = os.path.join(os.path.dirname(__file__), "monchis_logo_badge.png")

    # =========================================================================
    # SLIDE 1: PORTADA EJECUTIVA (Layout modular con cero traslape)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_slide_background(s1)

    # Tarjeta principal cálida
    create_card(s1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), bg_rgb=SURFACE, border_rgb=CARD_BORDER)

    # Inclusión del logo institucional de Monchis Café en la esquina superior derecha
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(9.3), Inches(1.2), Inches(2.6), Inches(2.6))

    # Categoría superior
    cat_cov = s1.shapes.add_textbox(Inches(1.3), Inches(1.15), Inches(7.8), Inches(0.35))
    tf_cat = cat_cov.text_frame
    tf_cat.word_wrap = True
    p0 = tf_cat.paragraphs[0]
    p0.text = "INGENIERÍA DE SOFTWARE & ADMINISTRACIÓN DE PROYECTOS"
    p0.font.name = "Calibri"
    p0.font.size = Pt(11.5)
    p0.font.bold = True
    p0.font.color.rgb = TERRACOTTA

    # Título principal en Cambria 24pt (evita desborde y saltos indeseados)
    title_cov = s1.shapes.add_textbox(Inches(1.3), Inches(1.5), Inches(7.8), Inches(0.8))
    tf_tit = title_cov.text_frame
    tf_tit.word_wrap = True
    p1 = tf_tit.paragraphs[0]
    p1.text = "ACTIVIDAD 2.2: COCOMO INTERMEDIO"
    p1.font.name = "Cambria"
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = ESPRESSO

    # Barra decorativa de acento ubicada estrictamente debajo del título
    line_cov = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.3), Inches(2.35), Inches(2.6), Inches(0.04))
    line_cov.fill.solid()
    line_cov.fill.fore_color.rgb = TERRACOTTA
    line_cov.line.fill.background()

    # Subtítulo descriptivo en caja separada
    sub_cov = s1.shapes.add_textbox(Inches(1.3), Inches(2.55), Inches(7.8), Inches(0.95))
    tf_sub = sub_cov.text_frame
    tf_sub.word_wrap = True
    p2 = tf_sub.paragraphs[0]
    p2.text = "Resolución Rigurosa de Casos de Estudio, Calibración de Conductores de Coste (EAF), Ecuaciones de Boehm y Hoja de Cálculo Automatizada"
    p2.font.name = "Calibri"
    p2.font.size = Pt(13.5)
    p2.font.color.rgb = ESPRESSO

    # Bloque de metadatos del estudiante y cátedra
    meta_cov = s1.shapes.add_textbox(Inches(1.3), Inches(3.65), Inches(10.5), Inches(2.7))
    tf_meta = meta_cov.text_frame
    tf_meta.word_wrap = True

    p3 = tf_meta.paragraphs[0]
    p3.text = "• Alumno: Ernesto Fierro                                      • Docente: Dr. Gabriel Navarro Salcedo"
    p3.font.name = "Calibri"
    p3.font.size = Pt(12.5)
    p3.font.bold = True
    p3.font.color.rgb = ESPRESSO
    p3.space_after = Pt(8)

    p4 = tf_meta.add_paragraph()
    p4.text = "• Materia: Administración de Proyectos de Software       • Fecha de Entrega: Octubre de 2026"
    p4.font.name = "Calibri"
    p4.font.size = Pt(12)
    p4.font.color.rgb = ESPRESSO
    p4.space_after = Pt(8)

    p5 = tf_meta.add_paragraph()
    p5.text = "• Componentes Entregables: Presentación Ejecutiva (.pptx) y Hoja de Cálculo Automatizada (.xlsx)"
    p5.font.name = "Calibri"
    p5.font.size = Pt(12)
    p5.font.color.rgb = ESPRESSO
    p5.space_after = Pt(8)

    p6 = tf_meta.add_paragraph()
    p6.text = "• Supuesto Económico: Las unidades monetarias se expresan en Pesos Mexicanos (MXN) para coherencia con la Actividad 2.1."
    p6.font.name = "Calibri"
    p6.font.size = Pt(11)
    p6.font.italic = True
    p6.font.color.rgb = MUTED

    add_footer(s1, 1)
    set_speaker_notes(s1, 
        "DEFENSA ORAL (Minuto 0:00 - 0:45):\n"
        "Buenos días, profesor Gabriel Navarro y compañeros. Presento la resolución formal de la Actividad 2.2: "
        "'Problemas COCOMO Intermedio'. En esta entrega abordamos la estimación de software con rigor matemático, "
        "calibrando el esfuerzo nominal mediante los 15 conductores de coste (EAF), evaluando el tiempo de desarrollo (TDEV) "
        "y determinando los costos económicos en Pesos Mexicanos (MXN). Toda la formulación está sincronizada con una hoja de cálculo "
        "completamente automatizada con celdas y matrices vinculadas."
    )

    # =========================================================================
    # SLIDE 2: FUNDAMENTACIÓN TEÓRICA Y CALIBRACIÓN DE COEFICIENTES
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_background(s2)
    add_header(s2, "Fundamentación Teórica del Modelo COCOMO Intermedio")

    # Panel Izquierdo: Formulación Matemática
    create_card(s2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.35))
    tb_s2_l = s2.shapes.add_textbox(Inches(1.05), Inches(1.7), Inches(5.1), Inches(4.95))
    tf_s2_l = tb_s2_l.text_frame
    tf_s2_l.word_wrap = True

    p = tf_s2_l.paragraphs[0]
    p.text = "Evolución Algorítmica (Barry W. Boehm, 1981)"
    p.font.name = "Cambria"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(10)

    p = tf_s2_l.add_paragraph()
    p.text = "A diferencia del Modelo Básico —que únicamente toma el tamaño (KLOC) como variable independiente—, el Modelo COCOMO Intermedio introduce el Factor de Ajuste del Esfuerzo (EAF) derivado de una matriz de 15 atributos del proyecto, del producto, de la plataforma y del personal."
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(14)

    p = tf_s2_l.add_paragraph()
    p.text = "Ecuación de Esfuerzo Ajustado (Personas-Mes):"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TERRACOTTA

    p = tf_s2_l.add_paragraph()
    p.text = "PM = a · EAF · (KLOC)^b"
    p.font.name = "Consolas"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(12)

    p = tf_s2_l.add_paragraph()
    p.text = "Ecuación de Tiempo de Desarrollo (Meses):"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TERRACOTTA

    p = tf_s2_l.add_paragraph()
    p.text = "TDEV = c · (PM_ajustado)^d"
    p.font.name = "Consolas"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(12)

    p = tf_s2_l.add_paragraph()
    p.text = "Factor de Ajuste del Esfuerzo (EAF):"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TERRACOTTA

    p = tf_s2_l.add_paragraph()
    p.text = "EAF = ∏ (f_i)   para i = 1 hasta 15"
    p.font.name = "Consolas"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO

    # Panel Derecho: Tabla de Coeficientes y Explicación Metodológica
    create_card(s2, Inches(6.65), Inches(1.5), Inches(5.88), Inches(5.35))
    tb_s2_r = s2.shapes.add_textbox(Inches(6.9), Inches(1.7), Inches(5.38), Inches(4.95))
    tf_s2_r = tb_s2_r.text_frame
    tf_s2_r.word_wrap = True

    p = tf_s2_r.paragraphs[0]
    p.text = "Tabla Oficial de Coeficientes de Calibración"
    p.font.name = "Cambria"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(10)

    # Insert Table inside right card
    rows, cols = 4, 5
    tbl_shape = s2.shapes.add_table(rows, cols, Inches(6.9), Inches(2.2), Inches(5.38), Inches(1.9))
    table = tbl_shape.table
    table.columns[0].width = Inches(1.78)
    table.columns[1].width = Inches(0.9)
    table.columns[2].width = Inches(0.9)
    table.columns[3].width = Inches(0.9)
    table.columns[4].width = Inches(0.9)

    tbl_headers = ["Modo Software", "a (PM)", "b (PM)", "c (TDEV)", "d (TDEV)"]
    for c_i, h in enumerate(tbl_headers):
        cell = table.cell(0, c_i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = ESPRESSO
        for p in cell.text_frame.paragraphs:
            p.font.name = "Calibri"
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.alignment = PP_ALIGN.CENTER

    coef_data = [
        ["Orgánico", "3.20", "1.05", "2.50", "0.38"],
        ["Semiacoplado", "3.00", "1.12", "2.50", "0.35"],
        ["Empotrado (Embebido)", "2.80", "1.20", "2.50", "0.32"]
    ]
    for r_i, r_vals in enumerate(coef_data, start=1):
        bg_row = TABLE_ROW_ALT if r_i % 2 == 1 else SURFACE
        for c_i, val in enumerate(r_vals):
            cell = table.cell(r_i, c_i)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_row
            for p in cell.text_frame.paragraphs:
                p.font.name = "Calibri"
                p.font.size = Pt(10)
                p.font.color.rgb = ESPRESSO
                p.alignment = PP_ALIGN.LEFT if c_i == 0 else PP_ALIGN.CENTER

    # Tarjeta explicativa de la diferencia Básico vs Intermedio
    create_card(s2, Inches(6.9), Inches(4.3), Inches(5.38), Inches(2.35), bg_rgb=PINK_LIGHT, border_rgb=ROSE_ACCENT, border_width=1)
    tb_diff = s2.shapes.add_textbox(Inches(7.05), Inches(4.38), Inches(5.1), Inches(2.15))
    tf_diff = tb_diff.text_frame
    tf_diff.word_wrap = True

    p = tf_diff.paragraphs[0]
    p.text = "Justificación Metodológica: ¿Por qué cambian los coeficientes?"
    p.font.name = "Cambria"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TERRACOTTA
    p.space_after = Pt(4)

    p = tf_diff.add_paragraph()
    p.text = "• En la Actividad 2.1 (Modelo Básico), el modo Orgánico utilizaba a = 2.40 y Empotrado a = 3.60, porque ese único coeficiente absorbía el promedio de la complejidad."
    p.font.name = "Calibri"
    p.font.size = Pt(10.5)
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(4)

    p = tf_diff.add_paragraph()
    p.text = "• En el Modelo Intermedio, Boehm recalibra empíricamente las constantes (a = 3.20 en Orgánico y a = 2.80 en Empotrado) para que el factor EAF sea quien ajuste directamente la dispersión ambiental del proyecto."
    p.font.name = "Calibri"
    p.font.size = Pt(10.5)
    p.font.color.rgb = ESPRESSO

    add_footer(s2, 2)
    set_speaker_notes(s2, 
        "DEFENSA ORAL (Minuto 0:45 - 1:30):\n"
        "Es crucial entender la diferencia con respecto a la Actividad 2.1. En el COCOMO Básico, el coeficiente 'a' era de 2.4 para orgánico "
        "porque funcionaba como una constante global agregada. Al pasar al COCOMO Intermedio, Barry Boehm recalibró estas constantes: "
        "el modo Orgánico sube a 3.2 y el Empotrado se reduce a 2.8. La razón matemática es que los 15 conductores de coste (EAF) son quienes "
        "ahora modulan de manera individualizada el esfuerzo real. Además, el tiempo de desarrollo (TDEV) debe calcularse rigurosamente utilizando "
        "el PM ajustado y no el nominal."
    )

    # =========================================================================
    # SLIDE 3: LOS 15 CONDUCTORES DE COSTE (Tipografía ampliada a 12pt)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_background(s3)
    add_header(s3, "Los 15 Conductores de Coste (Cost Drivers) y el Multiplicador EAF")

    categories = [
        ("1. Cualidades del Producto", [
            ("RELY", "Confiabilidad requerida del software", "0.75 a 1.40"),
            ("DATA", "Tamaño de la base de datos", "0.94 a 1.16"),
            ("CPLX", "Complejidad del producto", "0.70 a 1.65")
        ], Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.55)),
        ("2. Cualidades de la Plataforma / Hardware", [
            ("TIME", "Apremios de tiempo de ejecución (Run-time)", "1.00 a 1.66"),
            ("STOR", "Apremios de memoria principal", "1.00 a 1.56"),
            ("VIRT", "Volatilidad de la máquina virtual", "0.87 a 1.30"),
            ("TURN", "Tiempo de respuesta (Turnaround time)", "0.87 a 1.15")
        ], Inches(6.65), Inches(1.5), Inches(5.88), Inches(2.55)),
        ("3. Cualidades del Personal (Human Factors)", [
            ("ACAP", "Capacidad del analista de sistemas", "1.46 a 0.71"),
            ("AEXP", "Experiencia en el tipo de aplicación", "1.29 a 0.82"),
            ("PCAP", "Capacidad de los programadores", "1.42 a 0.70"),
            ("VEXP", "Experiencia en la plataforma virtual", "1.21 a 0.90"),
            ("LEXP", "Experiencia en lenguaje de programación", "1.14 a 0.95")
        ], Inches(0.8), Inches(4.25), Inches(5.6), Inches(2.6)),
        ("4. Cualidades del Proyecto", [
            ("TOOL", "Uso de herramientas modernas de software", "1.24 a 0.82"),
            ("MODP", "Uso de métodos de ingeniería de software", "1.24 a 0.82"),
            ("SCED", "Restricciones de cronograma de desarrollo", "1.23 – 1.00 – 1.10")
        ], Inches(6.65), Inches(4.25), Inches(5.88), Inches(2.6))
    ]

    for cat_title, drivers, left_pos, top_pos, w_pos, h_pos in categories:
        create_card(s3, left_pos, top_pos, w_pos, h_pos)
        tb = s3.shapes.add_textbox(left_pos + Inches(0.2), top_pos + Inches(0.12), w_pos - Inches(0.4), h_pos - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = cat_title
        p.font.name = "Cambria"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = ESPRESSO
        p.space_after = Pt(5)

        for acronym, d_name, r_range in drivers:
            pd = tf.add_paragraph()
            pd.text = f"• [{acronym}] {d_name} "
            pd.font.name = "Calibri"
            pd.font.size = Pt(12)
            pd.font.bold = True
            pd.font.color.rgb = ESPRESSO
            
            run = pd.add_run()
            run.text = f"({r_range})"
            run.font.bold = False
            run.font.color.rgb = MUTED
            pd.space_after = Pt(3)

    add_footer(s3, 3)
    set_speaker_notes(s3, 
        "DEFENSA ORAL (Minuto 1:30 - 2:15):\n"
        "Los 15 conductores de coste de Boehm se organizan en 4 cuadrantes. La escala consta de 6 niveles: "
        "Muy Bajo (1), Bajo (2), Nominal (3 con valor 1.00), Alto (4), Muy Alto (5) y Extra Alto (6). "
        "Nótese un detalle fundamental: en los conductores de producto y hardware, un mayor nivel incrementa el costo (>1.00); "
        "en cambio, en las cualidades del personal (como ACAP y PCAP), una alta capacidad abarata el esfuerzo (0.71), mientras que un personal novato "
        "lo penaliza severamente (hasta 1.46). El EAF resultante es la multiplicación acumulada de estos 15 factores."
    )

    # =========================================================================
    # SLIDE 4: PROBLEMA I (50 KLOC SEMIACOPLADO) — Potencia corregida: 7.1488
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_background(s4)
    add_header(s4, "Problema I — Caso Resuelto de Referencia (50 KLOC Semiacoplado)")

    # Columna Izquierda: Enunciado y Variables EAF
    create_card(s4, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.35))
    tb_p1_l = s4.shapes.add_textbox(Inches(1.05), Inches(1.65), Inches(5.1), Inches(3.0))
    tf_p1_l = tb_p1_l.text_frame
    tf_p1_l.word_wrap = True

    p = tf_p1_l.paragraphs[0]
    p.text = "1. ENUNCIADO OFICIAL (Cátedra Diapositiva 5):"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TERRACOTTA
    p.space_after = Pt(6)

    p = tf_p1_l.add_paragraph()
    p.text = "«Supongamos que tienes un proyecto de software con un tamaño de 50 KLOC, y es un proyecto semiacoplado. Además, tienes las siguientes variables de predicción: confiabilidad requerida (4), tamaño de base de datos (3), y restricciones de tiempo (3). Quieres saber cuánto esfuerzo se requiere para completar el proyecto.»"
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.italic = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(12)

    p = tf_p1_l.add_paragraph()
    p.text = "2. VARIABLES DE PREDICCIÓN IDENTIFICADAS:"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(6)

    p1_drivers = [
        ("Confiabilidad Requerida (RELY):", "Posición (4) [Alto] = 1.15"),
        ("Tamaño de Base de Datos (DATA):", "Posición (3) [Nominal] = 1.00"),
        ("Restricciones de Tiempo:", "Posición (3) [Nominal] = 1.00")
    ]
    for lbl, val in p1_drivers:
        p = tf_p1_l.add_paragraph()
        p.text = f"• {lbl} "
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = ESPRESSO
        run = p.add_run()
        run.text = val
        run.font.bold = False
        run.font.color.rgb = TERRACOTTA
        p.space_after = Pt(3)

    # Tarjeta de aclaración metodológica
    create_card(s4, Inches(1.05), Inches(4.7), Inches(5.1), Inches(1.95), bg_rgb=AMBER_BG, border_rgb=AMBER_BORDER, border_width=1)
    tb_p1_note = s4.shapes.add_textbox(Inches(1.15), Inches(4.75), Inches(4.9), Inches(1.8))
    tf_p1_n = tb_p1_note.text_frame
    tf_p1_n.word_wrap = True

    p = tf_p1_n.paragraphs[0]
    p.text = "Aclaración Técnica sobre «Restricciones de Tiempo»:"
    p.font.name = "Cambria"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = AMBER_TEXT
    p.space_after = Pt(4)

    p = tf_p1_n.add_paragraph()
    p.text = "El enunciado literal señala 'restricciones de tiempo (3)'. En la taxonomía COCOMO de Boehm, la posición (3) [Nominal = 1.00] aplica tanto para TIME (apremios de tiempo de ejecución de CPU) como para SCED (restricciones de calendario de desarrollo). En ambos casos el multiplicador es 1.00 neutro, sin alterar el producto."
    p.font.name = "Calibri"
    p.font.size = Pt(10.5)
    p.font.color.rgb = ESPRESSO

    # Columna Derecha: Modelado Matemático y Resultado
    create_card(s4, Inches(6.65), Inches(1.5), Inches(5.88), Inches(5.35))
    tb_p1_r = s4.shapes.add_textbox(Inches(6.9), Inches(1.65), Inches(5.38), Inches(3.6))
    tf_p1_r = tb_p1_r.text_frame
    tf_p1_r.word_wrap = True

    p = tf_p1_r.paragraphs[0]
    p.text = "3. MODELADO Y RESOLUCIÓN ALGORÍTMICA:"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(8)

    steps_p1 = [
        ("Paso 1: Parámetros Semiacoplado", "a = 3.00, b = 1.12 | c = 2.50, d = 0.35"),
        ("Paso 2: Esfuerzo Nominal (PM_nom)", "PM_nom = 3.0 · (50)^1.12 = 3.0 · 79.9551 = 239.8654 PM"),
        ("Paso 3: Cálculo del EAF", "EAF = 1.15 · 1.00 · 1.00 = 1.1500 (+15.0% de esfuerzo)"),
        ("Paso 4: Esfuerzo Ajustado (PM_ajustado)", "PM = 239.8654 · 1.1500 = 275.8452 ≈ 275.85 PM"),
        ("Paso 5: Tiempo de Desarrollo (TDEV)", "TDEV = 2.50 · (275.8452)^0.35 = 2.5 · 7.1488 = 17.87 Meses")
    ]
    for s_title, s_math in steps_p1:
        p = tf_p1_r.add_paragraph()
        p.text = f"• {s_title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = ESPRESSO
        run = p.add_run()
        run.text = s_math
        run.font.bold = False
        run.font.color.rgb = TERRACOTTA
        p.space_after = Pt(6)

    # Tarjeta de Resultado Oficial en Verde Salvia
    create_card(s4, Inches(6.9), Inches(5.35), Inches(5.38), Inches(1.3), bg_rgb=SAGE_BG, border_rgb=SAGE_BORDER, border_width=1.5)
    tb_p1_res = s4.shapes.add_textbox(Inches(7.05), Inches(5.42), Inches(5.1), Inches(1.15))
    tf_p1_res = tb_p1_res.text_frame
    tf_p1_res.word_wrap = True

    p = tf_p1_res.paragraphs[0]
    p.text = "✔ RESULTADO OFICIAL CONFIRMADO:"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = SAGE_TEXT
    p.space_after = Pt(2)

    p = tf_p1_res.add_paragraph()
    p.text = "Esfuerzo Requerido: 275.85 Personas-Mes (~276 PM)\nTiempo de Desarrollo Calculado: 17.87 Meses (~1.49 años)"
    p.font.name = "Calibri"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO

    add_footer(s4, 4)
    set_speaker_notes(s4, 
        "DEFENSA ORAL (Minuto 2:15 - 3:00):\n"
        "En el Problema I validamos el ejemplo resuelto de la diapositiva 5. Con 50 KLOC y modo Semiacoplado, el esfuerzo nominal es 239.87 PM. "
        "Los factores RELY=1.15, DATA=1.00 y restricciones de tiempo=1.00 generan un EAF de 1.15. Por tanto, el esfuerzo ajustado es 275.85 PM, "
        "lo que coincide al redondear con los 276 persona-mes oficiales. Además, demostramos el cálculo de TDEV: aplicando c=2.50 y d=0.35 sobre "
        "los 275.85 PM ajustados (donde 275.8452 elevado a la 0.35 da 7.1488), obtenemos 17.87 meses de calendario conforme a la metodología COCOMO Intermedio."
    )

    # =========================================================================
    # SLIDE 5: PROBLEMA II (100 KLOC SEMIACOPLADO) — Potencia corregida: 10.1984
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_background(s5)
    add_header(s5, "Problema II — Proyecto Semiacoplado (100 KLOC)")

    # Columna Izquierda: Enunciado y Variables EAF
    create_card(s5, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.35))
    tb_p2_l = s5.shapes.add_textbox(Inches(1.05), Inches(1.65), Inches(5.1), Inches(4.95))
    tf_p2_l = tb_p2_l.text_frame
    tf_p2_l.word_wrap = True

    p = tf_p2_l.paragraphs[0]
    p.text = "1. ENUNCIADO OFICIAL (Cátedra Diapositiva 7):"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TERRACOTTA
    p.space_after = Pt(6)

    p = tf_p2_l.add_paragraph()
    p.text = "«Supongamos que tienes un proyecto de software con un tamaño de 100 KLOC, y es un proyecto de tipo Semi Acoplado. Además, tienes las siguientes variables de predicción: Confiabilidad requerida: 5, Tamaño de base de datos: 4, Complejidad del producto: 3, Apremios de funcionamiento Run-time: 4, Volatilidad de la memoria virtual: 2. Se requiere saber cuánto esfuerzo se requiere para completar el proyecto.»"
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.italic = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(12)

    p = tf_p2_l.add_paragraph()
    p.text = "2. VARIABLES DE PREDICCIÓN IDENTIFICADAS:"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(6)

    p2_drivers = [
        ("Confiabilidad Requerida (RELY):", "Posición (5) [Muy Alto] = 1.40"),
        ("Tamaño Base de Datos (DATA):", "Posición (4) [Alto] = 1.08"),
        ("Complejidad del Producto (CPLX):", "Posición (3) [Nominal] = 1.00"),
        ("Apremios Run-time (TIME):", "Posición (4) [Alto] = 1.11"),
        ("Volatilidad Plataforma Virtual (VIRT):", "Posición (2) [Bajo] = 0.87")
    ]
    for lbl, val in p2_drivers:
        p = tf_p2_l.add_paragraph()
        p.text = f"• {lbl} "
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = ESPRESSO
        run = p.add_run()
        run.text = val
        run.font.bold = False
        run.font.color.rgb = TERRACOTTA
        p.space_after = Pt(3)

    p = tf_p2_l.add_paragraph()
    p.text = "Análisis: La confiabilidad crítica (1.40) y las restricciones de CPU (1.11) penalizan fuertemente, amortiguadas apenas por la baja volatilidad (0.87)."
    p.font.name = "Calibri"
    p.font.size = Pt(10.5)
    p.font.italic = True
    p.font.color.rgb = MUTED
    p.space_before = Pt(8)

    # Columna Derecha: Modelado Matemático y Resultado
    create_card(s5, Inches(6.65), Inches(1.5), Inches(5.88), Inches(5.35))
    tb_p2_r = s5.shapes.add_textbox(Inches(6.9), Inches(1.65), Inches(5.38), Inches(3.6))
    tf_p2_r = tb_p2_r.text_frame
    tf_p2_r.word_wrap = True

    p = tf_p2_r.paragraphs[0]
    p.text = "3. MODELADO Y RESOLUCIÓN ALGORÍTMICA:"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(8)

    steps_p2 = [
        ("Paso 1: Coeficientes Semiacoplado", "a = 3.00, b = 1.12 | c = 2.50, d = 0.35"),
        ("Paso 2: Esfuerzo Nominal (PM_nom)", "PM_nom = 3.0 · (100)^1.12 = 3.0 · 173.7801 = 521.3402 PM"),
        ("Paso 3: Cálculo del EAF", "EAF = 1.40 · 1.08 · 1.00 · 1.11 · 0.87 = 1.460138 ≈ 1.4601"),
        ("Paso 4: Esfuerzo Ajustado (PM_ajustado)", "PM = 521.3402 · 1.460138 = 761.2289 ≈ 761.23 PM"),
        ("Paso 5: Tiempo de Desarrollo (TDEV)", "TDEV = 2.50 · (761.2289)^0.35 = 2.5 · 10.1984 = 25.50 Meses")
    ]
    for s_title, s_math in steps_p2:
        p = tf_p2_r.add_paragraph()
        p.text = f"• {s_title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = ESPRESSO
        run = p.add_run()
        run.text = s_math
        run.font.bold = False
        run.font.color.rgb = TERRACOTTA
        p.space_after = Pt(6)

    # Tarjeta de Resultado Oficial en Verde Salvia
    create_card(s5, Inches(6.9), Inches(5.35), Inches(5.38), Inches(1.3), bg_rgb=SAGE_BG, border_rgb=SAGE_BORDER, border_width=1.5)
    tb_p2_res = s5.shapes.add_textbox(Inches(7.05), Inches(5.42), Inches(5.1), Inches(1.15))
    tf_p2_res = tb_p2_res.text_frame
    tf_p2_res.word_wrap = True

    p = tf_p2_res.paragraphs[0]
    p.text = "✔ RESPUESTA OFICIAL (ESFUERZO):"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = SAGE_TEXT
    p.space_after = Pt(2)

    p = tf_p2_res.add_paragraph()
    p.text = "Esfuerzo Requerido: 761.23 Personas-Mes (~761 PM)\nDuración Estimada: 25.50 Meses (~2.13 años)"
    p.font.name = "Calibri"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO

    add_footer(s5, 5)
    set_speaker_notes(s5, 
        "DEFENSA ORAL (Minuto 3:00 - 3:45):\n"
        "En el Problema II duplicamos el tamaño a 100 KLOC. El esfuerzo nominal pasa a 521.34 PM. "
        "Al aplicar los 5 conductores, el EAF alcanza 1.4601 (+46% sobre el nominal), debido a la alta confiabilidad (1.40) "
        "y apremios de tiempo de ejecución (1.11). El esfuerzo ajustado final es de 761.23 Personas-Mes. "
        "El tiempo de desarrollo formal TDEV, calculado con c=2.50 y d=0.35 sobre el esfuerzo ajustado (761.23 PM, cuya potencia da 10.1984), "
        "resulta en exactamente 25.50 meses (~2.13 años) de calendario."
    )

    # =========================================================================
    # SLIDE 6: PROBLEMA III (300 KLOC EMPOTRADO - TIEMPO)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_background(s6)
    add_header(s6, "Problema III — Proyecto Empotrado / Embebido (300 KLOC)")

    # Columna Izquierda: Enunciado y Variables EAF
    create_card(s6, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.35))
    tb_p3_l = s6.shapes.add_textbox(Inches(1.05), Inches(1.65), Inches(5.1), Inches(4.95))
    tf_p3_l = tb_p3_l.text_frame
    tf_p3_l.word_wrap = True

    p = tf_p3_l.paragraphs[0]
    p.text = "1. ENUNCIADO OFICIAL (Cátedra Diapositiva 8):"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TERRACOTTA
    p.space_after = Pt(6)

    p = tf_p3_l.add_paragraph()
    p.text = "«Tienes un proyecto de software con un tamaño de 300 KLOC, y es un proyecto empotrado. Además, tienes las siguientes variables de predicción: Confiabilidad requerida: 4, Tamaño de base de datos: 5, Complejidad del producto: 2, Capacidad del analista: 1, Volatilidad de la memoria virtual: 3. Quieres saber cuánto tiempo tomará completar el proyecto.»"
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.italic = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(12)

    p = tf_p3_l.add_paragraph()
    p.text = "2. VARIABLES DE PREDICCIÓN IDENTIFICADAS:"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(6)

    p3_drivers = [
        ("Confiabilidad Requerida (RELY):", "Posición (4) [Alto] = 1.15"),
        ("Tamaño Base de Datos (DATA):", "Posición (5) [Muy Alto] = 1.16"),
        ("Complejidad del Producto (CPLX):", "Posición (2) [Bajo] = 0.85"),
        ("Capacidad del Analista (ACAP):", "Posición (1) [Muy Bajo] = 1.46"),
        ("Volatilidad Plataforma Virtual (VIRT):", "Posición (3) [Nominal] = 1.00")
    ]
    for lbl, val in p3_drivers:
        p = tf_p3_l.add_paragraph()
        p.text = f"• {lbl} "
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = ESPRESSO
        run = p.add_run()
        run.text = val
        run.font.bold = False
        run.font.color.rgb = TERRACOTTA
        p.space_after = Pt(3)

    p = tf_p3_l.add_paragraph()
    p.text = "Hallazgo Clave: El analista inexperto (ACAP=1.46) es el mayor factor penalizante individual (+46%), que sumado a DATA (1.16) y RELY (1.15) detona un EAF crítico."
    p.font.name = "Calibri"
    p.font.size = Pt(10.5)
    p.font.italic = True
    p.font.color.rgb = MUTED
    p.space_before = Pt(8)

    # Columna Derecha: Modelado Matemático y Resultado
    create_card(s6, Inches(6.65), Inches(1.5), Inches(5.88), Inches(5.35))
    tb_p3_r = s6.shapes.add_textbox(Inches(6.9), Inches(1.65), Inches(5.38), Inches(3.6))
    tf_p3_r = tb_p3_r.text_frame
    tf_p3_r.word_wrap = True

    p = tf_p3_r.paragraphs[0]
    p.text = "3. MODELADO Y RESOLUCIÓN ALGORÍTMICA:"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(8)

    steps_p3 = [
        ("Paso 1: Coeficientes Empotrado", "a = 2.80, b = 1.20 | c = 2.50, d = 0.32"),
        ("Paso 2: Esfuerzo Nominal (PM_nom)", "PM_nom = 2.8 · (300)^1.20 = 2.8 · 938.7404 = 2,628.4731 PM"),
        ("Paso 3: Cálculo del EAF", "EAF = 1.15 · 1.16 · 0.85 · 1.46 · 1.00 = 1.655494 ≈ 1.6555"),
        ("Paso 4: Esfuerzo Ajustado (PM_ajustado)", "PM = 2,628.4731 · 1.655494 = 4,351.4214 ≈ 4,351.42 PM"),
        ("Paso 5: Tiempo de Desarrollo Solicitado (TDEV)", "TDEV = 2.50 · (4,351.4214)^0.32 = 2.5 · 14.6003 = 36.50 Meses")
    ]
    for s_title, s_math in steps_p3:
        p = tf_p3_r.add_paragraph()
        p.text = f"• {s_title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = ESPRESSO
        run = p.add_run()
        run.text = s_math
        run.font.bold = False
        run.font.color.rgb = TERRACOTTA
        p.space_after = Pt(6)

    # Tarjeta de Resultado Oficial en Verde Salvia
    create_card(s6, Inches(6.9), Inches(5.35), Inches(5.38), Inches(1.3), bg_rgb=SAGE_BG, border_rgb=SAGE_BORDER, border_width=1.5)
    tb_p3_res = s6.shapes.add_textbox(Inches(7.05), Inches(5.42), Inches(5.1), Inches(1.15))
    tf_p3_res = tb_p3_res.text_frame
    tf_p3_res.word_wrap = True

    p = tf_p3_res.paragraphs[0]
    p.text = "✔ RESPUESTA OFICIAL (TIEMPO DE DESARROLLO):"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = SAGE_TEXT
    p.space_after = Pt(2)

    p = tf_p3_res.add_paragraph()
    p.text = "Tiempo Estimado: 36.50 Meses (aprox. 3.04 años)\nEsfuerzo Requerido: 4,351.42 Personas-Mes (EAF = +65.55%)"
    p.font.name = "Calibri"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO

    add_footer(s6, 6)
    set_speaker_notes(s6, 
        "DEFENSA ORAL (Minuto 3:45 - 4:30):\n"
        "En el Problema III se solicita explícitamente el tiempo de desarrollo para un sistema empotrado de 300 KLOC. "
        "El esfuerzo nominal es de 2,628.47 PM. Al evaluar los conductores, la baja capacidad del analista (ACAP=1.46) "
        "representa el mayor castigo individual (+46%), que en sinergia con DATA=1.16 y RELY=1.15 eleva el EAF a 1.6555. "
        "Esto dispara el esfuerzo ajustado a 4,351.42 PM. Al aplicar la fórmula TDEV = 2.5 * (4,351.42)^0.32, el tiempo requerido "
        "es de 36.50 meses, equivalentes a poco más de 3 años continuos de desarrollo."
    )

    # =========================================================================
    # SLIDE 7: PROBLEMA IV (20 KLOC ORGÁNICO) — Potencia corregida: 5.2235
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_background(s7)
    add_header(s7, "Problema IV — Proyecto Orgánico (20 KLOC) y Costo Total")

    # Columna Izquierda: Enunciado y Variables EAF
    create_card(s7, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.35))
    tb_p4_l = s7.shapes.add_textbox(Inches(1.05), Inches(1.65), Inches(5.1), Inches(4.95))
    tf_p4_l = tb_p4_l.text_frame
    tf_p4_l.word_wrap = True

    p = tf_p4_l.paragraphs[0]
    p.text = "1. ENUNCIADO OFICIAL (Cátedra Diapositiva 9):"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TERRACOTTA
    p.space_after = Pt(6)

    p = tf_p4_l.add_paragraph()
    p.text = "«Tienes un proyecto de software con un tamaño de 20 KLOC, y es un proyecto orgánico. Quieres saber cuánto costará completar el proyecto, asumiendo que el costo por persona-mes es de $10,000 MXN. Además, tienes las siguientes variables: Confiabilidad: 1, Tamaño base datos: 5, Complejidad: 2, Apremios Run-time: 4, Capacidad analista: 1, Volatilidad memoria virtual: 2, Uso herramientas: 3.»"
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.italic = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(10)

    p = tf_p4_l.add_paragraph()
    p.text = "2. VARIABLES DE PREDICCIÓN IDENTIFICADAS:"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(4)

    p4_drivers = [
        ("RELY (1) [Muy Bajo] = 0.75", "DATA (5) [Muy Alto] = 1.16"),
        ("CPLX (2) [Bajo] = 0.85", "TIME (4) [Alto] = 1.11"),
        ("ACAP (1) [Muy Bajo] = 1.46", "VIRT (2) [Bajo] = 0.87"),
        ("TOOL (3) [Nominal] = 1.00", "Costo / PM = $10,000.00 MXN")
    ]
    for c1, c2 in p4_drivers:
        p = tf_p4_l.add_paragraph()
        p.text = f"• {c1}  |  {c2}"
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.color.rgb = ESPRESSO
        p.space_after = Pt(3)

    p = tf_p4_l.add_paragraph()
    p.text = "Compensación de Factores: Aunque ACAP (1.46), DATA (1.16) y TIME (1.11) penalizan, se compensan con RELY (0.75), CPLX (0.85) y VIRT (0.87), dejando un EAF neto moderado de 1.0426 (+4.3%)."
    p.font.name = "Calibri"
    p.font.size = Pt(10.5)
    p.font.italic = True
    p.font.color.rgb = MUTED
    p.space_before = Pt(6)

    # Columna Derecha: Modelado Matemático y Resultado
    create_card(s7, Inches(6.65), Inches(1.5), Inches(5.88), Inches(5.35))
    tb_p4_r = s7.shapes.add_textbox(Inches(6.9), Inches(1.65), Inches(5.38), Inches(3.6))
    tf_p4_r = tb_p4_r.text_frame
    tf_p4_r.word_wrap = True

    p = tf_p4_r.paragraphs[0]
    p.text = "3. MODELADO Y RESOLUCIÓN ALGORÍTMICA:"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(8)

    steps_p4 = [
        ("Paso 1: Coeficientes Orgánico", "a = 3.20, b = 1.05 | c = 2.50, d = 0.38"),
        ("Paso 2: Esfuerzo Nominal (PM_nom)", "PM_nom = 3.2 · (20)^1.05 = 3.2 · 23.2317 = 74.3415 PM"),
        ("Paso 3: Cálculo del EAF", "EAF = 0.75·1.16·0.85·1.11·1.46·0.87·1.00 = 1.042637 ≈ 1.0426"),
        ("Paso 4: Esfuerzo Ajustado (PM_ajustado)", "PM = 74.3415 · 1.042637 = 77.51125 ≈ 77.51 PM"),
        ("Paso 5: Respaldo de Tiempo (TDEV)", "TDEV = 2.50 · (77.51125)^0.38 = 2.5 · 5.2235 = 13.06 Meses"),
        ("Paso 6: Costo Total Estimado", "Costo = 77.51125 PM · $10,000 = $775,112.50 MXN")
    ]
    for s_title, s_math in steps_p4:
        p = tf_p4_r.add_paragraph()
        p.text = f"• {s_title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = ESPRESSO
        run = p.add_run()
        run.text = s_math
        run.font.bold = False
        run.font.color.rgb = TERRACOTTA
        p.space_after = Pt(5)

    # Tarjeta de Resultado Oficial en Verde Salvia
    create_card(s7, Inches(6.9), Inches(5.35), Inches(5.38), Inches(1.3), bg_rgb=SAGE_BG, border_rgb=SAGE_BORDER, border_width=1.5)
    tb_p4_res = s7.shapes.add_textbox(Inches(7.05), Inches(5.42), Inches(5.1), Inches(1.15))
    tf_p4_res = tb_p4_res.text_frame
    tf_p4_res.word_wrap = True

    p = tf_p4_res.paragraphs[0]
    p.text = "✔ RESPUESTA OFICIAL (PRESUPUESTO TOTAL):"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = SAGE_TEXT
    p.space_after = Pt(2)

    p = tf_p4_res.add_paragraph()
    p.text = "Costo Total: $775,112.50 MXN ($775,112.00 MXN sin centavos)\nTDEV Respaldado: 13.06 Meses | Esfuerzo: 77.51 Personas-Mes"
    p.font.name = "Calibri"
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO

    add_footer(s7, 7)
    set_speaker_notes(s7, 
        "DEFENSA ORAL (Minuto 4:30 - 5:15):\n"
        "En el Problema IV estimamos el costo de un proyecto orgánico de 20 KLOC a una tarifa de $10,000 MXN por persona-mes. "
        "El esfuerzo nominal es 74.34 PM. Aquí observamos una compensación interesante: DATA (1.16), TIME (1.11) y ACAP (1.46) penalizan, "
        "pero RELY (0.75), CPLX (0.85) y VIRT (0.87) amortiguan el impacto, dejando un EAF neto de 1.0426. "
        "El esfuerzo ajustado resultante es 77.51 PM. Al multiplicarlo por $10,000 obtenemos exactamente $775,112.50 MXN (o $775,112 MXN sin centavos). "
        "Además, respaldamos formalmente el cálculo del tiempo de desarrollo (TDEV): aplicando 2.50 * (77.51)^0.38 (donde la potencia da 5.2235) obtenemos 13.06 meses, "
        "demostrando la factibilidad temporal del proyecto."
    )

    # =========================================================================
    # SLIDE 8: PROBLEMA V (311 KLOC EMPOTRADO - TIEMPO Y COSTO)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_background(s8)
    add_header(s8, "Problema V — Proyecto Empotrado de Gran Escala (311 KLOC)")

    # Columna Izquierda: Enunciado y Variables EAF
    create_card(s8, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.35))
    tb_p5_l = s8.shapes.add_textbox(Inches(1.05), Inches(1.65), Inches(5.1), Inches(4.95))
    tf_p5_l = tb_p5_l.text_frame
    tf_p5_l.word_wrap = True

    p = tf_p5_l.paragraphs[0]
    p.text = "1. ENUNCIADO OFICIAL (Cátedra Diapositiva 10):"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TERRACOTTA
    p.space_after = Pt(6)

    p = tf_p5_l.add_paragraph()
    p.text = "«Tienes un proyecto de software con un tamaño de 311 KLOC, y es un proyecto empotrado. Quieres saber cuánto tiempo y el costo a la hora de completar el proyecto, asumiendo que el costo por persona-mes es de $25,000 MXN. Además, tienes las siguientes variables: Confiabilidad: 1, Tamaño base datos: 5, Complejidad: 2, Apremios Run-time: 4, Capacidad analista: 1, Volatilidad memoria virtual: 2, Uso herramientas: 3, Horario requerido: 4.»"
    p.font.name = "Calibri"
    p.font.size = Pt(11.5)
    p.font.italic = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(10)

    p = tf_p5_l.add_paragraph()
    p.text = "2. VARIABLES DE PREDICCIÓN IDENTIFICADAS:"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(4)

    p5_drivers = [
        ("Mismos 7 factores del Problema IV:", "EAF_base = 1.042637"),
        ("Horario Requerido / Restricciones (SCED):", "Posición (4) [Alto] = 1.04"),
        ("Tarifa por Persona-Mes:", "$25,000.00 MXN / PM")
    ]
    for lbl, val in p5_drivers:
        p = tf_p5_l.add_paragraph()
        p.text = f"• {lbl} "
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = ESPRESSO
        run = p.add_run()
        run.text = val
        run.font.bold = False
        run.font.color.rgb = TERRACOTTA
        p.space_after = Pt(3)

    p = tf_p5_l.add_paragraph()
    p.text = "Impacto de SCED: La compresión de cronograma (SCED=1.04) penaliza con un +4% adicional, elevando el EAF global a 1.0843."
    p.font.name = "Calibri"
    p.font.size = Pt(10.5)
    p.font.italic = True
    p.font.color.rgb = MUTED
    p.space_before = Pt(6)

    # Columna Derecha: Modelado Matemático y Resultado
    create_card(s8, Inches(6.65), Inches(1.5), Inches(5.88), Inches(5.35))
    tb_p5_r = s8.shapes.add_textbox(Inches(6.9), Inches(1.65), Inches(5.38), Inches(3.6))
    tf_p5_r = tb_p5_r.text_frame
    tf_p5_r.word_wrap = True

    p = tf_p5_r.paragraphs[0]
    p.text = "3. MODELADO Y RESOLUCIÓN ALGORÍTMICA:"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO
    p.space_after = Pt(8)

    steps_p5 = [
        ("Paso 1: Coeficientes Empotrado", "a = 2.80, b = 1.20 | c = 2.50, d = 0.32"),
        ("Paso 2: Esfuerzo Nominal (PM_nom)", "PM_nom = 2.8 · (311)^1.20 = 2.8 · 980.1949 = 2,744.5459 PM"),
        ("Paso 3: Cálculo del EAF", "EAF = 1.042637 · 1.04 = 1.084343 ≈ 1.0843 (+8.43%)"),
        ("Paso 4: Esfuerzo Ajustado (PM_ajustado)", "PM = 2,744.5459 · 1.084343 = 2,976.0286 ≈ 2,976.03 PM"),
        ("Paso 5: Tiempo de Desarrollo (TDEV)", "TDEV = 2.50 · (2,976.0286)^0.32 = 2.5 · 12.9289 = 32.32 Meses"),
        ("Paso 6: Costo Económico Total", "Costo = 2,976.0286 PM · $25,000 = $74,400,715.42 MXN")
    ]
    for s_title, s_math in steps_p5:
        p = tf_p5_r.add_paragraph()
        p.text = f"• {s_title}: "
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = ESPRESSO
        run = p.add_run()
        run.text = s_math
        run.font.bold = False
        run.font.color.rgb = TERRACOTTA
        p.space_after = Pt(5)

    # Tarjeta de Resultado Oficial en Verde Salvia
    create_card(s8, Inches(6.9), Inches(5.35), Inches(5.38), Inches(1.3), bg_rgb=SAGE_BG, border_rgb=SAGE_BORDER, border_width=1.5)
    tb_p5_res = s8.shapes.add_textbox(Inches(7.05), Inches(5.42), Inches(5.1), Inches(1.15))
    tf_p5_res = tb_p5_res.text_frame
    tf_p5_res.word_wrap = True

    p = tf_p5_res.paragraphs[0]
    p.text = "✔ RESPUESTAS OFICIALES (TIEMPO Y COSTO TOTAL):"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = SAGE_TEXT
    p.space_after = Pt(2)

    p = tf_p5_res.add_paragraph()
    p.text = "Tiempo Estimado: 32.32 Meses (~2.69 años)\nCosto Total: $74,400,715.42 MXN ($74,400,715.00 MXN sin centavos)"
    p.font.name = "Calibri"
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = ESPRESSO

    add_footer(s8, 8)
    set_speaker_notes(s8, 
        "DEFENSA ORAL (Minuto 5:15 - 6:00):\n"
        "El Problema V representa un megaproyecto empotrado de 311 KLOC a $25,000 MXN por persona-mes. "
        "A los 7 factores anteriores se suma SCED=1.04 por restricciones de cronograma, resultando en un EAF de 1.0843. "
        "El esfuerzo ajustado alcanza 2,976.03 PM. El tiempo estimado de desarrollo es de 32.32 meses (~2.69 años). "
        "Multiplicando el esfuerzo por los $25,000 por PM obtenemos una inversión de $74,400,715.42 MXN ($74,400,715 MXN sin centavos). "
        "Esta cifra ilustra la magnitud económica y el nivel de riesgo que demanda una gobernanza rigurosa en proyectos embebidos de gran escala."
    )

    # =========================================================================
    # SLIDE 9: MATRIZ CONSOLIDADA DE RESULTADOS (Celdas resaltadas en fondo verde)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_slide_background(s9)
    add_header(s9, "Matriz Consolidada de Resultados (Problemas I al V)")

    rows, cols = 6, 8
    tbl_shape9 = s9.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.3))
    t9 = tbl_shape9.table
    col_widths = [Inches(1.85), Inches(1.65), Inches(1.15), Inches(1.45), Inches(1.15), Inches(1.45), Inches(1.35), Inches(1.683)]
    for idx, w in enumerate(col_widths):
        t9.columns[idx].width = w

    headers_t9 = ["Problema", "Modo", "KLOC", "PM Nominal", "Factor EAF", "PM Ajustado", "TDEV (Meses)", "Costo Total (MXN)"]
    for c_i, h in enumerate(headers_t9):
        cell = t9.cell(0, c_i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = ESPRESSO
        for p in cell.text_frame.paragraphs:
            p.font.name = "Calibri"
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.alignment = PP_ALIGN.CENTER

    data_summary = [
        ["Problema I (Ejemplo)", "Semiacoplado", "50.0", "239.87 PM", "1.1500", "275.85 PM", "17.87 Meses", "-"],
        ["Problema II", "Semiacoplado", "100.0", "521.34 PM", "1.4601", "761.23 PM", "25.50 Meses", "-"],
        ["Problema III", "Empotrado", "300.0", "2,628.47 PM", "1.6555", "4,351.42 PM", "36.50 Meses", "-"],
        ["Problema IV", "Orgánico", "20.0", "74.34 PM", "1.0426", "77.51 PM", "13.06 Meses", "$775,112.50"],
        ["Problema V", "Empotrado", "311.0", "2,744.55 PM", "1.0843", "2,976.03 PM", "32.32 Meses", "$74,400,715.42"]
    ]

    for r_i, r_data in enumerate(data_summary, start=1):
        for c_i, val in enumerate(r_data):
            cell = t9.cell(r_i, c_i)
            cell.text = val
            cell.fill.solid()

            # Resaltar la incógnita central pedida por el enunciado en cada problema
            is_target = (
                (r_i == 1 and c_i == 5) or
                (r_i == 2 and c_i == 5) or
                (r_i == 3 and c_i == 6) or
                (r_i == 4 and c_i == 7) or
                (r_i == 5 and c_i in [6, 7])
            )

            if is_target:
                cell.fill.fore_color.rgb = SAGE_TARGET_BG
                for p in cell.text_frame.paragraphs:
                    p.font.name = "Calibri"
                    p.font.size = Pt(10.5)
                    p.font.bold = True
                    p.font.color.rgb = SAGE_TARGET_TEXT
                    p.alignment = PP_ALIGN.LEFT if c_i <= 1 else PP_ALIGN.CENTER
            else:
                bg_r = TABLE_ROW_ALT if r_i % 2 == 1 else SURFACE
                cell.fill.fore_color.rgb = bg_r
                for p in cell.text_frame.paragraphs:
                    p.font.name = "Calibri"
                    p.font.size = Pt(10)
                    p.font.color.rgb = ESPRESSO
                    p.alignment = PP_ALIGN.LEFT if c_i <= 1 else PP_ALIGN.CENTER

    # Tarjeta de notas y supuestos al pie de la matriz
    create_card(s9, Inches(0.8), Inches(5.95), Inches(11.733), Inches(0.9), bg_rgb=SURFACE, border_rgb=CARD_BORDER, border_width=1)
    tb_pie = s9.shapes.add_textbox(Inches(0.95), Inches(6.0), Inches(11.4), Inches(0.8))
    tf_pie = tb_pie.text_frame
    tf_pie.word_wrap = True

    pp0 = tf_pie.paragraphs[0]
    pp0.text = "NOTAS TÉCNICAS Y REVISIÓN DE INTEGRIDAD METODOLÓGICA:"
    pp0.font.name = "Cambria"
    pp0.font.size = Pt(10)
    pp0.font.bold = True
    pp0.font.color.rgb = ESPRESSO
    pp0.space_after = Pt(2)

    pp1 = tf_pie.add_paragraph()
    pp1.text = "1. Consistencia de TDEV: Los tiempos de desarrollo TDEV corresponden formalmente a la ecuación c · (PM_ajustado)^d (17.87, 25.50, 36.50, 13.06 y 32.32 Meses), unificando unidades e integridad de cálculo.\n2. Formato de Costos y Moneda: Cifras en Pesos Mexicanos (MXN). Problema IV da exactamente $775,112.50 MXN ($775,112.00 sin centavos) y Problema V da $74,400,715.42 MXN ($74,400,715.00 sin centavos). Las celdas resaltadas en fondo verde destacan las incógnitas solicitadas en cada caso."
    pp1.font.name = "Calibri"
    pp1.font.size = Pt(9)
    pp1.font.color.rgb = ESPRESSO

    add_footer(s9, 9)
    set_speaker_notes(s9, 
        "DEFENSA ORAL (Minuto 6:00 - 6:45):\n"
        "Esta matriz consolida los 5 problemas de la actividad. Destacamos la consistencia metodológica de la columna TDEV, "
        "donde cada valor se obtiene formalmente a partir del PM ajustado correspondiente: 17.87 meses para el Problema I, "
        "25.50 meses para el Problema II, 36.50 meses para el Problema III, 13.06 meses para el Problema IV y 32.32 meses para el Problema V. "
        "El formato de la columna TDEV se encuentra unificado en 'Meses', los costos se especifican con su desglose decimal exacto "
        "y su expresión entera sin centavos en MXN, y las celdas resaltadas en verde destacan las respuestas oficiales solicitadas por la cátedra."
    )

    # =========================================================================
    # SLIDE 10: CONCLUSIONES TÉCNICAS Y RECOMENDACIONES DE GESTIÓN
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_slide_background(s10)
    add_header(s10, "Conclusiones Técnicas, Análisis de Sensibilidad y Gobernanza")

    conclusions = [
        ("1. Sensibilidad y Multiplicadores Críticos del EAF",
         "En el Problema III, la baja capacidad del analista (ACAP=1.46) fue el multiplicador individual más costoso (+46%), que aunado a altas demandas de base de datos (DATA=1.16) y confiabilidad (RELY=1.15), incrementó el esfuerzo total un +65.5% sobre el nominal (de 2,628 a 4,351 PM), evidenciando la alta sensibilidad del modelo ante brechas en competencias analíticas."),
        ("2. Compensación Estratégica y Balance de Factores",
         "En el Problema IV, factores fuertemente desfavorables como la inexperiencia analítica (ACAP=1.46), gran volumen de datos (DATA=1.16) y apremios de CPU (TIME=1.11) fueron amortiguados eficazmente por requisitos relajados de confiabilidad (RELY=0.75), baja complejidad de software (CPLX=0.85) y ambiente virtual estable (VIRT=0.87), conteniendo el EAF neto en un moderado 1.0426 (+4.3%)."),
        ("3. Deseconomías de Escala en Proyectos de 300 KLOC o Más",
         "En proyectos de 300 KLOC o más (Problemas III y V), el exponente b=1.20 impone un crecimiento superlineal con marcadas deseconomías de escala (ley de potencias de Boehm). Esto se evidencia en el Problema III (300 KLOC) requiriendo 4,351.42 PM (36.50 meses) debido a la penalización de factores analíticos, y en el Problema V (311 KLOC) demandando 2,976.03 PM con una inversión de $74.4 M MXN (32.32 meses)."),
        ("4. Importancia de la Automatización y Control Algorítmico",
         "La vinculación dinámica de celdas y tablas paramétricas en la hoja de cálculo (.xlsx) elimina el error humano en operaciones exponenciales encadenadas, garantiza trazabilidad algorítmica y permite a los líderes de proyecto evaluar escenarios 'What-If' antes de comprometer recursos y calendarios.")
    ]

    col_w = Inches(5.6)
    col_w_r = Inches(5.88)
    card_h = Inches(2.25)

    coords = [
        (Inches(0.8), Inches(1.5), col_w),
        (Inches(6.65), Inches(1.5), col_w_r),
        (Inches(0.8), Inches(3.9), col_w),
        (Inches(6.65), Inches(3.9), col_w_r)
    ]

    for idx, (title, desc) in enumerate(conclusions):
        l, t, w = coords[idx]
        create_card(s10, l, t, w, card_h)
        tb = s10.shapes.add_textbox(l + Inches(0.2), t + Inches(0.12), w - Inches(0.4), card_h - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Cambria"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = ESPRESSO
        p.space_after = Pt(4)

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = "Calibri"
        p_desc.font.size = Pt(10.5)
        p_desc.font.color.rgb = ESPRESSO

    # Referencias al pie
    create_card(s10, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.65), bg_rgb=PINK_LIGHT, border_rgb=ROSE_ACCENT, border_width=1)
    tb_ref = s10.shapes.add_textbox(Inches(0.95), Inches(6.3), Inches(11.4), Inches(0.55))
    tf_ref = tb_ref.text_frame
    tf_ref.word_wrap = True
    p = tf_ref.paragraphs[0]
    p.text = "Referencias Normativas: Boehm, B. W. (1981). Software Engineering Economics. Prentice-Hall · Pressman, R. S. (2020). Software Engineering: A Practitioner's Approach. McGraw-Hill · Navarro Salcedo, G. (2026). Material de Cátedra de COCOMO Intermedio."
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.color.rgb = ESPRESSO

    add_footer(s10, 10)
    set_speaker_notes(s10, 
        "DEFENSA ORAL (Minuto 6:45 - 7:30):\n"
        "Para concluir nuestra defensa, extraemos cuatro lecciones cardinales de ingeniería de software. "
        "Primero: el factor humano es crítico; un analista novato (ACAP=1.46) representó el mayor sobrecosto individual en el caso de 300 KLOC. "
        "Segundo: los conductores interactúan en un delicado equilibrio; en el Problema IV factores favorables compensaron factores negativos. "
        "Tercero: en proyectos de 300 KLOC o más, el modelo empotrado impone un crecimiento superlineal por deseconomías de escala bajo la ley de potencia. "
        "Y cuarto: la automatización rigurosa en Excel elimina errores de desfase y habilita simulaciones de mitigación en tiempo real. Muchas gracias."
    )

    # =========================================================================
    # SLIDE 11: SÍNTESIS COMPARATIVA BÁSICO (ACT. 2.1) VS INTERMEDIO (ACT. 2.2)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_slide_background(s11)
    add_header(s11, "Síntesis Comparativa: COCOMO Básico (Act. 2.1) vs COCOMO Intermedio (Act. 2.2)")

    # Tabla Comparativa Central
    rows11, cols11 = 5, 4
    tbl_shape11 = s11.shapes.add_table(rows11, cols11, Inches(0.8), Inches(1.5), Inches(11.733), Inches(3.2))
    t11 = tbl_shape11.table
    t11.columns[0].width = Inches(2.333)
    t11.columns[1].width = Inches(3.1)
    t11.columns[2].width = Inches(3.2)
    t11.columns[3].width = Inches(3.1)

    headers_11 = ["Dimensión de Comparación", "COCOMO Básico (Actividad 2.1)", "COCOMO Intermedio (Actividad 2.2)", "Impacto en la Gestión"]
    for c_i, h in enumerate(headers_11):
        cell = t11.cell(0, c_i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = ESPRESSO
        for p in cell.text_frame.paragraphs:
            p.font.name = "Calibri"
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.alignment = PP_ALIGN.CENTER

    comp_data = [
        ["Variables de Entrada", "Únicamente KLOC (tamaño de líneas de código fuente)", "KLOC + 15 Conductores de Coste agrupados en el EAF", "Permite modelar el contexto humano, técnico y operativo real"],
        ["Ecuación de Esfuerzo", "PM = a · (KLOC)^b", "PM = a · EAF · (KLOC)^b", "Modula el esfuerzo según conductores (en estos casos osciló entre +4% y +66%)"],
        ["Calibración de 'a'", "Orgánico: a = 2.40 | Empotrado: a = 3.60", "Orgánico: a = 3.20 | Empotrado: a = 2.80", "Boehm recalibra para permitir la modulación limpia del EAF"],
        ["Tiempo de Desarrollo", "TDEV = c · (PM)^d", "TDEV = c · (PM_ajustado)^d", "Garantiza coherencia entre personal real y duración de calendario"]
    ]

    for r_i, r_data in enumerate(comp_data, start=1):
        bg_r = TABLE_ROW_ALT if r_i % 2 == 1 else SURFACE
        for c_i, val in enumerate(r_data):
            cell = t11.cell(r_i, c_i)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_r
            for p in cell.text_frame.paragraphs:
                p.font.name = "Calibri"
                p.font.size = Pt(10)
                p.font.color.rgb = ESPRESSO
                p.alignment = PP_ALIGN.LEFT if c_i <= 1 else PP_ALIGN.LEFT

    # Tarjeta de Conclusión de Cierre
    create_card(s11, Inches(0.8), Inches(4.9), Inches(11.733), Inches(1.9), bg_rgb=SURFACE, border_rgb=TERRACOTTA, border_width=1.5)
    tb_close = s11.shapes.add_textbox(Inches(1.0), Inches(5.0), Inches(11.333), Inches(1.7))
    tf_close = tb_close.text_frame
    tf_close.word_wrap = True

    p = tf_close.paragraphs[0]
    p.text = "CONCLUSIÓN METODOLÓGICA FINAL:"
    p.font.name = "Cambria"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TERRACOTTA
    p.space_after = Pt(4)

    p = tf_close.add_paragraph()
    p.text = "El Modelo COCOMO Intermedio supera con creces las limitaciones del Modelo Básico al transformar estimaciones estáticas en modelos dinámicos sensibles a la realidad del equipo de ingeniería. La automatización en hoja de cálculo desarrollada en esta actividad dota a la dirección del proyecto de una herramienta formal, auditable y calibrada para la toma de decisiones estratégicas, negociación de honorarios y cumplimiento estricto de cronogramas."
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.color.rgb = ESPRESSO

    add_footer(s11, 11)
    set_speaker_notes(s11, 
        "DEFENSA ORAL (Minuto 7:30 - 8:00):\n"
        "Esta diapositiva final sintetiza la transición metodológica entre la Actividad 2.1 y la 2.2. "
        "Demuestra cómo el modelo COCOMO evoluciona desde una simple regla de tamaño hacia un framework integral de gobernanza "
        "de proyectos de software. Con esto dejamos completamente resuelta la actividad con los máximos criterios de exactitud, "
        "diseño profesional y claridad expositiva. Quedo atento a sus preguntas, Dr. Gabriel Navarro."
    )

    # Guardar presentación en repositorio y Downloads
    out_pptx = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_2_2_Problemas_COCOMO_Intermedio.pptx"
    downloads_pptx = r"C:\Users\erfierro\Downloads\Actividad_2_2_Problemas_COCOMO_Intermedio.pptx"
    prs.save(out_pptx)
    shutil.copy2(out_pptx, downloads_pptx)
    print("Presentación PPTX generada exitosamente en:", out_pptx)
    print("Copia creada en Downloads:", downloads_pptx)

if __name__ == "__main__":
    build_presentation()
