# -*- coding: utf-8 -*-
"""
Script de Sincronización Absoluta de Entregables (DOCX, HTML y PDF)
Garantiza paridad 1:1 entre el Markdown maestro, el archivo DOCX de Word y el PDF oficial.
"""

import os
import re
import subprocess
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

MD_PATH = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.md"
DOCX_PATH = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.docx"
HTML_PATH = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.html"
PDF_REPO = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.pdf"
PDF_DOWNLOADS = os.path.expanduser(r"~\Downloads\Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.pdf")

def read_markdown():
    with open(MD_PATH, "r", encoding="utf-8") as f:
        return f.read()

# -------------------------------------------------------------------------
# XML HELPERS PARA DOCX
# -------------------------------------------------------------------------
def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E0", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}>'
                        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:left w:val="none"/>'
                        f'<w:right w:val="none"/>'
                        f'</w:tblBorders>')
    tblPr.append(borders)

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:cantSplit'))

def make_row_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:tblHeader'))

def add_page_number_to_footer(section):
    p_footer = section.footer.paragraphs[0]
    p_footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_footer.text = ""
    run = p_footer.add_run("Página ")
    run.font.name = "Arial"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    fld1 = OxmlElement('w:fldChar')
    fld1.set(qn('w:fldCharType'), 'begin')
    t1 = OxmlElement('w:instrText')
    t1.set(qn('xml:space'), 'preserve')
    t1.text = "PAGE"
    fld2 = OxmlElement('w:fldChar')
    fld2.set(qn('w:fldCharType'), 'separate')
    fld3 = OxmlElement('w:fldChar')
    fld3.set(qn('w:fldCharType'), 'end')
    run._r.append(fld1)
    run._r.append(t1)
    run._r.append(fld2)
    run._r.append(fld3)

    run2 = p_footer.add_run(" de ")
    run2.font.name = "Arial"
    run2.font.size = Pt(9)
    run2.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    fld4 = OxmlElement('w:fldChar')
    fld4.set(qn('w:fldCharType'), 'begin')
    t2 = OxmlElement('w:instrText')
    t2.set(qn('xml:space'), 'preserve')
    t2.text = "NUMPAGES"
    fld5 = OxmlElement('w:fldChar')
    fld5.set(qn('w:fldCharType'), 'separate')
    fld6 = OxmlElement('w:fldChar')
    fld6.set(qn('w:fldCharType'), 'end')
    run2._r.append(fld4)
    run2._r.append(t2)
    run2._r.append(fld5)
    run2._r.append(fld6)

# -------------------------------------------------------------------------
# GENERACIÓN DE DOCX COMPLETO Y FORMATEADO
# -------------------------------------------------------------------------
def build_docx(md_text):
    doc = Document()
    
    # Configuración de márgenes a 2.54 cm (1 pulgada)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.different_first_page_header_footer = True
        add_page_number_to_footer(section)

    # Estilo base
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)
    style_normal.paragraph_format.line_spacing = 1.2
    style_normal.paragraph_format.space_after = Pt(6)

    # Separar líneas del Markdown
    lines = md_text.split("\n")
    i = 0
    n = len(lines)

    # 1. PORTADA INSTITUCIONAL
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(36)
    p_inst.paragraph_format.space_after = Pt(4)
    run = p_inst.add_run("UNIVERSIDAD DE GUADALAJARA\n")
    run.bold = True
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    
    run = p_inst.add_run("CENTRO UNIVERSITARIO DE TONALÁ (CUTonalá)\n")
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0x2B, 0x4C, 0x7E)
    
    run = p_inst.add_run("DIVISIÓN DE INGENIERÍAS E INNOVACIÓN TECNOLÓGICA\nLICENCIATURA EN INGENIERÍA EN COMPUTACIÓN")
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(48)
    p_title.paragraph_format.space_after = Pt(12)
    run = p_title.add_run("ACTIVIDAD PARTICIPACIÓN:\nDISEÑO DE ESTRATEGIA DE SERVICIOS TI\n")
    run.bold = True
    run.font.size = Pt(15)
    run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    
    run = p_title.add_run("Proyecto Final: Monchis Café — Plataforma Web y Sistema de Gestión para Cafetería de Especialidad\n")
    run.italic = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
    
    run = p_title.add_run("Cátedra: Gestión de Servicios Informáticos")
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0x2B, 0x4C, 0x7E)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(72)
    p_meta.paragraph_format.space_after = Pt(0)
    p_meta.paragraph_format.line_spacing = 1.3
    
    meta_text = (
        "Docente: Dr. Gabriel Navarro Salcedo\n"
        "Estudiante: Ernesto Hatuey Fierro Medina (Código: 215487963)\n"
        "Rol: Desarrollador y Gestor de Servicios TI\n"
        "Fecha de Entrega: 17 de octubre de 2026\n"
        "Ciclo Escolar: 2026-B"
    )
    run = p_meta.add_run(meta_text)
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)

    doc.add_page_break()

    # Avanzar más allá del encabezado del markdown
    while i < n and not lines[i].startswith("# ÍNDICE GENERAL"):
        i += 1

    in_references = False

    while i < n:
        line = lines[i].rstrip()

        # Página nueva ante divisiones temáticas mayores
        if line == "---":
            i += 1
            continue

        # Encabezado 1 (# ...)
        if line.startswith("# "):
            h_text = line[2:].strip()
            if "UNIVERSIDAD" in h_text or "ACTIVIDAD" in h_text:
                i += 1
                continue
            
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(h_text)
            run.bold = True
            run.font.size = Pt(13.5)
            run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

            if "5. REFERENCIAS" in h_text:
                in_references = True
            i += 1
            continue

        # Encabezado 2 (## ...)
        if line.startswith("## "):
            h_text = line[3:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(h_text)
            run.bold = True
            run.font.size = Pt(12)
            run.font.color.rgb = RGBColor(0x2B, 0x4C, 0x7E)
            i += 1
            continue

        # Encabezado 3 (### ...)
        if line.startswith("### "):
            h_text = line[4:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(h_text)
            run.bold = True
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(0x31, 0x82, 0xCE)
            i += 1
            continue

        # Tablas Markdown
        if line.startswith("|"):
            table_lines = []
            while i < n and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            
            if len(table_lines) >= 3:
                # Parsear encabezados y filas
                header_cells = [c.strip() for c in table_lines[0].split("|")[1:-1]]
                data_rows = []
                for tl in table_lines[2:]:
                    cells = [c.strip() for c in tl.split("|")[1:-1]]
                    if cells:
                        data_rows.append(cells)
                
                table = doc.add_table(rows=len(data_rows) + 1, cols=len(header_cells))
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                set_table_borders(table)

                # Encabezado
                hdr_row = table.rows[0]
                make_row_cant_split(hdr_row)
                make_row_header(hdr_row)
                for c_idx, title in enumerate(header_cells):
                    cell = hdr_row.cells[c_idx]
                    set_cell_background(cell, "1A365D")
                    set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
                    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                    p = cell.paragraphs[0]
                    p.paragraph_format.space_after = Pt(0)
                    p.paragraph_format.line_spacing = 1.05
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run = p.add_run(title)
                    run.bold = True
                    run.font.size = Pt(9.5)
                    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

                # Filas de datos
                for r_idx, row_data in enumerate(data_rows):
                    row = table.rows[r_idx + 1]
                    make_row_cant_split(row)
                    bg_color = "F8FAFC" if (r_idx % 2 == 1) else "FFFFFF"
                    for c_idx in range(len(header_cells)):
                        cell = row.cells[c_idx]
                        if c_idx < len(row_data):
                            val = row_data[c_idx]
                        else:
                            val = ""
                        set_cell_background(cell, bg_color)
                        set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
                        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                        p = cell.paragraphs[0]
                        p.paragraph_format.space_after = Pt(0)
                        p.paragraph_format.line_spacing = 1.1
                        
                        # Alineación inteligente
                        if any(term in header_cells[c_idx].lower() for term in ["tipo", "impacto", "urgencia", "viabilidad", "riesgo", "prioridad", "total", "nivel"]):
                            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        else:
                            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                        
                        # Limpieza y formateo de negritas
                        run = p.add_run(val.replace("**", ""))
                        if "**" in val or c_idx == 0:
                            run.bold = True if c_idx == 0 or "**" in val else False
                        run.font.size = Pt(9)
                        run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)

                p_space = doc.add_paragraph()
                p_space.paragraph_format.space_after = Pt(4)
            continue

        # Listas con viñeta (* o -)
        if line.startswith("* ") or line.startswith("- "):
            item_text = line[2:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            
            if in_references:
                # Formato APA 7 con sangría francesa
                p.paragraph_format.left_indent = Inches(0.5)
                p.paragraph_format.first_line_indent = Inches(-0.5)
                run = p.add_run(item_text)
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
            else:
                run_bullet = p.add_run("• ")
                run_bullet.bold = True
                run_bullet.font.color.rgb = RGBColor(0x2B, 0x4C, 0x7E)
                run = p.add_run(item_text)
                run.font.size = Pt(10.5)
            i += 1
            continue

        # Listas numeradas (1. , 2. )
        m_num = re.match(r"^(\d+)\.\s+(.*)$", line)
        if m_num:
            num = m_num.group(1)
            item_text = m_num.group(2)
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.35)
            p.paragraph_format.first_line_indent = Inches(-0.25)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.18
            run_num = p.add_run(f"{num}. ")
            run_num.bold = True
            run_num.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
            run = p.add_run(item_text)
            run.font.size = Pt(10.5)
            i += 1
            continue

        # Párrafos regulares
        if line.strip():
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.2
            
            # Formatear cursivas iniciales como *Criterios de selección:*
            run = p.add_run(line.strip())
            run.font.size = Pt(10.5)
            run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
            i += 1
            continue

        i += 1

    doc.save(DOCX_PATH)
    print(f"[OK] DOCX generado exitosamente en: {DOCX_PATH}")

# -------------------------------------------------------------------------
# GENERACIÓN DE HTML Y PDF COMPLETO Y FORMATEADO
# -------------------------------------------------------------------------
def build_html_and_pdf(md_text):
    # Parsear Markdown a HTML semántico completo
    lines = md_text.split("\n")
    html_parts = []
    
    html_header = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Actividad Participación - Diseño de Estrategia de Servicios TI</title>
<style>
  @page {
    size: letter;
    margin: 2.54cm;
    @bottom-right {
      content: "Página " counter(page) " de " counter(pages);
      font-family: Arial, sans-serif;
      font-size: 9pt;
      color: #718096;
    }
  }
  body {
    font-family: Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.35;
    color: #1A202C;
    margin: 0;
    padding: 0;
  }
  .portada {
    text-align: center;
    page-break-after: always;
    padding-top: 2.5cm;
  }
  .portada .inst-main {
    font-size: 14pt;
    font-weight: bold;
    color: #1A365D;
    margin-bottom: 4px;
  }
  .portada .inst-sub {
    font-size: 12pt;
    font-weight: bold;
    color: #2B4C7E;
    margin-bottom: 4px;
  }
  .portada .inst-div {
    font-size: 10pt;
    color: #4A5568;
    margin-bottom: 2cm;
  }
  .portada h1 {
    font-size: 16pt;
    font-weight: bold;
    color: #1A365D;
    line-height: 1.3;
    margin-bottom: 12px;
  }
  .portada .subtitulo {
    font-size: 11pt;
    font-style: italic;
    color: #4A5568;
    margin-bottom: 8px;
  }
  .portada .catedra {
    font-size: 11pt;
    font-weight: bold;
    color: #2B4C7E;
    margin-bottom: 2.5cm;
  }
  .portada .meta {
    font-size: 10.5pt;
    line-height: 1.6;
    color: #2D3748;
  }
  .page-break {
    page-break-after: always;
  }
  h1 {
    font-size: 13.5pt;
    color: #1A365D;
    border-bottom: 1.5px solid #E2E8F0;
    padding-bottom: 4px;
    margin-top: 22px;
    margin-bottom: 10px;
    page-break-after: avoid;
  }
  h2 {
    font-size: 12pt;
    color: #2B4C7E;
    margin-top: 18px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }
  h3 {
    font-size: 11pt;
    color: #3182CE;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }
  p {
    margin-top: 0;
    margin-bottom: 8px;
    text-align: justify;
  }
  ul {
    margin-top: 4px;
    margin-bottom: 10px;
    padding-left: 20px;
  }
  li {
    margin-bottom: 4px;
  }
  ol {
    margin-top: 4px;
    margin-bottom: 10px;
    padding-left: 22px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    margin-bottom: 14px;
    font-size: 9pt;
    page-break-inside: avoid;
  }
  th {
    background-color: #1A365D;
    color: #FFFFFF;
    font-weight: bold;
    padding: 8px 6px;
    border: 1px solid #CBD5E0;
    text-align: center;
  }
  td {
    padding: 6px 8px;
    border: 1px solid #CBD5E0;
    vertical-align: middle;
  }
  tr:nth-child(even) td {
    background-color: #F8FAFC;
  }
  .referencias p {
    padding-left: 2em;
    text-indent: -2em;
    font-size: 9.5pt;
    margin-bottom: 8px;
    text-align: left;
  }
  .formula-box {
    background-color: #F7FAFC;
    border-left: 3px solid #3182CE;
    padding: 6px 12px;
    margin: 8px 0;
    font-size: 9.5pt;
    color: #2D3748;
  }
</style>
</head>
<body>
"""
    html_parts.append(html_header)

    # PORTADA
    portada_html = """
<div class="portada">
  <div class="inst-main">UNIVERSIDAD DE GUADALAJARA</div>
  <div class="inst-sub">CENTRO UNIVERSITARIO DE TONALÁ (CUTonalá)</div>
  <div class="inst-div">DIVISIÓN DE INGENIERÍAS E INNOVACIÓN TECNOLÓGICA<br>LICENCIATURA EN INGENIERÍA EN COMPUTACIÓN</div>
  
  <h1>ACTIVIDAD PARTICIPACIÓN:<br>DISEÑO DE ESTRATEGIA DE SERVICIOS TI</h1>
  <div class="subtitulo">Proyecto Final: Monchis Café — Plataforma Web y Sistema de Gestión para Cafetería de Especialidad</div>
  <div class="catedra">Cátedra: Gestión de Servicios Informáticos</div>
  
  <div class="meta">
    <strong>Docente:</strong> Dr. Gabriel Navarro Salcedo<br>
    <strong>Estudiante:</strong> Ernesto Hatuey Fierro Medina (Código: 215487963)<br>
    <strong>Rol:</strong> Desarrollador y Gestor de Servicios TI<br>
    <strong>Fecha de Entrega:</strong> 17 de octubre de 2026<br>
    <strong>Ciclo Escolar:</strong> 2026-B
  </div>
</div>
"""
    html_parts.append(portada_html)

    i = 0
    n = len(lines)
    while i < n and not lines[i].startswith("# ÍNDICE GENERAL"):
        i += 1

    in_ref_section = False

    while i < n:
        line = lines[i].rstrip()

        if line == "---":
            i += 1
            continue

        if line.startswith("# "):
            h_text = line[2:].strip()
            if "UNIVERSIDAD" in h_text or "ACTIVIDAD" in h_text:
                i += 1
                continue
            if in_ref_section:
                html_parts.append("</div>\n")
                in_ref_section = False
            html_parts.append(f"<h1>{h_text}</h1>\n")
            if "5. REFERENCIAS" in h_text:
                in_ref_section = True
                html_parts.append('<div class="referencias">\n')
            i += 1
            continue

        if line.startswith("## "):
            h_text = line[3:].strip()
            html_parts.append(f"<h2>{h_text}</h2>\n")
            i += 1
            continue

        if line.startswith("### "):
            h_text = line[4:].strip()
            html_parts.append(f"<h3>{h_text}</h3>\n")
            i += 1
            continue

        if line.startswith("|"):
            table_lines = []
            while i < n and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            if len(table_lines) >= 3:
                header_cells = [c.strip() for c in table_lines[0].split("|")[1:-1]]
                html_parts.append("<table>\n<thead>\n<tr>\n")
                for h in header_cells:
                    html_parts.append(f"  <th>{h}</th>\n")
                html_parts.append("</tr>\n</thead>\n<tbody>\n")
                for tl in table_lines[2:]:
                    cells = [c.strip() for c in tl.split("|")[1:-1]]
                    html_parts.append("<tr>\n")
                    for c_idx, val in enumerate(cells):
                        # Centrado inteligente
                        align_cls = ' style="text-align: center;"' if any(term in header_cells[c_idx].lower() for term in ["tipo", "impacto", "urgencia", "viabilidad", "riesgo", "prioridad", "total", "nivel"]) else ""
                        formatted_val = val.replace("**", "<strong>").replace("<strong>", "<strong>", 1)
                        # Reemplazo de markdown negrita
                        formatted_val = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', val)
                        html_parts.append(f"  <td{align_cls}>{formatted_val}</td>\n")
                    html_parts.append("</tr>\n")
                html_parts.append("</tbody>\n</table>\n")
            continue

        if line.startswith("* ") or line.startswith("- "):
            item_text = line[2:].strip()
            item_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item_text)
            if in_ref_section:
                html_parts.append(f"<p>{item_html}</p>\n")
            else:
                html_parts.append(f"<ul><li>{item_html}</li></ul>\n")
            i += 1
            continue

        m_num = re.match(r"^(\d+)\.\s+(.*)$", line)
        if m_num:
            num = m_num.group(1)
            item_text = m_num.group(2)
            item_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item_text)
            html_parts.append(f"<p style=\"margin-left: 20px; text-indent: -20px;\"><strong>{num}.</strong> {item_html}</p>\n")
            i += 1
            continue

        if line.strip():
            p_text = line.strip()
            p_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', p_text)
            p_html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', p_html)
            html_parts.append(f"<p>{p_html}</p>\n")
            i += 1
            continue

        i += 1

    if in_ref_section:
        html_parts.append("</div>\n")

    html_parts.append("</body>\n</html>")

    full_html = "".join(html_parts)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"[OK] HTML generado exitosamente en: {HTML_PATH}")

    # Compilación a PDF mediante Chrome Headless
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\erfierro\AppData\Local\Google\Chrome\Application\chrome.exe"
    ]
    chrome_bin = None
    for cp in chrome_paths:
        if os.path.exists(cp):
            chrome_bin = cp
            break
            
    if chrome_bin:
        cmd = [
            chrome_bin,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={PDF_REPO}",
            HTML_PATH
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[OK] PDF generado exitosamente en: {PDF_REPO}")
            shutil.copy2(PDF_REPO, PDF_DOWNLOADS)
            print(f"[OK] Copia colocada en carpeta Descargas: {PDF_DOWNLOADS}")
        else:
            print(f"[ERROR] Error al compilar PDF con Chrome: {res.stderr}")
    else:
        print("[ADVERTENCIA] No se encontro el ejecutable de Chrome para generar el PDF.")

if __name__ == "__main__":
    print("Iniciando sincronizacion absoluta de entregables...")
    md_content = read_markdown()
    build_docx(md_content)
    build_html_and_pdf(md_content)
    print("Sincronizacion completada con exito.")
