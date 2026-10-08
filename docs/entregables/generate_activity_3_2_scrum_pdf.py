import os
import subprocess
import shutil

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Actividad 3.2 - Gestion de Proyecto con SCRUM y Estimacion con COCOMO Intermedio</title>
<style>
  @page {
    size: letter;
    margin: 20mm 18mm 20mm 18mm;
    @bottom-right {
      content: counter(page);
    }
  }
  
  *, *:before, *:after {
    box-sizing: border-box;
  }

  body {
    font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
    color: #1a202c;
    line-height: 1.5;
    font-size: 10pt;
    margin: 0;
    padding: 0;
    background-color: #ffffff;
  }

  /* Portada */
  .cover-page {
    page-break-after: always;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    padding: 40px 20px 20px 20px;
    border: 2px solid #2b4c7e;
  }

  .cover-header {
    border-bottom: 2px solid #2b4c7e;
    padding-bottom: 20px;
  }

  .cover-header h1 {
    font-size: 16pt;
    font-weight: 700;
    color: #1a365d;
    margin: 0 0 8px 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .cover-header h2 {
    font-size: 13pt;
    font-weight: 600;
    color: #2b4c7e;
    margin: 0 0 6px 0;
  }

  .cover-header h3 {
    font-size: 11pt;
    font-weight: 500;
    color: #4a5568;
    margin: 0;
  }

  .cover-body {
    margin: 40px 0;
  }

  .cover-badge {
    display: inline-block;
    background-color: #edf2f7;
    color: #2b4c7e;
    padding: 6px 16px;
    font-size: 9.5pt;
    font-weight: 600;
    border: 1px solid #cbd5e0;
    border-radius: 4px;
    margin-bottom: 20px;
    text-transform: uppercase;
  }

  .cover-title {
    font-size: 19pt;
    font-weight: 800;
    color: #1a365d;
    margin: 0 0 15px 0;
    line-height: 1.3;
  }

  .cover-subtitle {
    font-size: 12pt;
    color: #4a5568;
    font-weight: 500;
    max-width: 650px;
    margin: 0 auto;
    line-height: 1.4;
  }

  .cover-meta {
    background-color: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 20px;
    text-align: left;
    max-width: 520px;
    margin: 0 auto;
  }

  .cover-meta table {
    width: 100%;
    border-collapse: collapse;
  }

  .cover-meta td {
    padding: 5px 8px;
    font-size: 9.5pt;
  }

  .cover-meta td.label {
    font-weight: 700;
    color: #2b4c7e;
    width: 38%;
  }

  .cover-meta td.val {
    color: #2d3748;
  }

  .cover-footer {
    border-top: 1px solid #e2e8f0;
    padding-top: 15px;
    font-size: 9pt;
    color: #718096;
  }

  /* Encabezados y Secciones */
  h2.section-title {
    font-size: 12.5pt;
    font-weight: 700;
    color: #1a365d;
    border-bottom: 2px solid #2b4c7e;
    padding-bottom: 4px;
    margin: 22px 0 12px 0;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    page-break-after: avoid;
  }

  h3.subsection-title {
    font-size: 10.5pt;
    font-weight: 700;
    color: #2b4c7e;
    margin: 14px 0 6px 0;
    page-break-after: avoid;
  }

  h4.subsubsection-title {
    font-size: 9.5pt;
    font-weight: 700;
    color: #2d3748;
    margin: 10px 0 4px 0;
    page-break-after: avoid;
  }

  p {
    margin: 0 0 9px 0;
    text-align: justify;
  }

  /* Listas */
  ul, ol {
    margin: 0 0 10px 0;
    padding-left: 20px;
  }

  li {
    margin-bottom: 4px;
    text-align: justify;
  }

  /* Tablas Formales */
  table.formal-table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 16px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
  }

  table.formal-table th, table.formal-table td {
    border: 1px solid #cbd5e0;
    padding: 6px 8px;
    vertical-align: top;
  }

  table.formal-table th {
    background-color: #2b4c7e;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    text-transform: uppercase;
    font-size: 8pt;
    letter-spacing: 0.3px;
  }

  table.formal-table tr:nth-child(even) {
    background-color: #f8fafc;
  }

  table.formal-table tr:hover {
    background-color: #edf2f7;
  }

  .text-center { text-align: center; }
  .text-right { text-align: right; }
  .font-bold { font-weight: 700; }

  /* Cuadros Destacados */
  .box-note {
    background-color: #f7fafc;
    border-left: 4px solid #2b4c7e;
    padding: 10px 14px;
    margin: 10px 0 14px 0;
    font-size: 9pt;
    border-top: 1px solid #e2e8f0;
    border-right: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
  }

  .box-note p:last-child {
    margin-bottom: 0;
  }

  /* Fórmulas Matemáticas */
  .math-block {
    background-color: #f8fafc;
    border: 1px solid #cbd5e0;
    border-left: 4px solid #3182ce;
    padding: 10px 16px;
    margin: 10px 0 14px 0;
    font-family: 'Cambria Math', 'Times New Roman', serif;
    font-size: 10pt;
    text-align: center;
  }

  .math-formula {
    font-size: 11pt;
    font-weight: 600;
    color: #1a365d;
    margin: 4px 0;
  }

  .math-desc {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 8.5pt;
    color: #4a5568;
    margin-top: 4px;
  }

  /* User Story Card */
  .us-card {
    border: 1px solid #cbd5e0;
    border-radius: 4px;
    background-color: #ffffff;
    margin-bottom: 10px;
    padding: 8px 12px;
    page-break-inside: avoid;
  }

  .us-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    margin-bottom: 6px;
  }

  .us-card-title {
    font-size: 9.5pt;
    font-weight: 700;
    color: #1a365d;
  }

  .us-card-tag {
    font-size: 8pt;
    font-weight: 600;
    padding: 2px 6px;
    background-color: #edf2f7;
    border: 1px solid #cbd5e0;
    border-radius: 3px;
    color: #2b4c7e;
  }

  .page-break {
    page-break-before: always;
  }

  .reference-item {
    padding-left: 24px;
    text-indent: -24px;
    margin-bottom: 8px;
    font-size: 9pt;
    text-align: justify;
  }
</style>
</head>
<body>

<!-- PORTADA -->
<div class="cover-page">
  <div class="cover-header">
    <h1>Universidad de Guadalajara</h1>
    <h2>Centro Universitario de Tonalá (CUTonalá)</h2>
    <h3>División de Ingenierías e Innovación Tecnológica | Licenciatura en Ingeniería en Computación</h3>
  </div>

  <div class="cover-body">
    <div class="cover-badge">Asignatura: Proyecto Integrador de Desarrollo de Software</div>
    <div class="cover-title">Actividad 3.2: Gestión de Proyecto con SCRUM y Estimación de Esfuerzo con el Modelo COCOMO Intermedio</div>
    <div class="cover-subtitle">
      Planificación Operativa Ágil y Estimación Paramétrica Formal para el Sistema Web ERP de Gestión Empresarial "TechSolutions" (60 KLOC)
    </div>
  </div>

  <div class="cover-meta">
    <table>
      <tr>
        <td class="label">Docente:</td>
        <td class="val">Dr. Gabriel Navarro Salcedo</td>
      </tr>
      <tr>
        <td class="label">Estudiante:</td>
        <td class="val">Ernesto Hatuey Fierro Medina</td>
      </tr>
      <tr>
        <td class="label">Código de Estudiante:</td>
        <td class="val">215487963</td>
      </tr>
      <tr>
        <td class="label">Caso de Estudio:</td>
        <td class="val">TechSolutions S.A. de C.V. (Sistema Web de 60 KLOC)</td>
      </tr>
      <tr>
        <td class="label">Marco Normativo:</td>
        <td class="val">The Scrum Guide 2020 & COCOMO 81 (Barry Boehm)</td>
      </tr>
      <tr>
        <td class="label">Fecha de Entrega:</td>
        <td class="val">8 de octubre de 2026</td>
      </tr>
    </table>
  </div>

  <div class="cover-footer">
    Tonalá, Jalisco, México &bull; Ciclo Escolar 2026-B
  </div>
</div>

<!-- SECCIÓN 1: INTRODUCCIÓN Y CONTEXTO -->
<h2 class="section-title">1. Introducción y Contexto del Proyecto</h2>

<p>
El presente informe documenta la planificación operativa y la estimación cuantitativa de esfuerzo y tiempo para el desarrollo del sistema web integral solicitado por la empresa ficticia <strong>"TechSolutions"</strong>. Dicho sistema tiene como propósito central optimizar y automatizar los procesos de negocio en cuatro áreas fundamentales: gestión de productos, control de inventarios, gestión de ventas y clientes, y generación de reportes personalizados.
</p>

<p>
De acuerdo con las especificaciones técnicas iniciales, el tamaño global del software se ha estimado en <strong>60 KLOC</strong> (60,000 líneas lógicas de código fuente entregadas). Para abordar este desafío con rigor académico y profesional, se aplican dos marcos complementarios de la ingeniería de software:
</p>

<ol>
  <li>
    <strong>Marco Ágil SCRUM (Schwaber & Sutherland, 2020):</strong> Empleado para la organización del equipo, descomposición del trabajo en Historias de Usuario, priorización de valor de negocio, planificación de Sprints y seguimiento visual del flujo de desarrollo mediante tableros y métricas de velocidad.
  </li>
  <li>
    <strong>Modelo Paramétrico COCOMO Intermedio (Boehm, 1981):</strong> Utilizado para el cálculo formal y macroeconómico del esfuerzo total (en Personas-Mes), tiempo calendario de desarrollo y requerimientos promedio de personal, ajustados a través de quince conductores de costo específicos.
  </li>
</ol>

<div class="box-note">
  <strong>Reconciliación de Alcance Metodológico:</strong> Con el fin de garantizar total coherencia técnica entre ambos marcos, en este informe se define de forma explícita que la planificación ágil en cuatro Sprints (8 semanas de desarrollo con un equipo de 4 desarrolladores) abarca la <strong>Fase 1: Minimum Viable Product (MVP) / Core Release</strong>, la cual comprende el núcleo funcional operable (estimado en 12 a 15 KLOC). Por su parte, la estimación paramétrica con COCOMO Intermedio modela la totalidad del sistema enterprise contratado (60 KLOC), incluyendo fases subsecuentes de integración contable, facturación masiva multirregión, migración de datos legacy y hardening de infraestructura de alta disponibilidad.
</div>

<!-- SECCIÓN 2: FORMACIÓN DEL EQUIPO SCRUM -->
<h2 class="section-title">2. Estructura y Conformación del Scrum Team</h2>

<p>
En estricto apego a <em>The Scrum Guide 2020</em> (Schwaber & Sutherland, 2020), la unidad fundamental de trabajo es un <strong>Scrum Team</strong> cohesivo y autogestionado, conformado por profesionales enfocados en un único Objetivo del Producto. El marco Scrum 2020 establece explícitamente que <em>no existen subequipos ni jerarquías internas</em>; no se reconocen cargos de "Lead" o líderes técnicos subordinados. Todos los miembros responsables de construir el incremento comparten la designación de <strong>Developers</strong>.
</p>

<table class="formal-table">
  <thead>
    <tr>
      <th style="width: 25%;">Rol en Scrum</th>
      <th style="width: 25%;">Asignación</th>
      <th style="width: 50%;">Responsabilidades Clave (Scrum Guide 2020)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="font-bold">Product Owner (PO)</td>
      <td>Ing. Roberto Valenzuela</td>
      <td>
        Responsable de maximizar el valor del producto resultante del trabajo del Scrum Team. Administra de forma efectiva el Product Backlog: desarrolla y comunica explícitamente el Objetivo del Producto, redacta y ordena los elementos del Product Backlog, y asegura que sea transparente, visible y comprendido por la organización y los interesados de TechSolutions.
      </td>
    </tr>
    <tr>
      <td class="font-bold">Scrum Master (SM)</td>
      <td>Lic. Diana Morales</td>
      <td>
        Líder que sirve al Scrum Team y a la organización. Responsable de fomentar la comprensión teórica y práctica de Scrum, facilitar la mejora continua, eliminar impedimentos organizacionales y técnicos que frenen el avance de los Developers, y asegurar que todos los eventos de Scrum se celebren de manera positiva, productiva y dentro de los límites de tiempo.
      </td>
    </tr>
    <tr>
      <td class="font-bold">Developer 1</td>
      <td>Ing. Carlos Mendoza</td>
      <td>
        Especialista en arquitectura backend y modelado de datos relacionales (PostgreSQL, Prisma ORM, Node.js/TypeScript). Responsable del diseño e implementación de APIs REST, procedimientos transaccionales ACID y consistencia del kardex.
      </td>
    </tr>
    <tr>
      <td class="font-bold">Developer 2</td>
      <td>Ing. Sofía Reyes</td>
      <td>
        Especialista en ingeniería de frontend y experiencia de usuario (Vue 3, Vite, Pinia, Tailwind CSS). Responsable de interfaces interactivas, componentes accesibles, rendimiento en cliente y diseño responsive del Punto de Venta.
      </td>
    </tr>
    <tr>
      <td class="font-bold">Developer 3</td>
      <td>Ing. Alejandro Silva</td>
      <td>
        Desarrollador full stack especializado en lógica transaccional, servicios de facturación electrónica (CFDI 4.0), generación asíncrona de reportes y pasarelas de cobro multimétodo.
      </td>
    </tr>
    <tr>
      <td class="font-bold">Developer 4</td>
      <td>Ing. Mariana Torres</td>
      <td>
        Especialista en aseguramiento de calidad automatizado (QA) e integración continua (Playwright, Jest, Docker, CI/CD). Diseña suites de pruebas unitarias, de integración y E2E para garantizar la adherencia a la Definition of Done.
      </td>
    </tr>
  </tbody>
</table>

<div class="box-note">
  <strong>Stack Tecnológico Homogéneo del Proyecto:</strong> Con el fin de evitar discrepancias en la implementación, el sistema se construye sobre un ecosistema web estandarizado: <em>Frontend:</em> Vue 3 (Composition API), Vite, Pinia y Tailwind CSS; <em>Backend:</em> Node.js con TypeScript, Express/Nest y Prisma ORM; <em>Base de Datos:</em> PostgreSQL y Redis para caché de sesiones; <em>QA & DevOps:</em> Playwright, Jest, Docker y GitHub Actions.
</div>

<!-- SECCIÓN 3: PRODUCT BACKLOG -->
<h2 class="section-title">3. Product Backlog y Especificación de Historias de Usuario</h2>

<p>
El Product Backlog es una lista ordenada y emergente de todo lo que se requiere para mejorar el producto (Schwaber & Sutherland, 2020). Su compromiso asociado es el <strong>Objetivo del Producto (Product Goal)</strong>:
</p>

<div class="box-note">
  <strong>Compromiso: Objetivo del Producto (Product Goal):</strong><br>
  <em>"Desarrollar y poner en operación un sistema web transaccional y modular de nivel empresarial para TechSolutions, que unifique y automatice el catálogo de productos, el control de inventarios multialmacén mediante kardex en tiempo real, el procesamiento de ventas en terminales POS con facturación fiscal electrónica, y un motor analítico de toma de decisiones estratégicas, garantizando una disponibilidad operativa del 99.8% y una experiencia de usuario ágil."</em>
</div>

<p>
A continuación, se especifican doce (12) Historias de Usuario representativas distribuidas equitativamente entre los cuatro módulos requeridos. Cada historia se describe en formato estándar <em>(Como... Quiero... Para...)</em>, con criterios de aceptación en formato formal de comportamiento <strong>Gherkin (Dado... Cuando... Entonces...)</strong> y su clasificación de priorización mediante el método <strong>MoSCoW</strong> (Must Have, Should Have, Could Have).
</p>

<table class="formal-table">
  <thead>
    <tr>
      <th style="width: 8%;">ID</th>
      <th style="width: 20%;">Módulo</th>
      <th style="width: 44%;">Historia de Usuario y Criterios de Aceptación</th>
      <th style="width: 8%;">MoSCoW</th>
      <th style="width: 10%; text-align: center;">Story Points</th>
      <th style="width: 10%; text-align: center;">Sprint Asignado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="font-bold">US-01</td>
      <td>Gestión de Productos</td>
      <td>
        <strong>Catálogo maestro de productos y matriz de variantes.</strong><br>
        <em>Como</em> administrador de catálogo, <em>quiero</em> registrar, actualizar y dar de baja productos con soporte para variantes (talla, color, presentación), <em>para</em> mantener actualizada la oferta comercial.<br>
        <strong>Criterio de Aceptación (Gherkin):</strong> <em>Dado</em> que el administrador ingresa un producto con código SKU y código de barras únicos, <em>cuando</em> completa los atributos obligatorios y adjunta imágenes, <em>entonces</em> el sistema valida la no duplicidad y almacena el registro en menos de 1 segundo.
      </td>
      <td class="text-center font-bold">Must</td>
      <td class="text-center font-bold">13</td>
      <td class="text-center">Sprint 1</td>
    </tr>
    <tr>
      <td class="font-bold">US-02</td>
      <td>Gestión de Productos</td>
      <td>
        <strong>Categorización taxonómica y gestión de marcas.</strong><br>
        <em>Como</em> gestor de inventario, <em>quiero</em> estructurar categorías jerárquicas multinivel y marcas asociadas, <em>para</em> clasificar los productos y facilitar la búsqueda y navegación.<br>
        <strong>Criterio de Aceptación:</strong> <em>Dado</em> un árbol de categorías de hasta 3 niveles, <em>cuando</em> se asocia un producto a una subcategoría, <em>entonces</em> hereda las propiedades impositivas y de clasificación de la categoría padre.
      </td>
      <td class="text-center font-bold">Should</td>
      <td class="text-center font-bold">5</td>
      <td class="text-center">Sprint 1</td>
    </tr>
    <tr>
      <td class="font-bold">US-03</td>
      <td>Gestión de Clientes</td>
      <td>
        <strong>Directorio centralizado y expediente de clientes.</strong><br>
        <em>Como</em> ejecutivo de ventas, <em>quiero</em> administrar un padrón integral de clientes con datos de contacto, fiscales y límite crediticio, <em>para</em> personalizar la atención y controlar cartera.<br>
        <strong>Criterio de Aceptación:</strong> <em>Dado</em> un cliente con RFC válido, <em>cuando</em> se registra en el sistema, <em>entonces</em> se le asigna un expediente con saldo inicial cero y se valida que el RFC no esté duplicado en la base de datos.
      </td>
      <td class="text-center font-bold">Must</td>
      <td class="text-center font-bold">8</td>
      <td class="text-center">Sprint 1</td>
    </tr>
    <tr>
      <td class="font-bold">US-04</td>
      <td>Control de Inventarios</td>
      <td>
        <strong>Registro transaccional de movimientos en Kardex multialmacén.</strong><br>
        <em>Como</em> jefe de almacén, <em>quiero</em> registrar entradas, salidas y transferencias entre sucursales con cálculo automático de existencias, <em>para</em> tener trazabilidad física y contable del stock.<br>
        <strong>Criterio de Aceptación:</strong> <em>Dado</em> un movimiento de salida por venta o traspaso, <em>cuando</em> se ejecuta la transacción en base de datos, <em>entonces</em> el stock se descuenta atómicamente y se genera un folio inmutable en la bitácora del kardex.
      </td>
      <td class="text-center font-bold">Must</td>
      <td class="text-center font-bold">13</td>
      <td class="text-center">Sprint 2</td>
    </tr>
    <tr>
      <td class="font-bold">US-05</td>
      <td>Control de Inventarios</td>
      <td>
        <strong>Monitor preventivo y alertas de stock mínimo de reorden.</strong><br>
        <em>Como</em> encargado de compras, <em>quiero</em> recibir alertas automáticas cuando un artículo alcance o baje de su umbral mínimo de seguridad, <em>para</em> evitar quiebres de inventario.<br>
        <strong>Criterio de Aceptación:</strong> <em>Dado</em> que las existencias de un producto llegan al nivel crítico configurado, <em>cuando</em> finaliza la transacción, <em>entonces</em> el sistema genera una alerta visual en el dashboard y envía una notificación por correo al departamento de compras.
      </td>
      <td class="text-center font-bold">Should</td>
      <td class="text-center font-bold">5</td>
      <td class="text-center">Sprint 2</td>
    </tr>
    <tr>
      <td class="font-bold">US-06</td>
      <td>Control de Inventarios</td>
      <td>
        <strong>Módulo de tomas físicas y conciliación de ajustes de inventario.</strong><br>
        <em>Como</em> auditor interno, <em>quiero</em> realizar conteos ciegos periódicos y registrar mermas o sobrantes justificados, <em>para</em> conciliar el stock físico contra el inventario teórico.<br>
        <strong>Criterio de Aceptación:</strong> <em>Dado</em> un arqueo físico concluido, <em>cuando</em> el auditor somete las diferencias encontradas, <em>entonces</em> el sistema calcula la desviación en unidades e importe y exige autorización del supervisor antes de aplicar el ajuste al kardex.
      </td>
      <td class="text-center font-bold">Could</td>
      <td class="text-center font-bold">8</td>
      <td class="text-center">Sprint 2</td>
    </tr>
    <tr>
      <td class="font-bold">US-07</td>
      <td>Gestión de Ventas</td>
      <td>
        <strong>Terminal Punto de Venta (POS) y procesamiento de cobros multimétodo.</strong><br>
        <em>Como</em> cajero de sucursal, <em>quiero</em> escanear productos rápidamente y cobrar mediante efectivo, tarjeta bancaria o transferencia combinada, <em>para</em> agilizar el cobro y emitir tickets.<br>
        <strong>Criterio de Aceptación:</strong> <em>Dado</em> un carrito con 5 artículos, <em>cuando</em> el cajero procesa un pago mixto (efectivo y tarjeta), <em>entonces</em> el sistema valida la liquidación exacta, descuenta el stock y genera el ticket de venta en menos de 1.5 segundos.
      </td>
      <td class="text-center font-bold">Must</td>
      <td class="text-center font-bold">13</td>
      <td class="text-center">Sprint 3</td>
    </tr>
    <tr>
      <td class="font-bold">US-08</td>
      <td>Gestión de Ventas</td>
      <td>
        <strong>Facturación electrónica CFDI 4.0 y timbrado fiscal digital.</strong><br>
        <em>Como</em> facturista, <em>quiero</em> timbrar facturas electrónicas a partir de tickets de venta vigentes y gestionar notas de crédito, <em>para</em> cumplir con los requerimientos tributarios del SAT.<br>
        <strong>Criterio de Aceptación:</strong> <em>Dado</em> un ticket liquidado y los datos fiscales del receptor validados, <em>cuando</em> se solicita la emisión, <em>entonces</em> el servicio web timbra el XML ante el PAC autorizado y genera el archivo PDF correspondiente para su descarga o envío.
      </td>
      <td class="text-center font-bold">Must</td>
      <td class="text-center font-bold">8</td>
      <td class="text-center">Sprint 3</td>
    </tr>
    <tr>
      <td class="font-bold">US-09</td>
      <td>Gestión de Ventas</td>
      <td>
        <strong>Emisión de cotizaciones comerciales y conversión a orden de venta.</strong><br>
        <em>Como</em> asesor comercial, <em>quiero</em> generar propuestas económicas formales con vigencia definida y convertirlas en ventas con un clic, <em>para</em> reducir tiempos de captura.<br>
        <strong>Criterio de Aceptación:</strong> <em>Dado</em> una cotización vigente con precios pactados, <em>cuando</em> el cliente acepta la oferta, <em>entonces</em> el sistema traslada automáticamente los renglones al POS conservando las condiciones comerciales.
      </td>
      <td class="text-center font-bold">Could</td>
      <td class="text-center font-bold">5</td>
      <td class="text-center">Sprint 3</td>
    </tr>
    <tr>
      <td class="font-bold">US-10</td>
      <td>Reportes Personalizados</td>
      <td>
        <strong>Motor analítico y dashboard consolidado de ventas.</strong><br>
        <em>Como</em> director comercial, <em>quiero</em> visualizar gráficos interactivos de ventas por periodo, sucursal, producto y margen de utilidad, <em>para</em> evaluar el rendimiento del negocio.<br>
        <strong>Criterio de Aceptación:</strong> <em>Dado</em> un rango de fechas y filtros aplicados por sucursal, <em>cuando</em> se consulta el tablero, <em>entonces</em> las métricas agregadas (ventas totales, ticket promedio, margen bruto) se calculan y renderizan en menos de 2 segundos.
      </td>
      <td class="text-center font-bold">Must</td>
      <td class="text-center font-bold">13</td>
      <td class="text-center">Sprint 4</td>
    </tr>
    <tr>
      <td class="font-bold">US-11</td>
      <td>Reportes Personalizados</td>
      <td>
        <strong>Reporte de rotación y valuación de inventario bajo método PEPS.</strong><br>
        <em>Como</em> gerente de finanzas, <em>quiero</em> consultar la rotación de stock, productos sin movimiento y el costo valorizado de almacén, <em>para</em> optimizar la inversión en existencias.<br>
        <strong>Criterio de Aceptación:</strong> <em>Dado</em> el cierre mensual de operaciones, <em>cuando</em> se genera la valuación, <em>entonces</em> el sistema computa el costo total aplicando el método Primeras Entradas, Primeras Salidas (PEPS) y clasifica artículos según matriz ABC.
      </td>
      <td class="text-center font-bold">Should</td>
      <td class="text-center font-bold">8</td>
      <td class="text-center">Sprint 4</td>
    </tr>
    <tr>
      <td class="font-bold">US-12</td>
      <td>Reportes Personalizados</td>
      <td>
        <strong>Módulo exportador asíncrono multipropósito (Excel, PDF y CSV).</strong><br>
        <em>Como</em> analista operativo, <em>quiero</em> exportar grandes volúmenes de datos transaccionales en formatos abiertos sin bloquear la interfaz, <em>para</em> realizar análisis avanzados externos.<br>
        <strong>Criterio de Aceptación:</strong> <em>Dado</em> un reporte con más de 10,000 registros, <em>cuando</em> se solicita la exportación a Excel o PDF, <em>entonces</em> una tarea en segundo plano procesa la descarga notificando al usuario mediante un enlace seguro cuando el archivo esté listo.
      </td>
      <td class="text-center font-bold">Must</td>
      <td class="text-center font-bold">5</td>
      <td class="text-center">Sprint 4</td>
    </tr>
  </tbody>
</table>

<p>
<strong>Resumen Numérico Consolidado del Product Backlog:</strong> El backlog de la Fase 1 contiene doce (12) Historias de Usuario con una suma acumulada de exactamente <strong>104 Story Points</strong>, distribuidas a razón de <strong>26 Story Points por cada uno de los 4 Sprints</strong> planificados.
</p>

<!-- SECCIÓN 4: ESTIMACIÓN ÁGIL CON PLANNING POKER -->
<div class="page-break"></div>
<h2 class="section-title">4. Estimación del Proyecto usando SCRUM: Planning Poker y Velocidad del Equipo</h2>

<p>
Para estimar el esfuerzo relativo de cada Historia de Usuario, el equipo Scrum ejecutó sesiones formales de <strong>Planning Poker</strong> (Cohn, 2005). Se utilizó la baraja de escala estándar modificada de Fibonacci:
</p>

<div class="math-block">
  <div class="math-formula">Baraja de Fibonacci: { 1, 2, 3, 5, 8, 13, 21 }</div>
  <div class="math-desc">Unidades: Story Points (SP) representativos de esfuerzo, complejidad técnica e incertidumbre.</div>
</div>

<p>
<strong>Dinámica de Consenso por Discusión Técnica:</strong> En estricto apego al marco ágil, la estimación <em>no se obtiene mediante promedios numéricos o votos mayoritarios</em>, ya que promediar oculta la incertidumbre y las discrepancias de diseño técnico. En cada ronda de votación, los cuatro Developers presentan sus cartas de forma simultánea. Cuando surgen discrepancias (por ejemplo, en US-06 donde se emitieron votos de 5 y 13), los desarrolladores con votos extremos exponen sus justificaciones técnicas (riesgos de concurrencia en bases de datos, complejidad de la interfaz o necesidad de auditoría). Tras el debate, se efectúa una segunda ronda hasta alcanzar un <strong>consenso argumentativo pleno</strong>.
</p>

<table class="formal-table">
  <thead>
    <tr>
      <th style="width: 8%; text-align: center;">US</th>
      <th style="width: 25%;">Historia de Usuario</th>
      <th style="width: 8%; text-align: center;">Dev 1</th>
      <th style="width: 8%; text-align: center;">Dev 2</th>
      <th style="width: 8%; text-align: center;">Dev 3</th>
      <th style="width: 8%; text-align: center;">Dev 4</th>
      <th style="width: 10%; text-align: center;">Consenso</th>
      <th style="width: 25%;">Justificación Técnica del Consenso</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="text-center font-bold">US-01</td>
      <td>Catálogo Maestro y Variantes</td>
      <td class="text-center">13</td>
      <td class="text-center">13</td>
      <td class="text-center">8</td>
      <td class="text-center">13</td>
      <td class="text-center font-bold">13</td>
      <td>Alta complejidad en la matriz de atributos dinámicos y persistencia relacional.</td>
    </tr>
    <tr>
      <td class="text-center font-bold">US-02</td>
      <td>Categorización y Marcas</td>
      <td class="text-center">5</td>
      <td class="text-center">5</td>
      <td class="text-center">3</td>
      <td class="text-center">5</td>
      <td class="text-center font-bold">5</td>
      <td>Estructura jerárquica recursiva estándar; CRUD con validaciones de árbol.</td>
    </tr>
    <tr>
      <td class="text-center font-bold">US-03</td>
      <td>Directorio de Clientes</td>
      <td class="text-center">8</td>
      <td class="text-center">8</td>
      <td class="text-center">5</td>
      <td class="text-center">8</td>
      <td class="text-center font-bold">8</td>
      <td>Validaciones fiscales de RFC, historial crediticio y control de saldo deudor.</td>
    </tr>
    <tr>
      <td class="text-center font-bold">US-04</td>
      <td>Kardex Transaccional</td>
      <td class="text-center">13</td>
      <td class="text-center">8</td>
      <td class="text-center">13</td>
      <td class="text-center">13</td>
      <td class="text-center font-bold">13</td>
      <td>Transacciones atómicas estrictas (ACID), bloqueos de fila y auditoría inmutable.</td>
    </tr>
    <tr>
      <td class="text-center font-bold">US-05</td>
      <td>Monitor y Alertas Stock</td>
      <td class="text-center">5</td>
      <td class="text-center">5</td>
      <td class="text-center">5</td>
      <td class="text-center">3</td>
      <td class="text-center font-bold">5</td>
      <td>Disparadores de eventos en base de datos y despacho asíncrono de correos.</td>
    </tr>
    <tr>
      <td class="text-center font-bold">US-06</td>
      <td>Tomas Físicas y Conciliación</td>
      <td class="text-center">8</td>
      <td class="text-center">5</td>
      <td class="text-center">8</td>
      <td class="text-center">8</td>
      <td class="text-center font-bold">8</td>
      <td>Algoritmo de cálculo de desviaciones, arqueo ciego y doble confirmación.</td>
    </tr>
    <tr>
      <td class="text-center font-bold">US-07</td>
      <td>Terminal POS y Cobro</td>
      <td class="text-center">13</td>
      <td class="text-center">13</td>
      <td class="text-center">13</td>
      <td class="text-center">8</td>
      <td class="text-center font-bold">13</td>
      <td>Manejo de estados de carrito en cliente, lector de barras y pagos divididos.</td>
    </tr>
    <tr>
      <td class="text-center font-bold">US-08</td>
      <td>Facturación CFDI 4.0</td>
      <td class="text-center">8</td>
      <td class="text-center">5</td>
      <td class="text-center">8</td>
      <td class="text-center">8</td>
      <td class="text-center font-bold">8</td>
      <td>Integración con Web Services de PAC certificado, sellado criptográfico y XML.</td>
    </tr>
    <tr>
      <td class="text-center font-bold">US-09</td>
      <td>Cotizaciones Comerciales</td>
      <td class="text-center">5</td>
      <td class="text-center">5</td>
      <td class="text-center">5</td>
      <td class="text-center">3</td>
      <td class="text-center font-bold">5</td>
      <td>Generación de folios con caducidad y clonación estructurada hacia orden POS.</td>
    </tr>
    <tr>
      <td class="text-center font-bold">US-10</td>
      <td>Motor Analítico Ventas</td>
      <td class="text-center">13</td>
      <td class="text-center">13</td>
      <td class="text-center">8</td>
      <td class="text-center">13</td>
      <td class="text-center font-bold">13</td>
      <td>Consultas agregadas complejas (GROUP BY, OLAP), caché Redis y gráficas interactivas.</td>
    </tr>
    <tr>
      <td class="text-center font-bold">US-11</td>
      <td>Valuación Inventario (PEPS)</td>
      <td class="text-center">8</td>
      <td class="text-center">8</td>
      <td class="text-center">8</td>
      <td class="text-center">5</td>
      <td class="text-center font-bold">8</td>
      <td>Lógica contable de capas de costo histórico por lote y matriz de rotación ABC.</td>
    </tr>
    <tr>
      <td class="text-center font-bold">US-12</td>
      <td>Exportador Asíncrono</td>
      <td class="text-center">5</td>
      <td class="text-center">5</td>
      <td class="text-center">5</td>
      <td class="text-center">5</td>
      <td class="text-center font-bold">5</td>
      <td>Colas de trabajo en segundo plano para generación de buffers XLSX/PDF sin bloquear.</td>
    </tr>
  </tbody>
</table>

<h3 class="subsection-title">4.1. Cálculo de Capacidad, Velocidad y Previsión de Sprints</h3>

<p>
La capacidad de trabajo del equipo se fundamenta en la dedicación formal de los cuatro Developers durante un Sprint estándar de 2 semanas (10 días laborables):
</p>

<div class="math-block">
  <div class="math-formula">Capacidad Nominal = 4 Developers &times; 10 d&iacute;as h&aacute;biles &times; 6 horas productivas/d&iacute;a = 240 horas por Sprint</div>
  <div class="math-desc">Se asumen 6 horas netas de trabajo técnico al día por desarrollador (descontando eventos, coordinación y pausas operativas).</div>
</div>

<p>
Con base en la complejidad de las historias seleccionadas y la experiencia previa del equipo, se estableció una <strong>Velocidad del Equipo ($V$) de 26 Story Points por Sprint</strong>. Esto establece una relación de esfuerzo medio equivalente a:
</p>

<div class="math-block">
  <div class="math-formula">Factor de Esfuerzo = 240 horas / 26 Story Points &asymp; 9.23 horas-hombre por Story Point</div>
</div>

<p>
A partir de estos valores consolidados, la cantidad exacta de Sprints requeridos para concluir las 104 Story Points del Product Backlog es:
</p>

<div class="math-block">
  <div class="math-formula">Sprints Requeridos = Total Story Points / Velocidad = 104 SP / 26 SP/Sprint = 4.0 Sprints</div>
  <div class="math-desc">El plan cubre exactamente los 4 Sprints solicitados en la planeación operativa, con una carga equilibrada al 100%.</div>
</div>

<!-- SECCIÓN 5: PLANIFICACIÓN DE SPRINTS -->
<div class="page-break"></div>
<h2 class="section-title">5. Planificación Operativa de Sprints y Desglose de Tareas Detalladas</h2>

<p>
En cumplimiento de <em>The Scrum Guide 2020</em>, la <strong>Sprint Planning</strong> aborda tres temas esenciales: <em>¿Por qué es valioso este Sprint?</em> (Sprint Goal), <em>¿Qué se puede hacer en este Sprint?</em> (Selección de PBIs) y <em>¿Cómo se realizará el trabajo elegido?</em> (Plan de acción y descomposición en tareas). Asimismo, los Developers descomponen los elementos en tareas con una duración estimada de <strong>2 a 8 horas</strong> (elementos de un día de trabajo o menos).
</p>

<div class="box-note">
  <strong>Distribución y Justificación de las 240 Horas por Sprint:</strong><br>
  Para cada Sprint, las 240 horas de capacidad nominal del equipo se componen rigurosamente de la siguiente manera:
  <ul>
    <li><strong>Desarrollo y codificación de historias (Backlog core):</strong> 132 horas desglosadas en tareas técnicas específicas de 4 a 8 horas (mostradas en las tablas siguientes).</li>
    <li><strong>Pruebas de integración, QA automatizado y Code Review:</strong> 48 horas distribuidas entre los 4 desarrolladores (12 h por persona durante el Sprint).</li>
    <li><strong>Eventos formales de Scrum (Scrum Guide 2020):</strong> 40 horas en total para el equipo: Sprint Planning (4 h &times; 4 = 16 h), Daily Scrums (15 min &times; 9 d &times; 4 = 9 h), Sprint Review (2 h &times; 4 = 8 h) y Sprint Retrospective (1.5 h &times; 4 = 6 h, aprox. 39-40 h).</li>
    <li><strong>Refinamiento continuo del Product Backlog:</strong> 20 horas acumuladas (aproximadamente el 8% del tiempo del equipo, dentro del límite máximo del 10% que prescribe Scrum).</li>
    <li><strong>Suma total exacta:</strong> 132 h + 48 h + 40 h + 20 h = <strong>240 horas por Sprint</strong>.</li>
  </ul>
</div>

<!-- SPRINT 1 -->
<h3 class="subsection-title">Sprint 1 (Semanas 1 y 2): Cimientos del Sistema, Catálogo de Productos y Clientes</h3>
<p>
<strong>Compromiso (Sprint Goal):</strong> <em>"Establecer la infraestructura base del sistema y habilitar la administración integral del catálogo de productos y el padrón centralizado de clientes bajo estándares de seguridad."</em><br>
<strong>Puntos Comprometidos:</strong> 26 SP (US-01: 13 SP, US-02: 5 SP, US-03: 8 SP).<br>
<strong>Incremento de Software:</strong> Primer incremento utilizable que permite autenticación segura de usuarios, administración de catálogo multinivel y registro de clientes. <em>(Nota: No constituye aún un MVP de negocio, pues no incluye operaciones comerciales ni inventario).</em>
</p>

<table class="formal-table">
  <thead>
    <tr>
      <th style="width: 10%;">ID Tarea</th>
      <th style="width: 10%;">Historia</th>
      <th style="width: 45%;">Descripción de la Tarea Técnica</th>
      <th style="width: 15%;">Responsable</th>
      <th style="width: 10%; text-align: center;">Horas Est.</th>
      <th style="width: 10%; text-align: center;">Estado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="font-bold">T1.1</td>
      <td>US-01</td>
      <td>Modelado de esquema Prisma para productos, atributos dinámicos y migración PostgreSQL.</td>
      <td>Developer 1</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T1.2</td>
      <td>US-01</td>
      <td>Implementación de endpoints REST para CRUD de productos con carga y compresión de fotos.</td>
      <td>Developer 1</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T1.3</td>
      <td>US-01</td>
      <td>Desarrollo de interfaz en Vue 3 con validaciones en formulario reactivo para productos.</td>
      <td>Developer 2</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T1.4</td>
      <td>US-01</td>
      <td>Implementación de pruebas unitarias Jest y pruebas E2E en Playwright para catálogo.</td>
      <td>Developer 4</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T1.5</td>
      <td>US-02</td>
      <td>Diseño de estructura arbórea para categorías y endpoints jerárquicos recursivos.</td>
      <td>Developer 3</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T1.6</td>
      <td>US-02</td>
      <td>Componente de interfaz con visualización en árbol y drag-and-drop para categorías.</td>
      <td>Developer 2</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T1.7</td>
      <td>US-03</td>
      <td>Modelado de tabla de clientes, validación de RFC/correo y lógica de límite de crédito.</td>
      <td>Developer 1</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T1.8</td>
      <td>US-03</td>
      <td>Vista de padrón de clientes con paginación, filtros dinámicos y modal de edición.</td>
      <td>Developer 2</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T1.9</td>
      <td>US-03</td>
      <td>Pruebas de validación de unicidad de RFC y cálculo de límites de crédito en backend.</td>
      <td>Developer 4</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T1.10</td>
      <td>Infra</td>
      <td>Configuración de contenedor Docker, pipeline CI/CD en GitHub Actions y linting.</td>
      <td>Developer 3</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
  </tbody>
</table>

<!-- SPRINT 2 -->
<h3 class="subsection-title">Sprint 2 (Semanas 3 y 4): Control de Inventarios Multi-Almacén y Kardex</h3>
<p>
<strong>Compromiso (Sprint Goal):</strong> <em>"Garantizar la trazabilidad y consistencia transaccional del inventario mediante el kardex multialmacén, control de mermas y sistema preventivo de stock mínimo."</em><br>
<strong>Puntos Comprometidos:</strong> 26 SP (US-04: 13 SP, US-05: 5 SP, US-06: 8 SP).<br>
<strong>Incremento de Software:</strong> Segundo incremento acumulado que añade la gestión física y contable del stock sobre los productos y clientes previamente implementados.
</p>

<table class="formal-table">
  <thead>
    <tr>
      <th style="width: 10%;">ID Tarea</th>
      <th style="width: 10%;">Historia</th>
      <th style="width: 45%;">Descripción de la Tarea Técnica</th>
      <th style="width: 15%;">Responsable</th>
      <th style="width: 10%; text-align: center;">Horas Est.</th>
      <th style="width: 10%; text-align: center;">Estado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="font-bold">T2.1</td>
      <td>US-04</td>
      <td>Diseño de tabla de kardex con aislamiento transaccional PostgreSQL (SERIALIZABLE) y locks.</td>
      <td>Developer 1</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T2.2</td>
      <td>US-04</td>
      <td>Servicio backend de transferencias entre almacenes con reversiones seguras (Rollback).</td>
      <td>Developer 3</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T2.3</td>
      <td>US-04</td>
      <td>Interfaz de consulta del kardex cronológico con filtros por sucursal, fecha y SKU.</td>
      <td>Developer 2</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T2.4</td>
      <td>US-04</td>
      <td>Pruebas de estrés y concurrencia para evitar condiciones de carrera (Race Conditions) en stock.</td>
      <td>Developer 4</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T2.5</td>
      <td>US-05</td>
      <td>Creación de disparadores de stock mínimo y cola en segundo plano con Redis/BullMQ.</td>
      <td>Developer 1</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T2.6</td>
      <td>US-05</td>
      <td>Centro de notificaciones visuales en frontend con badges y alertas configurables.</td>
      <td>Developer 2</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T2.7</td>
      <td>US-06</td>
      <td>Servicio para generación de hojas de conteo ciego y captura de existencias físicas.</td>
      <td>Developer 3</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T2.8</td>
      <td>US-06</td>
      <td>Pantalla de conciliación de diferencias de inventario con autorización de supervisión.</td>
      <td>Developer 2</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T2.9</td>
      <td>US-06</td>
      <td>Pruebas automatizadas del flujo de autorización de ajustes y auditoría de mermas.</td>
      <td>Developer 4</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
  </tbody>
</table>

<!-- SPRINT 3 -->
<div class="page-break"></div>
<h3 class="subsection-title">Sprint 3 (Semanas 5 y 6): Punto de Venta (POS), Facturación Fiscal y Cotizaciones</h3>
<p>
<strong>Compromiso (Sprint Goal):</strong> <em>"Integrar el flujo comercial completo procesando transacciones en terminales POS con descuento en kardex, cobros multimétodo y timbrado fiscal digital."</em><br>
<strong>Puntos Comprometidos:</strong> 26 SP (US-07: 13 SP, US-08: 8 SP, US-09: 5 SP).<br>
<strong>Incremento de Software:</strong> <strong>Minimum Viable Product (MVP Operable de Negocio).</strong> En este punto del ciclo de vida, el producto alcanza viabilidad operativa plena: una sucursal puede operar atendiendo clientes, cobrando ventas, facturando y descontando existencias en tiempo real.
</p>

<table class="formal-table">
  <thead>
    <tr>
      <th style="width: 10%;">ID Tarea</th>
      <th style="width: 10%;">Historia</th>
      <th style="width: 45%;">Descripción de la Tarea Técnica</th>
      <th style="width: 15%;">Responsable</th>
      <th style="width: 10%; text-align: center;">Horas Est.</th>
      <th style="width: 10%; text-align: center;">Estado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="font-bold">T3.1</td>
      <td>US-07</td>
      <td>Desarrollo de interfaz de Punto de Venta rápida con navegación por teclado y lector de barras.</td>
      <td>Developer 2</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T3.2</td>
      <td>US-07</td>
      <td>Servicio transaccional de liquidación de ventas con soporte para múltiples métodos de pago.</td>
      <td>Developer 1</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T3.3</td>
      <td>US-07</td>
      <td>Módulo de impresión térmica de tickets de venta con códigos QR y desglose fiscal.</td>
      <td>Developer 3</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T3.4</td>
      <td>US-07</td>
      <td>Pruebas de latencia en POS (validación de respuesta menor a 1.5 s bajo concurrencia).</td>
      <td>Developer 4</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T3.5</td>
      <td>US-08</td>
      <td>Integración con Web Service de PAC para generación y timbrado de comprobantes CFDI 4.0.</td>
      <td>Developer 3</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T3.6</td>
      <td>US-08</td>
      <td>Servicio de generación de representación impresa en PDF de la factura y entrega de XML.</td>
      <td>Developer 1</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T3.7</td>
      <td>US-08</td>
      <td>Pruebas de validación de sellado digital, cancelación de comprobantes y validaciones de RFC.</td>
      <td>Developer 4</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T3.8</td>
      <td>US-09</td>
      <td>Modelo y endpoints para cotizaciones con cálculo de vigencia y bloqueo de precios pactados.</td>
      <td>Developer 1</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T3.9</td>
      <td>US-09</td>
      <td>Botón y flujo de conversión de cotización directa a ticket del POS conservando ítems.</td>
      <td>Developer 2</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
  </tbody>
</table>

<!-- SPRINT 4 -->
<h3 class="subsection-title">Sprint 4 (Semanas 7 y 8): Reportes Personalizados, Business Intelligence y Hardening</h3>
<p>
<strong>Compromiso (Sprint Goal):</strong> <em>"Consolidar la plataforma de analítica y reportes de gestión comercial y de inventarios, asegurando exportaciones asíncronas y estabilidad para producción."</em><br>
<strong>Puntos Comprometidos:</strong> 26 SP (US-10: 13 SP, US-11: 8 SP, US-12: 5 SP).<br>
<strong>Incremento de Software:</strong> <strong>Entrega de la Fase 1 / Core Release.</strong> Sistema integral completamente funcional que engloba catálogo, clientes, inventario físico, ventas POS, timbrado CFDI y analítica gerencial exportable.
</p>

<table class="formal-table">
  <thead>
    <tr>
      <th style="width: 10%;">ID Tarea</th>
      <th style="width: 10%;">Historia</th>
      <th style="width: 45%;">Descripción de la Tarea Técnica</th>
      <th style="width: 15%;">Responsable</th>
      <th style="width: 10%; text-align: center;">Horas Est.</th>
      <th style="width: 10%; text-align: center;">Estado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="font-bold">T4.1</td>
      <td>US-10</td>
      <td>Consultas analíticas optimizadas en PostgreSQL (vistas materializadas, agregaciones).</td>
      <td>Developer 1</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T4.2</td>
      <td>US-10</td>
      <td>Dashboard interactivo con Chart.js/ApexCharts para ventas por periodo, sucursal y margen.</td>
      <td>Developer 2</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T4.3</td>
      <td>US-10</td>
      <td>Estrategia de caché en Redis para consultas de reportes ejecutivos de alta demanda.</td>
      <td>Developer 3</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T4.4</td>
      <td>US-11</td>
      <td>Implementación de algoritmo contable de valuación por capas PEPS y matriz de rotación ABC.</td>
      <td>Developer 1</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T4.5</td>
      <td>US-11</td>
      <td>Interfaz de auditoría de costos de inventario con comparativa de márgenes históricos.</td>
      <td>Developer 2</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T4.6</td>
      <td>US-12</td>
      <td>Worker asíncrono para generación en background de archivos Excel (xlsx) y PDF masivos.</td>
      <td>Developer 3</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T4.7</td>
      <td>US-12</td>
      <td>Mecanismo seguro de descarga temporal mediante URLs firmadas y limpieza de archivos.</td>
      <td>Developer 1</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T4.8</td>
      <td>Calidad</td>
      <td>Suite de pruebas E2E de regresión completa del sistema con Playwright.</td>
      <td>Developer 4</td>
      <td class="text-center">8 h</td>
      <td class="text-center">Done</td>
    </tr>
    <tr>
      <td class="font-bold">T4.9</td>
      <td>DevOps</td>
      <td>Hardening de seguridad (OWASP Top 10, headers HSTS, rate limiting) y despliegue a Staging.</td>
      <td>Developer 3</td>
      <td class="text-center">6 h</td>
      <td class="text-center">Done</td>
    </tr>
  </tbody>
</table>

<h3 class="subsection-title">5.1. Tablero SCRUM Operativo y Definition of Done (DoD)</h3>

<p>
Para garantizar el flujo de valor y la inspección continua, el Scrum Team gestiona las tareas a través de un <strong>Tablero SCRUM (Kanban Board)</strong> estructurado en cuatro estados con límites explícitos de trabajo en progreso:
</p>

<table class="formal-table">
  <thead>
    <tr>
      <th style="width: 25%;">To Do (Sprint Backlog)</th>
      <th style="width: 25%;">In Progress (WIP = 4)</th>
      <th style="width: 25%;">Code Review &amp; QA (WIP = 4)</th>
      <th style="width: 25%;">Done (Cumple DoD 100%)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        Tareas planificadas y priorizadas para el Sprint actual que aún no han sido iniciadas por los desarrolladores.
      </td>
      <td>
        <strong>Límite estricto de 4 tareas simultáneas</strong> (una por Developer) para fomentar el enfoque y evitar el desperdicio por multitarea.
      </td>
      <td>
        Revisión cruzada obligatoria de Pull Request por al menos dos pares. Ejecución de suites automatizadas de pruebas en el pipeline CI/CD.
      </td>
      <td>
        Ítems que cumplen estrictamente todos los criterios de la <strong>Definition of Done</strong> y están listos para producción.
      </td>
    </tr>
  </tbody>
</table>

<div class="box-note">
  <strong>Compromiso: Definition of Done (DoD) Formal del Scrum Team:</strong><br>
  Un elemento del Backlog se considera formalmente <em>"Terminado" (Done)</em> únicamente cuando:
  <ol>
    <li>El código fuente ha sido integrado a la rama principal mediante Pull Request aprobado por al menos 2 Developers.</li>
    <li>Cumple con el estándar de codificación limpio, sin advertencias de linter y tipado estricto en TypeScript.</li>
    <li>Cuenta con pruebas unitarias en Jest con una cobertura de código mínima del 80% en lógica de negocio.</li>
    <li>Pasa satisfactoriamente las pruebas de integración y flujos E2E automatizados en Playwright.</li>
    <li>La documentación técnica de la API en Swagger/OpenAPI ha sido generada y validada.</li>
    <li>Ha sido desplegado y verificado satisfactoriamente en el entorno de Staging/Pre-producción.</li>
  </ol>
</div>

<!-- SECCIÓN 6: ESTIMACIÓN COCOMO INTERMEDIO -->
<div class="page-break"></div>
<h2 class="section-title">6. Estimación Paramétrica del Proyecto mediante el Modelo COCOMO Intermedio</h2>

<p>
El modelo <strong>COCOMO Intermedio</strong> (<em>Constructive Cost Model</em>, Boehm, 1981) es un estándar matemático y paramétrico de la ingeniería de software diseñado para calcular el esfuerzo, el tiempo y el personal necesario para completar un sistema en función de su tamaño estimado en miles de líneas de código fuente (KLOC) y quince factores de ajuste (<em>Cost Drivers</em>).
</p>

<h3 class="subsection-title">6.1. Justificación Rigurosa del Modo de Desarrollo: Semidesarrollado (Semi-Detached)</h3>

<p>
Siguiendo las pautas de Boehm (1981), el proyecto de TechSolutions se clasifica formalmente en el modo <strong>Semidesarrollado (*Semi-Detached*)</strong> debido a la concurrencia de los siguientes factores técnicos y organizacionales:
</p>

<ul>
  <li>
    <strong>Requerimientos Mixtos en Grado de Rigidez:</strong> El sistema contiene módulos con requerimientos sumamente estrictos e inflexibles (el módulo de Kardex exige consistencia transaccional ACID pura y la facturación electrónica CFDI 4.0 está atada a normativas fiscales inmutables del SAT), combinados con módulos altamente flexibles y adaptativos (la interfaz visual de usuario, el Punto de Venta web y los tableros analíticos gerenciales configurables).
  </li>
  <li>
    <strong>Experiencia Heterogénea del Personal:</strong> El equipo técnico posee un nivel sobresaliente de dominio en tecnologías web modernas (Vue 3, TypeScript, PostgreSQL), pero cuenta con una experiencia moderada o en desarrollo respecto a las reglas de negocio específicas y dinámicas operativas internas de la empresa TechSolutions.
  </li>
  <li>
    <strong>Dimensión y Restricciones del Software:</strong> Con un tamaño de <strong>60 KLOC</strong>, el sistema supera la cota típica del modo orgánico (&le; 50 KLOC), pero no opera bajo las limitaciones de hardware en tiempo real extremas propias del modo empotrado (*Embedded*).
  </li>
</ul>

<h3 class="subsection-title">6.2. Coeficientes y Ecuaciones del Modelo</h3>

<p>
Para el modo <em>Semidesarrollado</em>, las constantes matemáticas de calibración empírica definidas por Boehm (1981) son:
</p>

<div class="math-block">
  <div class="math-formula">a = 3.0 &emsp;|&emsp; b = 1.12 &emsp;|&emsp; c = 2.5 &emsp;|&emsp; d = 0.35</div>
  <div class="math-desc">Tama&ntilde;o del software: S = 60 KLOC (60,000 l&iacute;neas l&oacute;gicas de c&oacute;digo fuente).</div>
</div>

<p>
Las ecuaciones fundamentales para el esfuerzo nominal ($E_{\text{nominal}}$), esfuerzo ajustado ($E$), tiempo calendario de desarrollo ($T_{\text{dev}}$) y personal promedio ($N$) son:
</p>

<div class="math-block">
  <div class="math-formula">E_{\text{nominal}} = a \cdot (\text{KLOC})^b</div>
  <div class="math-formula">E = E_{\text{nominal}} \cdot \text{EAF} \quad [\text{Personas-Mes (PM)}]</div>
  <div class="math-formula">T_{\text{dev}} = c \cdot (E)^d \quad [\text{Meses calendarios}]</div>
  <div class="math-formula">N = \frac{E}{T_{\text{dev}}} \quad [\text{Personas requeridas}]</div>
</div>

<h3 class="subsection-title">6.3. Cálculo del Esfuerzo Nominal</h3>

<p>
Sustituyendo el tamaño $S = 60\text{ KLOC}$ en la ecuación de esfuerzo nominal:
</p>

<div class="math-block">
  <div class="math-formula">E_{\text{nominal}} = 3.0 \cdot (60)^{1.12}</div>
  <div class="math-desc">
    C&aacute;lculo anal&iacute;tico: ln(60) &asymp; 4.09434456 &implies; 1.12 &times; 4.09434456 &asymp; 4.5856659 &implies; e^{4.5856659} = 60^{1.12} &asymp; 98.0707<br>
    <strong>E_{\text{nominal}} = 3.0 &times; 98.0707 = 294.21 Personas-Mes (PM)</strong>
  </div>
</div>

<h3 class="subsection-title">6.4. Evaluación de los Quince (15) Factores de Ajuste de Costo (Cost Drivers)</h3>

<p>
A continuación, se detalla la ponderación justificada de los quince conductores de costo para el proyecto TechSolutions, divididos en las cuatro categorías estándar de Boehm (1981):
</p>

<table class="formal-table">
  <thead>
    <tr>
      <th style="width: 15%;">Categoría</th>
      <th style="width: 10%;">Factor</th>
      <th style="width: 35%;">Descripción del Conductor</th>
      <th style="width: 15%; text-align: center;">Calificación</th>
      <th style="width: 10%; text-align: center;">Multiplicador</th>
      <th style="width: 15%;">Justificación Técnica en TechSolutions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="3" class="font-bold">Atributos del Producto</td>
      <td class="font-bold">RELY</td>
      <td>Fiabilidad requerida del software</td>
      <td class="text-center">Alto</td>
      <td class="text-center font-bold">1.15</td>
      <td>Fallas en inventario o ventas generan pérdidas financieras y fiscales.</td>
    </tr>
    <tr>
      <td class="font-bold">DATA</td>
      <td>Tamaño de la base de datos (D/P)</td>
      <td class="text-center">Alto</td>
      <td class="text-center font-bold">1.08</td>
      <td>Volumen de datos de transacciones comerciales supera los 100 bytes/LOC.</td>
    </tr>
    <tr>
      <td class="font-bold">CPLX</td>
      <td>Complejidad del producto</td>
      <td class="text-center">Alto</td>
      <td class="text-center font-bold">1.15</td>
      <td>Algoritmos de kardex, transacciones concurrentes y timbrado digital.</td>
    </tr>
    <tr>
      <td rowspan="4" class="font-bold">Atributos de Plataforma</td>
      <td class="font-bold">TIME</td>
      <td>Restricción de tiempo de ejecución</td>
      <td class="text-center">Nominal</td>
      <td class="text-center font-bold">1.00</td>
      <td>Uso de CPU previsto menor al 50% de la capacidad disponible en la nube.</td>
    </tr>
    <tr>
      <td class="font-bold">STOR</td>
      <td>Restricción de memoria principal</td>
      <td class="text-center">Nominal</td>
      <td class="text-center font-bold">1.00</td>
      <td>No existen restricciones severas de memoria en la infraestructura cloud.</td>
    </tr>
    <tr>
      <td class="font-bold">VIRT</td>
      <td>Volatilidad de la máquina virtual</td>
      <td class="text-center">Bajo</td>
      <td class="text-center font-bold">0.87</td>
      <td>Entorno de producción estable en contenedores Docker sobre Linux LTS.</td>
    </tr>
    <tr>
      <td class="font-bold">TURN</td>
      <td>Tiempo de respuesta del computador</td>
      <td class="text-center">Bajo</td>
      <td class="text-center font-bold">0.87</td>
      <td>Tiempos de respuesta inmediatos con Vite local y pipelines CI/CD rápidos.</td>
    </tr>
    <tr>
      <td rowspan="5" class="font-bold">Atributos del Personal</td>
      <td class="font-bold">ACAP</td>
      <td>Capacidad del analista de sistemas</td>
      <td class="text-center">Alto</td>
      <td class="text-center font-bold">0.86</td>
      <td>Analistas con amplia capacidad para modelar requerimientos complejos.</td>
    </tr>
    <tr>
      <td class="font-bold">AEXP</td>
      <td>Experiencia en la aplicación</td>
      <td class="text-center">Nominal</td>
      <td class="text-center font-bold">1.00</td>
      <td>Experiencia media del equipo en desarrollo de sistemas ERP comerciales.</td>
    </tr>
    <tr>
      <td class="font-bold">PCAP</td>
      <td>Capacidad de los programadores</td>
      <td class="text-center">Alto</td>
      <td class="text-center font-bold">0.86</td>
      <td>Programadores altamente calificados en TypeScript, Vue 3 y SQL.</td>
    </tr>
    <tr>
      <td class="font-bold">VEXP</td>
      <td>Experiencia en plataforma virtual</td>
      <td class="text-center">Nominal</td>
      <td class="text-center font-bold">1.00</td>
      <td>Familiaridad estándar de 1 a 3 años en ecosistemas cloud y Linux.</td>
    </tr>
    <tr>
      <td class="font-bold">LEXP</td>
      <td>Experiencia en el lenguaje</td>
      <td class="text-center">Alto</td>
      <td class="text-center font-bold">0.95</td>
      <td>Más de 2 años de experiencia continua en TypeScript, Node.js y SQL.</td>
    </tr>
    <tr>
      <td rowspan="3" class="font-bold">Atributos del Proyecto</td>
      <td class="font-bold">MODP</td>
      <td>Prácticas modernas de programación</td>
      <td class="text-center">Alto</td>
      <td class="text-center font-bold">0.91</td>
      <td>Adopción rigurosa de Clean Architecture, TDD y revisiones de código.</td>
    </tr>
    <tr>
      <td class="font-bold">TOOL</td>
      <td>Uso de herramientas de software</td>
      <td class="text-center">Alto</td>
      <td class="text-center font-bold">0.91</td>
      <td>Uso integral de IDEs avanzados, linters, profiling y Docker containers.</td>
    </tr>
    <tr>
      <td class="font-bold">SCED</td>
      <td>Restricción en el cronograma</td>
      <td class="text-center">Nominal</td>
      <td class="text-center font-bold">1.00</td>
      <td>Cronograma de desarrollo planificado sin compresión forzada de plazos.</td>
    </tr>
  </tbody>
</table>

<h3 class="subsection-title">6.5. Cálculo del Factor de Ajuste del Esfuerzo (EAF) y Esfuerzo Ajustado</h3>

<p>
El multiplicador acumulado de ajuste del esfuerzo (EAF) se calcula mediante el producto de los quince factores:
</p>

<div class="math-block">
  <div class="math-formula">
    EAF = &prod;_{i=1}^{15} F_i = (1.15 &times; 1.08 &times; 1.15) &times; (1.00 &times; 1.00 &times; 0.87 &times; 0.87) &times; (0.86 &times; 1.00 &times; 0.86 &times; 1.00 &times; 0.95) &times; (0.91 &times; 0.91 &times; 1.00)
  </div>
  <div class="math-desc">
    Desglose por grupos:<br>
    Producto: 1.15 &times; 1.08 &times; 1.15 = 1.4283 &emsp;|&emsp; Plataforma: 0.87 &times; 0.87 = 0.7569<br>
    Personal: 0.86 &times; 0.86 &times; 0.95 = 0.70262 &emsp;|&emsp; Proyecto: 0.91 &times; 0.91 = 0.8281<br>
    <strong>EAF = 1.4283 &times; 0.7569 &times; 0.70262 &times; 0.8281 &asymp; 0.6290 (Reducción del 37.1% del esfuerzo nominal)</strong>
  </div>
</div>

<p>
Aplicando el factor de ajuste sobre el esfuerzo nominal:
</p>

<div class="math-block">
  <div class="math-formula">E = E_{\text{nominal}} \cdot \text{EAF} = 294.21 \cdot 0.6290 = 185.06 \text{ Personas-Mes (PM)}</div>
</div>

<h3 class="subsection-title">6.6. Cálculo del Tiempo de Desarrollo, Personal Requerido y Productividad</h3>

<p>
A partir del esfuerzo ajustado de $185.06\text{ PM}$, se calcula el tiempo de desarrollo calendario estimado ($T_{\text{dev}}$):
</p>

<div class="math-block">
  <div class="math-formula">T_{\text{dev}} = c \cdot (E)^d = 2.5 \cdot (185.06)^{0.35}</div>
  <div class="math-desc">
    C&aacute;lculo anal&iacute;tico: ln(185.06) &asymp; 5.22068 &implies; 0.35 &times; 5.22068 &asymp; 1.82724 &implies; e^{1.82724} = (185.06)^{0.35} &asymp; 6.2163<br>
    <strong>T_{\text{dev}} = 2.5 &times; 6.2163 = 15.54 Meses calendarios</strong>
  </div>
</div>

<p>
El personal promedio requerido a lo largo de los 15.54 meses de desarrollo es:
</p>

<div class="math-block">
  <div class="math-formula">N = \frac{E}{T_{\text{dev}}} = \frac{185.06 \text{ PM}}{15.54 \text{ meses}} = 11.91 \approx 12 \text{ Ingenieros a tiempo completo}</div>
</div>

<p>
La productividad media resultante esperada para el proyecto bajo las condiciones evaluadas es:
</p>

<div class="math-block">
  <div class="math-formula">Productividad = \frac{60,000 \text{ LOC}}{185.06 \text{ PM}} = 324.22 \text{ LOC por Persona-Mes}</div>
  <div class="math-desc">Equivalente a aproximadamente 2.03 LOC netas terminadas y probadas por hora de trabajo.</div>
</div>

<!-- SECCIÓN 7: REFLEXIÓN COMPARATIVA -->
<div class="page-break"></div>
<h2 class="section-title">7. Reflexión Comparativa: SCRUM vs. Modelo COCOMO Intermedio</h2>

<p>
El análisis comparativo entre la planeación ágil mediante <strong>SCRUM</strong> y la estimación algorítmica con <strong>COCOMO Intermedio</strong> permite evidenciar dos filosofías complementarias en la gestión moderna de la ingeniería de software (Pressman & Maxim, 2020).
</p>

<table class="formal-table">
  <thead>
    <tr>
      <th style="width: 20%;">Criterio de Comparación</th>
      <th style="width: 40%;">Marco Ágil SCRUM (Schwaber &amp; Sutherland, 2020)</th>
      <th style="width: 40%;">Modelo COCOMO Intermedio (Boehm, 1981)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="font-bold">Paradigma Central</td>
      <td>Empírico y adaptativo. Se basa en inspección, adaptación y transparencia en ciclos cortos.</td>
      <td>Predictivo y paramétrico. Se fundamenta en regresiones estadísticas y datos históricos de proyectos.</td>
    </tr>
    <tr>
      <td class="font-bold">Unidad de Medida</td>
      <td>Story Points (SP) y horas ideales de esfuerzo relativo para tareas técnicas.</td>
      <td>Líneas de código entregadas (KLOC), Personas-Mes (PM) y meses calendarios.</td>
    </tr>
    <tr>
      <td class="font-bold">Horizonte Temporal</td>
      <td>Cadencia de corto plazo (Sprints fijos de 2 semanas) con metas tácticas claras.</td>
      <td>Proyección de ciclo de vida completo a mediano/largo plazo (15.54 meses).</td>
    </tr>
    <tr>
      <td class="font-bold">Gestión de Requerimientos</td>
      <td>Abierto al cambio continuo. El Product Backlog es emergente y se reordena según valor.</td>
      <td>Asume alcance y tamaño definidos preliminarmente para proyectar costos y contratos.</td>
    </tr>
    <tr>
      <td class="font-bold">Mitigación del Riesgo</td>
      <td>Temprana, mediante entregas frecuentes de software funcional inspeccionable cada 2 semanas.</td>
      <td>Financiera y de dotación, mediante dimensionamiento formal de personal y presupuesto global.</td>
    </tr>
    <tr>
      <td class="font-bold">Participación del Cliente</td>
      <td>Constante y colaborativa en cada Sprint Planning, Review y refinamiento del Backlog.</td>
      <td>Enfocada en la fase inicial de licitación, negociación contractual y cierre de hitos mayores.</td>
    </tr>
  </tbody>
</table>

<h3 class="subsection-title">7.1. Reconciliación de la Brecha de Esfuerzo (8 Semanas vs. 15.54 Meses)</h3>

<p>
Una observación analítica fundamental radica en la aparente discrepancia numérica entre la planificación Scrum (4 Sprints de 2 semanas con 4 desarrolladores = 960 horas &asymp; 6 Personas-Mes) y el resultado de COCOMO Intermedio (185.06 Personas-Mes, 15.54 meses con 12 personas). Lejos de representar un error de cálculo, esta diferencia ilustra con precisión dos niveles de abstracción:
</p>

<ol>
  <li>
    <strong>Diferenciación de Alcance (Fase 1 MVP vs. Ciclo Enterprise Total):</strong><br>
    La planificación Scrum presentada abarca la <strong>Fase 1: Minimum Viable Product (MVP) / Core Release</strong>. En ella, un equipo compacto de 4 ingenieros construye el núcleo crítico operativo (104 Story Points, estimado en 12 a 15 KLOC), logrando que TechSolutions empiece a operar su catálogo, kardex, punto de venta y reportes esenciales al concluir el Sprint 3 y 4. En contraste, COCOMO modela la totalidad del sistema enterprise (60 KLOC), el cual requerirá entre 24 y 28 Sprints adicionales para abarcar contabilidad electrónica automatizada, facturación multirregión, integraciones bancarias, migración de datos históricos, arquitectura de alta disponibilidad y auditorías de seguridad forense.
  </li>
  <li>
    <strong>El Cono de Incertidumbre (Boehm, 1981):</strong><br>
    Al inicio de un proyecto, la incertidumbre sobre el alcance real puede variar hasta en un factor de $4\times$. La estimación COCOMO otorga una frontera presupuestal macro, mientras que Scrum mitiga activamente el Cono de Incertidumbre al reducir el desperdicio: las funcionalidades secundarias que el cliente decida no implementar tras inspeccionar el MVP en producción evitarán el gasto de líneas de código innecesarias.
  </li>
</ol>

<h3 class="subsection-title">7.2. Recomendación de Gobernanza: Enfoque Híbrido Ágil-Paramétrico</h3>

<p>
Para proyectos tecnológicos de la escala de TechSolutions, la mejor práctica de la ingeniería de software contemporánea consiste en articular un <strong>modelo híbrido</strong>:
</p>

<ul>
  <li>
    <strong>Gobernanza Financiera con COCOMO:</strong> La dirección de la empresa utiliza COCOMO Intermedio como herramienta formal para calcular la viabilidad económica, comprometer presupuestos plurianuales ante comités de inversión y estimar los recursos de infraestructura necesarios (185 PM).
  </li>
  <li>
    <strong>Ejecución Operativa con SCRUM:</strong> El equipo de ingeniería adopta Scrum para construir el producto de forma iterativa e incremental, protegiendo al negocio mediante entregas tempranas de valor tangible (MVP en Sprint 3), calidad certificada mediante la Definition of Done y capacidad de pivotar ante cambios del mercado.
  </li>
</ul>

<!-- SECCIÓN 8: REFERENCIAS BIBLIOGRÁFICAS -->
<h2 class="section-title">8. Referencias Bibliográficas (Formato APA 7)</h2>

<div class="reference-item">
  Boehm, B. W. (1981). <em>Software Engineering Economics</em>. Prentice-Hall.
</div>

<div class="reference-item">
  Cohn, M. (2005). <em>Agile Estimating and Planning</em>. Prentice Hall PTR.
</div>

<div class="reference-item">
  Pressman, R. S., &amp; Maxim, B. R. (2020). <em>Software Engineering: A Practitioner's Approach</em> (9.ª ed.). McGraw-Hill Education.
</div>

<div class="reference-item">
  Schwaber, K., &amp; Sutherland, J. (2020). <em>The Scrum Guide: The Definitive Guide to Scrum: The Rules of the Game</em>. Scrum.org. https://scrumguides.org/
</div>

<div class="reference-item">
  Sommerville, I. (2016). <em>Software Engineering</em> (10.ª ed.). Pearson.
</div>

</body>
</html>
"""

html_path = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_3_2_SCRUM_COCOMO_TechSolutions.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML generado exitosamente en: {html_path}")

# Compilacion con Chrome Headless
pdf_path_repo = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_3_2_SCRUM_COCOMO_TechSolutions.pdf"
pdf_path_downloads = r"C:\Users\erfierro\Downloads\Actividad_3_2_SCRUM_COCOMO_TechSolutions.pdf"

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path_repo}",
    html_path
]

print("Compilando PDF con Chrome Headless...")
subprocess.run(cmd, check=True)
print(f"PDF generado exitosamente en repositorio: {pdf_path_repo}")

# Copiar a Descargas
shutil.copyfile(pdf_path_repo, pdf_path_downloads)
print(f"PDF copiado exitosamente a Descargas: {pdf_path_downloads}")
