import os
import sys
import base64
import subprocess
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

EXPODIT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(EXPODIT_DIR, "..", "..", ".."))
ASSETS_DIR = os.path.join(EXPODIT_DIR, "assets")
DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

# Browser detection for headless PDF generation (Edge / Chrome)
possible_browsers = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]
BROWSER_PATH = next((p for p in possible_browsers if os.path.exists(p)), None)

# Helper to read base64 image
def get_base64_img(path):
    if not os.path.isabs(path):
        full_path = os.path.normpath(os.path.join(PROJECT_ROOT, path))
    else:
        full_path = path
    if not os.path.exists(full_path):
        full_path = os.path.normpath(os.path.join(EXPODIT_DIR, path))
        if not os.path.exists(full_path):
            print(f"Warning: image not found: {full_path}")
            return ""
    with open(full_path, "rb") as f:
        data = f.read()
    ext = os.path.splitext(full_path)[1].lower().replace(".", "")
    if ext == "jpg":
        ext = "jpeg"
    return f"data:image/{ext};base64,{base64.b64encode(data).decode('utf-8')}"

raw_paths = {
    "udg": os.path.normpath(os.path.join(PROJECT_ROOT, r"docs\entregables\img\escudo_udg_oficial.png")),
    "monchis": os.path.normpath(os.path.join(PROJECT_ROOT, r"docs\entregables\monchis_logo_badge.png")),
    "arch": os.path.normpath(os.path.join(EXPODIT_DIR, r"assets\diagrama_arquitectura_monchis.png")),
    "ods": os.path.normpath(os.path.join(EXPODIT_DIR, r"assets\diagrama_ods_monchis.png")),
    "notion": os.path.normpath(os.path.join(EXPODIT_DIR, r"assets\tablero_notion_monchis.png")),
    "login": os.path.normpath(os.path.join(PROJECT_ROOT, r"docs\entregables\img\evidencia4_login.png")),
    "pos": os.path.normpath(os.path.join(PROJECT_ROOT, r"docs\entregables\img\evidencia3_pos.png")),
    "admin": os.path.normpath(os.path.join(PROJECT_ROOT, r"docs\entregables\img\evidencia5_admin.png")),
    "web": os.path.normpath(os.path.join(PROJECT_ROOT, r"docs\entregables\img\m3_despliegue_web.png")),
}

img_udg = get_base64_img(raw_paths["udg"])
img_monchis = get_base64_img(raw_paths["monchis"])
img_arch = get_base64_img(raw_paths["arch"])
img_ods = get_base64_img(raw_paths["ods"])
img_notion = get_base64_img(raw_paths["notion"])
img_login = get_base64_img(raw_paths["login"])
img_pos = get_base64_img(raw_paths["pos"])
img_admin = get_base64_img(raw_paths["admin"])
img_web = get_base64_img(raw_paths["web"])

NOTION_BOARD_URL = "https://app.notion.com/p/423f4201a73581ab8e7cc80ff7b771fe"

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Presentación ExpoDIT 2026 - Monchis Café</title>
<style>
  @page {{
    size: 16in 9in;
    margin: 0;
  }}
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', system-ui, -apple-system, Roboto, Helvetica, Arial, sans-serif;
  }}
  body {{
    background: #4B3B33;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .slide {{
    width: 16in;
    height: 9in;
    max-width: 16in;
    max-height: 9in;
    overflow: hidden;
    background: #FBF1EC;
    position: relative;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 0.55in 0.8in 0.45in 0.8in;
  }}

  /* Top decorative brand bar */
  .slide::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 8px;
    background: linear-gradient(90deg, #C97567 0%, #E08D80 35%, #7C9473 70%, #4B3B33 100%);
  }}

  /* Header */
  .slide-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 2px solid #E8DCD4;
    padding-bottom: 0.16in;
    margin-bottom: 0.2in;
  }}
  .header-titles {{
    flex: 1;
  }}
  .header-badge {{
    display: inline-block;
    background: #F3D9D3;
    color: #9E3E30;
    font-size: 10.5pt;
    font-weight: 800;
    padding: 3px 12px;
    border-radius: 12px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 4px;
    border: 1px solid #E5C3BB;
  }}
  .header-title {{
    font-size: 25pt;
    font-weight: 900;
    color: #4B3B33;
    line-height: 1.15;
    letter-spacing: -0.5px;
  }}
  .header-subtitle {{
    font-size: 12.5pt;
    color: #8A776D;
    font-weight: 600;
    margin-top: 3px;
  }}
  .header-logos {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}
  .header-logos img {{
    height: 50px;
    object-fit: contain;
  }}

  /* Content area */
  .slide-body {{
    flex: 1;
    display: flex;
    gap: 0.35in;
    align-items: stretch;
    min-height: 0;
  }}

  /* Footer */
  .slide-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1.5px solid #E8DCD4;
    padding-top: 0.12in;
    margin-top: 0.15in;
    font-size: 10pt;
    color: #8A776D;
    font-weight: 600;
  }}
  .slide-footer .student-info {{
    display: flex;
    gap: 12px;
    align-items: center;
  }}
  .slide-footer .pill {{
    background: #F3D9D3;
    color: #9E3E30;
    padding: 2px 8px;
    border-radius: 6px;
    font-weight: 800;
    font-size: 9pt;
  }}

  /* Slide 1: Cover */
  .cover-slide {{
    background: linear-gradient(135deg, #FBF1EC 0%, #F5E6DE 55%, #EED7CC 100%);
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 0.7in 1in;
  }}
  .cover-top {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 40px;
    margin-bottom: 18px;
  }}
  .cover-top img.logo-udg {{
    height: 88px;
  }}
  .cover-top img.logo-monchis {{
    height: 94px;
  }}
  .cover-badge-event {{
    display: inline-block;
    background: #C97567;
    color: #FFFFFF;
    font-size: 12pt;
    font-weight: 800;
    padding: 6px 24px;
    border-radius: 20px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(201, 117, 103, 0.25);
  }}
  .cover-title {{
    font-size: 42pt;
    font-weight: 900;
    color: #4B3B33;
    line-height: 1.12;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
  }}
  .cover-title span {{
    color: #C97567;
  }}
  .cover-subtitle {{
    font-size: 16.5pt;
    font-weight: 600;
    color: #5B4A41;
    max-width: 1050px;
    margin: 0 auto 24px auto;
    line-height: 1.35;
  }}
  .cover-meta-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    width: 100%;
    max-width: 1150px;
    margin-top: 10px;
  }}
  .cover-meta-card {{
    background: #FFFFFF;
    border: 1.5px solid #E8DCD4;
    border-radius: 12px;
    padding: 14px 16px;
    text-align: left;
    box-shadow: 0 4px 14px rgba(75, 59, 51, 0.05);
  }}
  .cover-meta-card .label {{
    font-size: 8.5pt;
    font-weight: 800;
    color: #C97567;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .cover-meta-card .val {{
    font-size: 11.5pt;
    font-weight: 800;
    color: #4B3B33;
    margin-top: 3px;
    line-height: 1.25;
  }}
  .cover-meta-card .sub {{
    font-size: 8.5pt;
    color: #8A776D;
    margin-top: 3px;
  }}

  /* General Card Styles */
  .card {{
    background: #FFFFFF;
    border-radius: 14px;
    border: 1.5px solid #E8DCD4;
    padding: 18px;
    box-shadow: 0 4px 14px rgba(75, 59, 51, 0.05);
    display: flex;
    flex-direction: column;
  }}
  .card-header {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    padding-bottom: 8px;
    border-bottom: 1.5px solid #F3EAE4;
  }}
  .card-icon {{
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: #F8EFE9;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17pt;
  }}
  .card-title {{
    font-size: 13.5pt;
    font-weight: 800;
    color: #4B3B33;
  }}
  .card-text {{
    font-size: 10.5pt;
    color: #5B4A41;
    line-height: 1.5;
  }}
  .card-list {{
    list-style: none;
    margin-top: 6px;
  }}
  .card-list li {{
    position: relative;
    padding-left: 18px;
    margin-bottom: 7px;
    font-size: 10.5pt;
    color: #5B4A41;
    line-height: 1.45;
  }}
  .card-list li::before {{
    content: "•";
    position: absolute;
    left: 4px;
    color: #C97567;
    font-size: 15pt;
    line-height: 1;
    top: -2px;
  }}
  .card-list li strong {{
    color: #4B3B33;
  }}

  /* Highlighting tags */
  .tag {{
    display: inline-block;
    padding: 3px 9px;
    border-radius: 6px;
    font-size: 9pt;
    font-weight: 700;
  }}
  .tag-terracotta {{ background: #FDEBE7; color: #9E3E30; }}
  .tag-green {{ background: #EBF3EA; color: #32612B; }}
  .tag-mocha {{ background: #F5EFEB; color: #5B4A41; }}
  .tag-blue {{ background: #EAF0F8; color: #2B4C6F; }}

  /* Columns layout */
  .col-half {{
    flex: 1;
  }}

  /* Image showcase wrapper */
  .img-showcase {{
    background: #FFFFFF;
    border: 1.5px solid #E8DCD4;
    border-radius: 14px;
    padding: 10px;
    box-shadow: 0 4px 14px rgba(75, 59, 51, 0.05);
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: center;
    align-items: center;
  }}
  .img-showcase img {{
    max-width: 100%;
    max-height: 100%;
    border-radius: 8px;
    object-fit: contain;
    border: 1px solid #EFE4DC;
  }}
  .img-caption {{
    margin-top: 8px;
    font-size: 9.5pt;
    font-weight: 700;
    color: #8A776D;
    text-align: center;
  }}

  /* Metrics strip */
  .metric-box {{
    background: #FDF9F6;
    border: 1px solid #E8DCD4;
    border-radius: 10px;
    padding: 10px;
    text-align: center;
  }}
  .metric-val {{
    font-size: 20pt;
    font-weight: 900;
    color: #C97567;
    line-height: 1;
  }}
  .metric-lbl {{
    font-size: 9pt;
    font-weight: 700;
    color: #5B4A41;
    margin-top: 4px;
  }}

  /* Interactive Notion button link */
  .notion-link-btn {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #4B3B33;
    color: #FFFFFF;
    text-decoration: none;
    font-size: 10.5pt;
    font-weight: 700;
    padding: 8px 16px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(75, 59, 51, 0.2);
    transition: background 0.2s;
  }}
  .notion-link-btn:hover {{
    background: #C97567;
  }}
</style>
</head>
<body>

<!-- SLIDE 1: PORTADA -->
<div class="slide cover-slide">
  <div class="cover-top">
    <img class="logo-udg" src="{img_udg}" alt="Universidad de Guadalajara">
    <img class="logo-monchis" src="{img_monchis}" alt="Monchis Café">
  </div>
  <div class="cover-badge-event">EXPODIT 2026 • PROYECTO ESPECIALIZANTE • CRN: 196727</div>
  <h1 class="cover-title">MONCHIS <span>CAFÉ</span></h1>
  <div class="cover-subtitle">Sistema Web de Gestión Segura, Punto de Venta Distribuido y Trazabilidad Agroecológica para Cafetería Orgánica y Comercial</div>
  
  <div class="cover-meta-grid">
    <div class="cover-meta-card">
      <div class="label">Responsable / Alumno</div>
      <div class="val">Ernesto Hatuey Fierro M.</div>
      <div class="sub">Código: 223977036 • Especializante (Equipo 2)</div>
    </div>
    <div class="cover-meta-card">
      <div class="label">Profesor Titular / Curso</div>
      <div class="val">Dr. Gabriel Navarro S.</div>
      <div class="sub">CRN: 196727 • Centro Univ. de Tonalá (CUT)</div>
    </div>
    <div class="cover-meta-card">
      <div class="label">Cronograma Ágil</div>
      <div class="val">10 Ago 2026 &rarr; 27 Nov 2026</div>
      <div class="sub">Defensa Oficial Expo DIT: Viernes 27 Nov</div>
    </div>
    <div class="cover-meta-card">
      <div class="label">Compromiso ONU 2030</div>
      <div class="val">ODS 8, ODS 9, ODS 13</div>
      <div class="sub">Acción por el Clima & Consumo Verde (ODS 12)</div>
    </div>
  </div>
</div>

<!-- SLIDE 2: PROBLEMÁTICA & DIAGNÓSTICO OPERATIVO -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Diagnóstico & Contexto Operativo</div>
      <div class="header-title">Problemática en Cafeterías de Especialidad</div>
      <div class="header-subtitle">Brechas financieras, operativas y ecológicas detectadas en el modelo tradicional</div>
    </div>
    <div class="header-logos">
      <img src="{img_udg}" alt="UDG">
      <img src="{img_monchis}" alt="Monchis">
    </div>
  </div>
  
  <div class="slide-body">
    <div class="card" style="flex: 1; border-top: 4px solid #C97567;">
      <div class="card-header">
        <div class="card-icon">📉</div>
        <div class="card-title">Fugas Financieras y Descontrol de Stock</div>
      </div>
      <p class="card-text">
        El registro manual en libretas o POS genéricos provoca hasta un <strong>18% de discrepancias en corte de caja</strong> diario y pérdida de inventario no registrado por falta de mermas tabuladas.
      </p>
      <ul class="card-list" style="margin-top: 10px;">
        <li><strong>Falta de trazabilidad:</strong> Mezcla de granos orgánicos de altura con mezclas comerciales.</li>
        <li><strong>Cálculo analógico de mermas:</strong> Desconocimiento del costo real por taza servida vs grano.</li>
        <li><strong>Vulnerabilidad en cobro:</strong> Ausencia de conciliación automática entre tickets y efectivo.</li>
      </ul>
      <div style="margin-top: auto; padding-top: 10px;">
        <span class="tag tag-terracotta">Impacto: -18% Rentabilidad</span>
      </div>
    </div>

    <div class="card" style="flex: 1; border-top: 4px solid #8A776D;">
      <div class="card-header">
        <div class="card-icon">🏷️</div>
        <div class="card-title">Opacidad de Origen y Comercio Injusto</div>
      </div>
      <p class="card-text">
        Los consumidores actuales exigen certidumbre del grano que beben. La cadena convencional castiga a las pequeñas cooperativas campesinas con intermediación abusiva.
      </p>
      <ul class="card-list" style="margin-top: 10px;">
        <li><strong>Inexistencia de certificación digital:</strong> Imposible validar al comensal el lote (Chiapas/Veracruz).</li>
        <li><strong>Falta de soporte al barista:</strong> El personal carece de recetas técnicas digitales de extracción.</li>
        <li><strong>Desconfianza del cliente:</strong> Riesgo de reputación por sospecha de sustitución de producto.</li>
      </ul>
      <div style="margin-top: auto; padding-top: 10px;">
        <span class="tag tag-mocha">Impacto: Pérdida de valor agregado</span>
      </div>
    </div>

    <div class="card" style="flex: 1; border-top: 4px solid #7C9473;">
      <div class="card-header">
        <div class="card-icon">🥤</div>
        <div class="card-title">Huella Ecológica de Desechables</div>
      </div>
      <p class="card-text">
        En campus universitarios y barras urbanas, una sola barra genera miles de vasos desechables de plástico y polipapel al mes que terminan en vertederos sin reciclaje.
      </p>
      <ul class="card-list" style="margin-top: 10px;">
        <li><strong>Incentivos nulos:</strong> Los sistemas no premian al cliente que aporta termo reusable.</li>
        <li><strong>Falta de métricas verdes:</strong> La gerencia no puede cuantificar su ahorro de CO₂.</li>
        <li><strong>Rezago ecológico:</strong> Incumplimiento de normativas de reducción de plásticos.</li>
      </ul>
      <div style="margin-top: auto; padding-top: 10px;">
        <span class="tag tag-green">Meta: Evitar +4,500 vasos/año</span>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">CRN: 196727</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 2 / 11</div>
  </div>
</div>

<!-- SLIDE 3: ODS ONU -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Alineación Estratégica ONU 2030</div>
      <div class="header-title">Justificación e Impacto en los ODS (Ficha Oficial Expo DIT)</div>
      <div class="header-subtitle">Monchis Café como agente de mitigación climática, crecimiento económico e innovación tecnológica</div>
    </div>
    <div class="header-logos">
      <img src="{img_udg}" alt="UDG">
      <img src="{img_monchis}" alt="Monchis">
    </div>
  </div>
  
  <div class="slide-body">
    <div class="col-half" style="display: flex; flex-direction: column; justify-content: space-between;">
      <div class="card" style="border-left: 5px solid #7C9473; padding: 13px;">
        <div class="card-header" style="margin-bottom: 5px; padding-bottom: 5px;">
          <div class="card-icon" style="width: 30px; height: 30px; font-size: 13pt;">🌍</div>
          <div class="card-title" style="font-size: 11.5pt;">ODS 13: Acción por el Clima & Green IT (Oficial)</div>
        </div>
        <p class="card-text" style="font-size: 9.5pt;">
          Despliegue serverless en <strong>Google Cloud Run que escala a cero</strong> eliminando consumo en reposo, SSG con Vite para optimización energética y <strong>mitigación de +4,500 vasos desechables al año</strong> mediante sellos ecológicos de termo.
        </p>
      </div>

      <div class="card" style="border-left: 5px solid #C97567; padding: 13px;">
        <div class="card-header" style="margin-bottom: 5px; padding-bottom: 5px;">
          <div class="card-icon" style="width: 30px; height: 30px; font-size: 13pt;">☕</div>
          <div class="card-title" style="font-size: 11.5pt;">ODS 8: Trabajo Decente y Crecimiento Económico (Oficial)</div>
        </div>
        <p class="card-text" style="font-size: 9.5pt;">
          Trazabilidad directa por lote que conecta las compras con cooperativas cafetaleras independientes en Chiapas y Veracruz, asegurando un <strong>margen directo +35% superior</strong> frente a los acaparadores intermediarios.
        </p>
      </div>

      <div class="card" style="border-left: 5px solid #2B4C6F; padding: 13px;">
        <div class="card-header" style="margin-bottom: 5px; padding-bottom: 5px;">
          <div class="card-icon" style="width: 30px; height: 30px; font-size: 13pt;">☁️</div>
          <div class="card-title" style="font-size: 11.5pt;">ODS 9: Industria, Innovación e Infraestructura (Oficial)</div>
        </div>
        <p class="card-text" style="font-size: 9.5pt;">
          Arquitectura cloud elástica desacoplada en 5 capas con bus de eventos asíncronos AMQP RabbitMQ (patrón Saga) y base de datos relacional Cloud SQL con integridad transaccional ACID estricta.
        </p>
      </div>

      <div class="card" style="border-left: 5px solid #8A776D; padding: 13px;">
        <div class="card-header" style="margin-bottom: 5px; padding-bottom: 5px;">
          <div class="card-icon" style="width: 30px; height: 30px; font-size: 13pt;">🌱</div>
          <div class="card-title" style="font-size: 11.5pt;">ODS 12: Producción y Consumo Responsables</div>
        </div>
        <p class="card-text" style="font-size: 9.5pt;">
          Motor Monchis Rewards de sellos verdes en el POS, control milimétrico de mermas por gramaje de café molido y auditoría digital inmutable de residuos.
        </p>
      </div>
    </div>

    <div class="col-half">
      <div class="img-showcase">
        <img src="{img_ods}" alt="Diagrama Oficial ODS Monchis Café">
        <div class="img-caption">Figura 1: Matriz Gráfica de Métricas e Indicadores de Impacto Sostenible (ODS 8, 9, 13 y 12)</div>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">CRN: 196727</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 3 / 11</div>
  </div>
</div>

<!-- SLIDE 4: METODOLOGÍA ÁGIL & TABLERO NOTION (CON CAPTURA Y LINK) -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Gestión Ágil & Sprints en Notion</div>
      <div class="header-title">Tablero Ágil del Proyecto Monchis Café</div>
      <div class="header-subtitle">Monitoreo formal de 8 Sprints de ingeniería completados y entrega final de Expo DIT</div>
    </div>
    <div class="header-logos">
      <img src="{img_udg}" alt="UDG">
      <img src="{img_monchis}" alt="Monchis">
    </div>
  </div>
  
  <div class="slide-body">
    <div class="col-half" style="flex: 0.9; display: flex; flex-direction: column; justify-content: space-between;">
      <div class="card" style="border-left: 5px solid #C97567; padding: 16px;">
        <div class="card-header" style="margin-bottom: 6px; padding-bottom: 6px;">
          <div class="card-icon" style="width: 32px; height: 32px; font-size: 14pt;">📋</div>
          <div class="card-title" style="font-size: 12pt;">Ciclo de Desarrollo Ágil (100% Completado)</div>
        </div>
        <p class="card-text" style="font-size: 10pt; line-height: 1.5;">
          <strong>Inicio Formal: 10 de Agosto de 2026</strong> en monorepo Docker, Prisma ORM y arquitectura modular.<br>
          Se ejecutaron <strong>8 Sprints de 2 semanas</strong> cubriendo el ciclo completo de vida del software: seguridad perimetral, bus de eventos RabbitMQ Saga, UI reactiva Vite, POS multipago, fidelización verde, CI/CD y despliegue elástico en GCP.
        </p>
      </div>

      <div class="card" style="border-left: 5px solid #7C9473; padding: 14px;">
        <div class="card-header" style="margin-bottom: 6px; padding-bottom: 6px;">
          <div class="card-icon" style="width: 32px; height: 32px; font-size: 14pt;">🚀</div>
          <div class="card-title" style="font-size: 11.5pt;">Hito Activo: Presentación en Expo DIT</div>
        </div>
        <p class="card-text" style="font-size: 9.5pt; color: #5B4A41; line-height: 1.45;">
          <strong>Actividad Pendiente:</strong> Presentación y Defensa Oficial en Expo DIT 2026 &bull; <strong>Viernes 27 de Noviembre de 2026</strong> (CRN: 196727, CUTonalá).
        </p>
        <div style="margin-top: 10px;">
          <a href="{NOTION_BOARD_URL}" target="_blank" class="notion-link-btn">
            <span>🔗 Abrir Tablero Oficial en Notion ↗</span>
          </a>
        </div>
      </div>

      <div class="card" style="background: #FDF9F6; border: 1px solid #E8DCD4; padding: 10px 14px;">
        <div style="font-size: 9pt; color: #8A776D; line-height: 1.4;">
          <strong>ID Base de Datos:</strong> <code>423f4201a73581ab8e7cc80ff7b771fe</code><br>
          <strong>Workspace:</strong> Ernesto's Notion &bull; Responsable: Ernesto Hatuey Fierro M.
        </div>
      </div>
    </div>

    <div class="col-half" style="flex: 1.1;">
      <div class="img-showcase">
        <img src="{img_notion}" alt="Captura Real del Tablero Ágil en Notion">
        <div class="img-caption">Figura 2: Captura en Tiempo Real del Tablero Ágil de Monchis Café en Notion (8 Sprints Done & Hito Final Activo)</div>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">CRN: 196727</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 4 / 11</div>
  </div>
</div>

<!-- SLIDE 5: OBJETIVOS DEL PROYECTO & MÉTRICAS -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Alcance & Directrices Técnicas</div>
      <div class="header-title">Objetivos del Proyecto & Métricas de Éxito</div>
      <div class="header-subtitle">Metas de desarrollo formal, KPIs cuantitativos y directrices de ingeniería</div>
    </div>
    <div class="header-logos">
      <img src="{img_udg}" alt="UDG">
      <img src="{img_monchis}" alt="Monchis">
    </div>
  </div>
  
  <div class="slide-body">
    <div class="col-half" style="display: flex; flex-direction: column; gap: 14px;">
      <div class="card" style="border-left: 5px solid #C97567; padding: 16px;">
        <div class="card-header" style="margin-bottom: 6px; padding-bottom: 6px;">
          <div class="card-icon" style="width: 32px; height: 32px; font-size: 14pt;">🎯</div>
          <div class="card-title" style="font-size: 12pt;">Objetivo General</div>
        </div>
        <p class="card-text" style="font-size: 10.5pt; font-weight: 500; color: #4B3B33; line-height: 1.5;">
          Diseñar, construir e implementar una <strong>plataforma web integral y distribuida</strong> para la administración comercial de Monchis Café, garantizando transacciones seguras bajo arquitectura orientada a eventos, control riguroso de inventario de granos orgánicos y mezclas comerciales, y un ecosistema de fidelización sustentable alineado a la Agenda ONU 2030 (ODS 8, 9 y 13).
        </p>
      </div>

      <div class="card" style="padding: 14px;">
        <div class="card-header" style="margin-bottom: 6px; padding-bottom: 6px;">
          <div class="card-icon" style="width: 32px; height: 32px; font-size: 14pt;">📊</div>
          <div class="card-title" style="font-size: 11.5pt;">Métricas Cuantitativas Clave</div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 2px;">
          <div class="metric-box">
            <div class="metric-val">&lt; 200 ms</div>
            <div class="metric-lbl">Tiempo de Respuesta API</div>
          </div>
          <div class="metric-box">
            <div class="metric-val">100%</div>
            <div class="metric-lbl">Consistencia en Cortes</div>
          </div>
          <div class="metric-box">
            <div class="metric-val">0</div>
            <div class="metric-lbl">Pérdida de Órdenes (Saga)</div>
          </div>
          <div class="metric-box">
            <div class="metric-val">99.9%</div>
            <div class="metric-lbl">Disponibilidad Cloud Run</div>
          </div>
        </div>
      </div>
    </div>

    <div class="col-half">
      <div class="card" style="height: 100%;">
        <div class="card-header">
          <div class="card-icon">⚙️</div>
          <div class="card-title">Objetivos Específicos de Ingeniería</div>
        </div>
        <ul class="card-list" style="font-size: 10pt;">
          <li>
            <strong>1. Transaccionalidad Concurrente y Resiliente:</strong><br>
            Construir un motor asíncrono con RabbitMQ que soporte horas pico de venta sin bloqueos en el punto de venta.
          </li>
          <li>
            <strong>2. Seguridad Perimetral y Control RBAC:</strong><br>
            Asegurar endpoints mediante tokens JWT (RS256), protección contra ataques de fuerza bruta y filtrado reCAPTCHA Enterprise.
          </li>
          <li>
            <strong>3. Doble Catálogo y Control de Mermas:</strong><br>
            Distinguir inventario orgánico certificado vs comercial y descontar gramos de café e insumos automáticamente por receta.
          </li>
          <li>
            <strong>4. Módulo Verde Monchis Rewards (ODS 13 y 12):</strong><br>
            Premiar al cliente sustentable mediante sellos ecológicos digitales integrados al ticket para mitigar residuos plásticos.
          </li>
          <li>
            <strong>5. Despliegue Elástico CI/CD:</strong><br>
            Automatizar pipeline de pruebas unitarias/E2E y despliegue continuo en Google Cloud Run y Cloud SQL.
          </li>
        </ul>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">CRN: 196727</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 5 / 11</div>
  </div>
</div>

<!-- SLIDE 6: SOLUCIÓN PROPUESTA (GENIALIDADES) -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Innovación Tecnológica & Valor Diferencial</div>
      <div class="header-title">Solución Propuesta: Las Genialidades del Proyecto</div>
      <div class="header-subtitle">¿Por qué Monchis Café redefine el software de hospitalidad y comercio sustentable?</div>
    </div>
    <div class="header-logos">
      <img src="{img_udg}" alt="UDG">
      <img src="{img_monchis}" alt="Monchis">
    </div>
  </div>
  
  <div class="slide-body">
    <div class="card" style="flex: 1; border-top: 4px solid #C97567;">
      <div class="card-header">
        <div class="card-icon">⚡</div>
        <div class="card-title">1. Resiliencia Saga con RabbitMQ</div>
      </div>
      <p class="card-text">
        Si se cae la red o el gateway bancario a mitad de orden, el <strong>Patrón Saga con compensación transaccional</strong> y Dead Letter Queue (DLQ) asegura que jamás se cobre sin descontar stock ni se pierdan órdenes en cola.
      </p>
      <div style="margin-top: auto; padding-top: 10px;">
        <span class="tag tag-terracotta">Cero discrepancias</span>
      </div>
    </div>

    <div class="card" style="flex: 1; border-top: 4px solid #7C9473;">
      <div class="card-header">
        <div class="card-icon">🌱</div>
        <div class="card-title">2. Monchis Green Rewards</div>
      </div>
      <p class="card-text">
        Integración de un <strong>algoritmo de recompensas ecológicas en tiempo real</strong>: cada vez que el barista marca "Trae termo reusable", se calcula el sello ecológico, se descuenta el vaso y se audita el ahorro de CO₂ de la cafetería.
      </p>
      <div style="margin-top: auto; padding-top: 10px;">
        <span class="tag tag-green">Gamificación Verde</span>
      </div>
    </div>

    <div class="card" style="flex: 1; border-top: 4px solid #2B4C6F;">
      <div class="card-header">
        <div class="card-icon">🛡️</div>
        <div class="card-title">3. Seguridad Grado Corporativo</div>
      </div>
      <p class="card-text">
        Autenticación robusta con <strong>reCAPTCHA Enterprise v3</strong> para neutralizar bots, hashing <strong>bcrypt con salt 12</strong>, tokens criptográficos <strong>JWT RS256</strong> y arquitectura RBAC que blinda datos de ventas y auditoría.
      </p>
      <div style="margin-top: auto; padding-top: 10px;">
        <span class="tag tag-blue">Protección Criptográfica</span>
      </div>
    </div>

    <div class="card" style="flex: 1; border-top: 4px solid #4B3B33;">
      <div class="card-header">
        <div class="card-icon">☁️</div>
        <div class="card-title">4. Serverless Cloud Run</div>
      </div>
      <p class="card-text">
        Contenedores Docker desplegados sobre <strong>Google Cloud Platform</strong> con autoescalado de 0 a N instancias según demanda. En periodos sin clientes los costos bajan a cero, optimizando al máximo el presupuesto del negocio.
      </p>
      <div style="margin-top: auto; padding-top: 10px;">
        <span class="tag tag-mocha">Escalabilidad Elástica</span>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">CRN: 196727</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 6 / 11</div>
  </div>
</div>

<!-- SLIDE 7: ARQUITECTURA DEL SOFTWARE (GRAPHIC DIAGRAM) -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Diseño de Ingeniería de Software</div>
      <div class="header-title">Arquitectura y Diagrama del Sistema</div>
      <div class="header-subtitle">Estructura distribuida en 5 capas desacopladas mediante bus asíncrono</div>
    </div>
    <div class="header-logos">
      <img src="{img_udg}" alt="UDG">
      <img src="{img_monchis}" alt="Monchis">
    </div>
  </div>
  
  <div class="slide-body">
    <div class="col-half" style="flex: 1.1;">
      <div class="img-showcase">
        <img src="{img_arch}" alt="Diagrama de Arquitectura Oficial Monchis Café">
        <div class="img-caption">Figura 3: Diagrama de 5 Capas de Software Monchis Café (Frontend, API Gateway, Bus, Persistencia e Infraestructura)</div>
      </div>
    </div>

    <div class="col-half" style="flex: 0.9; display: flex; flex-direction: column; justify-content: space-between;">
      <div class="card" style="border-left: 4px solid #C97567; padding: 12px 16px;">
        <div class="card-title" style="font-size: 11pt; color: #C97567;">Capa 1: Interfaz Reactiva (Vue 3 / Vite)</div>
        <p class="card-text" style="font-size: 9.5pt; margin-top: 3px;">
          Punto de Venta reactivo (POS), Gestión de Catálogo y Dashboard de Administrador con Pinia State y componentes Tailwind optimizados para tablets y pantallas táctiles.
        </p>
      </div>

      <div class="card" style="border-left: 4px solid #2B4C6F; padding: 12px 16px;">
        <div class="card-title" style="font-size: 11pt; color: #2B4C6F;">Capa 2: API Gateway & Core (Next.js 14)</div>
        <p class="card-text" style="font-size: 9.5pt; margin-top: 3px;">
          Rutas API seguras con middleware de validación JWT, control RBAC (Admin, Barista, Auditor), sanitización de payloads y validación de tokens de reCAPTCHA.
        </p>
      </div>

      <div class="card" style="border-left: 4px solid #8A776D; padding: 12px 16px;">
        <div class="card-title" style="font-size: 11pt; color: #8A776D;">Capa 3: Bus Asíncrono (RabbitMQ Saga)</div>
        <p class="card-text" style="font-size: 9.5pt; margin-top: 3px;">
          Colas independientes para eventos <code>order.created</code>, <code>inventory.deduct</code> y <code>points.accrue</code> con Dead Letter Queue para tolerancia a fallas.
        </p>
      </div>

      <div class="card" style="border-left: 4px solid #7C9473; padding: 12px 16px;">
        <div class="card-title" style="font-size: 11pt; color: #7C9473;">Capa 4 & 5: Persistencia & Cloud Run</div>
        <p class="card-text" style="font-size: 9.5pt; margin-top: 3px;">
          PostgreSQL Cloud SQL con Prisma ORM (migraciones estrictas), Redis para caché de sesión y contenedores Docker administrados en Google Cloud Platform.
        </p>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">CRN: 196727</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 7 / 11</div>
  </div>
</div>

<!-- SLIDE 8: STACK TECNOLÓGICO & DEVSECOPS -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Ecosistema & Herramientas de Desarrollo</div>
      <div class="header-title">Stack Tecnológico & Flujo DevSecOps</div>
      <div class="header-subtitle">Herramientas modernas para alta concurrencia, seguridad bancaria y entrega continua</div>
    </div>
    <div class="header-logos">
      <img src="{img_udg}" alt="UDG">
      <img src="{img_monchis}" alt="Monchis">
    </div>
  </div>
  
  <div class="slide-body">
    <div class="card" style="flex: 1;">
      <div class="card-header">
        <div class="card-icon">🎨</div>
        <div class="card-title">Frontend & UI</div>
      </div>
      <ul class="card-list">
        <li><strong>Vue 3 & Vite:</strong> Renderizado ultra-rápido de vistas y hot reloading para POS en caliente.</li>
        <li><strong>TypeScript:</strong> Tipado estático estricto en órdenes, catálogo y clientes.</li>
        <li><strong>Tailwind CSS:</strong> Sistema de diseño pastel cálido emblemático de Monchis Café.</li>
        <li><strong>Pinia State:</strong> Estado global reactivo para el carrito de compras y sellos ecológicos.</li>
      </ul>
      <div style="margin-top: auto; padding-top: 8px;">
        <span class="tag tag-terracotta">UX/UI Diseñado para Baristas</span>
      </div>
    </div>

    <div class="card" style="flex: 1;">
      <div class="card-header">
        <div class="card-icon">⚙️</div>
        <div class="card-title">Backend & Datos</div>
      </div>
      <ul class="card-list">
        <li><strong>Next.js 14 & Node.js:</strong> API REST modular, serverless functions y middleware seguro.</li>
        <li><strong>PostgreSQL 16:</strong> Base de datos ACID para integridad contable absoluta.</li>
        <li><strong>Prisma ORM:</strong> Tipado estricto de consultas SQL y migraciones reproducibles.</li>
        <li><strong>RabbitMQ:</strong> Broker de mensajería asíncrona AMQP para orquestación Saga.</li>
      </ul>
      <div style="margin-top: auto; padding-top: 8px;">
        <span class="tag tag-blue">Microservicios & Consistencia</span>
      </div>
    </div>

    <div class="card" style="flex: 1;">
      <div class="card-header">
        <div class="card-icon">🛡️</div>
        <div class="card-title">Seguridad & Auth</div>
      </div>
      <ul class="card-list">
        <li><strong>JWT (RS256):</strong> Tokens firmados asimétricamente para autorización sin estado.</li>
        <li><strong>bcrypt (Salt 12):</strong> Hashing unidireccional de contraseñas de baristas y admins.</li>
        <li><strong>reCAPTCHA Enterprise v3:</strong> Detección pasiva de bots en login y recuperación.</li>
        <li><strong>CORS & Helmet:</strong> Cabeceras HTTP endurecidas contra XSS y CSRF (OWASP).</li>
      </ul>
      <div style="margin-top: auto; padding-top: 8px;">
        <span class="tag tag-mocha">Cumplimiento OWASP Top 10</span>
      </div>
    </div>

    <div class="card" style="flex: 1;">
      <div class="card-header">
        <div class="card-icon">🚀</div>
        <div class="card-title">DevSecOps & Cloud</div>
      </div>
      <ul class="card-list">
        <li><strong>Google Cloud Run:</strong> Ejecución de contenedores escalable a cero con SSL automático.</li>
        <li><strong>Docker Multi-stage:</strong> Imágenes de producción ultraligeras e inmutables.</li>
        <li><strong>GitHub Actions:</strong> Pipeline CI/CD con linting, pruebas unitarias y despliegue a GCP.</li>
        <li><strong>Cloud Monitoring:</strong> Monitoreo de latencia, tasa de errores HTTP 5xx y memoria.</li>
      </ul>
      <div style="margin-top: auto; padding-top: 8px;">
        <span class="tag tag-green">Infraestructura Elástica</span>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">CRN: 196727</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 8 / 11</div>
  </div>
</div>

<!-- SLIDE 9: MÓDULOS CORE & EVIDENCIA DE PRUEBAS (LOGIN & POS) -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Aseguramiento de Calidad & Operación</div>
      <div class="header-title">Módulos Core: Seguridad RBAC & Punto de Venta</div>
      <div class="header-subtitle">Validación formal de casos de prueba de acceso y operación táctil en barra con sellos ecológicos</div>
    </div>
    <div class="header-logos">
      <img src="{img_udg}" alt="UDG">
      <img src="{img_monchis}" alt="Monchis">
    </div>
  </div>
  
  <div class="slide-body">
    <!-- Login & Smoke Testing -->
    <div class="col-half" style="display: flex; flex-direction: column; gap: 10px;">
      <div class="img-showcase" style="height: 220px;">
        <img src="{img_login}" alt="Captura Real de Login Monchis Café">
        <div class="img-caption">Figura 4: Login Seguro con reCAPTCHA Enterprise y Rate Limiting</div>
      </div>
      <div class="card" style="padding: 12px;">
        <div class="card-title" style="font-size: 11pt;">Matriz de Smoke Tests (100% Exitosos)</div>
        <table style="width: 100%; border-collapse: collapse; margin-top: 6px; font-size: 8.5pt;">
          <thead>
            <tr style="background: #F3EAE4; color: #4B3B33; text-align: left;">
              <th style="padding: 4px 6px; border: 1px solid #E8DCD4;">ID</th>
              <th style="padding: 4px 6px; border: 1px solid #E8DCD4;">Escenario</th>
              <th style="padding: 4px 6px; border: 1px solid #E8DCD4;">Salida Esperada</th>
              <th style="padding: 4px 6px; border: 1px solid #E8DCD4;">Estatus</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="padding: 4px 6px; border: 1px solid #E8DCD4; font-weight: 700;">CP-01</td>
              <td style="padding: 4px 6px; border: 1px solid #E8DCD4;">Admin con credenciales válidas</td>
              <td style="padding: 4px 6px; border: 1px solid #E8DCD4;">Redirección a /admin/dashboard</td>
              <td style="padding: 4px 6px; border: 1px solid #E8DCD4;"><span class="tag tag-green">OK</span></td>
            </tr>
            <tr>
              <td style="padding: 4px 6px; border: 1px solid #E8DCD4; font-weight: 700;">CP-02</td>
              <td style="padding: 4px 6px; border: 1px solid #E8DCD4;">Barista con credenciales válidas</td>
              <td style="padding: 4px 6px; border: 1px solid #E8DCD4;">Redirección a vista POS /pos</td>
              <td style="padding: 4px 6px; border: 1px solid #E8DCD4;"><span class="tag tag-green">OK</span></td>
            </tr>
            <tr>
              <td style="padding: 4px 6px; border: 1px solid #E8DCD4; font-weight: 700;">CP-03</td>
              <td style="padding: 4px 6px; border: 1px solid #E8DCD4;">Password erróneo (3 intentos)</td>
              <td style="padding: 4px 6px; border: 1px solid #E8DCD4;">Bloqueo temporal 60s (Rate Limit)</td>
              <td style="padding: 4px 6px; border: 1px solid #E8DCD4;"><span class="tag tag-green">OK</span></td>
            </tr>
            <tr>
              <td style="padding: 4px 6px; border: 1px solid #E8DCD4; font-weight: 700;">CP-04</td>
              <td style="padding: 4px 6px; border: 1px solid #E8DCD4;">Token reCAPTCHA inválido</td>
              <td style="padding: 4px 6px; border: 1px solid #E8DCD4;">Rechazo con código HTTP 403</td>
              <td style="padding: 4px 6px; border: 1px solid #E8DCD4;"><span class="tag tag-green">OK</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- POS & Green Rewards -->
    <div class="col-half" style="display: flex; flex-direction: column; gap: 10px;">
      <div class="img-showcase" style="height: 220px;">
        <img src="{img_pos}" alt="Captura Real del POS Monchis Café">
        <div class="img-caption">Figura 5: Punto de Venta con Carrito Reactivo y Botón de Termo Reusable</div>
      </div>
      <div class="card" style="padding: 12px; border-left: 4px solid #7C9473;">
        <div class="card-title" style="font-size: 11pt; color: #7C9473;">Innovación del Botón Ecológico Monchis Rewards</div>
        <p class="card-text" style="font-size: 9.5pt; margin-top: 4px;">
          Al marcar <strong>"Trae termo reusable (+1 sello ecológico)"</strong> se dispara una operación atómica: acredita sello en billetera digital, descuenta cero vasos de inventario y suma +1 impacto mitigado al contador ODS 13 de la cafetería.
        </p>
        <div style="margin-top: 6px; font-size: 9pt; color: #5B4A41;">
          <strong>Cobro Multi-Método:</strong> Efectivo, Tarjeta, Transferencia y Mixto con cálculo de cambio en tiempo real.
        </div>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">CRN: 196727</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 9 / 11</div>
  </div>
</div>

<!-- SLIDE 10: PANEL ADMINISTRATIVO & TRAZABILIDAD -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Gestión Gerencial & Auditoría</div>
      <div class="header-title">Panel Administrativo & Trazabilidad Agroecológica</div>
      <div class="header-subtitle">Control integral de inventarios, reportes de corte y procedencia de cooperativas campesinas</div>
    </div>
    <div class="header-logos">
      <img src="{img_udg}" alt="UDG">
      <img src="{img_monchis}" alt="Monchis">
    </div>
  </div>
  
  <div class="slide-body">
    <div class="col-half" style="flex: 1.1;">
      <div class="img-showcase">
        <img src="{img_admin}" alt="Captura Real del Panel Administrativo">
        <div class="img-caption">Figura 6: Tablero Administrativo con Métricas UTM, Control de Stock y Registro de Ventas</div>
      </div>
    </div>

    <div class="col-half" style="flex: 0.9; display: flex; flex-direction: column; justify-content: space-between;">
      <div class="card" style="border-left: 4px solid #C97567; padding: 13px 16px;">
        <div class="card-header" style="margin-bottom: 4px; padding-bottom: 4px;">
          <div class="card-icon" style="width: 28px; height: 28px; font-size: 13pt;">📦</div>
          <div class="card-title" style="font-size: 11pt;">Control de Stock por Gramaje y Receta</div>
        </div>
        <p class="card-text" style="font-size: 9.5pt;">
          Cada bebida servida descuenta automáticamente los gramos exactos de grano (18g espresso orgánico Chiapas) y mililitros de leche, alertando al administrador antes del agotamiento de lote.
        </p>
      </div>

      <div class="card" style="border-left: 4px solid #8A776D; padding: 13px 16px;">
        <div class="card-header" style="margin-bottom: 4px; padding-bottom: 4px;">
          <div class="card-icon" style="width: 28px; height: 28px; font-size: 13pt;">🤝</div>
          <div class="card-title" style="font-size: 11pt;">Trazabilidad Directa de Cooperativa</div>
        </div>
        <p class="card-text" style="font-size: 9.5pt;">
          Ficha documental de procedencia: cooperativa asociada, altitud de cultivo (1,400 msnm), fecha de cosecha y nota de cata. El sistema genera etiquetas QR que demuestran autenticidad al cliente.
        </p>
      </div>

      <div class="card" style="border-left: 4px solid #7C9473; padding: 13px 16px;">
        <div class="card-header" style="margin-bottom: 4px; padding-bottom: 4px;">
          <div class="card-icon" style="width: 28px; height: 28px; font-size: 13pt;">📊</div>
          <div class="card-title" style="font-size: 11pt;">Métricas de Campaña y Cortes Diarios</div>
        </div>
        <p class="card-text" style="font-size: 9.5pt;">
          Auditoría de ventas por turno, tasa de conversión y balance contable consolidado inmutable, con exportación a PDF y hojas de cálculo para el auditor institucional.
        </p>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">CRN: 196727</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 10 / 11</div>
  </div>
</div>

<!-- SLIDE 11: CONCLUSIONES & DEMO EN VIVO -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Cierre Académico & Resultados</div>
      <div class="header-title">Conclusiones del Proyecto Integrador</div>
      <div class="header-subtitle">Validación integral de competencias de ingeniería y compromiso social en ExpoDIT 2026</div>
    </div>
    <div class="header-logos">
      <img src="{img_udg}" alt="UDG">
      <img src="{img_monchis}" alt="Monchis">
    </div>
  </div>
  
  <div class="slide-body">
    <div class="col-half" style="flex: 1.1;">
      <div class="img-showcase">
        <img src="{img_web}" alt="Despliegue Web Activo Monchis Café">
        <div class="img-caption">Figura 7: Despliegue en Vivo del Sistema Web Monchis Café en Google Cloud Platform</div>
      </div>
    </div>

    <div class="col-half" style="flex: 0.9; display: flex; flex-direction: column; justify-content: space-between;">
      <div class="card" style="border-left: 4px solid #7C9473;">
        <div class="card-title" style="font-size: 11.5pt; color: #7C9473;">1. Solución Tecnológica Integral</div>
        <p class="card-text" style="font-size: 9.5pt; margin-top: 4px;">
          Se cumplió con el <strong>100% de los requisitos del Proyecto Integrador</strong>: arquitectura elástica desacoplada, control RBAC seguro, persistencia relacional estricta y respuesta inferior a 200 ms.
        </p>
      </div>

      <div class="card" style="border-left: 4px solid #C97567;">
        <div class="card-title" style="font-size: 11.5pt; color: #C97567;">2. Impacto Socio-Ambiental Tangible</div>
        <p class="card-text" style="font-size: 9.5pt; margin-top: 4px;">
          El software trasciende la función contable: apoya a cooperativas campesinas locales (ODS 8), acelera infraestructura digital moderna (ODS 9) y combate activamente el cambio climático y desechables plásticos (ODS 13 & 12).
        </p>
      </div>

      <div class="card" style="border-left: 4px solid #4B3B33; background: #FDF9F6;">
        <div class="card-title" style="font-size: 11.5pt; color: #4B3B33;">3. Madurez de Ingeniería en ExpoDIT</div>
        <p class="card-text" style="font-size: 9.5pt; margin-top: 4px;">
          La aplicación de patrones formales (Saga, RBAC, CI/CD, Containerización) demuestra el rigor técnico adquirido durante la trayectoria en el <strong>Centro Universitario de Tonalá</strong>.
        </p>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">CRN: 196727</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 11 / 11</div>
  </div>
</div>

</body>
</html>
"""

html_path = os.path.join(EXPODIT_DIR, "Presentacion_ExpoDIT_Monchis_Cafe.html")
pdf_path = os.path.join(EXPODIT_DIR, "Presentacion_ExpoDIT_Monchis_Cafe.pdf")
pptx_path = os.path.join(EXPODIT_DIR, "Presentacion_ExpoDIT_Monchis_Cafe.pptx")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"HTML presentation written: {html_path}")

# =========================================================================
# COMPILE PDF USING EDGE / CHROME HEADLESS
# =========================================================================
if BROWSER_PATH:
    print(f"Compiling PDF with Headless Browser ({BROWSER_PATH})...")
    cmd = [
        BROWSER_PATH,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    subprocess.run(cmd, check=True)
    print(f"PDF successfully generated: {pdf_path}")

    # Copy PDF to Downloads
    if os.path.exists(DOWNLOADS_DIR):
        dest_pdf_downloads = os.path.join(DOWNLOADS_DIR, "Presentacion_ExpoDIT_Monchis_Cafe.pdf")
        shutil.copy2(pdf_path, dest_pdf_downloads)
        print(f"PDF copied to Downloads: {dest_pdf_downloads}")
else:
    print("Warning: No compatible browser found for headless PDF generation.")

# =========================================================================
# GENERATE EDITABLE PPTX (python-pptx) - EXACTLY 11 SLIDES
# =========================================================================
print("Generating PowerPoint PPTX presentation (11 slides)...")
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Exact Monchis Café pastel corporate colors
C_BG = RGBColor(0xFB, 0xF1, 0xEC)            # #FBF1EC Fondo crema cálido
C_TERRACOTTA = RGBColor(0xC9, 0x75, 0x67)     # #C97567 Terracota primario
C_SOFT_CORAL = RGBColor(0xE0, 0x8D, 0x80)     # #E08D80 Coral suave
C_DARK_COFFEE = RGBColor(0x4B, 0x3B, 0x33)    # #4B3B33 Café oscuro títulos
C_WARM_MOCHA = RGBColor(0x5B, 0x4A, 0x41)     # #5B4A41 Café texto
C_MUTED_COFFEE = RGBColor(0x8A, 0x77, 0x6D)   # #8A776D Café secundario
C_SAGE_GREEN = RGBColor(0x7C, 0x94, 0x73)     # #7C9473 Verde ODS 12/13
C_NAVY_TECH = RGBColor(0x2B, 0x4C, 0x6F)      # #2B4C6F Azul arquitectura

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = C_BG

def add_header(slide, badge, title, subtitle):
    set_slide_background(slide)
    
    # Top decorative bar
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_TERRACOTTA
    top_bar.line.fill.background()

    # Header container
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(9.5), Inches(1.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = badge.upper()
    p0.font.size = Pt(9.5)
    p0.font.bold = True
    p0.font.color.rgb = C_TERRACOTTA
    
    p1 = tf.add_paragraph()
    p1.text = title
    p1.font.size = Pt(21)
    p1.font.bold = True
    p1.font.color.rgb = C_DARK_COFFEE
    
    p2 = tf.add_paragraph()
    p2.text = subtitle
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = C_MUTED_COFFEE
    
    # Logos
    if os.path.exists(raw_paths["udg"]):
        slide.shapes.add_picture(raw_paths["udg"], Inches(10.8), Inches(0.35), height=Inches(0.85))
    if os.path.exists(raw_paths["monchis"]):
        slide.shapes.add_picture(raw_paths["monchis"], Inches(11.9), Inches(0.35), height=Inches(0.85))

def add_footer(slide, current_slide, total_slides=11):
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.35))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"Ernesto Hatuey Fierro M. (223977036) • CRN: 196727 | Equipo 2 • CUTonalá (DIT) | Dr. Gabriel Navarro Salcedo | Slide {current_slide} / {total_slides}"
    p.font.size = Pt(9)
    p.font.color.rgb = C_MUTED_COFFEE

# ==========================================
# SLIDE 1: PORTADA
# ==========================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

top_bar1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
top_bar1.fill.solid()
top_bar1.fill.fore_color.rgb = C_TERRACOTTA
top_bar1.line.fill.background()

if os.path.exists(raw_paths["udg"]):
    s1.shapes.add_picture(raw_paths["udg"], Inches(5.1), Inches(0.7), height=Inches(1.15))
if os.path.exists(raw_paths["monchis"]):
    s1.shapes.add_picture(raw_paths["monchis"], Inches(6.8), Inches(0.7), height=Inches(1.15))

tb_c = s1.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(11.333), Inches(4.6))
tf_c = tb_c.text_frame
tf_c.word_wrap = True

p = tf_c.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
p.text = "EXPODIT 2026 • PROYECTO ESPECIALIZANTE • CRN: 196727"
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = C_TERRACOTTA

p = tf_c.add_paragraph()
p.alignment = PP_ALIGN.CENTER
p.text = "MONCHIS CAFÉ"
p.font.size = Pt(38)
p.font.bold = True
p.font.color.rgb = C_DARK_COFFEE

p = tf_c.add_paragraph()
p.alignment = PP_ALIGN.CENTER
p.text = "Sistema Web de Gestión Segura, Punto de Venta Distribuido y Trazabilidad Agroecológica"
p.font.size = Pt(15.5)
p.font.bold = True
p.font.color.rgb = C_WARM_MOCHA

p = tf_c.add_paragraph()
p.alignment = PP_ALIGN.CENTER
p.text = "Responsable: Ernesto Hatuey Fierro Meléndez (223977036) • Modalidad Especializante (Equipo 2)"
p.font.size = Pt(12.5)
p.font.bold = True
p.font.color.rgb = C_DARK_COFFEE

p = tf_c.add_paragraph()
p.alignment = PP_ALIGN.CENTER
p.text = "Inicio: 10 de Agosto 2026 • Presentación Oficial Expo DIT: Viernes 27 de Noviembre 2026"
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = C_TERRACOTTA

p = tf_c.add_paragraph()
p.alignment = PP_ALIGN.CENTER
p.text = "Profesor Titular: Dr. Gabriel Navarro Salcedo | Centro Universitario de Tonalá (CUTonalá - DIT)"
p.font.size = Pt(11)
p.font.color.rgb = C_MUTED_COFFEE

p = tf_c.add_paragraph()
p.alignment = PP_ALIGN.CENTER
p.text = "Alineación ODS Oficial: ODS 8, ODS 9, ODS 13 (Acción por el Clima) & ODS 12"
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = C_SAGE_GREEN

# ==========================================
# SLIDE 2: PROBLEMÁTICA
# ==========================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "Diagnóstico & Contexto", "Problemática en Cafeterías de Especialidad", "Fugas financieras, falta de trazabilidad de origen y generación masiva de desechables")
tb = s2.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "1. FUGAS FINANCIERAS Y DESCONTROL DE INVENTARIO:\n• Hasta 18% de discrepancia en cierres de caja por registro manual en libretas o POS genéricos.\n• Falta de costeo automático por gramaje en bebidas preparadas y mermas no tabuladas.\n• Ausencia de validación cruzada entre tickets emitidos y efectivo en bóveda.\n\n2. OPACIDAD EN TRAZABILIDAD Y COMERCIO INJUSTO:\n• Imposibilidad de certificar digitalmente al comensal el origen campesino del grano (Chiapas/Veracruz).\n• Intermediación comercial excesiva que castiga el margen de las cooperativas agrícolas locales.\n• El personal en barra carece de guías técnicas digitales para recetas de extracción.\n\n3. HUELLA ECOLÓGICA DE PLÁSTICOS DE UN SOLO USO:\n• Generación de miles de vasos plásticos y polipapel al mes sin alternativa de reciclaje en campus.\n• Los sistemas convencionales no premian de forma automatizada al cliente que aporta termo reusable.\n• Meta de impacto del proyecto: Mitigar y evitar más de 4,500 vasos desechables al año."
add_footer(s2, 2)

# ==========================================
# SLIDE 3: ODS ONU
# ==========================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "Alineación ONU 2030", "Justificación e Impacto en los ODS (Ficha Oficial Expo DIT)", "Alineación oficial con ODS 8, 9 y 13 (Acción por el Clima), complementado con ODS 12")
tb = s3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.5), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "• ODS 13 (Acción por el Clima & Green IT - Oficial):\nDespliegue serverless en Google Cloud Run que escala a cero (reducción de huella de carbono), optimización SSG con Vite para eficiencia energética y mitigación de +4,500 vasos desechables al año.\n\n• ODS 8 (Trabajo Decente y Crecimiento Económico - Oficial):\nCompras directas a cooperativas cafetaleras independientes de Chiapas y Veracruz con +35% de margen directo sin intermediarios.\n\n• ODS 9 (Industria, Innovación e Infraestructura - Oficial):\nArquitectura cloud elástica en 5 capas con bus de eventos RabbitMQ (patrón Saga) y tolerancia absoluta a fallas de red.\n\n• ODS 12 (Consumo Responsable):\nSellos ecológicos Monchis Rewards que premian el uso de termo reusable y control de mermas por gramaje."
if os.path.exists(raw_paths["ods"]):
    s3.shapes.add_picture(raw_paths["ods"], Inches(6.6), Inches(1.8), width=Inches(5.9))
add_footer(s3, 3)

# ==========================================
# SLIDE 4: METODOLOGÍA ÁGIL & TABLERO EN NOTION
# ==========================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "Gestión Ágil & Sprints en Notion", "Tablero Ágil del Proyecto Monchis Café", "Monitoreo formal de 8 Sprints de ingeniería completados y entrega final de Expo DIT")

tb = s4.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.0), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "METODOLOGÍA DE 8 SPRINTS (100% COMPLETADOS):\n• Inicio formal: 10 de Agosto de 2026 en monorepo Docker y Prisma.\n• Sprints 1 al 8 ejecutados exitosamente:\n  1. Setup Arquitectura Monorepo y Docker Compose\n  2. Seguridad Core, Auth JWT RS256 y reCAPTCHA\n  3. Broker RabbitMQ, Patrón Saga y Reversas\n  4. Frontend SPA Vue 3 + Vite, Diseño Pastel y SSG\n  5. Punto de Venta (POS) Táctil para Baristas\n  6. Trazabilidad Café Orgánico y Monchis Rewards\n  7. Pipelines DevSecOps CI/CD en GitHub Actions\n  8. Despliegue en GCP Cloud Run y Paquete ExpoDIT\n\nHITO FINAL ACTIVO:\n🚀 Presentación y Defensa en Expo DIT 2026\n🗓️ Viernes 27 de Noviembre de 2026 (CRN: 196727)\n\nENLACE AL TABLERO EN NOTION:\nhttps://app.notion.com/p/423f4201a73581ab8e7cc80ff7b771fe"

if os.path.exists(raw_paths["notion"]):
    s4.shapes.add_picture(raw_paths["notion"], Inches(6.1), Inches(1.8), width=Inches(6.4))
add_footer(s4, 4)

# ==========================================
# SLIDE 5: OBJETIVOS & MÉTRICAS
# ==========================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "Alcance & Directrices Técnicas", "Objetivos del Proyecto & Métricas de Éxito", "Metas de desarrollo formal, KPIs cuantitativos y directrices de ingeniería")
tb = s5.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "OBJETIVO GENERAL:\nDiseñar, construir e implementar una plataforma web integral y distribuida para la administración comercial de Monchis Café, garantizando transacciones seguras bajo arquitectura orientada a eventos, control riguroso de inventario de granos orgánicos y mezclas comerciales, y un ecosistema de fidelización sustentable alineado a la Agenda ONU 2030 (ODS 8, 9 y 13).\n\nMÉTRICAS CLAVE DE INGENIERÍA:\n• Latencia API: < 200 ms en endpoints transaccionales.\n• Consistencia de Caja: 100% de conciliación en turnos.\n• Tolerancia a Fallos: 0 órdenes perdidas gracias al Patrón Saga en RabbitMQ.\n• Disponibilidad Cloud Run: 99.9% uptime con autoescalado elástico a cero.\n\nOBJETIVOS ESPECÍFICOS:\n1. Transaccionalidad Concurrente: Patrón Saga con RabbitMQ para evitar pérdidas de órdenes.\n2. Seguridad RBAC: Roles blindados (Admin vs Barista) con JWT RS256 y reCAPTCHA Enterprise.\n3. Doble Catálogo: Control de mermas por gramaje para café orgánico y convencional.\n4. Módulo Verde: Sistema gamificado Monchis Rewards integrado al ticket (ODS 13 y 12).\n5. Despliegue Elástico: Contenedores Docker autoescalables en Google Cloud Run y Cloud SQL."
add_footer(s5, 5)

# ==========================================
# SLIDE 6: SOLUCIÓN PROPUESTA (GENIALIDADES)
# ==========================================
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "Innovación Tecnológica & Valor Diferencial", "Solución Propuesta: Las Genialidades del Proyecto", "¿Por qué Monchis Café redefine el software de hospitalidad y comercio sustentable?")
tb = s6.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "1. RESILIENCIA SAGA CON RABBITMQ:\nCompensación automática de transacciones y Dead Letter Queue (DLQ). Si se cae la red o el banco, jamás se cobra sin descontar stock ni se pierden pedidos.\n\n2. MONCHIS GREEN REWARDS:\nAlgoritmo de gamificación verde en barra que acredita sellos ecológicos inmediatos al usar termo reusable, descontando el vaso y auditando el CO₂ mitigado.\n\n3. SEGURIDAD GRADO CORPORATIVO:\nTokens asimétricos RS256, hashing de contraseñas bcrypt con salt 12 y protección Google reCAPTCHA Enterprise v3 en tiempo real.\n\n4. ARQUITECTURA SERVERLESS CLOUD RUN:\nContenedores escalables de 0 a N con facturación bajo demanda. En periodos sin clientes los costos de infraestructura bajan a cero."
add_footer(s6, 6)

# ==========================================
# SLIDE 7: ARQUITECTURA DEL SISTEMA
# ==========================================
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "Diseño de Ingeniería de Software", "Arquitectura y Diagrama del Sistema", "Estructura distribuida en 5 capas desacopladas mediante bus asíncrono")
if os.path.exists(raw_paths["arch"]):
    s7.shapes.add_picture(raw_paths["arch"], Inches(0.8), Inches(1.8), width=Inches(7.2))
tb = s7.shapes.add_textbox(Inches(8.3), Inches(1.8), Inches(4.2), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "5 CAPAS DESACOPLADAS:\n\n• Capa 1: UI Reactiva\nVue 3 / Vite / Pinia / Tailwind pastel para POS y Dashboard.\n\n• Capa 2: API Gateway & Core\nNext.js 14 / Rutas protegidas RBAC / reCAPTCHA.\n\n• Capa 3: Bus Asíncrono\nRabbitMQ Saga Pattern con colas de compensación.\n\n• Capa 4: Persistencia Relacional\nPostgreSQL 16 Cloud SQL con Prisma ORM.\n\n• Capa 5: Infraestructura Cloud\nGoogle Cloud Run serverless y Cloud Logging."
add_footer(s7, 7)

# ==========================================
# SLIDE 8: STACK TECNOLÓGICO & DEVSECOPS
# ==========================================
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "Ecosistema Tecnológico & Entrega Continua", "Stack Tecnológico & Flujo DevSecOps", "Herramientas modernas para alta concurrencia, seguridad bancaria y entrega continua")
tb = s8.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "• FRONTEND & UI:\nVue 3, Vite, TypeScript, Tailwind CSS pastel, Pinia State Management, Lucide Icons.\n\n• BACKEND & MICROSERVICIOS:\nNext.js 14 API Routes, Node.js runtime, RabbitMQ AMQP, Prisma ORM.\n\n• BASES DE DATOS & CACHÉ:\nPostgreSQL 16 (Cloud SQL) con integridad ACID estricta y Redis Cache de sesiones.\n\n• SEGURIDAD & PERÍMETRO:\nJSON Web Tokens (RS256), bcrypt salt 12, Google reCAPTCHA Enterprise, cabeceras Helmet/CORS.\n\n• DEVSECOPS & CLOUD:\nDocker Multi-stage, Google Cloud Run, Cloud SQL, GitHub Actions CI/CD y Cloud Monitoring."
add_footer(s8, 8)

# ==========================================
# SLIDE 9: MÓDULOS CORE (SEGURIDAD & POS)
# ==========================================
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "Aseguramiento de Calidad & Operación", "Módulos Core: Seguridad RBAC & Punto de Venta", "Validación formal de casos de prueba de acceso y operación táctil en barra con sellos ecológicos")
if os.path.exists(raw_paths["login"]):
    s9.shapes.add_picture(raw_paths["login"], Inches(0.8), Inches(1.8), width=Inches(5.7))
if os.path.exists(raw_paths["pos"]):
    s9.shapes.add_picture(raw_paths["pos"], Inches(6.8), Inches(1.8), width=Inches(5.7))

tb = s9.shapes.add_textbox(Inches(0.8), Inches(5.3), Inches(11.733), Inches(1.5))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "SMOKE TESTS DE LOGIN (100% OK): CP-01 Admin a Dashboard • CP-02 Barista a POS • CP-03 Rate Limit por password erróneo • CP-04 Rechazo reCAPTCHA inválido.\nPUNTO DE VENTA (POS) TÁCTIL: Carrito reactivo, cobro multi-método y botón ecológico 'Trae termo reusable' (+1 sello verde Monchis Rewards)."
add_footer(s9, 9)

# ==========================================
# SLIDE 10: PANEL ADMINISTRATIVO & TRAZABILIDAD
# ==========================================
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "Gestión Gerencial & Auditoría", "Panel Administrativo & Trazabilidad Agroecológica", "Control integral de inventarios, reportes de corte y procedencia de cooperativas campesinas")
if os.path.exists(raw_paths["admin"]):
    s10.shapes.add_picture(raw_paths["admin"], Inches(0.8), Inches(1.8), width=Inches(6.4))
tb = s10.shapes.add_textbox(Inches(7.5), Inches(1.8), Inches(5.0), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "CAPACIDADES GERENCIALES & AUDITORÍA:\n\n• Control de Stock por Gramaje y Receta:\nCada bebida vendida descuenta automáticamente los gramos exactos de grano (18g espresso orgánico) y mililitros de leche, alertando antes del agotamiento.\n\n• Trazabilidad de Cooperativas Campesinas:\nRegistro de lotes de Chiapas y Veracruz con altitud (1,400 msnm), nota de cata y códigos QR verificables.\n\n• Métricas de Impacto Verde:\nContador auditado de vasos desechables evitados y huella de carbono mitigada.\n\n• Auditoría Contable Inmutable:\nVentas por turno y exportación de reportes a PDF y hojas de cálculo para el auditor."
add_footer(s10, 10)

# ==========================================
# SLIDE 11: CONCLUSIONES & DEMO EN VIVO
# ==========================================
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, "Cierre Académico & Resultados", "Conclusiones del Proyecto Integrador", "Validación integral de competencias de ingeniería y compromiso social en ExpoDIT 2026")
if os.path.exists(raw_paths["web"]):
    s11.shapes.add_picture(raw_paths["web"], Inches(0.8), Inches(1.8), width=Inches(6.4))
tb = s11.shapes.add_textbox(Inches(7.5), Inches(1.8), Inches(5.0), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "CONCLUSIONES FORMALES:\n\n1. Solución Tecnológica Integral:\n100% de los requerimientos implementados con arquitectura elástica en 5 capas y respuesta < 200 ms.\n\n2. Impacto Socio-Ambiental Tangible:\nApoyo directo a cooperativas campesinas (ODS 8), infraestructura digital moderna (ODS 9) y combate activo a plásticos desechables (ODS 13 y 12).\n\n3. Rigor de Ingeniería en ExpoDIT:\nAplicación demostrada de patrones formales (Saga, RBAC, CI/CD y Serverless Cloud Run en CUTonalá).\n\n• Despliegue en producción activo y verificado en Google Cloud Platform."
add_footer(s11, 11)

prs.save(pptx_path)
print(f"PPTX successfully generated (11 slides): {pptx_path}")

if os.path.exists(DOWNLOADS_DIR):
    dest_pptx_downloads = os.path.join(DOWNLOADS_DIR, "Presentacion_ExpoDIT_Monchis_Cafe.pptx")
    shutil.copy2(pptx_path, dest_pptx_downloads)
    print(f"PPTX copied to Downloads: {dest_pptx_downloads}")

print("\nALL PRESENTATION DELIVERABLES (11 SLIDES) SUCCESSFULLY CREATED AND COPIED!")
