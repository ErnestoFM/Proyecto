const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType, HeadingLevel, BorderStyle } = require('docx');

async function createDocument() {
  const primaryColor = "8C6B52"; // Café tostado
  const secondaryColor = "D98C7F"; // Terracota pastel
  const headerBgColor = "FAF3ED"; // Crema cálido
  const borderColor = "D9D9D9";

  const tableHeaderStyle = {
    fill: "8C6B52",
    color: "FFFFFF",
    bold: true,
  };

  const doc = new Document({
    sections: [
      {
        properties: {},
        children: [
          // Header / Portada de la actividad
          new Paragraph({
            text: "ACTIVIDAD 1.3: DISEÑO DE PRESUPUESTO DE PROYECTO DE SOFTWARE",
            heading: HeadingLevel.TITLE,
            alignment: AlignmentType.CENTER,
            spacing: { after: 120 },
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "Materia / Asignatura: ", bold: true }),
              new TextRun({ text: "Desarrollo de Software Integrador\n" }),
              new TextRun({ text: "Docente: ", bold: true }),
              new TextRun({ text: "Gabriel Navarro Salcedo\n" }),
              new TextRun({ text: "Alumno: ", bold: true }),
              new TextRun({ text: "Ernesto Hatuey Fierro Meléndez\n" }),
              new TextRun({ text: "Proyecto: ", bold: true }),
              new TextRun({ text: "Monchis Café — Plataforma Web Segura para Cafetería Orgánica y Comercial\n" }),
              new TextRun({ text: "Fecha: ", bold: true }),
              new TextRun({ text: "2026-09-01" }),
            ],
            spacing: { after: 400 },
          }),

          // 1. OBJETIVO Y COMPRENSIÓN DEL PROYECTO
          new Paragraph({
            text: "1. Objetivo y Comprensión del Proyecto",
            heading: HeadingLevel.HEADING_1,
            spacing: { before: 240, after: 120 },
          }),
          new Paragraph({
            children: [
              new TextRun({
                text: "El objetivo de este documento es presentar la propuesta de presupuesto detallada y coherente para el desarrollo e implementación de la plataforma web de ",
              }),
              new TextRun({ text: "Monchis Café", bold: true }),
              new TextRun({
                text: ", una cafetería que combina la venta de café orgánico de especialidad regional con productos complementarios comerciales.\n\n",
              }),
              new TextRun({ text: "Alcance Técnico del Sistema:\n", bold: true }),
              new TextRun({ text: "• Architecture Monorepo: Frontend en Vue 3 con vite-ssg (SEO optimizado) y Backend Next.js API Routes.\n" }),
              new TextRun({ text: "• Punto de Venta (POS): Módulo de caja con soporte para efectivo, tarjetas, SPEI, Monchis Rewards y monedero.\n" }),
              new TextRun({ text: "• Orquestador de Eventos con RabbitMQ (Patrón Saga): Transacciones compensatorias (reversas automáticas de cobro en caso de falta de insumos de café orgánico) y Dead Letter Queue (DLQ).\n" }),
              new TextRun({ text: "• Autenticación Stateless y Seguridad: JWT con rotación + Google reCAPTCHA v2/v3 + 2FA para el Administrador.\n" }),
              new TextRun({ text: "• Módulo ODS: Trazabilidad estricta de café de origen regional y programa de incentivos ecológicos (termos/tazas reutilizables).\n" }),
            ],
            spacing: { after: 240 },
          }),

          // 2. DESGLOSE DE PRESUPUESTO
          new Paragraph({
            text: "2. Desglose del Presupuesto por Rubros",
            heading: HeadingLevel.HEADING_1,
            spacing: { before: 240, after: 120 },
          }),

          // TABLA RRHH
          new Paragraph({
            text: "A. Recursos Humanos (Equipo de Desarrollo — 10 Semanas / 2.5 Meses)",
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 180, after: 120 },
          }),
          createTable(
            ["Rol", "Cantidad", "Horas Totales", "Tarifa/Hora", "Costo Total (MXN)"],
            [
              ["Project Manager / Scrum Master", "1", "100 hrs", "$350.00 MXN", "$35,000.00 MXN"],
              ["Diseñador UI/UX (Paleta Pastel)", "1", "80 hrs", "$280.00 MXN", "$22,400.00 MXN"],
              ["Desarrollador Frontend (Vue 3 / SSG)", "1", "200 hrs", "$320.00 MXN", "$64,000.00 MXN"],
              ["Desarrollador Backend (Next.js / RabbitMQ)", "1", "200 hrs", "$340.00 MXN", "$68,000.00 MXN"],
              ["Ingeniero QA / DevOps (TDD & CI/CD)", "1", "100 hrs", "$300.00 MXN", "$30,000.00 MXN"],
              ["Subtotal Recursos Humanos", "5", "680 hrs", "-", "$219,400.00 MXN"],
            ]
          ),

          // TABLA LICENCIAS Y NUBE
          new Paragraph({
            text: "B. Licencias y Servicios Tecnológicos (Cloud & APIs — 12 Meses)",
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 240, after: 120 },
          }),
          createTable(
            ["Concepto", "Proveedor / Servicio", "Duración", "Costo Total (MXN)"],
            [
              ["Infraestructura Cloud (VPS / Docker)", "AWS EC2 / Hetzner Cloud", "12 meses", "$9,600.00 MXN"],
              ["Base de Datos Gestionada (PostgreSQL)", "Supabase / AWS RDS", "12 meses", "$7,200.00 MXN"],
              ["Broker de Mensajería (RabbitMQ Cloud)", "CloudAMQP Cluster", "12 meses", "$6,000.00 MXN"],
              ["Seguridad Anti-Bot", "Google reCAPTCHA Enterprise", "12 meses", "$1,800.00 MXN"],
              ["Correos Transaccionales (SMTP & 2FA)", "Resend / SendGrid API", "12 meses", "$2,400.00 MXN"],
              ["Dominio Web & Certificado SSL Wildcard", "Cloudflare / Namecheap", "12 meses", "$1,200.00 MXN"],
              ["Subtotal Licencias y Servicios Cloud", "-", "-", "$28,200.00 MXN"],
            ]
          ),

          // TABLA HARDWARE
          new Paragraph({
            text: "C. Hardware y Equipos de Pruebas POS",
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 240, after: 120 },
          }),
          createTable(
            ["Concepto", "Cantidad", "Costo Unitario", "Costo Total (MXN)"],
            [
              ["Tableta Touch POS para Pruebas de Caja", "1", "$7,500.00 MXN", "$7,500.00 MXN"],
              ["Lector de Código de Barras USB/Bluetooth", "1", "$1,800.00 MXN", "$1,800.00 MXN"],
              ["Impresora Térmica de Tickets 80mm", "1", "$2,200.00 MXN", "$2,200.00 MXN"],
              ["Subtotal Hardware POS", "-", "-", "$11,500.00 MXN"],
            ]
          ),

          // TABLA ODS Y OTROS
          new Paragraph({
            text: "D. Módulo de Sostenibilidad (ODS) y Gastos Operativos / Legales",
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 240, after: 120 },
          }),
          createTable(
            ["Concepto / Rubro", "Descripción / Alineación", "Costo Total (MXN)"],
            [
              ["Módulo Trazabilidad de Café Orgánico (ODS 12)", "Registro de fincas, fechas de tostado, lotes y descuentos por termos reutilizables", "$16,000.00 MXN"],
              ["Atribución de Tráfico Local (ODS 8 y 9)", "Reporte de conversión desde Google Maps e Instagram para potenciar comercio local", "$8,500.00 MXN"],
              ["Gastos Legales y Políticas de Datos (ODS 16)", "Términos de servicio, aviso de privacidad y cumplimiento de datos personales", "$6,000.00 MXN"],
              ["Marketing de Lanzamiento", "Promoción local, fichas de Google Business y campañas digitales", "$8,000.00 MXN"],
              ["Subtotal ODS, Legales y Marketing", "-", "$38,500.00 MXN"],
            ]
          ),

          // RESUMEN GENERAL
          new Paragraph({
            text: "3. Resumen Ejecutivo y Fondo de Reserva",
            heading: HeadingLevel.HEADING_1,
            spacing: { before: 280, after: 120 },
          }),
          createTable(
            ["Rubro Presupuestal", "Monto Subtotal (MXN)"],
            [
              ["1. Recursos Humanos (Equipo Dev - 10 Semanas)", "$219,400.00 MXN"],
              ["2. Licencias y Servicios Cloud (12 Meses)", "$28,200.00 MXN"],
              ["3. Hardware POS de Pruebas", "$11,500.00 MXN"],
              ["4. Módulo ODS (Trazabilidad y Tráfico Local)", "$24,500.00 MXN"],
              ["5. Legales, Políticas de Datos y Marketing", "$14,000.00 MXN"],
              ["SUBTOTAL ACUMULADO PROYECTO", "$297,600.00 MXN"],
              ["Margen de Imprevistos / Contingencia (10%)", "$29,760.00 MXN"],
              ["TOTAL GENERAL ESTIMADO DEL PROYECTO", "$327,360.00 MXN"],
            ]
          ),

          // JUSTIFICACIÓN TÉCNICA
          new Paragraph({
            text: "4. Justificación Técnica y Metodológica",
            heading: HeadingLevel.HEADING_1,
            spacing: { before: 280, after: 120 },
          }),
          new Paragraph({
            children: [
              new TextRun({ text: "Justificación del Stack Tecnológico:\n", bold: true }),
              new TextRun({
                text: "• Vue 3 + vite-ssg: Elegido para el portal público debido a la velocidad de carga instantánea y la optimización de SEO mediante prerenderizado estático en tiempo de compilación. Esto posiciona a Monchis Café orgánicamente en búsquedas locales (Google Maps).\n",
              }),
              new TextRun({
                text: "• Next.js + Prisma ORM + PostgreSQL: Garantiza seguridad de tipos estricta (TypeScript), consultas optimizadas y control relacional estricto sobre el inventario y lotes de café.\n",
              }),
              new TextRun({
                text: "• RabbitMQ + Patrón Saga: Esencial para evitar la sobreventa. En un entorno de cafetería activa, si el stock de un café de especialidad se agota simultáneamente entre la caja física y un pedido en línea, el patrón Saga revierte la transacción automáticamente.\n\n",
              }),
              new TextRun({ text: "Metodología de Desarrollo (TDD & Scrum por Fases):\n", bold: true }),
              new TextRun({
                text: "El proyecto se ejecutará en 10 semanas distribuidas en 5 Sprints bajo metodología Scrum, aplicando Desarrollo Guiado por Pruebas (TDD). Esto asegura que cada módulo (autenticación JWT, POS, RabbitMQ Saga, panel de atribución) cuente con pruebas unitarias, de integración y Playwright E2E antes de su despliegue a producción.\n",
              }),
            ],
            spacing: { after: 240 },
          }),
        ],
      },
    ],
  });

  const buffer = await Packer.toBuffer(doc);
  const outputPath = path.join(__dirname, '..', 'Actividad_1.3_Presupuesto_Monchis_Cafe.docx');
  fs.writeFileSync(outputPath, buffer);
  console.log(`Documento creado exitosamente en: ${outputPath}`);
}

function createTable(headers, rows) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [
      new TableRow({
        children: headers.map(
          (header) =>
            new TableCell({
              children: [
                new Paragraph({
                  children: [new TextRun({ text: header, bold: true, color: "FFFFFF" })],
                  alignment: AlignmentType.CENTER,
                }),
              ],
              shading: { fill: "8C6B52" },
            })
        ),
      }),
      ...rows.map(
        (row, idx) =>
          new TableRow({
            children: row.map(
              (cellText, cellIdx) =>
                new TableCell({
                  children: [
                    new Paragraph({
                      children: [
                        new TextRun({
                          text: cellText,
                          bold: idx === rows.length - 1, // bold on subtotal/total row
                        }),
                      ],
                      alignment: cellIdx >= row.length - 2 ? AlignmentType.RIGHT : AlignmentType.LEFT,
                    }),
                  ],
                  shading: { fill: idx % 2 === 0 ? "FFFDFB" : "FAF3ED" },
                })
            ),
          })
      ),
    ],
  });
}

createDocument().catch(console.error);
