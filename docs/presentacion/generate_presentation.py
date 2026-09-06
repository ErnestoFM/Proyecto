import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def create_deck(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # completely blank layout

    # Colores sobrios y profesionales
    NAVY = RGBColor(27, 54, 93)      # #1B365D Primario
    TEAL = RGBColor(0, 128, 128)     # #008080 Acento
    DARK = RGBColor(33, 37, 41)      # #212529 Texto principal
    MUTED = RGBColor(108, 117, 125)  # #6C757D Secundario
    LIGHT_BG = RGBColor(245, 247, 250)

    def add_header(slide, title_text, category_text="PRODUCTO INTEGRADOR — ADMINISTRACIÓN DE PROYECTOS"):
        # Categoría superior
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.name = "Calibri"
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = TEAL

        # Título principal
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY

    def set_speaker_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = notes_text

    # -------------------------------------------------------------
    # SLIDE 1: PORTADA
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    box1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.5))
    tf1 = box1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "PRODUCTO INTEGRADOR: AVANCE DE PROYECTO"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEAL
    
    p2 = tf1.add_paragraph()
    p2.text = "Monchis Café: Plataforma Web Segura para Cafetería Orgánica y Comercial"
    p2.font.name = "Calibri"
    p2.font.size = Pt(30)
    p2.font.bold = True
    p2.font.color.rgb = NAVY
    p2.space_before = Pt(15)

    p3 = tf1.add_paragraph()
    p3.text = "Planificación Estratégica, Plan Operativo, Estimación COCOMO y Arquitectura de Software Alineada a los ODS"
    p3.font.name = "Calibri"
    p3.font.size = Pt(16)
    p3.font.color.rgb = MUTED
    p3.space_before = Pt(10)

    p4 = tf1.add_paragraph()
    p4.text = "Materia: Unidad 1. Administración de Proyectos  |  Docente: Dr. Gabriel Navarro Salcedo\nAutor y Líder de Proyecto: Ernesto Fierro  |  Fecha: Septiembre 2026"
    p4.font.name = "Calibri"
    p4.font.size = Pt(13)
    p4.font.bold = True
    p4.font.color.rgb = DARK
    p4.space_before = Pt(35)

    set_speaker_notes(s1, 
        "DEFENSA ORAL (Minuto 0:00 - 0:45):\n"
        "Buenos días, profesor Gabriel Navarro y compañeros. Presento el avance del Producto Integrador titulado: "
        "'Monchis Café: Plataforma Web Segura para Cafetería Orgánica y Comercial'. "
        "En este proyecto abordamos la ingeniería de software no solo como una solución técnica, sino como un proyecto "
        "integral de gestión, aplicando rigurosamente los marcos estratégicos, operativos, estimación formal por COCOMO "
        "y metodologías ágiles SCRUM, alineados a la Agenda 2030 de la ONU."
    )

    # -------------------------------------------------------------
    # SLIDE 2: INTRODUCCIÓN - PROPÓSITO Y ALINEACIÓN ODS
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. Introducción: Propósito del Sistema y Marco ODS (Agenda 2030)")
    
    box2 = s2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf2 = box2.text_frame
    tf2.word_wrap = True

    items2 = [
        ("Propósito Central del Software:", 
         "Desarrollar una plataforma integral y resiliente que resuelva los cuellos de botella operativos en mostrador (POS), garantice la trazabilidad del café orgánico de especialidad y fidelice a los clientes mediante incentivos ecológicos."),
        ("ODS 8: Trabajo Decente y Crecimiento Económico (Metas 8.2 y 8.3):", 
         "Formaliza las operaciones de la cafetería y cooperativas cafetaleras de Chiapas/Oaxaca, agiliza los cobros en barra reduciendo el estrés laboral del barista y elimina pérdidas por errores de caja."),
        ("ODS 9: Industria, Innovación e Infraestructura (Metas 9.4 y 9.c):", 
         "Infraestructura cloud basada en monorepo de alto rendimiento (Turborepo), colas RabbitMQ con patrón Saga para consistencia de transacciones y principios de Green Software Engineering (menor consumo de CPU/servidores con SSG)."),
        ("ODS 12: Producción y Consumo Responsables (Metas 12.2, 12.5 y 12.8):", 
         "Sistema 'Monchis Rewards' que bonifica el uso de termos reutilizables (reduciendo más de 4,500 vasos desechables semestrales) y control PEPS de caducidades para evitar desperdicio de insumos."),
        ("ODS 16: Paz, Justicia e Instituciones Sólidas (Metas 16.5 y 16.6):", 
         "Transparencia transaccional absoluta, auditoría inmutable en base de datos y seguridad estricta stateless (JWT + reCAPTCHA) protegiendo la privacidad ciudadana sin brechas de datos.")
    ]
    for idx, (head, desc) in enumerate(items2):
        p = tf2.add_paragraph() if idx > 0 else tf2.paragraphs[0]
        p.text = f"• {head} "
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = NAVY
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK

    set_speaker_notes(s2, 
        "DEFENSA ORAL (Minuto 0:45 - 1:30):\n"
        "El propósito de Monchis Café es conectar la rentabilidad de una cafetería artesanal con la sustentabilidad real. "
        "No seleccionamos los ODS al azar; cada uno impacta la arquitectura: el ODS 8 agiliza el POS y formaliza el comercio justo; "
        "el ODS 9 introduce ingeniería de software verde y microservicios orientados a eventos; el ODS 12 ataca directamente el desperdicio "
        "con incentivos para vasos reutilizables; y el ODS 16 garantiza transparencia contable y ciberseguridad con autenticación sin estado."
    )

    # -------------------------------------------------------------
    # SLIDE 3: INTRODUCCIÓN - ALCANCE DEL SISTEMA (IN-SCOPE VS OUT-OF-SCOPE)
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "2. Introducción: Alcance del Sistema y Priorización MoSCoW")

    # Dos columnas: In-Scope y Out-of-Scope
    box3_l = s3.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tf3_l = box3_l.text_frame
    tf3_l.word_wrap = True
    p = tf3_l.paragraphs[0]
    p.text = "DENTRO DEL ALCANCE (IN-SCOPE) — FASE 1"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = NAVY

    in_scope = [
        "Arquitectura Monorepo modular (Vue 3 + Next.js API + Prisma).",
        "Punto de Venta (POS) web táctil optimizado para barra.",
        "Módulo de cobro mixto: Efectivo (cálculo de cambio), tarjeta, SPEI y puntos.",
        "Resiliencia de transacciones: Patrón Saga con colas RabbitMQ y reversas automáticas.",
        "Módulo 'Monchis Rewards' con sellos digitales y bono ecológico por termo.",
        "Trazabilidad de lotes orgánicos (finca, altura, tueste y caducidad PEPS).",
        "Panel de administración con atribución de marketing UTM (Google Maps vs Instagram).",
        "Prerenderizado SEO con vite-ssg y esquemas estructurados Schema.org."
    ]
    for item in in_scope:
        pi = tf3_l.add_paragraph()
        pi.text = f"✓ {item}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = DARK
        pi.space_before = Pt(6)

    box3_r = s3.shapes.add_textbox(Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tf3_r = box3_r.text_frame
    tf3_r.word_wrap = True
    p_r = tf3_r.paragraphs[0]
    p_r.text = "FUERA DEL ALCANCE (OUT-OF-SCOPE) — POSTERGADO"
    p_r.font.bold = True
    p_r.font.size = Pt(14)
    p_r.font.color.rgb = TEAL

    out_scope = [
        "Facturación electrónica oficial ante el SAT (CFDI 4.0) — Planificada para Fase 2.",
        "Desarrollo de aplicaciones móviles nativas iOS/Android (se opera como PWA/Web responsive).",
        "Integración con flotillas de reparto de terceros tipo Uber Eats / Rappi.",
        "Hardware POS propietario bespoke (se utiliza tablet comercial estándar de 10.5\").",
        "Sensores IoT integrados en tolvas de molienda en tiempo real.",
        "Pasarelas de cobro con criptoactivos."
    ]
    for item in out_scope:
        pi = tf3_r.add_paragraph()
        pi.text = f"✗ {item}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = MUTED
        pi.space_before = Pt(6)

    set_speaker_notes(s3, 
        "DEFENSA ORAL (Minuto 1:30 - 2:15):\n"
        "Para garantizar el éxito de un proyecto de 16 semanas, delimitamos estrictamente las fronteras del sistema bajo la técnica MoSCoW. "
        "En el alcance obligatorio incluimos el POS táctil, pagos mixtos, el patrón Saga para evitar pérdidas de inventario y la trazabilidad de lotes. "
        "Dejamos formalmente fuera de esta fase elementos que introducirían riesgo innecesario, como la facturación CFDI o apps móviles nativas, "
        "enfocando el 100% de la energía en la estabilidad y adopción en el punto de venta."
    )

    # -------------------------------------------------------------
    # SLIDE 4: POSICIONAMIENTO - OPORTUNIDAD Y PLANTEAMIENTO DEL PROBLEMA
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "3. Posicionamiento: Planteamiento del Problema y Oportunidad")

    box4_l = s4.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tf4_l = box4_l.text_frame
    tf4_l.word_wrap = True
    p = tf4_l.paragraphs[0]
    p.text = "PLANTEAMIENTO DEL PROBLEMA"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = NAVY

    problems = [
        ("Ineficiencia y Errores en Barra:", "Tiempos de cobro superiores a 2.5 minutos en horas pico y descuadres continuos en arqueo de caja por falta de control de pagos mixtos."),
        ("Pérdida Económica por Mermas:", "El café de especialidad pierde frescura a los 21-30 días; sin trazabilidad PEPS automatizada, se generan mermas de insumos de alto costo."),
        ("Impacto Ambiental No Mitigado:", "Uso desmedido de vasos plásticos y cartón plastificado de un solo uso por falta de un sistema digital de incentivos al cliente."),
        ("Opacidad con Productores:", "Falta de visibilidad de las cooperativas agrícolas regionales de Chiapas y Oaxaca en la experiencia final del consumidor.")
    ]
    for head, desc in problems:
        pi = tf4_l.add_paragraph()
        pi.text = f"• {head} "
        pi.font.bold = True
        pi.font.size = Pt(11)
        pi.font.color.rgb = DARK
        pi.space_before = Pt(8)
        run = pi.add_run()
        run.text = desc
        run.font.bold = False

    box4_r = s4.shapes.add_textbox(Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tf4_r = box4_r.text_frame
    tf4_r.word_wrap = True
    p_r = tf4_r.paragraphs[0]
    p_r.text = "OPORTUNIDAD DE NEGOCIO Y PROPUESTA DE VALOR"
    p_r.font.bold = True
    p_r.font.size = Pt(14)
    p_r.font.color.rgb = TEAL

    opps = [
        ("Mercado de Café Consciente en Auge:", "Incremento anual del 18% en la preferencia de consumidores por cafeterías con trazabilidad ética y prácticas ecológicas verificables."),
        ("Digitalización Ágil y de Bajo Costo:", "Sustitución de costosos sistemas POS tradicionales de renta mensual por una solución web moderna, rápida y personalizada."),
        ("Fidelización Directa 'Eco-Friendly':", "Monchis Rewards convierte el hábito de llevar termo en descuentos automáticos y cashback digital, reteniendo al cliente local."),
        ("Atribución de Marketing Geolocalizado:", "Identificación de si el cliente llega por recomendación en Google Maps o Instagram para enfocar la inversión publicitaria.")
    ]
    for head, desc in opps:
        pi = tf4_r.add_paragraph()
        pi.text = f"• {head} "
        pi.font.bold = True
        pi.font.size = Pt(11)
        pi.font.color.rgb = DARK
        pi.space_before = Pt(8)
        run = pi.add_run()
        run.text = desc
        run.font.bold = False

    set_speaker_notes(s4, 
        "DEFENSA ORAL (Minuto 2:15 - 3:00):\n"
        "En el posicionamiento observamos una realidad crítica: las cafeterías artesanales sufren lentitud en el cobro, descuadres contables "
        "y mermas por café vencido en bodega. Monchis Café capitaliza la oportunidad: un nicho de clientes eco-conscientes que valoran el comercio justo. "
        "Nuestra propuesta no es solo cobrar café, sino fidelizar a través del impacto ecológico y la optimización de los márgenes del negocio."
    )

    # -------------------------------------------------------------
    # SLIDE 5: PLANEACIÓN ESTRATÉGICA - IDENTIDAD Y BALANCED SCORECARD
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "4. Planeación Estratégica: Identidad y Balanced Scorecard")

    box5 = s5.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf5 = box5.text_frame
    tf5.word_wrap = True

    p = tf5.paragraphs[0]
    p.text = "Misión: Brindar una experiencia gastronómica de café de especialidad superior, apalancada en tecnología limpia que certifique el origen ético del grano y erradique el desperdicio de insumos en beneficio de nuestra comunidad y el medio ambiente."
    p.font.size = Pt(11)
    p.font.italic = True
    p.font.color.rgb = DARK

    p_v = tf5.add_paragraph()
    p_v.text = "Visión: Convertirnos para 2028 en la cadena de cafeterías artesanales líder regional en transformación digital sostenible, siendo un modelo replicable de economía circular y Green IT en el sector restaurantero."
    p_v.font.size = Pt(11)
    p_v.font.italic = True
    p_v.font.color.rgb = DARK
    p_v.space_before = Pt(6)

    p_bsc = tf5.add_paragraph()
    p_bsc.text = "MAPA ESTRATÉGICO DE CUATRO PERSPECTIVAS (BALANCED SCORECARD):"
    p_bsc.font.bold = True
    p_bsc.font.size = Pt(12)
    p_bsc.font.color.rgb = NAVY
    p_bsc.space_before = Pt(14)

    bsc_items = [
        ("Perspectiva Financiera & Sostenible (ODS 8 y 12):", "Maximizar el margen bruto reduciendo mermas a <1.5% y disminuyendo el costo operativo de empaques desechables."),
        ("Perspectiva del Cliente (ODS 12 y 16):", "Reducir el tiempo de espera en mostrador a <30 segundos y visibilizar la historia de los productores en cada ticket digital."),
        ("Perspectiva de Procesos Internos (ODS 9 y 16):", "Cero discrepancias contables gracias al Patrón Saga con RabbitMQ y política PEPS automática en el inventario."),
        ("Perspectiva de Aprendizaje y Crecimiento (ODS 8 y 9):", "Adopción de estándares de ingeniería de software moderna (TDD, Monorepo, CI/CD) y cultura ágil de alta eficiencia.")
    ]
    for cat, det in bsc_items:
        pi = tf5.add_paragraph()
        pi.text = f"• {cat} "
        pi.font.bold = True
        pi.font.size = Pt(11)
        pi.font.color.rgb = TEAL
        pi.space_before = Pt(6)
        run = pi.add_run()
        run.text = det
        run.font.bold = False
        run.font.color.rgb = DARK

    set_speaker_notes(s5, 
        "DEFENSA ORAL (Minuto 3:00 - 3:45):\n"
        "El plan estratégico se diseñó bajo el Cuadro de Mando Integral (Balanced Scorecard). Alineamos la causa y efecto: "
        "capacitamos al equipo en procesos internos robustos (como el patrón Saga), lo que optimiza los tiempos y la experiencia del cliente, "
        "traduciéndose directamente en rentabilidad financiera y menor huella ecológica."
    )

    # -------------------------------------------------------------
    # SLIDE 6: PLANEACIÓN ESTRATÉGICA - MATRIZ DOFA
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "5. Planeación Estratégica: Matriz DOFA (Diagnóstico Interno y Externo)")

    # Tabla 2x2 para DOFA
    table_shape = s6.shapes.add_table(3, 2, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.0))
    table = table_shape.table
    table.columns[0].width = Inches(5.8)
    table.columns[1].width = Inches(5.9)

    table.cell(0, 0).text = "FACTORES INTERNOS"
    table.cell(0, 1).text = "FACTORES EXTERNOS"
    for c in [table.cell(0, 0), table.cell(0, 1)]:
        c.fill.solid()
        c.fill.fore_color.rgb = NAVY
        p = c.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.font.size = Pt(11)

    table.cell(1, 0).text = "FORTALEZAS (F)\n• F1: Arquitectura desacoplada (Monorepo Turborepo + Vue 3 + Next.js).\n• F2: Resiliencia transaccional con Patrón Saga y colas RabbitMQ.\n• F3: Propuesta ODS diferenciada (trazabilidad y bono ecológico).\n• F4: Ciberseguridad por diseño (autenticación stateless JWT + reCAPTCHA)."
    table.cell(1, 1).text = "OPORTUNIDADES (O)\n• O1: Creciente demanda comunitaria de café sustentable y comercio justo.\n• O2: Vacío tecnológico en soluciones accesibles para cafeterías artesanales.\n• O3: Canales de captación geolocalizados gratuitos (Google Maps / Instagram).\n• O4: Acceso a estímulos de emprendimiento verde y sustentabilidad."

    table.cell(2, 0).text = "DEBILIDADES (D)\n• D1: Complejidad técnica inicial en infraestructura distribuida.\n• D2: Curva de aprendizaje del personal de barra en lectura de códigos y POS.\n• D3: Equipo de desarrollo compacto que exige priorización rigurosa."
    table.cell(2, 1).text = "AMENAZAS (A)\n• A1: Intermitencia de conectividad a internet en la zona de la cafetería.\n• A2: Competencia de franquicias corporativas con apps y monederos masivos.\n• A3: Inflación en precios de insumos agrícolas y grano de especialidad.\n• A4: Ataques automatizados y fraude transaccional en pasarelas web."

    for row_idx in [1, 2]:
        for col_idx in [0, 1]:
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(9.5)
                p.font.color.rgb = DARK

    set_speaker_notes(s6, 
        "DEFENSA ORAL (Minuto 3:45 - 4:10):\n"
        "En la matriz DOFA identificamos con realismo los 4 cuadrantes. "
        "Internamente nos fortalecen la arquitectura monorepo resiliente con el Patrón Saga y la seguridad stateless. "
        "En el entorno externo, aprovechamos la creciente conciencia de consumo responsable de café. "
        "Reconocemos la debilidad de la infraestructura distribuida y la amenaza de intermitencia de internet, "
        "lo que nos lleva directamente a formular los 4 cruces estratégicos que veremos a continuación."
    )

    # -------------------------------------------------------------
    # SLIDE 7: PLANEACIÓN ESTRATÉGICA - MATRIZ DE CRUCES (FO, DO, FA, DA)
    # -------------------------------------------------------------
    s7_cross = prs.slides.add_slide(blank_layout)
    add_header(s7_cross, "6. Planeación Estratégica: Matriz de Cruces Estratégicos (FO, DO, FA, DA)")

    # Tabla 2x2 para los 4 cuadrantes de cruce
    table_cross_shape = s7_cross.shapes.add_table(2, 2, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tc = table_cross_shape.table
    tc.columns[0].width = Inches(5.8)
    tc.columns[1].width = Inches(5.9)

    # Cuadrante FO (Maxi-Maxi)
    c_fo = tc.cell(0, 0)
    c_fo.fill.solid()
    c_fo.fill.fore_color.rgb = LIGHT_BG
    tf_fo = c_fo.text_frame
    tf_fo.word_wrap = True
    p = tf_fo.paragraphs[0]
    p.text = "ESTRATEGIAS FO (Maxi-Maxi): Usar Fortalezas para aprovechar Oportunidades"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = NAVY
    p_desc = tf_fo.add_paragraph()
    p_desc.text = "• E-FO1 (F3, F5 + O1, O3): Campañas de Marketing Geolocalizado con Trazabilidad ODS.\nLanzar campañas en Instagram y Google Maps destacando el origen de las fincas regionales y el bono de -$5.00 por termo ecológico, midiendo la conversión directa con el panel de atribución UTM."
    p_desc.font.size = Pt(9.5)
    p_desc.font.color.rgb = DARK
    p_desc.space_before = Pt(4)

    # Cuadrante DO (Mini-Maxi)
    c_do = tc.cell(0, 1)
    c_do.fill.solid()
    c_do.fill.fore_color.rgb = LIGHT_BG
    tf_do = c_do.text_frame
    tf_do.word_wrap = True
    p = tf_do.paragraphs[0]
    p.text = "ESTRATEGIAS DO (Mini-Maxi): Superar Debilidades aprovechando Oportunidades"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = TEAL
    p_desc = tf_do.add_paragraph()
    p_desc.text = "• E-DO1 (D2 + O2): Capacitación Acelerada mediante UI Táctil Intuitiva.\nDiseñar interfaces táctiles minimalistas con flujos asistidos en el POS para capacitar a los baristas en menos de 2 horas, posicionando a la cafetería como líder en modernización tecnológica accesible."
    p_desc.font.size = Pt(9.5)
    p_desc.font.color.rgb = DARK
    p_desc.space_before = Pt(4)

    # Cuadrante FA (Maxi-Mini)
    c_fa = tc.cell(1, 0)
    c_fa.fill.solid()
    c_fa.fill.fore_color.rgb = LIGHT_BG
    tf_fa = c_fa.text_frame
    tf_fa.word_wrap = True
    p = tf_fa.paragraphs[0]
    p.text = "ESTRATEGIAS FA (Maxi-Mini): Usar Fortalezas para neutralizar Amenazas"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = TEAL
    p_desc = tf_fa.add_paragraph()
    p_desc.text = "• E-FA1 (F4 + A4): Blindaje de Ciberseguridad Stateless y Anti-Fraude.\nNeutralizar ataques automatizados y fraudes en pasarelas mediante rate limiting en Redis, reCAPTCHA v2/v3 y tokens JWT sin estado, protegiendo las transacciones sin elevar costos de licenciamiento."
    p_desc.font.size = Pt(9.5)
    p_desc.font.color.rgb = DARK
    p_desc.space_before = Pt(4)

    # Cuadrante DA (Mini-Mini)
    c_da = tc.cell(1, 1)
    c_da.fill.solid()
    c_da.fill.fore_color.rgb = LIGHT_BG
    tf_da = c_da.text_frame
    tf_da.word_wrap = True
    p = tf_da.paragraphs[0]
    p.text = "ESTRATEGIAS DA (Mini-Mini): Minimizar Debilidades y eludir Amenazas"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(180, 0, 0)
    p_desc = tf_da.add_paragraph()
    p_desc.text = "• E-DA1 (D1 + A1): Resiliencia Offline en POS con Almacenamiento Local.\nImplementar cola de transacciones en caché del navegador (Pinia / LocalStorage) para que interrupciones momentáneas del internet local no impidan continuar cobrando órdenes en mostrador."
    p_desc.font.size = Pt(9.5)
    p_desc.font.color.rgb = DARK
    p_desc.space_before = Pt(4)

    set_speaker_notes(s7_cross, 
        "DEFENSA ORAL (Minuto 4:10 - 4:40):\n"
        "Aquí presentamos los 4 cruces estratégicos formalizados: "
        "En FO, usamos la trazabilidad y SEO para captar clientes desde Google Maps e Instagram; "
        "en DO, compensamos la falta de experiencia del personal con una UI sumamente intuitiva; "
        "en FA, protegemos la plataforma con seguridad stateless y reCAPTCHA contra fraudes; "
        "y en DA, implementamos persistencia offline en el POS para que una caída de internet no detenga las ventas en barra."
    )

    # -------------------------------------------------------------
    # SLIDE 8: PLANEACIÓN OPERATIVA - CICLO DE 16 SEMANAS Y SPRINTS
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "7. Planeación Operativa: Estructura de Sprints (16 Semanas)")

    table_shape7 = s7.shapes.add_table(9, 4, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    t7 = table_shape7.table
    t7.columns[0].width = Inches(1.5)
    t7.columns[1].width = Inches(2.2)
    t7.columns[2].width = Inches(5.6)
    t7.columns[3].width = Inches(2.4)

    h_titles = ["SPRINT / TIEMPO", "FASE DEL PROYECTO", "OBJETIVO OPERATIVO Y ENTREGABLE CLAVE", "CRITERIO DE ÉXITO"]
    for i, h in enumerate(h_titles):
        cell = t7.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(255, 255, 255)

    sprints_data = [
        ("Sprint 1 (Sem 1-2)", "Fase 1: Infraestructura", "Monorepo Turborepo, esquema Prisma PostgreSQL y Docker local.", "Build en <45s, 0 errores."),
        ("Sprint 2 (Sem 3-4)", "Fase 2: Seguridad Core", "Auth stateless JWT rotativo, RBAC y Google reCAPTCHA v2/v3.", "100% tests unitarios auth."),
        ("Sprint 3 (Sem 5-6)", "Fase 2: Broker & Saga", "Topic Exchange RabbitMQ, colas de retardo y reversas automáticas.", "Compensación en <500ms."),
        ("Sprint 4 (Sem 7-8)", "Fase 3: Frontend & SEO", "Vistas públicas Vue 3, tokens pastel y prerender con vite-ssg.", "Lighthouse SEO = 100/100."),
        ("Sprint 5 (Sem 9-10)", "Fase 4: POS & Cobro", "Interfaz táctil de barra, escaneo QR y soporte de pagos mixtos.", "Registro de venta <15s."),
        ("Sprint 6 (Sem 11-12)", "Fase 4: ODS & Rewards", "Trazabilidad de lotes orgánicos y motor de bonos por termo.", "100% lotes con origen."),
        ("Sprint 7 (Sem 13-14)", "Fase 5 y 6: Admin & QA", "Dashboard analítico UTM, auditoría DLQ y testing Playwright.", "Cobertura de código >85%."),
        ("Sprint 8 (Sem 15-16)", "Fase 7: Cloud & Release", "Despliegue en GCP Cloud Run con Terraform y auditoría OWASP.", "Uptime >99.5%, p95 <250ms.")
    ]
    for row_idx, data in enumerate(sprints_data, start=1):
        for col_idx, text in enumerate(data):
            cell = t7.cell(row_idx, col_idx)
            cell.text = text
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9)
            p.font.color.rgb = DARK
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if row_idx % 2 == 0 else RGBColor(255, 255, 255)

    set_speaker_notes(s7, 
        "DEFENSA ORAL (Minuto 4:20 - 5:00):\n"
        "El plan operativo aterriza la estrategia en 8 sprints quincenales a lo largo de 16 semanas. "
        "Cada sprint tiene un entregable verificable con criterios de aceptación cuantificables (KPIs). "
        "Desde la base de datos en el Sprint 1 hasta el despliegue serverless con Terraform en el Sprint 8, "
        "garantizamos un desarrollo disciplinado con pruebas automatizadas continuas."
    )

    # -------------------------------------------------------------
    # SLIDE 9: ORGANIZACIÓN SCRUM - ROLES Y APLICACIÓN
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "8. Organización: Marco Ágil SCRUM y Asignación de Roles")

    box8_l = s8.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tf8_l = box8_l.text_frame
    tf8_l.word_wrap = True
    p = tf8_l.paragraphs[0]
    p.text = "ROLES DEL EQUIPO SCRUM (ALINEADOS A ODS)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = NAVY

    scrum_roles = [
        ("Product Owner / Stakeholder:", "Define historias de usuario, prioriza el Product Backlog según el retorno de inversión y valida la conformidad con los lineamientos de sustentabilidad ODS."),
        ("Scrum Master (Ernesto Fierro):", "Facilita la disciplina ágil, remueve impedimentos técnicos de CI/CD, vela por un ritmo sostenible de trabajo (ODS 8) y administra el presupuesto."),
        ("Development Team (Full-Stack & DevOps):", "Responsables del incremento de software funcional: arquitectura en contenedores, APIs tipadas en TypeScript, frontend reactivo y orquestación Saga."),
        ("QA & Security Champion:", "Valida la cobertura de pruebas Vitest/Playwright, audita la accesibilidad WCAG y mitiga riesgos del OWASP Top 10 (ODS 16).")
    ]
    for r_title, r_desc in scrum_roles:
        pi = tf8_l.add_paragraph()
        pi.text = f"• {r_title} "
        pi.font.bold = True
        pi.font.size = Pt(10.5)
        pi.font.color.rgb = DARK
        pi.space_before = Pt(8)
        run = pi.add_run()
        run.text = r_desc
        run.font.bold = False

    box8_r = s8.shapes.add_textbox(Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tf8_r = box8_r.text_frame
    tf8_r.word_wrap = True
    p_r = tf8_r.paragraphs[0]
    p_r.text = "¿CÓMO APLICAMOS SCRUM AL PROYECTO?"
    p_r.font.bold = True
    p_r.font.size = Pt(13)
    p_r.font.color.rgb = TEAL

    scrum_events = [
        ("Sprint Planning (Cada 2 semanas):", "Descomposición del Product Backlog en tareas técnicas medibles estimadas con Planning Poker y asignación al Sprint Backlog."),
        ("Daily Standups (15 minutos):", "Sincronización de avances: ¿Qué se logró ayer? ¿Qué se hará hoy? ¿Qué impedimentos técnicos (bloqueos de dependencias/APIs) existen?"),
        ("Sprint Review & Demostración:", "Demostración en vivo del software desplegado en entorno de Staging al final de cada quincena para feedback inmediato."),
        ("Sprint Retrospective:", "Análisis de lecciones aprendidas sobre velocidad de desarrollo, deuda técnica acumulada y mejoras en el pipeline de GitHub Actions.")
    ]
    for e_title, e_desc in scrum_events:
        pi = tf8_r.add_paragraph()
        pi.text = f"• {e_title} "
        pi.font.bold = True
        pi.font.size = Pt(10.5)
        pi.font.color.rgb = DARK
        pi.space_before = Pt(8)
        run = pi.add_run()
        run.text = e_desc
        run.font.bold = False

    set_speaker_notes(s8, 
        "DEFENSA ORAL (Minuto 5:00 - 5:40):\n"
        "La metodología SCRUM organiza el flujo de trabajo en ciclos cortos de entrega de valor continuo. "
        "En mi rol de Scrum Master y desarrollador líder, me aseguro de que el backlog esté priorizado bajo criterios ODS y técnicos. "
        "Realizamos ceremonias formales de planificación quincenal, seguimiento diario de impedimentos y retrospectivas "
        "para garantizar que la deuda técnica se mantenga en cero antes de pasar a la siguiente fase."
    )

    # -------------------------------------------------------------
    # SLIDE 10: PROGRAMACIÓN - GANTT, PERT Y RUTA CRÍTICA (CPM)
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "9. Programación del Proyecto: Diagramas de Gantt y PERT (Ruta Crítica)")

    box9_l = s9.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tf9_l = box9_l.text_frame
    tf9_l.word_wrap = True
    p = tf9_l.paragraphs[0]
    p.text = "DESGLOSE DE ACTIVIDADES PERT / CPM"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = NAVY

    pert_tasks = [
        ("A: Requerimientos y ODS (Sem 1-2)", "Duración: 2 sem | Predecesora: Ninguna"),
        ("B: Arquitectura Monorepo y BD (Sem 2-3)", "Duración: 2 sem | Predecesora: A"),
        ("C: Backend Core y Auth JWT (Sem 4-5)", "Duración: 2 sem | Predecesora: B [RUTA CRÍTICA]"),
        ("D: Broker RabbitMQ y Saga (Sem 6-7)", "Duración: 2 sem | Predecesora: C [RUTA CRÍTICA]"),
        ("E: Frontend Core y vite-ssg (Sem 6-7)", "Duración: 2 sem | Predecesora: B (Holgura: 2 sem)"),
        ("F: Módulo POS y Cobro Mixto (Sem 8-10)", "Duración: 3 sem | Predecesora: D, E [RUTA CRÍTICA]"),
        ("G: Trazabilidad y Fidelización Eco (Sem 11-12)", "Duración: 2 sem | Predecesora: F [RUTA CRÍTICA]"),
        ("H: Dashboard y Analítica UTM (Sem 12-13)", "Duración: 2 sem | Predecesora: F (Holgura: 1 sem)"),
        ("I: Testing Multicapa & QA (Sem 13-14)", "Duración: 2 sem | Predecesora: G, H [RUTA CRÍTICA]"),
        ("J: Despliegue Cloud en GCP (Sem 15-16)", "Duración: 2 sem | Predecesora: I [RUTA CRÍTICA]")
    ]
    for name, det in pert_tasks:
        pi = tf9_l.add_paragraph()
        pi.text = f"• {name}: "
        pi.font.bold = True
        pi.font.size = Pt(9.5)
        pi.font.color.rgb = DARK
        pi.space_before = Pt(3)
        run = pi.add_run()
        run.text = det
        run.font.bold = False
        if "RUTA CRÍTICA" in det:
            run.font.color.rgb = RGBColor(180, 0, 0)
            run.font.bold = True

    box9_r = s9.shapes.add_textbox(Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tf9_r = box9_r.text_frame
    tf9_r.word_wrap = True
    p_r = tf9_r.paragraphs[0]
    p_r.text = "DIAGRAMA DE RED PERT & RUTA CRÍTICA"
    p_r.font.bold = True
    p_r.font.size = Pt(13)
    p_r.font.color.rgb = TEAL

    p_pert = tf9_r.add_paragraph()
    p_pert.text = (
        "Secuencia de la Ruta Crítica (Duración Total: 16 semanas):\n\n"
        "  [Nodo Inicio]\n"
        "        │\n"
        "        ▼\n"
        "     (A: Reqs) ──► (B: Monorepo) ──► (C: Backend Core) ──► (D: RabbitMQ Saga)\n"
        "                                                                │\n"
        "  ┌─────────────────────────────────────────────────────────────┘\n"
        "  ▼\n"
        "(F: POS & Pagos Mixtos) ──► (G: Trazabilidad Eco) ──► (I: Testing QA) ──► (J: GCP Release)\n"
        "                                                                               │\n"
        "                                                                               ▼\n"
        "                                                                          [Proyecto Fin]\n\n"
        "• Holguras Identificadas: La actividad E (Frontend Landing) y H (Dashboard Admin) cuentan con 2 y 1 semana de holgura respectivamente.\n"
        "• Cualquier retraso en las actividades de la Ruta Crítica (C, D, F, G, I, J) compromete directamente la fecha de liberación del 22 de Septiembre."
    )
    p_pert.font.name = "Consolas"
    p_pert.font.size = Pt(9)
    p_pert.font.color.rgb = DARK

    set_speaker_notes(s9, 
        "DEFENSA ORAL (Minuto 5:40 - 6:30):\n"
        "Para la programación formal aplicamos el Método de la Ruta Crítica (CPM) mediante el grafo PERT. "
        "Calculamos tiempos tempranos, tiempos tardíos y holguras. La ruta crítica pasa obligatoriamente por el Backend Core, "
        "el broker de RabbitMQ, el módulo POS y las pruebas de QA. Actividades como el Frontend público o el Dashboard tienen holgura positiva, "
        "lo que permite absorber cualquier contingencia sin impactar el hito final de 16 semanas."
    )

    # -------------------------------------------------------------
    # SLIDE 11: PROGRAMACIÓN - HISTOGRAMA DE RECURSOS
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "10. Programación del Proyecto: Histograma y Distribución de Recursos")

    box10 = s10.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf10 = box10.text_frame
    tf10.word_wrap = True

    p = tf10.paragraphs[0]
    p.text = "DISTRIBUCIÓN DE ESFUERZO SEMANAL POR PERFIL (TOTAL: 2,720 HORAS / PROYECTO)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = NAVY

    res_table = s10.shapes.add_table(6, 6, Inches(0.8), Inches(2.2), Inches(11.7), Inches(4.5))
    t10 = res_table.table
    t10.columns[0].width = Inches(2.7)
    t10.columns[1].width = Inches(1.8)
    t10.columns[2].width = Inches(1.8)
    t10.columns[3].width = Inches(1.8)
    t10.columns[4].width = Inches(1.8)
    t10.columns[5].width = Inches(1.8)

    h10 = ["ROL DEL PROYECTO", "SEM 1 - 4 (INICIO)", "SEM 5 - 8 (CORE)", "SEM 9 - 12 (POS)", "SEM 13 - 16 (QA/PROD)", "TOTAL HORAS"]
    for i, h in enumerate(h10):
        c = t10.cell(0, i)
        c.fill.solid()
        c.fill.fore_color.rgb = NAVY
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = RGBColor(255, 255, 255)

    r_rows = [
        ("Líder de Proyecto / Scrum Master", "80 hrs (20h/sem)", "80 hrs (20h/sem)", "80 hrs (20h/sem)", "80 hrs (20h/sem)", "320 hrs"),
        ("Arquitecto de Software & DevOps", "160 hrs (40h/sem)", "160 hrs (40h/sem)", "160 hrs (40h/sem)", "160 hrs (40h/sem)", "640 hrs"),
        ("Desarrollador Full-Stack Backend", "160 hrs (40h/sem)", "160 hrs (40h/sem)", "160 hrs (40h/sem)", "160 hrs (40h/sem)", "640 hrs"),
        ("Desarrollador Full-Stack Frontend", "160 hrs (40h/sem)", "160 hrs (40h/sem)", "160 hrs (40h/sem)", "160 hrs (40h/sem)", "640 hrs"),
        ("Especialista en QA & Seguridad", "40 hrs (10h/sem)", "120 hrs (30h/sem)", "160 hrs (40h/sem)", "160 hrs (40h/sem)", "480 hrs")
    ]
    for r_idx, row in enumerate(r_rows, start=1):
        for c_idx, val in enumerate(row):
            cell = t10.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9)
            p.font.color.rgb = DARK
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if r_idx % 2 == 0 else RGBColor(255, 255, 255)

    set_speaker_notes(s10, 
        "DEFENSA ORAL (Minuto 6:30 - 7:05):\n"
        "El histograma de recursos asegura que no existan picos de sobreasignación que pongan en riesgo al equipo ni la calidad del software. "
        "Las áreas de arquitectura y desarrollo mantienen una carga regular constante de 40 horas semanales, "
        "mientras que QA incrementa su dedicación de manera progresiva conforme el software madura, alcanzando el 100% de dedicación "
        "en las fases finales de pruebas multicapa y auditoría de ciberseguridad."
    )

    # -------------------------------------------------------------
    # SLIDE 12: ESTIMACIÓN COCOMO - MODELO BÁSICO
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "11. Estimación de Software: Modelo COCOMO Básico")

    box11_l = s11.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tf11_l = box11_l.text_frame
    tf11_l.word_wrap = True
    p = tf11_l.paragraphs[0]
    p.text = "PARÁMETROS Y CLASIFICACIÓN DEL PROYECTO"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = NAVY

    cocomo_basics = [
        ("Tamaño Estimado del Software (SLOC):", "22.5 KLOC (22,500 líneas de código fuente en TypeScript, SQL y templates)."),
        ("Modo de Desarrollo Seleccionado:", "Semiacoplado (Semidetached). Justificación: Es una aplicación web empresarial con restricciones medias de seguridad, colas RabbitMQ y pasarelas de pago mixtas."),
        ("Ecuaciones del Modelo Básico (COCOMO 81):", ""),
        ("• Esfuerzo (Personas-Mes):", "E = a × (KLOC)^b"),
        ("• Tiempo de Desarrollo (Meses):", "TDEV = c × (E)^d"),
        ("• Coeficientes Semiacoplado:", "a = 3.0 | b = 1.12 | c = 2.5 | d = 0.35")
    ]
    for h, d in cocomo_basics:
        pi = tf11_l.add_paragraph()
        pi.text = f"{h} {d}"
        pi.font.size = Pt(11)
        pi.font.color.rgb = DARK
        pi.space_before = Pt(6)

    box11_r = s11.shapes.add_textbox(Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tf11_r = box11_r.text_frame
    tf11_r.word_wrap = True
    p_r = tf11_r.paragraphs[0]
    p_r.text = "CÁLCULO MATEMÁTICO DEL MODELO BÁSICO"
    p_r.font.bold = True
    p_r.font.size = Pt(13)
    p_r.font.color.rgb = TEAL

    calc_steps = (
        "Paso 1: Cálculo del Esfuerzo Nominal\n"
        "  E = 3.0 × (22.5)^1.12\n"
        "  (22.5)^1.12 ≈ 32.511\n"
        "  E = 3.0 × 32.511 = 97.53 Personas-Mes (PM)\n\n"
        "Paso 2: Cálculo del Tiempo de Desarrollo Estimado\n"
        "  TDEV = 2.5 × (97.53)^0.35\n"
        "  (97.53)^0.35 ≈ 4.97 meses\n"
        "  TDEV ≈ 5.0 Meses (aprox. 20 semanas nominales)\n\n"
        "Paso 3: Personal Promedio Requerido\n"
        "  N = E / TDEV = 97.53 / 4.97 ≈ 19.6 Personas nominales\n\n"
        "Paso 4: Productividad Nominal Básica\n"
        "  Prod = KLOC / E = 22,500 / 97.53 ≈ 230 LOC / Persona-Mes\n\n"
        "Observación Crítica: El modelo básico sobrestima el esfuerzo al no considerar el impacto de herramientas modernas (Next.js, Prisma, Turborepo) ni la alta capacidad técnica del equipo. Por ello es indispensable el Modelo Intermedio."
    )
    pi = tf11_r.add_paragraph()
    pi.text = calc_steps
    pi.font.name = "Consolas"
    pi.font.size = Pt(9.5)
    pi.font.color.rgb = DARK

    set_speaker_notes(s11, 
        "DEFENSA ORAL (Minuto 7:05 - 7:50):\n"
        "Aplicamos formalmente el modelo COCOMO 81. Estimamos un tamaño de 22.5 KLOC para todo el monorepo. "
        "En modo Semiacoplado, el modelo básico arroja 97.5 personas-mes y un tiempo de desarrollo teórico de 5 meses. "
        "Sin embargo, como señala la literatura de ingeniería de software, el modelo básico ignora multiplicadores de productividad modernos. "
        "Por eso procedemos a refinarlo con el Modelo COCOMO Intermedio mediante los 15 conductores de costo."
    )

    # -------------------------------------------------------------
    # SLIDE 13: ESTIMACIÓN COCOMO - MODELO INTERMEDIO (15 COST DRIVERS)
    # -------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "12. Estimación de Software: Modelo COCOMO Intermedio (15 Cost Drivers)")

    # Tabla 1 (Izquierda): Producto y Plataforma (7 conductores)
    t1_shape = s12.shapes.add_table(8, 3, Inches(0.8), Inches(1.5), Inches(5.7), Inches(3.0))
    t1 = t1_shape.table
    t1.columns[0].width = Inches(3.2)
    t1.columns[1].width = Inches(1.3)
    t1.columns[2].width = Inches(1.2)

    h_t1 = ["PRODUCTO & PLATAFORMA", "NIVEL", "VALOR"]
    for i, h in enumerate(h_t1):
        c = t1.cell(0, i)
        c.fill.solid()
        c.fill.fore_color.rgb = NAVY
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = RGBColor(255, 255, 255)

    drivers_col1 = [
        ("1. RELY (Confiabilidad requerida)", "Alto", "1.15"),
        ("2. DATA (Tamaño base de datos)", "Nominal", "1.00"),
        ("3. CPLX (Complejidad de software)", "Alto", "1.15"),
        ("4. TIME (Restricción tiempo CPU)", "Nominal", "1.00"),
        ("5. STOR (Restricción de memoria)", "Nominal", "1.00"),
        ("6. VIRT (Volatilidad máquina virtual)", "Bajo", "0.87"),
        ("7. TURN (Tiempo de respuesta comp.)", "Nominal", "1.00"),
    ]
    for r_idx, (cd, niv, val) in enumerate(drivers_col1, start=1):
        for c_idx, text in enumerate([cd, niv, val]):
            cell = t1.cell(r_idx, c_idx)
            cell.text = text
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(8.5)
            if c_idx == 2 and val != "1.00":
                p.font.bold = True
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if r_idx % 2 == 0 else RGBColor(255, 255, 255)

    # Tabla 2 (Derecha): Personal y Proyecto (8 conductores)
    t2_shape = s12.shapes.add_table(9, 3, Inches(6.8), Inches(1.5), Inches(5.7), Inches(3.3))
    t2 = t2_shape.table
    t2.columns[0].width = Inches(3.2)
    t2.columns[1].width = Inches(1.3)
    t2.columns[2].width = Inches(1.2)

    h_t2 = ["PERSONAL & PROYECTO", "NIVEL", "VALOR"]
    for i, h in enumerate(h_t2):
        c = t2.cell(0, i)
        c.fill.solid()
        c.fill.fore_color.rgb = TEAL
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = RGBColor(255, 255, 255)

    drivers_col2 = [
        ("8. ACAP (Capacidad del analista)", "Alto", "0.86"),
        ("9. AEXP (Experiencia en aplicación)", "Nominal", "1.00"),
        ("10. PCAP (Capacidad programadores)", "Alto", "0.86"),
        ("11. VEXP (Experiencia en plataforma)", "Nominal", "1.00"),
        ("12. LEXP (Experiencia en lenguajes)", "Alto", "0.95"),
        ("13. MODP (Prácticas modernas prog.)", "Muy Alto", "0.82"),
        ("14. TOOL (Herramientas software)", "Alto", "0.91"),
        ("15. SCED (Cronograma requerido)", "Nominal", "1.00"),
    ]
    for r_idx, (cd, niv, val) in enumerate(drivers_col2, start=1):
        for c_idx, text in enumerate([cd, niv, val]):
            cell = t2.cell(r_idx, c_idx)
            cell.text = text
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(8.5)
            if c_idx == 2 and val != "1.00":
                p.font.bold = True
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if r_idx % 2 == 0 else RGBColor(255, 255, 255)

    # Cuadro resumen debajo de las dos tablas
    box12 = s12.shapes.add_textbox(Inches(0.8), Inches(4.9), Inches(11.7), Inches(2.2))
    tf12 = box12.text_frame
    tf12.word_wrap = True

    p = tf12.paragraphs[0]
    p.text = "CÁLCULO DEL FACTOR DE AJUSTE (EAF) Y ESFUERZO REFINADO:"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = NAVY

    res_cocomo = (
        "• EAF (Multiplicador de los 15 Cost Drivers): 1.15 × 1.00 × 1.15 × 1.00 × 1.00 × 0.87 × 1.00 × 0.86 × 1.00 × 0.86 × 1.00 × 0.95 × 0.82 × 0.91 × 1.00 = 0.795.\n"
        "• Esfuerzo Ajustado (E_intermedio): EAF × E_básico = 0.795 × 97.53 PM = 77.54 Personas-Mes (Ahorro del 20.5% en esfuerzo).\n"
        "• Tiempo de Desarrollo Estimado (TDEV): 2.5 × (77.54)^0.35 = 4.59 Meses (≈ 18.3 semanas de calendario).\n"
        "• Conclusión: Las altas calificaciones en capital humano (ACAP=0.86, PCAP=0.86), prácticas modernas (MODP=0.82) y herramientas (TOOL=0.91) compensan la complejidad del Patrón Saga (CPLX=1.15) y los requisitos de dinero real (RELY=1.15), validando la entrega en 16 semanas."
    )
    pi = tf12.add_paragraph()
    pi.text = res_cocomo
    pi.font.size = Pt(9.5)
    pi.font.color.rgb = DARK

    set_speaker_notes(s12, 
        "DEFENSA ORAL (Minuto 7:50 - 8:30):\n"
        "En el modelo COCOMO Intermedio evaluamos con rigor los 15 conductores de costo de Boehm distribuidos en dos bloques: "
        "a la izquierda los atributos de producto y plataforma, y a la derecha los de personal y proyecto. "
        "Aunque factores como la confiabilidad financiera RELY (1.15) y la complejidad distribuida CPLX (1.15) demandan más esfuerzo, "
        "la alta capacidad del equipo (ACAP=0.86, PCAP=0.86) y el uso de prácticas modernas como TDD y monorepo (MODP=0.82, TOOL=0.91) "
        "reducen el esfuerzo en un 20.5%, arrojando un EAF de 0.795 y un tiempo realista de 4.5 meses."
    )

    # -------------------------------------------------------------
    # SLIDE 14: ESTIMACIÓN PRESUPUESTAL - ESTRUCTURA Y TOTAL
    # -------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "13. Estimación Presupuestal: Resumen del Presupuesto Integral")

    table_shape13 = s13.shapes.add_table(6, 4, Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.5))
    t13 = table_shape13.table
    t13.columns[0].width = Inches(1.2)
    t13.columns[1].width = Inches(4.5)
    t13.columns[2].width = Inches(3.2)
    t13.columns[3].width = Inches(2.8)

    h13 = ["WBS", "CATEGORÍA DEL PRESUPUESTO", "DESCRIPCIÓN DE PARTIDAS", "MONTO TOTAL (MXN)"]
    for i, h in enumerate(h13):
        c = t13.cell(0, i)
        c.fill.solid()
        c.fill.fore_color.rgb = NAVY
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(255, 255, 255)

    budget_rows = [
        ("1.0", "Recursos Humanos (Labor)", "5 Roles técnicos (Scrum Master, Arquitecto, Devs, QA) - 2,720 horas.", "$358,000.00 MXN"),
        ("2.0", "Recursos Materiales y Equipos", "Tablet mostrador POS 10.5\", Impresora térmica 80mm y Lector QR 2D.", "$9,500.00 MXN"),
        ("3.0", "Servicios Cloud y Licenciamiento", "Google Cloud Platform (Cloud Run, SQL), RabbitMQ, Dominio y GitHub.", "$12,750.00 MXN"),
        ("4.0", "Fondo de Contingencia y Riesgos", "Reserva preventiva calculada al 10% de los costos directos.", "$38,025.00 MXN"),
        ("TOTAL", "PRESUPUESTO TOTAL DEL PROYECTO", "Inversión integral calculada a 16 semanas (4 meses)", "$418,275.00 MXN")
    ]
    for r_idx, row in enumerate(budget_rows, start=1):
        for c_idx, val in enumerate(row):
            cell = t13.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            if r_idx == 5:
                p.font.bold = True
                p.font.size = Pt(11)
                p.font.color.rgb = RGBColor(255, 255, 255)
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY
            else:
                p.font.color.rgb = DARK
                cell.fill.solid()
                cell.fill.fore_color.rgb = LIGHT_BG if r_idx % 2 == 0 else RGBColor(255, 255, 255)

    box13 = s13.shapes.add_textbox(Inches(0.8), Inches(6.2), Inches(11.7), Inches(0.8))
    tf13 = box13.text_frame
    p = tf13.paragraphs[0]
    p.text = "Nota: El desglose detallado con tarifas horarias y fórmulas automáticas se encuentra formalizado en la plantilla oficial de Smartsheet generada en el proyecto (Presupuesto_Monchis_Cafe.xlsx)."
    p.font.size = Pt(10.5)
    p.font.italic = True
    p.font.color.rgb = MUTED

    set_speaker_notes(s13, 
        "DEFENSA ORAL (Minuto 8:30 - 9:00):\n"
        "El presupuesto integral del proyecto asciende a $418,275 pesos mexicanos. "
        "El 85% corresponde a mano de obra especializada en desarrollo y QA. "
        "Aprovechamos servicios administrados en la nube para reducir costos fijos de servidores, "
        "e incorporamos formalmente un 10% de contingencia para amortiguar cualquier imprevisto técnico o de volatilidad cambiaria."
    )

    # -------------------------------------------------------------
    # SLIDE 15: MODELADO Y DISEÑO - DIAGRAMAS UML (CASOS DE USO Y CLASES)
    # -------------------------------------------------------------
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "14. Modelado y Diseño: Diagramas UML (Casos de Uso y Clases)")

    box14_l = s14.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tf14_l = box14_l.text_frame
    tf14_l.word_wrap = True
    p = tf14_l.paragraphs[0]
    p.text = "CASOS DE USO PRINCIPALES DEL SISTEMA"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = NAVY

    uml_cases = [
        ("Actor: Barista / Cajero (POS)", "• Registrar orden con escaneo de código de barras.\n• Aplicar pagos mixtos (Efectivo, Tarjeta, Puntos Monchis).\n• Asignar bono ecológico si el cliente presenta termo reutilizable.\n• Emisión de ticket digital con QR de trazabilidad de finca."),
        ("Actor: Administrador / Dueño", "• Dar de alta lotes de café con fecha de tueste y origen.\n• Consultar panel de ventas con atribución UTM (Maps vs Instagram).\n• Supervisar mermas y auditoría de transacciones fallidas en DLQ."),
        ("Actor: Cliente Eco-Consciente", "• Acumular sellos digitales y canjear cashback Monchis Rewards.\n• Consultar catálogo público prerenderizado con historia de fincas.")
    ]
    for act, desc in uml_cases:
        pi = tf14_l.add_paragraph()
        pi.text = f"• {act}:"
        pi.font.bold = True
        pi.font.size = Pt(10.5)
        pi.font.color.rgb = TEAL
        pi.space_before = Pt(6)
        run = pi.add_run()
        run.text = f"\n{desc}"
        run.font.bold = False
        run.font.color.rgb = DARK

    box14_r = s14.shapes.add_textbox(Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tf14_r = box14_r.text_frame
    tf14_r.word_wrap = True
    p_r = tf14_r.paragraphs[0]
    p_r.text = "DIAGRAMA DE CLASES DEL DOMINIO (PRISMA)"
    p_r.font.bold = True
    p_r.font.size = Pt(13)
    p_r.font.color.rgb = TEAL

    classes_ascii = (
        "┌──────────────────────────┐       ┌──────────────────────────┐\n"
        "│         Product          │ 1   * │        CoffeeBatch       │\n"
        "├──────────────────────────┼───────┼──────────────────────────┤\n"
        "│ id: String (UUID)        │       │ id: String               │\n"
        "│ name: String             │       │ farmName: String         │\n"
        "│ price: Decimal           │       │ altitudeMeters: Int      │\n"
        "│ category: CategoryEnum   │       │ roastDate: DateTime      │\n"
        "└────────────┬─────────────┘       │ expiryDate: DateTime     │\n"
        "             │ 1                   └──────────────────────────┘\n"
        "             │ *\n"
        "┌────────────▼─────────────┐       ┌──────────────────────────┐\n"
        "│        OrderItem         │ *   1 │          Order           │\n"
        "├──────────────────────────┼───────┼──────────────────────────┤\n"
        "│ quantity: Int            │       │ totalAmount: Decimal     │\n"
        "│ unitPrice: Decimal       │       │ ecoBonusDiscount: Decimal│\n"
        "│ subtotal: Decimal        │       │ paymentStatus: StatusEnum│\n"
        "└──────────────────────────┘       └──────────────────────────┘"
    )
    pi = tf14_r.add_paragraph()
    pi.text = classes_ascii
    pi.font.name = "Consolas"
    pi.font.size = Pt(9.5)
    pi.font.color.rgb = DARK

    set_speaker_notes(s14, 
        "DEFENSA ORAL (Minuto 9:00 - 9:30):\n"
        "En el modelado UML destacamos la cohesión del dominio: la entidad Product se vincula a CoffeeBatch para "
        "trazar altitud, finca y fecha de tueste, cumpliendo con la política PEPS. Los casos de uso separan de forma estricta "
        "los privilegios: el cajero sólo opera transacciones de mostrador, mientras que el administrador audita mermas "
        "y canales de tráfico UTM."
    )

    # -------------------------------------------------------------
    # SLIDE 16: MODELADO Y DISEÑO - DIAGRAMA DE SECUENCIA (SAGA PATTERN)
    # -------------------------------------------------------------
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "15. Modelado y Diseño: Diagrama de Secuencia (Patrón Saga y Reversas)")

    box15 = s15.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf15 = box15.text_frame
    tf15.word_wrap = True

    p = tf15.paragraphs[0]
    p.text = "FLUJO TRANSACCIONAL RESILIENTE CON RABBITMQ (CONSISTENCIA EVENTUAL)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = NAVY

    sequence_ascii = (
        " [Barista / POS]          [API Gateway]             [RabbitMQ Bus]           [Saga Orchestrator]      [Inventory / DB]\n"
        "        │                        │                         │                          │                       │\n"
        "        │── 1. Enviar Venta ────►│                         │                          │                       │\n"
        "        │   (Items + Pagos)      │── 2. Emitir Evento ────►│                          │                       │\n"
        "        │                        │      'OrderPlaced'      │── 3. Consumir Evento ───►│                       │\n"
        "        │                        │                         │                          │── 4. Bloquear Stock ─►│\n"
        "        │                        │                         │                          │   (Valida Lote PEPS)  │\n"
        "        │                        │                         │                          │◄── Stock OK ──────────│\n"
        "        │                        │                         │                          │                       │\n"
        "        │                        │                         │   [ESCENARIO DE FALLO EN PASARELA DE COBRO]      │\n"
        "        │                        │                         │                          │                       │\n"
        "        │                        │                         │◄── 5. Emitir Compensac. ─│ (PaymentFailed)       │\n"
        "        │                        │                         │   'RevertStockEvent'     │                       │\n"
        "        │                        │                         │                          │── 6. Desbloquea Stock►│\n"
        "        │◄── 7. Alerta POS ──────│◄── 7. Notificar ────────│                          │    (Reversa Saga)     │\n"
        "        │    'Venta Revertida'   │    WebSocket/SSE        │                          │                       │\n\n"
        "Garantía de Negocio: Erradica discrepancias entre inventario físico y contable aun si se pierde conexión con la pasarela bancaria."
    )
    pi = tf15.add_paragraph()
    pi.text = sequence_ascii
    pi.font.name = "Consolas"
    pi.font.size = Pt(9.5)
    pi.font.color.rgb = DARK

    set_speaker_notes(s15, 
        "DEFENSA ORAL (Minuto 9:30 - 10:00):\n"
        "Este diagrama de secuencia es el corazón de la resiliencia del software. Al procesar una venta, el orquestador Saga coordina "
        "la reserva de inventario y el cobro. Si la transacción financiera falla, RabbitMQ no deja cabos sueltos: emite de inmediato "
        "un evento compensatorio que libera el lote de café en la base de datos y avisa a la pantalla del barista. "
        "Así cumplimos con el ODS 16, garantizando total transparencia financiera."
    )

    # -------------------------------------------------------------
    # SLIDE 17: MODELADO Y DISEÑO - WIREFRAMES Y BOCETOS DE UI
    # -------------------------------------------------------------
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "16. Modelado y Diseño: Wireframes y Arquitectura de Pantallas")

    box16_l = s16.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tf16_l = box16_l.text_frame
    tf16_l.word_wrap = True
    p = tf16_l.paragraphs[0]
    p.text = "WIREFRAME ESQUEMÁTICO: PUNTO DE VENTA (POS)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = NAVY

    wf_pos = (
        "┌────────────────────────────────────────────────────────┐\n"
        "│ MONCHIS CAFÉ POS     [Barista: Ernesto]     [14:35 PM] │\n"
        "├──────────────────────────┬─────────────────────────────┤\n"
        "│ [Categorías de Café]     │ ORDEN ACTUAL (#1042)        │\n"
        "│ [Espresso] [Latte] [Cold]│ • 1x Latte Orgánico Chiapas │\n"
        "│                          │   Lote #A-24 (Tueste 3d)    │\n"
        "│ ┌────────┐  ┌────────┐   │   $65.00                    │\n"
        "│ │American│  │FlatWhie│   │ ─────────────────────────── │\n"
        "│ │ $45.00 │  │ $60.00 │   │ Subtotal:           $65.00  │\n"
        "│ └────────┘  └────────┘   │ [✓] Bono Termo Eco: -$5.00  │\n"
        "│                          │ Total a Cobrar:     $60.00  │\n"
        "│ ┌────────┐  ┌────────┐   │ ─────────────────────────── │\n"
        "│ │Mocha   │  │PourOver│   │ [ EFECTIVO ]  [ TARJETA ]   │\n"
        "│ │ $68.00 │  │ $75.00 │   │ [ SPEI QR  ]  [ PUNTOS  ]   │\n"
        "│ └────────┘  └────────┘   │ [ PAGO MIXTO: Cambio: $0.00]│\n"
        "│ [Escanear Lote/Finca QR] │ [ COBRAR E IMPRIMIR TICKET] │\n"
        "└──────────────────────────┴─────────────────────────────┘"
    )
    pi = tf16_l.add_paragraph()
    pi.text = wf_pos
    pi.font.name = "Consolas"
    pi.font.size = Pt(8.5)
    pi.font.color.rgb = DARK

    box16_r = s16.shapes.add_textbox(Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tf16_r = box16_r.text_frame
    tf16_r.word_wrap = True
    p_r = tf16_r.paragraphs[0]
    p_r.text = "PRINCIPIOS DE DISEÑO UI/UX IMPLEMENTADOS"
    p_r.font.bold = True
    p_r.font.size = Pt(13)
    p_r.font.color.rgb = TEAL

    ux_principles = [
        ("Optimización Táctil en Mostrador:", "Botones con área mínima de impacto de 48x48px y soporte de teclado numérico para cálculo instantáneo de cambio."),
        ("Paleta de Color Pastel Cálida:", "Uso de tonos café suaves, crema y menta que reducen la fatiga visual de los baristas durante jornadas prolongadas."),
        ("Accesibilidad Web WCAG 2.1 AA:", "Contraste de color superior a 4.5:1, etiquetas semánticas para lectores de pantalla y compatibilidad con prefers-reduced-motion."),
        ("Transparencia en Pantalla:", "Visualización inmediata del descuento por termo ecológico (-$5.00) y el origen del lote antes de confirmar la transacción.")
    ]
    for head, desc in ux_principles:
        pi = tf16_r.add_paragraph()
        pi.text = f"• {head} "
        pi.font.bold = True
        pi.font.size = Pt(11)
        pi.font.color.rgb = DARK
        pi.space_before = Pt(8)
        run = pi.add_run()
        run.text = desc
        run.font.bold = False

    set_speaker_notes(s16, 
        "DEFENSA ORAL (Minuto 10:00 - 10:20):\n"
        "En el diseño visual del POS priorizamos la ergonomía y la velocidad. "
        "El barista puede seleccionar productos, aplicar el bono ecológico de termo en un clic y registrar pagos mixtos con cálculo "
        "automático de cambio en menos de 15 segundos. Cumplimos además con accesibilidad universal WCAG 2.1 AA "
        "y un sistema de diseño cálido pastel altamente estético."
    )

    # -------------------------------------------------------------
    # SLIDE 18: CONCLUSIÓN Y RESULTADOS ESPERADOS
    # -------------------------------------------------------------
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "17. Conclusiones y Defensa del Proyecto")

    box17 = s17.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf17 = box17.text_frame
    tf17.word_wrap = True

    conclusions = [
        ("Viabilidad Técnica y Operativa:", 
         "El proyecto integra metodologías ágiles SCRUM y modelos formales de estimación COCOMO Intermedio (EAF: 0.795), garantizando la entrega de los 8 Sprints en el plazo estipulado de 16 semanas con alta disciplina arquitectónica."),
        ("Alineación con la Agenda 2030 (ODS):", 
         "Monchis Café demuestra que el desarrollo de software sustentable (Green Software) no es teórico: desvía más de 4,500 vasos plásticos semestrales (ODS 12), agiliza la microeconomía de especialidad (ODS 8) y protege datos con arquitectura Zero Trust (ODS 16)."),
        ("Resiliencia Transaccional y Financiera:", 
         "La implementación del Patrón Saga con RabbitMQ elimina pérdidas de inventario por caídas de pasarela, protegiendo la inversión integral presupuestada de $418,275 MXN."),
        ("Estado Actual y Próximos Pasos:", 
         "Monorepo configurado, especificaciones y requerimientos formalizados bajo normas APA 7, listos para la fase de pruebas automatizadas multicapa y despliegue en Google Cloud Platform.")
    ]
    for idx, (head, desc) in enumerate(conclusions):
        p = tf17.add_paragraph() if idx > 0 else tf17.paragraphs[0]
        p.text = f"✔ {head} "
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = NAVY
        p.space_before = Pt(10)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK

    set_speaker_notes(s17, 
        "DEFENSA ORAL (Minuto 10:20 - 10:45):\n"
        "En conclusión, Monchis Café es un proyecto donde la ingeniería de software, la gestión rigurosa de proyectos "
        "y la sustentabilidad convergen armónicamente. El modelo COCOMO valida nuestra productividad, la planificación PERT "
        "blinda los tiempos de entrega y los principios ODS dotan al software de un propósito ético y rentable. "
        "Quedo atento a las preguntas y retroalimentación del profesor Gabriel Navarro. Muchas gracias."
    )

    prs.save(output_path)
    print(f"Presentación PPTX generada con éxito en: {output_path}")

if __name__ == "__main__":
    create_deck(r"d:\ernestofm\Proyecto\docs\presentacion\Presentacion_Producto_Integrador_Monchis_Cafe.pptx")
