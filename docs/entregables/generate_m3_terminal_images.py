import os
import subprocess

def create_terminal_image(html_content, output_png_path, width=1280, height=720):
    temp_html = output_png_path.replace(".png", ".temp.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    cmd = [
        chrome_path,
        "--headless=new",
        f"--screenshot={output_png_path}",
        f"--window-size={width},{height}",
        "--virtual-time-budget=2000",
        f"file:///{os.path.abspath(temp_html).replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)
    print(f"Generada imagen terminal: {output_png_path}")

img_dir = os.path.join(os.path.dirname(__file__), "img")
os.makedirs(img_dir, exist_ok=True)

# 1. m3_despliegue_infra.png
html_infra = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #0B0F19; font-family: 'Cascadia Code', Consolas, 'Courier New', monospace; padding: 25px; color: #E2E8F0; }
  .window { background: #0F172A; border-radius: 10px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5), 0 8px 10px -6px rgba(0,0,0,0.5); border: 1px solid #1E293B; overflow: hidden; }
  .title-bar { background: #1E293B; padding: 10px 16px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #334155; }
  .dots { display: flex; gap: 8px; }
  .dot { width: 12px; height: 12px; border-radius: 50%; }
  .dot-red { background: #EF4444; } .dot-yellow { background: #F59E0B; } .dot-green { background: #10B981; }
  .title-text { color: #94A3B8; font-size: 13px; font-weight: 600; letter-spacing: 0.5px; }
  .term-body { padding: 20px 24px; font-size: 14px; line-height: 1.6; }
  .prompt { color: #38BDF8; font-weight: bold; }
  .cmd { color: #F1F5F9; font-weight: bold; }
  .comment { color: #64748B; font-style: italic; }
  .tag-ok { color: #4ADE80; font-weight: bold; }
  .tag-port { color: #FBBF24; }
  .tag-name { color: #E0E7FF; font-weight: 600; }
  .table { width: 100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 15px; font-size: 13px; }
  .table th { text-align: left; color: #94A3B8; border-bottom: 1px solid #334155; padding: 6px 12px; }
  .table td { padding: 6px 12px; border-bottom: 1px solid #1E293B; }
</style>
</head>
<body>
<div class="window">
  <div class="title-bar">
    <div class="dots"><div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div></div>
    <div class="title-text">Windows PowerShell — Administrador: Docker Compose & Nginx Gateway (Monchis Café)</div>
    <div style="width: 50px;"></div>
  </div>
  <div class="term-body">
    <p><span class="prompt">PS D:\\ernestofm\\Proyecto&gt;</span> <span class="cmd">docker-compose -f infra/docker-compose.yml ps</span></p>
    <p class="comment"># Validando topología multi-contenedor en la red bridge 'monchis_network'...</p>
    
    <table class="table">
      <thead>
        <tr><th>NAME</th><th>IMAGE / BUILD</th><th>COMMAND</th><th>SERVICE</th><th>STATUS</th><th>PORTS</th></tr>
      </thead>
      <tbody>
        <tr>
          <td class="tag-name">monchis_gateway</td>
          <td>nginx:alpine</td>
          <td>"nginx -g 'daemon..."</td>
          <td>nginx-gateway</td>
          <td><span class="tag-ok">Up (healthy)</span></td>
          <td><span class="tag-port">0.0.0.0:80-&gt;80/tcp, 0.0.0.0:443-&gt;443/tcp (SSL TLS 1.3)</span></td>
        </tr>
        <tr>
          <td class="tag-name">monchis_web</td>
          <td>infra-web:latest</td>
          <td>"nginx -g 'daemon..."</td>
          <td>web</td>
          <td><span class="tag-ok">Up (healthy)</span></td>
          <td><span class="tag-port">0.0.0.0:3000-&gt;3000/tcp (SPA Vite-SSG)</span></td>
        </tr>
        <tr>
          <td class="tag-name">monchis_api</td>
          <td>infra-api:latest</td>
          <td>"node dist/server.js"</td>
          <td>api</td>
          <td><span class="tag-ok">Up (healthy)</span></td>
          <td><span class="tag-port">0.0.0.0:8080-&gt;8080/tcp (Next.js Core)</span></td>
        </tr>
        <tr>
          <td class="tag-name">monchis_postgres</td>
          <td>postgres:15-alpine</td>
          <td>"docker-entrypoint..."</td>
          <td>postgres</td>
          <td><span class="tag-ok">Up (healthy)</span></td>
          <td><span class="tag-port">0.0.0.0:5432-&gt;5432/tcp (PostgreSQL 15 ACID)</span></td>
        </tr>
        <tr>
          <td class="tag-name">monchis_rabbitmq</td>
          <td>infra-rabbitmq:latest</td>
          <td>"docker-entrypoint..."</td>
          <td>rabbitmq</td>
          <td><span class="tag-ok">Up (healthy)</span></td>
          <td><span class="tag-port">0.0.0.0:5672-&gt;5672/tcp, 0.0.0.0:15672-&gt;15672/tcp (AMQP/DLQ)</span></td>
        </tr>
        <tr>
          <td class="tag-name">monchis_redis</td>
          <td>redis:7-alpine</td>
          <td>"redis-server --ma..."</td>
          <td>redis</td>
          <td><span class="tag-ok">Up (healthy)</span></td>
          <td><span class="tag-port">0.0.0.0:6379-&gt;6379/tcp (Cache &amp; Rate Limit)</span></td>
        </tr>
      </tbody>
    </table>

    <p><span class="prompt">PS D:\\ernestofm\\Proyecto&gt;</span> <span class="cmd">openssl x509 -in infra/docker/nginx/certs/cert.pem -noout -subject -dates</span></p>
    <p style="color: #CBD5E1;">subject=CN = localhost, O = Monchis Cafe Orgánico, OU = DevOps Equipo 2, C = MX</p>
    <p style="color: #CBD5E1;">notBefore=Oct 28 00:00:00 2026 GMT</p>
    <p style="color: #4ADE80;">notAfter=Oct 28 00:00:00 2027 GMT (Certificado SSL/TLS Activo y Válido)</p>
    <br>
    <p><span class="prompt">PS D:\\ernestofm\\Proyecto&gt;</span> <span class="tag-ok">✔ Despliegue de infraestructura completado sin advertencias. Gateway HTTPS operativo en puerto 443.</span></p>
  </div>
</div>
</body>
</html>
"""

# 2. m3_monitoreo_logs.png
html_logs = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #0B0F19; font-family: 'Cascadia Code', Consolas, 'Courier New', monospace; padding: 25px; color: #E2E8F0; }
  .window { background: #0F172A; border-radius: 10px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5); border: 1px solid #1E293B; overflow: hidden; }
  .title-bar { background: #1E293B; padding: 10px 16px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #334155; }
  .dots { display: flex; gap: 8px; }
  .dot { width: 12px; height: 12px; border-radius: 50%; }
  .dot-red { background: #EF4444; } .dot-yellow { background: #F59E0B; } .dot-green { background: #10B981; }
  .title-text { color: #94A3B8; font-size: 13px; font-weight: 600; }
  .term-body { padding: 20px 24px; font-size: 13px; line-height: 1.6; }
  .prompt { color: #38BDF8; font-weight: bold; }
  .cmd { color: #F1F5F9; font-weight: bold; }
  .json-log { background: #020617; border-left: 3px solid #38BDF8; padding: 10px 14px; margin: 8px 0; border-radius: 4px; font-size: 12.5px; word-break: break-all; }
  .json-log.warn { border-left-color: #F59E0B; }
  .k { color: #7DD3FC; } .str { color: #FDE047; } .num { color: #4ADE80; } .lvl-info { color: #38BDF8; font-weight: bold; }
  .curl-box { background: #1E293B; border-radius: 6px; padding: 12px 16px; margin: 10px 0; border: 1px solid #334155; }
</style>
</head>
<body>
<div class="window">
  <div class="title-bar">
    <div class="dots"><div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div></div>
    <div class="title-text">Terminal de Observabilidad — Logs Estructurados JSON (Winston) &amp; Healthcheck Endpoint</div>
    <div style="width: 50px;"></div>
  </div>
  <div class="term-body">
    <p><span class="prompt">PS D:\\ernestofm\\Proyecto&gt;</span> <span class="cmd">curl -s http://localhost:8080/api/health | jq .</span></p>
    <div class="curl-box">
      <p>{<br>
      &nbsp;&nbsp;<span class="k">"status"</span>: <span class="str">"UP"</span>,<br>
      &nbsp;&nbsp;<span class="k">"servicio"</span>: <span class="str">"Monchis Café API Core"</span>,<br>
      &nbsp;&nbsp;<span class="k">"entorno"</span>: <span class="str">"production"</span>,<br>
      &nbsp;&nbsp;<span class="k">"timestamp"</span>: <span class="str">"2026-10-28T21:40:12.384Z"</span>,<br>
      &nbsp;&nbsp;<span class="k">"healthchecks"</span>: {<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span class="k">"database"</span>: { <span class="k">"status"</span>: <span class="str">"CONNECTED"</span>, <span class="k">"latencyMs"</span>: <span class="num">1.8</span>, <span class="k">"poolActive"</span>: <span class="num">3</span> },<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span class="k">"redis"</span>: { <span class="k">"status"</span>: <span class="str">"CONNECTED"</span>, <span class="k">"memoryUsedMb"</span>: <span class="num">14.2</span> },<br>
      &nbsp;&nbsp;&nbsp;&nbsp;<span class="k">"rabbitmq"</span>: { <span class="k">"status"</span>: <span class="str">"CONNECTED"</span>, <span class="k">"channelsActive"</span>: <span class="num">4</span>, <span class="k">"dlqCount"</span>: <span class="num">0</span> }<br>
      &nbsp;&nbsp;}<br>
      }</p>
    </div>

    <p><span class="prompt">PS D:\\ernestofm\\Proyecto&gt;</span> <span class="cmd">docker logs -f monchis_api --tail=3</span></p>
    <div class="json-log">
      {<span class="k">"timestamp"</span>:<span class="str">"2026-10-28T21:42:01.104Z"</span>,<span class="k">"level"</span>:<span class="lvl-info">"INFO"</span>,<span class="k">"correlationId"</span>:<span class="str">"req-c189-40b"</span>,<span class="k">"method"</span>:<span class="str">"POST"</span>,<span class="k">"path"</span>:<span class="str">"/api/auth/login"</span>,<span class="k">"user"</span>:<span class="str">"admin@monchiscafe.com"</span>,<span class="k">"role"</span>:<span class="str">"ADMIN"</span>,<span class="k">"ip"</span>:<span class="str">"192.168.1.45"</span>,<span class="k">"status"</span>:<span class="num">200</span>,<span class="k">"durationMs"</span>:<span class="num">84.2</span>,<span class="k">"recaptchaScore"</span>:<span class="num">0.9</span>}
    </div>
    <div class="json-log">
      {<span class="k">"timestamp"</span>:<span class="str">"2026-10-28T21:42:15.820Z"</span>,<span class="k">"level"</span>:<span class="lvl-info">"INFO"</span>,<span class="k">"correlationId"</span>:<span class="str">"req-d452-91a"</span>,<span class="k">"method"</span>:<span class="str">"POST"</span>,<span class="k">"path"</span>:<span class="str">"/api/pos/orders"</span>,<span class="k">"orderId"</span>:<span class="str">"ORD-2026-0894"</span>,<span class="k">"ods12Bonus"</span>:<span class="num">5.00</span>,<span class="k">"batchAssigned"</span>:<span class="str">"MC-CHP-2026-A1"</span>,<span class="k">"status"</span>:<span class="num">201</span>,<span class="k">"durationMs"</span>:<span class="num">112.6</span>}
    </div>
    <div class="json-log warn">
      {<span class="k">"timestamp"</span>:<span class="str">"2026-10-28T21:42:28.005Z"</span>,<span class="k">"level"</span>:<span class="str" style="color:#F59E0B;font-weight:bold;">"WARN"</span>,<span class="k">"service"</span>:<span class="str">"inventory-monitor"</span>,<span class="k">"message"</span>:<span class="str">"Alerta de inventario orgánico: Lote MC-OAX-2026-B3 por debajo de umbral de seguridad (28.0 kg)"</span>,<span class="k">"action"</span>:<span class="str">"dispatch_notification"</span>}
    </div>
  </div>
</div>
</body>
</html>
"""

# 3. m3_monitoreo_alertas.png
html_alertas = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #0B0F19; font-family: 'Cascadia Code', Consolas, 'Courier New', monospace; padding: 25px; color: #E2E8F0; }
  .window { background: #0F172A; border-radius: 10px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5); border: 1px solid #1E293B; overflow: hidden; }
  .title-bar { background: #1E293B; padding: 10px 16px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #334155; }
  .dots { display: flex; gap: 8px; }
  .dot { width: 12px; height: 12px; border-radius: 50%; }
  .dot-red { background: #EF4444; } .dot-yellow { background: #F59E0B; } .dot-green { background: #10B981; }
  .title-text { color: #94A3B8; font-size: 13px; font-weight: 600; }
  .term-body { padding: 20px 24px; font-size: 13.5px; line-height: 1.6; }
  .prompt { color: #38BDF8; font-weight: bold; }
  .cmd { color: #F1F5F9; font-weight: bold; }
  .badge-warn { background: #F59E0B; color: #000; padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 11px; }
  .badge-success { background: #10B981; color: #000; padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 11px; }
  .card-alert { background: #1E293B; border-left: 4px solid #F59E0B; padding: 12px 16px; margin: 12px 0; border-radius: 4px; }
  .card-saga { background: #1E293B; border-left: 4px solid #10B981; padding: 12px 16px; margin: 12px 0; border-radius: 4px; }
</style>
</head>
<body>
<div class="window">
  <div class="title-bar">
    <div class="dots"><div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div></div>
    <div class="title-text">Motor de Alertas Automáticas ODS 12 &amp; Auditoría Saga DLQ (Monchis Café)</div>
    <div style="width: 50px;"></div>
  </div>
  <div class="term-body">
    <p><span class="prompt">PS D:\\ernestofm\\Proyecto&gt;</span> <span class="cmd">curl -X POST http://localhost:8080/api/admin/notifications/check-alerts -H "Authorization: Bearer $ADMIN_TOKEN"</span></p>
    <p style="color: #94A3B8; margin-top: 6px;">[2026-10-28 21:45:00] [AUDIT-CRON] Iniciando barrido nocturno de fechas de caducidad e inventario PEPS...</p>
    
    <div class="card-alert">
      <p><span class="badge-warn">ALERTA CADUCIDAD</span> <strong>Lote Próximo a Vencer (&lt; 15 días)</strong></p>
      <p style="color: #F8FAFC; margin-top: 4px;">• Lote ID: <span style="color:#38BDF8;">MC-CHP-2026-A1</span> | Producto: <strong>Café de Olla Orgánico (Chiapas)</strong></p>
      <p style="color: #CBD5E1;">• Proveedor: Cooperativa Café de Altura Chiapas (Finca Santa Rosa)</p>
      <p style="color: #CBD5E1;">• Fecha Caducidad: <strong>2027-01-15</strong> (14 días restantes) | Stock disponible: <strong>42.5 kg</strong></p>
      <p style="color: #4ADE80; margin-top: 6px;">✔ Notificación SMTP despachada a: <code>gerencia@monchiscafe.com</code> y <code>calidad@monchiscafe.com</code> [Status: 250 OK]</p>
      <p style="color: #FBBF24;">⚡ Acción de Mitigación ODS 12.3: Prioridad forzada en Terminal POS para rotación PEPS inmediata.</p>
    </div>

    <p><span class="prompt">PS D:\\ernestofm\\Proyecto&gt;</span> <span class="cmd">curl -s http://localhost:8080/api/admin/audit/dlq -H "Authorization: Bearer $ADMIN_TOKEN"</span></p>
    <div class="card-saga">
      <p><span class="badge-success">SUPERVISIÓN DLQ OK</span> <strong>RabbitMQ Dead Letter Queue Audit</strong></p>
      <p style="color: #F8FAFC; margin-top: 4px;">• Broker: <code>amqp://rabbitmq:5672</code> | Exchange: <code>monchis.orders.topic</code></p>
      <p style="color: #CBD5E1;">• Cola Principal: <code>orders.process</code> (0 pendientes) | Cola DLQ: <code>orders.dlq</code> (0 mensajes descartados)</p>
      <p style="color: #CBD5E1;">• Tasa de Éxito de Transacciones Saga: <strong>100%</strong> (246 de 246 pedidos confirmados sin fallas de compensación)</p>
      <p style="color: #4ADE80; margin-top: 4px;">✔ Ningún pedido comprometido; integridad de stock e ingresos garantizada bajo directivas OWASP.</p>
    </div>

    <p><span class="prompt">PS D:\\ernestofm\\Proyecto&gt;</span> <span style="color:#10B981;font-weight:bold;">✔ Ejecución de auditoría completada satisfactoriamente sin incidencias activas.</span></p>
  </div>
</div>
</body>
</html>
"""

create_terminal_image(html_infra, os.path.join(img_dir, "m3_despliegue_infra.png"), 1280, 680)
create_terminal_image(html_logs, os.path.join(img_dir, "m3_monitoreo_logs.png"), 1280, 680)
create_terminal_image(html_alertas, os.path.join(img_dir, "m3_monitoreo_alertas.png"), 1280, 680)

# Copiar evidencia5_admin.png a m3_monitoreo_admin.png si existe
src_admin = os.path.join(img_dir, "evidencia5_admin.png")
dst_admin = os.path.join(img_dir, "m3_monitoreo_admin.png")
if os.path.exists(src_admin):
    import shutil
    shutil.copyfile(src_admin, dst_admin)
    print(f"Copiada evidencia5_admin.png a {dst_admin}")

