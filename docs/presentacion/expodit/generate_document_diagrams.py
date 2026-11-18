import os
import subprocess

OUT_DIR = r"d:\ernestofm\Proyecto\docs\presentacion\expodit\assets"
os.makedirs(OUT_DIR, exist_ok=True)
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def render_html_to_png(html_content, output_png_path, width=1280, height=720):
    temp_html = output_png_path.replace(".png", "_temp.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    cmd = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--screenshot={output_png_path}",
        "--default-background-color=00000000",
        temp_html
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)
    print(f"Generated: {output_png_path}")

# =========================================================================
# 1. PLAN ESTRATÉGICO (DIAGRAMA GRÁFICO)
# =========================================================================
html_plan_est = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }
  body {
    width: 1200px;
    height: 640px;
    background: #FAF7F2;
    padding: 25px 35px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .header {
    border-bottom: 2px solid #8C6B52;
    padding-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .header h2 { font-size: 22px; color: #1A365D; font-weight: 800; }
  .header span { background: #EFE8DF; color: #8C6B52; font-size: 12px; font-weight: 700; padding: 4px 12px; border-radius: 12px; }
  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-top: 15px;
    height: 520px;
  }
  .col {
    background: #FFFFFF;
    border: 1.5px solid #E2D9CF;
    border-radius: 12px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    box-shadow: 0 4px 12px rgba(140, 107, 82, 0.08);
  }
  .col-title {
    background: #8C6B52;
    color: white;
    font-size: 14px;
    font-weight: 800;
    text-align: center;
    padding: 8px;
    border-radius: 8px;
    letter-spacing: 0.5px;
  }
  .col-2 .col-title { background: #2B6CB0; }
  .col-3 .col-title { background: #2F855A; }
  .card-item {
    background: #FAF5EF;
    border-left: 4px solid #8C6B52;
    padding: 10px 12px;
    border-radius: 6px;
    font-size: 11px;
    color: #4A5568;
    line-height: 1.4;
  }
  .col-2 .card-item { border-left-color: #2B6CB0; background: #F0F4F8; }
  .col-3 .card-item { border-left-color: #2F855A; background: #F0F9F4; }
  .card-item strong { color: #1A365D; display: block; margin-bottom: 3px; font-size: 12px; }
  .arrow { text-align: center; color: #8C6B52; font-size: 18px; font-weight: bold; margin: -4px 0; }
</style>
</head>
<body>
  <div class="header">
    <h2>MONCHIS CAFÉ — PLAN ESTRATÉGICO DE DESARROLLO DE SOFTWARE</h2>
    <span>Ingeniería en Ciencias Computacionales • CUTonalá</span>
  </div>
  <div class="grid">
    <div class="col">
      <div class="col-title">FASE 1: ALINEACIÓN Y DISEÑO</div>
      <div class="card-item">
        <strong>1. Diagnóstico de Negocio</strong>
        Levantamiento de problemáticas de mermas, inventarios analógicos y huella de desechables.
      </div>
      <div class="arrow">↓</div>
      <div class="card-item">
        <strong>2. Marco de Arquitectura</strong>
        Definición de Matriz de Zachman (6x4), especificación OpenAPI y diseño relacional Prisma.
      </div>
      <div class="arrow">↓</div>
      <div class="card-item">
        <strong>3. Estrategia ODS ONU 2030</strong>
        Integración nativa de metas ODS 12, 8, 9 y 16 en la lógica transaccional del sistema.
      </div>
    </div>
    
    <div class="col-col col-2 col">
      <div class="col-title">FASE 2: CONSTRUCCIÓN Y DESACOPLE</div>
      <div class="card-item">
        <strong>4. Interfaz Táctil POS (Vue 3)</strong>
        Punto de venta reactivo optimizado para barra rápida con cálculo de bonos ecológicos.
      </div>
      <div class="arrow">↓</div>
      <div class="card-item">
        <strong>5. Bus Asíncrono RabbitMQ</strong>
        Orquestación con Patrón Saga para aislamiento transaccional y prevención de ventas caídas.
      </div>
      <div class="arrow">↓</div>
      <div class="card-item">
        <strong>6. Seguridad Perimetral y RBAC</strong>
        Control de acceso con JWT asimétrico, reCAPTCHA Enterprise v3 y rate limiting.
      </div>
    </div>

    <div class="col-col col-3 col">
      <div class="col-title">FASE 3: DESPLIEGUE Y OPERACIÓN</div>
      <div class="card-item">
        <strong>7. Pipeline CI/CD Automatizado</strong>
        77 pruebas unitarias Vitest y suites E2E en GitHub Actions con contenedores Docker.
      </div>
      <div class="arrow">↓</div>
      <div class="card-item">
        <strong>8. Nube Google Cloud Run</strong>
        Despliegue elástico Serverless con persistencia ACID en PostgreSQL Cloud SQL.
      </div>
      <div class="arrow">↓</div>
      <div class="card-item">
        <strong>9. Sostenibilidad y Monitoreo SRE</strong>
        Tablero gerencial con auditoría SHA-256 y métricas de huella de carbono ahorrada.
      </div>
    </div>
  </div>
</body>
</html>
"""

# =========================================================================
# 2. DIAGRAMA DE GANTT (DIAGRAMA GRÁFICO)
# =========================================================================
html_gantt = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }
  body {
    width: 1200px;
    height: 640px;
    background: #FAF7F2;
    padding: 25px 35px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .header {
    border-bottom: 2px solid #8C6B52;
    padding-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .header h2 { font-size: 22px; color: #1A365D; font-weight: 800; }
  .header span { background: #EFE8DF; color: #8C6B52; font-size: 12px; font-weight: 700; padding: 4px 12px; border-radius: 12px; }
  .gantt-table {
    width: 100%;
    margin-top: 15px;
    border-collapse: collapse;
    background: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(140, 107, 82, 0.08);
  }
  th, td { padding: 8px 10px; font-size: 11px; text-align: left; border-bottom: 1px solid #EFE8DF; }
  th { background: #8C6B52; color: white; font-weight: 800; }
  .month-hdr { background: #7A5B44; text-align: center; }
  .bar-cell { width: 450px; position: relative; background: #FAF9F6; }
  .bar {
    height: 14px;
    border-radius: 4px;
    position: relative;
    font-size: 9px;
    font-weight: 700;
    color: white;
    display: flex;
    align-items: center;
    padding-left: 6px;
  }
  .bar-1 { background: #8C6B52; margin-left: 0; width: 15%; }
  .bar-2 { background: #C49A70; margin-left: 12%; width: 18%; }
  .bar-3 { background: #2B6CB0; margin-left: 28%; width: 22%; }
  .bar-4 { background: #DD6B20; margin-left: 45%; width: 20%; }
  .bar-5 { background: #2F855A; margin-left: 60%; width: 22%; }
  .bar-6 { background: #319795; margin-left: 75%; width: 18%; }
  .bar-7 { background: #1A365D; margin-left: 85%; width: 15%; }
</style>
</head>
<body>
  <div class="header">
    <h2>MONCHIS CAFÉ — CRONOGRAMA MAESTRO (DIAGRAMA DE GANTT)</h2>
    <span>Duración: 14 Semanas • Ciclo 2026B</span>
  </div>
  <table class="gantt-table">
    <thead>
      <tr>
        <th rowspan="2" style="width: 25px;">#</th>
        <th rowspan="2" style="width: 220px;">Fase / Actividad</th>
        <th rowspan="2" style="width: 110px;">Responsable</th>
        <th rowspan="2" style="width: 70px;">Duración</th>
        <th colspan="3" class="month-hdr">Ago - Sep</th>
        <th colspan="4" class="month-hdr">Octubre</th>
        <th colspan="3" class="month-hdr">Noviembre</th>
      </tr>
      <tr style="background: #EFE8DF; color: #5D493B; font-size: 10px; font-weight: 800; text-align: center;">
        <th>S1-S2</th><th>S3-S4</th><th>S5</th><th>S6-S7</th><th>S8</th><th>S9</th><th>S10</th><th>S11</th><th>S12</th><th>S13-14</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>1</td><td><strong>Requerimientos & ODS</strong></td><td>Ernesto Fierro</td><td>2 sem</td>
        <td colspan="10" class="bar-cell"><div class="bar bar-1">Plan ODS & Casos</div></td>
      </tr>
      <tr>
        <td>2</td><td><strong>Matriz Zachman & Arquitectura</strong></td><td>Ernesto Fierro</td><td>3 sem</td>
        <td colspan="10" class="bar-cell"><div class="bar bar-2">Zachman 6x4</div></td>
      </tr>
      <tr>
        <td>3</td><td><strong>Base de Datos & Auth JWT</strong></td><td>Equipo 2</td><td>3 sem</td>
        <td colspan="10" class="bar-cell"><div class="bar bar-3">Prisma / PostgreSQL</div></td>
      </tr>
      <tr>
        <td>4</td><td><strong>Bus RabbitMQ (Patrón Saga)</strong></td><td>Equipo 2</td><td>3 sem</td>
        <td colspan="10" class="bar-cell"><div class="bar bar-4">RabbitMQ Saga</div></td>
      </tr>
      <tr>
        <td>5</td><td><strong>Punto de Venta POS (Vue 3)</strong></td><td>Equipo 2</td><td>3 sem</td>
        <td colspan="10" class="bar-cell"><div class="bar bar-5">POS & Monchis Rewards</div></td>
      </tr>
      <tr>
        <td>6</td><td><strong>Pruebas de Humo & E2E</strong></td><td>Ernesto Fierro</td><td>2 sem</td>
        <td colspan="10" class="bar-cell"><div class="bar bar-6">Smoke Tests (5)</div></td>
      </tr>
      <tr>
        <td>7</td><td><strong>Despliegue GCP & ExpoDIT</strong></td><td>Equipo 2</td><td>2 sem</td>
        <td colspan="10" class="bar-cell"><div class="bar bar-7">Cloud Run & Pitch</div></td>
      </tr>
    </tbody>
  </table>
</body>
</html>
"""

# =========================================================================
# 3. DIAGRAMA DE PERT / RUTA CRÍTICA (DIAGRAMA GRÁFICO)
# =========================================================================
html_pert = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }
  body {
    width: 1200px;
    height: 640px;
    background: #FAF7F2;
    padding: 25px 35px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .header {
    border-bottom: 2px solid #8C6B52;
    padding-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .header h2 { font-size: 22px; color: #1A365D; font-weight: 800; }
  .header span { background: #EFE8DF; color: #8C6B52; font-size: 12px; font-weight: 700; padding: 4px 12px; border-radius: 12px; }
  .pert-container {
    height: 520px;
    background: white;
    border-radius: 12px;
    border: 1.5px solid #E2D9CF;
    position: relative;
    margin-top: 15px;
    box-shadow: 0 4px 12px rgba(140, 107, 82, 0.08);
  }
  .node {
    width: 100px;
    height: 65px;
    border-radius: 8px;
    border: 2px solid #8C6B52;
    background: #FAF5EF;
    position: absolute;
    display: flex;
    flex-direction: column;
    text-align: center;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }
  .node.critical { border-color: #C53030; background: #FFF5F5; }
  .node-hdr { background: #8C6B52; color: white; font-size: 10px; font-weight: 800; padding: 2px; }
  .node.critical .node-hdr { background: #C53030; }
  .node-body { display: flex; flex: 1; font-size: 10px; font-weight: 700; color: #2D3748; }
  .node-col { flex: 1; display: flex; align-items: center; justify-content: center; border-right: 1px solid #E2D9CF; }
  .node-col:last-child { border-right: none; }
  .path-line {
    position: absolute;
    height: 3px;
    background: #CBD5E0;
    transform-origin: 0 0;
  }
  .path-line.critical { background: #C53030; height: 4px; }
  .legend {
    position: absolute;
    bottom: 15px;
    right: 20px;
    background: #FAF7F2;
    border: 1px solid #E2D9CF;
    padding: 8px 14px;
    border-radius: 8px;
    display: flex;
    gap: 15px;
    font-size: 11px;
    font-weight: 700;
  }
</style>
</head>
<body>
  <div class="header">
    <h2>MONCHIS CAFÉ — DIAGRAMA DE PERT Y RUTA CRÍTICA</h2>
    <span>Holgura Cero en Ruta Crítica: A → B → C → D → E → G (14 Semanas)</span>
  </div>
  <div class="pert-container">
    <!-- SVG Lines for connectors -->
    <svg style="position: absolute; top:0; left:0; width:100%; height:100%; pointer-events: none;">
      <!-- Critical line A to B -->
      <line x1="130" y1="260" x2="230" y2="260" stroke="#C53030" stroke-width="4" />
      <polygon points="230,260 220,255 220,265" fill="#C53030" />
      <!-- Critical line B to C -->
      <line x1="330" y1="260" x2="430" y2="260" stroke="#C53030" stroke-width="4" />
      <polygon points="430,260 420,255 420,265" fill="#C53030" />
      <!-- Non-critical line B to F (Docs) -->
      <line x1="330" y1="240" x2="450" y2="120" stroke="#8C6B52" stroke-width="2" stroke-dasharray="4" />
      <!-- Critical line C to D -->
      <line x1="530" y1="260" x2="630" y2="260" stroke="#C53030" stroke-width="4" />
      <polygon points="630,260 620,255 620,265" fill="#C53030" />
      <!-- Line D to E -->
      <line x1="730" y1="260" x2="830" y2="260" stroke="#C53030" stroke-width="4" />
      <polygon points="830,260 820,255 820,265" fill="#C53030" />
      <!-- Line F to E -->
      <line x1="550" y1="120" x2="830" y2="240" stroke="#8C6B52" stroke-width="2" stroke-dasharray="4" />
      <!-- Line E to G -->
      <line x1="930" y1="260" x2="1030" y2="260" stroke="#C53030" stroke-width="4" />
      <polygon points="1030,260 1020,255 1020,265" fill="#C53030" />
    </svg>

    <!-- Node Start / A -->
    <div class="node critical" style="top: 225px; left: 30px;">
      <div class="node-hdr">Act A: Req ODS</div>
      <div class="node-body">
        <div class="node-col">ES: 0</div>
        <div class="node-col">D: 2</div>
        <div class="node-col">EF: 2</div>
      </div>
    </div>

    <!-- Node B: Zachman -->
    <div class="node critical" style="top: 225px; left: 230px;">
      <div class="node-hdr">Act B: Zachman</div>
      <div class="node-body">
        <div class="node-col">ES: 2</div>
        <div class="node-col">D: 3</div>
        <div class="node-col">EF: 5</div>
      </div>
    </div>

    <!-- Node F: Documentacion (Parallel) -->
    <div class="node" style="top: 90px; left: 450px;">
      <div class="node-hdr">Act F: Manuales</div>
      <div class="node-body">
        <div class="node-col">ES: 5</div>
        <div class="node-col">D: 3</div>
        <div class="node-col">EF: 8</div>
      </div>
    </div>

    <!-- Node C: DB & Saga -->
    <div class="node critical" style="top: 225px; left: 430px;">
      <div class="node-hdr">Act C: RabbitMQ</div>
      <div class="node-body">
        <div class="node-col">ES: 5</div>
        <div class="node-col">D: 3</div>
        <div class="node-col">EF: 8</div>
      </div>
    </div>

    <!-- Node D: POS Vue 3 -->
    <div class="node critical" style="top: 225px; left: 630px;">
      <div class="node-hdr">Act D: POS UI</div>
      <div class="node-body">
        <div class="node-col">ES: 8</div>
        <div class="node-col">D: 3</div>
        <div class="node-col">EF: 11</div>
      </div>
    </div>

    <!-- Node E: QA Tests -->
    <div class="node critical" style="top: 225px; left: 830px;">
      <div class="node-hdr">Act E: Pruebas</div>
      <div class="node-body">
        <div class="node-col">ES: 11</div>
        <div class="node-col">D: 2</div>
        <div class="node-col">EF: 13</div>
      </div>
    </div>

    <!-- Node G: Cloud Run Deploy -->
    <div class="node critical" style="top: 225px; left: 1030px;">
      <div class="node-hdr">Act G: Cloud Run</div>
      <div class="node-body">
        <div class="node-col">ES: 13</div>
        <div class="node-col">D: 1</div>
        <div class="node-col">EF: 14</div>
      </div>
    </div>

    <div class="legend">
      <span style="color: #C53030;">■ Ruta Crítica (Holgura = 0)</span>
      <span style="color: #8C6B52;">- - Ruta Secundaria (Holgura = 3 sem)</span>
    </div>
  </div>
</body>
</html>
"""

# =========================================================================
# 4. BURNDOWN CHART & SPRINT BACKLOG (DIAGRAMA GRÁFICO)
# =========================================================================
html_burndown = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }
  body {
    width: 1200px;
    height: 640px;
    background: #FAF7F2;
    padding: 25px 35px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .header {
    border-bottom: 2px solid #8C6B52;
    padding-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .header h2 { font-size: 22px; color: #1A365D; font-weight: 800; }
  .header span { background: #EFE8DF; color: #8C6B52; font-size: 12px; font-weight: 700; padding: 4px 12px; border-radius: 12px; }
  .chart-box {
    height: 520px;
    background: white;
    border-radius: 12px;
    border: 1.5px solid #E2D9CF;
    padding: 25px 35px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 4px 12px rgba(140, 107, 82, 0.08);
  }
  .chart-title { font-size: 14px; font-weight: 800; color: #1A365D; margin-bottom: 10px; }
  svg { width: 100%; height: 420px; }
</style>
</head>
<body>
  <div class="header">
    <h2>MONCHIS CAFÉ — BURNDOWN CHART (SPRINT BACKLOG)</h2>
    <span>Sprint 4: Velocidad Real vs Ideal (40 Story Points)</span>
  </div>
  <div class="chart-box">
    <div class="chart-title">Seguimiento de Puntos de Historia Completados a lo largo de 10 días de Sprint</div>
    <svg viewBox="0 0 1000 400">
      <!-- Grid lines -->
      <line x1="80" y1="50" x2="950" y2="50" stroke="#EDF2F7" stroke-width="1.5" />
      <text x="40" y="55" font-size="12" fill="#718096" font-family="Segoe UI">40 SP</text>
      
      <line x1="80" y1="125" x2="950" y2="125" stroke="#EDF2F7" stroke-width="1.5" />
      <text x="40" y="130" font-size="12" fill="#718096" font-family="Segoe UI">30 SP</text>
      
      <line x1="80" y1="200" x2="950" y2="200" stroke="#EDF2F7" stroke-width="1.5" />
      <text x="40" y="205" font-size="12" fill="#718096" font-family="Segoe UI">20 SP</text>
      
      <line x1="80" y1="275" x2="950" y2="275" stroke="#EDF2F7" stroke-width="1.5" />
      <text x="40" y="280" font-size="12" fill="#718096" font-family="Segoe UI">10 SP</text>

      <line x1="80" y1="350" x2="950" y2="350" stroke="#CBD5E0" stroke-width="2" />
      <text x="45" y="355" font-size="12" fill="#718096" font-family="Segoe UI">0 SP</text>

      <!-- Day labels -->
      <text x="80" y="375" font-size="12" fill="#4A5568" font-weight="700">Día 1</text>
      <text x="175" y="375" font-size="12" fill="#4A5568" font-weight="700">Día 2</text>
      <text x="270" y="375" font-size="12" fill="#4A5568" font-weight="700">Día 3</text>
      <text x="365" y="375" font-size="12" fill="#4A5568" font-weight="700">Día 4</text>
      <text x="460" y="375" font-size="12" fill="#4A5568" font-weight="700">Día 5</text>
      <text x="555" y="375" font-size="12" fill="#4A5568" font-weight="700">Día 6</text>
      <text x="650" y="375" font-size="12" fill="#4A5568" font-weight="700">Día 7</text>
      <text x="745" y="375" font-size="12" fill="#4A5568" font-weight="700">Día 8</text>
      <text x="840" y="375" font-size="12" fill="#4A5568" font-weight="700">Día 9</text>
      <text x="930" y="375" font-size="12" fill="#4A5568" font-weight="700">Día 10</text>

      <!-- Ideal Line (Grey Dashed) -->
      <line x1="80" y1="50" x2="930" y2="350" stroke="#A0AEC0" stroke-width="2.5" stroke-dasharray="6" />

      <!-- Actual Line (Green Monchis) -->
      <polyline points="
        80,50 
        175,70 
        270,110 
        365,145 
        460,205 
        555,220 
        650,250 
        745,290 
        840,320 
        930,350" 
        fill="none" stroke="#2F855A" stroke-width="4" />

      <!-- Points on actual line -->
      <circle cx="80" cy="50" r="5" fill="#2F855A" />
      <circle cx="175" cy="70" r="5" fill="#2F855A" />
      <circle cx="270" cy="110" r="5" fill="#2F855A" />
      <circle cx="365" cy="145" r="5" fill="#2F855A" />
      <circle cx="460" cy="205" r="5" fill="#2F855A" />
      <circle cx="555" cy="220" r="5" fill="#2F855A" />
      <circle cx="650" cy="250" r="5" fill="#2F855A" />
      <circle cx="745" cy="290" r="5" fill="#2F855A" />
      <circle cx="840" cy="320" r="5" fill="#2F855A" />
      <circle cx="930" cy="350" r="6" fill="#1A365D" />

      <!-- Legend -->
      <rect x="700" y="60" width="220" height="60" rx="8" fill="#FAF5EF" stroke="#E2D9CF" />
      <line x1="720" y1="80" x2="750" y2="80" stroke="#A0AEC0" stroke-width="2.5" stroke-dasharray="4" />
      <text x="760" y="84" font-size="11" fill="#4A5568" font-weight="700">Línea Ideal</text>
      
      <line x1="720" y1="102" x2="750" y2="102" stroke="#2F855A" stroke-width="3" />
      <text x="760" y="106" font-size="11" fill="#2F855A" font-weight="700">Trabajo Real (40 SP)</text>
    </svg>
  </div>
</body>
</html>
"""

# =========================================================================
# 5. MAPA DE RIESGOS (MATRIZ GRÁFICA)
# =========================================================================
html_riesgos = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }
  body {
    width: 1200px;
    height: 640px;
    background: #FAF7F2;
    padding: 25px 35px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .header {
    border-bottom: 2px solid #8C6B52;
    padding-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .header h2 { font-size: 22px; color: #1A365D; font-weight: 800; }
  .header span { background: #EFE8DF; color: #8C6B52; font-size: 12px; font-weight: 700; padding: 4px 12px; border-radius: 12px; }
  .risk-table {
    width: 100%;
    margin-top: 15px;
    border-collapse: collapse;
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(140, 107, 82, 0.08);
  }
  th, td { border: 1.5px solid #CBD5E0; padding: 12px 14px; text-align: center; }
  th { background: #8C6B52; color: white; font-weight: 800; font-size: 13px; }
  .th-side { background: #7A5B44; width: 140px; font-weight: 800; }
  .cell-low { background: #DEF7EC; color: #03543F; font-size: 11px; font-weight: 700; }
  .cell-med { background: #FEF08A; color: #713F12; font-size: 11px; font-weight: 700; }
  .cell-high { background: #FDE8E8; color: #9B1C1C; font-size: 11px; font-weight: 700; }
  .desc-box { font-size: 10.5px; line-height: 1.3; margin-top: 4px; font-weight: normal; }
</style>
</head>
<body>
  <div class="header">
    <h2>MONCHIS CAFÉ — MATRIZ Y MAPA DE ADMINISTRACIÓN DE RIESGOS</h2>
    <span>Evaluación de Probabilidad vs Impacto Inherente</span>
  </div>
  <table class="risk-table">
    <thead>
      <tr>
        <th class="th-side">IMPACTO / PROB.</th>
        <th>RARO (1)</th>
        <th>POSIBLE (2)</th>
        <th>PROBABLE (3)</th>
        <th>INEVITABLE (4)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="th-side" style="color: white;">ALTO (3)</td>
        <td class="cell-med">
          <strong>R3: Descuadre Contable</strong>
          <div class="desc-box">Mitigado por auditoría SHA-256</div>
        </td>
        <td class="cell-high">
          <strong>R1: Caída de Red en Barra</strong>
          <div class="desc-box">Mitigado con RabbitMQ Saga</div>
        </td>
        <td class="cell-high">
          <strong>R5: Fuga de Granos Especiales</strong>
          <div class="desc-box">Mitigado con recetario digital</div>
        </td>
        <td class="cell-high" style="background: #F87171; color: white;">
          <strong>Zona Crítica Inaceptable</strong>
        </td>
      </tr>
      <tr>
        <td class="th-side" style="color: white;">MEDIO (2)</td>
        <td class="cell-low">
          <strong>R4: Bloqueo de reCAPTCHA</strong>
          <div class="desc-box">Resuelto con bypass local de prueba</div>
        </td>
        <td class="cell-med">
          <strong>R2: Picos de Concurrencia</strong>
          <div class="desc-box">Mitigado por Cloud Run autoescalable</div>
        </td>
        <td class="cell-med">
          <strong>R6: Desabasto de Vasos Reusables</strong>
          <div class="desc-box">Mitigado con alerta de reorden</div>
        </td>
        <td class="cell-high">
          <strong>Sobrecarga Operativa</strong>
        </td>
      </tr>
      <tr>
        <td class="th-side" style="color: white;">BAJO (1)</td>
        <td class="cell-low">
          <strong>R7: Errores Visuales CSS</strong>
          <div class="desc-box">Mitigado con Tailwind components</div>
        </td>
        <td class="cell-low">
          <strong>R8: Retardo en Lectura QR</strong>
          <div class="desc-box">Mitigado con escáner ZXing nativo</div>
        </td>
        <td class="cell-low">
          <strong>R9: Dudas de Barista</strong>
          <div class="desc-box">Mitigado con Manual de Usuario</div>
        </td>
        <td class="cell-med">
          <strong>Desgaste de Equipos</strong>
        </td>
      </tr>
    </tbody>
  </table>
</body>
</html>
"""

render_html_to_png(html_plan_est, os.path.join(OUT_DIR, "plan_estrategico_monchis.png"))
render_html_to_png(html_gantt, os.path.join(OUT_DIR, "diagrama_gantt_monchis.png"))
render_html_to_png(html_pert, os.path.join(OUT_DIR, "diagrama_pert_monchis.png"))
render_html_to_png(html_burndown, os.path.join(OUT_DIR, "burndown_chart_monchis.png"))
render_html_to_png(html_riesgos, os.path.join(OUT_DIR, "mapa_riesgos_monchis.png"))

print("All document diagrams generated successfully!")
