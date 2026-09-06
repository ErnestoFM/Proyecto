import xlsxwriter

def create_budget_file(filepath):
    wb = xlsxwriter.Workbook(filepath)
    ws = wb.add_worksheet('Project Budget Proposal')
    
    # Configuración de estilos
    title_fmt = wb.add_format({
        'bold': True, 'font_size': 16, 'font_color': '#1B365D',
        'bottom': 2, 'bottom_color': '#1B365D'
    })
    subtitle_fmt = wb.add_format({
        'font_size': 11, 'italic': True, 'font_color': '#555555'
    })
    meta_label = wb.add_format({'bold': True, 'font_size': 10, 'bg_color': '#F0F4F8'})
    meta_val = wb.add_format({'font_size': 10})
    
    header_fmt = wb.add_format({
        'bold': True, 'font_color': '#FFFFFF', 'bg_color': '#1B365D',
        'border': 1, 'align': 'center', 'valign': 'vcenter'
    })
    cat_header = wb.add_format({
        'bold': True, 'font_color': '#1B365D', 'bg_color': '#D9E2EC',
        'border': 1, 'align': 'left'
    })
    cell_text = wb.add_format({'border': 1, 'font_size': 10})
    cell_center = wb.add_format({'border': 1, 'font_size': 10, 'align': 'center'})
    cell_num = wb.add_format({'border': 1, 'font_size': 10, 'align': 'right', 'num_format': '#,##0.00'})
    cell_curr = wb.add_format({'border': 1, 'font_size': 10, 'align': 'right', 'num_format': '$#,##0.00'})
    cell_total_curr = wb.add_format({
        'border': 1, 'bold': True, 'bg_color': '#F0F4F8', 'font_size': 10,
        'align': 'right', 'num_format': '$#,##0.00'
    })
    grand_total_fmt = wb.add_format({
        'border': 2, 'bold': True, 'bg_color': '#1B365D', 'font_color': '#FFFFFF',
        'font_size': 12, 'align': 'right', 'num_format': '$#,##0.00'
    })
    grand_total_lbl = wb.add_format({
        'border': 2, 'bold': True, 'bg_color': '#1B365D', 'font_color': '#FFFFFF',
        'font_size': 12, 'align': 'left'
    })

    # Títulos
    ws.merge_range('A1:H1', 'MONCHIS CAFÉ — PROPUESTA DE PRESUPUESTO DE PROYECTO', title_fmt)
    ws.write('A2', 'Plataforma Web Segura para Cafetería Orgánica y Comercial (Alineada a ODS)', subtitle_fmt)
    
    # Metadatos del Proyecto
    ws.write('A4', 'PROYECTO:', meta_label)
    ws.write('B4', 'Monchis Café POS & Sostenibilidad', meta_val)
    ws.write('D4', 'LÍDER / RESPONSABLE:', meta_label)
    ws.write('E4', 'Ernesto Fierro', meta_val)
    ws.write('G4', 'DURACIÓN:', meta_label)
    ws.write('H4', '16 Semanas (4 Meses)', meta_val)

    ws.write('A5', 'MATERIA:', meta_label)
    ws.write('B5', 'Administración de Proyectos', meta_val)
    ws.write('D5', 'DOCENTE:', meta_label)
    ws.write('E5', 'Dr. Gabriel Navarro Salcedo', meta_val)
    ws.write('G5', 'MONEDA:', meta_label)
    ws.write('H5', 'MXN (Pesos Mexicanos)', meta_val)

    # Encabezados de tabla
    headers = ['WBS', 'CATEGORÍA / TAREA', 'DESCRIPCIÓN Y ESPECIFICACIÓN', 'DEDICACIÓN / CANTIDAD', 'UNIDAD', 'COSTO UNITARIO ($)', 'COSTO TOTAL ($)', 'ALINEACIÓN ODS']
    col_widths = [8, 32, 45, 22, 12, 18, 18, 18]
    for col_idx, width in enumerate(col_widths):
        ws.set_column(col_idx, col_idx, width)
        
    for col_idx, h_text in enumerate(headers):
        ws.write(6, col_idx, h_text, header_fmt)
        
    row = 7
    
    # 1.0 RECURSOS HUMANOS (MANO DE OBRA / LABOR)
    ws.merge_range(row, 0, row, 7, '1.0 RECURSOS HUMANOS Y DESARROLLO (LABOR)', cat_header)
    row += 1
    
    labor_data = [
        ('1.1', 'Líder de Proyecto / Scrum Master', 'Gestión de sprints, riesgos, calidad y alineación ODS', 320, 'Horas', 150.00, 'ODS 8'),
        ('1.2', 'Arquitecto de Software & DevOps', 'Arquitectura monorepo, Docker, CI/CD y RabbitMQ', 640, 'Horas', 150.00, 'ODS 9'),
        ('1.3', 'Desarrollador Full-Stack Backend', 'API Next.js, Prisma ORM, Patrón Saga y autenticación stateless', 640, 'Horas', 125.00, 'ODS 12'),
        ('1.4', 'Desarrollador Full-Stack Frontend', 'Interfaz táctil POS Vue 3, Pinia, SEO vite-ssg y accesibilidad', 640, 'Horas', 125.00, 'ODS 12'),
        ('1.5', 'Especialista en QA & Ciberseguridad', 'Pruebas Vitest, Playwright, escaneo OWASP y a11y', 480, 'Horas', 112.50, 'ODS 16'),
    ]
    
    labor_start_row = row + 1
    for item in labor_data:
        ws.write(row, 0, item[0], cell_center)
        ws.write(row, 1, item[1], cell_text)
        ws.write(row, 2, item[2], cell_text)
        ws.write(row, 3, item[3], cell_num)
        ws.write(row, 4, item[4], cell_center)
        ws.write(row, 5, item[5], cell_curr)
        ws.write_formula(row, 6, f'=D{row+1}*F{row+1}', cell_curr)
        ws.write(row, 7, item[6], cell_center)
        row += 1
    labor_end_row = row
    
    # Subtotal Labor
    ws.merge_range(row, 0, row, 5, 'SUBTOTAL RECURSOS HUMANOS (1.0)', cell_total_curr)
    ws.write_formula(row, 6, f'=SUM(G{labor_start_row}:G{labor_end_row})', cell_total_curr)
    ws.write(row, 7, '', cell_total_curr)
    labor_subtotal_row = row + 1
    row += 2

    # 2.0 RECURSOS MATERIALES Y EQUIPAMIENTO (MATERIALS & HARDWARE)
    ws.merge_range(row, 0, row, 7, '2.0 RECURSOS MATERIALES Y EQUIPAMIENTO (MATERIALS & HARDWARE)', cat_header)
    row += 1
    mat_start_row = row + 1
    
    mat_data = [
        ('2.1', 'Terminal Táctil Mostrador POS', 'Tablet táctil 10.5" con soporte metálico de mostrador', 1, 'Pieza', 6500.00, 'ODS 8, 9'),
        ('2.2', 'Impresora Térmica de Tickets', 'Impresora 80mm USB/Red para tickets ecológicos', 1, 'Pieza', 1800.00, 'ODS 12'),
        ('2.3', 'Lector de Código de Barras / QR', 'Scanner 1D/2D USB de alta precisión para inventario y sellos', 1, 'Pieza', 1200.00, 'ODS 12'),
    ]
    for item in mat_data:
        ws.write(row, 0, item[0], cell_center)
        ws.write(row, 1, item[1], cell_text)
        ws.write(row, 2, item[2], cell_text)
        ws.write(row, 3, item[3], cell_num)
        ws.write(row, 4, item[4], cell_center)
        ws.write(row, 5, item[5], cell_curr)
        ws.write_formula(row, 6, f'=D{row+1}*F{row+1}', cell_curr)
        ws.write(row, 7, item[6], cell_center)
        row += 1
    mat_end_row = row
    
    ws.merge_range(row, 0, row, 5, 'SUBTOTAL MATERIALES Y EQUIPO (2.0)', cell_total_curr)
    ws.write_formula(row, 6, f'=SUM(G{mat_start_row}:G{mat_end_row})', cell_total_curr)
    ws.write(row, 7, '', cell_total_curr)
    mat_subtotal_row = row + 1
    row += 2

    # 3.0 INFRAESTRUCTURA CLOUD Y LICENCIAS (FIXED & CLOUD SERVICES)
    ws.merge_range(row, 0, row, 7, '3.0 INFRAESTRUCTURA CLOUD Y LICENCIAS DE SOFTWARE (FIXED & CLOUD)', cat_header)
    row += 1
    cloud_start_row = row + 1
    
    cloud_data = [
        ('3.1', 'Google Cloud Platform (GCP)', 'Cloud Run, Cloud SQL PostgreSQL, Cloud Memorystore (4 meses)', 4, 'Meses', 1800.00, 'ODS 9'),
        ('3.2', 'CloudAMQP (RabbitMQ Administrado)', 'Broker de mensajería con soporte DLQ y SLA (4 meses)', 4, 'Meses', 550.00, 'ODS 9, 16'),
        ('3.3', 'Dominio Web y Certificados SSL', 'Registro de dominio oficial y certificado Wildcard TLS 1.3', 1, 'Anual', 950.00, 'ODS 16'),
        ('3.4', 'Herramientas de Trabajo y DevOps', 'GitHub Team y herramientas colaborativas de desarrollo (4 meses)', 4, 'Meses', 600.00, 'ODS 9'),
    ]
    for item in cloud_data:
        ws.write(row, 0, item[0], cell_center)
        ws.write(row, 1, item[1], cell_text)
        ws.write(row, 2, item[2], cell_text)
        ws.write(row, 3, item[3], cell_num)
        ws.write(row, 4, item[4], cell_center)
        ws.write(row, 5, item[5], cell_curr)
        ws.write_formula(row, 6, f'=D{row+1}*F{row+1}', cell_curr)
        ws.write(row, 7, item[6], cell_center)
        row += 1
    cloud_end_row = row
    
    ws.merge_range(row, 0, row, 5, 'SUBTOTAL INFRAESTRUCTURA Y SERVICIOS (3.0)', cell_total_curr)
    ws.write_formula(row, 6, f'=SUM(G{cloud_start_row}:G{cloud_end_row})', cell_total_curr)
    ws.write(row, 7, '', cell_total_curr)
    cloud_subtotal_row = row + 1
    row += 2

    # 4.0 CONTINGENCIAS Y GESTIÓN DE RIESGOS (MISC / CONTINGENCY)
    ws.merge_range(row, 0, row, 7, '4.0 CONTINGENCIA OPERATIVA Y RIESGOS (CONTINGENCY & MISC)', cat_header)
    row += 1
    ws.write(row, 0, '4.1', cell_center)
    ws.write(row, 1, 'Fondo de Contingencia para Riesgos (10%)', cell_text)
    ws.write(row, 2, 'Reserva para imprevistos técnicos, fluctuación cambiaria y picos de tráfico', cell_text)
    ws.write(row, 3, 10, cell_num)
    ws.write(row, 4, '% Directo', cell_center)
    ws.write(row, 5, 0.10, cell_num)
    ws.write_formula(row, 6, f'=(G{labor_subtotal_row}+G{mat_subtotal_row}+G{cloud_subtotal_row})*0.10', cell_curr)
    ws.write(row, 7, 'General', cell_center)
    contingency_row = row + 1
    row += 1
    
    ws.merge_range(row, 0, row, 5, 'SUBTOTAL CONTINGENCIA (4.0)', cell_total_curr)
    ws.write_formula(row, 6, f'=G{contingency_row}', cell_total_curr)
    ws.write(row, 7, '', cell_total_curr)
    contingency_subtotal_row = row + 1
    row += 2

    # GRAN TOTAL DEL PROYECTO
    ws.merge_range(row, 0, row, 5, 'PRESUPUESTO TOTAL INTEGRAL DEL PROYECTO (MXN):', grand_total_lbl)
    ws.write_formula(row, 6, f'=G{labor_subtotal_row}+G{mat_subtotal_row}+G{cloud_subtotal_row}+G{contingency_subtotal_row}', grand_total_fmt)
    ws.write(row, 7, '100% ODS', grand_total_fmt)
    
    row += 2
    ws.write(row, 0, 'Notas de Aprobación:', wb.add_format({'bold': True, 'font_size': 10}))
    ws.write(row+1, 0, '1. El presupuesto fue calculado para un horizonte de 16 semanas bajo metodología ágil Scrum.', subtitle_fmt)
    ws.write(row+2, 0, '2. Los costos de personal reflejan las tarifas del mercado local para desarrollo web y QA.', subtitle_fmt)
    ws.write(row+3, 0, '3. Toda la infraestructura en la nube está dimensionada para eficiencia energética y bajo consumo.', subtitle_fmt)
    
    wb.close()
    print(f"Archivo de presupuesto generado exitosamente en: {filepath}")

if __name__ == '__main__':
    create_budget_file(r'd:\ernestofm\Proyecto\docs\presupuesto\Presupuesto_Monchis_Cafe.xlsx')
