# -*- coding: utf-8 -*-
"""
Generador del Entregable Académico Oficial:
Actividad 3.6: Investigación y Aplicación de Marcos de Trabajo y Estándares en la Gestión de Servicios Informáticos
Módulo 2: Buenas Prácticas de Calidad en el Desarrollo de Software / Gestión de Servicios TI
Docente: Dr. Gabriel Navarro Salcedo
Estudiante: Ernesto Hatuey Fierro Meléndez (Código: 215487963)
Proyecto Integrador: Monchis Café — Plataforma Web Integral y Sistema de Gestión de Servicios para Cafetería Orgánica y Comercial
Universidad de Guadalajara - Centro Universitario de Tonalá (CUTonalá)
"""

import os
import subprocess
import shutil
import re
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def build_deliverables():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    entregables_dir = os.path.join(repo_root, "docs", "entregables")
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    docx_path = os.path.join(entregables_dir, "Actividad_3_6_Investigacion_Marcos_Servicios_TI_MonchisCafe.docx")
    html_path = os.path.join(entregables_dir, "Actividad_3_6_Investigacion_Marcos_Servicios_TI_MonchisCafe.html")
    pdf_path = os.path.join(entregables_dir, "Actividad_3_6_Investigacion_Marcos_Servicios_TI_MonchisCafe.pdf")
    md_path = os.path.join(entregables_dir, "Actividad_3_6_Investigacion_Marcos_Servicios_TI_MonchisCafe.md")

    download_docx = os.path.join(downloads_dir, "Actividad_3_6_Investigacion_Marcos_Servicios_TI_MonchisCafe.docx")
    download_pdf = os.path.join(downloads_dir, "Actividad_3_6_Investigacion_Marcos_Servicios_TI_MonchisCafe.pdf")

    # =========================================================================
    # 1. CONSTRUCCIÓN DEL DOCUMENTO WORD (.DOCX)
    # =========================================================================
    doc = Document()

    # Estilos base
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(10.5)
    style_normal.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(4)

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(28)
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(24)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(11.5)
        run.italic = True
        run.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
        return p

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(0x2B, 0x4C, 0x7E)
        return p

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.italic = True
        run.font.name = 'Arial'
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
        return p

    def add_page_number_to_footer(section):
        p_footer = section.footer.paragraphs[0]
        p_footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_footer.text = ""
        run = p_footer.add_run()
        run.font.name = 'Arial'
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
        
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')
        instrText = OxmlElement('w:instrText')
        instrText.set(qn('xml:space'), 'preserve')
        instrText.text = "PAGE"
        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'separate')
        fldChar3 = OxmlElement('w:fldChar')
        fldChar3.set(qn('w:fldCharType'), 'end')
        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)
        run._r.append(fldChar3)

    def set_cell_shading(cell, color_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    # Configuración de página
    sec1 = doc.sections[0]
    sec1.orientation = WD_ORIENT.PORTRAIT
    sec1.page_width = Inches(8.5)
    sec1.page_height = Inches(11.0)
    sec1.top_margin = Inches(0.9)
    sec1.bottom_margin = Inches(0.9)
    sec1.left_margin = Inches(0.9)
    sec1.right_margin = Inches(0.9)
    add_page_number_to_footer(sec1)

    # PORTADA
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(3)
    run_inst = p_inst.add_run("UNIVERSIDAD DE GUADALAJARA\nCENTRO UNIVERSITARIO DE TONALÁ (CUTONALÁ)")
    run_inst.bold = True
    run_inst.font.name = 'Arial'
    run_inst.font.size = Pt(12)
    run_inst.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    p_subinst = doc.add_paragraph()
    p_subinst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subinst.paragraph_format.space_after = Pt(20)
    run_subinst = p_subinst.add_run("División de Ingenierías e Innovación Tecnológica\nLicenciatura en Ingeniería en Computación\nMódulo 2: Buenas Prácticas de Calidad en el Desarrollo de Software")
    run_subinst.font.name = 'Arial'
    run_subinst.font.size = Pt(10)
    run_subinst.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    add_title("ACTIVIDAD 3.6: INVESTIGACIÓN Y APLICACIÓN DE MARCOS DE TRABAJO Y ESTÁNDARES EN LA GESTIÓN DE SERVICIOS INFORMÁTICOS")
    add_subtitle("Diseño de la Estrategia de Servicios TI basada en el Ciclo de Vida ITIL e ISO/IEC 20000-1 para la Plataforma Monchis Café")

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(28)
    p_meta.paragraph_format.space_after = Pt(10)
    p_meta.paragraph_format.line_spacing = 1.3

    runs_meta = [
        ("Docente: ", True), ("Dr. Gabriel Navarro Salcedo\n", False),
        ("Estudiante: ", True), ("Ernesto Hatuey Fierro Meléndez\n", False),
        ("Código Estudiantil: ", True), ("215487963\n", False),
        ("Proyecto Integrador: ", True), ("Monchis Café — Plataforma Web Segura para Cafetería Orgánica y Comercial\n", False),
        ("Especialidad Técnica: ", True), ("Arquitectura de Software y Gestión de Servicios TI\n", False),
        ("Fecha de Entrega: ", True), ("26 de octubre de 2026\n", False),
        ("Ciclo Académico: ", True), ("2026-B", False)
    ]
    for text, bold in runs_meta:
        r = p_meta.add_run(text)
        r.font.name = 'Arial'
        r.font.size = Pt(10)
        r.bold = bold
        r.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)

    doc.add_page_break()

    # ÍNDICE GENERAL
    add_heading_1("Índice General")
    toc_items = [
        ("1. Introducción y Justificación de la Gestión de Servicios TI", "3"),
        ("2. Investigación Preliminar de Marcos de Trabajo y Estándares", "3"),
        ("    2.1. ITIL (Information Technology Infrastructure Library)", "3"),
        ("    2.2. ISO/IEC 20000 (Sistema de Gestión de Servicios TI)", "3"),
        ("    2.3. Otros Marcos Relevantes: COBIT 2019, CMMI-SVC y TOGAF", "3"),
        ("3. Descripción Detallada de los Marcos Seleccionados", "4"),
        ("    3.1. ITIL v4: Objetivos, Principios Guía y Áreas Clave", "4"),
        ("    3.2. ISO/IEC 20000-1:2018: Principios y Estructura Normativa", "4"),
        ("4. Análisis Comparativo entre ITIL e ISO/IEC 20000", "4"),
        ("    4.1. Matriz Comparativa Multidimensional", "4"),
        ("    4.2. Sinergia Metodológica en el Contexto del Proyecto", "4"),
        ("5. Adaptación al Proyecto Final: Monchis Café", "5"),
        ("    5.1. Justificación de Elección según Requisitos de Monchis Café", "5"),
        ("    5.2. Estrategia de Servicios TI en las Fases del Ciclo de Vida ITIL", "5"),
        ("        5.2.1. Estrategia del Servicio (Service Strategy)", "5"),
        ("        5.2.2. Diseño del Servicio (Service Design)", "5"),
        ("        5.2.3. Transición del Servicio (Service Transition)", "5"),
        ("        5.2.4. Operación del Servicio (Service Operation)", "5"),
        ("        5.2.5. Mejora Continua del Servicio (Continual Service Improvement)", "5"),
        ("    5.3. Matriz Integradora: Valor, Procesos, Roles y Herramientas", "6"),
        ("    5.4. Ejemplos Específicos de Aplicación en Fases Clave", "6"),
        ("        5.4.1. Gestión de Riesgos: Consistencia Transaccional con RabbitMQ Saga", "6"),
        ("        5.4.2. Entrega de Servicios: Despliegue de Actualizaciones al POS en Barra", "6"),
        ("        5.4.3. Mejora Continua: Telemetría de Latencia y Desabasto de Café Orgánico", "6"),
        ("    5.5. Esquema Conceptual de la Estrategia de Servicios TI", "6"),
        ("6. Conclusiones y Desafíos de Adaptación", "7"),
        ("7. Referencias Bibliográficas (Normas APA 7.ª edición)", "8")
    ]
    for item, page in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.line_spacing = 1.1
        p_toc.paragraph_format.space_after = Pt(1.5)
        r_item = p_toc.add_run(item)
        r_item.font.name = 'Arial'
        r_item.font.size = Pt(9.5)
        r_dots = p_toc.add_run(" " + "." * (75 - len(item) - len(page)) + " ")
        r_dots.font.name = 'Arial'
        r_dots.font.size = Pt(8.5)
        r_dots.font.color.rgb = RGBColor(0xA0, 0xAE, 0xC0)
        r_page = p_toc.add_run(page)
        r_page.font.name = 'Arial'
        r_page.font.size = Pt(9.5)
        r_page.bold = True
        r_page.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    doc.add_page_break()

    # 1. INTRODUCCIÓN
    add_heading_1("1. Introducción y Justificación de la Gestión de Servicios TI")
    doc.add_paragraph(
        "En la ingeniería de software contemporánea, el desarrollo de aplicaciones informáticas ha superado definitivamente "
        "el enfoque tradicional centrado de forma exclusiva en la codificación y entrega de artefactos tecnológicos aislados. "
        "Bajo el paradigma de la Gestión de Servicios de Tecnologías de la Información (ITSM), un sistema tecnológico debe "
        "concebirse, desplegarse y administrarse como un medio estructurado para co-crear valor tangible para los usuarios y el negocio, "
        "habilitando los resultados estratégicos que la organización persigue sin que los clientes asuman directamente la carga "
        "de los costos operativos subyacentes ni los riesgos técnicos específicos (AXELOS, 2019; ISO/IEC, 2018)."
    )
    doc.add_paragraph(
        "Para el proyecto integrador Monchis Café —una plataforma web integral y sistema de punto de venta (POS) diseñado "
        "para una cafetería especializada en café orgánico de cooperativas mexicanas y productos comerciales—, la gestión rigurosa "
        "de servicios TI adquiere una trascendencia crítica. La operación de barra no puede tolerar caídas de servicio durante "
        "las horas pico matutinas, pérdidas de inventario de lotes orgánicos ni inconsistencias transaccionales al registrar cobros mixtos "
        "(efectivo, tarjeta bancaria y transferencias SPEI). Asimismo, los requerimientos de seguridad estatutaria (conforme a la "
        "Ley Federal de Protección de Datos Personales en Posesión de los Particulares - LFPDPPP) y el compromiso con los Objetivos "
        "de Desarrollo Sostenible (ODS 12: Producción y Consumo Responsables) exigen procesos estandarizados, gobernanza sólida "
        "y acuerdos de nivel de servicio (SLAs) formalizados."
    )
    doc.add_paragraph(
        "El objetivo fundamental de esta actividad es realizar una investigación exhaustiva sobre los marcos de trabajo y estándares "
        "más representativos en la gestión de servicios informáticos (ITIL, ISO/IEC 20000, COBIT, CMMI y TOGAF), seleccionar "
        "los dos marcos más pertinentes para Monchis Café (ITIL v4 e ISO/IEC 20000-1:2018), efectuar un análisis comparativo crítico "
        "y diseñar una estrategia integral de servicios TI articulada en las cinco fases del ciclo de vida ITIL, integrando valor, procesos, "
        "roles específicos y herramientas tecnológicas que aseguren la calidad, resiliencia y mejora continua del servicio."
    )

    # 2. INVESTIGACIÓN PRELIMINAR
    add_heading_1("2. Investigación Preliminar de Marcos de Trabajo y Estándares")
    doc.add_paragraph(
        "La gestión de servicios informáticos ha evolucionado mediante marcos de buenas prácticas y normas internacionales "
        "que proporcionan directrices probadas para planificar, entregar, operar y controlar servicios de tecnología:"
    )

    add_heading_2("2.1. ITIL (Information Technology Infrastructure Library)")
    doc.add_paragraph(
        "Desarrollado originalmente en el Reino Unido por la Central Computer and Telecommunications Agency (CCTA) y gestionado "
        "actualmente por AXELOS, ITIL representa el marco de referencia de facto más adoptado a nivel mundial para ITSM (Steinberg, 2011; Cartlidge et al., 2012). "
        "Históricamente, ITIL v3 (2007/2011) introdujo el modelo de Ciclo de Vida del Servicio dividido en cinco fases interconectadas: "
        "Estrategia del Servicio (Service Strategy), Diseño del Servicio (Service Design), Transición del Servicio (Service Transition), "
        "Operación del Servicio (Service Operation) y Mejora Continua del Servicio (Continual Service Improvement - CSI). "
        "Con la publicación de ITIL 4 en 2019, el marco evolucionó hacia un modelo más ágil, flexible y holístico denominado "
        "Sistema de Valor del Servicio (SVS), el cual incorpora la Cadena de Valor del Servicio (Service Value Chain), cuatro dimensiones "
        "de gestión (Organizaciones y personas; Información y tecnología; Socios y proveedores; Flujos de valor y procesos) y 34 prácticas "
        "de gestión (AXELOS, 2019). ITIL no impone reglas rígidas, sino que opera bajo la premisa de 'adoptar y adaptar' (adopt and adapt)."
    )

    add_heading_2("2.2. ISO/IEC 20000 (Norma Internacional de Gestión de Servicios de TI)")
    doc.add_paragraph(
        "La norma ISO/IEC 20000, desarrollada conjuntamente por ISO e IEC, constituye el primer estándar internacional auditable "
        "y certificable formalmente para la gestión de servicios de tecnología (ISO/IEC, 2018). Su parte medular, la ISO/IEC 20000-1:2018 "
        "('Service management system requirements'), establece los requisitos obligatorios para que un proveedor planifique, establezca, "
        "implemente, opere, monitoree, revise, mantenga y mejore un Sistema de Gestión de Servicios de TI (SGSTI / SMS). "
        "A diferencia de las guías descriptivas de ITIL, la norma ISO prescribe cláusulas normativas de cumplimiento estricto "
        "(cláusulas 4 a 10 bajo la estructura de alto nivel de ISO - High Level Structure), gobernadas por el ciclo de Deming: "
        "Planificar (Plan), Hacer (Do), Verificar (Check) y Actuar (Act) (Bon et al., 2020)."
    )

    add_heading_2("2.3. Otros Marcos Relevantes: COBIT 2019, CMMI-SVC y TOGAF")
    doc.add_paragraph(
        "• COBIT 2019 (Control Objectives for Information and Related Technologies): Creado por ISACA (2018), es el marco líder para la Gobernanza "
        "y Gestión de la Información y la Tecnología de la Empresa (EGIT). Mientras ITIL e ISO 20000 se concentran en cómo entregar y gestionar los servicios, "
        "COBIT opera en el nivel directivo, alineando los objetivos corporativos con los de TI mediante 40 objetivos en cinco dominios: EDM, APO, BAI, DSS y MEA.\n\n"
        "• CMMI-SVC (Capability Maturity Model Integration for Services): Desarrollado por el CMMI Institute (ISACA, 2020), evalúa y mejora "
        "la madurez y capacidad de los procesos de prestación de servicios a través de cinco niveles formales (Inicial, Gestionado, Definido, "
        "Gestionado Cuantitativamente y Optimizado). Es ampliamente utilizado en licitaciones que requieren certificación de procesos repetibles.\n\n"
        "• TOGAF (The Open Group Architecture Framework): Marco de referencia de The Open Group (2022) enfocado en Arquitectura Empresarial. "
        "A través de su Método de Desarrollo de Arquitectura (ADM), proporciona una estructura para diseñar, planificar e implementar las "
        "arquitecturas de negocio, datos, aplicaciones y tecnología."
    )

    doc.add_page_break()

    # 3. DESCRIPCIÓN DETALLADA DE LOS MARCOS SELECCIONADOS
    add_heading_1("3. Descripción Detallada de los Marcos Seleccionados")
    doc.add_paragraph(
        "Para el proyecto Monchis Café se seleccionan ITIL (en su versión v4 y ciclo de vida de servicio) y la norma ISO/IEC 20000-1:2018. "
        "A continuación se analizan sus principios, objetivos y áreas clave de aplicación."
    )

    add_heading_2("3.1. ITIL v4: Objetivos, Principios Guía y Áreas Clave")
    doc.add_paragraph(
        "Objetivo Fundamental: Facilitar la co-creación de valor mediante la gestión integral de productos y servicios digitales, "
        "brindando un marco operativo ágil, centrado en el cliente y adaptable a entornos en la nube y arquitecturas modernas (AXELOS, 2019).\n\n"
        "Principios Guía Universales de ITIL v4:\n"
        "1. Enfocarse en el valor (Focus on value): Cada acción y servicio debe generar valor directo o indirecto para las partes interesadas.\n"
        "2. Empezar donde se está (Start where you are): Aprovechar los servicios, código e infraestructura existentes sin reinventar la rueda.\n"
        "3. Progresar iterativamente con retroalimentación: Dividir el trabajo en partes manejables y validar con usuarios reales de barra.\n"
        "4. Colaborar y promover visibilidad: Compartir información transparente entre desarrollo, personal de barra y gerencia.\n"
        "5. Pensar y trabajar holísticamente: Ningún servicio opera de forma aislada; considerar siempre las 4 dimensiones de gestión.\n"
        "6. Mantenerlo simple y práctico: Eliminar burocracia innecesaria y diseñar interfaces táctiles directas a prueba de errores.\n"
        "7. Optimizar y automatizar: Maximizar la eficiencia humana mediante flujos automatizados (CI/CD, scripts de telemetría y backups).\n\n"
        "Áreas Clave de Aplicación: Gestión del portafolio y catálogo de servicios, gestión de niveles de servicio (SLA/OLA), habilitación del cambio, "
        "gestión de incidentes y solicitudes, gestión de problemas y mejora continua del servicio."
    )

    add_heading_2("3.2. ISO/IEC 20000-1:2018: Principios y Estructura Normativa")
    doc.add_paragraph(
        "Objetivo Fundamental: Establecer, implementar, mantener y mejorar continuamente un Sistema de Gestión de Servicios (SGSTI) formal, "
        "demostrando ante clientes y auditores que la organización cumple con estándares de calidad internacionales rigurosos (ISO/IEC, 2018).\n\n"
        "Principios y Estructura de Alto Nivel (HLS):\n"
        "• Contexto y Liderazgo (Cl. 4 y 5): Alcance formal del SGSTI, política de calidad y asignación de roles y autoridades directivas.\n"
        "• Planificación y Apoyo (Cl. 6 y 7): Gestión proactiva de riesgos y oportunidades, objetivos del servicio y provisión de recursos y competencias.\n"
        "• Operación del Servicio (Cl. 8): Planificación operativa, portafolio, acuerdos de servicio (SLAs), diseño y transición, resolución de incidentes y problemas, "
        "y aseguramiento del servicio (disponibilidad, continuidad del negocio, seguridad de la información y control del cambio).\n"
        "• Evaluación y Mejora (Cl. 9 y 10): Monitoreo de métricas, auditorías internas, gestión de no conformidades y mejora continua con ciclo PDCA."
    )

    # 4. ANÁLISIS COMPARATIVO
    add_heading_1("4. Análisis Comparativo entre ITIL e ISO/IEC 20000-1")
    doc.add_paragraph(
        "Aunque ambos marcos coinciden en la entrega de valor al cliente, difieren en alcance, obligatoriedad y metodología operativa:"
    )

    t_comp_headers = ["Dimensión Analítica", "ITIL v4 (AXELOS)", "ISO/IEC 20000-1:2018 (ISO/IEC)", "Impacto en Monchis Café"]
    t_comp_rows = [
        [
            "Naturaleza y Propósito",
            "Marco de referencia de buenas prácticas descriptivas. Explica el 'cómo' gestionar servicios de TI con agilidad y flexibilidad.",
            "Estándar internacional normativo y prescriptivo. Dictamina el 'qué debe cumplir' formalmente un SGSTI auditable.",
            "ITIL guía el desarrollo técnico ágil (RabbitMQ, Vue 3); ISO 20000 garantiza el control riguroso de cambios y seguridad de datos."
        ],
        [
            "Certificación Formal",
            "Certificación para personas y profesionales (Fundamentos, Managing Professional). No certifica empresas.",
            "Certificación formal para organizaciones emitida por organismos acreditadores externos tras auditoría de conformidad.",
            "Permite a Ernesto Hatuey formarse en ITIL como arquitecto, mientras el diseño del software queda listo para certificación ISO 20000."
        ],
        [
            "Enfoque de Adopción",
            "Filosofía de 'Adoptar y adaptar'. Las organizaciones toman solo las prácticas que agregan valor y descartan lo superfluo.",
            "Cumplimiento obligatorio de todas las cláusulas normativas (cláusulas 4 a 10) para superar auditorías sin no conformidades.",
            "Evita burocracia: adaptamos ITIL a la escala de cafetería, pero adoptamos las cláusulas críticas de ISO 20000 en seguridad y continuidad."
        ],
        [
            "Ciclo de Vida y Valor",
            "Enfoque en Sistema de Valor del Servicio (SVS), 4 dimensiones y co-creación de valor entre proveedor y cliente.",
            "Enfoque estructurado por procesos alineado al ciclo Deming (PDCA: Planificar, Hacer, Verificar, Actuar) y mejora continua.",
            "Armonización perfecta: las fases del ciclo de vida ITIL definen el flujo operativo, mientras el PDCA asegura auditoría continua."
        ],
        [
            "Gestión del Cambio",
            "Habilitación del cambio (Change Enablement) con evaluación de riesgos basada en velocidad y valor, y comité ágil (CAB).",
            "Control formal de cambios, evaluación documental rigurosa de impacto y mitigación obligatoria de riesgos del servicio.",
            "Protege el POS en barra: ningún cambio se despliega sin pruebas automatizadas (CI/CD) ni plan de marcha atrás (rollback)."
        ],
        [
            "Costo y Complejidad",
            "Bajo costo de adopción interna; altamente flexible y compatible con metodologías ágiles (Scrum, DevOps, Kanban).",
            "Requiere disciplina documental estricta y costos de auditoría externa si se busca la certificación oficial.",
            "Para Monchis Café, adoptamos las directrices ISO 20000 internamente como política de calidad sin incurrir en costos de certificación."
        ]
    ]

    t_comp = doc.add_table(rows=len(t_comp_rows) + 1, cols=4)
    t_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_comp._tbl.tblPr.append(parse_xml(
        r'<w:tblBorders %s>'
        r'<w:top w:val="single" w:sz="6" w:space="0" w:color="A0AEC0"/>'
        r'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="A0AEC0"/>'
        r'<w:left w:val="single" w:sz="6" w:space="0" w:color="A0AEC0"/>'
        r'<w:right w:val="single" w:sz="6" w:space="0" w:color="A0AEC0"/>'
        r'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/>'
        r'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/>'
        r'</w:tblBorders>' % nsdecls('w')
    ))

    comp_widths = [Inches(1.3), Inches(1.8), Inches(1.8), Inches(1.8)]
    for idx, text in enumerate(t_comp_headers):
        cell = t_comp.rows[0].cells[idx]
        cell.width = comp_widths[idx]
        cell.text = text
        set_cell_shading(cell, "1A365D")
        set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.runs[0]
        run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for r_idx, r_data in enumerate(t_comp_rows):
        row = t_comp.rows[r_idx + 1]
        bg_col = "F7FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.width = comp_widths[c_idx]
            cell.text = val
            set_cell_shading(cell, bg_col)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.1
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            run = p.runs[0]
            run.font.name = 'Arial'
            run.font.size = Pt(8)
            if c_idx == 0:
                run.bold = True
                run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
            else:
                run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)

    add_heading_2("4.2. Sinergia Metodológica en el Contexto del Proyecto")
    doc.add_paragraph(
        "La integración conjunta de ITIL v4 e ISO/IEC 20000-1 crea una potente sinergia técnica y de negocio. ITIL proporciona "
        "las mejores prácticas operativas y la flexibilidad ágil que un proyecto dinámico requiere, mientras que la norma ISO "
        "aporta la estructura formal de gobernanza, la gestión preventiva del riesgo y el aseguramiento sistemático de la calidad "
        "a través del ciclo PDCA. De este modo, Monchis Café evita tanto una implementación burocrática y rígida como una operación desordenada."
    )

    doc.add_page_break()

    # 5. ADAPTACIÓN AL PROYECTO FINAL: MONCHIS CAFÉ
    add_heading_1("5. Adaptación de los Marcos al Proyecto Final: Monchis Café")

    add_heading_2("5.1. Justificación de Elección según Requisitos de Monchis Café")
    doc.add_paragraph(
        "La selección de ITIL v4 e ISO/IEC 20000-1 se fundamenta directamente en las necesidades de Monchis Café:\n\n"
        "1. Requisitos Técnicos y de Negocio: Frontend reactivo en Vue 3 para tabletas de barra, backend en Next.js, base de datos PostgreSQL "
        "con Prisma y broker RabbitMQ con patrón Saga para transacciones concurrentes. Requisitos de cobro multimodal en <45 s, rotación PEPS "
        "de café orgánico y gamificación Monchis Rewards demandan alta disponibilidad (99.9%) y consistencia transaccional absoluta.\n\n"
        "2. Necesidades Operativas: Cajeros y baristas requieren interfaces amigables y un canal de soporte técnico ágil (MTTR < 60 min) "
        "para evitar que un fallo en terminal congele las ventas en horas pico matutinas.\n\n"
        "3. Beneficios Cuantificables: Reducción del 85% en merma de café orgánico por alertas de caducidad, ahorro de más de $36,000 MXN anuales "
        "en licencias cerradas y protección de datos conforme a la ley LFPDPPP."
    )

    add_heading_2("5.2. Estrategia de Servicios TI en las Fases del Ciclo de Vida ITIL")
    doc.add_paragraph(
        "A continuación se adapta la estrategia integral de servicios TI articulada en las cinco fases del ciclo de vida ITIL e ISO 20000:"
    )

    add_heading_3("5.2.1. Estrategia del Servicio (Service Strategy)")
    doc.add_paragraph(
        "• Valor del Servicio: Utilidad ('Fit for Purpose': acelerar el cobro a <45 s, certificar café orgánico y bonificar $5.00 MXN por termo - ODS 12) "
        "y Garantía ('Fit for Use': disponibilidad 99.9%, seguridad stateless con JWT en cookies HttpOnly y resiliencia Saga en RabbitMQ).\n"
        "• Portafolio y Catálogo: Servicios Principales (POS Táctil Omnicanal, Trazabilidad Orgánica PEPS, Monedero Digital Rewards), "
        "Habilitadores (RabbitMQ Saga, PostgreSQL transaccional, Seguridad JWT/2FA) y Soporte (Mesa de Ayuda N1/N2, Backups RTO<1h, Monitoreo /api/health)."
    )

    add_heading_3("5.2.2. Diseño del Servicio (Service Design)")
    doc.add_paragraph(
        "• Acuerdos de Nivel de Servicio (SLAs): SLA-POS-01 (Disponibilidad mensual >= 99.9%); SLA-POS-02 (Latencia P95 <= 400 ms); "
        "SLA-INC-01 (Respuesta en barra <= 15 min; resolución MTTR <= 60 min).\n"
        "• Continuidad y Seguridad (ISO 20000 Cl. 8.7): RPO <= 15 min y RTO <= 60 min con respaldos incrementales cifrados en la nube, "
        "encriptación TLS 1.3, reCAPTCHA v3 y control de acceso basado en roles (RBAC: Cajero, Barista, Administrador)."
    )

    add_heading_3("5.2.3. Transición del Servicio (Service Transition)")
    doc.add_paragraph(
        "• Habilitación del Cambio: Clasificación en Cambios Estándar (preaprobados), Cambios Normales (pruebas en staging y aprobación) "
        "y Cambios de Emergencia (parches urgentes con comité de emergencia CAB).\n"
        "• Liberación y Configuración: Pipeline CI/CD en GitHub Actions (validación de tipos, lint y Vitest), imágenes contenerizadas Docker "
        "multi-stage y monorepo estructurado con Turborepo."
    )

    add_heading_3("5.2.4. Operación del Servicio (Service Operation)")
    doc.add_paragraph(
        "• Mesa de Ayuda (Service Desk): Nivel 0 (Validaciones táctiles de autoservicio), Nivel 1 (Soporte en sitio por barista líder "
        "para impresoras térmicas y red) y Nivel 2 (Soporte especializado por Ernesto Hatuey para base de datos y RabbitMQ).\n"
        "• Problemas y Monitoreo: Causa raíz inspeccionando la Dead Letter Queue (DLQ) de RabbitMQ y supervisión periódica del endpoint `/api/health`."
    )

    add_heading_3("5.2.5. Mejora Continua del Servicio (Continual Service Improvement - CSI)")
    doc.add_paragraph(
        "• Ciclo Deming (PDCA) y 7 Pasos ITIL: Planificar (definir métricas de cobro y merma), Hacer (recopilar datos con `correlation_id`), "
        "Verificar (evaluar SLAs en revisión directiva mensual) y Actuar (registrar iniciativas en el Registro de Mejora Continua - CIR)."
    )

    doc.add_page_break()

    # 5.3. MATRIZ INTEGRADORA Y EJEMPLOS
    add_heading_2("5.3. Matriz Integradora: Valor, Procesos, Roles y Herramientas")
    doc.add_paragraph(
        "La siguiente matriz consolida la articulación de la estrategia cumpliendo con los cuatro elementos clave exigidos:"
    )

    t_matriz_headers = ["Fase ITIL / ISO", "Valor Generado para Monchis Café", "Procesos y Prácticas Clave", "Roles y Responsables", "Herramientas Tecnológicas"]
    t_matriz_rows = [
        [
            "Estrategia\n(ISO Cl. 4 y 6)",
            "Alineación tecnológica con rentabilidad comercial, agilidad en barra y sustentabilidad ecológica (ODS 12).",
            "• Portafolio de Servicios\n• Gestión Financiera TI\n• Relaciones con Negocio\n• Utilidad y Garantía",
            "• Líder TI (Ernesto Hatuey)\n• Dueño / Gerencia General",
            "• Hoja CAPEX/OPEX\n• Catálogo de Servicios\n• Matriz ODS 12"
        ],
        [
            "Diseño\n(ISO Cl. 8.2 y 8.7)",
            "Disponibilidad 99.9%, cobro en caja < 45 s y protección estricta de datos personales (LFPDPPP).",
            "• Niveles de Servicio (SLAs)\n• Continuidad (RTO/RPO)\n• Seguridad de la Info.\n• Capacidad y Disponibilidad",
            "• Arquitecto de Software\n• Ingeniero de Requerimientos",
            "• Prisma ORM & PostgreSQL\n• JWT en cookies HttpOnly\n• Google reCAPTCHA v3"
        ],
        [
            "Transición\n(ISO Cl. 8.5 y 8.6)",
            "Despliegues sin interrupción de ventas en mostrador, cero regresiones y compilación estandarizada.",
            "• Habilitación del Cambio\n• Liberación (Release Mgmt)\n• Gestión de Activos (SACM)\n• Pruebas de Regresión",
            "• Desarrollador Full-Stack\n• Comité de Cambios (CAB)\n• Cajero líder (UAT)",
            "• GitHub Actions (CI/CD)\n• Vitest (Pruebas unitarias)\n• Docker multi-stage\n• Turborepo monorepo"
        ],
        [
            "Operación\n(ISO Cl. 8.3 y 8.4)",
            "Resolución rápida de fallos en barra (MTTR < 60 min), cuadres de caja exactos y flujo ininterrumpido.",
            "• Mesa de Ayuda (Service Desk)\n• Gestión de Incidentes\n• Gestión de Problemas (RCA)\n• Eventos y Monitoreo",
            "• Operador N1 (Cajero/Barista)\n• Soporte N2 (Ernesto Hatuey)\n• Proveedor ISP de enlace",
            "• POS táctil en Vue 3\n• RabbitMQ Topic Exchange\n• Dead Letter Queue (DLQ)\n• Endpoint /api/health"
        ],
        [
            "Mejora Continua\n(ISO Cl. 9 y 10)",
            "Optimización iterativa basada en métricas reales de ventas, reducción de mermas y retención Rewards.",
            "• Ciclo Deming PDCA\n• 7 Pasos de Mejora ITIL\n• Auditoría de Servicio\n• Medición de CSFs y KPIs",
            "• Líder de Mejora Continua\n• Gerente de Cafetería",
            "• Panel Analítico Next.js\n• Registro de Mejora (CIR)\n• Atribución UTM campañas"
        ]
    ]

    t_matriz = doc.add_table(rows=len(t_matriz_rows) + 1, cols=5)
    t_matriz.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_matriz._tbl.tblPr.append(parse_xml(
        r'<w:tblBorders %s>'
        r'<w:top w:val="single" w:sz="6" w:space="0" w:color="A0AEC0"/>'
        r'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="A0AEC0"/>'
        r'<w:left w:val="single" w:sz="6" w:space="0" w:color="A0AEC0"/>'
        r'<w:right w:val="single" w:sz="6" w:space="0" w:color="A0AEC0"/>'
        r'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/>'
        r'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/>'
        r'</w:tblBorders>' % nsdecls('w')
    ))

    matriz_widths = [Inches(1.2), Inches(1.5), Inches(1.5), Inches(1.3), Inches(1.2)]
    for idx, text in enumerate(t_matriz_headers):
        cell = t_matriz.rows[0].cells[idx]
        cell.width = matriz_widths[idx]
        cell.text = text
        set_cell_shading(cell, "1A365D")
        set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.runs[0]
        run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for r_idx, r_data in enumerate(t_matriz_rows):
        row = t_matriz.rows[r_idx + 1]
        bg_col = "F7FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.width = matriz_widths[c_idx]
            cell.text = val
            set_cell_shading(cell, bg_col)
            set_cell_margins(cell, top=60, bottom=60, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.1
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            run = p.runs[0]
            run.font.name = 'Arial'
            run.font.size = Pt(8)
            if c_idx == 0:
                run.bold = True
                run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
            else:
                run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)

    add_heading_2("5.4. Ejemplos Específicos de Aplicación en Fases Clave del Proyecto")
    doc.add_paragraph(
        "• Gestión de Riesgos (Consistencia Transaccional con Saga): En picos matutinos, dos clientes piden simultáneamente el último lote "
        "de café de Oaxaca. Para evitar cobros en descubierto, el orquestador Saga en RabbitMQ detecta el desabasto y ejecuta una compensación "
        "automática: cancela la preautorización bancaria y notifica a la pantalla táctil para ofrecer otra variedad sin descuadrar la caja.\n\n"
        "• Entrega de Servicios (Despliegue de Actualizaciones al POS): Se actualiza el software de barra clasificándolo como 'Cambio Normal'. "
        "Pasa por el pipeline CI/CD de GitHub Actions y se despliega a las 22:30 hrs (fuera de horario comercial) mediante contenedores Docker "
        "con estrategia Zero-Downtime y procedimiento formal de marcha atrás (rollback < 90 s).\n\n"
        "• Mejora Continua (Telemetría de Latencia): Mediante análisis de logs con `correlation_id` y `/api/health`, se identificó que la consulta "
        "de trazabilidad demoraba 1,200 ms. Se añadió un índice compuesto en PostgreSQL (`numero_lote`, `fecha_caducidad`), reduciendo "
        "la latencia P95 a 65 ms, documentándose en la revisión directiva mensual."
    )

    add_heading_2("5.5. Esquema Conceptual de la Estrategia de Servicios TI")
    p_diag = doc.add_paragraph()
    p_diag.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_diag.paragraph_format.space_before = Pt(4)
    p_diag.paragraph_format.space_after = Pt(4)
    r_diag = p_diag.add_run(
        "┌────────────────────────────────────────────────────────────────────────────────────────┐\n"
        "│         ESTRATEGIA INTEGRAL DE SERVICIOS TI — \"MONCHIS CAFÉ\" (ITIL v4 + ISO 20000)     │\n"
        "├────────────────────────────┬────────────────────────────┬──────────────────────────────┤\n"
        "│ 1. ESTRATEGIA (Plan / Cl.6) │ 2. DISEÑO (Do / Cl. 8.2)   │ 3. TRANSICIÓN (Do / Cl. 8.5) │\n"
        "│ • Utilidad: Cobro < 45 s   │ • SLA: 99.9% Uptime, P95<400│ • Habilitación del Cambio    │\n"
        "│ • Garantía: Uptime, LFPDPPP│ • RTO < 1h, RPO < 15m      │ • CI/CD con GitHub Actions   │\n"
        "│ • Catálogo: Core / Support │ • Seguridad: JWT + reCAPTCHA│ • Docker multi-stage + Vitest│\n"
        "├────────────────────────────┴─────────────┬──────────────┴──────────────────────────────┤\n"
        "│ 4. OPERACIÓN (Do / Cl. 8.3-8.4)          │ 5. MEJORA CONTINUA (Check/Act / Cl. 9-10)   │\n"
        "│ • Mesa de Ayuda: Niveles N0 / N1 / N2    │ • Ciclo Deming PDCA + Registro CIR          │\n"
        "│ • RabbitMQ + Patrón Saga (DLQ)           │ • Análisis mensual de KPIs y latencia P95   │\n"
        "│ • POS Táctil Vue 3 + Telemetría /health  │ • Optimización de índices en PostgreSQL     │\n"
        "└──────────────────────────────────────────┴─────────────────────────────────────────────┘"
    )
    r_diag.font.name = 'Courier New'
    r_diag.font.size = Pt(7)
    r_diag.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

    doc.add_page_break()

    # 6. CONCLUSIONES Y DESAFÍOS DE ADAPTACIÓN
    add_heading_1("6. Conclusiones y Desafíos de Adaptación")
    doc.add_paragraph(
        "El desarrollo de esta actividad formativa permite consolidar una visión profesional y madura sobre el papel de las tecnologías "
        "de información en el ámbito empresarial contemporáneo. Diseñar una plataforma como Monchis Café no consiste meramente en concatenar "
        "componentes de frontend en Vue 3 o rutas API en Next.js; la verdadera viabilidad comercial y operativa de un sistema depende "
        "de su concepción como un servicio gestionado de extremo a extremo, donde la disponibilidad, la seguridad, la trazabilidad y la resolución "
        "de incidentes están formalmente pactadas, monitoreadas y protegidas bajo estándares reconocidos internacionalmente."
    )
    doc.add_paragraph(
        "La integración conjunta de ITIL v4 e ISO/IEC 20000-1:2018 demostró ser la combinación ideal para el proyecto. ITIL suministra "
        "el marco de referencia ágil, centrado en el cliente y enfocado en la co-creación de valor real, guiando las prácticas operativas "
        "diarias del punto de venta y la resiliencia transaccional con RabbitMQ Saga. Simultáneamente, la norma ISO aporta la disciplina de control, "
        "la gestión estructurada del riesgo y el compromiso irrenunciable con la mejora continua mediante el ciclo PDCA, dotando a Monchis Café "
        "de una arquitectura técnica lista para operar bajo auditorías rigurosas y con pleno cumplimiento de la ley de protección de datos personales."
    )
    doc.add_paragraph(
        "Principales Desafíos Enfrentados en la Adaptación:\n\n"
        "1. Evitar la Sobrecarga Burocrática: Uno de los riesgos inherentes al aplicar estándares corporativos como ISO 20000 a una pequeña empresa "
        "o proyecto individual es la tentación de generar documentación estéril o comités innecesarios. El desafío se superó aplicando el principio guía "
        "de ITIL 'Mantenerlo simple y práctico' (Keep it simple and practical), automatizando el control de cambios y las pruebas mediante pipelines de CI/CD.\n\n"
        "2. Dimensión Humana y Capacitación Operativa: El personal de barra (cajeros y baristas) tiene una rotación natural y no cuenta con formación informática. "
        "La estrategia TI resolvió esta brecha mediante un diseño de interfaz táctil guiado por prevención de errores, manuales de Nivel 0 intuitivos "
        "y un canal directo de soporte técnico N1/N2 con tiempos de respuesta bajo SLA garantizados.\n\n"
        "3. Disciplina en la Medición y Mejora: La mejora continua exige recopilar datos objetivos en lugar de impresiones empíricas. "
        "Integrar trazabilidad estructurada de logs con identificadores únicos (`correlation_id`) y endpoints de salud representa un esfuerzo técnico "
        "adicional en la arquitectura, pero constituye el único medio para identificar cuellos de botella antes de que afecten la atención al público."
    )

    doc.add_page_break()

    # 7. REFERENCIAS BIBLIOGRÁFICAS (APA 7)
    add_heading_1("7. Referencias Bibliográficas")
    references = [
        "AXELOS. (2019). <i>ITIL Foundation: ITIL 4 Edition</i>. The Stationery Office (TSO).",
        "Bon, J. van, Pieper, M., & Veen, A. van der. (2020). <i>Foundations of IT Service Management with ISO/IEC 20000-1:2018</i>. Van Haren Publishing.",
        "Cartlidge, A., Hanna, A., Rudd, C., Macfarlane, I., Windebank, J., & Rance, S. (2012). <i>An introductory overview of ITIL V3</i>. The UK Chapter of the itSMF.",
        "International Organization for Standardization, & International Electrotechnical Commission. (2018). <i>Information technology — Service management — Part 1: Service management system requirements</i> (ISO/IEC Standard No. 20000-1:2018). ISO/IEC. https://www.iso.org/standard/70636.html",
        "International Organization for Standardization, & International Electrotechnical Commission. (2019). <i>Information technology — Service management — Part 2: Guidance on the application of service management systems</i> (ISO/IEC Standard No. 20000-2:2019). ISO/IEC.",
        "ISACA. (2018). <i>COBIT 2019 Framework: Introduction and methodology</i>. Information Systems Audit and Control Association.",
        "ISACA. (2020). <i>CMMI for Services, Version 2.0</i>. CMMI Institute.",
        "Steinberg, R. A. (2011). <i>ITIL Service Strategy (2011 edition)</i>. The Stationery Office (TSO).",
        "The Open Group. (2022). <i>The TOGAF Standard, 10th Edition: Introduction and core concepts</i>. The Open Group."
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(6)
        
        parts = ref.split("<i>")
        for part in parts:
            if "</i>" in part:
                italic_text, normal_text = part.split("</i>")
                r_it = p_ref.add_run(italic_text)
                r_it.font.name = 'Arial'
                r_it.font.size = Pt(9.5)
                r_it.italic = True
                r_it.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
                
                r_norm = p_ref.add_run(normal_text)
                r_norm.font.name = 'Arial'
                r_norm.font.size = Pt(9.5)
                r_norm.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
            else:
                r_norm = p_ref.add_run(part)
                r_norm.font.name = 'Arial'
                r_norm.font.size = Pt(9.5)
                r_norm.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)

    os.makedirs(entregables_dir, exist_ok=True)
    doc.save(docx_path)
    print(f"DOCX generado: {docx_path}")
    shutil.copyfile(docx_path, download_docx)
    print(f"DOCX copiado a Descargas: {download_docx}")

    # =========================================================================
    # 2. CONSTRUCCIÓN DEL DOCUMENTO HTML PARA PDF CON EXACTAMENTE 8 PÁGINAS
    # =========================================================================
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Actividad 3.6: Investigación y Aplicación de Marcos de Trabajo y Estándares en la Gestión de Servicios Informáticos</title>
  <style>
    @page {{
      size: letter;
      margin: 2.1cm 2.0cm 2.1cm 2.0cm;
      @bottom-right {{
        content: counter(page);
        font-family: Arial, sans-serif;
        font-size: 8.5pt;
        color: #718096;
      }}
    }}
    body {{
      font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif;
      font-size: 9.8pt;
      line-height: 1.28;
      color: #2D3748;
      background: #FFFFFF;
      margin: 0;
      padding: 0;
    }}
    .page-break {{
      page-break-before: always;
    }}
    .cover {{
      text-align: center;
      padding-top: 2.5cm;
      padding-bottom: 2cm;
      box-sizing: border-box;
    }}
    .inst-header {{
      font-size: 12.5pt;
      font-weight: bold;
      color: #1A365D;
      text-transform: uppercase;
      margin-bottom: 4px;
      letter-spacing: 0.5px;
    }}
    .subinst-header {{
      font-size: 10pt;
      color: #4A5568;
      margin-bottom: 35px;
      line-height: 1.35;
    }}
    .doc-title {{
      font-size: 16pt;
      font-weight: bold;
      color: #1A365D;
      margin-bottom: 10px;
      line-height: 1.25;
      text-transform: uppercase;
    }}
    .doc-subtitle {{
      font-size: 11pt;
      font-style: italic;
      color: #4A5568;
      margin-bottom: 45px;
      line-height: 1.35;
    }}
    .meta-box {{
      margin: 0 auto;
      max-width: 560px;
      border-top: 2px solid #CBD5E0;
      border-bottom: 2px solid #CBD5E0;
      padding: 18px 8px;
      font-size: 9.5pt;
      line-height: 1.55;
      text-align: left;
    }}
    .meta-box table {{
      width: 100%;
      border-collapse: collapse;
    }}
    .meta-box td {{
      padding: 3px 5px;
      border: none;
    }}
    .meta-box td.label {{
      font-weight: bold;
      color: #1A365D;
      width: 32%;
    }}
    .meta-box td.val {{
      color: #2D3748;
    }}
    h1 {{
      font-size: 12.5pt;
      font-weight: bold;
      color: #1A365D;
      border-bottom: 1.5px solid #CBD5E0;
      padding-bottom: 3px;
      margin-top: 14px;
      margin-bottom: 7px;
      page-break-after: avoid;
    }}
    h2 {{
      font-size: 10.8pt;
      font-weight: bold;
      color: #2B4C7E;
      margin-top: 10px;
      margin-bottom: 4px;
      page-break-after: avoid;
    }}
    h3 {{
      font-size: 9.8pt;
      font-weight: bold;
      font-style: italic;
      color: #2D3748;
      margin-top: 8px;
      margin-bottom: 3px;
      page-break-after: avoid;
    }}
    p {{
      margin-top: 0;
      margin-bottom: 6px;
      text-align: justify;
    }}
    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 8px;
      margin-bottom: 10px;
      font-size: 7.8pt;
    }}
    table.data-table th {{
      background-color: #1A365D;
      color: #FFFFFF;
      font-weight: bold;
      padding: 5px 5px;
      text-align: center;
      border: 1px solid #A0AEC0;
    }}
    table.data-table td {{
      padding: 4px 5px;
      border: 1px solid #CBD5E0;
      vertical-align: top;
      line-height: 1.2;
    }}
    table.data-table tr:nth-child(even) {{
      background-color: #F7FAFC;
    }}
    .diagram-box {{
      background: #F8FAFC;
      border: 1px solid #CBD5E0;
      border-radius: 4px;
      padding: 6px;
      margin: 8px 0;
      font-family: 'Courier New', Courier, monospace;
      font-size: 7pt;
      line-height: 1.1;
      color: #1A365D;
      white-space: pre;
    }}
    .toc-item {{
      display: flex;
      justify-content: space-between;
      margin-bottom: 3px;
      font-size: 9pt;
    }}
    .toc-title {{
      color: #2D3748;
    }}
    .toc-dots {{
      flex-grow: 1;
      border-bottom: 1px dotted #A0AEC0;
      margin: 0 5px 2px 5px;
    }}
    .toc-page {{
      font-weight: bold;
      color: #1A365D;
    }}
    .ref-entry {{
      padding-left: 20px;
      text-indent: -20px;
      margin-bottom: 6px;
      font-size: 9pt;
      line-height: 1.25;
      text-align: justify;
    }}
  </style>
</head>
<body>

  <!-- PÁGINA 1: PORTADA -->
  <div class="cover">
    <div class="inst-header">Universidad de Guadalajara</div>
    <div class="inst-header">Centro Universitario de Tonalá (CUTonalá)</div>
    <div class="subinst-header">
      División de Ingenierías e Innovación Tecnológica<br>
      Licenciatura en Ingeniería en Computación<br>
      Módulo 2: Buenas Prácticas de Calidad en el Desarrollo de Software
    </div>

    <div class="doc-title">
      Actividad 3.6: Investigación y Aplicación de Marcos de Trabajo y Estándares en la Gestión de Servicios Informáticos
    </div>
    <div class="doc-subtitle">
      Diseño de la Estrategia de Servicios TI basada en el Ciclo de Vida ITIL e ISO/IEC 20000-1 para la Plataforma Monchis Café
    </div>

    <div class="meta-box">
      <table>
        <tr>
          <td class="label">Docente:</td>
          <td class="val">Dr. Gabriel Navarro Salcedo</td>
        </tr>
        <tr>
          <td class="label">Estudiante:</td>
          <td class="val">Ernesto Hatuey Fierro Meléndez</td>
        </tr>
        <tr>
          <td class="label">Código Estudiantil:</td>
          <td class="val">215487963</td>
        </tr>
        <tr>
          <td class="label">Proyecto Integrador:</td>
          <td class="val">Monchis Café — Plataforma Web Segura para Cafetería Orgánica y Comercial</td>
        </tr>
        <tr>
          <td class="label">Especialidad:</td>
          <td class="val">Arquitectura de Software y Gestión de Servicios TI</td>
        </tr>
        <tr>
          <td class="label">Fecha de Entrega:</td>
          <td class="val">26 de octubre de 2026</td>
        </tr>
        <tr>
          <td class="label">Ciclo Académico:</td>
          <td class="val">2026-B</td>
        </tr>
      </table>
    </div>
  </div>

  <!-- PÁGINA 2: ÍNDICE GENERAL -->
  <div class="page-break"></div>
  <h1>Índice General</h1>
  <div style="margin-top: 15px;">
    <div class="toc-item"><span class="toc-title">1. Introducción y Justificación de la Gestión de Servicios TI</span><span class="toc-dots"></span><span class="toc-page">3</span></div>
    <div class="toc-item"><span class="toc-title">2. Investigación Preliminar de Marcos de Trabajo y Estándares</span><span class="toc-dots"></span><span class="toc-page">3</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span class="toc-title">2.1. ITIL (Information Technology Infrastructure Library)</span><span class="toc-dots"></span><span class="toc-page">3</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span class="toc-title">2.2. ISO/IEC 20000 (Sistema de Gestión de Servicios TI)</span><span class="toc-dots"></span><span class="toc-page">3</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span class="toc-title">2.3. Otros Marcos Relevantes: COBIT 2019, CMMI-SVC y TOGAF</span><span class="toc-dots"></span><span class="toc-page">3</span></div>
    <div class="toc-item"><span class="toc-title">3. Descripción Detallada de los Marcos Seleccionados</span><span class="toc-dots"></span><span class="toc-page">4</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span class="toc-title">3.1. ITIL v4: Objetivos, Principios Guía y Áreas Clave</span><span class="toc-dots"></span><span class="toc-page">4</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span class="toc-title">3.2. ISO/IEC 20000-1:2018: Principios y Estructura Normativa</span><span class="toc-dots"></span><span class="toc-page">4</span></div>
    <div class="toc-item"><span class="toc-title">4. Análisis Comparativo entre ITIL e ISO/IEC 20000</span><span class="toc-dots"></span><span class="toc-page">4</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span class="toc-title">4.1. Matriz Comparativa Multidimensional</span><span class="toc-dots"></span><span class="toc-page">4</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span class="toc-title">4.2. Sinergia Metodológica en el Contexto del Proyecto</span><span class="toc-dots"></span><span class="toc-page">4</span></div>
    <div class="toc-item"><span class="toc-title">5. Adaptación al Proyecto Final: Monchis Café</span><span class="toc-dots"></span><span class="toc-page">5</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span class="toc-title">5.1. Justificación de Elección según Requisitos de Monchis Café</span><span class="toc-dots"></span><span class="toc-page">5</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span class="toc-title">5.2. Estrategia de Servicios TI en las Fases del Ciclo de Vida ITIL</span><span class="toc-dots"></span><span class="toc-page">5</span></div>
    <div class="toc-item" style="padding-left: 24px;"><span class="toc-title">5.2.1. Estrategia del Servicio (Service Strategy)</span><span class="toc-dots"></span><span class="toc-page">5</span></div>
    <div class="toc-item" style="padding-left: 24px;"><span class="toc-title">5.2.2. Diseño del Servicio (Service Design)</span><span class="toc-dots"></span><span class="toc-page">5</span></div>
    <div class="toc-item" style="padding-left: 24px;"><span class="toc-title">5.2.3. Transición del Servicio (Service Transition)</span><span class="toc-dots"></span><span class="toc-page">5</span></div>
    <div class="toc-item" style="padding-left: 24px;"><span class="toc-title">5.2.4. Operación del Servicio (Service Operation)</span><span class="toc-dots"></span><span class="toc-page">5</span></div>
    <div class="toc-item" style="padding-left: 24px;"><span class="toc-title">5.2.5. Mejora Continua del Servicio (Continual Service Improvement)</span><span class="toc-dots"></span><span class="toc-page">5</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span class="toc-title">5.3. Matriz Integradora: Valor, Procesos, Roles y Herramientas</span><span class="toc-dots"></span><span class="toc-page">6</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span class="toc-title">5.4. Ejemplos Específicos de Aplicación en Fases Clave</span><span class="toc-dots"></span><span class="toc-page">6</span></div>
    <div class="toc-item" style="padding-left: 24px;"><span class="toc-title">5.4.1. Gestión de Riesgos: Consistencia Transaccional con RabbitMQ Saga</span><span class="toc-dots"></span><span class="toc-page">6</span></div>
    <div class="toc-item" style="padding-left: 24px;"><span class="toc-title">5.4.2. Entrega de Servicios: Despliegue de Actualizaciones al POS en Barra</span><span class="toc-dots"></span><span class="toc-page">6</span></div>
    <div class="toc-item" style="padding-left: 24px;"><span class="toc-title">5.4.3. Mejora Continua: Telemetría de Latencia y Desabasto de Café Orgánico</span><span class="toc-dots"></span><span class="toc-page">6</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span class="toc-title">5.5. Esquema Conceptual de la Estrategia de Servicios TI</span><span class="toc-dots"></span><span class="toc-page">6</span></div>
    <div class="toc-item"><span class="toc-title">6. Conclusiones y Desafíos de Adaptación</span><span class="toc-dots"></span><span class="toc-page">7</span></div>
    <div class="toc-item"><span class="toc-title">7. Referencias Bibliográficas (Normas APA 7.ª edición)</span><span class="toc-dots"></span><span class="toc-page">8</span></div>
  </div>

  <!-- PÁGINA 3: INTRODUCCIÓN Y MARCOS PRELIMINARES -->
  <div class="page-break"></div>
  <h1>1. Introducción y Justificación de la Gestión de Servicios TI</h1>
  <p>
    En la ingeniería de software contemporánea, el desarrollo de aplicaciones informáticas ha superado definitivamente el enfoque tradicional centrado de forma exclusiva en la codificación y entrega de artefactos tecnológicos aislados. Bajo el paradigma de la Gestión de Servicios de Tecnologías de la Información (ITSM), un sistema tecnológico debe concebirse, desplegarse y administrarse como un medio estructurado para co-crear valor tangible para los usuarios y el negocio, habilitando los resultados estratégicos que la organización persigue sin que los clientes asuman directamente la carga de los costos operativos subyacentes ni los riesgos técnicos específicos (AXELOS, 2019; ISO/IEC, 2018).
  </p>
  <p>
    Para el proyecto integrador Monchis Café —una plataforma web integral y sistema de punto de venta (POS) diseñado para una cafetería especializada en café orgánico de cooperativas mexicanas y productos comerciales—, la gestión rigurosa de servicios TI adquiere una trascendencia crítica. La operación de barra no puede tolerar caídas de servicio durante las horas pico matutinas, pérdidas de inventario de lotes orgánicos ni inconsistencias transaccionales al registrar cobros mixtos (efectivo, tarjeta bancaria y transferencias SPEI). Asimismo, los requerimientos de seguridad estatutaria (conforme a la Ley Federal de Protección de Datos Personales en Posesión de los Particulares - LFPDPPP) y el compromiso con los Objetivos de Desarrollo Sostenible (ODS 12: Producción y Consumo Responsables) exigen procesos estandarizados, gobernanza sólida y acuerdos de nivel de servicio (SLAs) formalizados.
  </p>
  <p>
    El objetivo fundamental de esta actividad es realizar una investigación exhaustiva sobre los marcos de trabajo y estándares más representativos en la gestión de servicios informáticos (ITIL, ISO/IEC 20000, COBIT, CMMI y TOGAF), seleccionar los dos marcos más pertinentes para Monchis Café (ITIL v4 e ISO/IEC 20000-1:2018), efectuar un análisis comparativo crítico y diseñar una estrategia integral de servicios TI articulada en las cinco fases del ciclo de vida ITIL, integrando valor, procesos, roles específicos y herramientas tecnológicas que aseguren la calidad, resiliencia y mejora continua del servicio.
  </p>

  <h1>2. Investigación Preliminar de Marcos de Trabajo y Estándares</h1>
  <p>
    La gestión de servicios informáticos ha evolucionado mediante marcos de buenas prácticas y normas internacionales que proporcionan directrices probadas para planificar, entregar, operar y controlar servicios de tecnología:
  </p>

  <h2>2.1. ITIL (Information Technology Infrastructure Library)</h2>
  <p>
    Desarrollado originalmente en el Reino Unido por la Central Computer and Telecommunications Agency (CCTA) y gestionado actualmente por AXELOS, ITIL representa el marco de referencia de facto más adoptado a nivel mundial para ITSM (Steinberg, 2011; Cartlidge et al., 2012). Históricamente, ITIL v3 (2007/2011) introdujo el modelo de Ciclo de Vida del Servicio dividido en cinco fases interconectadas: Estrategia del Servicio (Service Strategy), Diseño del Servicio (Service Design), Transición del Servicio (Service Transition), Operación del Servicio (Service Operation) y Mejora Continua del Servicio (Continual Service Improvement - CSI). Con la publicación de ITIL 4 en 2019, el marco evolucionó hacia un modelo más ágil, flexible y holístico denominado Sistema de Valor del Servicio (SVS), el cual incorpora la Cadena de Valor del Servicio (Service Value Chain), cuatro dimensiones de gestión (Organizaciones y personas; Información y tecnología; Socios y proveedores; Flujos de valor y procesos) y 34 prácticas de gestión (AXELOS, 2019). ITIL no impone reglas rígidas, sino que opera bajo la premisa de "adoptar y adaptar" (adopt and adapt).
  </p>

  <h2>2.2. ISO/IEC 20000 (Norma Internacional de Gestión de Servicios de TI)</h2>
  <p>
    La norma ISO/IEC 20000, desarrollada conjuntamente por ISO e IEC, constituye el primer estándar internacional auditable y certificable formalmente para la gestión de servicios de tecnología (ISO/IEC, 2018). Su parte medular, la ISO/IEC 20000-1:2018 ("Service management system requirements"), establece los requisitos obligatorios para que un proveedor planifique, establezca, implemente, opere, monitoree, revise, mantenga y mejore un Sistema de Gestión de Servicios de TI (SGSTI / SMS). A diferencia de las guías descriptivas de ITIL, la norma ISO prescribe cláusulas normativas de cumplimiento estricto (cláusulas 4 a 10 bajo la estructura de alto nivel de ISO - High Level Structure), gobernadas por el ciclo de Deming: Planificar (Plan), Hacer (Do), Verificar (Check) y Actuar (Act) (Bon et al., 2020).
  </p>

  <h2>2.3. Otros Marcos Relevantes: COBIT 2019, CMMI-SVC y TOGAF</h2>
  <p>
    <b>• COBIT 2019 (Control Objectives for Information and Related Technologies):</b> Creado por ISACA (2018), es el marco líder para la Gobernanza y Gestión de la Información y la Tecnología de la Empresa (EGIT). Mientras ITIL e ISO 20000 se concentran en cómo entregar y gestionar los servicios, COBIT opera en el nivel directivo, alineando los objetivos corporativos con los de TI mediante 40 objetivos en cinco dominios: EDM, APO, BAI, DSS y MEA.<br>
    <b>• CMMI-SVC (Capability Maturity Model Integration for Services):</b> Desarrollado por el CMMI Institute (ISACA, 2020), evalúa y mejora la madurez y capacidad de los procesos de prestación de servicios a través de cinco niveles formales (Inicial, Gestionado, Definido, Gestionado Cuantitativamente y Optimizado). Es ampliamente utilizado en licitaciones que requieren certificación de procesos repetibles.<br>
    <b>• TOGAF (The Open Group Architecture Framework):</b> Marco de referencia de The Open Group (2022) enfocado en Arquitectura Empresarial. A través de su Método de Desarrollo de Arquitectura (ADM), proporciona una estructura para diseñar, planificar e implementar las arquitecturas de negocio, datos, aplicaciones y tecnología.
  </p>

  <!-- PÁGINA 4: DESCRIPCIÓN DETALLADA Y ANÁLISIS COMPARATIVO -->
  <div class="page-break"></div>
  <h1>3. Descripción Detallada de los Marcos Seleccionados</h1>
  <p>
    Para el proyecto Monchis Café se seleccionan ITIL (en su versión v4 y ciclo de vida de servicio) y la norma ISO/IEC 20000-1:2018. A continuación se analizan sus principios, objetivos y áreas clave de aplicación.
  </p>

  <h2>3.1. ITIL v4: Objetivos, Principios Guía y Áreas Clave</h2>
  <p>
    <b>Objetivo Fundamental:</b> Facilitar la co-creación de valor mediante la gestión integral de productos y servicios digitales, brindando un marco operativo ágil, centrado en el cliente y adaptable a entornos en la nube y arquitecturas modernas (AXELOS, 2019).<br>
    <b>Principios Guía Universales de ITIL v4:</b> (1) <i>Enfocarse en el valor:</i> Cada acción debe generar valor directo para los comensales y el negocio; (2) <i>Empezar donde se está:</i> Aprovechar la arquitectura existente en Vue 3 y Next.js; (3) <i>Progresar iterativamente con retroalimentación:</i> Validar con usuarios reales de barra; (4) <i>Colaborar y promover visibilidad:</i> Información compartida entre desarrollo y cafetería; (5) <i>Pensar y trabajar holísticamente:</i> Abarcar tecnología, personas y procesos; (6) <i>Mantenerlo simple y práctico:</i> Interfaces táctiles intuitivas sin burocracia; (7) <i>Optimizar y automatizar:</i> Despliegues automáticos con CI/CD y monitoreo proactivo.<br>
    <b>Áreas Clave:</b> Portafolio y catálogo de servicios, gestión de niveles de servicio (SLA/OLA), habilitación del cambio, incidentes, problemas y mejora continua.
  </p>

  <h2>3.2. ISO/IEC 20000-1:2018: Principios y Estructura Normativa</h2>
  <p>
    <b>Objetivo Fundamental:</b> Establecer, implementar, mantener y mejorar continuamente un Sistema de Gestión de Servicios (SGSTI) formal, demostrando que la organización cumple con estándares de calidad internacionales rigurosos (ISO/IEC, 2018).<br>
    <b>Principios y Estructura HLS:</b> Contexto y Liderazgo (Cl. 4 y 5: alcance y política de calidad); Planificación y Apoyo (Cl. 6 y 7: gestión de riesgos y provisión de recursos); Operación del Servicio (Cl. 8: SLAs, diseño, transición, resolución de incidentes, problemas, continuidad, disponibilidad y seguridad); Evaluación y Mejora (Cl. 9 y 10: métricas, auditorías y ciclo PDCA de Deming).
  </p>

  <h1>4. Análisis Comparativo entre ITIL e ISO/IEC 20000-1</h1>
  <p>
    Aunque ambos marcos coinciden en la entrega de valor al cliente, difieren en alcance, obligatoriedad y metodología operativa:
  </p>

  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 17%;">Dimensión Analítica</th>
        <th style="width: 27%;">ITIL v4 (AXELOS)</th>
        <th style="width: 27%;">ISO/IEC 20000-1:2018 (ISO/IEC)</th>
        <th style="width: 29%;">Impacto en Monchis Café</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="font-weight: bold; color: #1A365D;">Naturaleza y Propósito</td>
        <td>Marco de buenas prácticas descriptivas. Explica el "cómo" gestionar servicios de TI con agilidad y flexibilidad.</td>
        <td>Estándar internacional normativo y prescriptivo. Dictamina el "qué debe cumplir" formalmente un SGSTI auditable.</td>
        <td>ITIL guía el desarrollo técnico ágil (RabbitMQ, Vue 3); ISO 20000 garantiza el control riguroso de cambios y seguridad de datos.</td>
      </tr>
      <tr>
        <td style="font-weight: bold; color: #1A365D;">Certificación Formal</td>
        <td>Certificación para personas y profesionales (Fundamentos, Managing Professional). No certifica empresas.</td>
        <td>Certificación formal para organizaciones emitida por organismos acreditadores externos tras auditoría de conformidad.</td>
        <td>Permite a Ernesto Hatuey formarse en ITIL como arquitecto, mientras el diseño del software queda listo para certificación ISO 20000.</td>
      </tr>
      <tr>
        <td style="font-weight: bold; color: #1A365D;">Enfoque de Adopción</td>
        <td>Filosofía de "Adoptar y adaptar". Las organizaciones toman solo las prácticas que agregan valor y descartan lo superfluo.</td>
        <td>Cumplimiento obligatorio de todas las cláusulas normativas (cláusulas 4 a 10) para superar auditorías sin no conformidades.</td>
        <td>Evita burocracia: adaptamos ITIL a la escala de cafetería, pero adoptamos las cláusulas críticas de ISO 20000 en seguridad y continuidad.</td>
      </tr>
      <tr>
        <td style="font-weight: bold; color: #1A365D;">Ciclo de Vida y Valor</td>
        <td>Enfoque en Sistema de Valor del Servicio (SVS), 4 dimensiones y co-creación de valor entre proveedor y cliente.</td>
        <td>Enfoque estructurado por procesos alineado al ciclo Deming (PDCA: Planificar, Hacer, Verificar, Actuar) y mejora continua.</td>
        <td>Armonización perfecta: las fases del ciclo de vida ITIL definen el flujo operativo, mientras el PDCA asegura auditoría continua.</td>
      </tr>
      <tr>
        <td style="font-weight: bold; color: #1A365D;">Gestión de Cambios</td>
        <td>Habilitación del cambio (Change Enablement) con evaluación de riesgos basada en velocidad y valor, y comité ágil (CAB).</td>
        <td>Control formal de cambios, evaluación documental rigurosa de impacto y mitigación obligatoria de riesgos del servicio.</td>
        <td>Protege el POS en barra: ningún cambio se despliega sin pruebas automatizadas (CI/CD) ni plan de marcha atrás (rollback).</td>
      </tr>
      <tr>
        <td style="font-weight: bold; color: #1A365D;">Costo y Complejidad</td>
        <td>Bajo costo de adopción interna; altamente flexible y compatible con metodologías ágiles (Scrum, DevOps, Kanban).</td>
        <td>Requiere disciplina documental estricta y costos de auditoría externa si se busca la certificación oficial.</td>
        <td>Para Monchis Café, adoptamos las directrices ISO 20000 internamente como política de calidad sin incurrir en costos de certificación.</td>
      </tr>
    </tbody>
  </table>

  <h2>4.2. Sinergia Metodológica en el Contexto del Proyecto</h2>
  <p>
    La integración conjunta de ITIL v4 e ISO/IEC 20000-1 crea una potente sinergia técnica y de negocio. ITIL proporciona las mejores prácticas operativas y la flexibilidad ágil que un proyecto dinámico requiere, mientras que la norma ISO aporta la estructura formal de gobernanza, la gestión preventiva del riesgo y el aseguramiento sistemático de la calidad a través del ciclo PDCA. De este modo, Monchis Café evita tanto una implementación burocrática y rígida como una operación desordenada.
  </p>

  <!-- PÁGINA 5: ADAPTACIÓN Y CICLO DE VIDA ITIL -->
  <div class="page-break"></div>
  <h1>5. Adaptación de los Marcos al Proyecto Final: Monchis Café</h1>

  <h2>5.1. Justificación de Elección según Requisitos de Monchis Café</h2>
  <p>
    La selección de ITIL v4 e ISO/IEC 20000-1 se fundamenta directamente en las necesidades de Monchis Café:<br>
    <b>1. Requisitos Técnicos y de Negocio:</b> Frontend reactivo en Vue 3 para tabletas de barra, backend en Next.js, base de datos PostgreSQL con Prisma y broker RabbitMQ con patrón Saga para transacciones concurrentes. Requisitos de cobro multimodal en &lt;45 s, rotación PEPS de café orgánico y gamificación Monchis Rewards demandan alta disponibilidad (99.9%) y consistencia transaccional absoluta.<br>
    <b>2. Necesidades Operativas:</b> Cajeros y baristas requieren interfaces amigables y un canal de soporte técnico ágil (MTTR &lt; 60 min) para evitar que un fallo en terminal congele las ventas en horas pico matutinas.<br>
    <b>3. Beneficios Cuantificables:</b> Reducción del 85% en merma de café orgánico por alertas de caducidad, ahorro de más de $36,000 MXN anuales en licencias cerradas y protección de datos conforme a la ley LFPDPPP.
  </p>

  <h2>5.2. Estrategia de Servicios TI en las Fases del Ciclo de Vida ITIL</h2>
  <p>
    A continuación se adapta la estrategia integral de servicios TI articulada en las cinco fases del ciclo de vida ITIL e ISO 20000:
  </p>

  <h3>5.2.1. Estrategia del Servicio (Service Strategy)</h3>
  <p>
    <b>• Valor del Servicio:</b> Utilidad ('Fit for Purpose': acelerar el cobro a &lt;45 s, certificar café orgánico y bonificar $5.00 MXN por termo - ODS 12) y Garantía ('Fit for Use': disponibilidad 99.9%, seguridad stateless con JWT en cookies HttpOnly y resiliencia Saga en RabbitMQ).<br>
    <b>• Portafolio y Catálogo:</b> Servicios Principales (POS Táctil Omnicanal, Trazabilidad Orgánica PEPS, Monedero Digital Rewards), Habilitadores (RabbitMQ Saga, PostgreSQL transaccional, Seguridad JWT/2FA) y Soporte (Mesa de Ayuda N1/N2, Backups RTO&lt;1h, Monitoreo /api/health).
  </p>

  <h3>5.2.2. Diseño del Servicio (Service Design)</h3>
  <p>
    <b>• Acuerdos de Nivel de Servicio (SLAs):</b> SLA-POS-01 (Disponibilidad mensual &ge; 99.9%); SLA-POS-02 (Latencia P95 &le; 400 ms); SLA-INC-01 (Respuesta en barra &le; 15 min; resolución MTTR &le; 60 min).<br>
    <b>• Continuidad y Seguridad (ISO 20000 Cl. 8.7):</b> RPO &le; 15 min y RTO &le; 60 min con respaldos incrementales cifrados en la nube, encriptación TLS 1.3, reCAPTCHA v3 y control de acceso basado en roles (RBAC: Cajero, Barista, Administrador).
  </p>

  <h3>5.2.3. Transición del Servicio (Service Transition)</h3>
  <p>
    <b>• Habilitación del Cambio:</b> Clasificación en Cambios Estándar (preaprobados), Cambios Normales (pruebas en staging y aprobación) y Cambios de Emergencia (parches urgentes con comité de emergencia CAB).<br>
    <b>• Liberación y Configuración:</b> Pipeline CI/CD en GitHub Actions (validación de tipos, lint y Vitest), imágenes contenerizadas Docker multi-stage y monorepo estructurado con Turborepo.
  </p>

  <h3>5.2.4. Operación del Servicio (Service Operation)</h3>
  <p>
    <b>• Mesa de Ayuda (Service Desk):</b> Nivel 0 (Validaciones táctiles de autoservicio), Nivel 1 (Soporte en sitio por barista líder para impresoras térmicas y red) y Nivel 2 (Soporte especializado por Ernesto Hatuey para base de datos y RabbitMQ).<br>
    <b>• Problemas y Monitoreo:</b> Causa raíz inspeccionando la Dead Letter Queue (DLQ) de RabbitMQ y supervisión periódica del endpoint `/api/health`.
  </p>

  <h3>5.2.5. Mejora Continua del Servicio (Continual Service Improvement - CSI)</h3>
  <p>
    <b>• Ciclo Deming (PDCA) y 7 Pasos ITIL:</b> Planificar (definir métricas de cobro y merma), Hacer (recopilar datos con `correlation_id`), Verificar (evaluar SLAs en revisión directiva mensual) y Actuar (registrar iniciativas en el Registro de Mejora Continua - CIR).
  </p>

  <!-- PÁGINA 6: MATRIZ INTEGRADORA Y EJEMPLOS PRÁCTICOS -->
  <div class="page-break"></div>
  <h1>5.3. Matriz Integradora: Valor, Procesos, Roles y Herramientas</h1>
  <p>
    La siguiente matriz consolida la articulación de la estrategia cumpliendo con los cuatro elementos clave exigidos:
  </p>

  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 17%;">Fase ITIL / ISO</th>
        <th style="width: 23%;">Valor Generado para Monchis Café</th>
        <th style="width: 22%;">Procesos y Prácticas Clave</th>
        <th style="width: 19%;">Roles y Responsables</th>
        <th style="width: 19%;">Herramientas Tecnológicas</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="font-weight: bold; color: #1A365D;">Estrategia<br>(ISO Cl. 4 y 6)</td>
        <td>Alineación tecnológica con rentabilidad comercial, agilidad en barra y sustentabilidad ecológica (ODS 12).</td>
        <td>• Portafolio de Servicios<br>• Gestión Financiera TI<br>• Relaciones con Negocio<br>• Utilidad y Garantía</td>
        <td>• Líder TI (Ernesto Hatuey)<br>• Dueño / Gerencia General</td>
        <td>• Hoja CAPEX/OPEX<br>• Catálogo de Servicios<br>• Matriz ODS 12</td>
      </tr>
      <tr>
        <td style="font-weight: bold; color: #1A365D;">Diseño<br>(ISO Cl. 8.2 y 8.7)</td>
        <td>Disponibilidad 99.9%, cobro en caja &lt; 45 s y protección estricta de datos personales (LFPDPPP).</td>
        <td>• Niveles de Servicio (SLAs)<br>• Continuidad (RTO/RPO)<br>• Seguridad de la Info.<br>• Capacidad y Disponibilidad</td>
        <td>• Arquitecto de Software<br>• Ingeniero de Requerimientos</td>
        <td>• Prisma ORM & PostgreSQL<br>• JWT en cookies HttpOnly<br>• Google reCAPTCHA v3</td>
      </tr>
      <tr>
        <td style="font-weight: bold; color: #1A365D;">Transición<br>(ISO Cl. 8.5 y 8.6)</td>
        <td>Despliegues sin interrupción de ventas en mostrador, cero regresiones y compilación estandarizada.</td>
        <td>• Habilitación del Cambio<br>• Liberación (Release Mgmt)<br>• Gestión de Activos (SACM)<br>• Pruebas de Regresión</td>
        <td>• Desarrollador Full-Stack<br>• Comité de Cambios (CAB)<br>• Cajero líder (UAT)</td>
        <td>• GitHub Actions (CI/CD)<br>• Vitest (Pruebas unitarias)<br>• Docker multi-stage<br>• Turborepo monorepo</td>
      </tr>
      <tr>
        <td style="font-weight: bold; color: #1A365D;">Operación<br>(ISO Cl. 8.3 y 8.4)</td>
        <td>Resolución rápida de fallos en barra (MTTR &lt; 60 min), cuadres de caja exactos y flujo ininterrumpido.</td>
        <td>• Mesa de Ayuda (Service Desk)<br>• Gestión de Incidentes<br>• Gestión de Problemas (RCA)<br>• Eventos y Monitoreo</td>
        <td>• Operador N1 (Cajero/Barista)<br>• Soporte N2 (Ernesto Hatuey)<br>• Proveedor ISP de enlace</td>
        <td>• POS táctil en Vue 3<br>• RabbitMQ Topic Exchange<br>• Dead Letter Queue (DLQ)<br>• Endpoint /api/health</td>
      </tr>
      <tr>
        <td style="font-weight: bold; color: #1A365D;">Mejora Continua<br>(ISO Cl. 9 y 10)</td>
        <td>Optimización iterativa basada en métricas reales de ventas, reducción de mermas y retención Rewards.</td>
        <td>• Ciclo Deming PDCA<br>• 7 Pasos de Mejora ITIL<br>• Auditoría de Servicio<br>• Medición de CSFs y KPIs</td>
        <td>• Líder de Mejora Continua<br>• Gerente de Cafetería</td>
        <td>• Panel Analítico Next.js<br>• Registro de Mejora (CIR)<br>• Atribución UTM campañas</td>
      </tr>
    </tbody>
  </table>

  <h1>5.4. Ejemplos Específicos de Aplicación en Fases Clave</h1>
  <p>
    <b>• Gestión de Riesgos (Consistencia Transaccional con Saga):</b> En picos matutinos, dos clientes piden simultáneamente el último lote de café de Oaxaca. Para evitar cobros en descubierto, el orquestador Saga en RabbitMQ detecta el desabasto y ejecuta una compensación automática: cancela la preautorización bancaria y notifica a la pantalla táctil para ofrecer otra variedad sin descuadrar la caja.<br>
    <b>• Entrega de Servicios (Despliegue de Actualizaciones al POS):</b> Se actualiza el software de barra clasificándolo como "Cambio Normal". Pasa por el pipeline CI/CD de GitHub Actions y se despliega a las 22:30 hrs (fuera de horario comercial) mediante contenedores Docker con estrategia Zero-Downtime y procedimiento formal de marcha atrás (rollback &lt; 90 s).<br>
    <b>• Mejora Continua (Telemetría de Latencia):</b> Mediante análisis de logs con `correlation_id` y `/api/health`, se identificó que la consulta de trazabilidad demoraba 1,200 ms. Se añadió un índice compuesto en PostgreSQL (`numero_lote`, `fecha_caducidad`), reduciendo la latencia P95 a 65 ms, documentándose en la revisión directiva mensual.
  </p>

  <h2>5.5. Esquema Conceptual de la Estrategia de Servicios TI</h2>
  <div class="diagram-box">┌────────────────────────────────────────────────────────────────────────────────────────┐
│         ESTRATEGIA INTEGRAL DE SERVICIOS TI — "MONCHIS CAFÉ" (ITIL v4 + ISO 20000)     │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. ESTRATEGIA (Plan / Cl.6) │ 2. DISEÑO (Do / Cl. 8.2)   │ 3. TRANSICIÓN (Do / Cl. 8.5) │
│ • Utilidad: Cobro &lt; 45 s   │ • SLA: 99.9% Uptime, P95&lt;400│ • Habilitación del Cambio    │
│ • Garantía: Uptime, LFPDPPP│ • RTO &lt; 1h, RPO &lt; 15m      │ • CI/CD con GitHub Actions   │
│ • Catálogo: Core / Support │ • Seguridad: JWT + reCAPTCHA│ • Docker multi-stage + Vitest│
├────────────────────────────┴─────────────┬──────────────┴──────────────────────────────┤
│ 4. OPERACIÓN (Do / Cl. 8.3-8.4)          │ 5. MEJORA CONTINUA (Check/Act / Cl. 9-10)   │
│ • Mesa de Ayuda: Niveles N0 / N1 / N2    │ • Ciclo Deming PDCA + Registro CIR          │
│ • RabbitMQ + Patrón Saga (DLQ)           │ • Análisis mensual de KPIs y latencia P95   │
│ • POS Táctil Vue 3 + Telemetría /health  │ • Optimización de índices en PostgreSQL     │
└──────────────────────────────────────────┴─────────────────────────────────────────────┘</div>

  <!-- PÁGINA 7: CONCLUSIONES Y DESAFÍOS -->
  <div class="page-break"></div>
  <h1>6. Conclusiones y Desafíos de Adaptación</h1>
  <p>
    El desarrollo de esta actividad formativa permite consolidar una visión profesional y madura sobre el papel de las tecnologías de información en el ámbito empresarial contemporáneo. Diseñar una plataforma como Monchis Café no consiste meramente en concatenar componentes de frontend en Vue 3 o rutas API en Next.js; la verdadera viabilidad comercial y operativa de un sistema depende de su concepción como un servicio gestionado de extremo a extremo, donde la disponibilidad, la seguridad, la trazabilidad y la resolución de incidentes están formalmente pactadas, monitoreadas y protegidas bajo estándares reconocidos internacionalmente.
  </p>
  <p>
    La integración conjunta de ITIL v4 e ISO/IEC 20000-1:2018 demostró ser la combinación ideal para el proyecto. ITIL suministra el marco de referencia ágil, centrado en el cliente y enfocado en la co-creación de valor real, guiando las prácticas operativas diarias del punto de venta y la resiliencia transaccional con RabbitMQ Saga. Simultáneamente, la norma ISO aporta la disciplina de control, la gestión estructurada del riesgo y el compromiso irrenunciable con la mejora continua mediante el ciclo PDCA, dotando a Monchis Café de una arquitectura técnica lista para operar bajo auditorías rigurosas y con pleno cumplimiento de la ley de protección de datos personales.
  </p>
  <p>
    <b>Principales Desafíos Enfrentados en la Adaptación:</b><br><br>
    <b>1. Evitar la Sobrecarga Burocrática:</b> Uno de los riesgos inherentes al aplicar estándares corporativos como ISO 20000 a una pequeña empresa o proyecto individual es la tentación de generar documentación estéril o comités innecesarios. El desafío se superó aplicando el principio guía de ITIL "Mantenerlo simple y práctico" (Keep it simple and practical), automatizando el control de cambios y las pruebas mediante pipelines de CI/CD.<br><br>
    <b>2. Dimensión Humana y Capacitación Operativa:</b> El personal de barra (cajeros y baristas) tiene una rotación natural y no cuenta con formación informática. La estrategia TI resolvió esta brecha mediante un diseño de interfaz táctil guiado por prevención de errores, manuales de Nivel 0 intuitivos y un canal directo de soporte técnico N1/N2 con tiempos de respuesta bajo SLA garantizados.<br><br>
    <b>3. Disciplina en la Medición y Mejora:</b> La mejora continua exige recopilar datos objetivos en lugar de impresiones empíricas. Integrar trazabilidad estructurada de logs con identificadores únicos (`correlation_id`) y endpoints de salud representa un esfuerzo técnico adicional en la arquitectura, pero constituye el único medio para identificar cuellos de botella antes de que afecten la atención al público.
  </p>

  <!-- PÁGINA 8: REFERENCIAS (APA 7) -->
  <div class="page-break"></div>
  <h1>7. Referencias Bibliográficas</h1>
  <div style="margin-top: 15px;">
    <div class="ref-entry">AXELOS. (2019). <i>ITIL Foundation: ITIL 4 Edition</i>. The Stationery Office (TSO).</div>
    <div class="ref-entry">Bon, J. van, Pieper, M., & Veen, A. van der. (2020). <i>Foundations of IT Service Management with ISO/IEC 20000-1:2018</i>. Van Haren Publishing.</div>
    <div class="ref-entry">Cartlidge, A., Hanna, A., Rudd, C., Macfarlane, I., Windebank, J., & Rance, S. (2012). <i>An introductory overview of ITIL V3</i>. The UK Chapter of the itSMF.</div>
    <div class="ref-entry">International Organization for Standardization, & International Electrotechnical Commission. (2018). <i>Information technology — Service management — Part 1: Service management system requirements</i> (ISO/IEC Standard No. 20000-1:2018). ISO/IEC. https://www.iso.org/standard/70636.html</div>
    <div class="ref-entry">International Organization for Standardization, & International Electrotechnical Commission. (2019). <i>Information technology — Service management — Part 2: Guidance on the application of service management systems</i> (ISO/IEC Standard No. 20000-2:2019). ISO/IEC.</div>
    <div class="ref-entry">ISACA. (2018). <i>COBIT 2019 Framework: Introduction and methodology</i>. Information Systems Audit and Control Association.</div>
    <div class="ref-entry">ISACA. (2020). <i>CMMI for Services, Version 2.0</i>. CMMI Institute.</div>
    <div class="ref-entry">Steinberg, R. A. (2011). <i>ITIL Service Strategy (2011 edition)</i>. The Stationery Office (TSO).</div>
    <div class="ref-entry">The Open Group. (2022). <i>The TOGAF Standard, 10th Edition: Introduction and core concepts</i>. The Open Group.</div>
  </div>

</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML generado: {html_path}")

    # Compilación a PDF con Microsoft Edge Headless
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    ]
    browser_exe = None
    for p in edge_paths:
        if os.path.exists(p):
            browser_exe = p
            break

    if browser_exe:
        print(f"Compilando PDF usando: {browser_exe}...")
        cmd = [
            browser_exe,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            html_path
        ]
        subprocess.run(cmd, check=True)
        print(f"PDF generado: {pdf_path}")
        shutil.copyfile(pdf_path, download_pdf)
        print(f"PDF copiado a Descargas: {download_pdf}")

    # Generación de la versión Markdown (.md)
    md_content = f"""# ACTIVIDAD 3.6: INVESTIGACIÓN Y APLICACIÓN DE MARCOS DE TRABAJO Y ESTÁNDARES EN LA GESTIÓN DE SERVICIOS INFORMÁTICOS
## Módulo 2: Buenas Prácticas de Calidad en el Desarrollo de Software
### Cátedra: Proyecto Integrador de Desarrollo de Software / Gestión de Servicios TI

* **Docente:** Dr. Gabriel Navarro Salcedo  
* **Estudiante:** Ernesto Hatuey Fierro Meléndez (Código: 215487963)  
* **Proyecto Integrador:** Monchis Café — Plataforma Web Segura para Cafetería Orgánica y Comercial  
* **Institución:** Universidad de Guadalajara — Centro Universitario de Tonalá (CUTonalá)  
* **Fecha:** 26 de octubre de 2026 — **Ciclo:** 2026-B  

---

## ÍNDICE GENERAL
1. Introducción y Justificación de la Gestión de Servicios TI
2. Investigación Preliminar de Marcos de Trabajo y Estándares (ITIL, ISO/IEC 20000, COBIT, CMMI, TOGAF)
3. Descripción Detallada de los Marcos Seleccionados (ITIL v4 e ISO/IEC 20000-1:2018)
4. Análisis Comparativo entre ITIL e ISO/IEC 20000-1
5. Adaptación al Proyecto Final: Monchis Café (Fases del Ciclo de Vida ITIL, Valor, Procesos, Roles y Herramientas)
6. Conclusiones y Desafíos de Adaptación
7. Referencias Bibliográficas (Normas APA 7.ª edición)

---

*(Consulte los archivos oficiales compilados en formato Word `.docx` y `.pdf` en la carpeta `docs/entregables/` y en su directorio de Descargas).*
"""
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Markdown generado: {md_path}")

if __name__ == "__main__":
    build_deliverables()
