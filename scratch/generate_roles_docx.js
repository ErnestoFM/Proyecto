const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType, HeadingLevel } = require('docx');

async function createRolesDocument() {
  const doc = new Document({
    sections: [
      {
        properties: {},
        children: [
          // Entezado y Carátula
          new Paragraph({
            text: "ACTIVIDAD: DEFINICIÓN DE ROLES DEL EQUIPO Y PERFILES DE CONTRATACIÓN",
            heading: HeadingLevel.TITLE,
            alignment: AlignmentType.CENTER,
            spacing: { after: 120 },
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "Materia: ", bold: true }),
              new TextRun({ text: "Desarrollo de Software Integrador\n" }),
              new TextRun({ text: "Docente: ", bold: true }),
              new TextRun({ text: "Gabriel Navarro Salcedo\n" }),
              new TextRun({ text: "Alumno / Consultor: ", bold: true }),
              new TextRun({ text: "Ernesto Hatuey Fierro Meléndez\n" }),
              new TextRun({ text: "Proyecto: ", bold: true }),
              new TextRun({ text: "Monchis Café — Plataforma Web Segura para Cafetería Orgánica y Comercial\n" }),
              new TextRun({ text: "Enfoque: ", bold: true }),
              new TextRun({ text: "Estructura Organizacional y Criterios de Contratación de Consultoría Tech\n" }),
              new TextRun({ text: "Fecha: ", bold: true }),
              new TextRun({ text: "2026-09-01" }),
            ],
            spacing: { after: 360 },
          }),

          // Introducción
          new Paragraph({
            text: "1. Introducción y Enfoque de Consultoría",
            heading: HeadingLevel.HEADING_1,
            spacing: { before: 240, after: 120 },
          }),
          new Paragraph({
            children: [
              new TextRun({
                text: "En el marco del desarrollo de la plataforma web de ",
              }),
              new TextRun({ text: "Monchis Café", bold: true }),
              new TextRun({
                text: ", como firma de consultoría tecnológica se ha estructurado un equipo multidisciplinario de 5 perfiles clave. La solución requiere una arquitectura moderna en Monorepo (Vue 3 + Next.js API Routes), procesamiento asíncrono con RabbitMQ (Patrón Saga), seguridad robusa (JWT stateless + reCAPTCHA) y un diseño cálido pastel orientado a la conversión y fidelización.\n\n" +
                  "A continuación se presenta el manual de perfiles de contratación, responsabilidades y matriz de actividades específicas para cada uno de los integrantes del proyecto.",
              }),
            ],
            spacing: { after: 240 },
          }),

          // SECCIÓN ROLES
          new Paragraph({
            text: "2. Matriz de Roles, Perfiles y Responsabilidades",
            heading: HeadingLevel.HEADING_1,
            spacing: { before: 240, after: 180 },
          }),

          // ROL 1: PM / Scrum Master
          new Paragraph({
            text: "Rol 1: Project Manager / Scrum Master & Product Owner",
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 200, after: 120 },
          }),
          createRoleTable(
            "Project Manager / Scrum Master & Product Owner",
            "Dirección de Proyecto / Consultoría Tecnológica",
            "Licenciatura o Ingeniería en Software, Ciencias de la Computación o Tecnologías de la Información. Certificación Scrum Master (PSM I / CSM) o PMP deseable.",
            "Mínimo 3 años gestionando proyectos de desarrollo web/móvil, liderazgo de equipos ágiles, presupuestación y seguimiento de entregables.",
            "• Metodologías ágiles (Scrum, Kanban).\n• Herramientas de gestión (Jira, Trello, Confluence, GitHub Projects).\n• Gestión de riesgos y métricas de rendimiento (velocity, burndown).\n• Conocimiento general de arquitecturas web (Monorepo, REST/GraphQL).",
            "Liderazgo situacional, comunicación asertiva, resolución de conflictos, negociación con stakeholders, orientación a resultados y empatía con el cliente.",
            [
              "Facilitar la adopción de la metodología Scrum en los 5 sprints de desarrollo.",
              "Liderar la alineación con los Objetivos de Desarrollo Sostenible (ODS 8, 9, 12 y 16) del proyecto.",
              "Administrar el presupuesto de $327,360.00 MXN y controlar el margen de imprevistos.",
              "Coordinar la entrega oportuna de las 7 fases del desarrollo y actuar como enlace entre Monchis Café y el equipo técnico.",
            ],
            [
              "Fase 0/1 (Setup & Mockups): Definir el Product Backlog inicial, redactar historias de usuario (Given/When/Then) y organizar el sprint planning.",
              "Fase 2/3 (Backend & Frontend Core): Coordinar diariamente las standups, resolver bloqueos del equipo e inspeccionar el avance de las APIs y diseño.",
              "Fase 4/5 (POS, Rewards & Analytics): Dar seguimiento a las pruebas del Punto de Venta (POS) y validar el módulo de atribución de tráfico (Google Maps/Instagram).",
              "Fase 6/7 (QA & Despliegue): Liderar la revisión final de sprint (Sprint Review), coordinar la entrega al cliente y cerrar la bitácora del proyecto.",
            ]
          ),

          // ROL 2: UI/UX Designer
          new Paragraph({
            text: "Rol 2: Diseñador UI/UX & Especialista en Accesibilidad Web",
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 240, after: 120 },
          }),
          createRoleTable(
            "Diseñador UI/UX & Especialista en Accesibilidad (WCAG)",
            "Diseño de Producto Digital & Experiencia de Usuario",
            "Licenciatura en Diseño Digital, Diseño Gráfico, Interacción Humano-Computadora o carrera afín.",
            "Mínimo 2 años de experiencia en diseño de interfaces web y móviles, creación de Design Systems y pruebas de usabilidad.",
            "• Figma, Adobe XD, Illustrator.\n• HTML5/CSS3 avanzado, TailwindCSS tokens.\n• Normativas de accesibilidad WCAG 2.1 AA.\n• Prototipado interactivo y arquitectura de información.",
            "Creatividad visual, sensibilidad estética, atención al detalle, pensamiento sistémico y orientación a la usabilidad centrada en el usuario.",
            [
              "Diseñar el Sistema de Diseño visual de Monchis Café con su paleta cálida pastel (#FAF3ED, #8C6B52, #F3C9C9).",
              "Garantizar la usabilidad del Punto de Venta (POS) para cajeros bajo entornos de alta concurrencia.",
              "Asegurar que la web pública cumpla con los estándares de accesibilidad WCAG y puntuación >90% en Lighthouse.",
              "Crear componentes UI reutilizables y guías de estilos para el equipo Frontend.",
            ],
            [
              "Fase 0/1 (Setup & Mockups): Diseñar el kit de UI pastel en Figma, definir la tipografía (Poppins/Nunito) y maquetar los wireframes del POS y Landing.",
              "Fase 2/3 (Backend & Frontend Core): Validar la implementación de los tokens CSS en Vue 3 y supervisar que la iconografía (Phosphor Icons) mantenga coherencia.",
              "Fase 4/5 (POS & Rewards): Diseñar la interfaz del tarjetón digital Monchis Rewards (8vo café gratis) y el ecómetro de tazas reutilizables (ODS 12).",
              "Fase 6/7 (QA & Despliegue): Realizar la auditoría de accesibilidad con axe-core y corregir posibles contrastes de color o problemas de navegación por teclado.",
            ]
          ),

          // ROL 3: Frontend Lead
          new Paragraph({
            text: "Rol 3: Desarrollador Frontend Lead (Vue 3, vite-ssg & SEO)",
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 240, after: 120 },
          }),
          createRoleTable(
            "Desarrollador Frontend Lead (Vue 3 / SSG / SEO)",
            "Ingeniería de Software Frontend",
            "Ingeniería en Sistemas Computacionales, Informática o experiencia profesional equivalente comprobable.",
            "Mínimo 3 años desarrollando aplicaciones web SPA/SSG con Vue.js o React, TypeScript y estrategias de optimización SEO.",
            "• Vue 3 (Composition API), Vite, vite-ssg.\n• TypeScript, Pinia (State Management).\n• TailwindCSS, Vanilla CSS, @vueuse/motion, GSAP.\n• Pruebas unitarias con Vitest y E2E con Playwright.",
            "Capacidad analítica, pasión por el código limpio, trabajo en equipo, capacidad de resolución de problemas complejos y enfoque en rendimiento.",
            [
              "Construir la arquitectura Frontend en el Monorepo del proyecto utilizando Vue 3 y vite-ssg.",
              "Implementar el prerenderizado estático de páginas públicas para maximizar la indexabilidad SEO en búsquedas de cafeterías locales.",
              "Desarrollar el módulo de Punto de Venta (POS) con soporte para pagos en efectivo, tarjeta, SPEI y Monchis Rewards.",
              "Garantizar que el rendimiento de carga supere los 85 puntos en Lighthouse CI.",
            ],
            [
              "Fase 0/1 (Setup & Monorepo): Configurar el workspace de Vue 3 en Turborepo, instalar vite-ssg, Pinia y configurar los linters de código.",
              "Fase 2/3 (Core Frontend): Desarrollar la Landing Page (/), el Menú dinámico y la sección de Trazabilidad de lotes orgánicos con prerenderizado.",
              "Fase 4/5 (POS & Rewards): Programar la interfaz del POS responsivo para tableta/desktop, integrando la lectura de códigos de barras e impresoras térmicas.",
              "Fase 6/7 (QA & Optimization): Ejecutar pruebas E2E en Playwright para múltiples resoluciones (360px a 1440px) y optimizar el bundle final con compresión gzip/brotli.",
            ]
          ),

          // ROL 4: Backend Lead
          new Paragraph({
            text: "Rol 4: Desarrollador Backend Lead & Arquitecto de Eventos (Next.js & RabbitMQ)",
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 240, after: 120 },
          }),
          createRoleTable(
            "Desarrollador Backend Lead & Arquitecto de Eventos",
            "Ingeniería de Software Backend & Arquitectura de Datos",
            "Ingeniería en Ciencias de la Computación, Sistemas Computacionales o áreas afines.",
            "Mínimo 3.5 años de experiencia en desarrollo backend con Node.js, mensajería asíncrona, bases de datos relacionales y seguridad web.",
            "• Node.js, Next.js API Routes, TypeScript.\n• Prisma ORM, PostgreSQL, Redis.\n• Broker de Mensajería RabbitMQ (Patrón Saga, DLQ).\n• Autenticación JWT stateless, OAuth, reCAPTCHA, Zod validation.",
            "Pensamiento lógico riguroso, enfoque en seguridad defensiva, orientación a la arquitectura escalable y capacidad técnica autodidacta.",
            [
              "Diseñar y construir las APIs REST/GraphQL seguras para el funcionamiento de Monchis Café.",
              "Implementar el orquestador de transacciones RabbitMQ con Patrón Saga para ejecutar reversas automáticas ante agotamiento de inventario.",
              "Garantizar la seguridad de la plataforma mediante JWT stateless en cookies httpOnly, Google reCAPTCHA v2/v3 y 2FA.",
              "Modelar y mantener la base de datos PostgreSQL utilizando Prisma ORM con migraciones estrictas.",
            ],
            [
              "Fase 0/1 (Backend Setup): Configurar la base de datos PostgreSQL, definir el esquema MER en Prisma y configurar el contenedor Docker de RabbitMQ.",
              "Fase 2/3 (Backend Core): Desarrollar el módulo de autenticación con rotación de Refresh Tokens, middlewares de RBAC y validaciones con Zod.",
              "Fase 4/5 (Saga Pattern & POS): Implementar el flujo de venta distribuidas; si el café orgánico se agota, activar la transacción compensatoria (Saga) y enviar cola de retardo a DLQ.",
              "Fase 6/7 (QA & Hardening): Realizar pruebas de carga con Supertest, auditar consultas PostgreSQL para prevenir N+1 y asegurar la persistencia transaccional.",
            ]
          ),

          // ROL 5: QA & DevOps
          new Paragraph({
            text: "Rol 5: Ingeniero QA Automation, Seguridad & DevOps",
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 240, after: 120 },
          }),
          createRoleTable(
            "Ingeniero QA Automation, Seguridad (DAST/SAST) & DevOps",
            "Aseguramiento de Calidad, Ciberseguridad e Infraestructura",
            "Ingeniería en Ciberseguridad, Sistemas Computacionales, DevOps o equivalente.",
            "Mínimo 2.5 años en automatización de pruebas de software, integración continua (CI/CD), seguridad web defensiva y contenedorización.",
            "• Frameworks de automatización (Playwright, Vitest, Supertest).\n• Herramientas DAST/SAST (OWASP ZAP, ESLint Security, axe-core).\n• Docker, Docker Compose, GitHub Actions CI/CD.\n• Linux Administration, Nginx/Caddy, SSL/TLS, Terraform.",
            "Espíritu crítico y meticuloso, mentalidad defensiva orientada a la seguridad, proactividad en la automatización y trabajo en equipo.",
            [
              "Diseñar e implementar la estrategia de testing multicapa (unitarias, integración, regresión visual y E2E).",
              "Configurar los pipelines automatizados de CI/CD en GitHub Actions para compilación y pruebas continuas.",
              "Ejecutar escaneos de seguridad DAST con OWASP ZAP para prevenir vulnerabilidades XSS, SQLi y CSRF.",
              "Gestionar la infraestructura de servidores Docker Compose y despliegue en la nube.",
            ],
            [
              "Fase 0/1 (DevOps Setup): Crear los workflows de GitHub Actions (.github/workflows/), configurar linters y preparar las variables de entorno (.env).",
              "Fase 2/3 (Automation Core): Implementar los trajes de prueba unitaria en Vitest para utilidades y Supertest para endpoints de autenticación.",
              "Fase 4/5 (E2E & Security): Crear pruebas E2E en Playwright simulando compras completas en el POS y ejecutar análisis de vulnerabilidades OWASP ZAP.",
              "Fase 6/7 (CI/CD & Deploy): Configurar el despliegue automático a producción mediante Docker Compose, verificar certificados SSL y emitir el reporte final de calidad QA.",
            ]
          ),
        ],
      },
    ],
  });

  const buffer = await Packer.toBuffer(doc);
  const outputPath = path.join(__dirname, '..', 'Actividad_Definicion_de_Roles_Monchis_Cafe.docx');
  fs.writeFileSync(outputPath, buffer);
  console.log(`Documento creado exitosamente en: ${outputPath}`);
}

function createRoleTable(roleName, area, education, experience, hardSkills, softSkills, responsibilities, activities) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [
      createRow("ROL EN EL PROYECTO", roleName, true),
      createRow("ÁREA / DEPARTAMENTO", area),
      createRow("EDUCACIÓN / GRADO", education),
      createRow("EXPERIENCIA REQUERIDA", experience),
      createRow("COMPETENCIAS TÉCNICAS (HARD SKILLS)", hardSkills),
      createRow("HABILIDADES BLANDAS (SOFT SKILLS)", softSkills),
      createRow("RESPONSABILIDADES PRINCIPALES", responsibilities.map(r => `• ${r}`).join("\n")),
      createRow("ACTIVIDADES ESPECÍFICAS POR FASE (SPRINTS)", activities.map(a => `• ${a}`).join("\n\n")),
    ],
  });
}

function createRow(label, content, isHeader = false) {
  return new TableRow({
    children: [
      new TableCell({
        width: { size: 30, type: WidthType.PERCENTAGE },
        children: [
          new Paragraph({
            children: [new TextRun({ text: label, bold: true, color: isHeader ? "FFFFFF" : "4A3B32" })],
            alignment: AlignmentType.LEFT,
          }),
        ],
        shading: { fill: isHeader ? "8C6B52" : "FAF3ED" },
      }),
      new TableCell({
        width: { size: 70, type: WidthType.PERCENTAGE },
        children: content.split("\n").map(
          line =>
            new Paragraph({
              children: [
                new TextRun({
                  text: line,
                  bold: isHeader,
                  color: isHeader ? "FFFFFF" : "000000",
                }),
              ],
              spacing: { after: 40 },
            })
        ),
        shading: { fill: isHeader ? "8C6B52" : "FFFDFB" },
      }),
    ],
  });
}

createRolesDocument().catch(console.error);
