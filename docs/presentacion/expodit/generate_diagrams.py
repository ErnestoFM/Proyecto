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
# 1. DIAGRAMA DE ARQUITECTURA DE SOFTWARE (GRAPHIC DIAGRAM)
# =========================================================================
html_arch = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }
  body {
    width: 1200px;
    height: 640px;
    background: #FAF7F2;
    padding: 30px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .title-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #8C6B52;
    padding-bottom: 12px;
  }
  .title-bar h2 {
    font-size: 24px;
    color: #1A365D;
    font-weight: 800;
  }
  .title-bar span {
    font-size: 13px;
    color: #8C6B52;
    font-weight: 700;
    background: #EFE8DF;
    padding: 6px 14px;
    border-radius: 20px;
  }
  .diagram-container {
    display: flex;
    justify-content: space-between;
    align-items: stretch;
    gap: 15px;
    height: 520px;
    margin-top: 20px;
  }
  .layer-col {
    flex: 1;
    background: #FFFFFF;
    border-radius: 14px;
    border: 1.5px solid #E2D9CF;
    box-shadow: 0 4px 15px rgba(140, 107, 82, 0.08);
    display: flex;
    flex-direction: column;
    padding: 16px;
    position: relative;
  }
  .col-hdr {
    text-align: center;
    padding: 8px 10px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 14px;
    letter-spacing: 0.5px;
  }
  .col-1 .col-hdr { background: #8C6B52; }
  .col-2 .col-hdr { background: #2B6CB0; }
  .col-3 .col-hdr { background: #DD6B20; }
  .col-4 .col-hdr { background: #2F855A; }
  .col-5 .col-hdr { background: #1A365D; }

  .card-node {
    background: #FDFBF7;
    border: 1px solid #EADBCC;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.03);
  }
  .card-node h4 {
    font-size: 13px;
    font-weight: 800;
    color: #1A365D;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .card-node p {
    font-size: 11px;
    color: #4A5568;
    line-height: 1.35;
  }
  .card-badge {
    display: inline-block;
    font-size: 9.5px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    margin-top: 6px;
    background: #EBF8FF;
    color: #2B6CB0;
  }
  .arrow-indicator {
    position: absolute;
    right: -14px;
    top: 50%;
    transform: translateY(-50%);
    width: 24px;
    height: 24px;
    background: #8C6B52;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
    z-index: 10;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  }
  .footer-legend {
    background: #FAF7F2;
    border: 1px dashed #8C6B52;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 11px;
    color: #718096;
    display: flex;
    justify-content: space-between;
    margin-top: auto;
  }
</style>
</head>
<body>
  <div class="title-bar">
    <h2>Arquitectura de Software y Resiliencia Transaccional</h2>
    <span>Monorepo Modular • Monchis Café</span>
  </div>

  <div class="diagram-container">
    <!-- COL 1 -->
    <div class="layer-col col-1">
      <div class="col-hdr">1. CAPA CLIENTE / UI</div>
      <div class="card-node">
        <h4>📱 Punto de Venta (POS)</h4>
        <p>Interfaz web táctil para mostrador con selección rápida, bono por termo (-$5) y teclado numérico.</p>
        <span class="card-badge" style="background:#FEFCBF; color:#744210;">Vue 3 + Tailwind</span>
      </div>
      <div class="card-node">
        <h4>👤 Portal Clientes & Rewards</h4>
        <p>Historial de compras, sellos ecológicos digitales y tarjeta QR para canje en barra.</p>
        <span class="card-badge" style="background:#C6F6D5; color:#22543D;">Pinia + Vite SSG</span>
      </div>
      <div class="card-node">
        <h4>📊 Panel Administrativo</h4>
        <p>Control de mermas PEPS, gestión de lotes campesinos y analítica con métricas UTM.</p>
        <span class="card-badge">Diseño Cálido Pastel</span>
      </div>
      <div class="arrow-indicator">➔</div>
    </div>

    <!-- COL 2 -->
    <div class="layer-col col-2">
      <div class="col-hdr">2. API GATEWAY & AUTH</div>
      <div class="card-node">
        <h4>🔒 Seguridad Stateless</h4>
        <p>Tokens JWT en cookies seguras (HttpOnly, SameSite) con expiración corta y rotación.</p>
        <span class="card-badge">JWT + bcrypt</span>
      </div>
      <div class="card-node">
        <h4>🛡️ Control de Acceso RBAC</h4>
        <p>Principio de menor privilegio para 4 roles: Admin, Cajero, Cliente y Productor Campesino.</p>
        <span class="card-badge" style="background:#E9D8FD; color:#553C9A;">RBAC Granular</span>
      </div>
      <div class="card-node">
        <h4>🤖 Anti-Bot & 2FA TOTP</h4>
        <p>Protección perimetral con Google reCAPTCHA v3 y doble factor de autenticación TOTP.</p>
        <span class="card-badge" style="background:#FED7D7; color:#9B2C2C;">reCAPTCHA v3</span>
      </div>
      <div class="arrow-indicator">➔</div>
    </div>

    <!-- COL 3 -->
    <div class="layer-col col-3">
      <div class="col-hdr">3. PATRÓN SAGA / EVENTOS</div>
      <div class="card-node">
        <h4>🔄 Orquestador Saga</h4>
        <p>Garantiza consistencia eventual coordinando cobro mixto, reserva de stock y emisión de tickets.</p>
        <span class="card-badge" style="background:#FEEBC8; color:#7B341E;">RabbitMQ Broker</span>
      </div>
      <div class="card-node">
        <h4>⚡ Compensaciones Automáticas</h4>
        <p>Si la pasarela o banco falla, el bus emite 'RevertStockEvent' y libera el lote de café.</p>
        <span class="card-badge" style="background:#FED7D7; color:#742A2A;">Zero Data Loss</span>
      </div>
      <div class="card-node">
        <h4>📬 Dead Letter Queue (DLQ)</h4>
        <p>Reintentos exponenciales y auditoría de eventos no procesados para supervisión.</p>
        <span class="card-badge">Resiliencia ODS 16</span>
      </div>
      <div class="arrow-indicator">➔</div>
    </div>

    <!-- COL 4 -->
    <div class="layer-col col-4">
      <div class="col-hdr">4. DATOS & ORM</div>
      <div class="card-node">
        <h4>🗄️ PostgreSQL Cloud SQL</h4>
        <p>Base de datos relacional con integridad referencial, índices de alta concurrencia y ACID.</p>
        <span class="card-badge" style="background:#C6F6D5; color:#22543D;">PostgreSQL 16</span>
      </div>
      <div class="card-node">
        <h4>☕ Modelo de Trazabilidad</h4>
        <p>Tablas normalizadas: Lotes (origen campesino, altitud, tueste), Órdenes, Pagos y Sellos.</p>
        <span class="card-badge" style="background:#FEFCBF; color:#744210;">Prisma ORM</span>
      </div>
      <div class="card-node">
        <h4>🌱 Política PEPS</h4>
        <p>Control estricto de caducidades: Primeras Entradas, Primeras Salidas para evitar mermas.</p>
        <span class="card-badge">ODS 12 Eficiencia</span>
      </div>
      <div class="arrow-indicator">➔</div>
    </div>

    <!-- COL 5 -->
    <div class="layer-col col-5">
      <div class="col-hdr">5. INFRAESTRUCTURA CLOUD</div>
      <div class="card-node">
        <h4>☁️ Google Cloud Run</h4>
        <p>Contenedores Docker serverless auto-escalables (0 a N instancias) con balanceo y HTTPS.</p>
        <span class="card-badge" style="background:#EBF8FF; color:#2B6CB0;">GCP Cloud Run</span>
      </div>
      <div class="card-node">
        <h4>🚀 Pipeline CI/CD</h4>
        <p>Compilación automática en Cloud Build, validación con 77 pruebas Vitest y despliegue continuo.</p>
        <span class="card-badge" style="background:#E9D8FD; color:#553C9A;">Cloud Build</span>
      </div>
      <div class="card-node">
        <h4>⏱️ Rendimiento ISO 25010</h4>
        <p>Tiempos de respuesta de API inferiores a 200 ms y 99.9% de disponibilidad garantizada.</p>
        <span class="card-badge" style="background:#C6F6D5; color:#22543D;">Latencia &lt; 200ms</span>
      </div>
    </div>
  </div>
</body>
</html>
"""

# =========================================================================
# 2. DIAGRAMA DE ALINEACIÓN ODS (GRAPHIC DIAGRAM)
# =========================================================================
html_ods = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }
  body {
    width: 1200px;
    height: 640px;
    background: #FAF7F2;
    padding: 30px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .title-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #8C6B52;
    padding-bottom: 12px;
  }
  .title-bar h2 {
    font-size: 24px;
    color: #1A365D;
    font-weight: 800;
  }
  .title-bar span {
    font-size: 13px;
    color: #8C6B52;
    font-weight: 700;
    background: #EFE8DF;
    padding: 6px 14px;
    border-radius: 20px;
  }
  .ods-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    height: 520px;
    margin-top: 20px;
  }
  .ods-card {
    background: #FFFFFF;
    border-radius: 14px;
    border: 1.5px solid #E2D9CF;
    box-shadow: 0 4px 15px rgba(140, 107, 82, 0.08);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .ods-hdr {
    padding: 16px;
    color: white;
    font-weight: 800;
    text-align: center;
  }
  .ods-hdr .num { font-size: 32px; display: block; font-weight: 900; line-height: 1; margin-bottom: 4px; }
  .ods-hdr .title { font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }

  .c-ods12 { background: #CF8D2A; }
  .c-ods8  { background: #A21942; }
  .c-ods9  { background: #F36E25; }
  .c-ods16 { background: #00689D; }

  .ods-body {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    flex: 1;
    justify-content: space-between;
  }
  .ods-body h4 {
    font-size: 13px;
    font-weight: 800;
    color: #1A365D;
  }
  .ods-body ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .ods-body li {
    font-size: 11px;
    color: #4A5568;
    line-height: 1.4;
    margin-bottom: 8px;
    padding-left: 14px;
    position: relative;
  }
  .ods-body li::before {
    content: "✓";
    position: absolute;
    left: 0;
    color: #8C6B52;
    font-weight: bold;
  }
  .metric-badge {
    background: #FDFBF7;
    border: 1.5px solid #EADBCC;
    border-radius: 8px;
    padding: 10px;
    text-align: center;
  }
  .metric-badge .m-val {
    font-size: 18px;
    font-weight: 900;
    color: #8C6B52;
    display: block;
  }
  .metric-badge .m-lbl {
    font-size: 10px;
    color: #718096;
    font-weight: 600;
  }
</style>
</head>
<body>
  <div class="title-bar">
    <h2>Alineación Estratégica con los Objetivos de Desarrollo Sostenible</h2>
    <span>Agenda 2030 ONU • Monchis Café</span>
  </div>

  <div class="ods-grid">
    <!-- ODS 12 -->
    <div class="ods-card">
      <div class="ods-hdr c-ods12">
        <span class="num">ODS 12</span>
        <span class="title">Producción y Consumo Responsables</span>
      </div>
      <div class="ods-body">
        <div>
          <h4>Eje Sustentable Principal</h4>
          <ul>
            <li><strong>Bono Ecológico:</strong> Descuento automático (-$5 MXN) y sello digital por traer termo reusable.</li>
            <li><strong>Mermas Cero:</strong> Política PEPS en inventarios para erradicar desperdicios de café de altura.</li>
            <li><strong>Trazabilidad de Finca:</strong> Registro de origen y proceso de cultivo 100% orgánico sin pesticidas.</li>
          </ul>
        </div>
        <div class="metric-badge">
          <span class="m-val">> 4,500</span>
          <span class="m-lbl">Vasos plásticos desechables evitados semestralmente</span>
        </div>
      </div>
    </div>

    <!-- ODS 8 -->
    <div class="ods-card">
      <div class="ods-hdr c-ods8">
        <span class="num">ODS 8</span>
        <span class="title">Trabajo Decente y Crecimiento</span>
      </div>
      <div class="ods-body">
        <div>
          <h4>Microeconomía y Comercio Justo</h4>
          <ul>
            <li><strong>Comercio Directo:</strong> Enlace con cooperativas caficultoras regionales sin intermediarios usureros.</li>
            <li><strong>Ergonomía Operativa:</strong> POS táctil optimizado que agiliza el turno del barista (&lt; 15s por orden).</li>
            <li><strong>Cierre de Caja Transparente:</strong> Cuadratura automatizada de turnos que previene descuadres.</li>
          </ul>
        </div>
        <div class="metric-badge">
          <span class="m-val">+35%</span>
          <span class="m-lbl">Margen retenido en cooperativas campesinas locales</span>
        </div>
      </div>
    </div>

    <!-- ODS 9 -->
    <div class="ods-card">
      <div class="ods-hdr c-ods9">
        <span class="num">ODS 9</span>
        <span class="title">Industria, Innovación e Infraestructura</span>
      </div>
      <div class="ods-body">
        <div>
          <h4>Digitalización en Zonas Periurbanas</h4>
          <ul>
            <li><strong>Infraestructura Cloud:</strong> Despliegue en Google Cloud Run accesible desde tablets estándar comerciales.</li>
            <li><strong>Alta Concurrencia:</strong> Contenedores auto-escalables con respuesta menor a 200 ms.</li>
            <li><strong>Modernización PYME:</strong> Sistema web que democratiza herramientas empresariales para negocios familiares.</li>
          </ul>
        </div>
        <div class="metric-badge">
          <span class="m-val">&lt; 200 ms</span>
          <span class="m-lbl">Latencia de respuesta en barra y 99.9% disponibilidad</span>
        </div>
      </div>
    </div>

    <!-- ODS 16 -->
    <div class="ods-card">
      <div class="ods-hdr c-ods16">
        <span class="num">ODS 16</span>
        <span class="title">Paz, Justicia e Instituciones Sólidas</span>
      </div>
      <div class="ods-body">
        <div>
          <h4>Integridad de Datos y Zero Trust</h4>
          <ul>
            <li><strong>Transacciones Resilientes:</strong> Patrón Saga en RabbitMQ que elimina discrepancias contables.</li>
            <li><strong>Privacidad de Datos:</strong> Cifrado bcrypt, sesiones JWT protegidas y reCAPTCHA v3 anti-fraude.</li>
            <li><strong>Auditoría Permanente:</strong> Trazabilidad criptográfica de cada movimiento y reversa en el sistema.</li>
          </ul>
        </div>
        <div class="metric-badge">
          <span class="m-val">100%</span>
          <span class="m-lbl">Consistencia eventual transaccional garantizada</span>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

render_html_to_png(html_arch, os.path.join(OUT_DIR, "diagrama_arquitectura_monchis.png"))
render_html_to_png(html_ods, os.path.join(OUT_DIR, "diagrama_ods_monchis.png"))
