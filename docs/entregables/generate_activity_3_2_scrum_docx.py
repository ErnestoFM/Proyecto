import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import shutil
import os

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_document():
    doc = docx.Document()
    
    # Configuración de márgenes a 2.0 cm (aprox 0.79 pulgadas)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
    COLOR_PRIMARY = RGBColor(26, 54, 93)      # #1a365d Azul marino institucional
    COLOR_SECONDARY = RGBColor(43, 76, 126)   # #2b4c7e Azul corporativo
    COLOR_TEXT = RGBColor(45, 55, 72)         # #2d3748 Gris texto
    COLOR_MUTED = RGBColor(113, 128, 150)     # #718096 Gris medio
    
    # PORTADA
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst1 = p_inst.add_run("UNIVERSIDAD DE GUADALAJARA\n")
    r_inst1.bold = True
    r_inst1.font.size = Pt(16)
    r_inst1.font.color.rgb = COLOR_PRIMARY
    
    r_inst2 = p_inst.add_run("CENTRO UNIVERSITARIO DE TONALÁ (CUTonalá)\n")
    r_inst2.bold = True
    r_inst2.font.size = Pt(13)
    r_inst2.font.color.rgb = COLOR_SECONDARY
    
    r_inst3 = p_inst.add_run("División de Ingenierías e Innovación Tecnológica | Licenciatura en Ingeniería en Computación\n")
    r_inst3.font.size = Pt(10)
    r_inst3.font.color.rgb = COLOR_MUTED
    
    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_div = p_div.add_run("_______________________________________________________________________________")
    r_div.font.color.rgb = COLOR_SECONDARY
    
    doc.add_paragraph("\n")
    
    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_badge = p_badge.add_run("ASIGNATURA: PROYECTO INTEGRADOR DE DESARROLLO DE SOFTWARE")
    r_badge.bold = True
    r_badge.font.size = Pt(10)
    r_badge.font.color.rgb = COLOR_SECONDARY
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("ACTIVIDAD 3.2: GESTIÓN DE PROYECTO CON SCRUM Y ESTIMACIÓN DE ESFUERZO CON EL MODELO COCOMO INTERMEDIO\n")
    r_title.bold = True
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = COLOR_PRIMARY
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Planificación Operativa Ágil y Estimación Paramétrica Formal para el Sistema Web ERP de Gestión Empresarial \"TechSolutions\" (60 KLOC)")
    r_sub.font.size = Pt(11.5)
    r_sub.font.color.rgb = COLOR_TEXT
    
    doc.add_paragraph("\n\n")
    
    # Tabla de Datos en Portada
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Docente:", "Dr. Gabriel Navarro Salcedo"),
        ("Estudiante:", "Ernesto Hatuey Fierro Medina"),
        ("Código de Estudiante:", "215487963"),
        ("Caso de Estudio:", "TechSolutions S.A. de C.V. (Sistema Web de 60 KLOC)"),
        ("Marco Normativo:", "The Scrum Guide 2020 & COCOMO 81 (Barry Boehm)"),
        ("Fecha de Entrega:", "8 de octubre de 2026")
    ]
    for idx, (lbl, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        
        cell_lbl.width = Inches(2.2)
        cell_val.width = Inches(4.5)
        
        p_l = cell_lbl.paragraphs[0]
        r_l = p_l.add_run(lbl)
        r_l.bold = True
        r_l.font.size = Pt(9.5)
        r_l.font.color.rgb = COLOR_PRIMARY
        
        p_v = cell_val.paragraphs[0]
        r_v = p_v.add_run(val)
        r_v.font.size = Pt(9.5)
        r_v.font.color.rgb = COLOR_TEXT
        
        set_cell_background(cell_lbl, "F7FAFC")
        set_cell_background(cell_val, "F7FAFC")
        set_cell_margins(cell_lbl, top=80, bottom=80, left=120, right=120)
        set_cell_margins(cell_val, top=80, bottom=80, left=120, right=120)
        
    doc.add_paragraph("\n\n")
    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_foot = p_foot.add_run("Tonalá, Jalisco, México • Ciclo Escolar 2026-B")
    r_foot.font.size = Pt(9)
    r_foot.font.color.rgb = COLOR_MUTED
    
    doc.add_page_break()
    
    # SECCIÓN 1: INTRODUCCIÓN
    h1 = doc.add_heading("1. Introducción y Contexto del Proyecto", level=1)
    h1.runs[0].font.color.rgb = COLOR_PRIMARY
    
    p = doc.add_paragraph(
        "El presente informe documenta la planificación operativa y la estimación cuantitativa de esfuerzo y tiempo para el desarrollo del sistema web integral solicitado por la empresa ficticia \"TechSolutions\". Dicho sistema tiene como propósito central optimizar y automatizar los procesos de negocio en cuatro áreas fundamentales: gestión de productos, control de inventarios, gestión de ventas y clientes, y generación de reportes personalizados."
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    p = doc.add_paragraph(
        "De acuerdo con las especificaciones técnicas iniciales, el tamaño global del software se ha estimado en 60 KLOC (60,000 líneas lógicas de código fuente entregadas). Para abordar este desafío con rigor académico y profesional, se aplican dos marcos complementarios de la ingeniería de software:"
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    p_scrum = doc.add_paragraph(
        "1. Marco Ágil SCRUM (Schwaber & Sutherland, 2020): Empleado para la organización del equipo, descomposición del trabajo en Historias de Usuario, priorización de valor de negocio, planificación de Sprints y seguimiento visual del flujo de desarrollo mediante tableros y métricas de velocidad."
    )
    p_scrum.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    p_cocomo = doc.add_paragraph(
        "2. Modelo Paramétrico COCOMO Intermedio (Boehm, 1981): Utilizado para el cálculo formal y macroeconómico del esfuerzo total (en Personas-Mes), tiempo calendario de desarrollo y requerimientos promedio de personal, ajustados a través de quince conductores de costo específicos."
    )
    p_cocomo.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    p_box = doc.add_paragraph()
    p_box.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_box = p_box.add_run(
        "Reconciliación de Alcance Metodológico: Con el fin de garantizar total coherencia técnica entre ambos marcos, en este informe se define de forma explícita que la planificación ágil en cuatro Sprints (8 semanas de desarrollo con un equipo de 4 desarrolladores) abarca la Fase 1: Minimum Viable Product (MVP) / Core Release, la cual comprende el núcleo funcional operable (estimado en 12 a 15 KLOC). Por su parte, la estimación paramétrica con COCOMO Intermedio modela la totalidad del sistema enterprise contratado (60 KLOC), incluyendo fases subsecuentes de integración contable, facturación masiva multirregión, migración de datos legacy y hardening de infraestructura de alta disponibilidad."
    )
    r_box.italic = True
    r_box.font.color.rgb = COLOR_SECONDARY
    
    # SECCIÓN 2: FORMACIÓN DEL EQUIPO SCRUM
    h2 = doc.add_heading("2. Estructura y Conformación del Scrum Team", level=1)
    h2.runs[0].font.color.rgb = COLOR_PRIMARY
    
    p = doc.add_paragraph(
        "En estricto apego a The Scrum Guide 2020 (Schwaber & Sutherland, 2020), la unidad fundamental de trabajo es un Scrum Team cohesivo y autogestionado, conformado por profesionales enfocados en un único Objetivo del Producto. El marco Scrum 2020 establece explícitamente que no existen subequipos ni jerarquías internas; no se reconocen cargos de \"Lead\" o líderes técnicos subordinados. Todos los miembros responsables de construir el incremento comparten la designación de Developers."
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    team_table = doc.add_table(rows=7, cols=3)
    team_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Rol en Scrum", "Asignación", "Responsabilidades Clave (Scrum Guide 2020)"]
    for i, h in enumerate(headers):
        cell = team_table.rows[0].cells[i]
        set_cell_background(cell, "2B4C7E")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    team_data = [
        ("Product Owner (PO)", "Ing. Roberto Valenzuela", "Responsable de maximizar el valor del producto resultante del trabajo del Scrum Team. Administra de forma efectiva el Product Backlog: desarrolla y comunica explícitamente el Objetivo del Producto, redacta y ordena los elementos del Product Backlog, y asegura que sea transparente, visible y comprendido por la organización y los interesados de TechSolutions."),
        ("Scrum Master (SM)", "Lic. Diana Morales", "Líder que sirve al Scrum Team y a la organización. Responsable de fomentar la comprensión teórica y práctica de Scrum, facilitar la mejora continua, eliminar impedimentos organizacionales y técnicos que frenen el avance de los Developers, y asegurar que todos los eventos de Scrum se celebren de manera positiva, productiva y dentro de los límites de tiempo."),
        ("Developer 1", "Ing. Carlos Mendoza", "Especialista en arquitectura backend y modelado de datos relacionales (PostgreSQL, Prisma ORM, Node.js/TypeScript). Responsable del diseño e implementación de APIs REST, procedimientos transaccionales ACID y consistencia del kardex."),
        ("Developer 2", "Ing. Sofía Reyes", "Especialista en ingeniería de frontend y experiencia de usuario (Vue 3, Vite, Pinia, Tailwind CSS). Responsable de interfaces interactivas, componentes accesibles, rendimiento en cliente y diseño responsive del Punto de Venta."),
        ("Developer 3", "Ing. Alejandro Silva", "Desarrollador full stack especializado en lógica transaccional, servicios de facturación electrónica (CFDI 4.0), generación asíncrona de reportes y pasarelas de cobro multimétodo."),
        ("Developer 4", "Ing. Mariana Torres", "Especialista en aseguramiento de calidad automatizado (QA) e integración continua (Playwright, Jest, Docker, CI/CD). Diseña suites de pruebas unitarias, de integración y E2E para garantizar la adherencia a la Definition of Done.")
    ]
    
    for row_idx, data in enumerate(team_data, start=1):
        row = team_table.rows[row_idx]
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(8.5)
            if col_idx == 0:
                r.bold = True
            if row_idx % 2 == 0:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            
    doc.add_paragraph("\n")
    p_stack = doc.add_paragraph()
    r_st = p_stack.add_run(
        "Stack Tecnológico Homogéneo del Proyecto: Frontend: Vue 3 (Composition API), Vite, Pinia y Tailwind CSS; Backend: Node.js con TypeScript, Express/Nest y Prisma ORM; Base de Datos: PostgreSQL y Redis para caché; QA & DevOps: Playwright, Jest, Docker y GitHub Actions."
    )
    r_st.italic = True
    r_st.font.size = Pt(9)
    
    # SECCIÓN 3: PRODUCT BACKLOG
    doc.add_page_break()
    h3 = doc.add_heading("3. Product Backlog y Especificación de Historias de Usuario", level=1)
    h3.runs[0].font.color.rgb = COLOR_PRIMARY
    
    p = doc.add_paragraph(
        "El Product Backlog es una lista ordenada y emergente de todo lo que se requiere para mejorar el producto (Schwaber & Sutherland, 2020). Su compromiso asociado es el Objetivo del Producto (Product Goal):"
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    p_pgoal = doc.add_paragraph()
    p_pgoal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_pg = p_pgoal.add_run(
        "Compromiso: Objetivo del Producto (Product Goal):\n"
        "\"Desarrollar y poner en operación un sistema web transaccional y modular de nivel empresarial para TechSolutions, que unifique y automatice el catálogo de productos, el control de inventarios multialmacén mediante kardex en tiempo real, el procesamiento de ventas en terminales POS con facturación fiscal electrónica, y un motor analítico de toma de decisiones estratégicas, garantizando una disponibilidad operativa del 99.8% y una experiencia de usuario ágil.\""
    )
    r_pg.italic = True
    r_pg.font.color.rgb = COLOR_SECONDARY
    
    p = doc.add_paragraph(
        "A continuación, se especifican doce (12) Historias de Usuario representativas distribuidas equitativamente entre los cuatro módulos requeridos. Cada historia se describe en formato estándar (Como... Quiero... Para...), con criterios de aceptación en formato formal de comportamiento Gherkin (Dado... Cuando... Entonces...) y su clasificación de priorización mediante el método MoSCoW (Must Have, Should Have, Could Have)."
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    pb_table = doc.add_table(rows=13, cols=6)
    pb_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    pb_headers = ["ID", "Módulo", "Historia de Usuario y Criterio de Aceptación (Gherkin)", "MoSCoW", "Story Points", "Sprint"]
    for i, h in enumerate(pb_headers):
        cell = pb_table.rows[0].cells[i]
        set_cell_background(cell, "2B4C7E")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    pb_data = [
        ("US-01", "Gestión de Productos", "Catálogo maestro de productos y matriz de variantes. Como administrador de catálogo, quiero registrar, actualizar y dar de baja productos con soporte para variantes (talla, color, presentación), para mantener actualizada la oferta comercial.\nCriterio (Gherkin): Dado que el administrador ingresa un SKU único, cuando completa atributos obligatorios, entonces se almacena en < 1 s.", "Must", "13", "Sprint 1"),
        ("US-02", "Gestión de Productos", "Categorización taxonómica y gestión de marcas. Como gestor de inventario, quiero estructurar categorías jerárquicas multinivel y marcas asociadas, para clasificar los productos y facilitar la búsqueda.\nCriterio: Dado un árbol de categorías de 3 niveles, cuando se asocia un producto a una subcategoría, entonces hereda las propiedades del padre.", "Should", "5", "Sprint 1"),
        ("US-03", "Gestión de Clientes", "Directorio centralizado y expediente de clientes. Como ejecutivo de ventas, quiero administrar un padrón integral de clientes con datos de contacto, fiscales y límite crediticio, para personalizar la atención y controlar cartera.\nCriterio: Dado un RFC válido, cuando se registra el cliente, entonces se valida no duplicidad y se asigna expediente.", "Must", "8", "Sprint 1"),
        ("US-04", "Control de Inventarios", "Registro transaccional de movimientos en Kardex multialmacén. Como jefe de almacén, quiero registrar entradas, salidas y transferencias entre sucursales con cálculo automático de existencias, para tener trazabilidad física y contable.\nCriterio: Dado un movimiento de salida, cuando se ejecuta en BD, entonces el stock descuenta atómicamente con folio inmutable.", "Must", "13", "Sprint 2"),
        ("US-05", "Control de Inventarios", "Monitor preventivo y alertas de stock mínimo de reorden. Como encargado de compras, quiero recibir alertas automáticas cuando un artículo alcance o baje de su umbral mínimo de seguridad, para evitar quiebres de inventario.\nCriterio: Dado que las existencias llegan al nivel crítico, cuando finaliza la transacción, entonces se genera alerta visual y por correo.", "Should", "5", "Sprint 2"),
        ("US-06", "Control de Inventarios", "Módulo de tomas físicas y conciliación de ajustes de inventario. Como auditor interno, quiero realizar conteos ciegos periódicos y registrar mermas o sobrantes justificados, para conciliar el stock físico contra el inventario teórico.\nCriterio: Dado un arqueo físico, cuando el auditor somete las diferencias, entonces el sistema exige autorización de supervisión antes de ajustar kardex.", "Could", "8", "Sprint 2"),
        ("US-07", "Gestión de Ventas", "Terminal Punto de Venta (POS) y procesamiento de cobros multimétodo. Como cajero de sucursal, quiero escanear productos rápidamente y cobrar mediante efectivo, tarjeta o transferencia combinada, para agilizar el cobro y emitir tickets.\nCriterio: Dado un carrito con artículos, cuando se procesa pago mixto, entonces descuenta inventario y emite ticket en < 1.5 s.", "Must", "13", "Sprint 3"),
        ("US-08", "Gestión de Ventas", "Facturación electrónica CFDI 4.0 y timbrado fiscal digital. Como facturista, quiero timbrar facturas electrónicas a partir de tickets de venta vigentes y gestionar notas de crédito, para cumplir con los requerimientos tributarios del SAT.\nCriterio: Dado un ticket liquidado, cuando se solicita emisión, entonces el web service del PAC timbra el XML y genera el PDF.", "Must", "8", "Sprint 3"),
        ("US-09", "Gestión de Ventas", "Emisión de cotizaciones comerciales y conversión a orden de venta. Como asesor comercial, quiero generar propuestas económicas formales con vigencia definida y convertirlas en ventas con un clic, para reducir tiempos de captura.\nCriterio: Dado una cotización vigente, cuando el cliente acepta, entonces traslada los renglones al POS conservando precios pactados.", "Could", "5", "Sprint 3"),
        ("US-10", "Reportes Personalizados", "Motor analítico y dashboard consolidado de ventas. Como director comercial, quiero visualizar gráficos interactivos de ventas por periodo, sucursal, producto y margen de utilidad, para evaluar el rendimiento del negocio.\nCriterio: Dado un rango de fechas, cuando se consulta el tablero, entonces las métricas agregadas se renderizan en < 2 s.", "Must", "13", "Sprint 4"),
        ("US-11", "Reportes Personalizados", "Reporte de rotación y valuación de inventario bajo método PEPS. Como gerente de finanzas, quiero consultar la rotación de stock, productos sin movimiento y el costo valorizado de almacén, para optimizar la inversión en existencias.\nCriterio: Dado el cierre mensual, cuando se genera la valuación, entonces computa costo con PEPS y clasifica matriz ABC.", "Should", "8", "Sprint 4"),
        ("US-12", "Reportes Personalizados", "Módulo exportador asíncrono multipropósito (Excel, PDF y CSV). Como analista operativo, quiero exportar grandes volúmenes de datos transaccionales en formatos abiertos sin bloquear la interfaz, para realizar análisis avanzados externos.\nCriterio: Dado un reporte de > 10,000 filas, cuando se solicita descarga, entonces un worker procesa el archivo y notifica.", "Must", "5", "Sprint 4")
    ]
    
    for row_idx, data in enumerate(pb_data, start=1):
        row = pb_table.rows[row_idx]
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(8)
            if col_idx in [0, 3, 4, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r.bold = True
            if row_idx % 2 == 0:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            
    p_tot = doc.add_paragraph()
    r_t = p_tot.add_run(
        "\nResumen Numérico Consolidado del Product Backlog: El backlog de la Fase 1 contiene doce (12) Historias de Usuario con una suma acumulada de exactamente 104 Story Points, distribuidas a razón de 26 Story Points por cada uno de los 4 Sprints planificados."
    )
    r_t.bold = True
    r_t.font.size = Pt(9.5)
    
    # SECCIÓN 4: PLANNING POKER Y VELOCIDAD
    doc.add_page_break()
    h4 = doc.add_heading("4. Estimación del Proyecto usando SCRUM: Planning Poker y Velocidad del Equipo", level=1)
    h4.runs[0].font.color.rgb = COLOR_PRIMARY
    
    p = doc.add_paragraph(
        "Para estimar el esfuerzo relativo de cada Historia de Usuario, el equipo Scrum ejecutó sesiones formales de Planning Poker (Cohn, 2005). Se utilizó la baraja de escala estándar modificada de Fibonacci: { 1, 2, 3, 5, 8, 13, 21 } Story Points (SP)."
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    p = doc.add_paragraph(
        "Dinámica de Consenso por Discusión Técnica: En estricto apego al marco ágil, la estimación no se obtiene mediante promedios numéricos o votos mayoritarios, ya que promediar oculta la incertidumbre y las discrepancias de diseño técnico. En cada ronda de votación, los cuatro Developers presentan sus cartas de forma simultánea. Cuando surgen discrepancias (por ejemplo, en US-06 donde se emitieron votos de 5 y 13), los desarrolladores con votos extremos exponen sus justificaciones técnicas (riesgos de concurrencia en bases de datos, complejidad de la interfaz o necesidad de auditoría). Tras el debate, se efectúa una segunda ronda hasta alcanzar un consenso argumentativo pleno."
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    pp_table = doc.add_table(rows=13, cols=8)
    pp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    pp_headers = ["US", "Historia de Usuario", "Dev 1", "Dev 2", "Dev 3", "Dev 4", "Consenso", "Justificación Técnica del Consenso"]
    for i, h in enumerate(pp_headers):
        cell = pp_table.rows[0].cells[i]
        set_cell_background(cell, "2B4C7E")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    pp_data = [
        ("US-01", "Catálogo Maestro y Variantes", "13", "13", "8", "13", "13", "Alta complejidad en matriz de atributos dinámicos y esquema relacional."),
        ("US-02", "Categorización y Marcas", "5", "5", "3", "5", "5", "Estructura arbórea recursiva estándar; CRUD con validaciones de árbol."),
        ("US-03", "Directorio de Clientes", "8", "8", "5", "8", "8", "Validaciones fiscales de RFC, historial crediticio y saldo deudor."),
        ("US-04", "Kardex Transaccional", "13", "8", "13", "13", "13", "Transacciones atómicas estrictas (ACID), locks y bitácora inmutable."),
        ("US-05", "Monitor y Alertas Stock", "5", "5", "5", "3", "5", "Disparadores en BD y despacho asíncrono de correos con BullMQ."),
        ("US-06", "Tomas Físicas y Conciliación", "8", "5", "8", "8", "8", "Algoritmo de cálculo de desviaciones, arqueo ciego y doble confirmación."),
        ("US-07", "Terminal POS y Cobro", "13", "13", "13", "8", "13", "Manejo de estados de carrito reactivo, lector de barras y pagos divididos."),
        ("US-08", "Facturación CFDI 4.0", "8", "5", "8", "8", "8", "Integración con PAC certificado, sellado criptográfico y generación XML."),
        ("US-09", "Cotizaciones Comerciales", "5", "5", "5", "3", "5", "Generación de folios con caducidad y clonación estructurada hacia orden POS."),
        ("US-10", "Motor Analítico Ventas", "13", "13", "8", "13", "13", "Consultas complejas GROUP BY/OLAP, caché Redis y gráficos interactivos."),
        ("US-11", "Valuación Inventario (PEPS)", "8", "8", "8", "5", "8", "Lógica contable de capas de costo histórico y matriz de rotación ABC."),
        ("US-12", "Exportador Asíncrono", "5", "5", "5", "5", "5", "Colas en segundo plano para buffers XLSX/PDF sin bloquear navegador.")
    ]
    
    for row_idx, data in enumerate(pp_data, start=1):
        row = pp_table.rows[row_idx]
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(7.5)
            if col_idx in [0, 2, 3, 4, 5, 6]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if col_idx == 6:
                r.bold = True
            if row_idx % 2 == 0:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            
    doc.add_paragraph("\n")
    h41 = doc.add_heading("4.1. Cálculo de Capacidad, Velocidad y Previsión de Sprints", level=2)
    h41.runs[0].font.color.rgb = COLOR_SECONDARY
    
    p = doc.add_paragraph(
        "La capacidad de trabajo del equipo se fundamenta en la dedicación formal de los cuatro Developers durante un Sprint estándar de 2 semanas (10 días laborables):\n"
        "• Capacidad Nominal = 4 Developers × 10 días hábiles × 6 horas productivas/día = 240 horas por Sprint.\n"
        "• Velocidad del Equipo (V) = 26 Story Points por Sprint.\n"
        "• Factor de Esfuerzo Medio = 240 horas / 26 SP ≈ 9.23 horas-hombre por Story Point.\n"
        "• Previsión de Sprints Requeridos = 104 Story Points / 26 SP/Sprint = 4.0 Sprints exactos."
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    # SECCIÓN 5: PLANIFICACIÓN OPERATIVA DE SPRINTS
    doc.add_page_break()
    h5 = doc.add_heading("5. Planificación Operativa de Sprints y Desglose de Tareas Detalladas", level=1)
    h5.runs[0].font.color.rgb = COLOR_PRIMARY
    
    p = doc.add_paragraph(
        "En cumplimiento de The Scrum Guide 2020, la Sprint Planning aborda tres temas esenciales: ¿Por qué es valioso este Sprint? (Sprint Goal), ¿Qué se puede hacer en este Sprint? (Selección de PBIs) y ¿Cómo se realizará el trabajo elegido? (Plan de acción y descomposición en tareas). Asimismo, los Developers descomponen los elementos en tareas con una duración estimada de 2 a 8 horas (elementos de un día de trabajo o menos)."
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    p_box = doc.add_paragraph()
    p_box.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_box = p_box.add_run(
        "Distribución y Justificación de las 240 Horas por Sprint:\n"
        "• Desarrollo y codificación de historias (Backlog core): 132 horas desglosadas en tareas técnicas de 4 a 8 horas.\n"
        "• Pruebas de integración, QA automatizado y Code Review: 48 horas distribuidas entre los 4 desarrolladores (12 h por persona).\n"
        "• Eventos formales de Scrum: 40 horas en total (Sprint Planning 16 h, Daily Scrums 9 h, Sprint Review 8 h, Retrospectiva 6 h).\n"
        "• Refinamiento continuo del Product Backlog: 20 horas acumuladas (8% del tiempo del equipo, dentro del 10% que prescribe Scrum).\n"
        "• Suma total exacta: 132 h + 48 h + 40 h + 20 h = 240 horas por Sprint."
    )
    r_box.italic = True
    r_box.font.color.rgb = COLOR_SECONDARY
    
    sprints_info = [
        ("Sprint 1 (Semanas 1 y 2): Cimientos del Sistema, Catálogo de Productos y Clientes",
         "Sprint Goal: Establecer la infraestructura base del sistema y habilitar la administración integral del catálogo de productos y el padrón centralizado de clientes bajo estándares de seguridad.\nPuntos: 26 SP (US-01: 13 SP, US-02: 5 SP, US-03: 8 SP). Incremento: Primer incremento utilizable (catálogo y clientes). Nota: No es aún un MVP de negocio, pues no incluye ventas ni inventarios.",
         [
             ("T1.1", "US-01", "Modelado de esquema Prisma para productos, atributos y migración PostgreSQL.", "Developer 1", "6 h", "Done"),
             ("T1.2", "US-01", "Implementación de endpoints REST para CRUD de productos con carga de fotos.", "Developer 1", "8 h", "Done"),
             ("T1.3", "US-01", "Desarrollo de interfaz en Vue 3 con validaciones reactivas para productos.", "Developer 2", "8 h", "Done"),
             ("T1.4", "US-01", "Pruebas unitarias Jest y pruebas E2E en Playwright para catálogo.", "Developer 4", "6 h", "Done"),
             ("T1.5", "US-02", "Diseño de estructura arbórea para categorías y endpoints jerárquicos.", "Developer 3", "6 h", "Done"),
             ("T1.6", "US-02", "Componente frontend con visualización en árbol y drag-and-drop para categorías.", "Developer 2", "6 h", "Done"),
             ("T1.7", "US-03", "Modelado de tabla de clientes, validación de RFC y límite de crédito.", "Developer 1", "6 h", "Done"),
             ("T1.8", "US-03", "Vista de padrón de clientes con paginación, filtros dinámicos y modal.", "Developer 2", "8 h", "Done"),
             ("T1.9", "US-03", "Pruebas de validación de unicidad de RFC y límites de crédito en backend.", "Developer 4", "6 h", "Done"),
             ("T1.10", "Infra", "Configuración de contenedor Docker, pipeline CI/CD en GitHub Actions y linting.", "Developer 3", "8 h", "Done"),
         ]),
        ("Sprint 2 (Semanas 3 y 4): Control de Inventarios Multi-Almacén y Kardex",
         "Sprint Goal: Garantizar la trazabilidad y consistencia transaccional del inventario mediante el kardex multialmacén, control de mermas y sistema preventivo de stock mínimo.\nPuntos: 26 SP (US-04: 13 SP, US-05: 5 SP, US-06: 8 SP). Incremento: Segundo incremento acumulado con control físico y contable de inventario.",
         [
             ("T2.1", "US-04", "Diseño de tabla de kardex con aislamiento transaccional PostgreSQL y locks.", "Developer 1", "8 h", "Done"),
             ("T2.2", "US-04", "Servicio backend de transferencias entre almacenes con rollback seguro.", "Developer 3", "8 h", "Done"),
             ("T2.3", "US-04", "Interfaz de consulta de kardex con filtros por sucursal, fecha y SKU.", "Developer 2", "8 h", "Done"),
             ("T2.4", "US-04", "Pruebas de estrés y concurrencia para evitar race conditions en stock.", "Developer 4", "6 h", "Done"),
             ("T2.5", "US-05", "Creación de disparadores de stock mínimo y cola asíncrona con BullMQ.", "Developer 1", "6 h", "Done"),
             ("T2.6", "US-05", "Centro de notificaciones visuales en frontend con badges y alertas.", "Developer 2", "6 h", "Done"),
             ("T2.7", "US-06", "Servicio para generación de hojas de conteo ciego y captura de existencias.", "Developer 3", "8 h", "Done"),
             ("T2.8", "US-06", "Pantalla de conciliación de diferencias de inventario con autorización.", "Developer 2", "8 h", "Done"),
             ("T2.9", "US-06", "Pruebas automatizadas del flujo de autorización de ajustes de mermas.", "Developer 4", "6 h", "Done"),
         ]),
        ("Sprint 3 (Semanas 5 y 6): Punto de Venta (POS), Facturación Fiscal y Cotizaciones",
         "Sprint Goal: Integrar el flujo comercial completo procesando transacciones en terminales POS con descuento en kardex, cobros multimétodo y timbrado fiscal digital.\nPuntos: 26 SP (US-07: 13 SP, US-08: 8 SP, US-09: 5 SP). Incremento: Minimum Viable Product (MVP Operable de Negocio). Permite operar comercialmente.",
         [
             ("T3.1", "US-07", "Desarrollo de interfaz POS rápida con soporte para lector de código de barras.", "Developer 2", "8 h", "Done"),
             ("T3.2", "US-07", "Servicio transaccional de liquidación de ventas con cobro multimétodo.", "Developer 1", "8 h", "Done"),
             ("T3.3", "US-07", "Módulo de impresión térmica de tickets de venta con código QR fiscal.", "Developer 3", "6 h", "Done"),
             ("T3.4", "US-07", "Pruebas de latencia en POS (validación de respuesta < 1.5 s bajo concurrencia).", "Developer 4", "6 h", "Done"),
             ("T3.5", "US-08", "Integración con Web Service de PAC para generación y timbrado de CFDI 4.0.", "Developer 3", "8 h", "Done"),
             ("T3.6", "US-08", "Servicio de generación de representación impresa en PDF y entrega de XML.", "Developer 1", "6 h", "Done"),
             ("T3.7", "US-08", "Pruebas de validación de sellado digital y cancelación de comprobantes.", "Developer 4", "6 h", "Done"),
             ("T3.8", "US-09", "Modelo y endpoints para cotizaciones con cálculo de vigencia.", "Developer 1", "6 h", "Done"),
             ("T3.9", "US-09", "Flujo frontend de conversión de cotización directa a ticket del POS.", "Developer 2", "6 h", "Done"),
         ]),
        ("Sprint 4 (Semanas 7 y 8): Reportes Personalizados, Business Intelligence y Hardening",
         "Sprint Goal: Consolidar la plataforma de analítica y reportes de gestión comercial y de inventarios, asegurando exportaciones asíncronas y estabilidad para producción.\nPuntos: 26 SP (US-10: 13 SP, US-11: 8 SP, US-12: 5 SP). Incremento: Entrega de la Fase 1 / Core Release integral del sistema.",
         [
             ("T4.1", "US-10", "Consultas analíticas optimizadas en PostgreSQL (vistas materializadas).", "Developer 1", "8 h", "Done"),
             ("T4.2", "US-10", "Dashboard interactivo con Chart.js para ventas por periodo y sucursal.", "Developer 2", "8 h", "Done"),
             ("T4.3", "US-10", "Estrategia de caché en Redis para reportes ejecutivos de alta demanda.", "Developer 3", "6 h", "Done"),
             ("T4.4", "US-11", "Implementación de algoritmo de valuación PEPS y matriz de rotación ABC.", "Developer 1", "8 h", "Done"),
             ("T4.5", "US-11", "Interfaz de auditoría de costos de inventario con comparativa histórica.", "Developer 2", "6 h", "Done"),
             ("T4.6", "US-12", "Worker asíncrono para generación de archivos Excel (xlsx) y PDF masivos.", "Developer 3", "8 h", "Done"),
             ("T4.7", "US-12", "Mecanismo seguro de descarga temporal mediante URLs firmadas.", "Developer 1", "6 h", "Done"),
             ("T4.8", "Calidad", "Suite de pruebas E2E de regresión completa del sistema con Playwright.", "Developer 4", "8 h", "Done"),
             ("T4.9", "DevOps", "Hardening de seguridad (OWASP Top 10, HSTS, rate limiting) y despliegue Staging.", "Developer 3", "6 h", "Done"),
         ])
    ]
    
    for s_title, s_desc, s_tasks in sprints_info:
        hs = doc.add_heading(s_title, level=2)
        hs.runs[0].font.color.rgb = COLOR_SECONDARY
        
        p = doc.add_paragraph(s_desc)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        tbl = doc.add_table(rows=len(s_tasks)+1, cols=6)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        headers_t = ["ID Tarea", "Historia", "Descripción Técnica", "Responsable", "Horas", "Estado"]
        for i, h in enumerate(headers_t):
            cell = tbl.rows[0].cells[i]
            set_cell_background(cell, "2B4C7E")
            p = cell.paragraphs[0]
            r = p.add_run(h)
            r.bold = True
            r.font.size = Pt(8)
            r.font.color.rgb = RGBColor(255, 255, 255)
            
        for row_idx, task in enumerate(s_tasks, start=1):
            row = tbl.rows[row_idx]
            for col_idx, text in enumerate(task):
                cell = row.cells[col_idx]
                p = cell.paragraphs[0]
                r = p.add_run(text)
                r.font.size = Pt(8)
                if col_idx in [0, 1, 4, 5]:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                if col_idx in [0, 4, 5]:
                    r.bold = True
                if row_idx % 2 == 0:
                    set_cell_background(cell, "F8FAFC")
                set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
                
        doc.add_paragraph("\n")
        
    # Tablero Scrum y DoD
    h51 = doc.add_heading("5.1. Tablero SCRUM Operativo y Definition of Done (DoD)", level=2)
    h51.runs[0].font.color.rgb = COLOR_SECONDARY
    
    p = doc.add_paragraph(
        "Para garantizar el flujo continuo de valor y la inspección empírica, el equipo gestiona el trabajo mediante un Tablero SCRUM (Kanban Board) compuesto por cuatro columnas con límites estrictos de trabajo en progreso:\n"
        "1. To Do (Sprint Backlog): Tareas priorizadas del Sprint que aún no han sido iniciadas.\n"
        "2. In Progress (WIP = 4): Límite estricto de 4 tareas simultáneas (una activa por cada Developer) para evitar dispersión y sobrecarga.\n"
        "3. Code Review & QA (WIP = 4): Revisión cruzada obligatoria de Pull Request por al menos dos pares y ejecución automatizada de pruebas CI/CD.\n"
        "4. Done: Elementos que satisfacen el 100% de la Definition of Done y están listos para producción."
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    p_dod = doc.add_paragraph()
    p_dod.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_d = p_dod.add_run(
        "Compromiso: Definition of Done (DoD) Formal:\n"
        "Un elemento se considera terminado únicamente si: 1) Código integrado en rama principal vía PR aprobado por 2 desarrolladores; 2) Cumple con estándares TypeScript sin advertencias de linter; 3) Pruebas unitarias en Jest con cobertura ≥ 80% en lógica de negocio; 4) Pasa suites E2E en Playwright; 5) Documentación OpenAPI/Swagger actualizada; 6) Desplegado y verificado en entorno de Staging."
    )
    r_d.italic = True
    r_d.font.color.rgb = COLOR_SECONDARY
    
    # SECCIÓN 6: COCOMO INTERMEDIO
    doc.add_page_break()
    h6 = doc.add_heading("6. Estimación Paramétrica del Proyecto mediante el Modelo COCOMO Intermedio", level=1)
    h6.runs[0].font.color.rgb = COLOR_PRIMARY
    
    p = doc.add_paragraph(
        "El modelo COCOMO Intermedio (Constructive Cost Model, Boehm, 1981) es un estándar matemático y paramétrico de la ingeniería de software diseñado para calcular el esfuerzo, el tiempo y el personal necesario para completar un sistema en función de su tamaño estimado en miles de líneas de código fuente (KLOC) y quince factores de ajuste (Cost Drivers)."
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    h61 = doc.add_heading("6.1. Justificación Rigurosa del Modo de Desarrollo: Semidesarrollado (Semi-Detached)", level=2)
    h61.runs[0].font.color.rgb = COLOR_SECONDARY
    
    p = doc.add_paragraph(
        "Siguiendo las pautas de Boehm (1981), el proyecto de TechSolutions se clasifica formalmente en el modo Semidesarrollado (Semi-Detached) debido a la concurrencia de los siguientes factores técnicos y organizacionales:\n"
        "• Requerimientos Mixtos en Grado de Rigidez: El sistema contiene módulos con requerimientos sumamente estrictos e inflexibles (el módulo de Kardex exige consistencia transaccional ACID pura y la facturación electrónica CFDI 4.0 está atada a normativas fiscales inmutables del SAT), combinados con módulos altamente flexibles y adaptativos (la interfaz visual de usuario, el Punto de Venta web y los tableros analíticos gerenciales configurables).\n"
        "• Experiencia Heterogénea del Personal: El equipo técnico posee un nivel sobresaliente de dominio en tecnologías web modernas (Vue 3, TypeScript, PostgreSQL), pero cuenta con una experiencia moderada o en desarrollo respecto a las reglas de negocio específicas y dinámicas operativas internas de la empresa TechSolutions.\n"
        "• Dimensión y Restricciones del Software: Con un tamaño de 60 KLOC, el sistema supera la cota típica del modo orgánico (≤ 50 KLOC), pero no opera bajo las limitaciones de hardware en tiempo real extremas propias del modo empotrado (Embedded)."
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    h62 = doc.add_heading("6.2. Coeficientes y Ecuaciones del Modelo", level=2)
    h62.runs[0].font.color.rgb = COLOR_SECONDARY
    
    p = doc.add_paragraph(
        "Para el modo Semidesarrollado, las constantes matemáticas de calibración empírica definidas por Boehm (1981) son:\n"
        "a = 3.0  |  b = 1.12  |  c = 2.5  |  d = 0.35  (Tamaño S = 60 KLOC)\n\n"
        "Ecuaciones fundamentales:\n"
        "• Esfuerzo Nominal: E_nominal = a × (KLOC)^b\n"
        "• Esfuerzo Ajustado: E = E_nominal × EAF [Personas-Mes (PM)]\n"
        "• Tiempo de Desarrollo: Tdev = c × (E)^d [Meses calendarios]\n"
        "• Personal Promedio: N = E / Tdev [Personas requeridas]\n"
        "• Productividad Media: Prod = S / E [LOC / PM]"
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    h63 = doc.add_heading("6.3. Cálculo del Esfuerzo Nominal", level=2)
    h63.runs[0].font.color.rgb = COLOR_SECONDARY
    
    p = doc.add_paragraph(
        "Sustituyendo S = 60 KLOC:\n"
        "E_nominal = 3.0 × (60)^1.12\n"
        "Cálculo analítico: ln(60) ≈ 4.09434456 ⇒ 1.12 × 4.09434456 ≈ 4.5856659 ⇒ 60^1.12 ≈ 98.0707\n"
        "E_nominal = 3.0 × 98.0707 = 294.21 Personas-Mes (PM)."
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    h64 = doc.add_heading("6.4. Evaluación de los Quince (15) Cost Drivers y Cálculo del EAF", level=2)
    h64.runs[0].font.color.rgb = COLOR_SECONDARY
    
    cocomo_table = doc.add_table(rows=16, cols=6)
    cocomo_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_headers = ["Categoría", "Factor", "Descripción del Conductor", "Calificación", "Multiplicador", "Justificación Técnica en TechSolutions"]
    for i, h in enumerate(c_headers):
        cell = cocomo_table.rows[0].cells[i]
        set_cell_background(cell, "2B4C7E")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    drivers_data = [
        ("Producto", "RELY", "Fiabilidad requerida del software", "Alto", "1.15", "Fallas en inventario o ventas generan pérdidas financieras y fiscales directas."),
        ("Producto", "DATA", "Tamaño de base de datos (D/P)", "Alto", "1.08", "Volumen de transacciones comerciales supera los 100 bytes/LOC."),
        ("Producto", "CPLX", "Complejidad del producto", "Alto", "1.15", "Algoritmos de kardex, transacciones concurrentes y timbrado digital."),
        ("Plataforma", "TIME", "Restricción tiempo de ejecución", "Nominal", "1.00", "Uso de CPU previsto menor al 50% de la capacidad disponible en la nube."),
        ("Plataforma", "STOR", "Restricción de memoria principal", "Nominal", "1.00", "No existen restricciones severas de memoria en servidores cloud."),
        ("Plataforma", "VIRT", "Volatilidad de la máquina virtual", "Bajo", "0.87", "Entorno estable en contenedores Docker sobre Linux LTS."),
        ("Plataforma", "TURN", "Tiempo respuesta del computador", "Bajo", "0.87", "Tiempos de respuesta inmediatos con Vite local y pipelines CI/CD rápidos."),
        ("Personal", "ACAP", "Capacidad del analista", "Alto", "0.86", "Analistas con amplia capacidad para modelar requerimientos complejos."),
        ("Personal", "AEXP", "Experiencia en la aplicación", "Nominal", "1.00", "Experiencia media del equipo en desarrollo de sistemas ERP comerciales."),
        ("Personal", "PCAP", "Capacidad de los programadores", "Alto", "0.86", "Programadores altamente calificados en TypeScript, Vue 3 y SQL."),
        ("Personal", "VEXP", "Experiencia plataforma virtual", "Nominal", "1.00", "Familiaridad estándar de 1 a 3 años en ecosistemas cloud y Linux."),
        ("Personal", "LEXP", "Experiencia en el lenguaje", "Alto", "0.95", "Más de 2 años de experiencia continua en TypeScript, Node.js y SQL."),
        ("Proyecto", "MODP", "Prácticas modernas de software", "Alto", "0.91", "Adopción rigurosa de Clean Architecture, TDD y revisiones de código."),
        ("Proyecto", "TOOL", "Uso de herramientas de software", "Alto", "0.91", "Uso integral de IDEs avanzados, linters, profiling y Docker containers."),
        ("Proyecto", "SCED", "Restricción en el cronograma", "Nominal", "1.00", "Cronograma de desarrollo planificado sin compresión forzada de plazos.")
    ]
    
    for row_idx, data in enumerate(drivers_data, start=1):
        row = cocomo_table.rows[row_idx]
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(8)
            if col_idx in [0, 1, 3, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if col_idx in [1, 4]:
                r.bold = True
            if row_idx % 2 == 0:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            
    doc.add_paragraph("\n")
    p_eaf = doc.add_paragraph(
        "Cálculo del Factor de Ajuste del Esfuerzo (EAF):\n"
        "EAF = ∏ Fi = (1.15 × 1.08 × 1.15) × (1.00 × 1.00 × 0.87 × 0.87) × (0.86 × 1.00 × 0.86 × 1.00 × 0.95) × (0.91 × 0.91 × 1.00)\n"
        "• Producto: 1.4283  |  Plataforma: 0.7569  |  Personal: 0.70262  |  Proyecto: 0.8281\n"
        "• EAF = 1.4283 × 0.7569 × 0.70262 × 0.8281 ≈ 0.6290 (Reducción neta del 37.1% sobre el esfuerzo nominal).\n\n"
        "Resultados Finales del Modelo COCOMO Intermedio:\n"
        "1. Esfuerzo Ajustado (E) = 294.21 × 0.6290 = 185.06 Personas-Mes (PM).\n"
        "2. Tiempo de Desarrollo (Tdev) = 2.5 × (185.06)^0.35 = 2.5 × 6.2163 = 15.54 Meses calendarios.\n"
        "3. Personal Promedio Requerido (N) = 185.06 PM / 15.54 meses = 11.91 ≈ 12 Ingenieros a tiempo completo.\n"
        "4. Productividad Media = 60,000 LOC / 185.06 PM = 324.22 LOC / Persona-Mes (~2.03 LOC/hora)."
    )
    p_eaf.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    # SECCIÓN 7: REFLEXIÓN COMPARATIVA
    doc.add_page_break()
    h7 = doc.add_heading("7. Reflexión Comparativa: SCRUM vs. Modelo COCOMO Intermedio", level=1)
    h7.runs[0].font.color.rgb = COLOR_PRIMARY
    
    p = doc.add_paragraph(
        "El análisis comparativo entre la planeación ágil mediante SCRUM y la estimación algorítmica con COCOMO Intermedio permite evidenciar dos filosofías complementarias en la gestión moderna de la ingeniería de software (Pressman & Maxim, 2020)."
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    comp_table = doc.add_table(rows=7, cols=3)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cp_headers = ["Criterio de Comparación", "Marco Ágil SCRUM (Scrum Guide 2020)", "Modelo COCOMO Intermedio (Boehm, 1981)"]
    for i, h in enumerate(cp_headers):
        cell = comp_table.rows[0].cells[i]
        set_cell_background(cell, "2B4C7E")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    comp_data = [
        ("Paradigma Central", "Empírico y adaptativo. Se basa en inspección, adaptación y transparencia en ciclos cortos.", "Predictivo y paramétrico. Se fundamenta en regresiones estadísticas y datos históricos de proyectos."),
        ("Unidad de Medida", "Story Points (SP) y horas ideales de esfuerzo relativo para tareas técnicas.", "Líneas de código entregadas (KLOC), Personas-Mes (PM) y meses calendarios."),
        ("Horizonte Temporal", "Cadencia de corto plazo (Sprints fijos de 2 semanas) con metas tácticas claras.", "Proyección de ciclo de vida completo a mediano/largo plazo (15.54 meses)."),
        ("Gestión de Requerimientos", "Abierto al cambio continuo. El Product Backlog es emergente y se reordena según valor.", "Asume alcance y tamaño definidos preliminarmente para proyectar costos y contratos."),
        ("Mitigación del Riesgo", "Temprana, mediante entregas frecuentes de software funcional inspeccionable cada 2 semanas.", "Financiera y de dotación, mediante dimensionamiento formal de personal y presupuesto global."),
        ("Participación del Cliente", "Constante y colaborativa en cada Sprint Planning, Review y refinamiento del Backlog.", "Enfocada en la fase inicial de licitación, negociación contractual y cierre de hitos mayores.")
    ]
    
    for row_idx, data in enumerate(comp_data, start=1):
        row = comp_table.rows[row_idx]
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(8.5)
            if col_idx == 0:
                r.bold = True
            if row_idx % 2 == 0:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            
    doc.add_paragraph("\n")
    h71 = doc.add_heading("7.1. Reconciliación de la Brecha de Esfuerzo (8 Semanas vs. 15.54 Meses)", level=2)
    h71.runs[0].font.color.rgb = COLOR_SECONDARY
    
    p = doc.add_paragraph(
        "Una observación analítica fundamental radica en la aparente discrepancia numérica entre la planificación Scrum (4 Sprints de 2 semanas con 4 desarrolladores = 960 horas ≈ 6 Personas-Mes) y el resultado de COCOMO Intermedio (185.06 Personas-Mes, 15.54 meses con 12 personas). Lejos de representar un error de cálculo, esta diferencia ilustra con precisión dos niveles de abstracción:\n\n"
        "1. Diferenciación de Alcance (Fase 1 MVP vs. Ciclo Enterprise Total): La planificación Scrum presentada abarca la Fase 1: Minimum Viable Product (MVP) / Core Release. En ella, un equipo compacto de 4 ingenieros construye el núcleo crítico operativo (104 Story Points, estimado en 12 a 15 KLOC), logrando que TechSolutions empiece a operar su catálogo, kardex, punto de venta y reportes esenciales al concluir el Sprint 3 y 4. En contraste, COCOMO modela la totalidad del sistema enterprise (60 KLOC), el cual requerirá entre 24 y 28 Sprints adicionales para abarcar contabilidad electrónica automatizada, facturación multirregión, integraciones bancarias, migración de datos históricos, arquitectura de alta disponibilidad y auditorías de seguridad forense.\n\n"
        "2. El Cono de Incertidumbre (Boehm, 1981): Al inicio de un proyecto, la incertidumbre sobre el alcance real puede variar hasta en un factor de 4x. La estimación COCOMO otorga una frontera presupuestal macro, mientras que Scrum mitiga activamente el Cono de Incertidumbre al reducir el desperdicio: las funcionalidades secundarias que el cliente decida no implementar tras inspeccionar el MVP en producción evitarán el gasto de líneas de código innecesarias."
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    h72 = doc.add_heading("7.2. Recomendación de Gobernanza: Enfoque Híbrido Ágil-Paramétrico", level=2)
    h72.runs[0].font.color.rgb = COLOR_SECONDARY
    
    p = doc.add_paragraph(
        "Para proyectos tecnológicos de la escala de TechSolutions, la mejor práctica de la ingeniería de software contemporánea consiste en articular un modelo híbrido:\n"
        "• Gobernanza Financiera con COCOMO: La dirección de la empresa utiliza COCOMO Intermedio como herramienta formal para calcular la viabilidad económica, comprometer presupuestos plurianuales ante comités de inversión y estimar los recursos de infraestructura necesarios (185 PM).\n"
        "• Ejecución Operativa con SCRUM: El equipo de ingeniería adopta Scrum para construir el producto de forma iterativa e incremental, protegiendo al negocio mediante entregas tempranas de valor tangible (MVP en Sprint 3), calidad certificada mediante la Definition of Done y capacidad de pivotar ante cambios del mercado."
    )
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    # SECCIÓN 8: REFERENCIAS
    doc.add_page_break()
    h8 = doc.add_heading("8. Referencias Bibliográficas (Formato APA 7)", level=1)
    h8.runs[0].font.color.rgb = COLOR_PRIMARY
    
    refs = [
        "Boehm, B. W. (1981). Software Engineering Economics. Prentice-Hall.",
        "Cohn, M. (2005). Agile Estimating and Planning. Prentice Hall PTR.",
        "Pressman, R. S., & Maxim, B. R. (2020). Software Engineering: A Practitioner's Approach (9.ª ed.). McGraw-Hill Education.",
        "Schwaber, K., & Sutherland, J. (2020). The Scrum Guide: The Definitive Guide to Scrum: The Rules of the Game. Scrum.org. https://scrumguides.org/",
        "Sommerville, I. (2016). Software Engineering (10.ª ed.). Pearson."
    ]
    for r in refs:
        p_r = doc.add_paragraph(r)
        p_r.paragraph_format.left_indent = Inches(0.4)
        p_r.paragraph_format.first_line_indent = Inches(-0.4)
        p_r.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_r.runs[0].font.size = Pt(9.5)
        
    docx_path_repo = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_3_2_SCRUM_COCOMO_TechSolutions.docx"
    docx_path_downloads = r"C:\Users\erfierro\Downloads\Actividad_3_2_SCRUM_COCOMO_TechSolutions.docx"
    
    doc.save(docx_path_repo)
    shutil.copyfile(docx_path_repo, docx_path_downloads)
    print(f"DOCX generado exitosamente en repositorio: {docx_path_repo}")
    print(f"DOCX copiado exitosamente a Descargas: {docx_path_downloads}")

if __name__ == "__main__":
    create_document()
