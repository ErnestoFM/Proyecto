import sys, os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def generate_presentation():
    src_path = r'c:\Users\hatue\Documents\cafeteria\Proyecto\docs\entregables\Monchis_Cafe.pptx'
    out_path = r'c:\Users\hatue\Documents\cafeteria\Proyecto\docs\entregables\Monchis_Cafe.pptx'
    downloads_path = r'c:\Users\hatue\Downloads\Monchis_Cafe_Presentacion_Rediseñada.pptx'
    backup_path = r'c:\Users\hatue\Documents\cafeteria\Proyecto\docs\entregables\Monchis_Cafe_Presentacion_Rediseñada_20slides_backup.pptx'

    # Save backup first if not exists
    if not os.path.exists(backup_path):
        import shutil
        shutil.copyfile(src_path, backup_path)
        print(f"Respaldo creado en: {backup_path}")

    # Use the 20-slide base presentation
    base_file = backup_path if os.path.exists(backup_path) else src_path
    prs = Presentation(base_file)

    # Colores corporativos institucionales Monchis Café
    BG_COLOR = RGBColor(0xFB, 0xF1, 0xEC)       # #FBF1EC Fondo crema cálido
    TERRACOTTA = RGBColor(0xC9, 0x75, 0x67)     # #C97567 Terracota / Coral primario
    SOFT_CORAL = RGBColor(0xE0, 0x8D, 0x80)     # #E08D80 Coral suave
    DARK_COFFEE = RGBColor(0x4B, 0x3B, 0x33)    # #4B3B33 Café oscuro títulos
    WARM_MOCHA = RGBColor(0x5B, 0x4A, 0x41)     # #5B4A41 Café texto
    MUTED_COFFEE = RGBColor(0x8A, 0x77, 0x6D)   # #8A776D Café secundario
    SAGE_GREEN = RGBColor(0x7C, 0x94, 0x73)     # #7C9473 Verde ODS 12
    DARK_SAGE = RGBColor(0x5F, 0x73, 0x55)      # #5F7355 Verde oscuro DevSecOps
    CARD_BG = RGBColor(0xFF, 0xFF, 0xFF)        # Blanco puro
    CARD_BG_ALT = RGBColor(0xF3, 0xD9, 0xD3)    # Rosa crema
    CARD_BORDER = RGBColor(0xE8, 0xDC, 0xD4)    # Borde sutil
    NAVY_TECH = RGBColor(0x2B, 0x4C, 0x6F)      # Azul técnico DevOps
    NAVY_LIGHT = RGBColor(0xEA, 0xF0, 0xF8)     # Fondo azul suave
    AMBER_ALERT = RGBColor(0xD9, 0x77, 0x24)    # Ámbar alerta

    def set_slide_bg(slide):
        bg = slide.background
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR

    def add_header(slide, category_text, title_text):
        # Category header
        cat_box = slide.shapes.add_textbox(Emu(548640), Emu(292608), Emu(10058400), Emu(274320))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.name = "Calibri"
        p_c.font.size = Pt(10.5)
        p_c.font.bold = True
        p_c.font.color.rgb = TERRACOTTA

        # Title
        title_box = slide.shapes.add_textbox(Emu(548640), Emu(566928), Emu(11064240), Emu(640080))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Cambria"
        p_t.font.size = Pt(25.0)
        p_t.font.bold = True
        p_t.font.color.rgb = DARK_COFFEE

    def add_footer(slide, slide_num):
        # Left footer
        f_box = slide.shapes.add_textbox(Emu(548640), Emu(6492240), Emu(7315200), Emu(256032))
        tf_f = f_box.text_frame
        tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
        p_f = tf_f.paragraphs[0]
        p_f.text = "Monchis Café — Producto Integrador · Administración y DevOps"
        p_f.font.name = "Calibri"
        p_f.font.size = Pt(8.5)
        p_f.font.color.rgb = MUTED_COFFEE

        # Right footer (slide number)
        n_box = slide.shapes.add_textbox(Emu(11183112), Emu(6492240), Emu(548640), Emu(256032))
        tf_n = n_box.text_frame
        tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
        p_n = tf_n.paragraphs[0]
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.text = str(slide_num)
        p_n.font.name = "Calibri"
        p_n.font.size = Pt(8.5)
        p_n.font.color.rgb = MUTED_COFFEE

    # =========================================================================
    # 1. SLIDE 20: MATRIZ DE ZACHMAN (CUADRÍCULA 4x6)
    # =========================================================================
    slide_z1 = prs.slides.add_slide(prs.slide_layouts[0])
    set_slide_bg(slide_z1)
    add_header(slide_z1, "PRODUCTO INTEGRADOR — ARQUITECTURA DE SOFTWARE", "17. Arquitectura Empresarial: Matriz de Zachman (4 Capas × 6 Interrogantes)")
    add_footer(slide_z1, 20)

    # Sub-banner introductorio
    banner = slide_z1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(548640), Emu(1250000), Emu(11094720), Emu(360000))
    banner.fill.solid()
    banner.fill.fore_color.rgb = CARD_BG_ALT
    banner.line.color.rgb = CARD_BORDER
    banner.line.width = Pt(0.75)
    tf_b = banner.text_frame
    tf_b.margin_left = Emu(120000); tf_b.margin_top = Emu(40000)
    p_b = tf_b.paragraphs[0]
    p_b.text = "Actividad 3.5 — Matriz de Zachman aplicada a los requerimientos de Monchis Café (Equipo 2) · Estructura ortogonal completa de 24 artefactos"
    p_b.font.name = "Calibri"
    p_b.font.size = Pt(10.0)
    p_b.font.bold = True
    p_b.font.color.rgb = DARK_COFFEE

    x_level_w = Emu(1450000)
    col_w = Emu(1560000)
    col_gap = Emu(40000)
    start_x = Emu(548640)
    start_y = Emu(1680000)
    header_h = Emu(320000)
    row_h = Emu(1080000)
    row_gap = Emu(40000)

    # Encabezados de Columna (Interrogantes)
    columns_info = [
        ("QUÉ (Datos)", "Catálogo y Modelo", TERRACOTTA),
        ("CÓMO (Función)", "Procesos y Flujos", DARK_COFFEE),
        ("DÓNDE (Red)", "Topología y Paquetes", NAVY_TECH),
        ("QUIÉN (Personas)", "Roles y Permisos", DARK_SAGE),
        ("CUÁNDO (Tiempo)", "Eventos y Estados", AMBER_ALERT),
        ("POR QUÉ (Motivación)", "Objetivos y Reglas", SAGE_GREEN)
    ]

    # Corner box
    corner = slide_z1.shapes.add_shape(MSO_SHAPE.RECTANGLE, start_x, start_y, x_level_w, header_h)
    corner.fill.solid()
    corner.fill.fore_color.rgb = DARK_COFFEE
    corner.line.color.rgb = DARK_COFFEE
    tf_c = corner.text_frame
    tf_c.margin_left = Emu(50000); tf_c.margin_top = Emu(40000)
    p_c = tf_c.paragraphs[0]
    p_c.text = "NIVEL / PREGUNTA"
    p_c.font.name = "Calibri"
    p_c.font.size = Pt(9.0)
    p_c.font.bold = True
    p_c.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for c_idx, (col_title, col_sub, col_color) in enumerate(columns_info):
        cx = start_x + x_level_w + col_gap + c_idx * (col_w + col_gap)
        c_box = slide_z1.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, start_y, col_w, header_h)
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = col_color
        c_box.line.color.rgb = col_color
        tf = c_box.text_frame
        tf.margin_left = Emu(40000); tf.margin_top = Emu(30000)
        p1 = tf.paragraphs[0]
        p1.text = col_title
        p1.font.name = "Calibri"
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p1.alignment = PP_ALIGN.CENTER

    # Filas y Contenido (Exacto al PDF)
    rows_data = [
        {
            "level": "INTENCIÓN",
            "desc": "Visión del Planificador\n(Contextual)",
            "cells": [
                ("Características:", "Catálogo segmentado, POS multipago, Rewards ODS 12, trazabilidad y seguridad stateless."),
                ("Listado Proceso Negocio:", "PN-01 a PN-06: Abastecimiento, venta mostrador, sellos Rewards, mermas PEPS y corte de caja."),
                ("Diagramas de Contexto:", "DFD Nivel 0 con entidades externas: Cliente, Cajero, Admin, Cooperativas, Banco SPEI y Google."),
                ("Workflow (roles y act):", "Flujo de trabajo operativo entre los 4 roles humanos y Matriz RACI para 10 tareas clave."),
                ("Listado de Eventos:", "10 eventos de negocio (EVT-01..10): Apertura caja, termo reusable, cobro, alertas y corte Z."),
                ("Visión. Objetivos:", "Misión, visión, 4 objetivos SMART y alineación estratégica con ODS 12 (Metas 12.2, 12.3 y 12.5).")
            ]
        },
        {
            "level": "ALCANCE",
            "desc": "Visión del Dueño\n(Conceptual)",
            "cells": [
                ("Listado Requerimientos:", "Catálogo de 15 Requerimientos Funcionales (RF-01 a RF-15) con actores y criterios de éxito."),
                ("Diagramas de Actividad:", "DA-01 Venta en Mostrador con Bono Ecológico y DA-02 Abastecimiento de Café con Alerta PEPS."),
                ("Ambiente Operativo RNF:", "GCP Cloud Run, Docker Compose local y 7 RNF bajo la norma internacional ISO/IEC 25010."),
                ("Rol de Negocio:", "Fichas de caracterización de Administrador, Cajero de Turno, Cliente y Proveedor Campesino."),
                ("Cronograma de Negocio:", "4 fases de adopción en 16 semanas, hitos de negocio y ciclo diario de horarios en cafetería."),
                ("Prioridades de Negocio:", "Jerarquización formal MoSCoW (Must, Should, Could, Won't Have) y matriz de valor vs esfuerzo.")
            ]
        },
        {
            "level": "ALTO NIVEL",
            "desc": "Visión del Diseñador\n(Lógica)",
            "cells": [
                ("Listado Casos de Uso:", "Catálogo consolidado de 12 Casos de Uso (CU-01 a CU-12) cruzados con los requerimientos."),
                ("Especificación CU Principales:", "Plantillas formales Cockburn para CU-01 (Login reCAPTCHA), CU-03/04 (POS) y CU-12 (Reversa Saga)."),
                ("Subsistema, Módulo:", "Arquitectura Monorepo desacoplada: apps/web, apps/api, packages/database y packages/messaging."),
                ("Actores Descripción:", "Caracterización de 8 actores (humanos y sistemas/servicios) y matriz de interacción cruzada."),
                ("Precedencia Casos de Uso:", "Reglas de precedencia obligatoria, inclusión <<include>>, extensión <<extend>> y grafo dirigido."),
                ("Reglas del Negocio:", "8 reglas de negocio (RN-01 a RN-08) y jerarquización por nivel de prioridad crítica (P1, P2, P3).")
            ]
        },
        {
            "level": "DETALLE",
            "desc": "Visión del Constructor\n(Física)",
            "cells": [
                ("CU, Prototipos y Dominio:", "Diagrama UML global, wireframes reales de POS y Login, y MER relacional de base de datos."),
                ("Navegación y Rutas:", "Grafo de navegación en Vue Router 4, guardianes de ruta (beforeEach) y atajos de teclado (F2, Esc)."),
                ("Diagrama de Paquetes:", "Diagrama de paquetes UML @monchis/* bajo el Principio de Dependencias Acíclicas (ADP)."),
                ("Permisos y Roles (RBAC):", "Matriz CRUD de permisos RBAC por endpoint de API y rutas web, con principio de menor privilegio."),
                ("Diagrama de Estados:", "Autómatas finitos del ciclo de vida de una Orden de Venta (Order) y de un Lote de Café (Batch)."),
                ("Reglas en Modelo Análisis:", "Trazabilidad de las 8 reglas a código TypeScript, restricciones Prisma y pruebas Vitest.")
            ]
        }
    ]

    for r_idx, r_data in enumerate(rows_data):
        ry = start_y + header_h + row_gap + r_idx * (row_h + row_gap)

        # Level header card
        l_box = slide_z1.shapes.add_shape(MSO_SHAPE.RECTANGLE, start_x, ry, x_level_w, row_h)
        l_box.fill.solid()
        l_box.fill.fore_color.rgb = CARD_BG_ALT if r_idx % 2 == 0 else RGBColor(0xEA, 0xDC, 0xD4)
        l_box.line.color.rgb = TERRACOTTA
        l_box.line.width = Pt(1.0)
        tf_l = l_box.text_frame
        tf_l.margin_left = Emu(60000); tf_l.margin_top = Emu(80000)
        p_l1 = tf_l.paragraphs[0]
        p_l1.text = r_data["level"]
        p_l1.font.name = "Cambria"
        p_l1.font.size = Pt(10.5)
        p_l1.font.bold = True
        p_l1.font.color.rgb = DARK_COFFEE

        p_l2 = tf_l.add_paragraph()
        p_l2.text = r_data["desc"]
        p_l2.font.name = "Calibri"
        p_l2.font.size = Pt(8.0)
        p_l2.font.color.rgb = WARM_MOCHA

        # Cells
        for c_idx, (cell_title, cell_body) in enumerate(r_data["cells"]):
            cx = start_x + x_level_w + col_gap + c_idx * (col_w + col_gap)
            c_card = slide_z1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, ry, col_w, row_h)
            c_card.fill.solid()
            c_card.fill.fore_color.rgb = CARD_BG
            c_card.line.color.rgb = CARD_BORDER
            c_card.line.width = Pt(0.75)

            tf_c = c_card.text_frame
            tf_c.word_wrap = True
            tf_c.margin_left = Emu(60000); tf_c.margin_top = Emu(50000)
            tf_c.margin_right = Emu(60000); tf_c.margin_bottom = Emu(30000)

            p_t = tf_c.paragraphs[0]
            p_t.text = cell_title
            p_t.font.name = "Calibri"
            p_t.font.size = Pt(8.0)
            p_t.font.bold = True
            p_t.font.color.rgb = TERRACOTTA

            p_b = tf_c.add_paragraph()
            p_b.text = cell_body
            p_b.font.name = "Calibri"
            p_b.font.size = Pt(7.0)
            p_b.font.color.rgb = WARM_MOCHA

    # =========================================================================
    # 2. SLIDE 21: JUSTIFICACIÓN CONCEPTUAL Y COHERENCIA DE ZACHMAN
    # =========================================================================
    slide_z2 = prs.slides.add_slide(prs.slide_layouts[0])
    set_slide_bg(slide_z2)
    add_header(slide_z2, "PRODUCTO INTEGRADOR — ARQUITECTURA DE SOFTWARE", "18. Matriz de Zachman: Trazabilidad Vertical, Horizontal y Marco Teórico")
    add_footer(slide_z2, 21)

    # Top summary banner
    top_b = slide_z2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(548640), Emu(1250000), Emu(11094720), Emu(720000))
    top_b.fill.solid()
    top_b.fill.fore_color.rgb = CARD_BG_ALT
    top_b.line.color.rgb = TERRACOTTA
    top_b.line.width = Pt(1.0)
    tf_tb = top_b.text_frame
    tf_tb.margin_left = Emu(120000); tf_tb.margin_top = Emu(80000); tf_tb.margin_right = Emu(120000)
    p_tb1 = tf_tb.paragraphs[0]
    p_tb1.text = "Justificación Conceptual y Metodológica (Zachman, 1987)"
    p_tb1.font.name = "Cambria"
    p_tb1.font.size = Pt(12.0)
    p_tb1.font.bold = True
    p_tb1.font.color.rgb = DARK_COFFEE

    p_tb2 = tf_tb.add_paragraph()
    p_tb2.text = "La Matriz de Zachman aplicada a la ingeniería de requerimientos organiza la arquitectura de Monchis Café mediante una estructura bidimensional ortogonal que garantiza completitud, coherencia vertical (trazabilidad entre niveles de abstracción) y coherencia horizontal (respuestas complementarias a las 6 preguntas clásicas de comunicación)."
    p_tb2.font.name = "Calibri"
    p_tb2.font.size = Pt(9.5)
    p_tb2.font.color.rgb = WARM_MOCHA

    # Dos Columnas Principales: Coherencia Vertical y Coherencia Horizontal
    card_w = Emu(5447360)
    card_gap = Emu(200000)
    card_y = Emu(2100000)
    card_h = Emu(3400000)

    # Columna 1: Coherencia entre Capas (Vertical)
    c1 = slide_z2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(548640), card_y, card_w, card_h)
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = CARD_BORDER
    c1.line.width = Pt(1.0)
    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = Emu(140000); tf_c1.margin_top = Emu(120000); tf_c1.margin_right = Emu(140000)

    p = tf_c1.paragraphs[0]
    p.text = "1. Coherencia entre Capas (Trazabilidad Vertical)"
    p.font.name = "Cambria"
    p.font.size = Pt(13.0)
    p.font.bold = True
    p.font.color.rgb = DARK_COFFEE

    vertical_points = [
        ("Nivel 1 — Intención (Visión del Planificador):", " Establece el contexto macro del negocio de cafetería familiar y el modelo de comercio justo con cooperativas campesinas de Chiapas/Oaxaca, delimitando qué existe, cómo opera y por qué es rentable y sostenible bajo el ODS 12 (Sapag Chain, 2011)."),
        ("Nivel 2 — Alcance (Visión del Dueño del Negocio):", " Traduce las intenciones en especificaciones comerciales: los 15 Requerimientos Funcionales, diagramas de actividad de mostrador, el ambiente operativo bajo ISO/IEC 25010 y priorización MoSCoW para construir primero lo innegociable (Wiegers & Beatty, 2013)."),
        ("Nivel 3 — Alto Nivel (Visión del Diseñador del Sistema):", " Modela la solución lógica orientada a objetos: el catálogo de 12 Casos de Uso, la arquitectura modular de Monorepo, los actores primarios/secundarios, precedencia y las 8 reglas de negocio (Ross, 2003; Larman, 2004)."),
        ("Nivel 4 — Detalle (Visión del Constructor de Software):", " Aterriza las abstracciones en artefactos de implementación directa: esquemas relacionales en PostgreSQL 15, wireframes ergonómicos de mostrador, paquetes acíclicos (@monchis/*), matriz RBAC y diagramas de estados (Martin, 2002; Ferraiolo et al., 2001).")
    ]

    for title, desc in vertical_points:
        p_pt = tf_c1.add_paragraph()
        p_pt.space_before = Pt(6)
        r1 = p_pt.add_run()
        r1.text = "● " + title
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = TERRACOTTA

        r2 = p_pt.add_run()
        r2.text = desc
        r2.font.name = "Calibri"
        r2.font.size = Pt(9.0)
        r2.font.color.rgb = WARM_MOCHA

    # Columna 2: Coherencia entre Perspectivas (Horizontal)
    c2 = slide_z2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(548640) + card_w + card_gap, card_y, card_w, card_h)
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = CARD_BORDER
    c2.line.width = Pt(1.0)
    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = Emu(140000); tf_c2.margin_top = Emu(120000); tf_c2.margin_right = Emu(140000)

    p = tf_c2.paragraphs[0]
    p.text = "2. Coherencia entre Perspectivas (Alineación Horizontal)"
    p.font.name = "Cambria"
    p.font.size = Pt(13.0)
    p.font.bold = True
    p.font.color.rgb = DARK_COFFEE

    horizontal_points = [
        ("Columna QUÉ (Datos):", " Evoluciona desde las características de negocio y catálogo segmentado hasta el modelo entidad-relación y tablas relacionales Prisma."),
        ("Columna CÓMO (Función):", " Transita desde los macroprocesos de negocio (PN-01..06) hasta la especificación de navegación y transiciones de pantalla con Vue Router 4."),
        ("Columna DÓNDE (Red):", " Conecta el diagrama de contexto exterior (DFD Nivel 0) con la infraestructura cloud contenerizada en Google Cloud Run y paquetes acíclicos."),
        ("Columna QUIÉN (Personas):", " Pasa de la definición de roles humanos a la caracterización de 8 actores y la matriz de permisos RBAC con principio de menor privilegio."),
        ("Columna CUÁNDO (Tiempo):", " Evoluciona desde los 10 eventos comerciales diarios hasta las máquinas de estados finitos del ciclo de vida de órdenes y lotes de café."),
        ("Columna POR QUÉ (Motivación):", " Asegura que la visión estratégica de sostenibilidad ODS 12 se convierta en 8 reglas de negocio verificadas con tests unitarios en Vitest (Pressman & Maxim, 2021).")
    ]

    for title, desc in horizontal_points:
        p_pt = tf_c2.add_paragraph()
        p_pt.space_before = Pt(4)
        r1 = p_pt.add_run()
        r1.text = "● " + title
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = DARK_SAGE

        r2 = p_pt.add_run()
        r2.text = desc
        r2.font.name = "Calibri"
        r2.font.size = Pt(9.0)
        r2.font.color.rgb = WARM_MOCHA

    # Banner inferior de Referencias APA 7
    ref_b = slide_z2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(548640), Emu(5600000), Emu(11094720), Emu(780000))
    ref_b.fill.solid()
    ref_b.fill.fore_color.rgb = RGBColor(0xFA, 0xF5, 0xF2)
    ref_b.line.color.rgb = CARD_BORDER
    ref_b.line.width = Pt(0.75)
    tf_ref = ref_b.text_frame
    tf_ref.margin_left = Emu(100000); tf_ref.margin_top = Emu(50000); tf_ref.margin_right = Emu(100000)

    p_r0 = tf_ref.paragraphs[0]
    p_r0.text = "3. Referencias Bibliográficas Verídicas (Norma APA 7.ª Edición):"
    p_r0.font.name = "Calibri"
    p_r0.font.size = Pt(8.5)
    p_r0.font.bold = True
    p_r0.font.color.rgb = TERRACOTTA

    p_r1 = tf_ref.add_paragraph()
    p_r1.text = "• Zachman, J. A. (1987). A framework for information systems architecture. IBM Systems Journal, 26(3), 276–292.  |  • ISO/IEC/IEEE 29148:2018 Systems and software engineering — Requirements engineering.  |  • Cockburn, A. (2000). Writing Effective Use Cases.  |  • Pressman, R. S., & Maxim, B. R. (2021). Ingeniería de software: un enfoque práctico (9.ª ed.).  |  • Martin, R. C. (2002). Agile Software Development.  |  • Ferraiolo et al. (2001). Proposed NIST standard for RBAC."
    p_r1.font.name = "Calibri"
    p_r1.font.size = Pt(7.5)
    p_r1.font.color.rgb = MUTED_COFFEE

    # =========================================================================
    # 3. SLIDE 22: METODOLOGÍA DEVOPS Y DIAGRAMA CI/CD EN GCP CLOUD RUN
    # =========================================================================
    slide_devops = prs.slides.add_slide(prs.slide_layouts[0])
    set_slide_bg(slide_devops)
    add_header(slide_devops, "PRODUCTO INTEGRADOR — DEVOPS Y CALIDAD DE SOFTWARE", "19. Metodología DevOps: Ciclo DevSecOps, Toolchain y Despliegue en GCP")
    add_footer(slide_devops, 22)

    # Sub-banner explicativo Shift-Left Security
    banner_d = slide_devops.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(548640), Emu(1250000), Emu(11094720), Emu(400000))
    banner_d.fill.solid()
    banner_d.fill.fore_color.rgb = NAVY_LIGHT
    banner_d.line.color.rgb = NAVY_TECH
    banner_d.line.width = Pt(1.0)
    tf_bd = banner_d.text_frame
    tf_bd.margin_left = Emu(120000); tf_bd.margin_top = Emu(60000)
    p_bd = tf_bd.paragraphs[0]
    p_bd.text = "Ciclo DevSecOps 'Shift-Left Security': integración de seguridad, pruebas automatizadas y despliegue continuo en Google Cloud Run y Cloud SQL con validación en GitHub Actions."
    p_bd.font.name = "Calibri"
    p_bd.font.size = Pt(10.0)
    p_bd.font.bold = True
    p_bd.font.color.rgb = NAVY_TECH

    # DIAGRAMA VISUAL DEL PIPELINE DEVOPS (7 ETAPAS CONECTADAS)
    box_w = Emu(1460000)
    box_gap = Emu(145000)
    diag_y = Emu(1750000)
    diag_h = Emu(2500000)

    stages = [
        {
            "num": "1", "name": "PLANIFICACIÓN", "sub": "Plan & Setup", "color": DARK_COFFEE,
            "bullets": [
                "Historias en Trello",
                "Criterios DoD y RACI",
                "Límites WIP estrictos",
                "Alineación con ODS 12"
            ]
        },
        {
            "num": "2", "name": "DESARROLLO", "sub": "Code & Local", "color": TERRACOTTA,
            "bullets": [
                "Ramas feature/*",
                "Docker Compose local",
                "Pre-commit ESLint",
                "TypeScript estricto"
            ]
        },
        {
            "num": "3", "name": "PULL REQUEST", "sub": "Code Review", "color": SOFT_CORAL,
            "bullets": [
                "Push develop / main",
                "Webhook hacia CI",
                "Revisión por pares",
                "Aprobación QA & SM"
            ]
        },
        {
            "num": "4", "name": "CI PIPELINE", "sub": "Quality Gate", "color": NAVY_TECH,
            "bullets": [
                "SAST Snyk + npm audit",
                "Tests Vitest + Supertest",
                "Build Turbo monorepo",
                "Fallo = PR Rechazado"
            ]
        },
        {
            "num": "5", "name": "CD CONTINUO", "sub": "Despliegue GCP", "color": DARK_SAGE,
            "bullets": [
                "GCP Cloud Run (API)",
                "Cloud SQL PostgreSQL",
                "Vercel CDN + SSL",
                "Nginx SSG (clean URLs)"
            ]
        },
        {
            "num": "6", "name": "OPERACIÓN", "sub": "Operate & Monitor", "color": SAGE_GREEN,
            "bullets": [
                "Pruebas Playwright E2E",
                "Logs Winston en JSON",
                "Endpoint /health activo",
                "Auditoría RBAC y TLS"
            ]
        },
        {
            "num": "7", "name": "FEEDBACK", "sub": "Mejora Continua", "color": AMBER_ALERT,
            "bullets": [
                "Métrica clave Equipo 2:",
                "\"Vulnerabilidades corregidas\"",
                "Retrospectivas semanales",
                "Backlog optimizado"
            ]
        }
    ]

    for s_idx, st in enumerate(stages):
        sx = start_x + s_idx * (box_w + box_gap)

        # Stage box
        s_card = slide_devops.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, diag_y, box_w, diag_h)
        s_card.fill.solid()
        s_card.fill.fore_color.rgb = CARD_BG
        s_card.line.color.rgb = st["color"]
        s_card.line.width = Pt(1.5 if s_idx == 3 or s_idx == 4 else 1.0)

        # Header bar of the stage
        s_bar = slide_devops.shapes.add_shape(MSO_SHAPE.RECTANGLE, sx, diag_y, box_w, Emu(580000))
        s_bar.fill.solid()
        s_bar.fill.fore_color.rgb = st["color"]
        s_bar.line.color.rgb = st["color"]
        tf_sb = s_bar.text_frame
        tf_sb.margin_left = Emu(40000); tf_sb.margin_top = Emu(40000)
        p_sb1 = tf_sb.paragraphs[0]
        p_sb1.text = f"{st['num']}. {st['name']}"
        p_sb1.font.name = "Calibri"
        p_sb1.font.size = Pt(8.5)
        p_sb1.font.bold = True
        p_sb1.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p_sb1.alignment = PP_ALIGN.CENTER

        p_sb2 = tf_sb.add_paragraph()
        p_sb2.text = st["sub"]
        p_sb2.font.name = "Calibri"
        p_sb2.font.size = Pt(7.5)
        p_sb2.font.color.rgb = RGBColor(0xFB, 0xF1, 0xEC)
        p_sb2.alignment = PP_ALIGN.CENTER

        # Stage body
        tf_sc = s_card.text_frame
        tf_sc.word_wrap = True
        tf_sc.margin_left = Emu(70000); tf_sc.margin_top = Emu(640000); tf_sc.margin_right = Emu(70000)
        for b_idx, b_text in enumerate(st["bullets"]):
            p_b = tf_sc.paragraphs[0] if b_idx == 0 else tf_sc.add_paragraph()
            p_b.space_before = Pt(3)
            p_b.text = "• " + b_text
            p_b.font.name = "Calibri"
            p_b.font.size = Pt(7.5)
            p_b.font.color.rgb = DARK_COFFEE if "Vulnerabilidades" in b_text or "Fallo" in b_text else WARM_MOCHA
            if "Vulnerabilidades" in b_text or "Fallo" in b_text:
                p_b.font.bold = True

        # Flecha conectora hacia la siguiente etapa
        if s_idx < 6:
            arrow_x = sx + box_w + Emu(15000)
            arrow_y = diag_y + Emu(1150000)
            arrow = slide_devops.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, arrow_x, arrow_y, Emu(115000), Emu(180000))
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = TERRACOTTA
            arrow.line.color.rgb = TERRACOTTA

    # SECCIÓN INFERIOR: ROLES DEL EQUIPO + EVIDENCIAS DE INFRAESTRUCTURA REAL (COMMITS)
    bot_y = Emu(4380000)
    bot_h = Emu(2000000)
    half_w = Emu(5447360)

    # Cuadro Izquierdo: Roles DevOps Equipo 2
    b_roles = slide_devops.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x, bot_y, half_w, bot_h)
    b_roles.fill.solid()
    b_roles.fill.fore_color.rgb = CARD_BG
    b_roles.line.color.rgb = CARD_BORDER
    b_roles.line.width = Pt(1.0)
    tf_r = b_roles.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = Emu(140000); tf_r.margin_top = Emu(100000); tf_r.margin_right = Emu(140000)

    p = tf_r.paragraphs[0]
    p.text = "Roles del Equipo DevOps (Equipo 2) y Responsabilidades"
    p.font.name = "Cambria"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = DARK_COFFEE

    roles_data = [
        ("Ernesto Hatuey Fierro Medina", "Scrum Master & DevOps Lead (Ops):", " Ceremonias ágiles en Trello, Docker multi-stage, pipelines CI/CD (GitHub Actions), despliegue en Google Cloud Run y Nginx TLS."),
        ("Héctor Hernández", "Backend & Data Core Developer (Dev):", " API REST Node.js/Express, esquemas Prisma PostgreSQL, auth JWT stateless con cookies httpOnly y RabbitMQ Saga."),
        ("Jazmín Díaz", "Frontend Core Developer (Dev):", " SPA Vue 3 con Vite, Pinia, POS táctil para baristas, navegación con guards y módulo de lealtad Monchis Rewards (ODS 12)."),
        ("Oswaldo Millán", "QA & SecOps Engineer (QA):", " Pruebas unitarias Vitest, E2E Playwright, escaneo SAST (Snyk / npm audit) y métrica oficial: 'Cantidad de vulnerabilidades corregidas'.")
    ]

    for name, role, desc in roles_data:
        p_r = tf_r.add_paragraph()
        p_r.space_before = Pt(3)
        r1 = p_r.add_run()
        r1.text = "● " + name + " — "
        r1.font.name = "Calibri"; r1.font.size = Pt(8.5); r1.font.bold = True; r1.font.color.rgb = DARK_COFFEE

        r2 = p_r.add_run()
        r2.text = role
        r2.font.name = "Calibri"; r2.font.size = Pt(8.5); r2.font.bold = True; r2.font.color.rgb = TERRACOTTA

        r3 = p_r.add_run()
        r3.text = desc
        r3.font.name = "Calibri"; r3.font.size = Pt(8.0); r3.font.color.rgb = WARM_MOCHA

    # Cuadro Derecho: Nuevos Commits y Evidencias de Infraestructura Real
    b_infra = slide_devops.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x + half_w + card_gap, bot_y, half_w, bot_h)
    b_infra.fill.solid()
    b_infra.fill.fore_color.rgb = CARD_BG
    b_infra.line.color.rgb = NAVY_TECH
    b_infra.line.width = Pt(1.0)
    tf_i = b_infra.text_frame
    tf_i.word_wrap = True
    tf_i.margin_left = Emu(140000); tf_i.margin_top = Emu(100000); tf_i.margin_right = Emu(140000)

    p = tf_i.paragraphs[0]
    p.text = "Implementación Real en Repositorio (Nuevos Commits y GCP Cloud Run)"
    p.font.name = "Cambria"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = NAVY_TECH

    infra_points = [
        ("Pipeline CI/CD Automatizado (.github/workflows/):", " Pipeline de validación integral (ci.yml) con Turborepo, Vitest y Prisma Generate, más pipeline de CD (cd.yml) para despliegue automático hacia Cloud Run ante commits en main/master."),
        ("Producción en Google Cloud Run y Cloud SQL:", " Contenedores Docker inmutables desplegados en GCP con conexión socket Unix hacia Cloud SQL PostgreSQL 15 y gestión de variables mediante Secret Manager."),
        ("Prerenderizado SSG y Nginx Hardening:", " Soporte de URLs limpias en Nginx (try_files $uri.html) con cabeceras Helmet (CSP, HSTS, X-Frame-Options) y proxy inverso hacia el backend."),
        ("Funcionalidades Recientes Desplegadas:", " Módulo de Contacto enriquecido con WhatsApp y geolocalización, POS con vinculación de clientes, catálogo comercial de 16 productos e historial de compras con facturación simplificada.")
    ]

    for title, desc in infra_points:
        p_i = tf_i.add_paragraph()
        p_i.space_before = Pt(3)
        r1 = p_i.add_run()
        r1.text = "✔ " + title
        r1.font.name = "Calibri"; r1.font.size = Pt(8.5); r1.font.bold = True; r1.font.color.rgb = DARK_SAGE

        r2 = p_i.add_run()
        r2.text = desc
        r2.font.name = "Calibri"; r2.font.size = Pt(8.0); r2.font.color.rgb = WARM_MOCHA

    # =========================================================================
    # REORDENAMIENTO DE DIAPOSITIVAS:
    # Las diapositivas añadidas (z1, z2, devops) deben quedar antes de Conclusiones.
    # Conclusiones era la Slide 20 (índice 19).
    # Movemos conclusiones al final (Slide 23)
    # =========================================================================
    print("Reordenando diapositivas para situar Zachman y DevOps antes de Conclusiones...")
    conclusiones_slide_id = prs.slides._sldIdLst[19]

    prs.slides._sldIdLst.remove(conclusiones_slide_id)
    prs.slides._sldIdLst.append(conclusiones_slide_id)

    # Actualizamos el número de diapositiva en el footer de Conclusiones (Slide 23)
    conclusiones_slide = prs.slides[22]
    for s in conclusiones_slide.shapes:
        if s.has_text_frame:
            for p in s.text_frame.paragraphs:
                if p.text.strip() == "20":
                    p.text = "23"
                    print("Footer de Conclusiones actualizado a 23.")
                elif "17. Conclusiones" in p.text:
                    p.text = "20. Conclusiones y Defensa del Proyecto"
                    print("Título de Conclusiones actualizado a '20. Conclusiones y Defensa del Proyecto'.")

    # Guardamos en la ruta del proyecto
    prs.save(out_path)
    print(f"Presentación actualizada guardada exitosamente en:\n  {out_path}")

    # Guardamos copia directa en Downloads
    import shutil
    shutil.copyfile(out_path, downloads_path)
    print(f"Copia directa actualizada en Descargas:\n  {downloads_path}")
    print(f"Total de diapositivas final: {len(prs.slides)}")

if __name__ == '__main__':
    generate_presentation()
