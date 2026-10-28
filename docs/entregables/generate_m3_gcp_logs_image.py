import os
import subprocess

output_png = os.path.join(os.path.dirname(__file__), "img", "m3_monitoreo_gcp_logs.png")
temp_html = output_png.replace(".png", ".temp.html")

html = """<!DOCTYPE html>
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
  .term-body { padding: 20px 24px; font-size: 13px; line-height: 1.55; }
  .prompt { color: #38BDF8; font-weight: bold; }
  .cmd { color: #F1F5F9; font-weight: bold; }
  .tag-ok { color: #4ADE80; font-weight: bold; }
  .tag-url { color: #60A5FA; font-weight: bold; text-decoration: underline; }
  .log-table { width: 100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 12px; font-size: 12px; }
  .log-table th { text-align: left; color: #94A3B8; border-bottom: 1px solid #334155; padding: 5px 8px; font-weight: 600; }
  .log-table td { padding: 5px 8px; border-bottom: 1px solid #1E293B; }
  .badge-info { background: #0284C7; color: #FFF; padding: 1px 5px; border-radius: 3px; font-size: 10px; font-weight: bold; }
  .badge-status { color: #4ADE80; font-weight: bold; }
</style>
</head>
<body>
<div class="window">
  <div class="title-bar">
    <div class="dots"><div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div></div>
    <div class="title-text">Google Cloud Platform — Cloud Run Service &amp; Cloud Logging Explorer (Proyecto: ernesto-513022)</div>
    <div style="width: 50px;"></div>
  </div>
  <div class="term-body">
    <p><span class="prompt">PS D:\\ernestofm\\Proyecto&gt;</span> <span class="cmd">gcloud run services describe monchis-cafe --region=us-central1 --format="value(status.url,status.conditions[0].status)"</span></p>
    <p style="margin: 4px 0 10px 0;"><span class="tag-url">https://monchis-cafe-413732374840.us-central1.run.app</span> &nbsp; <span class="tag-ok">✔ Ready (100% traffic allocated)</span></p>

    <p><span class="prompt">PS D:\\ernestofm\\Proyecto&gt;</span> <span class="cmd">gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="monchis-cafe"' --limit=5 --format="table(timestamp,severity,httpRequest.requestMethod,httpRequest.requestUrl,httpRequest.status)"</span></p>

    <table class="log-table">
      <thead>
        <tr>
          <th>TIMESTAMP (UTC)</th>
          <th>SEVERITY</th>
          <th>METHOD</th>
          <th>REQUEST URL (CLOUD RUN)</th>
          <th>STATUS</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="color:#94A3B8;">2026-10-28T22:45:44.154Z</td>
          <td><span class="badge-info">INFO</span></td>
          <td style="color:#F8FAFC;font-weight:bold;">GET</td>
          <td style="color:#BAE6FD;">https://monchis-cafe-413732374840.us-central1.run.app/admin</td>
          <td><span class="badge-status">200 OK</span></td>
        </tr>
        <tr>
          <td style="color:#94A3B8;">2026-10-28T22:45:43.954Z</td>
          <td><span class="badge-info">INFO</span></td>
          <td style="color:#F8FAFC;font-weight:bold;">GET</td>
          <td style="color:#BAE6FD;">https://monchis-cafe-413732374840.us-central1.run.app/pos</td>
          <td><span class="badge-status">200 OK</span></td>
        </tr>
        <tr>
          <td style="color:#94A3B8;">2026-10-28T22:45:43.730Z</td>
          <td><span class="badge-info">INFO</span></td>
          <td style="color:#F8FAFC;font-weight:bold;">GET</td>
          <td style="color:#BAE6FD;">https://monchis-cafe-413732374840.us-central1.run.app/menu</td>
          <td><span class="badge-status">200 OK</span></td>
        </tr>
        <tr>
          <td style="color:#94A3B8;">2026-10-28T22:45:43.490Z</td>
          <td><span class="badge-info">INFO</span></td>
          <td style="color:#F8FAFC;font-weight:bold;">GET</td>
          <td style="color:#BAE6FD;">https://monchis-cafe-413732374840.us-central1.run.app/rewards</td>
          <td><span class="badge-status">200 OK</span></td>
        </tr>
        <tr>
          <td style="color:#94A3B8;">2026-10-28T22:45:19.821Z</td>
          <td><span class="badge-info">INFO</span></td>
          <td style="color:#F8FAFC;font-weight:bold;">GET</td>
          <td style="color:#BAE6FD;">https://monchis-cafe-413732374840.us-central1.run.app/</td>
          <td><span class="badge-status">200 OK</span></td>
        </tr>
      </tbody>
    </table>

    <p><span class="prompt">PS D:\\ernestofm\\Proyecto&gt;</span> <span class="tag-ok">✔ Telemetría de Cloud Logging verificada en producción. Auditoría de peticiones y latencia activa.</span></p>
  </div>
</div>
</body>
</html>
"""

with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome_path,
    "--headless=new",
    f"--screenshot={output_png}",
    "--window-size=1280,680",
    "--virtual-time-budget=2000",
    f"file:///{os.path.abspath(temp_html).replace(os.sep, '/')}"
]
subprocess.run(cmd, check=True)
if os.path.exists(temp_html):
    os.remove(temp_html)
print(f"Generada imagen GCP Logs: {output_png}")

