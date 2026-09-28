import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import os

def create_document():
    doc = docx.Document()
    
    # Page setup - Margins (2.5 cm approx 1 inch)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Buenas Prácticas de Calidad (Aplicaciones de Software) | Actividad de Participación")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(120, 120, 120)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Monchis Café — Plataforma Web Segura | Ernesto Fierro")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(120, 120, 120)

    # Styles
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(10.5)
    style_normal.font.color.rgb = RGBColor(40, 40, 40)

    # Helper XML shading & borders
    def set_cell_background(cell, fill_hex):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_table_borders(table, color="D3D3D3"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
                <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
                <w:insideV w:val="none"/>
                <w:left w:val="none"/>
                <w:right w:val="none"/>
            </w:tblBorders>
        ''')
        tblPr.append(borders)

    # Document Header / Banner Box
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("ACTIVIDAD DE PARTICIPACIÓN — TABLA COMPARATIVA")
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(10)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(31, 78, 121)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("Buenas Prácticas de Calidad en Aplicaciones de Software")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(17)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(31, 78, 121)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("Análisis Teórico y Propuesta Aplicada al Proyecto: Monchis Café")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(80, 80, 80)

    # Metadata Info Table
    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    
    col_widths = [Inches(3.4), Inches(3.5)]
    meta_data = [
        [("Materia / Asignatura:", " Buenas Prácticas de Calidad (Aplicaciones de Software)"),
         ("Docente:", " Dr. Gabriel Navarro Salcedo")],
        [("Alumno / Autor:", " Ernesto Fierro Moreno (Individual)"),
         ("Fecha de Entrega:", " 14 de Septiembre de 2026 (23:59 hrs)")]
    ]
    
    for row_idx, row in enumerate(meta_table.rows):
        for col_idx, cell in enumerate(row.cells):
            cell.width = col_widths[col_idx]
            set_cell_background(cell, "F2F5F8")
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            label, val = meta_data[row_idx][col_idx]
            run_lbl = p.add_run(label)
            run_lbl.font.bold = True
            run_lbl.font.size = Pt(9.5)
            run_lbl.font.color.rgb = RGBColor(31, 78, 121)
            run_val = p.add_run(val)
            run_val.font.size = Pt(9.5)
            run_val.font.color.rgb = RGBColor(50, 50, 50)
            
    # Add spacing after meta table
    p_sep = doc.add_paragraph()
    p_sep.paragraph_format.space_before = Pt(8)
    p_sep.paragraph_format.space_after = Pt(6)

    # Introduction / Context Paragraph
    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.space_after = Pt(12)
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_intro = p_intro.add_run(
        "El presente documento expone una tabla comparativa exhaustiva que aborda los ocho componentes clave del ciclo de vida y calidad en el desarrollo de software. En la primera columna se establece la fundamentación conceptual y teórica de cada fase según estándares de ingeniería de software; en la segunda columna se formula y analiza una propuesta de implementación concreta y aplicada a nuestro proyecto de titulación: "
    )
    r_intro_bold = p_intro.add_run("Monchis Café — Plataforma Web Segura para Cafetería Orgánica y Comercial")
    r_intro_bold.font.bold = True
    r_intro_bold.font.color.rgb = RGBColor(31, 78, 121)
    p_intro.add_run(
        ", sustentada en arquitectura Monorepo (Vue 3 + Next.js), transacciones asíncronas con RabbitMQ (Patrón Saga), seguridad stateless con JWT y reCAPTCHA, y trazabilidad de lotes agrícolas."
    )

    # COMPARATIVE TABLE
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table, "D0D7DE")

    # Header Row
    hdr_cells = table.rows[0].cells
    hdr_cells[0].width = Inches(2.7)
    hdr_cells[1].width = Inches(4.2)
    
    headers = [
        "ELEMENTO Y DEFINICIÓN CONCEPTUAL\n(Buenas Prácticas de Ingeniería)",
        "ANÁLISIS E IDEA APLICADA AL PROYECTO\n(Monchis Café: Plataforma Web Segura)"
    ]
    
    for i, title in enumerate(headers):
        cell = hdr_cells[i]
        set_cell_background(cell, "1F4E79")
        set_cell_margins(cell, top=160, bottom=160, left=160, right=160)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(title)
        run.font.name = "Calibri"
        run.font.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(255, 255, 255)

    # 8 Items Data
    items = [
        {
            "num": "2.1",
            "title": "Refinamiento del análisis y las estimaciones",
            "definition": (
                "Proceso iterativo dentro de marcos ágiles (Scrum/Kanban) en el cual los requerimientos del producto "
                "(historias de usuario, criterios de aceptación, dependencias técnicas y requerimientos no funcionales) "
                "se desglosan, clarifican y reevalúan continuamente.\n\n"
                "Su objetivo es mitigar la incertidumbre técnica y de negocio, permitiendo recalibrar las estimaciones "
                "de esfuerzo, costo y cronograma (mediante Story Points, Planning Poker o T-shirt Sizing) antes de comprometer "
                "los ítems a un Sprint de desarrollo."
            ),
            "applied": (
                "• Épica Focal: Transacciones Distribuidas en el Punto de Venta (POS).\n"
                "• Refinamiento Aplicado: La historia inicial de 'Cobro y Reversa' presentaba alta incertidumbre. Se refinó "
                "dividiéndola en tres historias de usuario atómicas con criterios de aceptación en formato Given-When-Then:\n"
                "  1) Encolamiento de eventos de venta en RabbitMQ.\n"
                "  2) Orquestación del Patrón Saga para reversas automáticas si se agotan los granos de café orgánico.\n"
                "  3) Rutina de reintentos exponenciales y Dead Letter Queue (DLQ).\n"
                "• Estimación: Se redujo la dispersión de estimación de 13 a 3 Story Points por ítem, garantizando entregables "
                "medibles y verificables en cada iteración del monorepo."
            )
        },
        {
            "num": "2.2",
            "title": "Refinamiento de capas y de base de datos",
            "definition": (
                "Optimización y formalización de la arquitectura multicapa (presentación, lógica de negocio, servicios "
                "y persistencia) junto con el modelado del esquema de la base de datos relacional/no relacional.\n\n"
                "Comprende la normalización estratégica (3FN) frente a la desnormalización para lectura rápida, definición "
                "de índices compuestos, llaves foráneas, integridad referencial, transaccionalidad ACID y aislamiento, "
                "evitando cuellos de botella y acoplamiento perjudicial entre subsistemas."
            ),
            "applied": (
                "• Base de Datos (PostgreSQL + Prisma ORM):\n"
                "  - Refinamiento de esquema: Se aisló el catálogo comercial del orgánico creando la entidad específica "
                "`LoteOrganico` vinculada a `Producto`, con índices en `fecha_caducidad`, `finca_origen` y `numero_lote` "
                "para agilizar búsquedas de trazabilidad y alertas de merma.\n"
                "  - Concurrencia POS: Implementación de transacciones con bloqueo pesimista/optimista al descontar inventario en caja.\n"
                "• Refinamiento de Capas:\n"
                "  - Desacoplamiento estricto: Capa de Presentación (Vue 3/Pinia) se comunica exclusivamente con la Capa de APIs "
                "(Next.js Routes) mediante DTOs tipados. Se incorporó una capa de eventos intermediaria gobernada por RabbitMQ "
                "para evitar que caídas de red bloqueen el checkout presencial."
            )
        },
        {
            "num": "2.3",
            "title": "Diseño de interfaces",
            "definition": (
                "Fase de ingeniería de software orientada a la experiencia del usuario (UX) y el diseño visual (UI), "
                "garantizando accesibilidad (normas WCAG 2.1), consistencia estética, ergonomía cognitiva y respuesta ágil.\n\n"
                "Abarca la elaboración de flujos de interacción, prototipos de baja y alta fidelidad (wireframes en Figma) "
                "y la consolidación de un Sistema de Diseño (Design System) con tokens de diseño (colores, espaciados, "
                "tipografías y componentes reutilizables)."
            ),
            "applied": (
                "• Design System 'Monchis Warm Pastel':\n"
                "  - Paleta cromática: Tonos café espresso (#4A2C11), crema suave (#FDFBF7), acentos terracota y verde matcha "
                "(#4D7C0F) distintivo para certificar visualmente los productos orgánicos.\n"
                "  - Tipografía moderna: Combinación de Outfit (encabezados cálidos) e Inter (cuerpo de texto de alta legibilidad).\n"
                "• Ergonomía por Perfil:\n"
                "  - Interfaz POS (Cajero): Optimizada para interacción táctil rápida, botones amplios, selector de métodos de pago mixtos "
                "(efectivo, tarjeta, SPEI, puntos Monchis) y respuesta táctil inmediata.\n"
                "  - Tienda Web y Monchis Rewards: Tarjetas de sellos digitales dinámicos (8vo café gratis) y barra de progreso de lealtad "
                "totalmente responsiva en móviles."
            )
        },
        {
            "num": "2.4",
            "title": "Programación de las capas",
            "definition": (
                "Materialización del código fuente estructurado bajo el Principio de Separación de Responsabilidades (SoC) "
                "y patrones de arquitectura (Layered Architecture, Clean Architecture, Repository Pattern).\n\n"
                "Cada capa encapsula una preocupación única: presentación (interacción y UI), aplicación/negocio "
                "(reglas de dominio, cálculos, validaciones) e infraestructura/persistencia (conexión a BD, APIs externas, brokers), "
                "comunicándose mediante interfaces y contratos de datos bien definidos."
            ),
            "applied": (
                "• Monchis Café Monorepo (TypeScript E2E):\n"
                "  1. Capa de Presentación (`apps/web`): Vistas y componentes en Vue 3 con Composition API (`<script setup>`) "
                "y stores reactivos de Pinia (`useCartStore`, `useAuthStore`, `usePosStore`).\n"
                "  2. Capa de Aplicación (`apps/api`): Handlers en Next.js API Routes que orquestan casos de uso: cálculo de cashback "
                "($1 por cada $10 MXN), aplicación de bonificación ecológica por termo reutilizable (ODS 12) y validación de roles RBAC.\n"
                "  3. Capa de Infraestructura / Mensajería: Publicadores y consumidores en Node.js que envían eventos "
                "`order.completed` hacia el Exchange de RabbitMQ.\n"
                "  4. Capa de Persistencia: Repositorios tipados utilizando Prisma Client contra PostgreSQL, garantizando cero SQL injection."
            )
        },
        {
            "num": "2.5",
            "title": "Consideraciones técnicas",
            "definition": (
                "Conjunto de restricciones, parámetros no funcionales y decisiones de infraestructura que condicionan la robustez, "
                "seguridad, disponibilidad, rendimiento y escalabilidad del software.\n\n"
                "Incluye políticas de seguridad (CORS, CSP, mitigación de OWASP Top 10), mecanismos de autenticación y autorización, "
                "gestión de fallos, tolerancia a particiones de red, latencia, auditoría y cumplimiento normativo de privacidad de datos."
            ),
            "applied": (
                "• Seguridad Robusta:\n"
                "  - Autenticación Stateless: JWT de corta duración (15 min) en memoria + Refresh Token (7 días) en cookie segura "
                "`httpOnly, Secure, SameSite=Strict` con rotación automática.\n"
                "  - Protección Anti-Bot: Integración obligatoria de Google reCAPTCHA v2/v3 en login, registro y checkout.\n"
                "  - Cero Hardcoding: Cifrado y gestión estricta de variables de entorno (`.env`) en backend y Docker.\n"
                "• Tolerancia a Fallos y Resiliencia:\n"
                "  - Manejo de caídas en RabbitMQ mediante colas de mensajes fallidos (Dead Letter Queue - DLQ) y reintentos escalonados "
                "(10s, 60s, 300s) con alerta SMTP automática al administrador.\n"
                "• Rendimiento: Prerenderizado estático con `vite-ssg` para catálogo público asegurando tiempos de carga < 1 segundo."
            )
        },
        {
            "num": "2.6",
            "title": "Estructura y componentes de las aplicaciones",
            "definition": (
                "Organización lógica y física del árbol del proyecto, jerarquía de directorios, empaquetado de dependencias "
                "y descomposición del sistema en componentes autónomos, cohesivos y con bajo acoplamiento.\n\n"
                "Fomenta la reutilización de código, la mantenibilidad modular, el mantenimiento independiente de módulos "
                "y la consistencia entre los diferentes subsistemas de una organización."
            ),
            "applied": (
                "• Arquitectura Monorepo con PNPM Workspaces y Turborepo:\n"
                "  ├── `apps/web`: Cliente frontend en Vue 3 + Vite + Tailwind/CSS.\n"
                "  ├── `apps/api`: Servidor backend y rutas API en Next.js.\n"
                "  ├── `packages/ui`: Librería interna de componentes visuales compartidos (botones, modales, badges de caducidad, tablas).\n"
                "  ├── `packages/shared`: Modelos de dominio, validadores Zod y tipos TypeScript compartidos para lograr seguridad de tipos "
                "End-to-End sin duplicidad de definiciones.\n"
                "• Modularización Interna: Cada app divide sus dominios en: `auth`, `pos`, `inventario`, `fidelizacion` y `admin`."
            )
        },
        {
            "num": "2.7",
            "title": "Mapas de sitio",
            "definition": (
                "Representación gráfica y jerárquica de la arquitectura de información y las rutas de navegación de una aplicación web.\n\n"
                "Define la relación entre páginas, niveles de profundidad, control de acceso por roles (público vs. restringido) "
                "y proporciona el plano para el diseño del menú de navegación, rutas del cliente (routers) y el archivo formal "
                "`sitemap.xml` para optimización en motores de búsqueda (SEO)."
            ),
            "applied": (
                "• Árbol de Rutas y Accesos en Monchis Café:\n"
                "  1. Zona Pública (SEO Indexable con `sitemap.xml`):\n"
                "     - `/` (Home / Historia y ODS) ➔ `/menu` (Catálogo orgánico y comercial) ➔ `/origen` (Trazabilidad de fincas) ➔ "
                "`/rewards` (Programa Monchis Rewards) ➔ `/auth/login` y `/auth/registro`.\n"
                "  2. Zona Operativa POS (Acceso Rol 'Cajero' y 'Admin'):\n"
                "     - `/pos` (Caja principal) ➔ `/pos/cobro` (Modal de pago mixto y canje) ➔ `/pos/historial` (Cierre de turno y arqueo).\n"
                "  3. Zona Administrativa (Acceso exclusivo 'Admin' con 2FA):\n"
                "     - `/admin` (Dashboard de métricas) ➔ `/admin/inventario` (Gestión de lotes y alertas de caducidad) ➔ "
                "`/admin/marketing` (Reporte de atribución de tráfico: Google Maps vs. Instagram vs. Tráfico Directo) ➔ `/admin/auditoria`."
            )
        },
        {
            "num": "2.8",
            "title": "Prácticas de calidad",
            "definition": (
                "Metodologías, estándares y disciplinas de ingeniería aplicadas durante todo el ciclo de desarrollo para garantizar "
                "que el software sea correcto, seguro, mantenible, eficiente y cumpla las expectativas del usuario.\n\n"
                "Abarca el Desarrollo Guiado por Pruebas (TDD), testing automatizado piramidal (unitarias, integración, E2E), "
                "análisis estático de código (linters, sonar), integración y entrega continua (CI/CD) y revisiones colaborativas de código."
            ),
            "applied": (
                "• Calidad y Testing Multicapa en Monchis Café:\n"
                "  - Metodología TDD: Implementación de pruebas previas a la lógica para el cálculo de recompensas y reembolsos Saga.\n"
                "  - Pirámide de Pruebas: Vitest para pruebas unitarias de utilitarios y componentes Vue; Supertest para endpoints API; "
                "y Playwright para pruebas E2E del flujo crítico de venta en el POS.\n"
                "  - Linters y Git Hooks: ESLint y Prettier orquestados mediante Husky y `lint-staged`, bloqueando commits con advertencias, "
                "código muerto o strings con datos sensibles hardcodeados.\n"
                "  - Pipeline CI/CD en GitHub Actions: Validación automática de build, tipado TypeScript (`tsc --noEmit`), ejecución de pruebas "
                "y auditoría de vulnerabilidades en dependencias (`pnpm audit`) en cada Pull Request."
            )
        }
    ]

    for idx, item in enumerate(items):
        row = table.add_row()
        cells = row.cells
        cells[0].width = Inches(2.7)
        cells[1].width = Inches(4.2)
        
        bg_color = "FBFBFD" if idx % 2 == 0 else "FFFFFF"
        set_cell_background(cells[0], bg_color)
        set_cell_background(cells[1], bg_color)
        
        set_cell_margins(cells[0], top=120, bottom=120, left=140, right=140)
        set_cell_margins(cells[1], top=120, bottom=120, left=140, right=140)
        
        # Columna 1: Definición
        p1 = cells[0].paragraphs[0]
        p1.paragraph_format.space_after = Pt(4)
        p1.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        run_num = p1.add_run(f"{item['num']} {item['title']}\n")
        run_num.font.name = "Calibri"
        run_num.font.bold = True
        run_num.font.size = Pt(10.5)
        run_num.font.color.rgb = RGBColor(31, 78, 121)
        
        run_def = p1.add_run(item['definition'])
        run_def.font.name = "Calibri"
        run_def.font.size = Pt(9.5)
        run_def.font.color.rgb = RGBColor(50, 50, 50)
        
        # Columna 2: Aplicación
        p2 = cells[1].paragraphs[0]
        p2.paragraph_format.space_after = Pt(4)
        p2.paragraph_format.line_spacing = 1.15
        p2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        run_app_lbl = p2.add_run(f"Aplicación al Sistema Monchis Café:\n")
        run_app_lbl.font.name = "Calibri"
        run_app_lbl.font.bold = True
        run_app_lbl.font.size = Pt(9.5)
        run_app_lbl.font.color.rgb = RGBColor(70, 70, 70)
        
        run_app = p2.add_run(item['applied'])
        run_app.font.name = "Calibri"
        run_app.font.size = Pt(9.5)
        run_app.font.color.rgb = RGBColor(40, 40, 40)

    # Post-table Conclusion / Quality Reflections
    p_c_title = doc.add_paragraph()
    p_c_title.paragraph_format.space_before = Pt(18)
    p_c_title.paragraph_format.space_after = Pt(6)
    r_ct = p_c_title.add_run("Conclusión y Reflexión sobre la Calidad en el Software")
    r_ct.font.name = "Calibri"
    r_ct.font.bold = True
    r_ct.font.size = Pt(12)
    r_ct.font.color.rgb = RGBColor(31, 78, 121)

    p_conc = doc.add_paragraph()
    p_conc.paragraph_format.space_after = Pt(8)
    p_conc.paragraph_format.line_spacing = 1.15
    p_conc.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_conc = p_conc.add_run(
        "La integración sinérgica de los ocho puntos analizados demuestra que la calidad no es una etapa aislada ni una prueba "
        "final previa a la entrega, sino una disciplina continua y transversal. Desde el refinamiento inicial de requerimientos "
        "y estimaciones, pasando por el diseño desacoplado en capas, hasta la aplicación de prácticas defensivas de seguridad, "
        "diseño de interfaces accesibles y pruebas automatizadas (TDD y testing multicapa), cada decisión impacta directamente "
        "en la confiabilidad y mantenibilidad del sistema. En el caso particular de "
    )
    r_conc_p = p_conc.add_run("Monchis Café")
    r_conc_p.font.bold = True
    p_conc.add_run(
        ", este enfoque garantiza la integridad de los datos en ventas concurrentes, protege la plataforma frente a ataques web "
        "y asegura una experiencia óptima tanto para los cajeros en el punto de venta como para los clientes de café orgánico y de especialidad."
    )

    # Save documents
    output_dir = r"d:\ernestofm\Proyecto\docs\metodologia"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, "Actividad_Participacion_Buenas_Practicas_Calidad.docx")
    doc.save(filename)
    print(f"Document successfully created at: {filename}")

if __name__ == "__main__":
    create_document()
