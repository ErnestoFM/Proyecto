const ExcelJS = require('exceljs');
const path = require('path');

async function createWorkbook() {
  const wb = new ExcelJS.Workbook();
  wb.creator = 'Gabriel Navarro Salcedo - Alumno';
  wb.created = new Date();

  // Forzar cálculo de fórmulas al abrir en Excel
  wb.calcPr = { fullCalcOnLoad: true };

  const ws = wb.addWorksheet('PERT - Proyecto Web', {
    views: [{ showGridLines: true }]
  });

  // Estilos de colores
  const darkNavy = '1E293B';
  const headerBlue = '2563EB';
  const lightBlue = 'DBEAFE';
  const criticalRed = 'EF4444';
  const criticalRedLight = 'FEE2E2';
  const criticalRedBorder = 'B91C1C';
  const successGreen = '10B981';
  const successGreenLight = 'D1FAE5';
  const borderGray = 'CBD5E1';
  const grayFill = 'F8FAFC';

  // Configuración de anchos de columna
  ws.columns = [
    { width: 4 },  // A (margen)
    { width: 8 },  // B (ID)
    { width: 28 }, // C (Actividad / Descripción)
    { width: 14 }, // D (Predecesoras)
    { width: 12 }, // E (To)
    { width: 12 }, // F (Tm)
    { width: 12 }, // G (Tp)
    { width: 14 }, // H (Te semanas)
    { width: 14 }, // I (Te días)
    { width: 14 }, // J (Varianza σ²)
    { width: 14 }, // K (Desv. σ)
    { width: 11 }, // L (ES días)
    { width: 11 }, // M (EF días)
    { width: 11 }, // N (LS días)
    { width: 11 }, // O (LF días)
    { width: 12 }, // P (Holgura H)
    { width: 15 }, // Q (¿Crítica?)
    { width: 16 }, // R (Fecha Inicio)
    { width: 16 }, // S (Fecha Fin)
  ];

  // Helper para bordes
  const thinBorder = {
    top: { style: 'thin', color: { argb: borderGray } },
    left: { style: 'thin', color: { argb: borderGray } },
    bottom: { style: 'thin', color: { argb: borderGray } },
    right: { style: 'thin', color: { argb: borderGray } }
  };

  const headerBorder = {
    top: { style: 'medium', color: { argb: '1E3A8A' } },
    left: { style: 'thin', color: { argb: '93C5FD' } },
    bottom: { style: 'medium', color: { argb: '1E3A8A' } },
    right: { style: 'thin', color: { argb: '93C5FD' } }
  };

  // 1. TÍTULO Y ENCABEZADO
  ws.mergeCells('B2:S2');
  const titleCell = ws.getCell('B2');
  titleCell.value = 'ACTIVIDAD 1.6: EJERCICIOS DIAGRAMA DE PERT Y RUTA CRÍTICA';
  titleCell.font = { name: 'Calibri', size: 16, bold: true, color: { argb: 'FFFFFF' } };
  titleCell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: darkNavy } };
  titleCell.alignment = { horizontal: 'center', vertical: 'middle' };
  ws.getRow(2).height = 32;

  ws.mergeCells('B3:S3');
  const subCell = ws.getCell('B3');
  subCell.value = 'Problema 1: Desarrollo de una Aplicación Web | Gestión de Proyectos de Software';
  subCell.font = { name: 'Calibri', size: 11, italic: true, color: { argb: 'E2E8F0' } };
  subCell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: '334155' } };
  subCell.alignment = { horizontal: 'center', vertical: 'middle' };
  ws.getRow(3).height = 20;

  // 2. PARÁMETROS DEL PROYECTO
  const params = [
    ['Fecha de Inicio del Proyecto:', '17 de agosto de 2026', 'Fórmula Tiempo Esperado (Te):', 'Te = (To + 4*Tm + Tp) / 6'],
    ['Régimen Laboral:', 'Semana Inglesa (5 días hábiles/sem)', 'Fórmula Varianza (σ²):', 'σ² = ((Tp - To) / 6)²'],
    ['Días por Semana:', 5, 'Fórmula Holgura (H):', 'H = LS - ES = LF - EF']
  ];

  for (let i = 0; i < params.length; i++) {
    const rowIdx = 5 + i;
    ws.getCell(`B${rowIdx}`).value = params[i][0];
    ws.getCell(`B${rowIdx}`).font = { bold: true, size: 10, color: { argb: '1E293B' } };
    ws.mergeCells(`C${rowIdx}:D${rowIdx}`);
    ws.getCell(`C${rowIdx}`).value = params[i][1];
    ws.getCell(`C${rowIdx}`).font = { size: 10 };
    ws.getCell(`C${rowIdx}`).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'F1F5F9' } };

    ws.mergeCells(`F${rowIdx}:G${rowIdx}`);
    ws.getCell(`F${rowIdx}`).value = params[i][2];
    ws.getCell(`F${rowIdx}`).font = { bold: true, size: 10, color: { argb: '1E293B' } };
    ws.mergeCells(`H${rowIdx}:J${rowIdx}`);
    ws.getCell(`H${rowIdx}`).value = params[i][3];
    ws.getCell(`H${rowIdx}`).font = { italic: true, size: 10, color: { argb: '2563EB' } };
    ws.getCell(`H${rowIdx}`).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'EFF6FF' } };
  }

  // 3. TABLA PRINCIPAL DE PERT
  const headerRowIdx = 9;
  const headers = [
    'ID', 'Actividad', 'Predec.', 'To (sem)', 'Tm (sem)', 'Tp (sem)',
    'Te (sem)', 'Te (días)', 'Varianza σ²', 'Desv. σ',
    'ES (días)', 'EF (días)', 'LS (días)', 'LF (días)', 'Holgura H',
    '¿Ruta Crítica?', 'Fecha Inicio', 'Fecha Fin'
  ];

  const colLetters = ['B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S'];
  for (let c = 0; c < headers.length; c++) {
    const cell = ws.getCell(`${colLetters[c]}${headerRowIdx}`);
    cell.value = headers[c];
    cell.font = { name: 'Calibri', size: 10, bold: true, color: { argb: 'FFFFFF' } };
    cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: headerBlue } };
    cell.alignment = { horizontal: 'center', vertical: 'middle', wrapText: true };
    cell.border = headerBorder;
  }
  ws.getRow(headerRowIdx).height = 28;

  // Fechas y cálculos con valores pre-evaluados (result) para visores que no ejecutan fórmulas automáticamente:
  const actData = [
    {
      row: 10, id: 'A', name: 'Planificación', pred: '—', to: 1.0, tm: 1.5, tp: 2.0,
      teSem: 1.5, teDias: 7.5, varVal: 0.0278, desvVal: 0.1667,
      es: 0, efVal: 7.5, lsVal: 0, lfVal: 7.5, hVal: 0, critVal: 'SÍ (CRÍTICA)',
      efForm: 'L10+I10', lsForm: 'O10-I10', lfForm: 'MIN(L11,L12)',
      fIniForm: 'DATE(2026,8,17)', fIniVal: new Date(2026, 7, 17),
      fFinForm: 'WORKDAY($R$10,ROUND(M10,0)-1)', fFinVal: new Date(2026, 7, 26)
    },
    {
      row: 11, id: 'B', name: 'Diseño de la interfaz', pred: 'A', to: 1.0, tm: 2.0, tp: 3.0,
      teSem: 2.0, teDias: 10.0, varVal: 0.1111, desvVal: 0.3333,
      es: 'M10', esVal: 7.5, efVal: 17.5, lsVal: 12.5, lfVal: 22.5, hVal: 5.0, critVal: 'NO',
      efForm: 'L11+I11', lsForm: 'O11-I11', lfForm: 'L13',
      fIniForm: 'WORKDAY(S10,1)', fIniVal: new Date(2026, 7, 27),
      fFinForm: 'WORKDAY($R$10,ROUND(M11,0)-1)', fFinVal: new Date(2026, 8, 9)
    },
    {
      row: 12, id: 'C', name: 'Desarrollo del backend', pred: 'A', to: 2.0, tm: 3.0, tp: 4.0,
      teSem: 3.0, teDias: 15.0, varVal: 0.1111, desvVal: 0.3333,
      es: 'M10', esVal: 7.5, efVal: 22.5, lsVal: 7.5, lfVal: 22.5, hVal: 0, critVal: 'SÍ (CRÍTICA)',
      efForm: 'L12+I12', lsForm: 'O12-I12', lfForm: 'L13',
      fIniForm: 'WORKDAY(S10,1)', fIniVal: new Date(2026, 7, 27),
      fFinForm: 'WORKDAY($R$10,ROUND(M12,0)-1)', fFinVal: new Date(2026, 8, 16)
    },
    {
      row: 13, id: 'D', name: 'Pruebas', pred: 'B, C', to: 1.0, tm: 1.5, tp: 2.0,
      teSem: 1.5, teDias: 7.5, varVal: 0.0278, desvVal: 0.1667,
      es: 'MAX(M11,M12)', esVal: 22.5, efVal: 30.0, lsVal: 22.5, lfVal: 30.0, hVal: 0, critVal: 'SÍ (CRÍTICA)',
      efForm: 'L13+I13', lsForm: 'O13-I13', lfForm: 'L14',
      fIniForm: 'WORKDAY(MAX(S11,S12),1)', fIniVal: new Date(2026, 8, 17),
      fFinForm: 'WORKDAY($R$10,ROUND(M13,0)-1)', fFinVal: new Date(2026, 8, 25)
    },
    {
      row: 14, id: 'E', name: 'Despliegue', pred: 'D', to: 0.5, tm: 1.0, tp: 1.5,
      teSem: 1.0, teDias: 5.0, varVal: 0.0278, desvVal: 0.1667,
      es: 'M13', esVal: 30.0, efVal: 35.0, lsVal: 30.0, lfVal: 35.0, hVal: 0, critVal: 'SÍ (CRÍTICA)',
      efForm: 'L14+I14', lsForm: 'O14-I14', lfForm: 'M14',
      fIniForm: 'WORKDAY(S13,1)', fIniVal: new Date(2026, 8, 28),
      fFinForm: 'WORKDAY($R$10,ROUND(M14,0)-1)', fFinVal: new Date(2026, 9, 2)
    },
  ];

  actData.forEach(act => {
    const r = act.row;
    ws.getCell(`B${r}`).value = act.id;
    ws.getCell(`B${r}`).alignment = { horizontal: 'center' };
    ws.getCell(`C${r}`).value = act.name;
    ws.getCell(`D${r}`).value = act.pred;
    ws.getCell(`D${r}`).alignment = { horizontal: 'center' };
    ws.getCell(`E${r}`).value = act.to;
    ws.getCell(`F${r}`).value = act.tm;
    ws.getCell(`G${r}`).value = act.tp;

    // Fórmulas PERT con resultado precargado
    ws.getCell(`H${r}`).value = { formula: `ROUND((E${r}+4*F${r}+G${r})/6, 4)`, result: act.teSem };
    ws.getCell(`I${r}`).value = { formula: `H${r}*5`, result: act.teDias };
    ws.getCell(`J${r}`).value = { formula: `ROUND(((G${r}-E${r})/6)^2, 4)`, result: act.varVal };
    ws.getCell(`K${r}`).value = { formula: `ROUND(SQRT(J${r}), 4)`, result: act.desvVal };

    // Tiempos tempranos y tardíos con resultado precargado
    if (typeof act.es === 'number') {
      ws.getCell(`L${r}`).value = act.es;
    } else {
      ws.getCell(`L${r}`).value = { formula: act.es, result: act.esVal };
    }
    ws.getCell(`M${r}`).value = { formula: act.efForm, result: act.efVal };
    ws.getCell(`N${r}`).value = { formula: act.lsForm, result: act.lsVal };
    ws.getCell(`O${r}`).value = { formula: act.lfForm, result: act.lfVal };
    ws.getCell(`P${r}`).value = { formula: `N${r}-L${r}`, result: act.hVal };
    ws.getCell(`Q${r}`).value = { formula: `IF(P${r}=0, "SÍ (CRÍTICA)", "NO")`, result: act.critVal };
    
    // Fechas con resultado precargado
    ws.getCell(`R${r}`).value = { formula: act.fIniForm, result: act.fIniVal };
    ws.getCell(`S${r}`).value = { formula: act.fFinForm, result: act.fFinVal };

    // Formatos de números y fechas
    ws.getCell(`E${r}`).numFmt = '0.0';
    ws.getCell(`F${r}`).numFmt = '0.0';
    ws.getCell(`G${r}`).numFmt = '0.0';
    ws.getCell(`H${r}`).numFmt = '0.00';
    ws.getCell(`I${r}`).numFmt = '0.0';
    ws.getCell(`J${r}`).numFmt = '0.0000';
    ws.getCell(`K${r}`).numFmt = '0.0000';
    ws.getCell(`L${r}`).numFmt = '0.0';
    ws.getCell(`M${r}`).numFmt = '0.0';
    ws.getCell(`N${r}`).numFmt = '0.0';
    ws.getCell(`O${r}`).numFmt = '0.0';
    ws.getCell(`P${r}`).numFmt = '0.0';
    ws.getCell(`R${r}`).numFmt = 'DD/MM/YYYY';
    ws.getCell(`S${r}`).numFmt = 'DD/MM/YYYY';

    // Estilos generales por celda
    for (let c = 0; c < headers.length; c++) {
      const cell = ws.getCell(`${colLetters[c]}${r}`);
      cell.border = thinBorder;
      cell.font = { name: 'Calibri', size: 10 };
      if (['E','F','G','H','I','J','K','L','M','N','O','P'].includes(colLetters[c])) {
        cell.alignment = { horizontal: 'right', vertical: 'middle' };
      } else if (['R','S','Q'].includes(colLetters[c])) {
        cell.alignment = { horizontal: 'center', vertical: 'middle' };
      } else {
        cell.alignment = { vertical: 'middle' };
      }
    }

    // Resaltado si es crítica o no (B es no crítica, las demás sí)
    if (act.id !== 'B') {
      ws.getCell(`B${r}`).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: criticalRedLight } };
      ws.getCell(`B${r}`).font = { bold: true, color: { argb: criticalRedBorder } };
      ws.getCell(`Q${r}`).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: criticalRedLight } };
      ws.getCell(`Q${r}`).font = { bold: true, color: { argb: criticalRedBorder } };
    } else {
      ws.getCell(`Q${r}`).font = { color: { argb: '64748B' } };
    }

    ws.getRow(r).height = 22;
  });

  // 4. TOTALES / RESUMEN DE LA RUTA CRÍTICA
  const totRow = 15;
  ws.getCell(`C${totRow}`).value = 'TOTAL RUTA CRÍTICA (A - C - D - E):';
  ws.getCell(`C${totRow}`).font = { bold: true, size: 10, color: { argb: '1E293B' } };
  ws.getCell(`C${totRow}`).alignment = { horizontal: 'right', vertical: 'middle' };

  ws.getCell(`H${totRow}`).value = { formula: 'H10+H12+H13+H14', result: 7.00 };
  ws.getCell(`H${totRow}`).font = { bold: true, size: 10, color: { argb: '1E293B' } };
  ws.getCell(`H${totRow}`).numFmt = '0.00 "sem"';
  ws.getCell(`H${totRow}`).alignment = { horizontal: 'right' };

  ws.getCell(`I${totRow}`).value = { formula: 'I10+I12+I13+I14', result: 35.0 };
  ws.getCell(`I${totRow}`).font = { bold: true, size: 10, color: { argb: 'B91C1C' } };
  ws.getCell(`I${totRow}`).numFmt = '0.0 "días"';
  ws.getCell(`I${totRow}`).alignment = { horizontal: 'right' };

  ws.getCell(`J${totRow}`).value = { formula: 'J10+J12+J13+J14', result: 0.1945 };
  ws.getCell(`J${totRow}`).font = { bold: true, size: 10 };
  ws.getCell(`J${totRow}`).numFmt = '0.0000';
  ws.getCell(`J${totRow}`).alignment = { horizontal: 'right' };

  ws.getCell(`K${totRow}`).value = { formula: `ROUND(SQRT(J${totRow}), 4)`, result: 0.4410 };
  ws.getCell(`K${totRow}`).font = { bold: true, size: 10 };
  ws.getCell(`K${totRow}`).numFmt = '0.0000';
  ws.getCell(`K${totRow}`).alignment = { horizontal: 'right' };

  ws.getCell(`R${totRow}`).value = { formula: 'R10', result: new Date(2026, 7, 17) };
  ws.getCell(`R${totRow}`).font = { bold: true, size: 10 };
  ws.getCell(`R${totRow}`).numFmt = 'DD/MM/YYYY';
  ws.getCell(`R${totRow}`).alignment = { horizontal: 'center' };

  ws.getCell(`S${totRow}`).value = { formula: 'S14', result: new Date(2026, 9, 2) };
  ws.getCell(`S${totRow}`).font = { bold: true, size: 10, color: { argb: 'B91C1C' } };
  ws.getCell(`S${totRow}`).numFmt = 'DD/MM/YYYY';
  ws.getCell(`S${totRow}`).alignment = { horizontal: 'center' };

  // Bordes fila totales
  for (let c = 0; c < headers.length; c++) {
    const cell = ws.getCell(`${colLetters[c]}${totRow}`);
    cell.border = {
      top: { style: 'thin', color: { argb: '1E293B' } },
      bottom: { style: 'double', color: { argb: '1E293B' } }
    };
    cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'F1F5F9' } };
  }
  ws.getRow(totRow).height = 24;

  // 5. CUADRO COMPARATIVO DE RUTAS
  ws.mergeCells('B18:G18');
  ws.getCell('B18').value = 'COMPARACIÓN DE TRAYECTORIAS / RUTAS';
  ws.getCell('B18').font = { bold: true, color: { argb: 'FFFFFF' }, size: 11 };
  ws.getCell('B18').fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: darkNavy } };
  ws.getCell('B18').alignment = { horizontal: 'center', vertical: 'middle' };
  ws.getRow(18).height = 24;

  const rutaHeaders = ['Ruta', 'Secuencia de Actividades', 'Duración (sem)', 'Duración (días hábiles)', 'Holgura Total', 'Estado'];
  const rCols = ['B', 'C', 'D', 'E', 'F', 'G'];
  for (let i = 0; i < rutaHeaders.length; i++) {
    const c = ws.getCell(`${rCols[i]}19`);
    c.value = rutaHeaders[i];
    c.font = { bold: true, size: 10, color: { argb: 'FFFFFF' } };
    c.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: headerBlue } };
    c.alignment = { horizontal: 'center', vertical: 'middle' };
    c.border = thinBorder;
  }
  ws.getRow(19).height = 22;

  // Fila Ruta 1
  ws.getCell('B20').value = 'Ruta 1';
  ws.getCell('B20').alignment = { horizontal: 'center' };
  ws.getCell('C20').value = 'A → B → D → E';
  ws.getCell('D20').value = { formula: 'H10+H11+H13+H14', result: 6.00 };
  ws.getCell('D20').numFmt = '0.00 "sem"';
  ws.getCell('E20').value = { formula: 'I10+I11+I13+I14', result: 30.0 };
  ws.getCell('E20').numFmt = '0.0 "días"';
  ws.getCell('F20').value = { formula: 'E21-E20', result: 5.0 };
  ws.getCell('F20').numFmt = '0.0 "días"';
  ws.getCell('G20').value = 'No Crítica (Holgura = 5 días / 1 sem)';
  ws.getCell('G20').font = { color: { argb: '64748B' }, italic: true };
  [...rCols].forEach(col => {
    ws.getCell(`${col}20`).border = thinBorder;
    if (['D','E','F'].includes(col)) ws.getCell(`${col}20`).alignment = { horizontal: 'right' };
  });

  // Fila Ruta 2
  ws.getCell('B21').value = 'Ruta 2 (CRÍTICA)';
  ws.getCell('B21').font = { bold: true, color: { argb: criticalRedBorder } };
  ws.getCell('B21').alignment = { horizontal: 'center' };
  ws.getCell('B21').fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: criticalRedLight } };
  ws.getCell('C21').value = 'A → C → D → E';
  ws.getCell('C21').font = { bold: true };
  ws.getCell('C21').fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: criticalRedLight } };
  ws.getCell('D21').value = { formula: 'H10+H12+H13+H14', result: 7.00 };
  ws.getCell('D21').font = { bold: true };
  ws.getCell('D21').numFmt = '0.00 "sem"';
  ws.getCell('D21').fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: criticalRedLight } };
  ws.getCell('E21').value = { formula: 'I10+I12+I13+I14', result: 35.0 };
  ws.getCell('E21').font = { bold: true, color: { argb: criticalRedBorder } };
  ws.getCell('E21').numFmt = '0.0 "días"';
  ws.getCell('E21').fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: criticalRedLight } };
  ws.getCell('F21').value = 0;
  ws.getCell('F21').font = { bold: true };
  ws.getCell('F21').numFmt = '0.0 "días"';
  ws.getCell('F21').fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: criticalRedLight } };
  ws.getCell('G21').value = '★ RUTA CRÍTICA (Mayor Duración)';
  ws.getCell('G21').font = { bold: true, color: { argb: criticalRedBorder } };
  ws.getCell('G21').fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: criticalRedLight } };
  [...rCols].forEach(col => {
    ws.getCell(`${col}21`).border = thinBorder;
    if (['D','E','F'].includes(col)) ws.getCell(`${col}21`).alignment = { horizontal: 'right' };
  });

  // 6. CUADRO DE CONCLUSIONES Y RESPUESTAS DEL EJERCICIO
  ws.mergeCells('I18:S18');
  ws.getCell('I18').value = 'CONCLUSIONES Y RESULTADOS EJECUTIVOS';
  ws.getCell('I18').font = { bold: true, color: { argb: 'FFFFFF' }, size: 11 };
  ws.getCell('I18').fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: darkNavy } };
  ws.getCell('I18').alignment = { horizontal: 'center', vertical: 'middle' };

  const conclRows = [
    {
      row: 19,
      label: 'Duración Total Estimada del Proyecto:',
      formula: '="7.00 semanas (" & TEXT(I15, "0.0") & " días hábiles de trabajo)"',
      val: '7.00 semanas (35.0 días hábiles de trabajo)',
      isBold: true
    },
    {
      row: 20,
      label: 'Ruta Crítica Identificada:',
      formula: '="A → C → D → E (Cualquier retraso en estas pospone la entrega)"',
      val: 'A → C → D → E (Cualquier retraso en estas pospone la entrega)',
      isBold: true
    },
    {
      row: 21,
      label: 'Actividad con Holgura Libre / Total:',
      formula: '="B (Diseño de interfaz) tiene " & TEXT(P11/5, "0.0") & " sem (" & TEXT(P11, "0.0") & " días) de holgura"',
      val: 'B (Diseño de interfaz) tiene 1.0 sem (5.0 días) de holgura',
      isBold: false
    },
    {
      row: 22,
      label: 'Fecha de Inicio de Actividades:',
      formula: '=PROPER(TEXT(R10, "dddd")) & " " & TEXT(R10, "DD/MM/YYYY") & " (17 de agosto de 2026)"',
      val: 'Lunes 17/08/2026 (17 de agosto de 2026)',
      isBold: false
    },
    {
      row: 23,
      label: 'Fecha de Término / Entrega del Proyecto:',
      formula: '=PROPER(TEXT(S14, "dddd")) & " " & TEXT(S14, "DD/MM/YYYY") & " (Semana inglesa de 5 días hábiles)"',
      val: 'Viernes 02/10/2026 (Semana inglesa de 5 días hábiles)',
      isBold: true
    },
    {
      row: 24,
      label: 'Varianza y Desviación Estándar Total:',
      formula: '="σ² = " & TEXT(J15, "0.0000") & " semanas² | σ = " & TEXT(K15, "0.0000") & " semanas (" & TEXT(K15*5, "0.00") & " días hábiles)"',
      val: 'σ² = 0.1945 semanas² | σ = 0.4410 semanas (2.20 días hábiles)',
      isBold: true
    }
  ];

  conclRows.forEach(item => {
    ws.mergeCells(`I${item.row}:L${item.row}`);
    const lbl = ws.getCell(`I${item.row}`);
    lbl.value = item.label;
    lbl.font = { bold: true, size: 9.5 };
    lbl.border = thinBorder;

    ws.mergeCells(`M${item.row}:S${item.row}`);
    const val = ws.getCell(`M${item.row}`);
    val.value = { formula: item.formula, result: item.val };
    val.font = { size: 9.5, bold: item.isBold, color: item.isBold ? { argb: '1E3A8A' } : { argb: '334155' } };
    val.fill = { type: 'pattern', pattern: 'solid', fgColor: item.isBold ? { argb: 'EFF6FF' } : { argb: 'FFFFFF' } };
    val.border = thinBorder;
    ws.getRow(item.row).height = 20;
  });

  // 7. DIAGRAMA DE RED / PERT EN HOJA
  ws.mergeCells('B26:S26');
  ws.getCell('B26').value = 'REPRESENTACIÓN DEL DIAGRAMA DE RED PERT (ACTIVIDAD EN EL NODO / AON)';
  ws.getCell('B26').font = { bold: true, color: { argb: 'FFFFFF' }, size: 11 };
  ws.getCell('B26').fill = { type: 'pattern', pattern: 'solid', fgColor: darkNavy };
  ws.getCell('B26').alignment = { horizontal: 'center', vertical: 'middle' };
  ws.getRow(26).height = 24;

  ws.mergeCells('B27:S27');
  ws.getCell('B27').value = 'Estructura de cada bloque: [ ES | Te | EF ]  arriba  /  [ Nombre Actividad (Holgura) ]  centro  /  [ LS | H | LF ]  abajo';
  ws.getCell('B27').font = { italic: true, size: 9.5, color: { argb: '64748B' } };
  ws.getCell('B27').alignment = { horizontal: 'center', vertical: 'middle' };
  ws.getRow(27).height = 18;

  // Función para dibujar un nodo PERT
  function drawPertNode(startCol, startRow, id, name, es, te, ef, ls, h, lf, isCrit) {
    const bgHeader = isCrit ? 'DC2626' : '3B82F6';
    const bgBody = isCrit ? 'FEE2E2' : 'F1F5F9';
    const textColor = isCrit ? '991B1B' : '1E293B';

    // Fila superior (ES | Te | EF)
    ws.getCell(`${startCol}${startRow}`).value = `ES: ${es}`;
    ws.getCell(`${startCol}${startRow}`).font = { size: 8, bold: true, color: { argb: 'FFFFFF' } };
    ws.getCell(`${startCol}${startRow}`).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: bgHeader } };
    ws.getCell(`${startCol}${startRow}`).alignment = { horizontal: 'center' };

    const midCol = String.fromCharCode(startCol.charCodeAt(0) + 1);
    ws.getCell(`${midCol}${startRow}`).value = `Te: ${te}d`;
    ws.getCell(`${midCol}${startRow}`).font = { size: 8, bold: true, color: { argb: 'FFFFFF' } };
    ws.getCell(`${midCol}${startRow}`).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: bgHeader } };
    ws.getCell(`${midCol}${startRow}`).alignment = { horizontal: 'center' };

    const endCol = String.fromCharCode(startCol.charCodeAt(0) + 2);
    ws.getCell(`${endCol}${startRow}`).value = `EF: ${ef}`;
    ws.getCell(`${endCol}${startRow}`).font = { size: 8, bold: true, color: { argb: 'FFFFFF' } };
    ws.getCell(`${endCol}${startRow}`).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: bgHeader } };
    ws.getCell(`${endCol}${startRow}`).alignment = { horizontal: 'center' };

    // Fila del medio (ID y Nombre)
    ws.mergeCells(`${startCol}${startRow+1}:${endCol}${startRow+1}`);
    const nameCell = ws.getCell(`${startCol}${startRow+1}`);
    nameCell.value = `[${id}] ${name}`;
    nameCell.font = { size: 9, bold: true, color: { argb: textColor } };
    nameCell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: bgBody } };
    nameCell.alignment = { horizontal: 'center', vertical: 'middle' };

    // Fila inferior (LS | Holgura | LF)
    ws.getCell(`${startCol}${startRow+2}`).value = `LS: ${ls}`;
    ws.getCell(`${startCol}${startRow+2}`).font = { size: 8, bold: true, color: { argb: textColor } };
    ws.getCell(`${startCol}${startRow+2}`).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: bgBody } };
    ws.getCell(`${startCol}${startRow+2}`).alignment = { horizontal: 'center' };

    ws.getCell(`${midCol}${startRow+2}`).value = `H: ${h}d`;
    ws.getCell(`${midCol}${startRow+2}`).font = { size: 8, bold: true, color: { argb: textColor } };
    ws.getCell(`${midCol}${startRow+2}`).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: bgBody } };
    ws.getCell(`${midCol}${startRow+2}`).alignment = { horizontal: 'center' };

    ws.getCell(`${endCol}${startRow+2}`).value = `LF: ${lf}`;
    ws.getCell(`${endCol}${startRow+2}`).font = { size: 8, bold: true, color: { argb: textColor } };
    ws.getCell(`${endCol}${startRow+2}`).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: bgBody } };
    ws.getCell(`${endCol}${startRow+2}`).alignment = { horizontal: 'center' };

    // Bordes
    for (let r = startRow; r <= startRow + 2; r++) {
      for (let c = startCol.charCodeAt(0); c <= endCol.charCodeAt(0); c++) {
        ws.getCell(`${String.fromCharCode(c)}${r}`).border = thinBorder;
      }
    }
  }

  // Dibujar Nodos:
  // INICIO -> A -> (B y C) -> D -> E -> FIN
  // Nodo A (Fila 32)
  drawPertNode('B', 32, 'A', 'Planificación', '0', '7.5', '7.5', '0', '0', '7.5', true);

  // Flechas entre A y ramas
  ws.getCell('E30').value = '↗ (Rama Sup)';
  ws.getCell('E30').font = { size: 9, bold: true, color: { argb: '64748B' } };
  ws.getCell('E34').value = '═════► (Crítica)';
  ws.getCell('E34').font = { size: 9, bold: true, color: { argb: 'DC2626' } };

  // Nodo B (Rama Superior, Fila 29)
  drawPertNode('F', 29, 'B', 'Diseño Interfaz', '7.5', '10', '17.5', '12.5', '5', '22.5', false);

  // Nodo C (Rama Inferior / Crítica, Fila 33)
  drawPertNode('F', 33, 'C', 'Desarrollo Backend', '7.5', '15', '22.5', '7.5', '0', '22.5', true);

  // Flechas convergentes a D
  ws.getCell('I30').value = '↘ (Holgura: 5d)';
  ws.getCell('I30').font = { size: 9, italic: true, color: { argb: '64748B' } };
  ws.getCell('I34').value = '═════► (Crítica)';
  ws.getCell('I34').font = { size: 9, bold: true, color: { argb: 'DC2626' } };

  // Nodo D (Fila 32)
  drawPertNode('J', 32, 'D', 'Pruebas', '22.5', '7.5', '30', '22.5', '0', '30', true);

  // Flecha a E
  ws.getCell('M33').value = '═════►';
  ws.getCell('M33').font = { size: 10, bold: true, color: { argb: 'DC2626' } };
  ws.getCell('M33').alignment = { horizontal: 'center' };

  // Nodo E (Fila 32)
  drawPertNode('N', 32, 'E', 'Despliegue', '30', '5', '35', '30', '0', '35', true);

  // Leyenda
  ws.mergeCells('B37:F37');
  ws.getCell('B37').value = '■ Rojo: Actividades de Ruta Crítica (Holgura = 0)';
  ws.getCell('B37').font = { bold: true, size: 9.5, color: { argb: 'DC2626' } };

  ws.mergeCells('G37:L37');
  ws.getCell('G37').value = '■ Azul: Actividades No Críticas (Con holgura admisible)';
  ws.getCell('G37').font = { bold: true, size: 9.5, color: { argb: '2563EB' } };

  const outPath = path.join(__dirname, 'Actividad_1.6_Diagrama_PERT_Problema_1.xlsx');
  await wb.xlsx.writeFile(outPath);
  console.log('Archivo creado exitosamente en:', outPath);
}

createWorkbook().catch(err => {
  console.error('Error al generar Excel:', err);
  process.exit(1);
});
