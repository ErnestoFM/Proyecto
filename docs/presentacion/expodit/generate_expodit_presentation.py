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

EXPODIT_DIR = r"d:\ernestofm\Proyecto\docs\presentacion\expodit"
ASSETS_DIR = os.path.join(EXPODIT_DIR, "assets")
DOWNLOADS_DIR = r"c:\Users\erfierro\Downloads"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Helper to read base64 image
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
img_login = get_base64_img(r"docs\entregables\img\evidencia4_login.png")
img_pos = get_base64_img(r"docs\entregables\img\evidencia3_pos.png")
img_admin = get_base64_img(r"docs\entregables\img\evidencia5_admin.png")
img_web = get_base64_img(r"docs\entregables\img\m3_despliegue_web.png")

raw_paths = {
    "udg": os.path.abspath(r"docs\entregables\img\escudo_udg_oficial.png"),
    "monchis": os.path.abspath(r"docs\entregables\monchis_logo_badge.png"),
    "arch": os.path.abspath(r"docs\presentacion\expodit\assets\diagrama_arquitectura_monchis.png"),
    "ods": os.path.abspath(r"docs\presentacion\expodit\assets\diagrama_ods_monchis.png"),
    "login": os.path.abspath(r"docs\entregables\img\evidencia4_login.png"),
    "pos": os.path.abspath(r"docs\entregables\img\evidencia3_pos.png"),
    "admin": os.path.abspath(r"docs\entregables\img\evidencia5_admin.png"),
    "web": os.path.abspath(r"docs\entregables\img\m3_despliegue_web.png"),
}

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
    background: #5A4A42;
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
    background: #FAF7F2;
    position: relative;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 0.6in 0.8in 0.5in 0.8in;
  }}

  /* Top decorative bar */
  .slide::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 8px;
    background: linear-gradient(90deg, #8C6B52 0%, #C49A70 35%, #2F855A 70%, #1A365D 100%);
  }}

  /* Header */
  .slide-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 2px solid #E6DCD1;
    padding-bottom: 0.2in;
    margin-bottom: 0.25in;
  }}
  .header-titles {{
    flex: 1;
  }}
  .header-badge {{
    display: inline-block;
    background: #F0E6D8;
    color: #8C6B52;
    font-size: 11pt;
    font-weight: 800;
    padding: 3px 12px;
    border-radius: 12px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 4px;
    border: 1px solid #DBCAB8;
  }}
  .header-title {{
    font-size: 26pt;
    font-weight: 900;
    color: #1A365D;
    line-height: 1.15;
    letter-spacing: -0.5px;
  }}
  .header-subtitle {{
    font-size: 13pt;
    color: #7A6657;
    font-weight: 600;
    margin-top: 4px;
  }}
  .header-logos {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}
  .header-logos img {{
    height: 52px;
    object-fit: contain;
  }}

  /* Content area */
  .slide-body {{
    flex: 1;
    display: flex;
    gap: 0.4in;
    align-items: stretch;
    min-height: 0;
  }}

  /* Footer */
  .slide-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1.5px solid #E6DCD1;
    padding-top: 0.15in;
    margin-top: 0.2in;
    font-size: 10.5pt;
    color: #8C7869;
    font-weight: 600;
  }}
  .slide-footer .student-info {{
    display: flex;
    gap: 14px;
    align-items: center;
  }}
  .slide-footer .pill {{
    background: #EAE1D5;
    color: #5D493B;
    padding: 2px 8px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 9.5pt;
  }}

  /* Slide 1: Cover */
  .cover-slide {{
    background: linear-gradient(135deg, #FAF7F2 0%, #F5ECE0 55%, #EDE2D2 100%);
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 0.8in 1in;
  }}
  .cover-top {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 40px;
    margin-bottom: 24px;
  }}
  .cover-top img.logo-udg {{
    height: 90px;
  }}
  .cover-top img.logo-monchis {{
    height: 95px;
  }}
  .cover-badge-event {{
    display: inline-block;
    background: #1A365D;
    color: #FFFFFF;
    font-size: 13pt;
    font-weight: 800;
    padding: 6px 22px;
    border-radius: 20px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(26,54,93,0.15);
  }}
  .cover-title {{
    font-size: 38pt;
    font-weight: 900;
    color: #4A3324;
    line-height: 1.15;
    margin-bottom: 12px;
    letter-spacing: -0.5px;
  }}
  .cover-title span {{
    color: #2F855A;
  }}
  .cover-subtitle {{
    font-size: 18pt;
    font-weight: 600;
    color: #7A604D;
    max-width: 1000px;
    margin: 0 auto 30px auto;
    line-height: 1.35;
  }}
  .cover-meta-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    width: 100%;
    max-width: 1100px;
    margin-top: 10px;
  }}
  .cover-meta-card {{
    background: #FFFFFF;
    border: 1.5px solid #E0D3C5;
    border-radius: 12px;
    padding: 14px 16px;
    text-align: left;
    box-shadow: 0 4px 14px rgba(140, 107, 82, 0.08);
  }}
  .cover-meta-card .label {{
    font-size: 9.5pt;
    font-weight: 800;
    color: #8C6B52;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .cover-meta-card .val {{
    font-size: 12.5pt;
    font-weight: 800;
    color: #1A365D;
    margin-top: 4px;
    line-height: 1.25;
  }}
  .cover-meta-card .sub {{
    font-size: 9.5pt;
    color: #718096;
    margin-top: 2px;
  }}

  /* General Card Styles */
  .card {{
    background: #FFFFFF;
    border-radius: 14px;
    border: 1.5px solid #E5DCD2;
    padding: 20px;
    box-shadow: 0 4px 16px rgba(140, 107, 82, 0.06);
    display: flex;
    flex-direction: column;
  }}
  .card-header {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1.5px solid #F0E8DE;
  }}
  .card-icon {{
    width: 38px;
    height: 38px;
    border-radius: 8px;
    background: #F5EFEB;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18pt;
  }}
  .card-title {{
    font-size: 14pt;
    font-weight: 800;
    color: #1A365D;
  }}
  .card-text {{
    font-size: 11pt;
    color: #4A5568;
    line-height: 1.5;
  }}
  .card-list {{
    list-style: none;
    margin-top: 8px;
  }}
  .card-list li {{
    position: relative;
    padding-left: 20px;
    margin-bottom: 8px;
    font-size: 11pt;
    color: #4A5568;
    line-height: 1.45;
  }}
  .card-list li::before {{
    content: "•";
    position: absolute;
    left: 4px;
    color: #8C6B52;
    font-size: 16pt;
    line-height: 1;
    top: -2px;
  }}
  .card-list li strong {{
    color: #2D3748;
  }}

  /* Highlighting tags */
  .tag {{
    display: inline-block;
    padding: 3px 9px;
    border-radius: 6px;
    font-size: 9.5pt;
    font-weight: 700;
  }}
  .tag-green {{ background: #DEF7EC; color: #03543F; }}
  .tag-blue {{ background: #E1EFFE; color: #1E429F; }}
  .tag-brown {{ background: #F6EBDD; color: #7B4722; }}
  .tag-red {{ background: #FDE8E8; color: #9B1C1C; }}

  /* Columns layout */
  .col-1-2 {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}
  .col-2-3 {{
    flex: 2;
  }}
  .col-1-3 {{
    flex: 1;
  }}
  .col-half {{
    flex: 1;
  }}

  /* Image showcase wrapper */
  .img-showcase {{
    background: #FFFFFF;
    border: 1.5px solid #E2D9CF;
    border-radius: 14px;
    padding: 10px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
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
    border: 1px solid #EDE4DA;
  }}
  .img-caption {{
    margin-top: 8px;
    font-size: 10pt;
    font-weight: 700;
    color: #718096;
    text-align: center;
  }}

  /* Metrics strip */
  .metric-box {{
    background: #FAF5EF;
    border: 1px solid #E2D5C7;
    border-radius: 10px;
    padding: 12px;
    text-align: center;
  }}
  .metric-val {{
    font-size: 22pt;
    font-weight: 900;
    color: #8C6B52;
    line-height: 1;
  }}
  .metric-lbl {{
    font-size: 9.5pt;
    font-weight: 700;
    color: #4A5568;
    margin-top: 4px;
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
  <div class="cover-badge-event">EXPODIT 2026 • PROYECTO INTEGRADOR DE DESARROLLO DE SOFTWARE</div>
  <h1 class="cover-title">MONCHIS <span>CAFÉ</span></h1>
  <div class="cover-subtitle">Sistema Web de Gestión Segura, Punto de Venta Distribuido y Trazabilidad Agroecológica para Cafetería Orgánica y Comercial</div>
  
  <div class="cover-meta-grid">
    <div class="cover-meta-card">
      <div class="label">Estudiante / Autor</div>
      <div class="val">Ernesto Hatuey Fierro M.</div>
      <div class="sub">Código: 223977036 • Equipo 2</div>
    </div>
    <div class="cover-meta-card">
      <div class="label">Profesor Titular</div>
      <div class="val">Dr. Gabriel Navarro S.</div>
      <div class="sub">Evaluación Final ExpoDIT 100 pts</div>
    </div>
    <div class="cover-meta-card">
      <div class="label">Centro Universitario</div>
      <div class="val">CUTonalá (DIT)</div>
      <div class="sub">Ing. en Ciencias Computacionales</div>
    </div>
    <div class="cover-meta-card">
      <div class="label">Compromiso ONU 2030</div>
      <div class="val">ODS 8, 9, 12 y 16</div>
      <div class="sub">Impacto Social, Verde y Resiliente</div>
    </div>
  </div>
</div>

<!-- SLIDE 2: PROBLEMÁTICA -->
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
    <div class="card" style="flex: 1; border-top: 4px solid #C53030;">
      <div class="card-header">
        <div class="card-icon">📉</div>
        <div class="card-title">Fugas Financieras y Descontrol de Stock</div>
      </div>
      <p class="card-text">
        El registro manual en libretas o software POS genérico provoca hasta un <strong>18% de discrepancias en corte de caja</strong> diario y pérdida de inventario no registrado por falta de mermas tabuladas.
      </p>
      <ul class="card-list" style="margin-top: 14px;">
        <li><strong>Falta de trazabilidad:</strong> Mezcla indiscriminada de granos orgánicos de altura con mezclas comerciales económicas.</li>
        <li><strong>Cálculo analógico de mermas:</strong> Desconocimiento del costo real por taza servida vs volumen de grano comprado.</li>
        <li><strong>Vulnerabilidad en cobro:</strong> Ausencia de validación cruzada entre tickets emitidos y efectivo en bóveda.</li>
      </ul>
      <div style="margin-top: auto; padding-top: 12px;">
        <span class="tag tag-red">Impacto: -18% Rentabilidad</span>
      </div>
    </div>

    <div class="card" style="flex: 1; border-top: 4px solid #D69E2E;">
      <div class="card-header">
        <div class="card-icon">🏷️</div>
        <div class="card-title">Opacidad de Origen y Comercio Injusto</div>
      </div>
      <p class="card-text">
        Los consumidores actuales exigen certidumbre del grano que consumen. La cadena de suministro convencional castiga a las pequeñas cooperativas campesinas con intermediación abusiva.
      </p>
      <ul class="card-list" style="margin-top: 14px;">
        <li><strong>Inexistencia de certificación digital:</strong> Imposible validar al cliente el lote de origen (Chiapas, Oaxaca, Veracruz).</li>
        <li><strong>Falta de incentivos al barista:</strong> El personal carece de guías técnicas digitales para recetas de extracción.</li>
        <li><strong>Desconfianza del consumidor:</strong> Riesgo de reputación por sospecha de sustitución de producto orgánico.</li>
      </ul>
      <div style="margin-top: auto; padding-top: 12px;">
        <span class="tag tag-brown">Impacto: Pérdida de valor agregado</span>
      </div>
    </div>

    <div class="card" style="flex: 1; border-top: 4px solid #2F855A;">
      <div class="card-header">
        <div class="card-icon">🥤</div>
        <div class="card-title">Huella Ecológica de Desechables</div>
      </div>
      <p class="card-text">
        En entornos universitarios y comerciales urbanos, una sola barra genera miles de vasos de polipapel y plástico al mes que terminan en vertederos sin opción de reciclaje.
      </p>
      <ul class="card-list" style="margin-top: 14px;">
        <li><strong>Incentivos nulos:</strong> Los sistemas convencionales no premian de forma automatizada al cliente que aporta termo reusable.</li>
        <li><strong>Falta de métricas verdes:</strong> La administración no puede cuantificar su huella de carbono ahorrada.</li>
        <li><strong>Incumplimiento de normativas:</strong> Rezago ante leyes estatales de reducción de plásticos de un solo uso.</li>
      </ul>
      <div style="margin-top: auto; padding-top: 12px;">
        <span class="tag tag-green">Meta: Evitar +4,500 vasos/año</span>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 2 / 13</div>
  </div>
</div>

<!-- SLIDE 3: ODS ONU -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Alineación Estratégica ONU 2030</div>
      <div class="header-title">Justificación e Impacto en los ODS</div>
      <div class="header-subtitle">Monchis Café como agente de transformación tecnológica, económica y ambiental</div>
    </div>
    <div class="header-logos">
      <img src="{img_udg}" alt="UDG">
      <img src="{img_monchis}" alt="Monchis">
    </div>
  </div>
  
  <div class="slide-body">
    <div class="col-half" style="display: flex; flex-direction: column; justify-content: space-between;">
      <div class="card" style="border-left: 5px solid #2F855A;">
        <div class="card-header">
          <div class="card-icon">🌱</div>
          <div class="card-title">ODS 12: Producción y Consumo Responsables</div>
        </div>
        <p class="card-text">
          Implementación nativa del motor de <strong>Sellos Ecológicos Monchis Rewards</strong>: cada orden donde el cliente presenta termo reusable descuenta automáticamente 1 vaso desechable del contador ecológico global y acredita un beneficio directo al cliente.
        </p>
      </div>

      <div class="card" style="border-left: 5px solid #8C6B52;">
        <div class="card-header">
          <div class="card-icon">☕</div>
          <div class="card-title">ODS 8: Trabajo Decente y Crecimiento Económico</div>
        </div>
        <p class="card-text">
          Trazabilidad por lote que conecta las compras de la cafetería con cooperativas cafetaleras independientes en Chiapas y Veracruz, asegurando un <strong>margen directo +35% superior</strong> frente a los comercializadores especulativos.
        </p>
      </div>

      <div class="card" style="border-left: 5px solid #2B6CB0;">
        <div class="card-header">
          <div class="card-icon">☁️</div>
          <div class="card-title">ODS 9 & 16: Innovación, Infraestructura y Seguridad</div>
        </div>
        <p class="card-text">
          Arquitectura cloud-native elástica en Google Cloud Run y bus de eventos asíncronos RabbitMQ. Registro de auditoría criptográfica SHA-256 para prevenir fraudes contables y garantizar transparencia institucional.
        </p>
      </div>
    </div>

    <div class="col-half">
      <div class="img-showcase">
        <img src="{img_ods}" alt="Diagrama Oficial ODS Monchis Café">
        <div class="img-caption">Figura 1: Matriz Gráfica de Métricas e Indicadores de Impacto Sostenible (ODS 12, 8, 9, 16)</div>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 3 / 13</div>
  </div>
</div>

<!-- SLIDE 4: OBJETIVO DEL PROYECTO -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Alcance & Directrices Técnicas</div>
      <div class="header-title">Objetivos del Proyecto Monchis Café</div>
      <div class="header-subtitle">Metas de desarrollo formal de software para la gestión comercial y ecológica</div>
    </div>
    <div class="header-logos">
      <img src="{img_udg}" alt="UDG">
      <img src="{img_monchis}" alt="Monchis">
    </div>
  </div>
  
  <div class="slide-body">
    <div class="col-half" style="display: flex; flex-direction: column; gap: 16px;">
      <div class="card" style="background: linear-gradient(135deg, #FAF5EF 0%, #FFFFFF 100%); border-left: 5px solid #1A365D;">
        <div class="card-header">
          <div class="card-icon">🎯</div>
          <div class="card-title">Objetivo General</div>
        </div>
        <p class="card-text" style="font-size: 12pt; font-weight: 500; color: #2D3748; line-height: 1.6;">
          Diseñar, construir e implementar una <strong>plataforma web integral y distribuida</strong> para la administración comercial de Monchis Café, garantizando transacciones seguras bajo arquitectura orientada a eventos, control riguroso de inventario de granos orgánicos y mezclas comerciales, y un ecosistema de fidelización sustentable alineado a la Agenda 2030 de la ONU.
        </p>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-icon">📊</div>
          <div class="card-title">Métricas de Éxito Cuantitativas</div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 4px;">
          <div class="metric-box">
            <div class="metric-val">&lt; 200 ms</div>
            <div class="metric-lbl">Tiempo de Respuesta API</div>
          </div>
          <div class="metric-box">
            <div class="metric-val">100%</div>
            <div class="metric-lbl">Consistencia en Cortes de Caja</div>
          </div>
          <div class="metric-box">
            <div class="metric-val">0</div>
            <div class="metric-lbl">Pérdida de Transacciones (Saga)</div>
          </div>
          <div class="metric-box">
            <div class="metric-val">99.9%</div>
            <div class="metric-lbl">Disponibilidad en Nube (GCP)</div>
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
        <ul class="card-list" style="font-size: 11pt;">
          <li>
            <strong>1. Transaccionalidad Concurrente y Resiliente:</strong><br>
            Construir un motor de pedidos asíncrono con RabbitMQ que soporte picos matutinos sin bloqueos en el punto de venta.
          </li>
          <li>
            <strong>2. Seguridad Perimetral y Control de Acceso (RBAC):</strong><br>
            Asegurar endpoints mediante tokens criptográficos JWT (RS256), protección contra ataques de fuerza bruta y filtrado reCAPTCHA Enterprise.
          </li>
          <li>
            <strong>3. Doble Catálogo y Control de Mermas:</strong><br>
            Distinguir inventario orgánico certificado vs comercial y descontar gramos de café e insumos automáticamente por receta.
          </li>
          <li>
            <strong>4. Módulo Verde Monchis Rewards:</strong><br>
            Premiar al cliente sustentable mediante sellos ecológicos digitales integrados al ticket de venta.
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
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 4 / 13</div>
  </div>
</div>

<!-- SLIDE 5: SOLUCIÓN PROPUESTA (GENIALIDADES) -->
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
    <div class="card" style="flex: 1; border-top: 4px solid #8C6B52;">
      <div class="card-header">
        <div class="card-icon">⚡</div>
        <div class="card-title">1. Resiliencia Saga con RabbitMQ</div>
      </div>
      <p class="card-text">
        Si se cae la red o el gateway bancario en mitad de una orden, el <strong>Patrón Saga con compensación transaccional</strong> y Dead Letter Queue (DLQ) asegura que jamás se cobre sin descontar stock ni se pierdan órdenes en cola.
      </p>
      <div style="margin-top: 14px; background: #FAF5EF; padding: 10px; border-radius: 8px;">
        <span class="tag tag-brown">Garantía: Cero discrepancias</span>
        <div style="font-size: 9.5pt; color: #7A6657; margin-top: 6px;">Consistencia eventual y aislamiento transaccional probado bajo estrés.</div>
      </div>
    </div>

    <div class="card" style="flex: 1; border-top: 4px solid #2F855A;">
      <div class="card-header">
        <div class="card-icon">🌱</div>
        <div class="card-title">2. Monchis Green Rewards</div>
      </div>
      <p class="card-text">
        Integración de un <strong>algoritmo de recompensas ecológicas en tiempo real</strong>: cada vez que el barista marca "Trae termo reusable", se calcula el sello ecológico, se descuenta el vaso y se audita el ahorro de CO₂ de la cafetería.
      </p>
      <div style="margin-top: 14px; background: #EDF7ED; padding: 10px; border-radius: 8px;">
        <span class="tag tag-green">Gamificación Verde</span>
        <div style="font-size: 9.5pt; color: #235A28; margin-top: 6px;">El cliente acumula sellos que canjea por bebidas orgánicas gratis.</div>
      </div>
    </div>

    <div class="card" style="flex: 1; border-top: 4px solid #2B6CB0;">
      <div class="card-header">
        <div class="card-icon">🛡️</div>
        <div class="card-title">3. Seguridad Grado Corporativo</div>
      </div>
      <p class="card-text">
        Autenticación robusta con <strong>reCAPTCHA Enterprise v3</strong> para neutralizar bots, hashing <strong>bcrypt con salt 12</strong>, tokens criptográficos <strong>JWT RS256</strong> y arquitectura RBAC que blinda datos de ventas y auditoría.
      </p>
      <div style="margin-top: 14px; background: #EBF8FF; padding: 10px; border-radius: 8px;">
        <span class="tag tag-blue">Protección Criptográfica</span>
        <div style="font-size: 9.5pt; color: #2B6CB0; margin-top: 6px;">Pruebas de humo verificadas en 100% de los casos críticos.</div>
      </div>
    </div>

    <div class="card" style="flex: 1; border-top: 4px solid #1A365D;">
      <div class="card-header">
        <div class="card-icon">☁️</div>
        <div class="card-title">4. Serverless Cloud Run</div>
      </div>
      <p class="card-text">
        Contenedores Docker desplegados sobre <strong>Google Cloud Platform</strong> con autoescalado de 0 a N instancias según demanda. En periodos sin clientes los costos bajan a cero, optimizando al máximo el presupuesto del negocio.
      </p>
      <div style="margin-top: 14px; background: #EEF2F6; padding: 10px; border-radius: 8px;">
        <span class="tag tag-blue">Escalabilidad Elástica</span>
        <div style="font-size: 9.5pt; color: #1A365D; margin-top: 6px;">Despliegue activo y monitoreado mediante Cloud Logging.</div>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 5 / 13</div>
  </div>
</div>

<!-- SLIDE 6: ARQUITECTURA DEL SOFTWARE (GRAPHIC DIAGRAM) -->
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
        <div class="img-caption">Figura 2: Diagrama de 5 Capas de Software Monchis Café (Frontend, API Gateway, Bus, Persistencia e Infraestructura)</div>
      </div>
    </div>

    <div class="col-half" style="flex: 0.9; display: flex; flex-direction: column; justify-content: space-between;">
      <div class="card" style="border-left: 4px solid #8C6B52;">
        <div class="card-title" style="font-size: 12pt; color: #8C6B52;">Capa 1: Interfaz Reactiva (Vue 3 / Vite)</div>
        <p class="card-text" style="font-size: 10.5pt; margin-top: 4px;">
          Punto de Venta reactivo (POS), Gestión de Catálogo y Dashboard de Administrador con Pinia State y componentes Tailwind optimizados para tablets y monitores touch.
        </p>
      </div>

      <div class="card" style="border-left: 4px solid #2B6CB0;">
        <div class="card-title" style="font-size: 12pt; color: #2B6CB0;">Capa 2: API Gateway & Core (Next.js 14)</div>
        <p class="card-text" style="font-size: 10.5pt; margin-top: 4px;">
          Rutas API seguras con middleware de validación JWT, control RBAC (Admin, Barista, Auditor), sanitización de payloads y validación de tokens de reCAPTCHA.
        </p>
      </div>

      <div class="card" style="border-left: 4px solid #DD6B20;">
        <div class="card-title" style="font-size: 12pt; color: #DD6B20;">Capa 3: Bus Asíncrono (RabbitMQ Saga)</div>
        <p class="card-text" style="font-size: 10.5pt; margin-top: 4px;">
          Colas independientes para eventos <code>order.created</code>, <code>inventory.deduct</code> y <code>points.accrue</code> con Dead Letter Queue para tolerancia a fallas.
        </p>
      </div>

      <div class="card" style="border-left: 4px solid #2F855A;">
        <div class="card-title" style="font-size: 12pt; color: #2F855A;">Capa 4 & 5: Persistencia & Cloud Run</div>
        <p class="card-text" style="font-size: 10.5pt; margin-top: 4px;">
          PostgreSQL Cloud SQL con Prisma ORM (migraciones estrictas), Redis para caché de sesión y contenedores Docker administrados en Google Cloud Platform.
        </p>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 6 / 13</div>
  </div>
</div>

<!-- SLIDE 7: HERRAMIENTAS Y STACK TECNOLÓGICO -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Ecosistema & Herramientas de Desarrollo</div>
      <div class="header-title">Stack Tecnológico Seleccionado</div>
      <div class="header-subtitle">Tecnologías modernas, probadas en producción e interoperables</div>
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
        <li><strong>TypeScript:</strong> Tipado estático estricto en modelos de productos, órdenes y usuarios.</li>
        <li><strong>Tailwind CSS:</strong> Sistema de diseño con paleta cálida pastel personalizada para Monchis Café.</li>
        <li><strong>Pinia State:</strong> Estado global reactivo para el carrito de compras y sellos ecológicos.</li>
      </ul>
      <div style="margin-top: auto; padding-top: 10px;">
        <span class="tag tag-brown">UX/UI Diseñado para Baristas</span>
      </div>
    </div>

    <div class="card" style="flex: 1;">
      <div class="card-header">
        <div class="card-icon">⚙️</div>
        <div class="card-title">Backend & Datos</div>
      </div>
      <ul class="card-list">
        <li><strong>Next.js 14 & Node.js:</strong> API REST modular, serverless functions y middleware de seguridad.</li>
        <li><strong>PostgreSQL 16:</strong> Base de datos relacional ACID para integridad contable absoluta.</li>
        <li><strong>Prisma ORM:</strong> Tipado seguro de consultas SQL y control de esquema reproducible.</li>
        <li><strong>RabbitMQ:</strong> Broker de mensajería asíncrona AMQP para orquestación transaccional Saga.</li>
      </ul>
      <div style="margin-top: auto; padding-top: 10px;">
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
        <li><strong>bcrypt (Salt 12):</strong> Hashing unidireccional de contraseñas de baristas y administradores.</li>
        <li><strong>Google reCAPTCHA v3:</strong> Detección pasiva de bots en formularios de login y recuperación.</li>
        <li><strong>CORS & Helmet:</strong> Cabeceras HTTP endurecidas contra XSS, CSRF y Clickjacking.</li>
      </ul>
      <div style="margin-top: auto; padding-top: 10px;">
        <span class="tag tag-red">Cumplimiento OWASP Top 10</span>
      </div>
    </div>

    <div class="card" style="flex: 1;">
      <div class="card-header">
        <div class="card-icon">🚀</div>
        <div class="card-title">DevOps & Cloud</div>
      </div>
      <ul class="card-list">
        <li><strong>Google Cloud Run:</strong> Ejecución de contenedores escalable a cero con certificado SSL automático.</li>
        <li><strong>Docker:</strong> Empaquetado inmutable multi-stage para optimización de imagen de producción.</li>
        <li><strong>GitHub Actions:</strong> Pipeline CI/CD con linting, pruebas unitarias y despliegue a GCP.</li>
        <li><strong>Cloud Monitoring:</strong> Monitoreo de latencia, tasa de errores HTTP 5xx y uso de memoria.</li>
      </ul>
      <div style="margin-top: auto; padding-top: 10px;">
        <span class="tag tag-green">Infraestructura Elástica</span>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 7 / 13</div>
  </div>
</div>

<!-- SLIDE 8: PRUEBAS DE HUMO (LOGIN & SEGURIDAD) -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Aseguramiento de Calidad de Software</div>
      <div class="header-title">Módulo de Seguridad & Pruebas de Humo (Login)</div>
      <div class="header-subtitle">Validación formal de casos de prueba según formato institucional de laboratorio</div>
    </div>
    <div class="header-logos">
      <img src="{img_udg}" alt="UDG">
      <img src="{img_monchis}" alt="Monchis">
    </div>
  </div>
  
  <div class="slide-body">
    <div class="col-half" style="flex: 1.1;">
      <div class="img-showcase">
        <img src="{img_login}" alt="Captura Real de Login Monchis Café">
        <div class="img-caption">Figura 3: Interfaz de Acceso Seguro Monchis Café con reCAPTCHA Enterprise y Validación en Tiempo Real</div>
      </div>
    </div>

    <div class="col-half" style="flex: 0.9; display: flex; flex-direction: column; justify-content: space-between;">
      <div class="card" style="padding: 14px;">
        <div class="card-title" style="font-size: 11.5pt; color: #1A365D;">Matriz de Casos de Prueba (Smoke Testing)</div>
        <table style="width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 9.5pt;">
          <thead>
            <tr style="background: #EFE8DF; color: #5D493B; text-align: left;">
              <th style="padding: 6px 8px; border: 1px solid #D8C7B5;">ID</th>
              <th style="padding: 6px 8px; border: 1px solid #D8C7B5;">Escenario</th>
              <th style="padding: 6px 8px; border: 1px solid #D8C7B5;">Salida Esperada</th>
              <th style="padding: 6px 8px; border: 1px solid #D8C7B5;">Resultado</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="padding: 5px 8px; border: 1px solid #E6DCD1; font-weight: 700;">CP-01</td>
              <td style="padding: 5px 8px; border: 1px solid #E6DCD1;">Admin con credenciales válidas</td>
              <td style="padding: 5px 8px; border: 1px solid #E6DCD1;">Redirección a /admin/dashboard</td>
              <td style="padding: 5px 8px; border: 1px solid #E6DCD1;"><span class="tag tag-green">EXITOSO</span></td>
            </tr>
            <tr>
              <td style="padding: 5px 8px; border: 1px solid #E6DCD1; font-weight: 700;">CP-02</td>
              <td style="padding: 5px 8px; border: 1px solid #E6DCD1;">Barista con credenciales válidas</td>
              <td style="padding: 5px 8px; border: 1px solid #E6DCD1;">Redirección a vista POS /pos</td>
              <td style="padding: 5px 8px; border: 1px solid #E6DCD1;"><span class="tag tag-green">EXITOSO</span></td>
            </tr>
            <tr>
              <td style="padding: 5px 8px; border: 1px solid #E6DCD1; font-weight: 700;">CP-03</td>
              <td style="padding: 5px 8px; border: 1px solid #E6DCD1;">Password erróneo (3 intentos)</td>
              <td style="padding: 5px 8px; border: 1px solid #E6DCD1;">Bloqueo temporal 60s (Rate Limit)</td>
              <td style="padding: 5px 8px; border: 1px solid #E6DCD1;"><span class="tag tag-green">EXITOSO</span></td>
            </tr>
            <tr>
              <td style="padding: 5px 8px; border: 1px solid #E6DCD1; font-weight: 700;">CP-04</td>
              <td style="padding: 5px 8px; border: 1px solid #E6DCD1;">Fallo de token reCAPTCHA</td>
              <td style="padding: 5px 8px; border: 1px solid #E6DCD1;">Rechazo con código HTTP 403</td>
              <td style="padding: 5px 8px; border: 1px solid #E6DCD1;"><span class="tag tag-green">EXITOSO</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="card" style="padding: 14px; background: #FAF5EF; border-left: 4px solid #2F855A;">
        <div class="card-title" style="font-size: 11pt; color: #2F855A;">Mecanismo de Autorización RBAC</div>
        <p class="card-text" style="font-size: 9.5pt; margin-top: 4px;">
          El token JWT contiene claims firmados con roles estrictos (<code>ADMIN</code>, <code>BARISTA</code>). Un Barista autenticado que intente ingresar a rutas contables recibe denegación inmediata sin exponer datos de servidor.
        </p>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 8 / 13</div>
  </div>
</div>

<!-- SLIDE 9: PUNTO DE VENTA (POS) & REWARDS -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Operación en Barra & Experiencia de Usuario</div>
      <div class="header-title">Módulo POS & Sellos Ecológicos Rewards</div>
      <div class="header-subtitle">Interfaz táctil de alta velocidad con cálculo de impacto ambiental en tiempo real</div>
    </div>
    <div class="header-logos">
      <img src="{img_udg}" alt="UDG">
      <img src="{img_monchis}" alt="Monchis">
    </div>
  </div>
  
  <div class="slide-body">
    <div class="col-half" style="flex: 1.1;">
      <div class="img-showcase">
        <img src="{img_pos}" alt="Captura Real del POS Monchis Café">
        <div class="img-caption">Figura 4: Punto de Venta con Carrito Reactivo, Métodos de Pago y Casilla de Termo Reusable</div>
      </div>
    </div>

    <div class="col-half" style="flex: 0.9; display: flex; flex-direction: column; justify-content: space-between;">
      <div class="card" style="border-left: 4px solid #2F855A;">
        <div class="card-header">
          <div class="card-icon">🌱</div>
          <div class="card-title">Innovación del Botón Ecológico</div>
        </div>
        <p class="card-text" style="font-size: 10.5pt;">
          Al activar <strong>"Trae termo reusable (+1 sello ecológico)"</strong>, el sistema ejecuta tres acciones atómicas:
        </p>
        <ul class="card-list" style="font-size: 10pt; margin-top: 6px;">
          <li>Acredita automáticamente el sello en la billetera de lealtad del cliente.</li>
          <li>Descuenta cero vasos desechables del inventario de insumos de empaque.</li>
          <li>Suma 1 impacto al contador de mitigación ambiental de la cooperativa.</li>
        </ul>
      </div>

      <div class="card" style="border-left: 4px solid #8C6B52;">
        <div class="card-header">
          <div class="card-icon">⚡</div>
          <div class="card-title">Flujo de Cobro Multi-Método</div>
        </div>
        <p class="card-text" style="font-size: 10.5pt;">
          Diseñado para absorber filas rápidas de cambio de clase: selección táctil con badges de café orgánico vs alimento comercial, soporte para <strong>Efectivo, Tarjeta, Transferencia y Mixto</strong> con cálculo exacto de cambio.
        </p>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 9 / 13</div>
  </div>
</div>

<!-- SLIDE 10: PANEL ADMINISTRATIVO & TRAZABILIDAD -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Gestión Gerencial & Auditoría</div>
      <div class="header-title">Panel Administrativo & Trazabilidad Agroecológica</div>
      <div class="header-subtitle">Control integral de inventarios, reportes de corte y procedencia de cooperativas</div>
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
        <div class="img-caption">Figura 5: Tablero Administrativo con Métricas UTM, Control de Stock y Registro de Ventas</div>
      </div>
    </div>

    <div class="col-half" style="flex: 0.9; display: flex; flex-direction: column; justify-content: space-between;">
      <div class="card" style="border-left: 4px solid #1A365D;">
        <div class="card-header">
          <div class="card-icon">📦</div>
          <div class="card-title">Control de Stock por Gramaje y Receta</div>
        </div>
        <p class="card-text" style="font-size: 10.5pt;">
          Cada bebida vendida descuenta automáticamente los gramos exactos de grano (p. ej. 18g por espresso doble orgánico Chiapas) y mililitros de leche, alertando al administrador antes de que se agote el lote.
        </p>
      </div>

      <div class="card" style="border-left: 4px solid #8C6B52;">
        <div class="card-header">
          <div class="card-icon">🤝</div>
          <div class="card-title">Trazabilidad Directa de Cooperativa</div>
        </div>
        <p class="card-text" style="font-size: 10.5pt;">
          Registro documental de lotes: productor asociado, fecha de cosecha, altitud del cultivo (1,400 msnm) y nota de cata. El sistema genera etiquetas QR que demuestran la autenticidad al comensal.
        </p>
      </div>

      <div class="card" style="border-left: 4px solid #2F855A;">
        <div class="card-header">
          <div class="card-icon">📊</div>
          <div class="card-title">Métricas de Campaña y Cortes Diarios</div>
        </div>
        <p class="card-text" style="font-size: 10.5pt;">
          Monitoreo analítico de ventas por turno, tasa de conversión y balance contable consolidado exportable a PDF y hojas de cálculo para el auditor.
        </p>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 10 / 13</div>
  </div>
</div>

<!-- SLIDE 11: VENTAJAS COMPETITIVAS -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Propuesta de Valor & Mercado</div>
      <div class="header-title">Ventajas Competitivas de Monchis Café</div>
      <div class="header-subtitle">Comparativa frente a sistemas POS comerciales tradicionales</div>
    </div>
    <div class="header-logos">
      <img src="{img_udg}" alt="UDG">
      <img src="{img_monchis}" alt="Monchis">
    </div>
  </div>
  
  <div class="slide-body">
    <div class="card" style="flex: 1; border-top: 4px solid #2F855A;">
      <div class="card-header">
        <div class="card-icon">🌱</div>
        <div class="card-title">Fidelización de Triple Impacto</div>
      </div>
      <p class="card-text">
        A diferencia de programas comerciales que solo otorgan puntos por dinero gastado, Monchis Café vincula los puntos al <strong>comportamiento ecológico</strong> y fomenta el hábito verde en la comunidad universitaria.
      </p>
      <ul class="card-list" style="margin-top: 10px;">
        <li>Retención de clientes jóvenes con conciencia ambiental.</li>
        <li>Ahorro directo en compras mayoristas de vasos y tapas.</li>
      </ul>
    </div>

    <div class="card" style="flex: 1; border-top: 4px solid #8C6B52;">
      <div class="card-header">
        <div class="card-icon">⚡</div>
        <div class="card-title">Cero Bloqueos Transaccionales</div>
      </div>
      <p class="card-text">
        Los sistemas monolíticos se congelan cuando falla internet o la base de datos externa. Con RabbitMQ y colas locales de resguardo, el cajero puede seguir cobrando sin detener la fila.
      </p>
      <ul class="card-list" style="margin-top: 10px;">
        <li>Arquitectura orientada a eventos desacoplada.</li>
        <li>Sincronización automática al restablecerse la red.</li>
      </ul>
    </div>

    <div class="card" style="flex: 1; border-top: 4px solid #2B6CB0;">
      <div class="card-header">
        <div class="card-icon">💰</div>
        <div class="card-title">Ahorro de Costos Operativos</div>
      </div>
      <p class="card-text">
        Sin licencias mensuales abusivas ni hardware propietario costoso. Corre sobre cualquier navegador moderno en tablets convencionales y escala a costo cero en Google Cloud Run.
      </p>
      <ul class="card-list" style="margin-top: 10px;">
        <li>Open Source y adaptabilidad total al negocio.</li>
        <li>Infraestructura en la nube con cobro por uso real.</li>
      </ul>
    </div>

    <div class="card" style="flex: 1; border-top: 4px solid #1A365D;">
      <div class="card-header">
        <div class="card-icon">🔒</div>
        <div class="card-title">Seguridad y Cumplimiento</div>
      </div>
      <p class="card-text">
        Diseñado bajo directrices OWASP y estándares bancarios: hashing criptográfico, cifrado en tránsito TLS 1.3 y registro inmutable de auditoría para evitar fraudes internos.
      </p>
      <ul class="card-list" style="margin-top: 10px;">
        <li>Control estricto de roles de acceso (RBAC).</li>
        <li>Protección contra bots con Google reCAPTCHA.</li>
      </ul>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 11 / 13</div>
  </div>
</div>

<!-- SLIDE 12: RECOMENDACIONES & TRABAJO FUTURO -->
<div class="slide">
  <div class="slide-header">
    <div class="header-titles">
      <div class="header-badge">Evolución & Escalabilidad</div>
      <div class="header-title">Recomendaciones & Trabajo Futuro</div>
      <div class="header-subtitle">Hoja de ruta estratégica para la consolidación comercial del sistema</div>
    </div>
    <div class="header-logos">
      <img src="{img_udg}" alt="UDG">
      <img src="{img_monchis}" alt="Monchis">
    </div>
  </div>
  
  <div class="slide-body">
    <div class="col-half" style="display: flex; flex-direction: column; gap: 16px;">
      <div class="card" style="border-left: 4px solid #8C6B52;">
        <div class="card-header">
          <div class="card-icon">📱</div>
          <div class="card-title">1. Aplicación Móvil PWA para Clientes (Pick & Go)</div>
        </div>
        <p class="card-text">
          Desarrollar la Progressive Web App para estudiantes y académicos, permitiendo ordenar con anticipación, seleccionar especificaciones de tostado y recoger la bebida sin hacer fila en hora pico.
        </p>
      </div>

      <div class="card" style="border-left: 4px solid #2B6CB0;">
        <div class="card-header">
          <div class="card-icon">💳</div>
          <div class="card-title">2. Integración de Pasarelas de Pago Físicas</div>
        </div>
        <p class="card-text">
          Conectar terminales punto de venta inteligentes mediante el SDK de Clip o Stripe Terminal con lectura directa de chip y tecnología contactless (NFC / Apple Pay / Google Wallet).
        </p>
      </div>
    </div>

    <div class="col-half" style="display: flex; flex-direction: column; gap: 16px;">
      <div class="card" style="border-left: 4px solid #2F855A;">
        <div class="card-header">
          <div class="card-icon">🤖</div>
          <div class="card-title">3. Modelos Predictivos de Demanda de Café (IA / ML)</div>
        </div>
        <p class="card-text">
          Implementar modelos de series temporales en BigQuery ML para pronosticar la necesidad de kilogramos de grano orgánico en función del clima, días festivos universitarios y periodos de exámenes.
        </p>
      </div>

      <div class="card" style="border-left: 4px solid #1A365D;">
        <div class="card-header">
          <div class="card-icon">🔗</div>
          <div class="card-title">4. Trazabilidad Blockchain para Caficultores</div>
        </div>
        <p class="card-text">
          Registrar el historial de cada lote de café en una red de libro mayor descentralizado permisionado, garantizando al comensal el pago íntegro y justo a las familias productoras de Chiapas.
        </p>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 12 / 13</div>
  </div>
</div>

<!-- SLIDE 13: CONCLUSIONES & DEMO EN VIVO -->
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
        <div class="img-caption">Figura 6: Despliegue en Vivo del Sistema Web Monchis Café en Google Cloud Platform</div>
      </div>
    </div>

    <div class="col-half" style="flex: 0.9; display: flex; flex-direction: column; justify-content: space-between;">
      <div class="card" style="border-left: 4px solid #2F855A;">
        <div class="card-title" style="font-size: 12pt; color: #2F855A;">1. Solución Tecnológica Integral</div>
        <p class="card-text" style="font-size: 10.5pt; margin-top: 4px;">
          Se cumplió con el <strong>100% de los requisitos del Proyecto Integrador</strong>: transaccionalidad robusta, control de usuarios con roles seguros, mantenimiento relacional y respuesta rápida.
        </p>
      </div>

      <div class="card" style="border-left: 4px solid #8C6B52;">
        <div class="card-title" style="font-size: 12pt; color: #8C6B52;">2. Impacto Socio-Ambiental Tangible</div>
        <p class="card-text" style="font-size: 10.5pt; margin-top: 4px;">
          El software trasciende la función contable: apoya a cooperativas campesinas locales (ODS 8) y combate el plástico de un solo uso en campus universitarios (ODS 12).
        </p>
      </div>

      <div class="card" style="border-left: 4px solid #1A365D; background: #FAF5EF;">
        <div class="card-title" style="font-size: 12pt; color: #1A365D;">3. Madurez de Ingeniería en ExpoDIT</div>
        <p class="card-text" style="font-size: 10.5pt; margin-top: 4px;">
          La aplicación de patrones formales (Saga, RBAC, CI/CD, Containerización) demuestra el rigor técnico adquirido durante la trayectoria en el <strong>Centro Universitario de Tonalá</strong>.
        </p>
      </div>
    </div>
  </div>

  <div class="slide-footer">
    <div class="student-info">
      <span>Ernesto Hatuey Fierro M. (223977036)</span>
      <span class="pill">Equipo 2</span>
      <span>Profesor: Dr. Gabriel Navarro Salcedo</span>
    </div>
    <div>EXPODIT 2026 • Slide 13 / 13</div>
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

# Copy PDF to Downloads
dest_pdf_downloads = os.path.join(DOWNLOADS_DIR, "Presentacion_ExpoDIT_Monchis_Cafe.pdf")
shutil.copy2(pdf_path, dest_pdf_downloads)
print(f"PDF copied to Downloads: {dest_pdf_downloads}")

# =========================================================================
# GENERATE EDITABLE PPTX (python-pptx)
# =========================================================================
print("Generating PowerPoint PPTX presentation...")
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Color constants
C_BG = RGBColor(250, 247, 242)
C_PRIMARY = RGBColor(140, 107, 82)
C_NAVY = RGBColor(26, 54, 93)
C_GREEN = RGBColor(47, 133, 90)
C_DARK = RGBColor(45, 55, 72)
C_MUTED = RGBColor(113, 128, 150)
C_WHITE = RGBColor(255, 255, 255)
C_CARD_BG = RGBColor(255, 255, 255)
C_CARD_BORDER = RGBColor(226, 217, 207)

def add_header(slide, badge, title, subtitle):
    # Header container
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(9.5), Inches(1.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = badge.upper()
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = C_PRIMARY
    
    p1 = tf.add_paragraph()
    p1.text = title
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY
    
    p2 = tf.add_paragraph()
    p2.text = subtitle
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_MUTED
    
    # Logos
    if os.path.exists(raw_paths["udg"]):
        slide.shapes.add_picture(raw_paths["udg"], Inches(10.8), Inches(0.4), height=Inches(0.9))
    if os.path.exists(raw_paths["monchis"]):
        slide.shapes.add_picture(raw_paths["monchis"], Inches(11.9), Inches(0.4), height=Inches(0.9))

def add_footer(slide, current_slide, total_slides=13):
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.4))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"Ernesto Hatuey Fierro M. (223977036) | Equipo 2 • CUTonalá (DIT) | Dr. Gabriel Navarro Salcedo | Slide {current_slide} / {total_slides}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_MUTED

# Slide 1: Cover
s1 = prs.slides.add_slide(blank_layout)
if os.path.exists(raw_paths["udg"]):
    s1.shapes.add_picture(raw_paths["udg"], Inches(5.0), Inches(0.8), height=Inches(1.2))
if os.path.exists(raw_paths["monchis"]):
    s1.shapes.add_picture(raw_paths["monchis"], Inches(6.8), Inches(0.8), height=Inches(1.2))

tb_c = s1.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.333), Inches(3.2))
tf_c = tb_c.text_frame
tf_c.word_wrap = True
p = tf_c.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
p.text = "EXPODIT 2026 • PROYECTO INTEGRADOR DE DESARROLLO DE SOFTWARE"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_NAVY

p = tf_c.add_paragraph()
p.alignment = PP_ALIGN.CENTER
p.text = "MONCHIS CAFÉ"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = C_PRIMARY

p = tf_c.add_paragraph()
p.alignment = PP_ALIGN.CENTER
p.text = "Sistema Web de Gestión Segura, Punto de Venta Distribuido y Trazabilidad Agroecológica"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_DARK

p = tf_c.add_paragraph()
p.alignment = PP_ALIGN.CENTER
p.text = "Ernesto Hatuey Fierro Meléndez (223977036) • Equipo 2 | CUTonalá Universidad de Guadalajara"
p.font.size = Pt(13)
p.font.color.rgb = C_MUTED

p = tf_c.add_paragraph()
p.alignment = PP_ALIGN.CENTER
p.text = "Titular: Dr. Gabriel Navarro Salcedo | Compromiso ODS 8, 9, 12 y 16"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_GREEN

# Slide 2: Problematica
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "Diagnóstico & Contexto", "Problemática en Cafeterías de Especialidad", "Fugas financieras, falta de trazabilidad y generación excesiva de desechables")
tb = s2.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "1. Fugas Financieras y Descontrol de Inventario:\n• Hasta 18% de discrepancia en cierres de caja por registro manual en libretas.\n• Falta de costeo automático por gramaje en bebidas preparadas.\n\n2. Opacidad en Trazabilidad y Comercio Injusto:\n• Imposibilidad de certificar al comensal el origen campesino del grano orgánico.\n• Intermediación comercial excesiva que castiga el margen de cooperativas.\n\n3. Huella Ecológica de Plásticos de un Solo Uso:\n• Generación masiva de miles de vasos plásticos y polipapel no reciclables en campus.\n• Inexistencia de incentivos automáticos al cliente por usar termo reusable."
add_footer(s2, 2)

# Slide 3: ODS
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "Alineación ONU 2030", "Justificación e Impacto en los ODS", "Contribución directa a los Objetivos de Desarrollo Sostenible")
tb = s3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.5), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "• ODS 12 (Consumo Responsable):\nSello ecológico Monchis Rewards que premia el uso de termos reusables (-4,500 vasos/año).\n\n• ODS 8 (Trabajo Decente):\nCompras directas a cooperativas cafetaleras de Chiapas con +35% de margen directo.\n\n• ODS 9 & 16 (Innovación y Seguridad):\nArquitectura resiliente en Google Cloud Run y auditoría criptográfica SHA-256."
if os.path.exists(raw_paths["ods"]):
    s3.shapes.add_picture(raw_paths["ods"], Inches(6.6), Inches(1.8), width=Inches(5.9))
add_footer(s3, 3)

# Slide 4: Objetivos
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "Alcance Formal", "Objetivos del Proyecto Monchis Café", "Metas de desarrollo formal de ingeniería y métricas clave de calidad")
tb = s4.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "OBJETIVO GENERAL:\nDesarrollar e implementar una plataforma web resiliente, segura y distribuida para la administración integral de punto de venta (POS), inventario con trazabilidad por lote y fidelización ecológica en cafeterías de especialidad.\n\nOBJETIVOS ESPECÍFICOS:\n1. Transaccionalidad Concurrente: Patrón Saga con RabbitMQ para evitar pérdidas de órdenes.\n2. Seguridad RBAC: Roles blindados (Admin vs Barista) con JWT RS256 y reCAPTCHA Enterprise.\n3. Doble Catálogo: Control de mermas por gramaje para café orgánico y convencional.\n4. Módulo Verde: Sistema gamificado Monchis Rewards integrado al ticket de venta.\n5. Despliegue Elástico: Contenedores Docker autoescalables en Google Cloud Run."
add_footer(s4, 4)

# Slide 5: Solución
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "Valor Diferencial", "Solución Propuesta: Las Genialidades de Monchis", "¿Por qué Monchis Café redefine el software de hospitalidad?")
tb = s5.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "1. Resiliencia Saga con RabbitMQ:\nCompensación automática de transacciones y Dead Letter Queue (DLQ) para tolerancia absoluta a fallas de red.\n\n2. Monchis Green Rewards:\nGamificación en barra que acredita sellos ecológicos inmediatos y descuenta desechables del inventario.\n\n3. Seguridad Bancaria y Antifraude:\nTokens asimétricos RS256, hashing bcrypt salt 12 y protección Google reCAPTCHA v3 en tiempo real.\n\n4. Arquitectura Serverless Cloud Run:\nContenedores escalables de 0 a N con facturación bajo demanda y costos mínimos de operación."
add_footer(s5, 5)

# Slide 6: Arquitectura (Image)
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "Ingeniería de Software", "Arquitectura y Diagrama del Sistema", "Estructura distribuida en 5 capas desacopladas por bus de eventos")
if os.path.exists(raw_paths["arch"]):
    s6.shapes.add_picture(raw_paths["arch"], Inches(0.8), Inches(1.8), width=Inches(7.2))
tb = s6.shapes.add_textbox(Inches(8.3), Inches(1.8), Inches(4.2), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "5 CAPAS DESACOPLADAS:\n\n• Capa 1: UI Reactiva (Vue 3 / Vite / Pinia)\n• Capa 2: API Gateway & Core (Next.js 14 / RBAC)\n• Capa 3: Bus Asíncrono (RabbitMQ Saga Pattern)\n• Capa 4: Persistencia Relacional (PostgreSQL / Prisma)\n• Capa 5: Infraestructura Cloud (Google Cloud Run)"
add_footer(s6, 6)

# Slide 7: Herramientas
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "Ecosistema Tecnológico", "Stack Tecnológico y Herramientas", "Herramientas modernas para alta concurrencia y despliegue continuo")
tb = s7.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "• Frontend: Vue 3, Vite, TypeScript, Tailwind CSS, Pinia State Management, Lucide Icons.\n\n• Backend & Microservicios: Next.js 14 API Routes, Node.js runtime, RabbitMQ AMQP, Prisma ORM.\n\n• Bases de Datos: PostgreSQL 16 (Cloud SQL) con integridad referencial ACID estricta y Redis Cache.\n\n• Seguridad: JSON Web Tokens (RS256), bcrypt salt 12, Google reCAPTCHA Enterprise, Helmet/CORS.\n\n• DevOps: Docker Multi-stage, Google Cloud Run, Cloud SQL, GitHub Actions CI/CD y Cloud Monitoring."
add_footer(s7, 7)

# Slide 8: Pruebas de Humo (Login Image)
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "Aseguramiento de Calidad", "Módulo de Seguridad y Pruebas de Humo (Login)", "Reporte formal de pruebas de humo y control RBAC")
if os.path.exists(raw_paths["login"]):
    s8.shapes.add_picture(raw_paths["login"], Inches(0.8), Inches(1.8), width=Inches(6.2))
tb = s8.shapes.add_textbox(Inches(7.3), Inches(1.8), Inches(5.2), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "CASOS DE PRUEBA DE HUMO (SMOKE TESTS):\n\n• CP-01: Admin con credenciales válidas -> Acceso a /admin/dashboard [EXITOSO]\n\n• CP-02: Barista con credenciales válidas -> Acceso a /pos [EXITOSO]\n\n• CP-03: Contraseña errónea (3 intentos) -> Bloqueo temporal por Rate Limit [EXITOSO]\n\n• CP-04: Token reCAPTCHA inválido -> Rechazo HTTP 403 [EXITOSO]\n\nResultado: 100% de pruebas funcionales y de seguridad aprobadas."
add_footer(s8, 8)

# Slide 9: POS (Image)
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "Experiencia en Barra", "Punto de Venta (POS) y Monchis Rewards", "Operación táctil rápida con acreditación automática de sellos ecológicos")
if os.path.exists(raw_paths["pos"]):
    s9.shapes.add_picture(raw_paths["pos"], Inches(0.8), Inches(1.8), width=Inches(6.4))
tb = s9.shapes.add_textbox(Inches(7.5), Inches(1.8), Inches(5.0), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "CARACTERÍSTICAS DEL POS:\n\n• Carrito reactivo con categorías (Café Orgánico, Repostería).\n• Botón ecológico 'Trae termo reusable' (+1 sello verde).\n• Soporte para múltiples métodos de pago (Efectivo, Tarjeta, Transferencia, Mixto).\n• Descuento automático de gramos de café e insumos por receta."
add_footer(s9, 9)

# Slide 10: Admin (Image)
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "Gestión y Auditoría", "Panel Administrativo y Trazabilidad", "Monitoreo en tiempo real de inventarios, cortes y procedencia de grano")
if os.path.exists(raw_paths["admin"]):
    s10.shapes.add_picture(raw_paths["admin"], Inches(0.8), Inches(1.8), width=Inches(6.4))
tb = s10.shapes.add_textbox(Inches(7.5), Inches(1.8), Inches(5.0), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "CAPACIDADES GERENCIALES:\n\n• Control de stock mínimo y alertas automáticas de reorden.\n• Trazabilidad de cooperativas campesinas (Chiapas, Veracruz).\n• Métricas de vasos evitados y huella de carbono mitigada.\n• Auditoría de transacciones contables protegidas contra edición."
add_footer(s10, 10)

# Slide 11: Ventajas
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, "Propuesta de Valor", "Ventajas Competitivas de Monchis Café", "Diferenciadores determinantes en el mercado y la academia")
tb = s11.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "1. Triple Impacto: Fidelización que conjuga economía, sociedad y medio ambiente.\n\n2. Resiliencia Concurrente: Cero órdenes caídas gracias al patrón Saga en RabbitMQ.\n\n3. Costo Operativo Óptimo: Despliegue elástico en GCP Cloud Run con escala a cero en horarios inhábiles.\n\n4. Seguridad Bancaria: Arquitectura blindada conforme a OWASP Top 10 y cifrado asimétrico."
add_footer(s11, 11)

# Slide 12: Recomendaciones
s12 = prs.slides.add_slide(blank_layout)
add_header(s12, "Evolución y Futuro", "Recomendaciones y Trabajo Futuro", "Evolución tecnológica de la plataforma hacia nuevos horizontes")
tb = s12.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "1. Aplicación Móvil PWA Pick & Go para pedidos anticipados sin filas de espera.\n\n2. Conexión de terminales inteligentes de cobro bancario físico (SDK Stripe/Clip).\n\n3. Modelos predictivos de demanda con IA (BigQuery ML) para optimizar compras de cosecha.\n\n4. Registro blockchain permisionado para trazabilidad inmutable desde finca hasta comensal."
add_footer(s12, 12)

# Slide 13: Conclusiones
s13 = prs.slides.add_slide(blank_layout)
add_header(s13, "Cierre Académico", "Conclusiones y Demostración en Vivo", "Cumplimiento integral de objetivos de ingeniería de software")
if os.path.exists(raw_paths["web"]):
    s13.shapes.add_picture(raw_paths["web"], Inches(0.8), Inches(1.8), width=Inches(6.4))
tb = s13.shapes.add_textbox(Inches(7.5), Inches(1.8), Inches(5.0), Inches(4.8))
tf = tb.text_frame
tf.word_wrap = True
tf.text = "CONCLUSIONES:\n\n• 100% de los requerimientos de la asignatura formalmente implementados.\n• Transformación tangible de una cafetería convencional en una empresa digital verde.\n• Despliegue activo y verificado en la nube (Google Cloud Platform).\n• Rigor de ingeniería reflejado en arquitectura, pruebas y compromiso con los ODS."
add_footer(s13, 13)

prs.save(pptx_path)
print(f"PPTX successfully generated: {pptx_path}")

dest_pptx_downloads = os.path.join(DOWNLOADS_DIR, "Presentacion_ExpoDIT_Monchis_Cafe.pptx")
shutil.copy2(pptx_path, dest_pptx_downloads)
print(f"PPTX copied to Downloads: {dest_pptx_downloads}")

print("\nALL PRESENTATION DELIVERABLES SUCCESSFULLY CREATED AND COPIED!")
