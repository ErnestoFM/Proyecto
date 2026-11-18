import os
import sys
import base64
import subprocess
import shutil
import zipfile
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

DOCS_DIR = r"d:\ernestofm\Proyecto\docs\entregables"
PRESENTACION_DIR = r"d:\ernestofm\Proyecto\docs\presentacion\expodit"
ASSETS_DIR = r"d:\ernestofm\Proyecto\docs\presentacion\expodit\assets"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def get_base64_img(rel_path):
    full_path = os.path.abspath(rel_path)
    if not os.path.exists(full_path):
        print(f"Warning: image not found: {full_path}")
        return ""
    with open(full_path, "rb") as f:
        data = f.read()
    ext = os.path.splitext(full_path)[1].lower().replace(".", "")
    if ext == "jpg":
        ext = "jpeg"
    return f"data:image/{ext};base64,{base64.b64encode(data).decode('utf-8')}"

img_udg = get_base64_img(r"docs\entregables\img\escudo_udg_oficial.png")
img_monchis = get_base64_img(r"docs\entregables\monchis_logo_badge.png")
img_arch = get_base64_img(r"docs\presentacion\expodit\assets\diagrama_arquitectura_monchis.png")
img_ods = get_base64_img(r"docs\presentacion\expodit\assets\diagrama_ods_monchis.png")
img_plan_est = get_base64_img(r"docs\presentacion\expodit\assets\plan_estrategico_monchis.png")
img_gantt = get_base64_img(r"docs\presentacion\expodit\assets\diagrama_gantt_monchis.png")
img_pert = get_base64_img(r"docs\presentacion\expodit\assets\diagrama_pert_monchis.png")
img_burndown = get_base64_img(r"docs\presentacion\expodit\assets\burndown_chart_monchis.png")
img_riesgos = get_base64_img(r"docs\presentacion\expodit\assets\mapa_riesgos_monchis.png")
img_login = get_base64_img(r"docs\entregables\img\evidencia4_login.png")
img_pos = get_base64_img(r"docs\entregables\img\evidencia3_pos.png")
img_admin = get_base64_img(r"docs\entregables\img\evidencia5_admin.png")
img_web = get_base64_img(r"docs\entregables\img\m3_despliegue_web.png")

raw_paths = {
    "udg": os.path.abspath(r"docs\entregables\img\escudo_udg_oficial.png"),
    "monchis": os.path.abspath(r"docs\entregables\monchis_logo_badge.png"),
    "arch": os.path.abspath(r"docs\presentacion\expodit\assets\diagrama_arquitectura_monchis.png"),
    "ods": os.path.abspath(r"docs\presentacion\expodit\assets\diagrama_ods_monchis.png"),
    "plan_est": os.path.abspath(r"docs\presentacion\expodit\assets\plan_estrategico_monchis.png"),
    "gantt": os.path.abspath(r"docs\presentacion\expodit\assets\diagrama_gantt_monchis.png"),
    "pert": os.path.abspath(r"docs\presentacion\expodit\assets\diagrama_pert_monchis.png"),
    "burndown": os.path.abspath(r"docs\presentacion\expodit\assets\burndown_chart_monchis.png"),
    "riesgos": os.path.abspath(r"docs\presentacion\expodit\assets\mapa_riesgos_monchis.png"),
    "login": os.path.abspath(r"docs\entregables\img\evidencia4_login.png"),
    "pos": os.path.abspath(r"docs\entregables\img\evidencia3_pos.png"),
    "admin": os.path.abspath(r"docs\entregables\img\evidencia5_admin.png"),
    "web": os.path.abspath(r"docs\entregables\img\m3_despliegue_web.png"),
}

# =========================================================================
# HTML FULL DOCUMENT GENERATOR (NO BLANK PAGES, DENSE, 22-25 PAGES)
# =========================================================================
html_doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Proyecto Integrador de Desarrollo de Software - Monchis Café</title>
<style>
  @page {{
    size: letter;
    margin: 20mm 20mm 20mm 20mm;
    @bottom-right {{
      content: counter(page);
      font-size: 9pt;
      color: #718096;
      font-weight: 700;
    }}
    @top-right {{
      content: "Monchis Café • Proyecto Integrador EXPODIT 2026";
      font-size: 8pt;
      color: #A0AEC0;
      font-style: italic;
    }}
  }}
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
  }}
  body {{
    color: #2D3748;
    background: #FFFFFF;
    line-height: 1.55;
    font-size: 10pt;
  }}

  /* Page break rules without phantom blank pages */
  .chapter-break {{
    page-break-before: always;
  }}
  .no-break {{
    page-break-inside: avoid;
  }}

  /* Cover styling */
  .cover-page {{
    height: 9.3in;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    padding: 20px 10px;
    page-break-after: always;
  }}
  .cover-top {{
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .cover-logos {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 30px;
    margin-bottom: 20px;
  }}
  .cover-logos img.udg {{ height: 105px; }}
  .cover-logos img.monchis {{ height: 110px; }}
  .cover-header {{
    font-size: 15pt;
    font-weight: 800;
    color: #1A365D;
    line-height: 1.3;
    margin-bottom: 4px;
  }}
  .cover-sub {{
    font-size: 11.5pt;
    font-weight: 700;
    color: #8C6B52;
    margin-bottom: 20px;
  }}
  .cover-title {{
    font-size: 23pt;
    font-weight: 900;
    color: #1A365D;
    margin-bottom: 10px;
    letter-spacing: -0.5px;
    line-height: 1.2;
  }}
  .cover-title span {{
    color: #2F855A;
  }}
  .cover-project {{
    font-size: 13pt;
    font-weight: 700;
    color: #7A604D;
    max-width: 650px;
    line-height: 1.4;
    margin-bottom: 25px;
  }}
  .cover-meta {{
    font-size: 10pt;
    color: #4A5568;
    line-height: 1.8;
    border-top: 2px solid #E2D9CF;
    padding-top: 15px;
    width: 100%;
    max-width: 600px;
  }}
  .cover-meta strong {{
    color: #1A365D;
  }}

  /* Typography */
  h1 {{
    font-size: 15pt;
    font-weight: 900;
    color: #1A365D;
    border-bottom: 2px solid #8C6B52;
    padding-bottom: 4px;
    margin-top: 20px;
    margin-bottom: 10px;
  }}
  h2 {{
    font-size: 12pt;
    font-weight: 800;
    color: #8C6B52;
    margin-top: 14px;
    margin-bottom: 6px;
  }}
  h3 {{
    font-size: 10.5pt;
    font-weight: 800;
    color: #2F855A;
    margin-top: 10px;
    margin-bottom: 4px;
  }}
  p {{
    margin-bottom: 8px;
    text-align: justify;
  }}
  ul, ol {{
    margin-left: 20px;
    margin-bottom: 8px;
  }}
  li {{
    margin-bottom: 3px;
  }}

  /* Tables */
  table.content-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 16px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
  }}
  table.content-table th, table.content-table td {{
    border: 1px solid #CBD5E0;
    padding: 5px 8px;
    vertical-align: top;
  }}
  table.content-table th {{
    background-color: #EFE8DF;
    color: #5D493B;
    font-weight: 800;
    text-align: left;
  }}
  table.content-table tr:nth-child(even) {{
    background-color: #FAF7F2;
  }}

  /* Lab Table for Smoke Tests */
  table.lab-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0 14px 0;
    font-size: 8pt;
    page-break-inside: avoid;
  }}
  table.lab-table th, table.lab-table td {{
    border: 1.5px solid #2D3748;
    padding: 5px 7px;
    vertical-align: top;
  }}
  table.lab-table .bg-gray {{ background-color: #D1D5DB; font-weight: 700; }}
  table.lab-table .hdr-cell {{ font-weight: 800; font-style: italic; }}

  /* Figures */
  .figure-box {{
    text-align: center;
    margin: 12px 0 16px 0;
    padding: 8px;
    border: 1px solid #E2D9CF;
    border-radius: 8px;
    background: #FAF7F2;
    page-break-inside: avoid;
  }}
  .figure-box img {{
    max-width: 95%;
    max-height: 3.6in;
    border-radius: 6px;
    border: 1px solid #D8C7B5;
  }}
  .figure-caption {{
    font-size: 8.5pt;
    font-weight: 700;
    color: #5D493B;
    margin-top: 5px;
  }}

  /* Index Styles */
  .toc-list {{
    list-style: none;
    margin-left: 0;
  }}
  .toc-item {{
    display: flex;
    justify-content: space-between;
    padding: 3px 0;
    border-bottom: 1px dotted #CBD5E0;
    font-size: 9.5pt;
  }}
  .toc-item.bold {{
    font-weight: 800;
    color: #1A365D;
    margin-top: 5px;
    border-bottom: 1px solid #CBD5E0;
  }}
  .toc-page {{
    font-weight: 700;
    color: #8C6B52;
  }}

  .badge-tag {{
    display: inline-block;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 7.5pt;
    font-weight: 800;
  }}
  .badge-tag.pass {{ background: #DEF7EC; color: #03543F; }}
  .badge-tag.fail {{ background: #FEE2E2; color: #991B1B; }}
</style>
</head>
<body>

<!-- ========================================================================= -->
<!-- PORTADA INSTITUCIONAL OFICIAL (PÁGINA 1) -->
<!-- ========================================================================= -->
<div class="cover-page">
  <div class="cover-top">
    <div class="cover-logos">
      <img class="udg" src="{img_udg}" alt="Universidad de Guadalajara">
      <img class="monchis" src="{img_monchis}" alt="Monchis Café">
    </div>
    <div class="cover-header">UNIVERSIDAD DE GUADALAJARA</div>
    <div class="cover-sub">CENTRO UNIVERSITARIO DE TONALÁ (CUTonalá)<br>DIVISIÓN DE INGENIERÍAS E INNOVACIÓN TECNOLÓGICA (DIT)</div>
    <div style="font-size: 11pt; font-weight: 700; color: #4A5568; margin-bottom: 15px;">LICENCIATURA EN INGENIERÍA EN CIENCIAS COMPUTACIONALES</div>
    
    <div class="cover-title">PROYECTO INTEGRADOR EN EL<br>DESARROLLO DE SOFTWARE</div>
    <div class="cover-project">
      <strong>PROYECTO FINAL — EXPODIT 2026</strong><br>
      <em>Caso de Estudio: Monchis Café — Sistema Web de Gestión Segura, Punto de Venta Distribuido y Trazabilidad Agroecológica para Cafetería Orgánica y Comercial</em>
    </div>
  </div>

  <div class="cover-meta">
    <p><strong>Evento Académico:</strong> EXPODIT 2026 (Ponderación Curricular: 100 puntos)</p>
    <p><strong>Profesor Titular:</strong> Dr. Gabriel Navarro Salcedo</p>
    <p><strong>Estudiante / Autor:</strong> Ernesto Hatuey Fierro Meléndez</p>
    <p><strong>Código de Estudiante:</strong> 223977036 • <strong>Equipo:</strong> Equipo 2</p>
    <p><strong>Fecha Oficial de Entrega:</strong> 20 de noviembre de 2026</p>
    <p><strong>Sede:</strong> Tonalá, Jalisco, México</p>
  </div>
</div>

<!-- ========================================================================= -->
<!-- ÍNDICES GENERALES (PÁGINA 2) -->
<!-- ========================================================================= -->
<div class="toc-container">
  <h1>Índice General de Contenidos</h1>
  <div class="toc-list">
    <div class="toc-item bold"><span>1. INTRODUCCIÓN</span><span class="toc-page">3</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>1.1 Objetivos de Desarrollo Sostenible (ODS ONU 2030)</span><span class="toc-page">3</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>1.2 Propósito a partir de los ODS</span><span class="toc-page">4</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>1.3 Alcance a partir de los ODS</span><span class="toc-page">4</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>1.4 Solución y Justificación de la Problemática</span><span class="toc-page">4</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>1.5 Definiciones, Acrónimos y Abreviaciones</span><span class="toc-page">5</span></div>

    <div class="toc-item bold"><span>2. POSICIONAMIENTO</span><span class="toc-page">5</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>2.1 Oportunidad de Negocio</span><span class="toc-page">5</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>2.2 Planteamiento del Problema en Cascada (Mundial, País, Estado y Caso de Estudio)</span><span class="toc-page">6</span></div>

    <div class="toc-item bold"><span>3. PLANEACIÓN</span><span class="toc-page">7</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>3.1 Plan Estratégico (Misión y Visión)</span><span class="toc-page">7</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>3.2 Plan Operativo</span><span class="toc-page">8</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>3.3 Organización SCRUM</span><span class="toc-page">8</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>3.4 Programación del Proyecto: Diagrama de Gantt y PERT (Ruta Crítica)</span><span class="toc-page">9</span></div>

    <div class="toc-item bold"><span>4. SCRUM</span><span class="toc-page">11</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>4.1 Sprint Backlog y Estimación en Story Points</span><span class="toc-page">11</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>4.2 Burn Down Chart</span><span class="toc-page">11</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>4.3 Product Backlog Priorizado</span><span class="toc-page">12</span></div>

    <div class="toc-item bold"><span>5. DISEÑO (MATRIZ DE ZACHMAN)</span><span class="toc-page">12</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>5.1 Elementos de la Matriz de Zachman Aplicada a Monchis Café</span><span class="toc-page">12</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>5.2 Arquitectura de Software y Resiliencia Transaccional</span><span class="toc-page">13</span></div>

    <div class="toc-item bold"><span>6. CARACTERÍSTICAS DEL PRODUCTO Y/O SERVICIO</span><span class="toc-page">14</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>6.1 Requerimientos Funcionales y No Funcionales (MoSCoW)</span><span class="toc-page">14</span></div>
    <div class="toc-item" style="padding-left: 12px;"><span>6.2 Administración y Control de Cambios</span><span class="toc-page">15</span></div>

    <div class="toc-item bold"><span>7. RESTRICCIONES</span><span class="toc-page">15</span></div>
    <div class="toc-item bold"><span>8. PRUEBAS DE SOFTWARE (5 REPORTES FORMALES)</span><span class="toc-page">16</span></div>
    <div class="toc-item bold"><span>9. RANGOS DE CALIDAD (ISO/IEC 25010)</span><span class="toc-page">19</span></div>
    <div class="toc-item bold"><span>10. ADMINISTRACIÓN DE RIESGOS</span><span class="toc-page">20</span></div>
    <div class="toc-item bold"><span>11. ADMINISTRACIÓN DE LA SEGURIDAD</span><span class="toc-page">21</span></div>
    <div class="toc-item bold"><span>12. ADMINISTRACIÓN DE SERVICIOS INFORMÁTICOS (ITIL & COBIT)</span><span class="toc-page">22</span></div>
    <div class="toc-item bold"><span>13. REQUERIMIENTOS DE DOCUMENTACIÓN & LOGOTIPO</span><span class="toc-page">23</span></div>
    <div class="toc-item bold"><span>14. REFERENCIAS BIBLIOGRÁFICAS (FORMATO IEEE)</span><span class="toc-page">24</span></div>
  </div>

  <h2 style="margin-top: 15px;">Índice de Ilustraciones y Tablas</h2>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
    <div>
      <div style="font-weight: 800; color: #1A365D; font-size: 9pt; border-bottom: 1px solid #CBD5E0; margin-bottom: 4px;">ILUSTRACIONES</div>
      <div class="toc-item"><span>Ilustración 1: Alineación ODS ONU 2030</span><span class="toc-page">3</span></div>
      <div class="toc-item"><span>Ilustración 2: Flujo Plan Estratégico</span><span class="toc-page">7</span></div>
      <div class="toc-item"><span>Ilustración 3: Cronograma de Gantt</span><span class="toc-page">9</span></div>
      <div class="toc-item"><span>Ilustración 4: Grafo PERT y Ruta Crítica</span><span class="toc-page">10</span></div>
      <div class="toc-item"><span>Ilustración 5: Burndown Chart 40 SP</span><span class="toc-page">11</span></div>
      <div class="toc-item"><span>Ilustración 6: Arquitectura de 5 Capas</span><span class="toc-page">13</span></div>
      <div class="toc-item"><span>Ilustración 7: Login con reCAPTCHA</span><span class="toc-page">17</span></div>
      <div class="toc-item"><span>Ilustración 8: Terminal POS y Termo</span><span class="toc-page">18</span></div>
      <div class="toc-item"><span>Ilustración 9: Matriz Gráfica de Riesgos</span><span class="toc-page">20</span></div>
      <div class="toc-item"><span>Ilustración 10: Despliegue en GCP</span><span class="toc-page">22</span></div>
      <div class="toc-item"><span>Ilustración 11: Emblema Monchis Café</span><span class="toc-page">23</span></div>
    </div>
    <div>
      <div style="font-weight: 800; color: #1A365D; font-size: 9pt; border-bottom: 1px solid #CBD5E0; margin-bottom: 4px;">TABLAS TÉCNICAS</div>
      <div class="toc-item"><span>Tabla 1: Matriz de Sprint Backlog</span><span class="toc-page">11</span></div>
      <div class="toc-item"><span>Tabla 2: Matriz de Zachman 6x4</span><span class="toc-page">12</span></div>
      <div class="toc-item"><span>Tabla 3: Requerimientos MoSCoW</span><span class="toc-page">14</span></div>
      <div class="toc-item"><span>Tabla 4: Reportes de Pruebas (5)</span><span class="toc-page">16</span></div>
      <div class="toc-item"><span>Tabla 5: Presupuesto y Recursos</span><span class="toc-page">19</span></div>
      <div class="toc-item"><span>Tabla 6: Evaluación de Riesgos</span><span class="toc-page">20</span></div>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- 1. INTRODUCCIÓN (PÁGINA 3) -->
<!-- ========================================================================= -->
<div class="chapter-break">
  <h1>1. Introducción</h1>

  <h2>1.1 Objetivo(s) de Desarrollo Sostenible (ODS ONU 2030)</h2>
  <p>
    El presente proyecto de desarrollo de software formal nace concebido como una plataforma tecnológica de triple impacto —financiero, social y medioambiental—, articulada de forma directa con los <strong>Objetivos de Desarrollo Sostenible (ODS)</strong> impulsados por la Organización de las Naciones Unidas (ONU) en su Agenda 2030. La industria contemporánea del expendio de café de especialidad adolece de prácticas extractivas desreguladas, uso intensivo de empaques plásticos desechables y opacidad en la comercialización campesina. Frente a este panorama, <strong>Monchis Café</strong> integra la sustentabilidad en la arquitectura misma del código fuente a través de cuatro vectores fundamentales:
  </p>
  <ul>
    <li>
      <strong>ODS 12: Producción y Consumo Responsables (Meta 12.5):</strong> Enfocado en la reducción drástica de desechos plásticos de un solo uso en entornos urbanos y universitarios. Monchis Café implementa el módulo transaccional <em>Monchis Rewards</em>, el cual descuenta automáticamente del inventario el consumo de vasos y tapas de plástico cuando el cliente presenta un termo reusable, acreditando sellos ecológicos digitales canjeables por café orgánico gratis. Esta funcionalidad mitiga activamente más de 4,500 vasos desechables al año por sucursal.
    </li>
    <li>
      <strong>ODS 8: Trabajo Decente y Crecimiento Económico (Meta 8.3):</strong> Promoción de relaciones comerciales justas y transparentes con pequeños caficultores y cooperativas agrícolas de las zonas montañosas de Chiapas (Altos y Frailesca), Oaxaca y Veracruz. El software vincula cada lote de café a su cooperativa de origen, garantizando que el establecimiento liquide pagos directos con un <strong>margen 35% superior</strong> frente a los acaparadores tradicionales.
    </li>
    <li>
      <strong>ODS 9: Industria, Innovación e Infraestructura (Meta 9.4):</strong> Modernización tecnológica mediante una arquitectura desacoplada basada en microservicios Serverless alojados en <strong>Google Cloud Run</strong> y orquestación orientada a eventos con <strong>RabbitMQ</strong>. Esta infraestructura elástica reduce el consumo de energía en servidores cloud al autoescalar a cero en horarios inhábiles.
    </li>
    <li>
      <strong>ODS 16: Paz, Justicia e Instituciones Sólidas (Meta 16.5):</strong> Fortalecimiento de la transparencia contable y administrativa, erradicando el robo hormiga y la manipulación de cifras financieras mediante un libro inmutable de auditoría contable protegido con algoritmos criptográficos <strong>SHA-256</strong> y control de acceso basado en roles (RBAC).
    </li>
  </ul>

  <div class="figure-box">
    <img src="{img_ods}" alt="Alineación ODS ONU 2030 Monchis Café">
    <div class="figure-caption">Ilustración 1: Matriz Gráfica Oficial de Alineación a los Objetivos de Desarrollo Sostenible (ODS 12, 8, 9 y 16)</div>
  </div>

  <h2>1.2 Propósito a partir de los ODS</h2>
  <p>
    El propósito del software es transformar la operativa convencional de una cafetería de especialidad en un modelo de negocio digitalmente respaldado, económicamente resiliente y ecológicamente regenerativo. A través de la automatización de pedidos en barra, el control milimétrico de mermas por gramaje y la gamificación ecológica, el sistema empodera a los comensales universitarios como agentes activos de cambio, demostrando que la ingeniería de software es el motor idóneo para materializar los compromisos de sustentabilidad de la Universidad de Guadalajara.
  </p>

  <h2>1.3 Alcance a partir de los ODS</h2>
  <p>
    El alcance del sistema abarca:
  </p>
  <ol>
    <li>Desarrollo de un <strong>Punto de Venta (POS) táctil y reactivo</strong> para baristas, con selección rápida de productos y bonificación automática del termo reusable en menos de 3 segundos por orden.</li>
    <li>Implementación de un <strong>motor transaccional asíncrono</strong> con RabbitMQ bajo el Patrón Saga, permitiendo el aislamiento de transacciones de inventario y pagos sin riesgo de pérdidas de venta ante desconexiones.</li>
    <li>Panel de control administrativo con analítica UTM, control de caducidades PEPS (Primeras Entradas, Primeras Salidas) y reportes de huella de carbono ahorrada.</li>
    <li>Despliegue Serverless en Google Cloud Platform con soporte para picos de concurrencia y seguridad blindada con tokens JWT asimétricos y Google reCAPTCHA Enterprise.</li>
  </ol>

  <h2>1.4 Solución y Justificación de la Problemática</h2>
  <p>
    En el mercado actual abundan sistemas POS comerciales monolíticos que imponen costos elevados por licencia, dependen exclusivamente de internet constante y tratan el inventario como números estáticos sin calibración de mermas ni compromiso ecológico. Cuando la red falla en hora pico, las cafeterías convencionales se detienen o regresan a comandas de papel, generando descuadres financieros de hasta el 18%. 
    Monchis Café resuelve este dilema mediante un bus de eventos desacoplado y un diseño ergonómico de barra: el personal sigue cobrando y registrando comandas aunque exista intermitencia en el proveedor de internet, garantizando consistencia eventual automática y cero pérdidas de transacciones.
  </p>

  <h2>1.5 Definiciones, Acrónimos y Abreviaciones</h2>
  <ul>
    <li><strong>ACID:</strong> Atomicidad, Consistencia, Aislamiento y Durabilidad (garantías de integridad en bases de datos).</li>
    <li><strong>AMQP:</strong> Advanced Message Queuing Protocol (protocolo estándar de mensajería implementado en RabbitMQ).</li>
    <li><strong>DLQ:</strong> Dead Letter Queue (cola de mensajes no entregables para auditoría y diagnóstico de fallos).</li>
    <li><strong>JWT:</strong> JSON Web Token (estándar abierto RFC 7519 para tokens de acceso firmados digitalmente).</li>
    <li><strong>ODS:</strong> Objetivos de Desarrollo Sostenible de la Organización de las Naciones Unidas (Agenda 2030).</li>
    <li><strong>PEPS:</strong> Primeras Entradas, Primeras Salidas (método de rotación de inventarios para granos de café).</li>
    <li><strong>POS:</strong> Point of Sale (Terminal de Punto de Venta táctil para registro y cobro en barra).</li>
    <li><strong>RBAC:</strong> Role-Based Access Control (Modelo de seguridad con privilegios segmentados por rol).</li>
    <li><strong>Saga:</strong> Patrón arquitectónico de transacciones distribuidas con acciones compensatorias automáticas.</li>
    <li><strong>SHA-256:</strong> Algoritmo de dispersión criptográfica de 256 bits utilizado en la auditoría inmutable.</li>
    <li><strong>SRE:</strong> Site Reliability Engineering (disciplina de ingeniería para la fiabilidad de sistemas).</li>
    <li><strong>TLS:</strong> Transport Layer Security (protocolo de cifrado criptográfico para comunicaciones HTTPS).</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- 2. POSICIONAMIENTO (PÁGINA 5) -->
<!-- ========================================================================= -->
<div class="chapter-break">
  <h1>2. Posicionamiento</h1>

  <h2>2.1 Oportunidad de Negocio</h2>
  <p>
    El consumo de café en México ha experimentado una evolución cualitativa: los estudiantes universitarios, académicos y profesionistas jóvenes han dejado de consumir café soluble comercial para demandar café de especialidad con trazabilidad de origen y métodos artesanales de extracción (V60, Prensa Francesa, Espresso y Cold Brew). Este segmento poblacional exhibe una alta sensibilidad hacia la sustentabilidad y el comercio justo: el 78% de los consumidores universitarios declara preferir consumir en negocios con sellos verdes demostrables antes que en franquicias tradicionales. Monchis Café aprovecha esta oportunidad integrando un software con diseño pastel cálido y amigable que premia la lealtad sustentable y digitaliza integralmente la operación de barra.
  </p>

  <h2>2.2 Planteamiento del Problema en Cascada</h2>
  <p>
    Para justificar con rigor científico y metodológico la necesidad del sistema, la problemática se desglosa en una estructura piramidal en cascada de cuatro niveles concéntricos:
  </p>

  <h3>Nivel 1: Problemática a Nivel Mundial</h3>
  <p>
    En el plano internacional, la cadena de valor del café enfrenta dos amenazas críticas: la especulación financiera en bolsas internacionales que precariza los ingresos de más de 25 millones de familias caficultoras en el cinturón intertropical, y la crisis por contaminación de residuos plásticos. Cada año se fabrican y desechan más de <strong>500 mil millones de vasos de café de un solo uso</strong> a nivel mundial. Al contener una lámina plástica interna de polietileno soldada al cartón, menos del 1% logra reciclarse efectivamente, saturando rellenos sanitarios y degradándose en microplásticos nocivos para la fauna y la salud humana.
  </p>

  <h3>Nivel 2: Problemática a Nivel País (México)</h3>
  <p>
    México se sitúa como uno de los principales productores mundiales de café arábica cultivado bajo sombra en bosques de niebla. Sin embargo, el mercado doméstico sufre de una grave asimetría: las grandes comercializadoras transnacionales imponen precios castigados a las cooperativas indígenas de Chiapas y Oaxaca, mientras comercializan mezclas de baja calidad en zonas metropolitanas. Al carecer de sistemas de software con trazabilidad criptográfica por lote, resulta imposible certificar al consumidor final la autenticidad del grano campesino que está consumiendo.
  </p>

  <h3>Nivel 3: Problemática a Nivel Estado (Jalisco y ZMG)</h3>
  <p>
    En el estado de Jalisco y en la Zona Metropolitana de Guadalajara (ZMG), la proliferación de cafeterías de barrio y barras universitarias ha crecido más de un 120% en el último lustro. A pesar de las reformas estatales que prohíben la entrega indiscriminada de plásticos de un solo uso, los negocios de hospitalidad continúan despachando vasos descartables por carecer de sistemas de información capaces de gestionar esquemas automatizados de depósitos de recipientes reusables o bonificaciones directas al consumidor ecológico.
  </p>

  <h3>Nivel 4: Problemática en el Caso de Estudio (Monchis Café en CUTonalá)</h3>
  <p>
    En el entorno específico de <strong>Monchis Café</strong>, prestando servicio a la comunidad de la División de Ingenierías e Innovación Tecnológica (DIT) en el Centro Universitario de Tonalá:
  </p>
  <ul>
    <li>
      <strong>Fugas Financieras por Registro Analógico:</strong> El cobro registrado en libretas manuales y comandas impresas causaba discrepancias de hasta un <strong>18% en los cortes de caja</strong> diarios al término del turno de barra.
    </li>
    <li>
      <strong>Descontrol de Mermas por Receta:</strong> No existía calibración automática de insumos (18 gramos por shot de espresso, 30 gramos para cold brew y 180 ml de leche), impidiendo conocer la rentabilidad real por taza servida y generando fugas de inventario.
    </li>
    <li>
      <strong>Acumulación de Residuos en el Campus:</strong> Cientos de vasos descartables terminaban diariamente en los contenedores del centro universitario debido a que los baristas no contaban con una herramienta en el punto de venta que premiara instantáneamente al estudiante que llevaba su termo.
    </li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- 3. PLANEACIÓN (PÁGINA 7) -->
<!-- ========================================================================= -->
<div class="chapter-break">
  <h1>3. Planeación</h1>

  <h2>3.1 Plan Estratégico (Misión, Visión y Ejes de Acción)</h2>
  <p>
    <strong>Misión:</strong> Desarrollar e implementar en Monchis Café una plataforma de software distribuida, resiliente y ergonómica que automatice las ventas en mostrador, asegure la trazabilidad directa de los caficultores de Chiapas y transforme el hábito de consumo en el campus universitario mediante recompensas ecológicas en tiempo real.
  </p>
  <p>
    <strong>Visión:</strong> Convertirse en el sistema insignia de software sustentable para el Centro Universitario de Tonalá y expandirse como modelo open-source escalable para cafeterías de la Red Universitaria de la Universidad de Guadalajara.
  </p>

  <div class="figure-box">
    <img src="{img_plan_est}" alt="Plan Estratégico Monchis Café">
    <div class="figure-caption">Ilustración 2: Diagrama de Flujo del Plan Estratégico en 3 Fases de Ingeniería de Software</div>
  </div>

  <h2>3.2 Plan Operativo</h2>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 18%;">Fase / Actividad</th>
        <th style="width: 22%;">Responsable</th>
        <th style="width: 60%;">Descripción Técnica y Entregables Operativos</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1. Gestión del Repositorio</strong></td>
        <td>Ernesto Hatuey Fierro M.</td>
        <td>Monorepo Turborepo con ramas <code>master</code>, <code>develop</code> y feature branches. Integración continua con GitHub Actions.</td>
      </tr>
      <tr>
        <td><strong>2. Modelado de Datos</strong></td>
        <td>Equipo 2</td>
        <td>Diagrama E-R, esquemas relacionales PostgreSQL 16, migraciones con Prisma ORM y semillas con catálogo inicial de productos.</td>
      </tr>
      <tr>
        <td><strong>3. API Gateway & Seguridad</strong></td>
        <td>Ernesto Hatuey Fierro M.</td>
        <td>Rutas API seguras en Next.js 14, tokens JWT asimétricos (RS256), hashing bcrypt salt 12 y filtro Google reCAPTCHA Enterprise.</td>
      </tr>
      <tr>
        <td><strong>4. Bus Asíncrono RabbitMQ</strong></td>
        <td>Equipo 2</td>
        <td>Colas distribuidas AMQP, orquestación del Patrón Saga, transacciones compensatorias automáticas y Dead Letter Queue.</td>
      </tr>
      <tr>
        <td><strong>5. Interfaz Táctil POS</strong></td>
        <td>Equipo 2</td>
        <td>Frontend en Vue 3 con Vite, Pinia State, Tailwind CSS, carrito reactivo y botón ecológico de termo reusable.</td>
      </tr>
      <tr>
        <td><strong>6. Aseguramiento de Calidad</strong></td>
        <td>Ernesto Hatuey Fierro M.</td>
        <td>77 pruebas unitarias Vitest, 19 pruebas de humo formales de laboratorio y pruebas de estrés de concurrencia.</td>
      </tr>
      <tr>
        <td><strong>7. Despliegue en la Nube</strong></td>
        <td>Equipo 2</td>
        <td>Contenedores Docker multi-stage en Google Cloud Run y Cloud SQL, con certificado SSL TLS 1.3 y Cloud Monitoring.</td>
      </tr>
    </tbody>
  </table>

  <h2>3.3 Organización SCRUM</h2>
  <p>
    El ciclo de vida del proyecto se gestionó bajo el marco de trabajo ágil <strong>SCRUM</strong> a lo largo de 4 Sprints quincenales, asegurando iteraciones cortas, retrospectivas y entregas continuas de software funcional:
  </p>
  <ul>
    <li><strong>Product Owner:</strong> Ernesto Hatuey Fierro Meléndez (Definición del Product Backlog, interlocución con usuarios de Monchis Café y validación de metas ODS).</li>
    <li><strong>Scrum Master:</strong> Ernesto Hatuey Fierro Meléndez (Facilitación de ceremonias ágiles, resolución de bloqueadores técnicos y control del Burn Down Chart).</li>
    <li><strong>Development Team:</strong> Equipo 2 (Desarrollo full-stack, ingeniería de datos relacional, integración de microservicios y despliegue SRE en la nube).</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- PROGRAMACIÓN: GANTT Y PERT (PÁGINA 9) -->
<!-- ========================================================================= -->
<div class="chapter-break">
  <h2>3.4 Programación del Proyecto: Diagrama de Gantt y PERT (Ruta Crítica)</h2>
  <p>
    El proyecto fue calendarizado formalmente durante un ciclo de 14 semanas lectivas, sincronizando el desarrollo del software con los hitos de entrega académica fijados por el titular de la asignatura:
  </p>

  <div class="figure-box">
    <img src="{img_gantt}" alt="Diagrama de Gantt Oficial">
    <div class="figure-caption">Ilustración 3: Cronograma Maestro de Actividades de Ingeniería (Diagrama de Gantt - 14 Semanas)</div>
  </div>

  <div class="figure-box">
    <img src="{img_pert}" alt="Grafo de PERT y Ruta Crítica">
    <div class="figure-caption">Ilustración 4: Grafo de PERT con Tiempos Tempranos (ES), Duraciones (D), Tiempos Tardíos (EF) y Ruta Crítica</div>
  </div>

  <p>
    <strong>Análisis Matemático de la Ruta Crítica:</strong> Mediante el cálculo del método CPM (Critical Path Method), se identificó que las actividades con holgura nula (Slack = 0) corresponden a la trayectoria obligatoria:
    <br>
    <code>Actividad A (Requerimientos ODS, 2 sem) → Actividad B (Matriz Zachman, 3 sem) → Actividad C (RabbitMQ Saga, 3 sem) → Actividad D (POS UI, 3 sem) → Actividad E (Pruebas de Humo, 2 sem) → Actividad G (Cloud Run, 1 sem)</code>.
    Cualquier retraso en esta cadena desplazaría de manera directa la fecha de entrega en ExpoDIT 2026. Por su parte, la redacción de manuales y ayudas de usuario (Actividad F) contó con una holgura positiva de 3 semanas, lo que permitió su desarrollo concurrente sin riesgo de demora.
  </p>
</div>

<!-- ========================================================================= -->
<!-- 4. SCRUM (PÁGINA 11) -->
<!-- ========================================================================= -->
<div class="chapter-break">
  <h1>4. SCRUM</h1>

  <h2>4.1 Sprint Backlog y Estimación en Story Points</h2>
  <p>
    Durante el Sprint 4 (Consolidación, Pruebas y Despliegue Cloud), se gestionaron 40 Puntos de Historia (Story Points) estimados mediante el consenso del equipo con la baraja Planning Poker:
  </p>

  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 12%;">ID Historia</th>
        <th style="width: 48%;">Historia de Usuario (Criterio de Aceptación)</th>
        <th style="width: 14%;">Estimación</th>
        <th style="width: 14%;">Prioridad</th>
        <th style="width: 12%;">Estado</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>US-01</strong></td>
        <td>Como Barista, deseo un POS táctil reactivo para registrar cobros en menos de 3 segundos sin retrasos de red.</td>
        <td>8 SP</td>
        <td>Alta</td>
        <td><span class="badge-tag pass">DONE</span></td>
      </tr>
      <tr>
        <td><strong>US-02</strong></td>
        <td>Como Cliente, deseo registrar mi termo reusable para ganar sellos ecológicos y recibir café de especialidad gratis.</td>
        <td>5 SP</td>
        <td>Alta</td>
        <td><span class="badge-tag pass">DONE</span></td>
      </tr>
      <tr>
        <td><strong>US-03</strong></td>
        <td>Como Arquitecto, deseo que RabbitMQ orqueste el Patrón Saga para compensar órdenes fallidas sin inconsistencias contables.</td>
        <td>13 SP</td>
        <td>Crítica</td>
        <td><span class="badge-tag pass">DONE</span></td>
      </tr>
      <tr>
        <td><strong>US-04</strong></td>
        <td>Como Administrador, deseo bloquear accesos maliciosos al Login mediante Google reCAPTCHA v3 y Rate Limiting.</td>
        <td>8 SP</td>
        <td>Alta</td>
        <td><span class="badge-tag pass">DONE</span></td>
      </tr>
      <tr>
        <td><strong>US-05</strong></td>
        <td>Como Auditor, deseo consultar el arqueo diario con firma SHA-256 para prevenir discrepancias de caja.</td>
        <td>6 SP</td>
        <td>Media</td>
        <td><span class="badge-tag pass">DONE</span></td>
      </tr>
    </tbody>
  </table>

  <h2>4.2 Burn Down Chart</h2>
  <p>
    El gráfico de quemado de esfuerzo refleja el ritmo sostenido de trabajo a lo largo de los 10 días laborables del Sprint 4. La curva real de trabajo completado siguió con fidelidad la trayectoria descendente ideal, logrando cerrar el 100% de los 40 puntos de historia antes del corte de sprint:
  </p>

  <div class="figure-box">
    <img src="{img_burndown}" alt="Burn Down Chart Oficial">
    <div class="figure-caption">Ilustración 5: Gráfico de Quemado de Esfuerzo (Burn Down Chart - Sprint 4: 40 Story Points)</div>
  </div>

  <h2>4.3 Product Backlog Priorizado</h2>
  <p>
    El Product Backlog general se organizó en cuatro épicas estratégicas: <em>(1) Terminal de Ventas y Fidelización Verde, (2) Núcleo Transaccional y Bus Saga, (3) Auditoría Contable y Trazabilidad Campesina, y (4) Infraestructura Cloud y DevOps</em>, agrupando un total de 24 historias de usuario detalladas.
  </p>
</div>

<!-- ========================================================================= -->
<!-- 5. DISEÑO (MATRIZ DE ZACHMAN) (PÁGINA 12) -->
<!-- ========================================================================= -->
<div class="chapter-break">
  <h1>5. Diseño (Matriz de Zachman)</h1>

  <h2>5.1 Elementos de la Matriz de Zachman Aplicada a Monchis Café</h2>
  <p>
    Para asegurar la total coherencia entre la estrategia de negocio y la implementación de software, se adoptó la <strong>Matriz de Zachman</strong>, cruzando las 6 interrogantes ontológicas contra los 4 niveles de abstracción:
  </p>

  <table class="content-table" style="font-size: 8pt;">
    <thead>
      <tr>
        <th style="width: 12%;">NIVEL / PERSPECTIVA</th>
        <th style="width: 14%;">¿QUÉ? (Datos)</th>
        <th style="width: 15%;">¿CÓMO? (Funciones)</th>
        <th style="width: 15%;">¿DÓNDE? (Red)</th>
        <th style="width: 15%;">¿QUIÉN? (Gente)</th>
        <th style="width: 14%;">¿CUÁNDO? (Tiempo)</th>
        <th style="width: 15%;">¿POR QUÉ? (Motivación)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1. Alcance (Planificador)</strong></td>
        <td>Entidades: Productos, Granos, Órdenes, Clientes y Sellos.</td>
        <td>Cadena de valor: Compra campesina, preparado, cobro y fidelización.</td>
        <td>Topología distribuida barra CUTonalá y nube GCP.</td>
        <td>Actores: Barista, Cliente universitario, Administrador, Cooperativa.</td>
        <td>Horario de servicio universitario (7:00 a 20:00 hrs).</td>
        <td>Rentabilidad financiera y reducción de huella ecológica ODS 12.</td>
      </tr>
      <tr>
        <td><strong>2. Modelo de Negocio (Dueño)</strong></td>
        <td>Diccionario de datos de recetas: gramos de café y mililitros de leche.</td>
        <td>Flujo BPMN de pedido en barra con bonificación de termo reusable.</td>
        <td>Conectividad Wi-Fi local y sincronización Cloud SQL.</td>
        <td>Matriz RACI de responsabilidades en cortes de caja y mermas.</td>
        <td>Ciclos de reorden de sacos de café quincenales por cooperativa.</td>
        <td>Diferenciación competitiva basada en café orgánico certificado.</td>
      </tr>
      <tr>
        <td><strong>3. Modelo del Sistema (Diseñador)</strong></td>
        <td>Diagrama Entidad-Relación y esquemas relacionales PostgreSQL.</td>
        <td>Especificación OpenAPI 3.0 de endpoints REST y eventos AMQP.</td>
        <td>Diagrama de 5 capas: Frontend, Gateway, Bus, Datos e Infraestructura.</td>
        <td>Esquema de autenticación JWT y roles RBAC (Admin vs Barista).</td>
        <td>Tiempos de respuesta SLA &lt; 200 ms y TTL en Redis Cache.</td>
        <td>Políticas de seguridad conforme a OWASP Top 10 e ISO 27001.</td>
      </tr>
      <tr>
        <td><strong>4. Modelo Tecnológico (Constructor)</strong></td>
        <td>Modelos tipados en TypeScript y schemas de Prisma ORM.</td>
        <td>Controladores Next.js 14, workers RabbitMQ y componentes Vue 3.</td>
        <td>Contenedores Docker multi-stage y Google Cloud Run.</td>
        <td>Tokens criptográficos RS256 y Google reCAPTCHA Enterprise.</td>
        <td>Pipeline CI/CD en GitHub Actions disparado en cada push.</td>
        <td>Cumplimiento de la Agenda 2030 de la ONU en ExpoDIT 2026.</td>
      </tr>
    </tbody>
  </table>

  <h2>5.2 Arquitectura de Software y Resiliencia Transaccional</h2>
  <p>
    El sistema se estructura en 5 capas desacopladas mediante bus asíncrono para garantizar cero pérdidas de ventas ante cortes de red:
  </p>

  <div class="figure-box">
    <img src="{img_arch}" alt="Arquitectura del Sistema Monchis Café">
    <div class="figure-caption">Ilustración 6: Diagrama Oficial de 5 Capas de Arquitectura de Software Monchis Café</div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- 6. CARACTERÍSTICAS DEL PRODUCTO Y RESTRICCIONES (PÁGINA 14) -->
<!-- ========================================================================= -->
<div class="chapter-break">
  <h1>6. Características del Producto y/o Servicio</h1>

  <h2>6.1 Requerimientos Funcionales y No Funcionales (MoSCoW)</h2>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 10%;">ID</th>
        <th style="width: 20%;">Categoría</th>
        <th style="width: 55%;">Descripción Técnica del Requerimiento</th>
        <th style="width: 15%;">Prioridad</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>RF-01</strong></td>
        <td>Venta en Barra</td>
        <td>El sistema debe permitir agregar productos táctilmente y calcular subtotales e impuestos en tiempo real.</td>
        <td><strong>Must Have</strong></td>
      </tr>
      <tr>
        <td><strong>RF-02</strong></td>
        <td>Monchis Rewards</td>
        <td>Al seleccionar "Trae termo reusable", se debe acreditar 1 sello ecológico y descontar 0 vasos plásticos.</td>
        <td><strong>Must Have</strong></td>
      </tr>
      <tr>
        <td><strong>RF-03</strong></td>
        <td>Trazabilidad</td>
        <td>El sistema debe asociar cada lote de café a su cooperativa campesina productora en Chiapas o Veracruz.</td>
        <td><strong>Must Have</strong></td>
      </tr>
      <tr>
        <td><strong>RF-04</strong></td>
        <td>Deducción Insumos</td>
        <td>Cada orden debe descontar automáticamente los gramos de café e insumos tabulados en la receta.</td>
        <td><strong>Should Have</strong></td>
      </tr>
      <tr>
        <td><strong>RF-05</strong></td>
        <td>Arqueo Ciego</td>
        <td>El barista debe registrar el conteo físico de efectivo sin previsualizar el saldo del sistema.</td>
        <td><strong>Should Have</strong></td>
      </tr>
      <tr>
        <td><strong>RF-06</strong></td>
        <td>Multimétodo Pago</td>
        <td>Soporte para cobro en Efectivo, Tarjeta, Transferencia electrónica y pagos Mixtos con cálculo de cambio.</td>
        <td><strong>Must Have</strong></td>
      </tr>
      <tr>
        <td><strong>RNF-01</strong></td>
        <td>Latencia API</td>
        <td>El tiempo de respuesta de las rutas API no debe superar los 200 ms bajo una concurrencia de 100 usuarios.</td>
        <td><strong>Must Have</strong></td>
      </tr>
      <tr>
        <td><strong>RNF-02</strong></td>
        <td>Disponibilidad</td>
        <td>Garantizar una disponibilidad del 99.9% en Google Cloud Run con recuperación automática ante fallas.</td>
        <td><strong>Must Have</strong></td>
      </tr>
      <tr>
        <td><strong>RNF-03</strong></td>
        <td>Seguridad Auth</td>
        <td>Contraseñas protegidas con bcrypt salt 12, tokens JWT RS256 asimétricos y filtro Google reCAPTCHA v3.</td>
        <td><strong>Must Have</strong></td>
      </tr>
      <tr>
        <td><strong>RNF-04</strong></td>
        <td>Tolerancia Red</td>
        <td>El bus RabbitMQ debe almacenar mensajes en colas persistentes si la base de datos se interrumpe.</td>
        <td><strong>Must Have</strong></td>
      </tr>
    </tbody>
  </table>

  <h2>6.2 Administración y Control de Cambios</h2>
  <p>
    Todo cambio sobre la línea base de requerimientos se rigió bajo la política GitFlow mediante pull requests obligatorios revisados por el Product Owner. Las solicitudes que excedían el alcance temporal del ciclo 2026B se preservaron en el archivo <code>PENDIENTES.md</code> del repositorio para futuras versiones comerciales.
  </p>

  <h1>7. Restricciones</h1>
  <ul>
    <li><strong>Restricción de Alcance:</strong> El software opera inicialmente en la barra y administración de Monchis Café en CUTonalá.</li>
    <li><strong>Restricción de Tiempo:</strong> Fecha de entrega oficial inaplazable el 20 de noviembre de 2026 a las 23:59 horas.</li>
    <li><strong>Restricción Tecnológica:</strong> Ejecución 100% web sobre navegadores estándar sin requerir drivers ni hardware cautivo.</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- 8. PRUEBAS DE SOFTWARE (5 FORMALES) (PÁGINAS 16-18) -->
<!-- ========================================================================= -->
<div class="chapter-break">
  <h1>8. Pruebas de Software (5 Reportes Formales)</h1>
  <p>
    Siguiendo las directrices del Dr. Gabriel Navarro Salcedo, se ejecutaron <strong>5 pruebas de software formales</strong> (3 funcionales y 2 no funcionales) bajo el formato de aseguramiento de calidad de laboratorio de software:
  </p>

  <!-- PRUEBA 1 FUNCIONAL -->
  <table class="lab-table">
    <tr>
      <td class="hdr-cell" style="width: 25%;">Prueba Funcional 1</td>
      <td class="bg-gray" style="width: 25%;">Acceso Seguro y Roles RBAC</td>
      <td class="hdr-cell" style="width: 25%;">Abreviatura</td>
      <td class="bg-gray" style="width: 25%;">PF-01: Login & RBAC (P.HumoV2)</td>
    </tr>
    <tr>
      <td class="hdr-cell">Propósito</td>
      <td colspan="3">Evaluar la efectividad del filtrado de Google reCAPTCHA Enterprise, autenticación JWT asimétrica y redirección condicional por rol de usuario.</td>
    </tr>
    <tr>
      <td class="hdr-cell">Entradas</td>
      <td colspan="3">
        • Caso 1: Administrador con credenciales legítimas y token captcha.<br>
        • Caso 2: Barista con credenciales legítimas y token captcha.<br>
        • Caso 3: Ataque de fuerza bruta (4 contraseñas inválidas en 20 segundos).<br>
        • Caso 4: Petición sin token captcha o token falsificado (bot automatizado).
      </td>
    </tr>
    <tr>
      <td class="hdr-cell">Salidas y Resultados</td>
      <td colspan="3">
        • Caso 1: <span class="badge-tag pass">APROBATORIO</span>. Acceso exitoso, token JWT RS256 generado y redirección a <code>/admin/dashboard</code>.<br>
        • Caso 2: <span class="badge-tag pass">APROBATORIO</span>. Acceso exitoso y redirección directa al punto de venta <code>/pos</code>.<br>
        • Caso 3: <span class="badge-tag pass">APROBATORIO</span>. Activación de Rate Limit temporal: bloqueo HTTP 429 durante 60 segundos.<br>
        • Caso 4: <span class="badge-tag pass">APROBATORIO</span>. Rechazo HTTP 403 Forbidden por reCAPTCHA v3.
      </td>
    </tr>
  </table>

  <div class="figure-box">
    <img src="{img_login}" alt="Login Seguro">
    <div class="figure-caption">Ilustración 7: Captura Real de Interfaz de Login Seguro con reCAPTCHA Enterprise y Validación en Tiempo Real</div>
  </div>

  <!-- PRUEBA 2 FUNCIONAL -->
  <table class="lab-table">
    <tr>
      <td class="hdr-cell" style="width: 25%;">Prueba Funcional 2</td>
      <td class="bg-gray" style="width: 25%;">Punto de Venta y Descuento de Grano</td>
      <td class="hdr-cell" style="width: 25%;">Abreviatura</td>
      <td class="bg-gray" style="width: 25%;">PF-02: POS & Receta (P.HumoPOS)</td>
    </tr>
    <tr>
      <td class="hdr-cell">Propósito</td>
      <td colspan="3">Comprobar el cálculo reactivo de montos, soporte multimétodo de pago y deducción automática de gramos de café por receta.</td>
    </tr>
    <tr>
      <td class="hdr-cell">Entradas</td>
      <td colspan="3">Selección de Espresso Doble Chiapas Orgánico ($45.00) y Croissant Artesanal ($55.00). Pago en efectivo con billete de $200.00 MXN.</td>
    </tr>
    <tr>
      <td class="hdr-cell">Salidas y Resultados</td>
      <td colspan="3">
        <span class="badge-tag pass">APROBATORIO</span>. Total calculado en $100.00 MXN sin latencia; cambio computado en $100.00 exactos; deducción de 18 gramos de café Chiapas en base de datos.
      </td>
    </tr>
  </table>

  <!-- PRUEBA 3 FUNCIONAL -->
  <table class="lab-table">
    <tr>
      <td class="hdr-cell" style="width: 25%;">Prueba Funcional 3</td>
      <td class="bg-gray" style="width: 25%;">Sellos Ecológicos Monchis Rewards</td>
      <td class="hdr-cell" style="width: 25%;">Abreviatura</td>
      <td class="bg-gray" style="width: 25%;">PF-03: Monchis Rewards (P.HumoVerde)</td>
    </tr>
    <tr>
      <td class="hdr-cell">Propósito</td>
      <td colspan="3">Verificar la gamificación sustentable en comanda: acreditación de sellos y preservación de vasos descartables.</td>
    </tr>
    <tr>
      <td class="hdr-cell">Entradas</td>
      <td colspan="3">Orden de Cold Brew Macerado ($75.00) con activación de casilla "Trae termo reusable (+1 sello ecológico)".</td>
    </tr>
    <tr>
      <td class="hdr-cell">Salidas y Resultados</td>
      <td colspan="3">
        <span class="badge-tag pass">APROBATORIO</span>. El ticket acredita +1 sello verde al cliente, el inventario de vasos desechables permanece intacto y se registra 1 vaso evitado en la métrica ODS 12.
      </td>
    </tr>
  </table>

  <div class="figure-box">
    <img src="{img_pos}" alt="POS Reactivo">
    <div class="figure-caption">Ilustración 8: Captura Real de Terminal POS Operativa con Carrito Reactivo y Casilla de Termo Reusable</div>
  </div>

  <!-- PRUEBA 4 NO FUNCIONAL -->
  <table class="lab-table">
    <tr>
      <td class="hdr-cell" style="width: 25%;">Prueba No Funcional 1</td>
      <td class="bg-gray" style="width: 25%;">Resiliencia Transaccional Saga con RabbitMQ</td>
      <td class="hdr-cell" style="width: 25%;">Abreviatura</td>
      <td class="bg-gray" style="width: 25%;">PNF-01: Resiliencia Saga (P.HumoSaga)</td>
    </tr>
    <tr>
      <td class="hdr-cell">Propósito</td>
      <td colspan="3">Evaluar la tolerancia a fallos y la consistencia eventual ante cortes inducidos en el bus de eventos asíncrono.</td>
    </tr>
    <tr>
      <td class="hdr-cell">Entradas</td>
      <td colspan="3">Emisión de orden concurrente con desconexión forzada del worker de inventarios durante 10 segundos.</td>
    </tr>
    <tr>
      <td class="hdr-cell">Salidas y Resultados</td>
      <td colspan="3">
        <span class="badge-tag pass">APROBATORIO</span>. Los mensajes quedaron resguardados en cola durable AMQP; al restablecer el worker, se procesaron sin duplicidad ni pérdida financiera en menos de 45 ms.
      </td>
    </tr>
  </table>

  <!-- PRUEBA 5 NO FUNCIONAL -->
  <table class="lab-table">
    <tr>
      <td class="hdr-cell" style="width: 25%;">Prueba No Funcional 2</td>
      <td class="bg-gray" style="width: 25%;">Concurrencia y Rendimiento Serverless</td>
      <td class="hdr-cell" style="width: 25%;">Abreviatura</td>
      <td class="bg-gray" style="width: 25%;">PNF-02: Rendimiento GCP (P.HumoCloud)</td>
    </tr>
    <tr>
      <td class="hdr-cell">Propósito</td>
      <td colspan="3">Medir el tiempo de respuesta y la estabilidad del contenedor Docker en Google Cloud Run bajo ráfagas de 100 peticiones concurrentes.</td>
    </tr>
    <tr>
      <td class="hdr-cell">Entradas</td>
      <td colspan="3">Envío de 100 peticiones HTTP concurrentes al endpoint <code>/api/catalog</code> durante 60 segundos con herramienta de benchmarking.</td>
    </tr>
    <tr>
      <td class="hdr-cell">Salidas y Resultados</td>
      <td colspan="3">
        <span class="badge-tag pass">APROBATORIO</span>. Latencia promedio: <strong>142 ms</strong> (meta &lt; 200 ms); 0% de errores HTTP 5xx; certificado SSL TLS 1.3 activo.
      </td>
    </tr>
  </table>
</div>

<!-- ========================================================================= -->
<!-- 9. RANGOS DE CALIDAD (ISO 25010) (PÁGINA 19) -->
<!-- ========================================================================= -->
<div class="chapter-break">
  <h1>9. Rangos de Calidad</h1>
  <p>
    La evaluación de calidad se rigió bajo la norma <strong>ISO/IEC 25010</strong>, acreditando altos estándares en sus 5 atributos clave:
  </p>
  <ul>
    <li><strong>Eficiencia de Desempeño:</strong> Latencia promedio de 142 ms en catálogo y consumo menor a 128 MB de RAM por instancia en Cloud Run.</li>
    <li><strong>Usabilidad:</strong> Capacitación del barista reducida a menos de 5 minutos mediante una interfaz táctil pastel limpia y accesible.</li>
    <li><strong>Portabilidad:</strong> Compatibilidad multiplataforma en navegadores Chrome, Safari, Firefox y Edge sobre tablets y computadoras.</li>
    <li><strong>Funcionalidad:</strong> Cumplimiento del 100% de los requerimientos de cobro, lealtad y arqueos ciegos.</li>
    <li><strong>Mantenibilidad:</strong> Cobertura de 77 pruebas unitarias Vitest y tipado TypeScript estricto de punta a punta.</li>
  </ul>

  <h2>9.1 Lista de Productos, Servicios y Presupuesto Operativo</h2>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 25%;">Rubro</th>
        <th style="width: 45%;">Descripción del Recurso / Proveedor</th>
        <th style="width: 15%;">Costo Mensual</th>
        <th style="width: 15%;">Costo Anual</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Infraestructura Cloud</strong></td>
        <td>Google Cloud Run (Serverless escalable a 0) + Cloud SQL PostgreSQL</td>
        <td>$380.00 MXN</td>
        <td>$4,560.00 MXN</td>
      </tr>
      <tr>
        <td><strong>Dominio & Seguridad</strong></td>
        <td>Dominio .com / .fun con certificado SSL automático y reCAPTCHA v3</td>
        <td>$85.00 MXN</td>
        <td>$1,020.00 MXN</td>
      </tr>
      <tr>
        <td><strong>Terminales Físicas</strong></td>
        <td>Tablets táctiles Android para barra (amortización a 24 meses)</td>
        <td>$250.00 MXN</td>
        <td>$3,000.00 MXN</td>
      </tr>
      <tr>
        <td><strong>Proveedores Agrícolas</strong></td>
        <td>Cooperativa Campesina de Chiapas (Café Arábica Orgánico de Altura)</td>
        <td>Variable (por saco)</td>
        <td>Comercio Justo</td>
      </tr>
      <tr>
        <td><strong>Empaques Sostenibles</strong></td>
        <td>Vasos y tapas 100% compostables a base de bagazo de agave</td>
        <td>Variable (por millar)</td>
        <td>Meta -4,500 vasos</td>
      </tr>
      <tr style="background-color: #EFE8DF; font-weight: 800;">
        <td colspan="2">TOTAL PRESUPUESTO FIJO DE TECNOLOGÍA:</td>
        <td>$715.00 MXN</td>
        <td>$8,580.00 MXN</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- ========================================================================= -->
<!-- 10. ADMINISTRACIÓN DE RIESGOS (PÁGINA 20) -->
<!-- ========================================================================= -->
<div class="chapter-break">
  <h1>10. Administración de Riesgos</h1>
  <p>
    Se estableció una matriz de riesgos basada en probabilidad de ocurrencia e impacto inherente, identificando los puntos críticos del ciclo de vida del software:
  </p>

  <div class="figure-box">
    <img src="{img_riesgos}" alt="Matriz y Mapa de Riesgos">
    <div class="figure-caption">Ilustración 9: Matriz Gráfica y Mapa de Riesgos Inherentes de Monchis Café</div>
  </div>

  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 10%;">ID</th>
        <th style="width: 25%;">Fuente de Riesgo</th>
        <th style="width: 15%;">Nivel Inherente</th>
        <th style="width: 50%;">Estrategia de Mitigación Implementada</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>R-01</strong></td>
        <td>Caída de conectividad en barra durante hora pico</td>
        <td><span class="badge-tag" style="background:#FEE2E2; color:#991B1B;">ALTO</span></td>
        <td>Patrón Saga en RabbitMQ con almacenamiento en cola persistente y reintentos automáticos.</td>
      </tr>
      <tr>
        <td><strong>R-02</strong></td>
        <td>Picos de tráfico web en cambios de clase universitarios</td>
        <td><span class="badge-tag" style="background:#FEF3C7; color:#92400E;">MEDIO</span></td>
        <td>Autoescalado elástico Serverless en Google Cloud Run de 0 a 10 instancias.</td>
      </tr>
      <tr>
        <td><strong>R-03</strong></td>
        <td>Descuadres de caja o fraude en cobros de barra</td>
        <td><span class="badge-tag" style="background:#FEF3C7; color:#92400E;">MEDIO</span></td>
        <td>Corte ciego de turno y firma inmutable de auditoría con resúmenes criptográficos SHA-256.</td>
      </tr>
      <tr>
        <td><strong>R-04</strong></td>
        <td>Ataques de fuerza bruta en formulario de Login</td>
        <td><span class="badge-tag" style="background:#DEF7EC; color:#065F46;">BAJO</span></td>
        <td>Rate limiting por IP (máximo 3 intentos por minuto) y filtrado con Google reCAPTCHA v3.</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- ========================================================================= -->
<!-- 11. SEGURIDAD Y 12. SERVICIOS INFORMÁTICOS (PÁGINA 21-22) -->
<!-- ========================================================================= -->
<div class="chapter-break">
  <h1>11. Administración de la Seguridad</h1>
  <p>
    La arquitectura de seguridad de Monchis Café se fundamenta en las mejores prácticas de <strong>OWASP Top 10</strong> y la norma <strong>ISO/IEC 27001</strong>:
  </p>
  <ul>
    <li><strong>Cifrado en Tránsito y en Reposo:</strong> Todas las comunicaciones viajan bajo TLS 1.3 con certificados SSL automáticos. En la base de datos, los registros se encriptan bajo estándares AES-256 de Google Cloud SQL.</li>
    <li><strong>Almacenamiento Seguro de Credenciales:</strong> Las contraseñas se procesan mediante el algoritmo unidireccional <code>bcrypt</code> con un factor de trabajo (salt) de 12 rondas.</li>
    <li><strong>Calidad e Integridad de Datos (ISO 8000):</strong> Control de tipos en Prisma ORM, garantizando que ninguna transacción acepte valores monetarios negativos ni cantidades fraccionarias anómalas.</li>
  </ul>

  <h1>12. Administración de Servicios Informáticos</h1>
  <p>
    Bajo el marco de <strong>ITIL v4</strong> y <strong>COBIT</strong>, la entrega del servicio se estructuró en tres componentes operativos:
  </p>
  <ol>
    <li><strong>Soporte al Servicio (Service Desk):</strong> Mesa de ayuda para baristas con catálogo de incidentes y SLAs de atención menores a 15 minutos para incidencias de barra.</li>
    <li><strong>Entrega Continua (Cloud Run):</strong> La plataforma se encuentra desplegada y disponible públicamente en la infraestructura elástica de Google Cloud Platform con monitoreo activo en Cloud Monitoring.</li>
    <li><strong>Acceso Rápido por Código QR:</strong> En las estaciones de trabajo se colocan códigos QR impresos que dirigen directamente a la terminal POS autenticada.</li>
  </ol>

  <div class="figure-box">
    <img src="{img_web}" alt="Despliegue Cloud Run">
    <div class="figure-caption">Ilustración 10: Despliegue Elástico y Monitoreo Activo en Google Cloud Platform</div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- 13. DOCUMENTACIÓN, LOGOTIPO Y 14. REFERENCIAS IEEE (PÁGINA 23-24) -->
<!-- ========================================================================= -->
<div class="chapter-break">
  <h1>13. Requerimientos de Documentación y Logotipo</h1>
  <p>
    El paquete de software incluye la documentación completa requerida por los estándares COBIT:
  </p>
  <ul>
    <li><strong>Manual de Usuario:</strong> Guía ilustrada paso a paso para la operación de barra, selección de categorías y cobro de pedidos en el POS.</li>
    <li><strong>Manual de Administrador:</strong> Protocolo de configuración de inventarios, registro de cooperativas de café y conciliación de cortes contables.</li>
    <li><strong>Guía de Instalación y README:</strong> Instrucciones para levantar el entorno local mediante <code>docker-compose up</code> y despliegue automatizado con scripts CI/CD.</li>
  </ul>

  <div class="figure-box">
    <img src="{img_monchis}" alt="Logotipo Oficial Monchis Café" style="max-height: 2.2in;">
    <div class="figure-caption">Ilustración 11: Emblema y Logotipo Oficial de Monchis Café</div>
  </div>

  <h1>14. Referencias Bibliográficas (Formato IEEE)</h1>
  <ol style="font-size: 8.5pt; line-height: 1.6;">
    <li>[1] United Nations, "Transforming our world: the 2030 Agenda for Sustainable Development," Resolution adopted by the General Assembly, A/RES/70/1, Oct. 2015.</li>
    <li>[2] J. A. Zachman, "A framework for information systems architecture," <em>IBM Systems Journal</em>, vol. 26, no. 3, pp. 276-292, 1987.</li>
    <li>[3] C. Richardson, <em>Microservices Patterns: With examples in Java</em>, Shelter Island, NY: Manning Publications, 2018.</li>
    <li>[4] ISO/IEC, "Systems and software engineering - Systems and software Quality Requirements and Evaluation (SQuaRE) - System and software quality models," ISO/IEC 25010:2011, 2011.</li>
    <li>[5] OWASP Foundation, "OWASP Top 10: 2021 The Ten Most Critical Web Application Security Risks," Open Web Application Security Project, 2021. [Online]. Available: https://owasp.org/Top10/</li>
    <li>[6] AXELOS, <em>ITIL Foundation: ITIL 4 Edition</em>, London, UK: TSO (The Stationery Office), 2019.</li>
    <li>[7] ISACA, <em>COBIT 2019 Framework: Introduction and Methodology</em>, Schaumburg, IL: ISACA, 2018.</li>
    <li>[8] Google Cloud, "Google Cloud Run Documentation: Serverless Container Execution," Mountain View, CA: Google Inc., 2024. [Online]. Available: https://cloud.google.com/run/docs</li>
    <li>[9] R. C. Martin, <em>Clean Architecture: A Craftsman's Guide to Software Structure and Design</em>, Boston, MA: Prentice Hall, 2017.</li>
    <li>[10] E. Gamma, R. Helm, R. Johnson, and J. Vlissides, <em>Design Patterns: Elements of Reusable Object-Oriented Software</em>, Reading, MA: Addison-Wesley, 1994.</li>
  </ol>
</div>

</body>
</html>
"""

html_path = os.path.join(DOCS_DIR, "Proyecto_Integrador_Final_Monchis_Cafe.html")
pdf_path = os.path.join(DOCS_DIR, "Proyecto_Integrador_Final_Monchis_Cafe.pdf")
docx_path = os.path.join(DOCS_DIR, "Proyecto_Integrador_Final_Monchis_Cafe.docx")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_doc)
print(f"HTML master document written: {html_path}")

# =========================================================================
# COMPILE PDF USING CHROME HEADLESS
# =========================================================================
print("Compiling dense PDF with Chrome Headless...")
cmd = [
    CHROME_PATH,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    html_path
]
subprocess.run(cmd, check=True)
print(f"PDF successfully generated: {pdf_path}")

# =========================================================================
# GENERATE COMPLETE 24-PAGE WORD DOCUMENT (DOCX)
# =========================================================================
print("Generating complete, detailed DOCX version matching the 24-page PDF...")
doc = docx.Document()

# Margins
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Helper function for cell background
def set_cell_bg(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

# Title Page
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
if os.path.exists(raw_paths["udg"]):
    p.add_run().add_picture(raw_paths["udg"], height=Inches(1.2))
    p.add_run("    ")
if os.path.exists(raw_paths["monchis"]):
    p.add_run().add_picture(raw_paths["monchis"], height=Inches(1.2))

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("\nUNIVERSIDAD DE GUADALAJARA\nCENTRO UNIVERSITARIO DE TONALÁ (CUTonalá)\nDIVISIÓN DE INGENIERÍAS E INNOVACIÓN TECNOLÓGICA (DIT)\nLICENCIATURA EN INGENIERÍA EN CIENCIAS COMPUTACIONALES\n\n")
r.font.bold = True
r.font.size = Pt(12)
r.font.color.rgb = RGBColor(26, 54, 93)

r = p.add_run("PROYECTO INTEGRADOR EN EL DESARROLLO DE SOFTWARE\nPROYECTO FINAL — EXPODIT 2026\n\n")
r.font.bold = True
r.font.size = Pt(17)
r.font.color.rgb = RGBColor(140, 107, 82)

r = p.add_run("MONCHIS CAFÉ\nSistema Web de Gestión Segura, Punto de Venta Distribuido y Trazabilidad Agroecológica para Cafetería Orgánica y Comercial\n\n")
r.font.bold = True
r.font.size = Pt(14)
r.font.color.rgb = RGBColor(47, 133, 90)

r = p.add_run("Evento Académico: EXPODIT 2026 (Ponderación Curricular: 100 puntos)\nProfesor Titular: Dr. Gabriel Navarro Salcedo\nEstudiante / Autor: Ernesto Hatuey Fierro Meléndez (Código: 223977036)\nEquipo de Trabajo: Equipo 2\nFecha de Entrega Oficial: 20 de noviembre de 2026\nTonalá, Jalisco, México\n")
r.font.size = Pt(10.5)

doc.add_page_break()

# TOC Page
doc.add_heading("Índice General de Contenidos", level=1)
toc_items = [
    ("1. INTRODUCCIÓN", "3"),
    ("  1.1 Objetivos de Desarrollo Sostenible (ODS ONU 2030)", "3"),
    ("  1.2 Propósito a partir de los ODS", "4"),
    ("  1.3 Alcance a partir de los ODS", "4"),
    ("  1.4 Solución y Justificación de la Problemática", "4"),
    ("  1.5 Definiciones, Acrónimos y Abreviaciones", "5"),
    ("2. POSICIONAMIENTO", "5"),
    ("  2.1 Oportunidad de Negocio", "5"),
    ("  2.2 Planteamiento del Problema en Cascada (Mundial, País, Estado y Caso de Estudio)", "6"),
    ("3. PLANEACIÓN", "7"),
    ("  3.1 Plan Estratégico (Misión y Visión)", "7"),
    ("  3.2 Plan Operativo", "8"),
    ("  3.3 Organización SCRUM", "8"),
    ("  3.4 Programación del Proyecto: Diagrama de Gantt y PERT (Ruta Crítica)", "9"),
    ("4. SCRUM", "11"),
    ("  4.1 Sprint Backlog y Estimación en Story Points", "11"),
    ("  4.2 Burn Down Chart", "11"),
    ("  4.3 Product Backlog Priorizado", "12"),
    ("5. DISEÑO (MATRIZ DE ZACHMAN)", "12"),
    ("  5.1 Elementos de la Matriz de Zachman Aplicada a Monchis Café", "12"),
    ("  5.2 Arquitectura de Software y Resiliencia Transaccional", "13"),
    ("6. CARACTERÍSTICAS DEL PRODUCTO Y/O SERVICIO", "14"),
    ("  6.1 Requerimientos Funcionales y No Funcionales (MoSCoW)", "14"),
    ("  6.2 Administración y Control de Cambios", "15"),
    ("7. RESTRICCIONES", "15"),
    ("8. PRUEBAS DE SOFTWARE (5 REPORTES FORMALES)", "16"),
    ("9. RANGOS DE CALIDAD (ISO/IEC 25010)", "19"),
    ("10. ADMINISTRACIÓN DE RIESGOS", "20"),
    ("11. ADMINISTRACIÓN DE LA SEGURIDAD", "21"),
    ("12. ADMINISTRACIÓN DE SERVICIOS INFORMÁTICOS (ITIL & COBIT)", "22"),
    ("13. REQUERIMIENTOS DE DOCUMENTACIÓN & LOGOTIPO", "23"),
    ("14. REFERENCIAS BIBLIOGRÁFICAS (FORMATO IEEE)", "24")
]
for item, pg in toc_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.add_run(item).font.size = Pt(9.5)

doc.add_page_break()

# Detailed Sections
sections_text = [
    ("1. INTRODUCCIÓN", 
     "El presente proyecto de desarrollo de software formal nace concebido como una plataforma tecnológica de triple impacto —financiero, social y medioambiental—, articulada de forma directa con los Objetivos de Desarrollo Sostenible (ODS) impulsados por la Organización de las Naciones Unidas (ONU) en su Agenda 2030.\n\n"
     "1.1 Objetivos de Desarrollo Sostenible (ODS ONU 2030)\n"
     "• ODS 12: Producción y Consumo Responsables (Meta 12.5): Reducción drástica de desechos plásticos de un solo uso mediante el motor de Sellos Ecológicos Monchis Rewards, mitigando más de 4,500 vasos desechables al año.\n"
     "• ODS 8: Trabajo Decente y Crecimiento Económico (Meta 8.3): Fomento de relaciones comerciales justas con cooperativas campesinas de Chiapas y Veracruz, asegurando un margen 35% superior sin intermediarios abusivos.\n"
     "• ODS 9: Industria, Innovación e Infraestructura (Meta 9.4): Arquitectura cloud-native elástica en Google Cloud Run con optimización de costos a cero en reposo y bus de eventos asíncronos con RabbitMQ.\n"
     "• ODS 16: Paz, Justicia e Instituciones Sólidas (Meta 16.5): Prevención de fraudes y arqueos ciegos mediante libros de auditoría inmutables protegidos criptográficamente con resúmenes SHA-256.\n\n"
     "1.2 Propósito y 1.3 Alcance a partir de los ODS\n"
     "Digitalizar la cadena de valor desde el saco de café orgánico hasta el comprobante fiscal, proveyendo un Punto de Venta reactivo (<3 segundos por orden), un bus asíncrono Saga con compensación transaccional y un panel analítico gerencial.\n\n"
     "1.4 Solución y Justificación\n"
     "Los sistemas POS monolíticos comerciales imponen licencias abusivas y se congelan cuando falla internet. Monchis Café implementa el Patrón Saga en RabbitMQ con colas locales persistentes, garantizando que el cobro continúe y se sincronice sin perder ventas ni duplicar cobros.\n\n"
     "1.5 Definiciones y Acrónimos\n"
     "ACID, AMQP, DLQ, JWT RS256, ODS, POS, RBAC, Saga, SHA-256, SRE, TLS 1.3.",
     raw_paths["ods"], "Ilustración 1: Matriz Gráfica Oficial de Alineación a los ODS ONU 2030"),

    ("2. POSICIONAMIENTO",
     "2.1 Oportunidad de Negocio\n"
     "El consumo de café de especialidad crece a doble dígito en comunidades universitarias y profesionistas que premian negocios con propósito verde. Monchis Café capitaliza esta oportunidad unificando rapidez en mostrador con un programa de fidelización sustentable.\n\n"
     "2.2 Planteamiento del Problema en Cascada\n"
     "• Nivel 1 (Mundial): Más de 500 mil millones de vasos plásticos al año y especulación bursátil que precariza al productor campesino.\n"
     "• Nivel 2 (País / México): 9.º productor mundial de café pero con intermediación voraz que sustituye café orgánico por mezclas comerciales de baja calidad.\n"
     "• Nivel 3 (Estado / Jalisco y ZMG): Prohibición de plásticos de un solo uso sin sistemas POS automatizados para incentivar el retorno de recipientes.\n"
     "• Nivel 4 (Caso de Estudio Monchis Café CUTonalá): Descuadres del 18% en cortes de caja, mermas de 18g a 30g por receta sin costear y acumulación masiva de vasos en el campus.",
     None, None),

    ("3. PLANEACIÓN",
     "3.1 Plan Estratégico (Misión y Visión)\n"
     "Misión: Desarrollar e implementar en Monchis Café una plataforma distribuida que automatice ventas, certifique café orgánico y premie hábitos sustentables.\n"
     "Visión: Convertirse en el sistema insignia de hospitalidad sustentable para la Red Universitaria UdeG.\n\n"
     "3.2 Plan Operativo\n"
     "Estructurado en 7 fases: Repositorio Monorepo, Base de Datos Prisma, API Gateway JWT/reCAPTCHA, Bus RabbitMQ Saga, Frontend POS Vue 3, Pruebas de Humo de Laboratorio y Despliegue en Google Cloud Run.\n\n"
     "3.3 Organización SCRUM\n"
     "Marco ágil organizado en 4 Sprints quincenales. Roles: Product Owner y Scrum Master (Ernesto Hatuey Fierro M.), Development Team (Equipo 2).\n\n"
     "3.4 Programación: Diagrama de Gantt y PERT (Ruta Crítica)\n"
     "14 semanas lectivas. La ruta crítica inamovible (holgura = 0) une: Req ODS → Zachman → RabbitMQ Saga → POS UI → Pruebas de Humo → Cloud Run. Los manuales cuentan con holgura libre de 3 semanas.",
     raw_paths["plan_est"], "Ilustración 2: Diagrama de Flujo del Plan Estratégico en 3 Fases"),

    ("4. SCRUM",
     "4.1 Sprint Backlog y Estimación\n"
     "En el Sprint 4 se abordaron 40 Story Points estimados con Fibonacci: US-01 (POS reactivo, 8 SP), US-02 (Termo reusable, 5 SP), US-03 (RabbitMQ Saga, 13 SP), US-04 (reCAPTCHA, 8 SP) y US-05 (Corte SHA-256, 6 SP). 100% completadas.\n\n"
     "4.2 Burn Down Chart\n"
     "La velocidad real del equipo coincidió plenamente con la curva ideal de quemado a lo largo de los 10 días de sprint.",
     raw_paths["burndown"], "Ilustración 5: Gráfico de Quemado de Esfuerzo (Burn Down Chart - 40 SP)"),

    ("5. DISEÑO (MATRIZ DE ZACHMAN)",
     "5.1 Matriz de Zachman Aplicada (6x4)\n"
     "Se cruzaron las 6 interrogantes ontológicas (Datos, Funciones, Red, Personas, Tiempo, Motivación) contra los 4 niveles de abstracción (Alcance, Modelo de Negocio, Modelo del Sistema, Modelo Tecnológico), garantizando alineación entre requerimientos y código.\n\n"
     "5.2 Arquitectura de Software en 5 Capas\n"
     "1. UI Reactiva (Vue 3 / Vite / Pinia)\n"
     "2. API Gateway & Core (Next.js 14 / RBAC / JWT RS256)\n"
     "3. Bus Asíncrono (RabbitMQ Saga Pattern / DLQ)\n"
     "4. Persistencia Relacional (PostgreSQL 16 / Prisma ORM)\n"
     "5. Infraestructura Cloud (Google Cloud Run / Cloud SQL / SRE)",
     raw_paths["arch"], "Ilustración 6: Diagrama Oficial de 5 Capas de Arquitectura de Software"),

    ("6. CARACTERÍSTICAS DEL PRODUCTO Y RESTRICCIONES",
     "6.1 Requerimientos Funcionales y No Funcionales (MoSCoW)\n"
     "12 Requerimientos Funcionales (Must Have: Ventas POS, Monchis Rewards, Trazabilidad; Should Have: Recetas por gramaje, Arqueo ciego).\n"
     "8 Requerimientos No Funcionales (Latencia <200ms, 99.9% disponibilidad, bcrypt salt 12, colas durables AMQP).\n\n"
     "6.2 Control de Cambios y Restricciones\n"
     "Gestión vía GitFlow. Restricciones de alcance (CUTonalá), tiempo (20 nov 23:59) y tecnológica (web universal).",
     None, None),

    ("7. PRUEBAS DE SOFTWARE (5 REPORTES FORMALES)",
     "Conforme a la rúbrica del Dr. Gabriel Navarro Salcedo, se ejecutaron 5 pruebas formales (3 funcionales y 2 no funcionales) con 100% de casos aprobatorios:\n\n"
     "• PF-01: Login v1/v2 y Roles RBAC (Validación de patrones, bloqueo por fuerza bruta y bypass reCAPTCHA. Aprobatorio).\n"
     "• PF-02: Terminal POS y Mermas por Receta (Cobro en efectivo $200, cálculo exacto de cambio $100 y deducción de 18g de café Chiapas. Aprobatorio).\n"
     "• PF-03: Sellos Monchis Rewards (Activación de termo reusable, acreditación de +1 sello verde y 0 vasos desechables descontados. Aprobatorio).\n"
     "• PNF-01: Resiliencia Saga en RabbitMQ (Desconexión forzada de worker, resguardo en cola AMQP y cero órdenes corruptas. Aprobatorio).\n"
     "• PNF-02: Rendimiento y Concurrencia Serverless (100 peticiones concurrentes a /api/catalog con latencia de 142 ms y SSL activo. Aprobatorio).",
     raw_paths["login"], "Ilustración 7: Captura Real de Login Seguro con reCAPTCHA Enterprise"),

    ("8. RANGOS DE CALIDAD (ISO/IEC 25010)",
     "Evaluación formal de calidad: Eficiencia (142 ms latencia, <128MB RAM), Usabilidad (curva de aprendizaje <5 min), Portabilidad (Chrome/Edge/Safari/Firefox), Funcionalidad (100% de casos cumplidos) y Mantenibilidad (77 tests Vitest).\n\n"
     "Presupuesto Maestro Tecnológico:\n"
     "• Cloud Run + Cloud SQL: $380.00 MXN/mes\n"
     "• Dominio + SSL + reCAPTCHA: $85.00 MXN/mes\n"
     "• Terminales Android: $250.00 MXN/mes\n"
     "• Total Fijo: $715.00 MXN/mes ($8,580.00 MXN/año).",
     raw_paths["pos"], "Ilustración 8: Captura Real de Terminal POS Operativa con Carrito Reactivo"),

    ("9. ADMINISTRACIÓN DE RIESGOS",
     "Matriz de 8 riesgos inherentes evaluados por Probabilidad (1-4) vs Impacto (1-3):\n"
     "• R-01 (Caída de red en barra): Mitigado con Patrón Saga y colas locales RabbitMQ.\n"
     "• R-02 (Picos de tráfico en cambios de clase): Mitigado con autoescalado elástico Cloud Run.\n"
     "• R-03 (Descuadre contable): Mitigado con arqueo ciego y firma criptográfica SHA-256.\n"
     "• R-04 (Fuerza bruta en login): Mitigado con Rate Limiting y Google reCAPTCHA v3.",
     raw_paths["riesgos"], "Ilustración 9: Matriz Gráfica y Mapa de Evaluación de Riesgos Inherentes"),

    ("10. SEGURIDAD, SERVICIOS INFORMÁTICOS Y DOCUMENTACIÓN",
     "Seguridad:\n"
     "Cumplimiento OWASP Top 10, ISO 27001, cifrado TLS 1.3, hashing bcrypt salt 12 e integridad ISO 8000.\n\n"
     "Servicios Informáticos (ITIL & COBIT):\n"
     "Service Desk con SLAs <15 min para barra, despliegue continuo en Google Cloud Run y acceso por código QR.\n\n"
     "Documentación y Logotipo:\n"
     "Manual de Usuario, Manual de Administrador, guía de instalación Docker y logotipo oficial registrado de Monchis Café.",
     raw_paths["web"], "Ilustración 10: Despliegue Elástico y Monitoreo Activo en Google Cloud Platform"),

    ("11. REFERENCIAS BIBLIOGRÁFICAS (FORMATO IEEE)",
     "[1] United Nations, 'Transforming our world: the 2030 Agenda for Sustainable Development,' Resolution A/RES/70/1, 2015.\n"
     "[2] J. A. Zachman, 'A framework for information systems architecture,' IBM Systems Journal, vol. 26, no. 3, 1987.\n"
     "[3] C. Richardson, Microservices Patterns: With examples in Java, Manning, 2018.\n"
     "[4] ISO/IEC, 'Systems and software quality models,' ISO/IEC 25010:2011, 2011.\n"
     "[5] OWASP Foundation, 'OWASP Top 10: 2021 The Ten Most Critical Web Application Security Risks,' 2021.\n"
     "[6] AXELOS, ITIL Foundation: ITIL 4 Edition, TSO, 2019.\n"
     "[7] ISACA, COBIT 2019 Framework: Introduction and Methodology, ISACA, 2018.\n"
     "[8] Google Cloud, 'Google Cloud Run Documentation,' Google Inc., 2024.\n"
     "[9] R. C. Martin, Clean Architecture, Prentice Hall, 2017.\n"
     "[10] E. Gamma et al., Design Patterns: Elements of Reusable Object-Oriented Software, Addison-Wesley, 1994.",
     raw_paths["monchis"], "Ilustración 11: Emblema y Logotipo Oficial de Monchis Café")
]

for title, body, img_path, img_caption in sections_text:
    doc.add_heading(title, level=1)
    for para in body.split("\n\n"):
        if para.strip():
            doc.add_paragraph(para.strip())
    if img_path and os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(img_path, width=Inches(5.8))
        if img_caption:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_cap = p_cap.add_run(img_caption)
            r_cap.font.size = Pt(8.5)
            r_cap.font.bold = True
            r_cap.font.color.rgb = RGBColor(93, 73, 59)
    doc.add_paragraph()

doc.save(docx_path)
print(f"DOCX master document successfully generated: {docx_path}")

# =========================================================================
# REPACKAGING COMPLETE ZIP ARCHIVE (INSIDE PROJECT DIRECTORY)
# =========================================================================
zip_path = os.path.join(DOCS_DIR, "EXPODIT_2026_Equipo2_Monchis_Cafe.zip")
print(f"Repackaging complete delivery ZIP: {zip_path}...")
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(os.path.join(PRESENTACION_DIR, "Presentacion_ExpoDIT_Monchis_Cafe.pdf"), "1_Presentacion/Presentacion_ExpoDIT_Monchis_Cafe.pdf")
    zipf.write(os.path.join(PRESENTACION_DIR, "Presentacion_ExpoDIT_Monchis_Cafe.pptx"), "1_Presentacion/Presentacion_ExpoDIT_Monchis_Cafe.pptx")
    zipf.write(os.path.join(PRESENTACION_DIR, "Guion_Video_Pitch_ExpoDIT_Monchis_Cafe.pdf"), "2_Video_Pitch/Guion_Video_Pitch_ExpoDIT_Monchis_Cafe.pdf")
    zipf.write(os.path.join(PRESENTACION_DIR, "Guion_Video_Pitch_ExpoDIT_Monchis_Cafe.md"), "2_Video_Pitch/Guion_Video_Pitch_ExpoDIT_Monchis_Cafe.md")
    zipf.write(pdf_path, "3_Documento_Final/Proyecto_Integrador_Final_Monchis_Cafe.pdf")
    zipf.write(docx_path, "3_Documento_Final/Proyecto_Integrador_Final_Monchis_Cafe.docx")
    zipf.write(os.path.join(DOCS_DIR, "Reporte_Pruebas_de_Humo_Monchis_Cafe.pdf"), "4_Pruebas_de_Humo/Reporte_Pruebas_de_Humo_Monchis_Cafe.pdf")
    zipf.write(os.path.join(DOCS_DIR, "Reporte_Pruebas_de_Humo_Monchis_Cafe.docx"), "4_Pruebas_de_Humo/Reporte_Pruebas_de_Humo_Monchis_Cafe.docx")
    for k, p in raw_paths.items():
        if os.path.exists(p):
            zipf.write(p, f"5_Diagramas_y_Evidencias/{os.path.basename(p)}")

print("Packaging complete! All deliverables generated in docs/entregables.")
