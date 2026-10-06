import os
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_cocomo_intermediate_excel():
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Styles
    navy_dark = "1B365D"
    teal = "008080"
    blue_header = "2C3E50"
    soft_blue = "EBF3FA"
    light_green = "F0FDF4"
    light_yellow = "FEF9C3"
    gray_light = "F8FAFC"
    border_color = "CBD5E1"

    font_title = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    font_sub = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_sec = Font(name="Calibri", size=12, bold=True, color="1B365D")
    font_bold = Font(name="Calibri", size=10, bold=True, color="0F172A")
    font_regular = Font(name="Calibri", size=10, color="1E293B")
    font_italic = Font(name="Calibri", size=9, italic=True, color="64748B")
    font_result = Font(name="Calibri", size=11, bold=True, color="166534")

    fill_navy = PatternFill(start_color=navy_dark, end_color=navy_dark, fill_type="solid")
    fill_teal = PatternFill(start_color=teal, end_color=teal, fill_type="solid")
    fill_blue_head = PatternFill(start_color=blue_header, end_color=blue_header, fill_type="solid")
    fill_soft_blue = PatternFill(start_color=soft_blue, end_color=soft_blue, fill_type="solid")
    fill_result = PatternFill(start_color=light_green, end_color=light_green, fill_type="solid")
    fill_zebra = PatternFill(start_color=gray_light, end_color=gray_light, fill_type="solid")
    fill_yellow = PatternFill(start_color=light_yellow, end_color=light_yellow, fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color=border_color),
        right=Side(style='thin', color=border_color),
        top=Side(style='thin', color=border_color),
        bottom=Side(style='thin', color=border_color)
    )
    result_border = Border(
        left=Side(style='thin', color="16A34A"),
        right=Side(style='thin', color="16A34A"),
        top=Side(style='thin', color="16A34A"),
        bottom=Side(style='double', color="16A34A")
    )

    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    # -------------------------------------------------------------------------
    # HOJA 1: RESUMEN Y MODELO DINÁMICO DE LOS 5 PROBLEMAS
    # -------------------------------------------------------------------------
    ws_main = wb.create_sheet(title="Resolución_Problemas")
    ws_main.views.sheetView[0].showGridLines = True

    # Banner
    ws_main.merge_cells("A1:K1")
    ws_main["A1"] = "ACTIVIDAD 2.2: PROBLEMAS COCOMO INTERMEDIO — HOJA AUTOMATIZADA"
    ws_main["A1"].font = font_title
    ws_main["A1"].fill = fill_navy
    ws_main["A1"].alignment = align_center
    ws_main.row_dimensions[1].height = 36

    ws_main.merge_cells("A2:K2")
    ws_main["A2"] = "Materia: Administración de Proyectos de Software · Docente: Dr. Gabriel Navarro Salcedo · Estudiante: Ernesto Fierro"
    ws_main["A2"].font = Font(name="Calibri", size=10, bold=True, color="E2E8F0")
    ws_main["A2"].fill = fill_blue_head
    ws_main["A2"].alignment = align_center
    ws_main.row_dimensions[2].height = 20

    # TABLA RESUMEN GENERAL (FILAS 4 A 11)
    ws_main["A4"] = "MATRIZ GENERAL DE RESULTADOS DE LOS PROBLEMAS I AL V"
    ws_main["A4"].font = font_sec
    ws_main.merge_cells("A4:K4")

    headers_summary = [
        "Problema", "Modo de Desarrollo", "Tamaño (KLOC)", "Coef. A", "Exp. B",
        "PM Nominal", "Factor EAF", "PM Ajustado", "TDEV (Meses)", "Costo / PM", "Costo Total (MXN)"
    ]

    for col_idx, text in enumerate(headers_summary, start=1):
        cell = ws_main.cell(row=5, column=col_idx, value=text)
        cell.font = Font(name="Calibri", size=9.5, bold=True, color="FFFFFF")
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = thin_border
    ws_main.row_dimensions[5].height = 26

    # Data rows for summary table linking to detailed sections below
    # Row 6: Problema I (detailed in row 15)
    # Row 7: Problema II (detailed in row 24)
    # Row 8: Problema III (detailed in row 34)
    # Row 9: Problema IV (detailed in row 44)
    # Row 10: Problema V (detailed in row 55)
    
    problems_summary_links = [
        ("Problema I (Ejemplo)", "=A15", "=B15", "=C15", "=D15", "=E15", "=G15", "=H15", "=I15", "=J15", "=K15"),
        ("Problema II", "=A24", "=B24", "=C24", "=D24", "=E24", "=G24", "=H24", "=I24", "=J24", "=K24"),
        ("Problema III", "=A33", "=B33", "=C33", "=D33", "=E33", "=G33", "=H33", "=I33", "=J33", "=K33"),
        ("Problema IV", "=A42", "=B42", "=C42", "=D42", "=E42", "=G42", "=H42", "=I42", "=J42", "=K42"),
        ("Problema V", "=A51", "=B51", "=C51", "=D51", "=E51", "=G51", "=H51", "=I51", "=J51", "=K51"),
    ]

    for r_idx, r_data in enumerate(problems_summary_links, start=6):
        fill_curr = fill_soft_blue if r_idx % 2 == 0 else fill_zebra
        for c_idx, val in enumerate(r_data, start=1):
            cell = ws_main.cell(row=r_idx, column=c_idx, value=val)
            cell.font = font_bold if c_idx in [1, 8, 9, 11] else font_regular
            cell.fill = fill_curr
            cell.border = thin_border
            if c_idx == 1:
                cell.alignment = align_left
            elif c_idx in [2]:
                cell.alignment = align_center
            elif c_idx in [3, 4, 5]:
                cell.alignment = align_right
                cell.number_format = "0.00"
            elif c_idx in [6, 7, 8, 9]:
                cell.alignment = align_right
                cell.number_format = "#,##0.00"
            elif c_idx in [10, 11]:
                cell.alignment = align_right
                cell.number_format = "$#,##0.00"
        ws_main.row_dimensions[r_idx].height = 20

    # -------------------------------------------------------------------------
    # DESGLOSE INDIVIDUAL DE PROBLEMAS CON CELDAS Y FÓRMULAS VINCULADAS
    # -------------------------------------------------------------------------
    
    def create_problem_block(start_row, prob_title, prob_desc, mode, kloc, drivers_list, cost_per_pm=None, req_time=False, req_cost=False):
        # Header block
        ws_main.merge_cells(start_row=start_row, start_column=1, end_row=start_row, end_column=11)
        ws_main.cell(row=start_row, column=1, value=f"{prob_title}: {prob_desc}").font = font_sec
        ws_main.row_dimensions[start_row].height = 22

        # Subheaders row
        h_row = start_row + 1
        headers_block = ["Modo", "KLOC", "Coef A", "Exp B", "PM Nominal", "Factores EAF Evaluados", "Cálculo EAF", "PM Ajustado", "TDEV (Meses)", "Costo / PM", "Costo Total"]
        for c_idx, h_text in enumerate(headers_block, start=1):
            c = ws_main.cell(row=h_row, column=c_idx, value=h_text)
            c.font = Font(name="Calibri", size=9, bold=True, color="FFFFFF")
            c.fill = fill_teal
            c.alignment = align_center
            c.border = thin_border
        ws_main.row_dimensions[h_row].height = 22

        # Calculation row
        calc_row = start_row + 2
        # Col A: Modo
        ws_main.cell(row=calc_row, column=1, value=mode).alignment = align_center
        # Col B: KLOC
        ws_main.cell(row=calc_row, column=2, value=kloc).number_format = "0.00"
        # Col C: Coef A (Linked to Coeficientes sheet)
        if mode == "Orgánico":
            ws_main.cell(row=calc_row, column=3, value="=Coeficientes!B6").number_format = "0.00"
            ws_main.cell(row=calc_row, column=4, value="=Coeficientes!C6").number_format = "0.00"
        elif mode == "Semiacoplado":
            ws_main.cell(row=calc_row, column=3, value="=Coeficientes!B7").number_format = "0.00"
            ws_main.cell(row=calc_row, column=4, value="=Coeficientes!C7").number_format = "0.00"
        else: # Empotrado / Embebido
            ws_main.cell(row=calc_row, column=3, value="=Coeficientes!B8").number_format = "0.00"
            ws_main.cell(row=calc_row, column=4, value="=Coeficientes!C8").number_format = "0.00"

        # Col E: PM Nominal formula = C * (B ^ D)
        ws_main.cell(row=calc_row, column=5, value=f"=C{calc_row}*POTENCIA(B{calc_row}, D{calc_row})").number_format = "#,##0.00"
        
        # Col F: Drivers description string
        drivers_str = " · ".join([f"{d[0]}({d[1]})={d[2]}" for d in drivers_list])
        ws_main.cell(row=calc_row, column=6, value=drivers_str).alignment = align_left

        # Col G: EAF formula = PRODUCT(...)
        mult_str = "*".join([str(d[2]) for d in drivers_list])
        ws_main.cell(row=calc_row, column=7, value=f"={mult_str}").number_format = "0.0000"

        # Col H: PM Ajustado formula = E * G
        ws_main.cell(row=calc_row, column=8, value=f"=E{calc_row}*G{calc_row}").number_format = "#,##0.00"

        # Col I: TDEV formula = Coef_C * (PM_adj ^ Coef_D)
        if mode == "Orgánico":
            ws_main.cell(row=calc_row, column=9, value=f"=Coeficientes!D6*POTENCIA(H{calc_row}, Coeficientes!E6)").number_format = "#,##0.00"
        elif mode == "Semiacoplado":
            ws_main.cell(row=calc_row, column=9, value=f"=Coeficientes!D7*POTENCIA(H{calc_row}, Coeficientes!E7)").number_format = "#,##0.00"
        else:
            ws_main.cell(row=calc_row, column=9, value=f"=Coeficientes!D8*POTENCIA(H{calc_row}, Coeficientes!E8)").number_format = "#,##0.00"

        # Col J: Cost per PM
        if cost_per_pm:
            ws_main.cell(row=calc_row, column=10, value=cost_per_pm).number_format = "$#,##0.00"
            # Col K: Total cost = PM_adj * Cost_per_PM
            ws_main.cell(row=calc_row, column=11, value=f"=H{calc_row}*J{calc_row}").number_format = "$#,##0.00"
        else:
            ws_main.cell(row=calc_row, column=10, value="-").alignment = align_center
            ws_main.cell(row=calc_row, column=11, value="-").alignment = align_center

        for col_idx in range(1, 12):
            c = ws_main.cell(row=calc_row, column=col_idx)
            c.font = font_bold if col_idx in [8, 9, 11] else font_regular
            c.border = result_border if col_idx in [8, 9, 11] else thin_border
            if col_idx in [8, 9, 11]:
                c.fill = fill_result
            else:
                c.fill = fill_zebra
        ws_main.row_dimensions[calc_row].height = 24

        # Add interpretation row
        interp_row = calc_row + 1
        ws_main.merge_cells(start_row=interp_row, start_column=1, end_row=interp_row, end_column=11)
        interp_cell = ws_main.cell(row=interp_row, column=1)
        if req_cost and req_time:
            interp_cell.value = f"→ RESPUESTA TÉCNICA: Se requiere un esfuerzo ajustado de {prob_title}, con un tiempo estimado de desarrollo de TDEV meses y una inversión total de honorarios de COSTO MXN."
        elif req_time:
            interp_cell.value = f"→ RESPUESTA TÉCNICA: El proyecto requiere un esfuerzo ajustado de {prob_title}, con una duración estimada de desarrollo (TDEV) de meses para su conclusión."
        elif req_cost:
            interp_cell.value = f"→ RESPUESTA TÉCNICA: El proyecto requiere un esfuerzo ajustado de {prob_title}, lo que representa un costo económico total estimado de COSTO MXN."
        else:
            interp_cell.value = f"→ RESPUESTA TÉCNICA: El esfuerzo total necesario para completar el proyecto es de aproximadamente PM_adj persona-mes."
        interp_cell.font = font_italic
        interp_cell.fill = fill_yellow
        interp_cell.alignment = align_left
        interp_cell.border = thin_border
        ws_main.row_dimensions[interp_row].height = 20

    # 1. PROBLEMA I
    create_problem_block(
        start_row=13,
        prob_title="PROBLEMA I (Ejemplo Resuelto de Clase)",
        prob_desc="Proyecto Semiacoplado de 50 KLOC con variables RELY(4), DATA(3), SCED(3)",
        mode="Semiacoplado",
        kloc=50.0,
        drivers_list=[("RELY", 4, 1.15), ("DATA", 3, 1.00), ("SCED", 3, 1.00)],
        cost_per_pm=None,
        req_time=False,
        req_cost=False
    )
    ws_main.cell(row=16, column=1, value="→ RESPUESTA TÉCNICA: Con un tamaño de 50 KLOC y EAF de 1.15, se requiere un esfuerzo ajustado de 275.85 persona-mes (aprox. 276 PM), idéntico al resultado oficial de la diapositiva 6.").font = font_italic

    # 2. PROBLEMA II
    create_problem_block(
        start_row=22,
        prob_title="PROBLEMA II",
        prob_desc="Proyecto Semiacoplado de 100 KLOC con variables RELY(5), DATA(4), CPLX(3), TIME(4), VIRT(2)",
        mode="Semiacoplado",
        kloc=100.0,
        drivers_list=[("RELY", 5, 1.40), ("DATA", 4, 1.08), ("CPLX", 3, 1.00), ("TIME", 4, 1.11), ("VIRT", 2, 0.87)],
        cost_per_pm=None,
        req_time=False,
        req_cost=False
    )
    ws_main.cell(row=25, column=1, value="→ RESPUESTA TÉCNICA: Para 100 KLOC en modo Semiacoplado con EAF = 1.4601, se requiere un esfuerzo ajustado de 761.23 persona-mes (aprox. 761 PM).").font = font_italic

    # 3. PROBLEMA III
    create_problem_block(
        start_row=31,
        prob_title="PROBLEMA III",
        prob_desc="Proyecto Empotrado de 300 KLOC. Se solicita TIEMPO DE DESARROLLO (TDEV)",
        mode="Empotrado",
        kloc=300.0,
        drivers_list=[("RELY", 4, 1.15), ("DATA", 5, 1.16), ("CPLX", 2, 0.85), ("ACAP", 1, 1.46), ("VIRT", 3, 1.00)],
        cost_per_pm=None,
        req_time=True,
        req_cost=False
    )
    ws_main.cell(row=34, column=1, value="→ RESPUESTA TÉCNICA: Con 300 KLOC en modo Empotrado (EAF = 1.6555 y PM ajustado = 4,351.42 PM), el tiempo estimado de desarrollo TDEV = 2.5*(4351.42)^0.32 es de 36.50 meses (aprox. 3 años).").font = font_italic

    # 4. PROBLEMA IV
    create_problem_block(
        start_row=40,
        prob_title="PROBLEMA IV",
        prob_desc="Proyecto Orgánico de 20 KLOC con costo de $10,000 MXN/PM. Se solicita COSTO TOTAL",
        mode="Orgánico",
        kloc=20.0,
        drivers_list=[("RELY", 1, 0.75), ("DATA", 5, 1.16), ("CPLX", 2, 0.85), ("TIME", 4, 1.11), ("ACAP", 1, 1.46), ("VIRT", 2, 0.87), ("TOOL", 3, 1.00)],
        cost_per_pm=10000.0,
        req_time=False,
        req_cost=True
    )
    ws_main.cell(row=43, column=1, value="→ RESPUESTA TÉCNICA: Para 20 KLOC en modo Orgánico (EAF = 1.0426 y PM ajustado = 77.51 PM) a $10,000/PM, el costo total del proyecto asciende a $775,112.00 MXN.").font = font_italic

    # 5. PROBLEMA V
    create_problem_block(
        start_row=49,
        prob_title="PROBLEMA V",
        prob_desc="Proyecto Empotrado de 311 KLOC con costo de $25,000 MXN/PM. Se solicita TIEMPO Y COSTO",
        mode="Empotrado",
        kloc=311.0,
        drivers_list=[("RELY", 1, 0.75), ("DATA", 5, 1.16), ("CPLX", 2, 0.85), ("TIME", 4, 1.11), ("ACAP", 1, 1.46), ("VIRT", 2, 0.87), ("TOOL", 3, 1.00), ("SCED", 4, 1.04)],
        cost_per_pm=25000.0,
        req_time=True,
        req_cost=True
    )
    ws_main.cell(row=52, column=1, value="→ RESPUESTA TÉCNICA: Para 311 KLOC en modo Empotrado (EAF = 1.0843 y PM ajustado = 2,976.03 PM), el tiempo es de 32.32 meses y el costo total asciende a $74,400,715.00 MXN.").font = font_italic

    # -------------------------------------------------------------------------
    # HOJA 2: TABLA DE CONDUCTORES DE COSTE (EAF)
    # -------------------------------------------------------------------------
    ws_eaf = wb.create_sheet(title="Matriz_EAF")
    ws_eaf.views.sheetView[0].showGridLines = True

    ws_eaf.merge_cells("A1:G1")
    ws_eaf["A1"] = "TABLA DE CALIFICACIÓN DE LOS 15 CONDUCTORES DE COSTE (COST DRIVERS DE BOEHM)"
    ws_eaf["A1"].font = font_title
    ws_eaf["A1"].fill = fill_navy
    ws_eaf["A1"].alignment = align_center
    ws_eaf.row_dimensions[1].height = 30

    eaf_headers = ["Conductor de Coste (Cost Driver)", "Muy Bajo (1)", "Bajo (2)", "Nominal (3)", "Alto (4)", "Muy Alto (5)", "Superior (6)"]
    for c_idx, h in enumerate(eaf_headers, start=1):
        cell = ws_eaf.cell(row=3, column=c_idx, value=h)
        cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        cell.fill = fill_teal
        cell.alignment = align_center
        cell.border = thin_border
    ws_eaf.row_dimensions[3].height = 24

    # 15 drivers data
    eaf_table_data = [
        ("CUALIDADES DEL PRODUCTO", "", "", "", "", "", ""),
        ("Confiabilidad requerida del software (RELY)", 0.75, 0.88, 1.00, 1.15, 1.40, "-"),
        ("Tamaño de la base de datos del uso (DATA)", "-", 0.94, 1.00, 1.08, 1.16, "-"),
        ("Complejidad del producto (CPLX)", 0.70, 0.85, 1.00, 1.15, 1.30, 1.65),
        ("CUALIDADES DEL HARDWARE / PLATAFORMA", "", "", "", "", "", ""),
        ("Apremios de funcionamiento Run-time (TIME)", "-", "-", 1.00, 1.11, 1.30, 1.66),
        ("Apremios de la memoria (STOR)", "-", "-", 1.00, 1.06, 1.21, 1.56),
        ("Volatilidad del ambiente virtual de la máquina (VIRT)", "-", 0.87, 1.00, 1.15, 1.30, "-"),
        ("Tiempo de turnabout requerido (TURN)", "-", 0.87, 1.00, 1.11, 1.15, "-"),
        ("CUALIDADES DEL PERSONAL", "", "", "", "", "", ""),
        ("Capacidad del analista (ACAP)", 1.46, 1.19, 1.00, 0.86, 0.71, "-"),
        ("Experiencia de los usos / aplicaciones (AEXP)", 1.29, 1.13, 1.00, 0.91, 0.82, "-"),
        ("Capacidad de la Software Engineer (PCAP)", 1.42, 1.17, 1.00, 0.86, 0.70, "-"),
        ("Experiencia virtual de la máquina (VEXP)", 1.21, 1.10, 1.00, 0.90, "-", "-"),
        ("Experiencia del lenguaje de programación (LEXP)", 1.14, 1.07, 1.00, 0.95, "-", "-"),
        ("CUALIDADES DEL PROYECTO", "", "", "", "", "", ""),
        ("Uso de las herramientas del software (TOOL)", 1.24, 1.10, 1.00, 0.91, 0.82, "-"),
        ("Uso de los métodos de la tecnología de dotación lógica (MODP)", 1.24, 1.10, 1.00, 0.91, 0.83, "-"),
        ("Horario requerido del desarrollo / restricciones (SCED)", 1.23, 1.08, 1.00, 1.04, 1.10, "-")
    ]

    r_eaf_curr = 4
    for row_vals in eaf_table_data:
        is_category = row_vals[1] == ""
        if is_category:
            ws_eaf.merge_cells(start_row=r_eaf_curr, start_column=1, end_row=r_eaf_curr, end_column=7)
            c = ws_eaf.cell(row=r_eaf_curr, column=1, value=row_vals[0])
            c.font = font_bold
            c.fill = fill_soft_blue
            c.alignment = align_left
            ws_eaf.row_dimensions[r_eaf_curr].height = 20
        else:
            for c_idx, val in enumerate(row_vals, start=1):
                c = ws_eaf.cell(row=r_eaf_curr, column=c_idx, value=val)
                c.font = font_regular
                c.border = thin_border
                if c_idx == 1:
                    c.alignment = align_left
                else:
                    c.alignment = align_center
                    if isinstance(val, (int, float)):
                        c.number_format = "0.00"
            ws_eaf.row_dimensions[r_eaf_curr].height = 18
        r_eaf_curr += 1

    # -------------------------------------------------------------------------
    # HOJA 3: TABLA DE COEFICIENTES COCOMO INTERMEDIO Y TIEMPO BÁSICO
    # -------------------------------------------------------------------------
    ws_coef = wb.create_sheet(title="Coeficientes")
    ws_coef.views.sheetView[0].showGridLines = True

    ws_coef.merge_cells("A1:E1")
    ws_coef["A1"] = "COEFICIENTES MODELO COCOMO INTERMEDIO Y TIEMPO (BOEHM)"
    ws_coef["A1"].font = font_title
    ws_coef["A1"].fill = fill_navy
    ws_coef["A1"].alignment = align_center
    ws_coef.row_dimensions[1].height = 30

    ws_coef.cell(row=3, column=1, value="Ecuación de Esfuerzo Intermedio: PM = A * EAF * (KLOC)^B").font = font_sec
    ws_coef.cell(row=4, column=1, value="Ecuación de Tiempo de Desarrollo: TDEV = C * (PM_ajustado)^D").font = font_sec

    coef_headers = ["Proyecto del Software", "Coeficiente a (PM)", "Exponente b (PM)", "Coeficiente c (TDEV)", "Exponente d (TDEV)"]
    for c_idx, h in enumerate(coef_headers, start=1):
        cell = ws_coef.cell(row=5, column=c_idx, value=h)
        cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        cell.fill = fill_blue_head
        cell.alignment = align_center
        cell.border = thin_border
    ws_coef.row_dimensions[5].height = 24

    coef_rows = [
        ("Orgánico", 3.2, 1.05, 2.5, 0.38),
        ("Semiacoplado", 3.0, 1.12, 2.5, 0.35),
        ("Embebido / Empotrado", 2.8, 1.20, 2.5, 0.32)
    ]

    for r_idx, (p_mode, a, b, c, d) in enumerate(coef_rows, start=6):
        fill_c = fill_soft_blue if r_idx % 2 == 0 else fill_zebra
        for col_idx, val in enumerate([p_mode, a, b, c, d], start=1):
            cell = ws_coef.cell(row=r_idx, column=col_idx, value=val)
            cell.font = font_bold if col_idx == 1 else font_regular
            cell.fill = fill_c
            cell.border = thin_border
            if col_idx == 1:
                cell.alignment = align_left
            else:
                cell.alignment = align_center
                cell.number_format = "0.00"
        ws_coef.row_dimensions[r_idx].height = 20

    # Auto-adjust column widths across all sheets
    for ws in [ws_main, ws_eaf, ws_coef]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or '')
                if not cell.coordinate in ws.merged_cells:
                    max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = max(max_len + 3, 11)

    ws_main.column_dimensions["A"].width = 24
    ws_main.column_dimensions["F"].width = 38
    ws_main.column_dimensions["K"].width = 18

    ws_eaf.column_dimensions["A"].width = 44
    ws_coef.column_dimensions["A"].width = 26

    # Save
    out_path = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_2_2_Problemas_COCOMO_Intermedio.xlsx"
    downloads_path = r"C:\Users\erfierro\Downloads\Actividad_2_2_Problemas_COCOMO_Intermedio.xlsx"
    wb.save(out_path)
    shutil.copy2(out_path, downloads_path)
    print("Excel generado exitosamente en:", out_path)
    print("Copia creada en Downloads:", downloads_path)

if __name__ == "__main__":
    build_cocomo_intermediate_excel()
