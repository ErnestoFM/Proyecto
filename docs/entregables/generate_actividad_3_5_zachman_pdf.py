import os
import subprocess

BASE_DIR = r"d:\ernestofm\Proyecto\docs\entregables\actividad_3_5_zachman"
HTML_OUT_PATH = os.path.join(r"d:\ernestofm\Proyecto\docs\entregables", "Actividad_3_5_Matriz_Zachman_Equipo2.html")
PDF_OUT_PATH = os.path.join(r"d:\ernestofm\Proyecto\docs\entregables", "Actividad_3_5_Matriz_Zachman_Equipo2.pdf")
DOWNLOADS_PDF_PATH = r"C:\Users\erfierro\Downloads\Actividad_3_5_Matriz_Zachman_Equipo2.pdf"

# Dictionary of Google Drive / Docs links.
# Can be updated with the actual links from the user.
DOCS_LINKS = {
    # Fila 1: INTENCIÓN
    "c01": "https://drive.google.com/file/d/1JN_dtu5lZ1W7tbtIF0IKflDZPmsfYhf3/view?usp=sharing", # 01_caracteristicas.docx
    "c02": "https://drive.google.com/file/d/1vcsIoEWRk4YHCevhiRMAXfcy3Bx66GEu/view?usp=sharing", # 02_procesos_negocio.docx
    "c03": "https://drive.google.com/file/d/1LzBN-nL0tG-zNTOaP2HoctF0gQJVmdd1/view?usp=sharing", # 03_diagrama_contexto.docx
    "c04": "https://drive.google.com/file/d/1Wzye6_ptLYnj-maWlK4KD0UG6N26zPra/view?usp=sharing", # 04_workflow_roles.docx
    "c05": "https://drive.google.com/file/d/1TfmMaKqq7NDDG6rJWS3F_GMakRlu5WEJ/view?usp=sharing", # 05_listado_eventos.docx
    "c06": "https://drive.google.com/file/d/1Ip5KtpyCUPkLIxO7MxxnFKhMVXtaz9CH/view?usp=sharing", # 06_vision_objetivos.docx
    
    # Fila 2: ALCANCE
    "c07": "https://drive.google.com/file/d/16W6lQikUgddAJ_KBMcXtxEKs69DheEdR/view?usp=sharing", # 07_listado_requerimientos.docx
    "c08": "https://drive.google.com/file/d/1Peu-KbIO6gYiDaw4GL4FjdYuPUxfrs_t/view?usp=sharing", # 08_diagramas_actividad.docx
    "c09": "https://drive.google.com/file/d/1tDRRXX3a6l6XLnXlf6dz8XU0syW5gYpv/view?usp=sharing", # 09_ambiente_operativo_rnf.docx
    "c10": "https://drive.google.com/file/d/1laKg-ZQjPQ6wK8LZf7HKQ8F1w1OdXUZ_/view?usp=sharing", # 10_rol_negocio.docx
    "c11": "https://drive.google.com/file/d/182RflhJkU9rRvR4cFmB2hGIaat-XJhpo/view?usp=sharing", # 11_cronograma_negocio.docx
    "c12": "https://drive.google.com/file/d/1j68qAoV3ERWpcu55pOt0arTVubQW8Oz9/view?usp=sharing", # 12_prioridades_negocio.docx
    
    # Fila 3: ALTO NIVEL
    "c13": "https://drive.google.com/file/d/1YreuU-wXv48jbjeqUQ8p9L3GmDx7d9d1/view?usp=sharing", # 13_listado_casos_uso.docx
    "c14": "https://drive.google.com/file/d/1_cDRjedF6fy1GsQmVd-IndjlCYP70CCp/view?usp=sharing", # 14_especificacion_casos_uso.docx
    "c15": "https://drive.google.com/file/d/1WRVpfAYHLaH3OTnbtSHMcCC6eMhOT7Kr/view?usp=sharing", # 15_subsistemas_modulos.docx
    "c16": "https://drive.google.com/file/d/14TNzrFVrvmTok-ft1q7ZJsq6ybI2MD6l/view?usp=sharing", # 16_actores_descripcion.docx
    "c17": "https://drive.google.com/file/d/1oc3S5ZsxEnefU3D5VnziqO1WboquZ0bU/view?usp=sharing", # 17_precedencia_casos_uso.docx
    "c18": "https://drive.google.com/file/d/1lQZliiNeIBKsRtnwZq_AQzI9-VYM0f3v/view?usp=sharing", # 18_reglas_negocio_prioridades.docx
    
    # Fila 4: DETALLE
    "c19": "https://drive.google.com/file/d/16cuwd5f5ozDXF5XtztKYo6OVAfNaArkI/view?usp=sharing", # 19_diagrama_cu_ui_dominio.docx
    "c20": "https://drive.google.com/file/d/1s87hXYzVU8eJpM2mPCoOuFC8T_gYCnNE/view?usp=sharing", # 20_especificacion_navegacion.docx
    "c21": "https://drive.google.com/file/d/1-eevSj942qa2g61nRMKnW1KZKvfrB1xj/view?usp=sharing", # 21_diagrama_paquetes.docx
    "c22": "https://drive.google.com/file/d/1rBP2enmghjbUN1aGE1FfZixubyQ2EwVC/view?usp=sharing", # 22_actores_permisos_rbac.docx
    "c23": "https://drive.google.com/file/d/1WoA5Sw573CwePZ04SNnRf51O8x21sjmx/view?usp=sharing", # 23_diagrama_estados.docx
    "c24": "https://drive.google.com/file/d/1u_WlrnJiJo7AeiG091-n-Gpevaq5MJ9y/view?usp=sharing", # 24_reglas_modelo_analisis.docx
}

def build_html(links):
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Actividad 3.5 Matriz de Zachman — Monchis Café (Equipo 2)</title>
<style>
  @page {{
    size: letter landscape;
    margin: 0.8cm;
  }}
  @page portadapg {{
    size: letter portrait;
    margin: 1.5cm;
  }}
  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  body {{
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #2D3748;
    margin: 0;
    padding: 0;
    background: #FFFFFF;
  }}
  
  /* Portada */
  .portada-page {{
    page: portadapg;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 98vh;
    text-align: center;
    padding: 2.5cm 1cm 1.5cm 1cm;
  }}
  .portada-header h1 {{
    font-size: 24pt;
    font-weight: 800;
    color: #1A365D;
    margin: 0 0 10px 0;
    letter-spacing: 0.5px;
  }}
  .portada-header h2 {{
    font-size: 16pt;
    font-weight: 600;
    color: #2B6CB0;
    margin: 0 0 8px 0;
  }}
  .portada-header h3 {{
    font-size: 13pt;
    font-weight: 500;
    color: #4A5568;
    margin: 0 0 6px 0;
  }}
  .portada-header h4 {{
    font-size: 12pt;
    font-weight: 500;
    color: #718096;
    margin: 0;
  }}
  .escudo-box {{
    margin: 15px auto;
  }}
  .escudo-box img {{
    height: 175px;
    width: auto;
    object-fit: contain;
  }}
  .portada-title {{
    margin: 20px 0;
  }}
  .portada-title h2 {{
    font-size: 20pt;
    font-weight: 800;
    color: #C05621;
    margin: 0 0 6px 0;
  }}
  .portada-title p {{
    font-size: 12pt;
    font-weight: 600;
    color: #4A5568;
    margin: 0;
  }}
  .portada-team {{
    margin: 20px auto;
    max-width: 500px;
    background: #F7FAFC;
    border-radius: 8px;
    border-left: 4px solid #1A365D;
    padding: 15px 25px;
    text-align: left;
  }}
  .portada-team h5 {{
    font-size: 11pt;
    font-weight: 700;
    color: #1A365D;
    margin: 0 0 10px 0;
    text-align: center;
  }}
  .portada-team ul {{
    list-style: none;
    padding: 0;
    margin: 0;
  }}
  .portada-team li {{
    font-size: 10pt;
    color: #2D3748;
    margin-bottom: 5px;
    display: flex;
    justify-content: space-between;
  }}
  .portada-team li span.codigo {{
    font-weight: 600;
    color: #2B6CB0;
  }}
  .portada-footer {{
    font-size: 10pt;
    color: #718096;
    border-top: 1px solid #E2E8F0;
    padding-top: 15px;
  }}

  /* Matriz de Zachman Page */
  .matrix-page {{
    page-break-after: always;
    padding: 0;
  }}
  .matrix-title {{
    text-align: center;
    font-size: 16pt;
    font-weight: 800;
    color: #C05621;
    margin: 0 0 8px 0;
  }}
  .matrix-table {{
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
    font-size: 7.5pt;
  }}
  .matrix-table th, .matrix-table td {{
    border: 1.5px solid #C05621;
    padding: 6px 5px;
    vertical-align: top;
    word-wrap: break-word;
    overflow-wrap: break-word;
  }}
  .matrix-table th {{
    background-color: #ED8936;
    color: #FFFFFF;
    text-align: center;
    font-weight: 800;
    font-size: 8pt;
    text-transform: uppercase;
  }}
  .row-hdr {{
    background-color: #ED8936;
    color: #FFFFFF;
    font-weight: 800;
    font-size: 8pt;
    text-align: center;
    vertical-align: middle !important;
    width: 7.5%;
  }}
  .cell-title {{
    font-weight: 800;
    color: #1A365D;
    display: block;
    margin-bottom: 3px;
    line-height: 1.15;
  }}
  .cell-link {{
    font-size: 6.8pt;
    color: #2B6CB0;
    text-decoration: underline;
    display: block;
    line-height: 1.15;
    word-break: break-all;
  }}
  .cell-desc {{
    font-size: 6.8pt;
    color: #4A5568;
    margin-top: 2px;
    line-height: 1.15;
  }}

  /* Justificación Metodológica Page */
  .justificacion-page {{
    page-break-before: always;
    padding: 10px 20px;
    font-size: 8.5pt;
    line-height: 1.35;
  }}
  .justificacion-page h2 {{
    font-size: 13pt;
    font-weight: 800;
    color: #1A365D;
    border-bottom: 2px solid #C05621;
    padding-bottom: 4px;
    margin-top: 0;
  }}
  .justificacion-page h3 {{
    font-size: 10pt;
    font-weight: 700;
    color: #C05621;
    margin: 8px 0 3px 0;
  }}
  .justificacion-page p {{
    margin: 0 0 6px 0;
    text-align: justify;
  }}
  .justificacion-page ol {{
    margin: 0 0 8px 0;
    padding-left: 18px;
  }}
  .justificacion-page li {{
    margin-bottom: 3px;
  }}
</style>
</head>
<body>

<!-- PÁGINA 1: PORTADA -->
<div class="portada-page">
  <div class="portada-header">
    <h1>UNIVERSIDAD DE GUADALAJARA</h1>
    <h2>Centro Universitario de Tonalá</h2>
    <h3>Ingeniería en Ciencias Computacionales</h3>
    <h4>Proyecto Integrador de Desarrollo de Software</h4>
  </div>

  <div class="escudo-box">
    <img src="file:///d:/ernestofm/Proyecto/docs/entregables/img/escudo_udg_oficial.png" alt="Escudo Oficial Universidad de Guadalajara">
  </div>

  <div class="portada-title">
    <h2>Actividad 3.5. Matriz de Zachman</h2>
    <p>Aplicación de la Arquitectura Conceptual y Lógica a los Requerimientos</p>
    <p style="font-size: 10.5pt; color: #8C6B52; margin-top: 4px; font-weight: 700;">Proyecto Oficial: Monchis Café — Cafetería Orgánica y Comercial (Equipo 2)</p>
  </div>

  <div class="portada-team">
    <h5>INTEGRANTES DEL EQUIPO 2</h5>
    <ul>
      <li><span>Ernesto Hatuey Fierro Medina</span> <span class="codigo">Código: 215487963</span></li>
      <li><span>Jazmín Díaz Cruz</span> <span class="codigo">Desarrollo Frontend</span></li>
      <li><span>Héctor Manuel Hernández Gómez</span> <span class="codigo">Desarrollo Backend</span></li>
      <li><span>Oswaldo Daniel Millán Rodríguez</span> <span class="codigo">QA & DevSecOps</span></li>
    </ul>
  </div>

  <div class="portada-footer">
    <p><strong>Docente:</strong> Dr. Gabriel Navarro Salcedo &nbsp;|&nbsp; <strong>Fecha:</strong> Octubre 2026 &nbsp;|&nbsp; Tonalá, Jalisco, México</p>
  </div>
</div>

<!-- PÁGINA 2: MATRIZ DE ZACHMAN APLICADA A REQUERIMIENTOS -->
<div class="matrix-page">
  <h2 class="matrix-title">Actividad. Matriz de Zachman aplicada al trabajo con requerimientos</h2>
  
  <table class="matrix-table">
    <thead>
      <tr>
        <th style="width: 7.5%;">NIVEL</th>
        <th style="width: 14.5%;">QUE</th>
        <th style="width: 15.5%;">COMO</th>
        <th style="width: 15.5%;">DONDE</th>
        <th style="width: 15.5%;">QUIEN</th>
        <th style="width: 15.5%;">CUANDO</th>
        <th style="width: 16%;">POR QUÉ</th>
      </tr>
    </thead>
    <tbody>
      <!-- FILA 1: INTENCIÓN -->
      <tr>
        <td class="row-hdr">INTENCIÓN</td>
        <td>
          <span class="cell-title">Características:</span>
          <a class="cell-link" href="{links['c01']}">{links['c01']}</a>
          <span class="cell-desc">Catálogo segmentado, POS multipago, Rewards ODS 12, trazabilidad y seguridad stateless.</span>
        </td>
        <td>
          <span class="cell-title">Listado de Proceso de Negocio:</span>
          <a class="cell-link" href="{links['c02']}">{links['c02']}</a>
          <span class="cell-desc">PN-01 a PN-06: Abastecimiento, venta mostrador, sellos Rewards, mermas PEPS y corte de caja.</span>
        </td>
        <td>
          <span class="cell-title">Diagramas de Contexto:</span>
          <a class="cell-link" href="{links['c03']}">{links['c03']}</a>
          <span class="cell-desc">DFD Nivel 0 con entidades externas: Cliente, Cajero, Admin, Cooperativas, Banco SPEI y Google.</span>
        </td>
        <td>
          <span class="cell-title">Workflow (roles y act):</span>
          <a class="cell-link" href="{links['c04']}">{links['c04']}</a>
          <span class="cell-desc">Flujo de trabajo operativo entre los 4 roles humanos y Matriz RACI para 10 tareas clave.</span>
        </td>
        <td>
          <span class="cell-title">Listado de Eventos:</span>
          <a class="cell-link" href="{links['c05']}">{links['c05']}</a>
          <span class="cell-desc">10 eventos de negocio (EVT-01 a EVT-10): Apertura caja, termo reusable, cobro, alertas y corte Z.</span>
        </td>
        <td>
          <span class="cell-title">Visión. Objetivos:</span>
          <a class="cell-link" href="{links['c06']}">{links['c06']}</a>
          <span class="cell-desc">Misión, visión, 4 objetivos SMART y alineación estratégica con ODS 12 (Metas 12.2, 12.3 y 12.5).</span>
        </td>
      </tr>

      <!-- FILA 2: ALCANCE -->
      <tr>
        <td class="row-hdr">ALCANCE</td>
        <td>
          <span class="cell-title">Listado de requerimientos:</span>
          <a class="cell-link" href="{links['c07']}">{links['c07']}</a>
          <span class="cell-desc">Catálogo de 15 Requerimientos Funcionales (RF-01 a RF-15) con actores y criterios de éxito.</span>
        </td>
        <td>
          <span class="cell-title">Diagramas de Actividad:</span>
          <a class="cell-link" href="{links['c08']}">{links['c08']}</a>
          <span class="cell-desc">DA-01 Venta en Mostrador con Bono Ecológico y DA-02 Abastecimiento de Café con Alerta PEPS.</span>
        </td>
        <td>
          <span class="cell-title">Ambiente Operativo. Requerimientos No funcionales:</span>
          <a class="cell-link" href="{links['c09']}">{links['c09']}</a>
          <span class="cell-desc">GCP Cloud Run, Docker Compose local y 7 RNF bajo la norma internacional ISO/IEC 25010.</span>
        </td>
        <td>
          <span class="cell-title">Rol de Negocio:</span>
          <a class="cell-link" href="{links['c10']}">{links['c10']}</a>
          <span class="cell-desc">Fichas de caracterización de Administrador, Cajero de Turno, Cliente y Proveedor Campesino.</span>
        </td>
        <td>
          <span class="cell-title">Cronograma de Negocio:</span>
          <a class="cell-link" href="{links['c11']}">{links['c11']}</a>
          <span class="cell-desc">4 fases de adopción en 16 semanas, hitos de negocio y ciclo diario de horarios en cafetería.</span>
        </td>
        <td>
          <span class="cell-title">Prioridades de Negocio:</span>
          <a class="cell-link" href="{links['c12']}">{links['c12']}</a>
          <span class="cell-desc">Jerarquización formal MoSCoW (Must, Should, Could, Won't Have) y matriz de valor vs esfuerzo.</span>
        </td>
      </tr>

      <!-- FILA 3: ALTO NIVEL -->
      <tr>
        <td class="row-hdr">ALTO NIVEL</td>
        <td>
          <span class="cell-title">Listado de casos de uso:</span>
          <a class="cell-link" href="{links['c13']}">{links['c13']}</a>
          <span class="cell-desc">Catálogo consolidado de 12 Casos de Uso (CU-01 a CU-12) cruzados con los requerimientos.</span>
        </td>
        <td>
          <span class="cell-title">Especificación de Casos de Uso principales:</span>
          <a class="cell-link" href="{links['c14']}">{links['c14']}</a>
          <span class="cell-desc">Plantillas formales Cockburn para CU-01 (Login reCAPTCHA), CU-03/04 (POS) y CU-12 (Reversa Saga).</span>
        </td>
        <td>
          <span class="cell-title">Subsistema, Módulo:</span>
          <a class="cell-link" href="{links['c15']}">{links['c15']}</a>
          <span class="cell-desc">Arquitectura Monorepo desacoplada: apps/web, apps/api, packages/database y packages/messaging.</span>
        </td>
        <td>
          <span class="cell-title">Actores Descripción:</span>
          <a class="cell-link" href="{links['c16']}">{links['c16']}</a>
          <span class="cell-desc">Caracterización de 8 actores (humanos y sistemas/servicios) y matriz de interacción cruzada.</span>
        </td>
        <td>
          <span class="cell-title">Precedencia de Casos de uso:</span>
          <a class="cell-link" href="{links['c17']}">{links['c17']}</a>
          <span class="cell-desc">Reglas de precedencia obligatoria, inclusión &lt;&lt;include&gt;&gt;, extensión &lt;&lt;extend&gt;&gt; y grafo dirigido.</span>
        </td>
        <td>
          <span class="cell-title">Prioridades del Proyecto. Reglas del Negocio:</span>
          <a class="cell-link" href="{links['c18']}">{links['c18']}</a>
          <span class="cell-desc">8 reglas de negocio (RN-01 a RN-08) y jerarquización por nivel de prioridad crítica (P1, P2, P3).</span>
        </td>
      </tr>

      <!-- FILA 4: DETALLE -->
      <tr>
        <td class="row-hdr">DETALLE</td>
        <td>
          <span class="cell-title">Diagrama Casos de Uso, Prototipo de Interfaces, Modelo de Dominio:</span>
          <a class="cell-link" href="{links['c19']}">{links['c19']}</a>
          <span class="cell-desc">Diagrama UML global, wireframes reales de POS y Login, y MER relacional de base de datos.</span>
        </td>
        <td>
          <span class="cell-title">Especificación de Casos de Uso, Prototipo de Navegación:</span>
          <a class="cell-link" href="{links['c20']}">{links['c20']}</a>
          <span class="cell-desc">Grafo de navegación en Vue Router 4, guardianes de ruta (beforeEach) y atajos de teclado (F2, Esc).</span>
        </td>
        <td>
          <span class="cell-title">Paquete:</span>
          <a class="cell-link" href="{links['c21']}">{links['c21']}</a>
          <span class="cell-desc">Diagrama de paquetes UML @monchis/* bajo el Principio de Dependencias Acíclicas (ADP).</span>
        </td>
        <td>
          <span class="cell-title">Actores. Permisos. Responsabilidades:</span>
          <a class="cell-link" href="{links['c22']}">{links['c22']}</a>
          <span class="cell-desc">Matriz CRUD de permisos RBAC por endpoint de API y rutas web, con principio de menor privilegio.</span>
        </td>
        <td>
          <span class="cell-title">Diagrama de Estados:</span>
          <a class="cell-link" href="{links['c23']}">{links['c23']}</a>
          <span class="cell-desc">Autómatas finitos del ciclo de vida de una Orden de Venta (Order) y de un Lote de Café (Batch).</span>
        </td>
        <td>
          <span class="cell-title">Reglas de Negocio asignadas en el Modelo de Análisis:</span>
          <a class="cell-link" href="{links['c24']}">{links['c24']}</a>
          <span class="cell-desc">Trazabilidad de las 8 reglas a código TypeScript, restricciones Prisma y pruebas Vitest.</span>
        </td>
      </tr>
    </tbody>
  </table>
</div>

<!-- PÁGINA 3: JUSTIFICACIÓN METODOLÓGICA Y FUENTES VERÍDICAS -->
<div class="justificacion-page">
  <h2>Justificación Conceptual y Metodológica de la Matriz de Zachman</h2>
  <p>La Matriz de Zachman aplicada a la ingeniería de requerimientos organiza la arquitectura de <strong>Monchis Café</strong> mediante una estructura bidimensional ortogonal que garantiza completitud, coherencia vertical (trazabilidad entre niveles de abstracción) y coherencia horizontal (respuestas complementarias a las 6 preguntas clásicas de comunicación humana) (Zachman, 1987).</p>
  
  <h3>1. Coherencia entre Capas (Trazabilidad Vertical):</h3>
  <ol>
    <li><strong>Nivel 1 (Intención - Visión del Planificador):</strong> Establece el contexto macro del negocio de cafetería familiar y el modelo de comercio justo con cooperativas campesinas, delimitando qué existe, cómo opera a grandes rasgos y por qué es rentable y sostenible bajo el ODS 12 (Sapag Chain, 2011).</li>
    <li><strong>Nivel 2 (Alcance - Visión del Dueño del Negocio):</strong> Traduce las intenciones en especificaciones comerciales concretas: los 15 Requerimientos Funcionales, diagramas de actividad de mostrador, el ambiente operativo bajo ISO/IEC 25010 y la priorización MoSCoW para construir primero lo innegociable (Wiegers & Beatty, 2013).</li>
    <li><strong>Nivel 3 (Alto Nivel - Visión del Diseñador del Sistema):</strong> Modela la solución lógica orientada a objetos: el catálogo de 12 Casos de Uso, la arquitectura modular de Monorepo, los actores primarios y secundarios, la precedencia de eventos y las 8 reglas de negocio (Ross, 2003; Larman, 2004).</li>
    <li><strong>Nivel 4 (Detalle - Visión del Constructor de Software):</strong> Aterriza las abstracciones en artefactos de implementación directa: esquemas relacionales de base de datos en PostgreSQL 15, wireframes ergonómicos de mostrador, paquetes acíclicos (@monchis/*), matriz de permisos RBAC y diagramas de estados (Martin, 2002; Ferraiolo et al., 2001).</li>
  </ol>

  <h3>2. Coherencia entre Perspectivas (Alineación Horizontal):</h3>
  <p>Cada una de las seis columnas mantiene un hilo conductor inquebrantable a lo largo de los cuatro niveles: la columna <strong>QUÉ</strong> evoluciona desde las características de negocio hasta el esquema de datos y entidades; la columna <strong>CÓMO</strong> transita desde los procesos macro hasta la especificación de navegación y transiciones de pantalla; la columna <strong>DÓNDE</strong> va desde el diagrama de contexto exterior hasta la arquitectura física de paquetes; la columna <strong>QUIÉN</strong> pasa de la definición de roles humanos a la matriz de permisos RBAC en código; la columna <strong>CUÁNDO</strong> evoluciona de los eventos comerciales a las máquinas de estado finitas; y la columna <strong>POR QUÉ</strong> asegura que la visión estratégica de sostenibilidad ODS 12 se convierta en restricciones de validación que se ejecutan automáticamente en el servidor (Pressman & Maxim, 2021).</p>

  <h3>3. Referencias Bibliográficas Verídicas (Norma APA 7.ª Edición):</h3>
  <ol>
    <li><strong>Bass, L., Clements, P., & Kazman, R. (2012).</strong> <em>Software Architecture in Practice</em> (3.ª ed.). Addison-Wesley.</li>
    <li><strong>Cockburn, A. (2000).</strong> <em>Writing Effective Use Cases</em>. Addison-Wesley Professional.</li>
    <li><strong>Evans, E. (2003).</strong> <em>Domain-Driven Design: Tackling Complexity in the Heart of Software</em>. Addison-Wesley.</li>
    <li><strong>Ferraiolo, D. F., Sandhu, R., Gavrila, S., Kuhn, D. R., & Chandramouli, R. (2001).</strong> Proposed NIST standard for role-based access control. <em>ACM TISSEC</em>, 4(3), 224–274.</li>
    <li><strong>Fowler, M. (2002).</strong> <em>Patterns of Enterprise Application Architecture</em>. Addison-Wesley.</li>
    <li><strong>ISO/IEC/IEEE. (2018).</strong> <em>ISO/IEC/IEEE 29148:2018 Systems and software engineering — Requirements engineering</em>. IEEE.</li>
    <li><strong>Martin, R. C. (2002).</strong> <em>Agile Software Development, Principles, Patterns, and Practices</em>. Prentice Hall.</li>
    <li><strong>Pressman, R. S., & Maxim, B. R. (2021).</strong> <em>Ingeniería de software: un enfoque práctico</em> (9.ª ed.). McGraw-Hill Interamericana.</li>
    <li><strong>Sommerville, I. (2011).</strong> <em>Ingeniería del software</em> (9.ª ed.). Addison-Wesley / Pearson Educación.</li>
    <li><strong>Zachman, J. A. (1987).</strong> A framework for information systems architecture. <em>IBM Systems Journal</em>, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276</li>
  </ol>
</div>

</body>
</html>
"""
    return html_content

def compile_pdf(html_path, pdf_path):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    print(f"Compilando PDF con Chrome Headless...")
    subprocess.run(cmd, check=True)
    print(f"PDF generado exitosamente en: {pdf_path}")

def main():
    print("Generando HTML maestro de la Matriz de Zachman...")
    html_code = build_html(DOCS_LINKS)
    with open(HTML_OUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_code)
    print(f"HTML guardado en: {HTML_OUT_PATH}")

    compile_pdf(HTML_OUT_PATH, PDF_OUT_PATH)

    # Copy to downloads
    import shutil
    shutil.copy2(PDF_OUT_PATH, DOWNLOADS_PDF_PATH)
    print(f"Copia depositada en Descargas: {DOWNLOADS_PDF_PATH}")

if __name__ == "__main__":
    main()

