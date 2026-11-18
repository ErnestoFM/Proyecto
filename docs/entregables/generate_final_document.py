import os
import sys
import base64
import subprocess
import shutil
import zipfile
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

DOCS_DIR = r"d:\ernestofm\Proyecto\docs\entregables"
ASSETS_DIR = r"d:\ernestofm\Proyecto\docs\presentacion\expodit\assets"
DOWNLOADS_DIR = r"c:\Users\erfierro\Downloads"
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

html_doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Proyecto Integrador de Desarrollo de Software - Monchis Café</title>
<style>
  @page {{
    size: letter;
    margin: 20mm 22mm 22mm 22mm;
    @bottom-right {{
      content: counter(page);
      font-size: 9pt;
      color: #718096;
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
    line-height: 1.6;
    font-size: 10pt;
  }}
  .page-break {{
    page-break-after: always;
  }}

  /* Cover styling matching institutional template */
  .cover-page {{
    min-height: 9.6in;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 30px;
  }}
  .cover-logos {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 30px;
    margin-bottom: 25px;
  }}
  .cover-logos img.udg {{ height: 110px; }}
  .cover-logos img.monchis {{ height: 115px; }}
  .cover-header {{
    font-size: 15pt;
    font-weight: 800;
    color: #1A365D;
    line-height: 1.3;
    margin-bottom: 4px;
  }}
  .cover-sub {{
    font-size: 12pt;
    font-weight: 700;
    color: #8C6B52;
    margin-bottom: 25px;
  }}
  .cover-title {{
    font-size: 24pt;
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
    margin-bottom: 35px;
    max-width: 600px;
  }}
  .cover-meta {{
    font-size: 10.5pt;
    color: #4A5568;
    line-height: 1.9;
  }}
  .cover-meta strong {{
    color: #1A365D;
  }}

  /* Typography */
  h1 {{
    font-size: 16pt;
    font-weight: 900;
    color: #1A365D;
    border-bottom: 2px solid #8C6B52;
    padding-bottom: 4px;
    margin-top: 24px;
    margin-bottom: 12px;
  }}
  h2 {{
    font-size: 12.5pt;
    font-weight: 800;
    color: #8C6B52;
    margin-top: 18px;
    margin-bottom: 8px;
  }}
  h3 {{
    font-size: 10.5pt;
    font-weight: 800;
    color: #2F855A;
    margin-top: 12px;
    margin-bottom: 6px;
  }}
  p {{
    margin-bottom: 10px;
    text-align: justify;
  }}
  ul, ol {{
    margin-left: 22px;
    margin-bottom: 10px;
  }}
  li {{
    margin-bottom: 4px;
  }}

  /* Tables */
  table.content-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 9pt;
  }}
  table.content-table th, table.content-table td {{
    border: 1px solid #CBD5E0;
    padding: 6px 10px;
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
    margin: 12px 0 20px 0;
    font-size: 8.5pt;
  }}
  table.lab-table th, table.lab-table td {{
    border: 1.5px solid #2D3748;
    padding: 6px 8px;
    vertical-align: top;
  }}
  table.lab-table .bg-gray {{ background-color: #D1D5DB; font-weight: 700; }}
  table.lab-table .hdr-cell {{ font-weight: 800; font-style: italic; }}

  /* Figures showcase */
  .figure-box {{
    text-align: center;
    margin: 16px 0;
    padding: 10px;
    border: 1px solid #E2D9CF;
    border-radius: 8px;
    background: #FAF7F2;
    page-break-inside: avoid;
  }}
  .figure-box img {{
    max-width: 95%;
    max-height: 4.2in;
    border-radius: 6px;
    border: 1px solid #D8C7B5;
  }}
  .figure-caption {{
    font-size: 9pt;
    font-weight: 700;
    color: #5D493B;
    margin-top: 6px;
  }}

  /* Index Styles */
  .toc-list {{
    list-style: none;
    margin-left: 0;
  }}
  .toc-item {{
    display: flex;
    justify-content: space-between;
    padding: 4px 0;
    border-bottom: 1px dotted #CBD5E0;
    font-size: 10pt;
  }}
  .toc-item.bold {{
    font-weight: 800;
    color: #1A365D;
    margin-top: 6px;
    border-bottom: 1px solid #CBD5E0;
  }}
  .toc-page {{
    font-weight: 700;
    color: #8C6B52;
  }}

  .badge-tag {{
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 8pt;
    font-weight: 800;
  }}
  .badge-tag.pass {{ background: #DEF7EC; color: #03543F; }}
</style>
</head>
<body>

<!-- PORTADA OFICIAL INSTITUCIONAL -->
<div class="cover-page page-break">
  <div class="cover-logos">
    <img class="udg" src="{img_udg}" alt="Universidad de Guadalajara">
    <img class="monchis" src="{img_monchis}" alt="Monchis Café">
  </div>
  <div class="cover-header">UNIVERSIDAD DE GUADALAJARA</div>
  <div class="cover-sub">CENTRO UNIVERSITARIO DE TONALÁ (CUTonalá)<br>DIVISIÓN DE INGENIERÍAS E INNOVACIÓN TECNOLÓGICA (DIT)</div>
  <div style="font-size: 11pt; font-weight: 700; color: #4A5568; margin-bottom: 15px;">LICENCIATURA EN INGENIERÍA EN CIENCIAS COMPUTACIONALES</div>

  <h1 class="cover-title">PROYECTO INTEGRADOR EN EL DESARROLLO DE SOFTWARE</h1>
  <div class="cover-project">
    <strong>Caso de Estudio: Monchis Café</strong><br>
    <em>Sistema Web de Gestión Segura, Punto de Venta Distribuido y Trazabilidad Agroecológica para Cafetería Orgánica y Comercial</em>
  </div>

  <div class="cover-meta">
    <p><strong>Evento de Evaluación:</strong> EXPODIT 2026 (Ponderación: 100 puntos)</p>
    <p><strong>Profesor Titular:</strong> Dr. Gabriel Navarro Salcedo</p>
    <p><strong>Estudiante / Autor:</strong> Ernesto Hatuey Fierro Meléndez</p>
    <p><strong>Código de Estudiante:</strong> 223977036</p>
    <p><strong>Equipo de Trabajo:</strong> Equipo 2</p>
    <p><strong>Fecha de Entrega Oficial:</strong> 20 de noviembre de 2026</p>
    <p><strong>Lugar:</strong> Tonalá, Jalisco, México</p>
  </div>
</div>

<!-- ========================================================================= -->
<!-- ÍNDICES GENERALES -->
<!-- ========================================================================= -->
<div class="page-break">
  <h1>Índice General</h1>
  <div class="toc-list">
    <div class="toc-item bold"><span>1. INTRODUCCIÓN</span><span class="toc-page">3</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>1.1 Objetivos de Desarrollo Sostenible (ODS ONU 2030)</span><span class="toc-page">3</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>1.2 Propósito a partir de los ODS</span><span class="toc-page">3</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>1.3 Alcance a partir de los ODS</span><span class="toc-page">4</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>1.4 Solución y Justificación de la Problemática</span><span class="toc-page">4</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>1.5 Definiciones, Acrónimos y Abreviaciones</span><span class="toc-page">4</span></div>

    <div class="toc-item bold"><span>2. POSICIONAMIENTO</span><span class="toc-page">5</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>2.1 Oportunidad de Negocio</span><span class="toc-page">5</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>2.2 Planteamiento del Problema en Cascada (Mundial, País, Estado y Caso de Estudio)</span><span class="toc-page">5</span></div>

    <div class="toc-item bold"><span>3. PLANEACIÓN</span><span class="toc-page">7</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>3.1 Plan Estratégico (Misión y Visión)</span><span class="toc-page">7</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>3.2 Plan Operativo</span><span class="toc-page">8</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>3.3 Organización SCRUM</span><span class="toc-page">8</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>3.4 Programación del Proyecto: Diagrama de Gantt y PERT (Ruta Crítica)</span><span class="toc-page">9</span></div>

    <div class="toc-item bold"><span>4. SCRUM</span><span class="toc-page">11</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>4.1 Sprint Backlog y Estimación</span><span class="toc-page">11</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>4.2 Burn Down Chart</span><span class="toc-page">11</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>4.3 Product Backlog</span><span class="toc-page">12</span></div>

    <div class="toc-item bold"><span>5. DISEÑO (MATRIZ DE ZACHMAN)</span><span class="toc-page">13</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>5.1 Elementos de la Matriz de Zachman Aplicada</span><span class="toc-page">13</span></div>

    <div class="toc-item bold"><span>6. CARACTERÍSTICAS DEL PRODUCTO Y/O SERVICIO</span><span class="toc-page">14</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>6.1 Requerimientos Funcionales y No Funcionales</span><span class="toc-page">14</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>6.2 Priorización (MoSCoW) y Administración de Cambios</span><span class="toc-page">15</span></div>

    <div class="toc-item bold"><span>7. RESTRICCIONES</span><span class="toc-page">15</span></div>
    <div class="toc-item bold"><span>8. PRUEBAS DE SOFTWARE (5 FORMALES)</span><span class="toc-page">16</span></div>
    <div class="toc-item bold"><span>9. RANGOS DE CALIDAD (ISO/IEC 25010)</span><span class="toc-page">19</span></div>
    <div class="toc-item bold"><span>10. ADMINISTRACIÓN DE RIESGOS</span><span class="toc-page">20</span></div>
    <div class="toc-item bold"><span>11. ADMINISTRACIÓN DE LA SEGURIDAD</span><span class="toc-page">21</span></div>
    <div class="toc-item bold"><span>12. ADMINISTRACIÓN DE SERVICIOS INFORMÁTICOS (ITIL & COBIT)</span><span class="toc-page">22</span></div>
    <div class="toc-item bold"><span>13. REQUERIMIENTOS DE DOCUMENTACIÓN & LOGOTIPO</span><span class="toc-page">23</span></div>
    <div class="toc-item bold"><span>14. REFERENCIAS BIBLIOGRÁFICAS (FORMATO IEEE)</span><span class="toc-page">24</span></div>
  </div>

  <h2 style="margin-top: 25px;">Índice de Ilustraciones</h2>
  <div class="toc-list">
    <div class="toc-item"><span>Ilustración 1: Diagrama Oficial de Alineación ODS ONU 2030</span><span class="toc-page">3</span></div>
    <div class="toc-item"><span>Ilustración 2: Diagrama de Flujo del Plan Estratégico</span><span class="toc-page">7</span></div>
    <div class="toc-item"><span>Ilustración 3: Cronograma Maestro de Actividades (Diagrama de Gantt)</span><span class="toc-page">9</span></div>
    <div class="toc-item"><span>Ilustración 4: Grafo de PERT y Determinación de Ruta Crítica</span><span class="toc-page">10</span></div>
    <div class="toc-item"><span>Ilustración 5: Gráfico de Quemado de Esfuerzo (Burn Down Chart)</span><span class="toc-page">11</span></div>
    <div class="toc-item"><span>Ilustración 6: Diagrama de 5 Capas de Arquitectura de Software</span><span class="toc-page">13</span></div>
    <div class="toc-item"><span>Ilustración 7: Captura Real de Interfaz de Login Seguro con reCAPTCHA</span><span class="toc-page">17</span></div>
    <div class="toc-item"><span>Ilustración 8: Captura Real de Terminal de Punto de Venta POS con Botón Ecológico</span><span class="toc-page">18</span></div>
    <div class="toc-item"><span>Ilustración 9: Matriz Gráfica y Mapa de Evaluación de Riesgos</span><span class="toc-page">20</span></div>
    <div class="toc-item"><span>Ilustración 10: Despliegue Elástico Activo en Google Cloud Platform</span><span class="toc-page">22</span></div>
    <div class="toc-item"><span>Ilustración 11: Emblema y Logotipo Oficial de Monchis Café</span><span class="toc-page">23</span></div>
  </div>

  <h2 style="margin-top: 20px;">Índice de Tablas</h2>
  <div class="toc-list">
    <div class="toc-item"><span>Tabla 1: Matriz de Sprint Backlog y Estimación de Story Points</span><span class="toc-page">11</span></div>
    <div class="toc-item"><span>Tabla 2: Matriz de Zachman Aplicada a Monchis Café (6x4)</span><span class="toc-page">13</span></div>
    <div class="toc-item"><span>Tabla 3: Clasificación y Priorización de Requerimientos MoSCoW</span><span class="toc-page">14</span></div>
    <div class="toc-item"><span>Tabla 4: Reporte Formal de Pruebas de Software (3 Funcionales y 2 No Funcionales)</span><span class="toc-page">16</span></div>
    <div class="toc-item"><span>Tabla 5: Lista de Productos, Servicios y Presupuesto Operativo</span><span class="toc-page">19</span></div>
    <div class="toc-item"><span>Tabla 6: Matriz de Evaluación de Riesgos Inherentes</span><span class="toc-page">20</span></div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- 1. INTRODUCCIÓN -->
<!-- ========================================================================= -->
<div class="page-break">
  <h1>1. Introducción</h1>

  <h2>1.1 Objetivo(s) de Desarrollo Sostenible (ODS ONU 2030)</h2>
  <p>
    El presente proyecto de desarrollo de software formal nace concebido como una herramienta de triple impacto (económico, social y ambiental), alineada de manera explícita con las directrices de la Organización de las Naciones Unidas (ONU) para la Agenda 2030. La industria de la hospitalidad y el expendio de café de especialidad enfrentan severos desafíos de sostenibilidad; por ello, Monchis Café integra en el núcleo de su modelo transaccional los siguientes Objetivos de Desarrollo Sostenible:
  </p>
  <ul>
    <li><strong>ODS 12: Producción y Consumo Responsables (Meta 12.5):</strong> Reducción drástica de la generación de desechos plásticos de un solo uso en entornos urbanos y universitarios. El software incorpora el motor de <em>Sellos Ecológicos Monchis Rewards</em>, que descuenta automáticamente vasos desechables del inventario e incentiva al cliente que presenta termo reusable.</li>
    <li><strong>ODS 8: Trabajo Decente y Crecimiento Económico (Meta 8.3):</strong> Fomento de relaciones comerciales éticas con pequeños productores y cooperativas cafetaleras de Chiapas, Oaxaca y Veracruz, garantizando un margen de ganancia 35% superior mediante trazabilidad directa sin intermediarios abusivos.</li>
    <li><strong>ODS 9: Industria, Innovación e Infraestructura (Meta 9.4):</strong> Adopción de tecnologías cloud-native limpias, microservicios asíncronos en contenedores Docker y escalabilidad elástica en Google Cloud Run con optimización de consumo energético y costos a cero en reposo.</li>
    <li><strong>ODS 16: Paz, Justicia e Instituciones Sólidas (Meta 16.5):</strong> Prevención de fraudes contables, evasión interna y robo hormiga mediante libros de auditoría inmutables protegidos criptográficamente con resúmenes SHA-256 y control de roles RBAC.</li>
  </ul>

  <div class="figure-box">
    <img src="{img_ods}" alt="Alineación ODS ONU 2030 Monchis Café">
    <div class="figure-caption">Ilustración 1: Diagrama Oficial de Alineación a los Objetivos de Desarrollo Sostenible (ODS 12, 8, 9 y 16)</div>
  </div>

  <h2>1.2 Propósito a partir de los ODS</h2>
  <p>
    El propósito fundamental del sistema <strong>Monchis Café</strong> es erradicar la opacidad operativa y el impacto ecológico negativo característico de las cafeterías convencionales. Mediante la digitalización de la cadena de valor —desde la recepción de sacos de café orgánico por cooperativa hasta la emisión del comprobante digital— se busca construir un ecosistema informático ágil y transparente que demuestre que la eficiencia comercial es perfectamente compatible con la preservación del medio ambiente y la dignificación del trabajo rural.
  </p>

  <h2>1.3 Alcance a partir de los ODS</h2>
  <p>
    El alcance del sistema abarca:
  </p>
  <ol>
    <li>Desarrollo de un <strong>Punto de Venta (POS) reactivo</strong> táctil para baristas con despacho de comandas en menos de 3 segundos y cálculo automático de bonos verdes por termo reusable.</li>
    <li>Implementación de un <strong>motor transaccional distribuido</strong> basado en el Patrón Saga con RabbitMQ para garantizar consistencia eventual absoluta entre pedidos, deducción de granos por gramaje y balance financiero.</li>
    <li>Módulo gerencial y de auditoría con tablero analítico para el monitoreo de métricas UTM, cortes de caja ciegos y cálculo del volumen de polipapel mitigado.</li>
    <li>Despliegue e infraestructura en Google Cloud Platform con alta disponibilidad del 99.9% y arquitectura zero-trust protegida con reCAPTCHA Enterprise y JWT asimétrico.</li>
  </ol>

  <h2>1.4 Solución y Justificación de la Problemática</h2>
  <p>
    Frente a la vulnerabilidad de los sistemas POS monolíticos comerciales —que exigen costosas rentas mensuales, dependen de conexiones continuas a bases de datos y carecen de conciencia ecológica—, Monchis Café ofrece una arquitectura desacoplada y orientada a eventos. Si se interrumpe la conexión a internet en la barra, el sistema sigue operando mediante almacenamiento local seguro y sincroniza la compensación transaccional al reanudarse el enlace, eliminando por completo las órdenes perdidas y el descuadre de inventarios.
  </p>

  <h2>1.5 Definiciones, Acrónimos y Abreviaciones</h2>
  <ul>
    <li><strong>ACID:</strong> Atomicidad, Consistencia, Aislamiento y Durabilidad (propiedades de la base de datos relacional).</li>
    <li><strong>AMQP:</strong> Advanced Message Queuing Protocol (protocolo de mensajería asíncrona implementado en RabbitMQ).</li>
    <li><strong>DLQ:</strong> Dead Letter Queue (cola de mensajes no procesables para análisis de fallos en el bus de eventos).</li>
    <li><strong>JWT:</strong> JSON Web Token (estándar criptográfico RFC 7519 para intercambio seguro de información de identidad).</li>
    <li><strong>ODS:</strong> Objetivos de Desarrollo Sostenible de la Organización de las Naciones Unidas.</li>
    <li><strong>POS:</strong> Point of Sale (Punto de Venta interactivo para cajeros y baristas).</li>
    <li><strong>RBAC:</strong> Role-Based Access Control (Control de Acceso Basado en Roles).</li>
    <li><strong>Saga:</strong> Patrón de diseño de software para transacciones distribuidas con acciones compensatorias.</li>
    <li><strong>SHA-256:</strong> Secure Hash Algorithm de 256 bits utilizado en la firma inmutable de auditoría.</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- 2. POSICIONAMIENTO -->
<!-- ========================================================================= -->
<div class="page-break">
  <h1>2. Posicionamiento</h1>

  <h2>2.1 Oportunidad de Negocio</h2>
  <p>
    El auge de la cultura del café de especialidad ha transformado el hábito de consumo en jóvenes universitarios y profesionistas urbanos, quienes demandan alimentos de alta calidad y demuestran una elevada disposición a premiar negocios con prácticas ecológicas y de comercio justo. Las pequeñas y medianas barras de café carecen de soluciones tecnológicas hechas a la medida: se ven forzadas a utilizar hojas de cálculo propensas a errores o sistemas heredados que tratan al café como un abarrotes genérico, sin distinguir variedades botánicas, tostados ni mermas por calibración del molino. Monchis Café capitaliza esta oportunidad ofreciendo un software moderno, escalable y con una narrativa sustentable que fideliza al consumidor.
  </p>

  <h2>2.2 Planteamiento del Problema en Cascada</h2>
  <p>
    Para dimensionar con rigor técnico y social la pertinencia del sistema, el problema se estructura en una cascada descendente de cuatro niveles:
  </p>

  <h3>Nivel 1: Problemática a Nivel Mundial</h3>
  <p>
    A escala global, la industria cafetalera enfrenta una crisis dual. Por un lado, la volatilidad de los precios en las bolsas de materias primas estrangula la supervivencia económica de más de 25 millones de familias productoras, capturando los intermediarios multinacionales hasta el 85% del valor de la taza servida. Por otro lado, el consumo descartable produce más de <strong>500 mil millones de vasos de un solo uso anualmente</strong>, los cuales, al contener películas plásticas internas de polietileno, resultan prácticamente imposibles de reciclar y terminan contaminando mantos acuíferos y ecosistemas marinos.
  </p>

  <h3>Nivel 2: Problemática a Nivel País (México)</h3>
  <p>
    México se posiciona como el 9.º productor mundial de café y líder histórico en producción orgánica bajo sombra (particularmente en los estados de Chiapas, Veracruz y Oaxaca). No obstante, los caficultores nacionales operan en condiciones de extrema vulnerabilidad financiera. En los centros de consumo masivo del país, las cadenas de cafeterías comerciales comercializan mezclas importadas de baja calidad etiquetándolas falsamente como café nacional de altura, engañando al consumidor por falta de plataformas tecnológicas de trazabilidad verificable de los lotes.
  </p>

  <h3>Nivel 3: Problemática a Nivel Estado (Jalisco y Zona Metropolitana de Guadalajara)</h3>
  <p>
    En el estado de Jalisco, particularmente en la Zona Metropolitana de Guadalajara (ZMG), el crecimiento de cafeterías de barrio y barras universitarias ha sido exponencial en los últimos cinco años. A pesar de la entrada en vigor de la Ley Estatal del Equilibrio Ecológico y Protección al Ambiente que restringe los plásticos de un solo uso, los establecimientos comerciales continúan despachando recipientes desechables debido a que sus sistemas de punto de venta no cuentan con módulos automatizados para gestionar depósitos de vasos reusables ni recompensar monetariamente al comensal ecológico.
  </p>

  <h3>Nivel 4: Problemática en el Caso de Estudio (Monchis Café en CUTonalá)</h3>
  <p>
    En el caso de estudio de <strong>Monchis Café</strong>, operando en el ecosistema estudiantil del Centro Universitario de Tonalá (CUTonalá):
  </p>
  <ul>
    <li><strong>Descuadres Financieros:</strong> El registro en comandas manuales de papel originaba hasta un <strong>18% de discrepancia</strong> entre el efectivo en caja y el inventario real al término de cada turno de barista.</li>
    <li><strong>Merma Oculta de Granos:</strong> No existía cálculo de los gramos exactos empleados por extracción (18 g para un espresso doble Chiapas vs 30 g para un macerado Cold Brew de 18 horas), lo que impedía conocer el costo unitario de producción.</li>
    <li><strong>Saturación de Basura en Campus:</strong> Se generaban semanalmente cientos de vasos y tapas de plástico en los contenedores del centro universitario por la falta de un incentivo gamificado que motivara a estudiantes y docentes a llevar sus propios cilindros o termos.</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- 3. PLANEACIÓN -->
<!-- ========================================================================= -->
<div class="page-break">
  <h1>3. Planeación</h1>

  <h2>3.1 Plan Estratégico (Misión y Visión)</h2>
  <p>
    <strong>Misión:</strong> Proveer a Monchis Café de un sistema informático integral, confiable y seguro que digitalice sus transacciones comerciales en barra, optimice el uso de inventarios agrícolas y promueva activamente hábitos de consumo ecológico y ético en la comunidad universitaria.
  </p>
  <p>
    <strong>Visión:</strong> Consolidarse como la plataforma de referencia en el Centro Universitario de Tonalá y en la Red Universitaria de la UdeG para la gestión inteligente de unidades de hospitalidad sustentable, demostrando la viabilidad de la tecnología Serverless y la trazabilidad agroecológica.
  </p>

  <div class="figure-box">
    <img src="{img_plan_est}" alt="Plan Estratégico Monchis Café">
    <div class="figure-caption">Ilustración 2: Diagrama de Flujo del Plan Estratégico en 3 Fases de Ingeniería</div>
  </div>

  <h2>3.2 Plan Operativo</h2>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 20%;">Actividad</th>
        <th style="width: 25%;">Responsable</th>
        <th style="width: 55%;">Descripción y Entregables Operativos</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1. Gestión del Repositorio</strong></td>
        <td>Ernesto Hatuey Fierro M.</td>
        <td>Monorepo Turborepo con ramas <code>master</code>, <code>develop</code> y feature branches. Conexión de CI/CD con GitHub Actions.</td>
      </tr>
      <tr>
        <td><strong>2. Modelo de Datos Relacional</strong></td>
        <td>Equipo 2</td>
        <td>Diseño E-R en PostgreSQL, esquema tipado en Prisma ORM, control de migraciones y semillas con 16 productos iniciales.</td>
      </tr>
      <tr>
        <td><strong>3. API Gateway y Core</strong></td>
        <td>Ernesto Hatuey Fierro M.</td>
        <td>Endpoints REST en Next.js 14, autenticación asimétrica JWT RS256, bcrypt salt 12 y filtro anti-bot reCAPTCHA Enterprise.</td>
      </tr>
      <tr>
        <td><strong>4. Bus Asíncrono RabbitMQ</strong></td>
        <td>Equipo 2</td>
        <td>Colas distribuidas, orquestación del Patrón Saga, transacciones compensatorias y Dead Letter Queue (DLQ).</td>
      </tr>
      <tr>
        <td><strong>5. Interfaz Táctil POS</strong></td>
        <td>Equipo 2</td>
        <td>Frontend en Vue 3 con Vite, Pinia State, Tailwind CSS, carrito reactivo y botón ecológico (+1 sello Monchis Rewards).</td>
      </tr>
      <tr>
        <td><strong>6. Aseguramiento de Calidad</strong></td>
        <td>Ernesto Hatuey Fierro M.</td>
        <td>77 pruebas unitarias Vitest, 19 pruebas de humo de laboratorio y pruebas de carga concurrente en GCP.</td>
      </tr>
      <tr>
        <td><strong>7. Despliegue en la Nube</strong></td>
        <td>Equipo 2</td>
        <td>Contenedores Docker multi-stage desplegados en Google Cloud Run y Cloud SQL con SSL y Cloud Monitoring.</td>
      </tr>
    </tbody>
  </table>

  <h2>3.3 Organización SCRUM</h2>
  <p>
    El desarrollo del proyecto se ejecutó siguiendo el marco ágil <strong>SCRUM</strong> estructurado en 4 Sprints de 2 semanas de duración cada uno. Los roles se distribuyeron de la siguiente forma:
  </p>
  <ul>
    <li><strong>Product Owner:</strong> Ernesto Hatuey Fierro Meléndez (Representación de stakeholders, definición y priorización de User Stories conforme a la Agenda ODS).</li>
    <li><strong>Scrum Master:</strong> Ernesto Hatuey Fierro Meléndez (Gestión del flujo ágil, eliminación de bloqueadores técnicos y moderación de Daily Scrums).</li>
    <li><strong>Development Team:</strong> Equipo 2 de Ingeniería de Software (Arquitectura backend, desarrollo frontend reactivo, seguridad y pruebas de laboratorio).</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- PROGRAMACIÓN: GANTT Y PERT -->
<!-- ========================================================================= -->
<div class="page-break">
  <h2>3.4 Programación del Proyecto: Diagrama de Gantt y PERT (Ruta Crítica)</h2>
  <p>
    El cronograma maestro de desarrollo abarcó un horizonte temporal de 14 semanas lectivas durante el ciclo 2026B. A continuación se presentan las representaciones gráficas del Diagrama de Gantt y del Grafo de PERT determinando la Ruta Crítica del software:
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
    <strong>Determinación de la Ruta Crítica:</strong> Como se observa en la Ilustración 4, la secuencia de actividades críticas con holgura nula (Slack = 0) corresponde a:
    <br>
    <code>Actividad A (Requerimientos ODS) → Actividad B (Zachman) → Actividad C (RabbitMQ Saga) → Actividad D (POS UI) → Actividad E (Pruebas de Humo) → Actividad G (Cloud Run)</code>, sumando una duración inamovible de <strong>14 semanas</strong>. La actividad de documentación de manuales (Actividad F) contó con una holgura libre de 3 semanas, ejecutándose en paralelo sin comprometer el hito de entrega en ExpoDIT.
  </p>
</div>

<!-- ========================================================================= -->
<!-- 4. SCRUM -->
<!-- ========================================================================= -->
<div class="page-break">
  <h1>4. SCRUM</h1>

  <h2>4.1 Sprint Backlog y Estimación de Story Points</h2>
  <p>
    En el Sprint 4 (Fase de Consolidación y Pruebas), se abordaron 40 Puntos de Historia (Story Points) estimados mediante Planning Poker con la serie de Fibonacci:
  </p>

  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 12%;">ID Historia</th>
        <th style="width: 45%;">Descripción de la Historia de Usuario</th>
        <th style="width: 15%;">Story Points</th>
        <th style="width: 15%;">Prioridad</th>
        <th style="width: 13%;">Estado</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>US-01</strong></td>
        <td>Como Barista, deseo un POS táctil para registrar cobros en menos de 3 segundos.</td>
        <td>8 SP</td>
        <td>Alta</td>
        <td><span class="badge-tag pass">DONE</span></td>
      </tr>
      <tr>
        <td><strong>US-02</strong></td>
        <td>Como Cliente, deseo registrar mi termo reusable para ganar sellos ecológicos.</td>
        <td>5 SP</td>
        <td>Alta</td>
        <td><span class="badge-tag pass">DONE</span></td>
      </tr>
      <tr>
        <td><strong>US-03</strong></td>
        <td>Como Arquitecto, deseo que RabbitMQ compense órdenes si falla la base de datos.</td>
        <td>13 SP</td>
        <td>Crítica</td>
        <td><span class="badge-tag pass">DONE</span></td>
      </tr>
      <tr>
        <td><strong>US-04</strong></td>
        <td>Como Administrador, deseo bloquear logins sospechosos mediante reCAPTCHA v3.</td>
        <td>8 SP</td>
        <td>Alta</td>
        <td><span class="badge-tag pass">DONE</span></td>
      </tr>
      <tr>
        <td><strong>US-05</strong></td>
        <td>Como Auditor, deseo ver el corte contable diario protegido con firma SHA-256.</td>
        <td>6 SP</td>
        <td>Media</td>
        <td><span class="badge-tag pass">DONE</span></td>
      </tr>
    </tbody>
  </table>

  <h2>4.2 Burn Down Chart</h2>
  <p>
    El gráfico de quemado de esfuerzo refleja una correlación casi perfecta entre la línea de velocidad ideal y el avance real del equipo a lo largo de los 10 días hábiles del sprint, completando el 100% de los 40 puntos de historia asignados:
  </p>

  <div class="figure-box">
    <img src="{img_burndown}" alt="Burn Down Chart Oficial">
    <div class="figure-caption">Ilustración 5: Gráfico de Quemado de Esfuerzo (Burn Down Chart - Sprint 4: 40 Story Points)</div>
  </div>

  <h2>4.3 Product Backlog</h2>
  <p>
    El Product Backlog general acumuló 24 historias de usuario priorizadas de acuerdo a su aporte de valor al negocio de Monchis Café y a la mitigación de los riesgos identificados en la matriz de Zachman.
  </p>
</div>

<!-- ========================================================================= -->
<!-- 5. DISEÑO (MATRIZ DE ZACHMAN) -->
<!-- ========================================================================= -->
<div class="page-break">
  <h1>5. Diseño (Matriz de Zachman)</h1>

  <h2>5.1 Elementos de la Matriz de Zachman Aplicada a Monchis Café</h2>
  <p>
    Para garantizar que la arquitectura responda a las necesidades de todas las partes interesadas, se empleó el Marco de Zachman estructurado en 6 interrogantes ontológicas a través de 4 niveles de abstracción:
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

  <div class="figure-box">
    <img src="{img_arch}" alt="Arquitectura del Sistema Monchis Café">
    <div class="figure-caption">Ilustración 6: Diagrama Oficial de 5 Capas de Arquitectura de Software Monchis Café</div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- 6. CARACTERÍSTICAS DEL PRODUCTO Y RESTRICCIONES -->
<!-- ========================================================================= -->
<div class="page-break">
  <h1>6. Características del Producto y/o Servicio</h1>

  <h2>6.1 Requerimientos Funcionales y No Funcionales (MoSCoW)</h2>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 10%;">ID</th>
        <th style="width: 25%;">Clasificación</th>
        <th style="width: 50%;">Descripción del Requerimiento</th>
        <th style="width: 15%;">Prioridad</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>RF-01</strong></td>
        <td>Ventas en Barra</td>
        <td>El sistema debe permitir la adición reactiva de bebidas con desglose de precios en tiempo real.</td>
        <td><strong>Must Have</strong></td>
      </tr>
      <tr>
        <td><strong>RF-02</strong></td>
        <td>Monchis Rewards</td>
        <td>Al seleccionar "Trae termo reusable", se debe bonificar 1 sello verde y descontar 0 vasos desechables.</td>
        <td><strong>Must Have</strong></td>
      </tr>
      <tr>
        <td><strong>RF-03</strong></td>
        <td>Trazabilidad de Grano</td>
        <td>El sistema debe asociar cada lote de café a su cooperativa productora de origen (Chiapas/Veracruz).</td>
        <td><strong>Must Have</strong></td>
      </tr>
      <tr>
        <td><strong>RF-04</strong></td>
        <td>Descuento por Receta</td>
        <td>Cada venta debe descontar los gramos exactos de insumo (18g espresso / 30g cold brew).</td>
        <td><strong>Should Have</strong></td>
      </tr>
      <tr>
        <td><strong>RF-05</strong></td>
        <td>Corte de Caja Ciego</td>
        <td>El barista debe ingresar el efectivo contado sin ver el saldo teórico del sistema.</td>
        <td><strong>Should Have</strong></td>
      </tr>
      <tr>
        <td><strong>RNF-01</strong></td>
        <td>Rendimiento</td>
        <td>El tiempo de respuesta de los endpoints API no debe superar los 200 ms bajo carga normal.</td>
        <td><strong>Must Have</strong></td>
      </tr>
      <tr>
        <td><strong>RNF-02</strong></td>
        <td>Disponibilidad</td>
        <td>La plataforma debe garantizar una disponibilidad del 99.9% en Google Cloud Run.</td>
        <td><strong>Must Have</strong></td>
      </tr>
      <tr>
        <td><strong>RNF-03</strong></td>
        <td>Seguridad</td>
        <td>Las contraseñas deben estar cifradas con bcrypt salt 12 y las peticiones protegidas por reCAPTCHA.</td>
        <td><strong>Must Have</strong></td>
      </tr>
      <tr>
        <td><strong>RNF-04</strong></td>
        <td>Tolerancia a Fallos</td>
        <td>El bus RabbitMQ debe retener mensajes en colas persistentes (DLQ) si la base de datos se desconecta.</td>
        <td><strong>Must Have</strong></td>
      </tr>
    </tbody>
  </table>

  <h2>6.2 Administración y Control de Cambios</h2>
  <p>
    Toda solicitud de cambio sobre los requerimientos se gestionó mediante el repositorio oficial de GitHub bajo el flujo GitFlow. Los cambios propuestos debían ser aprobados por el Product Owner tras evaluar su impacto en el presupuesto y en la fecha límite de ExpoDIT. Los requerimientos rechazados (como la pasarela física con hardware biométrico) se documentaron en el archivo <code>PENDIENTES.md</code> del repositorio para su posterior desarrollo.
  </p>

  <h1>7. Restricciones</h1>
  <ul>
    <li><strong>Restricción de Alcance:</strong> En su fase inicial, la plataforma atiende exclusivamente las operaciones de barra y administración de Monchis Café en las instalaciones del Centro Universitario de Tonalá.</li>
    <li><strong>Restricción de Tiempo:</strong> El proyecto cuenta con una fecha límite de entrega e integración inaplazable: 20 de noviembre de 2026 a las 23:59 horas.</li>
    <li><strong>Restricción Tecnológica:</strong> El sistema debe ejecutarse sobre navegadores modernos sin requerir software propietario adicional en las terminales táctiles del personal.</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- 8. PRUEBAS DE SOFTWARE (5 FORMALES) -->
<!-- ========================================================================= -->
<div class="page-break">
  <h1>8. Pruebas de Software (5 Reportes Formales)</h1>
  <p>
    Conforme a las directrices de evaluación del Dr. Gabriel Navarro Salcedo, se ejecutaron <strong>5 pruebas formales</strong> (3 funcionales y 2 no funcionales) bajo el formato estricto de aseguramiento de calidad de laboratorio de software:
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
      <td colspan="3">Evaluar la efectividad del filtrado de reCAPTCHA Enterprise, autenticación JWT asimétrica y redirección condicional por rol de usuario.</td>
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
    <div class="figure-caption">Ilustración 7: Captura Real de Interfaz de Login Seguro con reCAPTCHA y Validación en Tiempo Real</div>
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
      <td colspan="3">Comprobar el cálculo de montos en carrito reactivo, soporte multimétodo de pago y descuento automático de gramos de café por receta.</td>
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
<!-- 9. RANGOS DE CALIDAD (ISO 25010) -->
<!-- ========================================================================= -->
<div class="page-break">
  <h1>9. Rangos de Calidad</h1>
  <p>
    La calidad del sistema fue evaluada conforme a la norma internacional <strong>ISO/IEC 25010</strong>, cubriendo las 5 subcaracterísticas primordiales:
  </p>
  <ul>
    <li><strong>Eficiencia de Desempeño:</strong> Latencia promedio de 142 ms en consultas de catálogo y consumo de memoria inferior a 128 MB por instancia en Cloud Run.</li>
    <li><strong>Usabilidad:</strong> Curva de aprendizaje de baristas reducida a menos de 5 minutos gracias a la paleta cálida pastel, botones táctiles y tipografía de alta legibilidad.</li>
    <li><strong>Portabilidad:</strong> Compatibilidad multiplataforma garantizada en navegadores Chrome, Firefox, Safari y Edge, adaptándose a tablets táctiles y computadoras de escritorio.</li>
    <li><strong>Funcionalidad:</strong> Cumplimiento del 100% de los requerimientos funcionales del caso de estudio (POS, trazabilidad, lealtad y cortes de caja).</li>
    <li><strong>Mantenibilidad:</strong> Arquitectura monorepo tipada con TypeScript, separación estricta de capas y cobertura de 77 pruebas unitarias automatizadas.</li>
  </ul>

  <h2>9.1 Lista de Productos, Servicios y Presupuesto Operativo</h2>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 25%;">Categoría</th>
        <th style="width: 45%;">Descripción del Recurso / Proveedor</th>
        <th style="width: 15%;">Costo Mensual</th>
        <th style="width: 15%;">Inversión Anual</th>
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
<!-- 10. ADMINISTRACIÓN DE RIESGOS -->
<!-- ========================================================================= -->
<div class="page-break">
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
<!-- 11. SEGURIDAD Y 12. SERVICIOS INFORMÁTICOS -->
<!-- ========================================================================= -->
<div class="page-break">
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
<!-- 13. DOCUMENTACIÓN, LOGOTIPO Y 14. REFERENCIAS IEEE -->
<!-- ========================================================================= -->
<div class="page-break">
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
  <ol style="font-size: 9pt; line-height: 1.6;">
    <li>[1] United Nations, "Transforming our world: the 2030 Agenda for Sustainable Development," Resolution adopted by the General Assembly, A/RES/70/1, Oct. 2015.</li>
    <li>[2] J. A. Zachman, "A framework for information systems architecture," <em>IBM Systems Journal</em>, vol. 26, no. 3, pp. 276-292, 1987.</li>
    <li>[3] C. Richardson, <em>Microservices Patterns: With examples in Java</em>, Shelter Island, NY: Manning Publications, 2018.</li>
    <li>[4] ISO/IEC, "Systems and software engineering - Systems and software Quality Requirements and Evaluation (SQuaRE) - System and software quality models," ISO/IEC 25010:2011, 2011.</li>
    <li>[5] OWASP Foundation, "OWASP Top 10: 2021 The Ten Most Critical Web Application Security Risks," Open Web Application Security Project, 2021. [Online]. Available: https://owasp.org/Top10/</li>
    <li>[6] AXELOS, <em>ITIL Foundation: ITIL 4 Edition</em>, London, UK: TSO (The Stationery Office), 2019.</li>
    <li>[7] ISACA, <em>COBIT 2019 Framework: Introduction and Methodology</em>, Schaumburg, IL: ISACA, 2018.</li>
    <li>[8] Google Cloud, "Google Cloud Run Documentation: Serverless Container Execution," Mountain View, CA: Google Inc., 2024. [Online]. Available: https://cloud.google.com/run/docs</li>
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
print("Compiling PDF with Chrome Headless...")
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

dest_pdf_downloads = os.path.join(DOWNLOADS_DIR, "Proyecto_Integrador_Final_Monchis_Cafe.pdf")
shutil.copy2(pdf_path, dest_pdf_downloads)
print(f"PDF copied to Downloads: {dest_pdf_downloads}")

# =========================================================================
# GENERATE DOCX (python-docx)
# =========================================================================
print("Generating DOCX version for Master Final Document...")
doc = docx.Document()

# Page Margins
for section in doc.sections:
    section.top_margin = Inches(0.9)
    section.bottom_margin = Inches(0.9)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)

# Cover
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("UNIVERSIDAD DE GUADALAJARA\nCENTRO UNIVERSITARIO DE TONALÁ\nLICENCIATURA EN INGENIERÍA EN CIENCIAS COMPUTACIONALES\n\n")
run.font.bold = True
run.font.size = Pt(13)
run.font.color.rgb = RGBColor(26, 54, 93)

run = p.add_run("PROYECTO INTEGRADOR EN EL DESARROLLO DE SOFTWARE\nPROYECTO FINAL — EXPODIT 2026\n\n")
run.font.bold = True
run.font.size = Pt(18)
run.font.color.rgb = RGBColor(140, 107, 82)

run = p.add_run("MONCHIS CAFÉ\nSistema Web de Gestión Segura, Punto de Venta Distribuido y Trazabilidad Agroecológica\n\n")
run.font.bold = True
run.font.size = Pt(15)
run.font.color.rgb = RGBColor(47, 133, 90)

run = p.add_run("Estudiante: Ernesto Hatuey Fierro Meléndez (Código: 223977036)\nEquipo 2\nProfesor Titular: Dr. Gabriel Navarro Salcedo\nNoviembre de 2026\n")
run.font.size = Pt(11)

doc.add_page_break()

# Sections
sections_data = [
    ("1. Introducción", "El presente proyecto de desarrollo de software formal nace concebido como una herramienta de triple impacto (económico, social y ambiental), alineada de manera explícita con los ODS 12, 8, 9 y 16 de la Agenda 2030 de la ONU. La plataforma erradica la opacidad de los inventarios de café de altura, conecta con cooperativas de Chiapas y evita miles de vasos plásticos mediante el motor Monchis Rewards."),
    ("2. Posicionamiento", "El planteamiento del problema se estructura en una cascada de cuatro niveles: crisis mundial de desechables de polipapel, comercio injusto en México hacia caficultores independientes, incumplimiento normativo en Jalisco sobre plásticos de un solo uso, y descontrol de mermas y arqueos de caja en Monchis Café CUTonalá."),
    ("3. Planeación", "Se implementa un Plan Estratégico basado en misión y visión, un Plan Operativo con asignación clara de responsabilidades, organización bajo el marco ágil SCRUM, y programación de 14 semanas mediante Diagrama de Gantt y Grafo de PERT determinando la Ruta Crítica de holgura cero."),
    ("4. SCRUM", "Se completaron 4 Sprints quincenales. El Sprint Backlog del Sprint 4 abarcó 40 Story Points verificados en el Burn Down Chart con una velocidad óptima de entrega."),
    ("5. Diseño (Matriz de Zachman)", "Se estructuró la Matriz de Zachman (6 interrogantes x 4 niveles de abstracción), vinculando cada decisión técnica con datos, funciones, topología de red, actores RBAC, tiempos y motivación."),
    ("6. Características del Producto y Restricciones", "Se tabularon los requerimientos funcionales y no funcionales bajo la priorización MoSCoW, destacando la resiliencia Saga en RabbitMQ, el POS reactivo y las restricciones de tiempo y alcance institucional."),
    ("7. Pruebas de Software (5 Formales)", "Se ejecutaron 5 reportes formales de aseguramiento de calidad (3 funcionales y 2 no funcionales): Login y RBAC, Punto de Venta con mermas por gramaje, Monchis Rewards ecológico, Resiliencia Saga y Concurrencia en Google Cloud Run. 100% de casos aprobatorios."),
    ("8. Rangos de Calidad (ISO/IEC 25010)", "Evaluación exhaustiva de eficiencia (<200ms latencia), usabilidad pastel intuitiva, portabilidad web, funcionalidad completa y mantenibilidad monorepo."),
    ("9. Administración de Riesgos", "Matriz y mapa de riesgos mitigando caídas de red, sobrecargas de concurrencia y descuadres de caja mediante auditoría inmutable SHA-256."),
    ("10. Seguridad y Servicios Informáticos (ITIL & COBIT)", "Cumplimiento de estándares bancarios OWASP Top 10, ISO 27001, ITIL v4 para soporte y entrega, y catálogo de documentación COBIT con despliegue en Google Cloud Platform."),
    ("11. Referencias Bibliográficas (Formato IEEE)", "[1] United Nations ODS 2030.\n[2] J. A. Zachman, IBM Systems Journal, 1987.\n[3] C. Richardson, Microservices Patterns, 2018.\n[4] ISO/IEC 25010:2011.\n[5] OWASP Top 10: 2021.\n[6] AXELOS ITIL 4, 2019.\n[7] ISACA COBIT 2019.\n[8] Google Cloud Run Documentation, 2024.")
]

for title, content in sections_data:
    doc.add_heading(title, level=1)
    doc.add_paragraph(content)

doc.save(docx_path)
print(f"DOCX master document generated: {docx_path}")

dest_docx_downloads = os.path.join(DOWNLOADS_DIR, "Proyecto_Integrador_Final_Monchis_Cafe.docx")
shutil.copy2(docx_path, dest_docx_downloads)
print(f"DOCX copied to Downloads: {dest_docx_downloads}")

# =========================================================================
# PACKAGING FINAL ZIP ARCHIVE
# =========================================================================
zip_path = os.path.join(DOWNLOADS_DIR, "EXPODIT_2026_Equipo2_Monchis_Cafe.zip")
print(f"Creating complete delivery ZIP archive: {zip_path}...")

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # 1. Presentations
    zipf.write(os.path.join(DOWNLOADS_DIR, "Presentacion_ExpoDIT_Monchis_Cafe.pdf"), "1_Presentacion/Presentacion_ExpoDIT_Monchis_Cafe.pdf")
    zipf.write(os.path.join(DOWNLOADS_DIR, "Presentacion_ExpoDIT_Monchis_Cafe.pptx"), "1_Presentacion/Presentacion_ExpoDIT_Monchis_Cafe.pptx")
    # 2. Pitch Script
    zipf.write(os.path.join(DOWNLOADS_DIR, "Guion_Video_Pitch_ExpoDIT_Monchis_Cafe.pdf"), "2_Video_Pitch/Guion_Video_Pitch_ExpoDIT_Monchis_Cafe.pdf")
    zipf.write(os.path.join(DOCS_DIR, "../presentacion/expodit/Guion_Video_Pitch_ExpoDIT_Monchis_Cafe.md"), "2_Video_Pitch/Guion_Video_Pitch_ExpoDIT_Monchis_Cafe.md")
    # 3. Master Project Document
    zipf.write(os.path.join(DOWNLOADS_DIR, "Proyecto_Integrador_Final_Monchis_Cafe.pdf"), "3_Documento_Final/Proyecto_Integrador_Final_Monchis_Cafe.pdf")
    zipf.write(os.path.join(DOWNLOADS_DIR, "Proyecto_Integrador_Final_Monchis_Cafe.docx"), "3_Documento_Final/Proyecto_Integrador_Final_Monchis_Cafe.docx")
    # 4. Smoke Tests Report
    zipf.write(os.path.join(DOWNLOADS_DIR, "Reporte_Pruebas_de_Humo_Monchis_Cafe.pdf"), "4_Pruebas_de_Humo/Reporte_Pruebas_de_Humo_Monchis_Cafe.pdf")
    zipf.write(os.path.join(DOWNLOADS_DIR, "Reporte_Pruebas_de_Humo_Monchis_Cafe.docx"), "4_Pruebas_de_Humo/Reporte_Pruebas_de_Humo_Monchis_Cafe.docx")
    # 5. Graphical Assets
    for k, p in raw_paths.items():
        if os.path.exists(p):
            zipf.write(p, f"5_Diagramas_y_Evidencias/{os.path.basename(p)}")

print(f"Complete delivery package created successfully: {zip_path}")
print("\nALL EXPODIT DELIVERABLES GENERATED AND READY!")
