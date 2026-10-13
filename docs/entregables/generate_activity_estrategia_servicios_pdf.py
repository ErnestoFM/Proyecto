# -*- coding: utf-8 -*-
"""
Generador del Entregable Académico Oficial en DOCX, HTML y PDF:
Actividad PARTICIPACIÓN: Diseño de Estrategia de Servicios TI
Cátedra: Gestión de Servicios Informáticos
Docente: Dr. Gabriel Navarro Salcedo
Institución: Universidad de Guadalajara / Centro Universitario de Tonalá (CUTonalá)
División de Ingenierías e Innovación Tecnológica - Licenciatura en Ingeniería en Computación
Equipo de Proyecto:
  - Ernesto Hatuey Fierro Medina (Código: 215487963) [Líder y Arquitecto de Servicios TI]
  - Jazmín Díaz [Diseño de Servicios y Requerimientos]
  - Héctor Hernández [Infraestructura y Operación de Servicios TI]
  - Oswaldo Millán [Transición y Aseguramiento de Calidad de Software]
Fecha de Entrega: 17 de octubre de 2026
"""

import os
import subprocess
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

doc = Document()

# Configuración de estilos base (Arial 12 pt, interlineado 1.5, márgenes de 2.54 cm)
style_normal = doc.styles['Normal']
style_normal.font.name = 'Arial'
style_normal.font.size = Pt(11)
style_normal.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)
style_normal.paragraph_format.line_spacing = 1.35
style_normal.paragraph_format.space_after = Pt(6)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name = 'Arial'
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name = 'Arial'
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0x2B, 0x4C, 0x7E)
    return p

def add_heading_3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.italic = True
    run.font.name = 'Arial'
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0x31, 0x82, 0xCE)
    return p

def add_page_number_to_footer(section):
    p_footer = section.footer.paragraphs[0]
    p_footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_footer.text = ""
    run = p_footer.add_run()
    run.font.name = 'Arial'
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
    
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

# -------------------------------------------------------------------------
# SECCIÓN 1: PORTADA E INTRODUCCIÓN (PORTRAIT)
# -------------------------------------------------------------------------
sec1 = doc.sections[0]
sec1.orientation = WD_ORIENT.PORTRAIT
sec1.page_width = Inches(8.5)
sec1.page_height = Inches(11.0)
sec1.top_margin = Inches(1.0)
sec1.bottom_margin = Inches(1.0)
sec1.left_margin = Inches(1.0)
sec1.right_margin = Inches(1.0)

# Portada académica sobria
p_inst = doc.add_paragraph()
p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_inst.paragraph_format.space_before = Pt(28)
p_inst.paragraph_format.space_after = Pt(20)
p_inst.paragraph_format.line_spacing = 1.2
r_inst = p_inst.add_run(
    "UNIVERSIDAD DE GUADALAJARA\n"
    "Centro Universitario de Tonalá (CUTonalá)\n"
    "División de Ingenierías e Innovación Tecnológica\n"
    "Licenciatura en Ingeniería en Computación\n"
)
r_inst.bold = True
r_inst.font.size = Pt(12)

p_tit = doc.add_paragraph()
p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_tit.paragraph_format.space_before = Pt(36)
p_tit.paragraph_format.space_after = Pt(24)
p_tit.paragraph_format.line_spacing = 1.2
r_tit = p_tit.add_run(
    "ACTIVIDAD PARTICIPACIÓN\n"
    "DISEÑO DE ESTRATEGIA DE SERVICIOS TI\n"
    "Proyecto Final: Monchis Café (Plataforma Web y Sistema de Gestión Integral)\n"
)
r_tit.bold = True
r_tit.font.size = Pt(13)
r_tit.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

p_dat = doc.add_paragraph()
p_dat.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_dat.paragraph_format.space_before = Pt(45)
p_dat.paragraph_format.space_after = Pt(0)
p_dat.paragraph_format.line_spacing = 1.3
r_dat = p_dat.add_run(
    "Cátedra: Gestión de Servicios Informáticos\n"
    "Docente: Dr. Gabriel Navarro Salcedo\n\n"
    "Equipo de Proyecto:\n"
    "• Ernesto Hatuey Fierro Medina (Código: 215487963) — Líder y Arquitecto de Servicios TI\n"
    "• Jazmín Díaz — Diseño de Servicios y Requerimientos\n"
    "• Héctor Hernández — Especialista en Infraestructura y Operación TI\n"
    "• Oswaldo Millán — Especialista en Transición y Aseguramiento de Calidad\n\n"
    "Fecha de entrega: 17 de octubre de 2026\n"
    "Ciclo: 2026-B"
)
r_dat.font.size = Pt(11)

# Salto a Índice
doc.add_page_break()
add_page_number_to_footer(sec1)

add_heading_1("Índice General")

indice_items = [
    ("1. Introducción y Marco de Gestión de Servicios TI", "3"),
    ("2. Desarrollo de la Estrategia de Servicios TI", "4"),
    ("   2.1. ¿Qué servicios debemos ofrecer? (Portafolio y Catálogo de Servicios)", "4"),
    ("   2.2. ¿Cuál es su valor? (Definición de Valor: Utilidad y Garantía)", "6"),
    ("   2.3. ¿Cuáles son los resultados esperados? (Metas Cualitativas y Cuantitativas)", "7"),
    ("   2.4. ¿Cuáles son nuestros clientes potenciales? (Segmentación y Perfiles de Mercado)", "8"),
    ("   2.5. ¿Qué servicios son prioritarios? (Matriz de Priorización Estratégica)", "9"),
    ("   2.6. ¿Qué inversiones son necesarias? (Presupuesto y Recursos Financieros)", "10"),
    ("   2.7. ¿Qué servicios existen en el mercado que representen competencia directa? (Benchmarking)", "12"),
    ("   2.8. ¿Cómo podemos diferenciarnos de la competencia? (Propuesta de Valor Única)", "13"),
    ("3. Articulación de la Estrategia en las Fases del Ciclo de Vida del Servicio TI (ITIL)", "15"),
    ("   3.1. Estrategia del Servicio (Service Strategy)", "15"),
    ("   3.2. Diseño del Servicio (Service Design)", "15"),
    ("   3.3. Transición del Servicio (Service Transition)", "16"),
    ("   3.4. Operación del Servicio (Service Operation)", "16"),
    ("   3.5. Mejora Continua del Servicio (Continual Service Improvement)", "17"),
    ("4. Conclusiones Generales", "18"),
    ("5. Referencias Bibliográficas (APA 7.ª edición)", "19"),
]

for title, page in indice_items:
    p_ind = doc.add_paragraph()
    p_ind.paragraph_format.line_spacing = 1.15
    p_ind.paragraph_format.space_after = Pt(3)
    r1 = p_ind.add_run(title)
    r1.font.name = 'Arial'
    r1.font.size = Pt(10.5)
    if not title.startswith("   "):
        r1.bold = True

# Salto a Introducción
doc.add_page_break()

add_heading_1("1. Introducción y Marco de Gestión de Servicios TI")
doc.add_paragraph(
    "En la actualidad, las tecnologías de información han dejado de ser meras herramientas de soporte administrativo "
    "para convertirse en el núcleo estratégico que habilita, transforma y potencia los modelos de negocio. Bajo los principios "
    "de la Gestión de Servicios de Tecnologías de la Información (ITSM), formalizados en marcos de referencia reconocidos "
    "globalmente como ITIL (Information Technology Infrastructure Library) y el estándar internacional ISO/IEC 20000-1:2018, "
    "un servicio de TI se define como un medio para entregar valor a los clientes facilitando los resultados que ellos desean "
    "alcanzar, sin que estos deban asumir de forma directa la propiedad de costos y riesgos específicos (AXELOS, 2019; ISO/IEC, 2018)."
)
doc.add_paragraph(
    "El presente documento expone la Estrategia Integral de Servicios TI diseñada por el equipo de proyecto para Monchis Café, "
    "una empresa gastronómica regional especializada en café orgánico de cooperativas campesinas y productos comerciales "
    "complementarios. La estrategia no se limita a describir un paquete de software aislado; por el contrario, estructura un "
    "ecosistema de servicios gestionados que articula las cinco fases del ciclo de vida de los servicios TI: Estrategia, Diseño, "
    "Transición, Operación y Mejora Continua. Con ello, se garantiza que la inversión tecnológica responda directamente a las "
    "necesidades del negocio en mostrador, a la sostenibilidad ecológica (alineada a los Objetivos de Desarrollo Sostenible ODS 8, 9, 12 y 16) "
    "y a una experiencia omnicanal superior para el comensal contemporáneo."
)

# Sección 2: Desarrollo de la Estrategia
add_heading_1("2. Desarrollo de la Estrategia de Servicios TI")

# 2.1 Qué servicios debemos ofrecer
add_heading_2("2.1. ¿Qué servicios debemos ofrecer? (Portafolio y Catálogo de Servicios)")
doc.add_paragraph(
    "Para estructurar la oferta tecnológica, adoptamos la metodología de catálogo de servicios de ITIL v3 e ITIL 4, clasificando "
    "los servicios en tres niveles complementarios: Servicios Principales (Core), Servicios Habilitadores (Enabling) y Servicios de "
    "Soporte y Garantía (Support & Enhancing). Esta taxonomía permite visibilizar con claridad qué percibe el cliente final y qué capas "
    "de infraestructura, mensajería y seguridad sustentan la operación ininterrumpida de la cafetería."
)
doc.add_paragraph(
    "A. Servicios Principales (Core Services):\n"
    "1. Servicio de Punto de Venta Táctil (POS) Omnicanal y Procesamiento Multimodal de Pagos: Interfaz interactiva de alta velocidad "
    "optimizada para tabletas de barra (Vue 3 SPA). Facilita el registro inmediato de comandas, cobro simultáneo en efectivo (con cálculo "
    "automatizado de cambio), tarjetas mediante pasarelas comerciales (Stripe, Clip, Mercado Pago), transferencias electrónicas SPEI con clave "
    "de rastreo y emisión instantánea de recibos térmicos de 80 mm y tickets digitales.\n"
    "2. Servicio de Trazabilidad Integral de Café Orgánico y Gestión PEPS de Almacén: Registro granular de lotes de café de especialidad "
    "recibidos desde cooperativas campesinas (finca, altitud, perfil de tueste, fecha de tostado y caducidad). Garantiza rotación estricta "
    "PEPS (Primeras Entradas, Primeras Salidas) y genera códigos QR para que el cliente consulte en su smartphone el origen del grano servido en su taza.\n"
    "3. Servicio de Fidelización y Monedero Digital ('Monchis Rewards'): Tarjeta digital de sellos (8.ª bebida gratis tras 7 consumos acumulados), "
    "monedero de cashback (1 punto por cada $10 MXN gastados) y bonificación ecológica directa de $5.00 MXN al comensal que lleve termo o taza reutilizable (ODS 12)."
)
doc.add_paragraph(
    "B. Servicios Habilitadores e Infraestructura (Enabling Services):\n"
    "4. Servicio de Plataforma Cloud y Orquestación Asíncrona (RabbitMQ + Patrón Saga): Broker de eventos distribuidos que garantiza consistencia. "
    "Si un pedido se cobra en barra pero el stock de insumo orgánico se agota por concurrencia, el orquestador Saga ejecuta transacciones "
    "compensatorias automáticas (reversas inmediatas) y desvía fallos no recuperables a la Dead Letter Queue (DLQ) con alerta administrativa por SMTP.\n"
    "5. Servicio de Almacenamiento Seguro y Persistencia Transaccional (PostgreSQL + Prisma): Base de datos relacional con integridad "
    "referencial, consultas parametrizadas contra inyección SQL y particionamiento de datos comerciales frente a insumos de especialidad.\n"
    "6. Servicio de Seguridad Perimetral, Autenticación Stateless y Control de Acceso (RBAC): Emisión de JWT rotativos con Refresh Token en "
    "cookies seguras httpOnly + Secure + SameSite=Strict, validación anti-bot mediante Google reCAPTCHA v2/v3 y autenticación de doble factor (2FA) para administradores."
)
doc.add_paragraph(
    "C. Servicios de Soporte y Operación (Support Services):\n"
    "7. Servicio de Mesa de Ayuda (Service Desk) y Asistencia Técnica Continua: Soporte remoto y telefónico para cajeros y baristas ante atascos "
    "de periféricos, fallos de red o dudas de operación bajo acuerdos de nivel de servicio (SLA).\n"
    "8. Servicio de Respaldo Automatizado y Recuperación ante Desastres (Disaster Recovery): Copias de seguridad diarias incrementales y semanales "
    "completas, cifradas y replicadas en la nube, con tiempo objetivo de recuperación (RTO) menor a 60 minutos.\n"
    "9. Servicio de Monitoreo Proactivo y Telemetría: Vigilancia continua de memoria, endpoints de salud (/api/health) y saturación de colas RabbitMQ."
)

# 2.2 Cuál es su valor
add_heading_2("2.2. ¿Cuál es su valor? (Definición de Valor: Utilidad y Garantía)")
doc.add_paragraph(
    "Siguiendo el principio fundamental de ITIL, el valor no reside en las herramientas técnicas por sí mismas, sino en la percepción de los "
    "resultados habilitados para el cliente. En la gestión de servicios TI, el valor se compone de dos dimensiones inseparables: Utilidad "
    "('Fit for Purpose' —lo que el servicio hace para eliminar restricciones y mejorar el rendimiento) y Garantía ('Fit for Use' —la certeza de "
    "que el servicio estará disponible, tendrá la capacidad adecuada, será continuo y mantendrá la seguridad) (AXELOS, 2019; Steinberg, 2011)."
)
doc.add_paragraph(
    "1. Utilidad Comprobada (Fit for Purpose):\n"
    "• Agilidad Extrema en Barra: El POS táctil reduce el tiempo medio de atención por comensal de 2.5 minutos a menos de 45 segundos, "
    "permitiendo atender hasta un 60 % más de clientes en horarios pico matutinos sin aumentar el personal de mostrador.\n"
    "• Cuadre de Caja Inmediato: El cierre de turno se automatiza en un clic, eliminando 40 minutos diarios de conteo manual y discrepancias contables.\n"
    "• Reducción de Mermas de Café en un 85 %: Las alertas preventivas de desgasificación y caducidad aseguran que ningún lote de café especial envejezca en almacén."
)
doc.add_paragraph(
    "2. Garantía Técnica (Fit for Use):\n"
    "• Alta Disponibilidad (99.9 %): Arquitectura contenerizada en Docker que previene caídas imprevistas del sistema durante la jornada comercial.\n"
    "• Consistencia Transaccional con Cero Ventas Fantasma: El patrón Saga garantiza que jamás se cobre un insumo agotado sin compensación automática.\n"
    "• Seguridad Robusta: El esquema de autenticación stateless y RBAC garantiza que el personal solo acceda a las funciones correspondientes a su rol, "
    "protegiendo los fondos de caja y la privacidad de los comensales."
)

# 2.3 Resultados esperados
add_heading_2("2.3. ¿Cuáles son los resultados esperados? (Metas Cualitativas y Cuantitativas)")
doc.add_paragraph(
    "Para garantizar que la estrategia sea medible y auditable conforme a la fase de Mejora Continua de ITIL, se establecen metas "
    "cualitativas y cuantitativas vinculadas a Factores Críticos de Éxito (CSFs) e Indicadores Clave de Desempeño (KPIs):"
)

# 2.4 Clientes potenciales
add_heading_2("2.4. ¿Cuáles son nuestros clientes potenciales? (Segmentación y Perfiles de Mercado)")
doc.add_paragraph(
    "La estrategia de servicios TI de Monchis Café estructura una segmentación dual que atiende tanto al cliente final que consume en barra "
    "como al personal interno y a potenciales franquiciatarios independientes que requieren una solución tecnológica especializada:"
)
doc.add_paragraph(
    "• Segmento 1: Consumidores de Café de Especialidad y Nómadas Digitales. Comensales entre 22 y 55 años que valoran la procedencia orgánica, "
    "los métodos artesanales y la sostenibilidad. Demandan interfaces interactivas donde consultar el origen del café en su taza, métodos de pago "
    "rápidos sin contacto (contactless/SPEI) y recompensas de lealtad en su smartphone sin tarjetas plásticas contaminantes.\n"
    "• Segmento 2: Productores y Cooperativas Cafetaleras Regionales. Pequeños agricultores que buscan un canal justo y transparente para vender "
    "su grano de altura, beneficiándose del reconocimiento explícito de su finca y marca en el sistema de trazabilidad de Monchis Café.\n"
    "• Segmento 3: Personal Operativo y Gerencia de Monchis Café. Cajeros y baristas que precisan una pantalla táctil libre de errores, y administradores "
    "que necesitan auditar ingresos diarios, mermas de insumos y el retorno de inversión de campañas digitales en Instagram y Google Maps.\n"
    "• Segmento 4: Micro y Pequeñas Cafeterías Independientes (Modelo de Expansión SaaS). Establecimientos de 1 a 3 sucursales en ciudades medianas "
    "que están desatendidos por los complejos sistemas ERP restauranteros y limitados por terminales genéricas de cobro bancario."
)

# 2.5 Servicios prioritarios
add_heading_2("2.5. ¿Qué servicios son prioritarios? (Matriz de Priorización Estratégica)")
doc.add_paragraph(
    "La priorización de servicios se fundamenta en una matriz de doble entrada que contrasta el Impacto en la Continuidad del Negocio "
    "con la Factibilidad Técnica y Recursos Disponibles, distribuyendo el esfuerzo en cuatro fases de despliegue progresivo:"
)
doc.add_paragraph(
    "1. Prioridad 1 (Crítica e Inmediata - Semanas 1 a 4): Punto de Venta Táctil (POS), Procesamiento Multimodal de Pagos y Seguridad Stateless RBAC. "
    "Constituyen el núcleo vital sin el cual la cafetería no puede abrir sus puertas ni registrar cobros de manera legal y protegida.\n"
    "2. Prioridad 2 (Alta y Esencial - Semanas 5 a 8): Trazabilidad de Café Orgánico con rotación PEPS y la Infraestructura Resiliente RabbitMQ Saga. "
    "Sustentan la propuesta de valor diferencial del café de especialidad y blindan las transacciones simultáneas contra desabastos.\n"
    "3. Prioridad 3 (Media y Diferenciadora - Semanas 9 a 12): Programa de Fidelización Monchis Rewards (ODS 12) y Panel de Analítica con Atribución UTM. "
    "Consolidan la recurrencia del cliente y optimizan la inversión publicitaria una vez estabilizada la barra.\n"
    "4. Prioridad 4 (Soporte Continuo y Transversal): Mesa de Ayuda técnica, monitoreo proactivo mediante alertas SMTP y respaldos automatizados en la nube."
)

# 2.6 Inversiones necesarias
add_heading_2("2.6. ¿Qué inversiones son necesarias? (Presupuesto y Recursos Financieros)")
doc.add_paragraph(
    "Para materializar la estrategia de servicios TI se requiere una inversión inicial en activos fijos (CAPEX) de $28,480 MXN y un gasto "
    "operativo recurrente mensual (OPEX) de $4,850 MXN. Esta estructura financiera es sumamente competitiva y representa un costo significativamente "
    "menor en comparación con el software restaurantero tradicional que cobra licencias privativas por cada estación instalada."
)

# 2.7 Competencia en el mercado
add_heading_2("2.7. ¿Qué servicios existen en el mercado que representen competencia directa? (Benchmarking)")
doc.add_paragraph(
    "El mercado de software para alimentos y bebidas presenta diversas alternativas, pero ninguna combina la trazabilidad artesanal de café "
    "con resiliencia arquitectónica y herramientas de marketing local integradas:\n"
    "• Soft Restaurant: Líder tradicional en México para restaurantes de mediano y gran tamaño. Sin embargo, impone licencias muy costosas "
    "(más de $14,000 MXN iniciales), requiere pólizas de soporte anuales con costo extra, su interfaz es rígida y no incluye trazabilidad de lotes orgánicos.\n"
    "• Toast POS / Square: Plataformas internacionales modernas con excelente diseño visual, pero sus suscripciones mensuales en dólares resultan "
    "prohibitivas para cafeterías locales ($69 a $165 USD mensuales) y obligan a utilizar sus propias pasarelas con comisiones bancarias elevadas.\n"
    "• Clip Stand / Mercado Pago POS: Terminales de cobro accesibles en hardware, pero extremadamente básicas a nivel de software. Carecen de control "
    "PEPS de insumos, no ofrecen programas de fidelización gamificados por termo ni sincronización con campañas de marketing digital."
)

# 2.8 Cómo podemos diferenciarnos
add_heading_2("2.8. ¿Cómo podemos diferenciarnos de la competencia? (Propuesta de Valor Única)")
doc.add_paragraph(
    "Monchis Café construye una ventaja competitiva sustentable a través de cinco pilares de diferenciación:\n"
    "1. Especialización Nativa en Café de Especialidad y ODS 12: Modelado del ciclo real del grano (finca, altitud, tueste, PEPS) con código QR al comensal y bonificación por termo reusable.\n"
    "2. Resiliencia de Nivel Empresarial con RabbitMQ Saga: Eliminación de desajustes de caja e inventario mediante reversas automáticas inmediatas ante falta de stock.\n"
    "3. Conexión Directa entre SEO Local y Barra: Frontend prerenderizado (vite-ssg) con datos estructurados Schema.org y captura de UTMs que mide qué comensales provienen de Instagram o Google Maps.\n"
    "4. Cero Rentas Prohibitivas de Licencia: Arquitectura cloud ligera y contenerizada que evita ataduras con proveedores monopólicos de software comercial.\n"
    "5. Soporte Técnico Hiperlocal y Calidez Humana: Mesa de ayuda directa con ingenieros de software dedicados y SLAs garantizados en horarios de apertura."
)

# Sección 3: Articulación en Fases ITIL
add_heading_1("3. Articulación de la Estrategia en las Fases del Ciclo de Vida del Servicio TI (ITIL)")
doc.add_paragraph(
    "La estrategia diseñada cobra vida a través de las cinco fases del ciclo de vida del servicio TI establecidas en el marco ITIL (AXELOS, 2019; Steinberg, 2011):\n\n"
    "3.1. Estrategia del Servicio (Service Strategy): Establece la alineación directa con la misión de Monchis Café. Gestiona el portafolio de servicios "
    "(separando el catálogo activo de las funcionalidades en desarrollo), define el modelo financiero de costos e ingresos, y analiza los patrones de "
    "demanda en barra para dimensionar los servidores durante las horas punta matutinas.\n\n"
    "3.2. Diseño del Servicio (Service Design): Traduce las necesidades estratégicas en especificaciones técnicas de servicio. Formaliza los Acuerdos "
    "de Nivel de Servicio (SLA) con la administración, diseña la arquitectura de seguridad con JWT stateless, reCAPTCHA y 2FA gerencial, define los planes "
    "de contingencia y continuidad (ITSCM) y diseña la capacidad para atender más de 50 peticiones simultáneas por segundo sin latencia perceptible.\n\n"
    "3.3. Transición del Servicio (Service Transition): Asegura que los nuevos servicios se desplieguen en producción sin disrupción operativa. "
    "Implementa prácticas de DevOps mediante integración continua (CI) en GitHub Actions, pruebas exhaustivas TDD con Vitest, Supertest y Playwright, "
    "gestión controlada de cambios mediante pull requests y capacitación interactiva para el personal de cafetería previo al lanzamiento.\n\n"
    "3.4. Operación del Servicio (Service Operation): Garantiza la efectividad diaria y estabilidad de los servicios en mostrador. Estructura una "
    "Mesa de Ayuda (Service Desk) escalonada (Nivel 0 cajero, Nivel 1 soporte remoto, Nivel 2 ingeniería de software), gestiona incidentes con un MTTR menor "
    "a 60 minutos, monitorea proactivamente la salud de endpoints y colas RabbitMQ, y audita las alertas canalizadas a la Dead Letter Queue.\n\n"
    "3.5. Mejora Continua del Servicio (Continual Service Improvement - CSI): Aplica el ciclo Deming (Plan-Do-Check-Act) para perfeccionar continuamente "
    "la plataforma. Evalúa trimestralmente los KPIs de atención en caja y adopción de lealtad, recopila retroalimentación cualitativa de baristas y clientes, "
    "y optimiza el uso de recursos en la nube para reducir el gasto operativo mensual."
)

# Sección 4: Conclusiones
add_heading_1("4. Conclusiones Generales")
doc.add_paragraph(
    "El diseño de esta estrategia integral de servicios tecnológicos para Monchis Café demuestra con rigor que el valor de la informática no radica "
    "en la complejidad técnica aislada, sino en su capacidad para habilitar metas de negocio tangibles y resolver problemas humanos concretos. "
    "Articular las cinco fases de ITIL permitió transformar los obstáculos cotidianos de un establecimiento gastronómico —filas lentas en caja, "
    "descuadres contables, pérdida de frescura en insumos orgánicos y licencias comerciales asfixiantes— en una oferta de servicios diferenciada, "
    "altamente rentable y ecológicamente comprometida.\n\n"
    "La inversión inicial de $28,480 MXN y el gasto operativo de $4,850 MXN mensuales se amortizan con creces mediante la reducción del 85 % en mermas "
    "de café, la aceleración de cobro en barra y el ahorro de más de $36,000 MXN anuales frente al licenciamiento privativo. Asimismo, la vinculación "
    "con los Objetivos de Desarrollo Sostenible (ODS 8 y 12) confiere a Monchis Café una identidad ética y atractiva para las nuevas generaciones.\n\n"
    "Para nuestro equipo de estudiantes de Ingeniería en Computación de la Universidad de Guadalajara, este proyecto consolida un aprendizaje fundamental: "
    "el verdadero ingeniero de software trasciende la escritura de código para convertirse en un estratega y arquitecto de servicios capaz de entregar "
    "soluciones tecnológicas confiables, viables y transformadoras para su comunidad."
)

# Sección 5: Referencias
add_heading_1("5. Referencias Bibliográficas")
referencias = [
    "AXELOS. (2019). ITIL foundation: ITIL 4 edition. TSO (The Stationery Office).",
    "Bass, L., Weber, I., & Zhu, L. (2015). DevOps: A software architect's perspective. Addison-Wesley.",
    "International Organization for Standardization, & International Electrotechnical Commission. (2018). Information technology — Service management — Part 1: Service management system requirements (ISO/IEC Standard No. 20000-1:2018). ISO/IEC. https://www.iso.org/standard/70636.html",
    "International Organization for Standardization, & International Electrotechnical Commission. (2022). Information security, cybersecurity and privacy protection — Information security management systems — Requirements (ISO/IEC Standard No. 27001:2022). ISO/IEC. https://www.iso.org/standard/82875.html",
    "Kerzner, H. (2022). Project management: A systems approach to planning, scheduling, and controlling (13th ed.). John Wiley & Sons.",
    "Kim, G., Humble, J., Debois, P., & Willis, J. (2016). The DevOps handbook: How to create world-class agility, reliability, and security in technology organizations. IT Revolution Press.",
    "Newman, S. (2021). Building microservices: Designing fine-grained systems (2nd ed.). O'Reilly Media.",
    "Steinberg, R. (2011). ITIL service strategy (2011 ed.). TSO (The Stationery Office).",
    "Van Bon, J., de Jong, A., Kolthof, A., Pieper, M., Tjassing, R., van der Veen, A., & Verheijen, T. (2008). IT service management: An introduction based on ITIL V3. Van Haren Publishing."
]

for ref_text in referencias:
    p_ref = doc.add_paragraph(ref_text)
    p_ref.paragraph_format.line_spacing = 1.15
    p_ref.paragraph_format.left_indent = Inches(0.5)
    p_ref.paragraph_format.first_line_indent = Inches(-0.5)
    p_ref.paragraph_format.space_before = Pt(0)
    p_ref.paragraph_format.space_after = Pt(6)
    p_ref.runs[0].font.name = 'Arial'
    p_ref.runs[0].font.size = Pt(10)

docx_path = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.docx"
doc.save(docx_path)
print(f"Documento Word (.docx) guardado en: {docx_path}")

# =========================================================================
# GENERACIÓN DE PLANTILLA HTML EDITORIAL Y COMPILACIÓN A PDF (CHROME HEADLESS)
# =========================================================================
html_path = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.html"
pdf_repo = r"d:\ernestofm\Proyecto\docs\entregables\Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.pdf"
pdf_downloads = r"C:\Users\erfierro\Downloads\Actividad_Participacion_Estrategia_Servicios_TI_MonchisCafe.pdf"

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Actividad PARTICIPACIÓN: Diseño de Estrategia de Servicios TI - Monchis Café</title>
<style>
  @page {{
    size: letter;
    margin: 22mm 20mm 22mm 20mm;
    @bottom-center {{
      content: counter(page);
      font-family: Arial, sans-serif;
      font-size: 10pt;
      color: #718096;
    }}
  }}
  @page landscape-section {{
    size: letter landscape;
    margin: 18mm 15mm 18mm 15mm;
    @bottom-center {{
      content: counter(page);
      font-family: Arial, sans-serif;
      font-size: 10pt;
      color: #718096;
    }}
  }}
  body {{
    font-family: Arial, Helvetica, sans-serif;
    color: #1a202c;
    line-height: 1.45;
    font-size: 10.5pt;
    margin: 0;
    padding: 0;
  }}
  h1 {{
    font-size: 15pt;
    color: #1a365d;
    border-bottom: 2px solid #2b4c7e;
    padding-bottom: 5px;
    margin-top: 24px;
    margin-bottom: 12px;
    page-break-after: avoid;
  }}
  h2 {{
    font-size: 12.5pt;
    color: #2b4c7e;
    margin-top: 18px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }}
  h3 {{
    font-size: 11pt;
    color: #2c5282;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}
  p {{
    margin-top: 0;
    margin-bottom: 10px;
    text-align: justify;
  }}
  .cover {{
    text-align: center;
    page-break-after: always;
    padding-top: 35px;
  }}
  .cover-inst {{
    font-size: 12.5pt;
    font-weight: bold;
    color: #1a202c;
    line-height: 1.4;
    margin-bottom: 50px;
  }}
  .cover-title {{
    font-size: 17pt;
    font-weight: bold;
    color: #1a365d;
    line-height: 1.3;
    margin-bottom: 25px;
  }}
  .cover-sub {{
    font-size: 12.5pt;
    font-weight: bold;
    color: #744210;
    background: #fefcbf;
    display: inline-block;
    padding: 6px 18px;
    border-radius: 4px;
    border: 1px solid #d69e2e;
    margin-bottom: 60px;
  }}
  .cover-meta {{
    font-size: 10.5pt;
    color: #2d3748;
    line-height: 1.6;
    max-width: 650px;
    margin: 0 auto;
    text-align: left;
    background: #f7fafc;
    padding: 20px 30px;
    border-left: 4px solid #2b4c7e;
    border-radius: 4px;
  }}
  .cover-meta strong {{
    color: #1a365d;
  }}
  .page-break {{
    page-break-after: always;
  }}
  .toc {{
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 18px 24px;
    margin-bottom: 20px;
  }}
  .toc-row {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 7px;
    font-size: 10.5pt;
  }}
  .toc-row.main {{
    font-weight: bold;
    color: #1a365d;
    margin-top: 8px;
    border-bottom: 1px dashed #cbd5e0;
    padding-bottom: 2px;
  }}
  .toc-row.sub {{
    padding-left: 20px;
    color: #4a5568;
    font-size: 10pt;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
    margin-bottom: 16px;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #cbd5e0;
    padding: 8px 10px;
    text-align: left;
    vertical-align: top;
  }}
  th {{
    background-color: #2b4c7e;
    color: #ffffff;
    font-weight: bold;
    font-size: 9.5pt;
  }}
  tr:nth-child(even) {{
    background-color: #f7fafc;
  }}
  .diagram-box {{
    background: #f7fafc;
    border: 1px solid #cbd5e0;
    border-left: 4px solid #2b4c7e;
    padding: 12px 16px;
    font-family: "Courier New", Courier, monospace;
    font-size: 9pt;
    line-height: 1.35;
    white-space: pre;
    overflow-x: auto;
    margin: 14px 0;
    color: #2d3748;
    border-radius: 4px;
  }}
  .highlight-card {{
    background: #ebf8ff;
    border: 1px solid #bee3f8;
    border-left: 4px solid #3182ce;
    padding: 12px 16px;
    border-radius: 4px;
    margin: 12px 0;
  }}
  .highlight-card strong {{
    color: #2b6cb0;
  }}
  .ref-item {{
    padding-left: 35px;
    text-indent: -35px;
    margin-bottom: 10px;
    font-size: 10pt;
    text-align: justify;
  }}
</style>
</head>
<body>

<!-- PORTADA -->
<div class="cover">
  <div class="cover-inst">
    UNIVERSIDAD DE GUADALAJARA<br>
    Centro Universitario de Tonalá (CUTonalá)<br>
    División de Ingenierías e Innovación Tecnológica<br>
    Licenciatura en Ingeniería en Computación
  </div>
  
  <div class="cover-title">
    ACTIVIDAD PARTICIPACIÓN<br>
    DISEÑO DE ESTRATEGIA DE SERVICIOS TI
  </div>
  
  <div class="cover-sub">
    Proyecto Final: Plataforma Web Integral y Sistema de Gestión de Servicios "Monchis Café"
  </div>
  
  <div class="cover-meta">
    <p style="margin: 4px 0;"><strong>Cátedra:</strong> Gestión de Servicios Informáticos</p>
    <p style="margin: 4px 0;"><strong>Docente:</strong> Dr. Gabriel Navarro Salcedo</p>
    <p style="margin: 12px 0 4px 0;"><strong>Equipo de Proyecto:</strong></p>
    <p style="margin: 2px 0 2px 15px;">• <strong>Ernesto Hatuey Fierro Medina</strong> (Código: 215487963) — <em>Líder y Arquitecto de Servicios TI</em></p>
    <p style="margin: 2px 0 2px 15px;">• <strong>Jazmín Díaz</strong> — <em>Diseño de Servicios y Requerimientos</em></p>
    <p style="margin: 2px 0 2px 15px;">• <strong>Héctor Hernández</strong> — <em>Especialista en Infraestructura y Operación TI</em></p>
    <p style="margin: 2px 0 2px 15px;">• <strong>Oswaldo Millán</strong> — <em>Especialista en Transición y Calidad de Software</em></p>
    <p style="margin: 12px 0 4px 0;"><strong>Fecha de Entrega:</strong> 17 de octubre de 2026 | <strong>Ciclo Escolar:</strong> 2026-B</p>
  </div>
</div>

<!-- ÍNDICE -->
<h1>Índice General</h1>
<div class="toc">
  <div class="toc-row main"><span>1. Introducción y Marco de Gestión de Servicios TI</span><span>3</span></div>
  <div class="toc-row main"><span>2. Desarrollo de la Estrategia de Servicios TI</span><span>4</span></div>
  <div class="toc-row sub"><span>2.1. ¿Qué servicios debemos ofrecer? (Portafolio y Catálogo de Servicios)</span><span>4</span></div>
  <div class="toc-row sub"><span>2.2. ¿Cuál es su valor? (Definición de Valor: Utilidad y Garantía)</span><span>6</span></div>
  <div class="toc-row sub"><span>2.3. ¿Cuáles son los resultados esperados? (Metas Cualitativas y Cuantitativas)</span><span>7</span></div>
  <div class="toc-row sub"><span>2.4. ¿Cuáles son nuestros clientes potenciales? (Segmentación y Perfiles de Mercado)</span><span>8</span></div>
  <div class="toc-row sub"><span>2.5. ¿Qué servicios son prioritarios? (Matriz de Priorización Estratégica)</span><span>9</span></div>
  <div class="toc-row sub"><span>2.6. ¿Qué inversiones son necesarias? (Presupuesto y Recursos Financieros)</span><span>10</span></div>
  <div class="toc-row sub"><span>2.7. ¿Qué servicios existen en el mercado que representen competencia directa? (Benchmarking)</span><span>11</span></div>
  <div class="toc-row sub"><span>2.8. ¿Cómo podemos diferenciarnos de la competencia? (Propuesta de Valor Única)</span><span>12</span></div>
  <div class="toc-row main"><span>3. Articulación de la Estrategia en las Fases del Ciclo de Vida del Servicio TI (ITIL)</span><span>13</span></div>
  <div class="toc-row sub"><span>3.1. Estrategia del Servicio (Service Strategy)</span><span>13</span></div>
  <div class="toc-row sub"><span>3.2. Diseño del Servicio (Service Design)</span><span>13</span></div>
  <div class="toc-row sub"><span>3.3. Transición del Servicio (Service Transition)</span><span>14</span></div>
  <div class="toc-row sub"><span>3.4. Operación del Servicio (Service Operation)</span><span>14</span></div>
  <div class="toc-row sub"><span>3.5. Mejora Continua del Servicio (Continual Service Improvement)</span><span>15</span></div>
  <div class="toc-row main"><span>4. Conclusiones Generales</span><span>16</span></div>
  <div class="toc-row main"><span>5. Referencias Bibliográficas (APA 7.ª edición)</span><span>17</span></div>
</div>

<div class="page-break"></div>

<!-- 1. INTRODUCCIÓN -->
<h1>1. Introducción y Marco de Gestión de Servicios TI</h1>
<p>
  En la actualidad, las tecnologías de información han dejado de ser meras herramientas de soporte administrativo para convertirse en el núcleo estratégico que habilita, transforma y potencia los modelos de negocio. Bajo los principios de la Gestión de Servicios de Tecnologías de la Información (ITSM), formalizados en marcos de referencia reconocidos globalmente como <strong>ITIL (Information Technology Infrastructure Library)</strong> y el estándar internacional <strong>ISO/IEC 20000-1:2018</strong>, un servicio de TI se define como un medio para entregar valor a los clientes facilitando los resultados que ellos desean alcanzar, sin que estos deban asumir de forma directa la propiedad de costos y riesgos específicos (AXELOS, 2019; ISO/IEC, 2018).
</p>
<p>
  El presente documento expone la <strong>Estrategia Integral de Servicios TI</strong> diseñada por el equipo de proyecto para <strong>Monchis Café</strong>, una empresa gastronómica regional especializada en café orgánico de cooperativas campesinas y productos comerciales complementarios. La estrategia no se limita a describir un paquete de software aislado; por el contrario, estructura un <strong>ecosistema de servicios gestionados</strong> que articula las cinco fases del ciclo de vida de los servicios TI (Estrategia, Diseño, Transición, Operación y Mejora Continua). Con ello, se garantiza que la inversión tecnológica responda directamente a las necesidades del negocio en barra, a la sostenibilidad ecológica (alineada a los Objetivos de Desarrollo Sostenible de la ONU: ODS 8, 9, 12 y 16) y a una experiencia omnicanal superior para el comensal contemporáneo.
</p>

<!-- 2. DESARROLLO DE LA ESTRATEGIA -->
<h1>2. Desarrollo de la Estrategia de Servicios TI</h1>

<h2>2.1. ¿Qué servicios debemos ofrecer? (Portafolio y Catálogo de Servicios)</h2>
<p>
  Para estructurar la oferta tecnológica, adoptamos la metodología de catálogo de servicios de ITIL v3 e ITIL 4, clasificando los servicios en tres niveles complementarios: <strong>Servicios Principales (Core)</strong>, <strong>Servicios Habilitadores (Enabling)</strong> y <strong>Servicios de Soporte y Garantía (Support & Enhancing)</strong>. Esta taxonomía permite visibilizar con claridad qué percibe el cliente final y qué capas de infraestructura, mensajería y seguridad sustentan la operación ininterrumpida de la cafetería.
</p>

<div class="diagram-box">
                    ┌────────────────────────────────────────────────────────┐
                    │               CATÁLOGO DE SERVICIOS TI                 │
                    │                    "MONCHIS CAFÉ"                      │
                    └────────────────────────────────────────────────────────┘
                                                 │
         ┌───────────────────────────────────────┼──────────────────────────────────────┐
         ▼                                       ▼                                      ▼
┌─────────────────────────────┐   ┌─────────────────────────────┐   ┌─────────────────────────────┐
│    SERVICIOS PRINCIPALES    │   │    SERVICIOS HABILITADORES  │   │    SERVICIOS DE SOPORTE     │
│           (CORE)            │   │         (ENABLING)          │   │         (SUPPORT)           │
├─────────────────────────────┤   ├─────────────────────────────┤   ├─────────────────────────────┤
│ 1. Punto de Venta Táctil    │   │ 4. Plataforma Cloud &       │   │ 7. Mesa de Ayuda y Soporte  │
│    (POS) Omnicanal          │   │    Mensajería RabbitMQ      │   │    Técnico en Sitio/Remoto  │
│ 2. Trazabilidad de Café     │   │ 5. Gestión de Datos y       │   │ 8. Continuidad y Copias de  │
│    Orgánico y Lotes         │   │    Almacenamiento Seguro    │   │    Seguridad Automatizadas  │
│ 3. Fidelización y Monedero  │   │ 6. Seguridad Perimetral,    │   │ 9. Monitoreo Proactivo y    │
│    Digital (Monchis Rewards)│   │    Auth Stateless & 2FA     │   │    Alertamiento en Tiempo R.│
└─────────────────────────────┘   └─────────────────────────────┘   └─────────────────────────────┘
</div>

<p><strong>A. Servicios Principales (Core Services):</strong></p>
<p>
  <strong>1. Servicio de Punto de Venta Táctil (POS) Omnicanal y Procesamiento Multimodal de Pagos:</strong> Interfaz interactiva de alta velocidad optimizada para tabletas de barra (Vue 3 SPA). Facilita el registro inmediato de comandas, cobro mixto (efectivo con cálculo automatizado de cambio, tarjetas mediante pasarelas Stripe/Clip/Mercado Pago, transferencias electrónicas SPEI con clave de rastreo bancaria) y emisión de tickets térmicos de 80 mm y recibos digitales.<br>
  <em>Justificación:</em> Constituye el motor generador de ingresos de la cafetería. Una demora en caja destruye la experiencia del cliente y provoca pérdidas de venta directa.
</p>
<p>
  <strong>2. Servicio de Trazabilidad Integral de Café Orgánico y Gestión PEPS de Almacén:</strong> Registro granular de cada lote de café en grano recibido desde cooperativas productoras (origen geográfico, finca, altitud, perfil de tueste, fecha de tostado y caducidad). Implementa rotación estricta PEPS (Primeras Entradas, Primeras Salidas) y genera códigos QR para que los comensales consulten en su smartphone el origen del grano servido en su taza.<br>
  <em>Justificación:</em> La propuesta de valor de Monchis Café radica en el café orgánico de especialidad. Sin trazabilidad digitalizada, existe el riesgo de vender grano envejecido o perder la certificación de procedencia.
</p>
<p>
  <strong>3. Servicio de Fidelización y Monedero Digital ("Monchis Rewards"):</strong> Tarjeta digital de sellos (8.ª bebida gratis tras 7 consumos acumulados), monedero de cashback (1 punto por cada $10 MXN gastados) y bonificación ecológica directa de $5.00 MXN al cliente que lleve termo o taza reutilizable (alineado al ODS 12).<br>
  <em>Justificación:</em> Retener a un cliente cuesta una fracción de lo que cuesta adquirir uno nuevo. En el rubro gastronómico local, la fidelización digital gamificada crea barreras contra la competencia directa.
</p>

<p><strong>B. Servicios Habilitadores e Infraestructura (Enabling Services):</strong></p>
<p>
  <strong>4. Servicio de Plataforma Cloud y Orquestación Asíncrona (RabbitMQ + Patrón Saga):</strong> Infraestructura contenerizada bajo Docker y orquestación de transacciones distribuidas. Cuando una venta concurrente se procesa en barra y el inventario de un insumo se agota, el broker ejecuta transacciones compensatorias automáticas (reversas inmediatas) y desvía fallos a la Dead Letter Queue (DLQ) con alerta administrativa por SMTP.<br>
  <em>Justificación:</em> Previene ventas de insumos no disponibles y garantiza consistencia transaccional aun durante picos de demanda en horas punta matutinas.
</p>
<p>
  <strong>5. Servicio de Almacenamiento Seguro y Persistencia Transaccional (PostgreSQL + Prisma):</strong> Almacenamiento relacional estructurado con integridad referencial estricta, consultas parametrizadas contra inyecciones SQL y particionamiento lógico de catálogos comerciales frente a insumos de especialidad.<br>
  <em>Justificación:</em> Garantiza confidencialidad, no repudio y precisión matemática en los registros contables y fiscales del negocio.
</p>
<p>
  <strong>6. Servicio de Seguridad Perimetral, Autenticación Stateless y Control de Acceso (RBAC):</strong> Autenticación basada en JWT rotativos con Refresh Token en cookies <code>httpOnly + Secure + SameSite=Strict</code>, validación anti-bots con Google reCAPTCHA v2/v3, doble factor de autenticación (2FA) para roles gerenciales y auditoría de accesos.<br>
  <em>Justificación:</em> Protege los fondos de caja, los datos personales de clientes (LFPDPPP) y previene accesos indebidos desde terminales no autorizadas.
</p>

<p><strong>C. Servicios de Soporte y Operación (Support Services):</strong></p>
<p>
  <strong>7. Mesa de Ayuda (Service Desk) y Soporte Técnico Continuo (Nivel 1 y 2):</strong> Canal de asistencia remota e inmediata para cajeros y administradores ante incidencias de periféricos (impresoras trabadas, escáneres ópticos) o bloqueos del software bajo acuerdo de nivel de servicio (SLA).<br>
  <strong>8. Respaldo Automatizado y Recuperación ante Desastres (Disaster Recovery):</strong> Respaldos incrementales automatizados diarios y volcados completos semanales cifrados en la nube, con tiempo objetivo de recuperación (RTO) menor a 60 minutos.<br>
  <strong>9. Monitoreo Proactivo de Salud y Telemetría:</strong> Vigilancia continua del estado del servidor (/api/health), latencia de base de datos y colas muertas de mensajería (DLQ), disparando alertas SMTP antes de que un fallo impacte al comensal.
</p>

<h2>2.2. ¿Cuál es su valor? (Definición de Valor: Utilidad y Garantía)</h2>
<p>
  Siguiendo el principio fundamental de ITIL, <strong>el valor no reside en la tecnología misma, sino en la percepción de los resultados habilitados para el cliente</strong>. El valor se compone de dos factores inseparables: <strong>Utilidad (<em>Fit for Purpose</em>)</strong> —lo que el servicio hace para eliminar restricciones y mejorar el rendimiento— y <strong>Garantía (<em>Fit for Use</em>)</strong> —la certeza de que el servicio estará disponible, tendrá la capacidad adecuada, será continuo y mantendrá la seguridad— (AXELOS, 2019; Steinberg, 2011).
</p>

<div class="diagram-box">
                      ┌────────────────────────────────────────┐
                      │          CREACIÓN DE VALOR TI          │
                      │             (VALOR TOTAL)              │
                      └────────────────────────────────────────┘
                                           │
                ┌──────────────────────────┴──────────────────────────┐
                ▼                                                     ▼
    ┌─────────────────────────┐                           ┌─────────────────────────┐
    │  UTILIDAD DEL SERVICIO  │                           │  GARANTÍA DEL SERVICIO  │
    │   ("Fit for Purpose")   │                           │     ("Fit for Use")     │
    ├─────────────────────────┤                           ├─────────────────────────┤
    │ • Elimina cuellos de    │                           │ • Disponibilidad 99.9%  │
    │   botella en caja.      │                           │ • Transacciones seguras │
    │ • Trazabilidad de café  │                           │   (Stateless JWT + 2FA) │
    │   orgánico certificable.│                           │ • Resiliencia con Saga  │
    │ • Fidelización activa   │                           │   (Reversas automáticas)│
    │   y monetizable.        │                           │ • Recuperación RTO < 1h │
    └─────────────────────────┘                           └─────────────────────────┘
</div>

<p>
  <strong>Aportes Concretos a la Productividad:</strong> La interfaz táctil con pre-cálculo de cambio e integración de lectores ópticos reduce el tiempo promedio de atención por cliente de 2.5 minutos a menos de 45 segundos, permitiendo atender hasta un 60 % más de clientes en horas pico matutinas sin aumentar el personal de mostrador. Asimismo, el corte de caja automatizado elimina entre 40 y 60 minutos diarios de conteo manual, garantizando precisión contable absoluta.<br>
  <strong>Reducción de Costos y Mermas:</strong> Al desplegar un sistema modular contenerizado en la nube en lugar de pagar licencias privativas por cada terminal de trabajo, se ahorran más de $36,000 MXN anuales en suscripciones de software cerrado. Además, el control PEPS de insumos orgánicos previene la pérdida de grano por envejecimiento, reduciendo el desperdicio en un 85 %.<br>
  <strong>Diferenciación y Fidelización Sostenible:</strong> La bonificación directa por termo reusable atrae al público ecoconsciente y reduce el gasto en vasos desechables, mientras que la atribución de tráfico UTM permite a la gerencia comprobar si sus clientes provienen de recomendaciones en Google Maps o de anuncios en Instagram, optimizando la inversión en marketing.
</p>

<h2>2.3. ¿Cuáles son los resultados esperados? (Metas Cualitativas y Cuantitativas)</h2>
<p>
  Para asegurar que la estrategia sea evaluable conforme a la fase de Mejora Continua de ITIL, establecemos metas cualitativas y cuantitativas vinculadas a Factores Críticos de Éxito (CSFs) e Indicadores Clave de Desempeño (KPIs):
</p>

<table>
  <thead>
    <tr>
      <th style="width: 18%;">Dimensión</th>
      <th style="width: 25%;">Factor Crítico de Éxito (CSF)</th>
      <th style="width: 27%;">Métrica / Indicador Clave (KPI)</th>
      <th style="width: 15%;">Meta Cuantitativa</th>
      <th style="width: 15%;">Meta Cualitativa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Operación en Barra</strong></td>
      <td>Velocidad y fluidez en cobro</td>
      <td>Tiempo Medio de Atención en Caja (<em>Service Time</em>)</td>
      <td><strong>&le; 45 seg</strong> / cliente</td>
      <td>Servicio sin filas; imagen ágil y moderna.</td>
    </tr>
    <tr>
      <td><strong>Desempeño Técnico</strong></td>
      <td>Rapidez de respuesta del sistema</td>
      <td>Latencia de endpoints POS (Percentil 95)</td>
      <td><strong>&le; 400 ms</strong></td>
      <td>Sensación de inmediatez táctil en pantalla.</td>
    </tr>
    <tr>
      <td><strong>Disponibilidad</strong></td>
      <td>Continuidad en horario comercial</td>
      <td>Tiempo de Actividad (<em>System Uptime</em>)</td>
      <td><strong>&ge; 99.9 %</strong></td>
      <td>Confianza total: la caja nunca se "cae".</td>
    </tr>
    <tr>
      <td><strong>Fiabilidad Transaccional</strong></td>
      <td>Consistencia de cobro e inventario</td>
      <td>Tasa de inconsistencias transaccionales</td>
      <td><strong>0.0 %</strong> (Saga/DLQ)</td>
      <td>Cero disputas por cobros de insumos agotados.</td>
    </tr>
    <tr>
      <td><strong>Fidelización</strong></td>
      <td>Retención y recompra</td>
      <td>Adopción de Monchis Rewards</td>
      <td><strong>&ge; 40 %</strong> de frecuentes</td>
      <td>Sentido de recompensa y pertenencia a la marca.</td>
    </tr>
    <tr>
      <td><strong>Sostenibilidad</strong></td>
      <td>Reducción de residuos (ODS 12)</td>
      <td>Pedidos servidos en termo/taza reusable</td>
      <td><strong>&ge; 25 %</strong> del volumen</td>
      <td>Reputación de Monchis Café como líder ecológico.</td>
    </tr>
    <tr>
      <td><strong>Soporte TI</strong></td>
      <td>Resolución expedita de fallos</td>
      <td>Tiempo Medio de Resolución (<em>MTTR</em>)</td>
      <td><strong>&le; 60 min</strong></td>
      <td>Tranquilidad operativa del personal de barra.</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<h2>2.4. ¿Cuáles son nuestros clientes potenciales? (Segmentación y Perfiles de Mercado)</h2>
<p>
  La estrategia contempla una segmentación dual que atiende tanto al cliente final que consume en barra como al personal operativo interno y a potenciales microempresas del sector gastronómico interesadas en adoptar este modelo de servicios:
</p>
<p>
  • <strong>Consumidores de Café de Especialidad y Profesionales Locales (Segmento Externo):</strong> Comensales de 22 a 55 años con afinidad por el café artesanal y el trabajo remoto. Demandan rapidez de pago (contactless, SPEI), menús interactivos donde consultar notas de cata y origen del café, y un sistema de sellos digitales sin plásticos contaminantes.<br>
  • <strong>Productores y Cooperativas Campesinas Regionales (Socios de Valor):</strong> Pequeños productores que buscan un trato justo y visibilidad comercial. Valoran que su finca, altitud y método de cultivo sean destacados ante el comensal mediante códigos QR en cada orden.<br>
  • <strong>Personal Operativo y Gerencia de Monchis Café (Clientes Internos):</strong> Cajeros y baristas que requieren una herramienta táctil a prueba de errores humanos, y administradores que necesitan auditorías claras de flujo de caja, control de mermas y métricas de retorno de inversión de marketing.<br>
  • <strong>Micro y Pequeñas Cafeterías Independientes (Potencial Expansión SaaS):</strong> Establecimientos de 1 a 3 sucursales en ciudades intermedias desatendidos por el software ERP masivo (demasiado costoso) y frustrados por terminales bancarias básicas que no controlan insumos ni trazabilidad orgánica.
</p>

<h2>2.5. ¿Qué servicios son prioritarios? (Matriz de Priorización Estratégica)</h2>
<p>
  Aplicando criterios de impacto en la continuidad operativa y viabilidad técnica, se estructuró la siguiente matriz de priorización:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 15%;">Prioridad</th>
      <th style="width: 25%;">Servicio TI</th>
      <th style="width: 35%;">Justificación Estratégica</th>
      <th style="width: 25%;">Despliegue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>P1 (Crítica)</strong></td>
      <td>POS Táctil & Procesamiento de Pagos</td>
      <td>Núcleo vital generador de ingresos. Sin él no es posible cobrar ni operar legalmente.</td>
      <td>Fase 1 (Semanas 1–3)</td>
    </tr>
    <tr>
      <td><strong>P1 (Crítica)</strong></td>
      <td>Seguridad Stateless & Autenticación RBAC</td>
      <td>Protege las transacciones financieras y restringe accesos administrativos desde el arranque.</td>
      <td>Fase 1 (Semanas 2–4)</td>
    </tr>
    <tr>
      <td><strong>P2 (Alta)</strong></td>
      <td>Trazabilidad de Café Orgánico y PEPS</td>
      <td>Sustenta la propuesta de valor del café de especialidad y previene pérdidas por caducidad.</td>
      <td>Fase 2 (Semanas 5–7)</td>
    </tr>
    <tr>
      <td><strong>P2 (Alta)</strong></td>
      <td>Infraestructura Resiliente (RabbitMQ Saga)</td>
      <td>Blinda las transacciones concurrentes evitando desajustes entre cobro e inventario.</td>
      <td>Fase 2 (Semanas 6–8)</td>
    </tr>
    <tr>
      <td><strong>P3 (Media)</strong></td>
      <td>Fidelización Monchis Rewards (ODS 12)</td>
      <td>Impulsa la retención y la comunidad ecológica una vez estabilizado el flujo transaccional.</td>
      <td>Fase 3 (Semanas 9–11)</td>
    </tr>
    <tr>
      <td><strong>P3 (Media)</strong></td>
      <td>Panel Analítico & Atribución UTM</td>
      <td>Permite a la gerencia optimizar el gasto publicitario en Google Maps e Instagram.</td>
      <td>Fase 3 (Semanas 10–12)</td>
    </tr>
    <tr>
      <td><strong>P4 (Soporte)</strong></td>
      <td>Mesa de Ayuda, Monitoreo y Backups</td>
      <td>Garantiza la continuidad operativa, soporte a usuarios y recuperación ante desastres.</td>
      <td>Fase 4 (Transversal)</td>
    </tr>
  </tbody>
</table>

<h2>2.6. ¿Qué inversiones son necesarias? (Presupuesto y Recursos Financieros)</h2>
<p>
  La implementación y operación de la estrategia demanda una inversión inicial en activos (CAPEX) de <strong>$28,480 MXN</strong> y un gasto operativo mensual (OPEX) de <strong>$4,850 MXN</strong>, logrando un balance financiero altamente rentable:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 22%;">Rubro de Inversión</th>
      <th style="width: 38%;">Componente y Especificación</th>
      <th style="width: 12%;">Tipo</th>
      <th style="width: 14%;">Inversión Inicial</th>
      <th style="width: 14%;">Gasto Mensual</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Hardware en Barra</strong></td>
      <td>2 Tabletas industriales táctiles 10.5" Android con soporte de seguridad</td>
      <td>CAPEX</td>
      <td>$12,500 MXN</td>
      <td>$0 MXN</td>
    </tr>
    <tr>
      <td><strong>Hardware Periférico</strong></td>
      <td>2 Impresoras térmicas 80 mm + 2 Lectores de código 1D/2D</td>
      <td>CAPEX</td>
      <td>$7,800 MXN</td>
      <td>$0 MXN</td>
    </tr>
    <tr>
      <td><strong>Infraestructura Cloud</strong></td>
      <td>Servidor Virtual en GCP / Cloud Run para Backend y RabbitMQ</td>
      <td>OPEX</td>
      <td>$0 MXN</td>
      <td>$650 MXN</td>
    </tr>
    <tr>
      <td><strong>Base de Datos Cloud</strong></td>
      <td>Instancia administrada PostgreSQL con backups diarios cifrados</td>
      <td>OPEX</td>
      <td>$0 MXN</td>
      <td>$450 MXN</td>
    </tr>
    <tr>
      <td><strong>Dominio y Red (CDN)</strong></td>
      <td>Dominio .com.mx, SSL/TLS Let's Encrypt y Cloudflare CDN seguro</td>
      <td>CAPEX / OPEX</td>
      <td>$680 MXN (anual)</td>
      <td>$0 MXN</td>
    </tr>
    <tr>
      <td><strong>Servicio SMTP / DLQ</strong></td>
      <td>Pasarela de correo transaccional para alertas Saga y DLQ</td>
      <td>OPEX</td>
      <td>$0 MXN</td>
      <td>$250 MXN</td>
    </tr>
    <tr>
      <td><strong>Capacitación Operativa</strong></td>
      <td>Talleres prácticos para cajeros y baristas en barra (Nivel 0)</td>
      <td>CAPEX</td>
      <td>$3,500 MXN</td>
      <td>$0 MXN</td>
    </tr>
    <tr>
      <td><strong>Soporte y Operación</strong></td>
      <td>Mesa de ayuda remota Nivel 1/2, monitoreo y mantenimiento mensual</td>
      <td>OPEX</td>
      <td>$0 MXN</td>
      <td>$3,500 MXN</td>
    </tr>
    <tr>
      <td><strong>Fondo Contingencia</strong></td>
      <td>Reserva financiera para refacciones de conectividad y hardware</td>
      <td>CAPEX</td>
      <td>$4,000 MXN</td>
      <td>$0 MXN</td>
    </tr>
    <tr style="font-weight: bold; background-color: #e2e8f0;">
      <td colspan="3">TOTALES CONSOLIDADOS (INVERSIÓN INICIAL Y COSTO OPERATIVO MENSUAL)</td>
      <td>$28,480 MXN</td>
      <td>$4,850 MXN / mes</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<h2>2.7. ¿Qué servicios existen en el mercado que representen competencia directa? (Benchmarking)</h2>
<p>
  Para dimensionar la competitividad de Monchis Café, realizamos una comparación directa frente a las tres alternativas más utilizadas en el sector restaurantero mexicano:
</p>

<table>
  <thead>
    <tr>
      <th style="width: 20%;">Parámetro</th>
      <th style="width: 25%;">Soft Restaurant (Nacional)</th>
      <th style="width: 25%;">Toast POS / Square (Global)</th>
      <th style="width: 30%;">Estrategia "Monchis Café"</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Modelo de Costos</strong></td>
      <td>Licencia tradicional costosa (desde $14,000 MXN) + cobro por póliza de soporte.</td>
      <td>Renta mensual elevada ($69–$165 USD/mes) + comisiones bancarias cautivas.</td>
      <td><strong>Bajo OPEX ($4,850 MXN infra total), sin rentas de software por asiento ni ataduras comerciales.</strong></td>
    </tr>
    <tr>
      <td><strong>Trazabilidad de Café</strong></td>
      <td>Nula o muy genérica (solo descuento simple de insumos generales).</td>
      <td>Inexistente (inventario genérico de platillos sin procedencia campesina).</td>
      <td><strong>Nativa: Finca, altitud, lote, perfil de tueste, rotación PEPS y código QR al comensal.</strong></td>
    </tr>
    <tr>
      <td><strong>Resiliencia Técnica</strong></td>
      <td>Bloqueos de base de datos local y descuadres ante caídas de red.</td>
      <td>Dependencia absoluta de conexión a la nube del proveedor externo.</td>
      <td><strong>Avanzada: Patrón Saga con RabbitMQ, reversas automáticas y Dead Letter Queue auditada.</strong></td>
    </tr>
    <tr>
      <td><strong>Sostenibilidad (ODS)</strong></td>
      <td>Nula vinculación ambiental.</td>
      <td>Puntos genéricos por consumo con tarjeta.</td>
      <td><strong>Nativa: Bonificación de $5 MXN por termo/taza reusable y sellos digitales sin plásticos (ODS 12).</strong></td>
    </tr>
    <tr>
      <td><strong>SEO y Atribución</strong></td>
      <td>Inexistente; no conecta con la presencia web del negocio.</td>
      <td>Integración básica con módulos de pedidos propios.</td>
      <td><strong>Nativa: Captura de parámetros UTM (Google Maps vs Instagram) y frontend prerenderizado SEO (vite-ssg).</strong></td>
    </tr>
  </tbody>
</table>

<h2>2.8. ¿Cómo podemos diferenciarnos de la competencia? (Propuesta de Valor Única)</h2>
<p>
  La diferenciación de Monchis Café se fundamenta en cinco pilares que ninguna solución genérica del mercado ofrece de forma conjunta:
</p>
<div class="highlight-card">
  <strong>1. Especialización en Café de Especialidad y Sostenibilidad (ODS 12):</strong> A diferencia de los sistemas tradicionales que tratan el café como una mercancía genérica, nuestra plataforma modela el ciclo de vida del grano (origen cooperativo, altitud, fecha de tueste) y recompensa activamente al comensal ecológico.<br><br>
  <strong>2. Resiliencia Transaccional con Patrón Saga:</strong> Implementamos microservicios asíncronos en RabbitMQ. Si una bebida se cobra en caja pero se agota el café orgánico en almacén, el sistema ejecuta una transacción compensatoria inmediata, evitando discusiones y descuadres.<br><br>
  <strong>3. Conexión Directa entre Marketing Digital (SEO) y Caja:</strong> La plataforma prerenderizada (<code>vite-ssg</code>) posiciona la cafetería en búsquedas locales y transfiere los parámetros UTM a la cuenta del comensal para saber exactamente qué campañas de redes generan ventas en barra.<br><br>
  <strong>4. Cero Rentas Prohibitivas de Licencia:</strong> Arquitectura moderna basada en estándares abiertos que ahorra más de $36,000 MXN anuales frente al software privativo.<br><br>
  <strong>5. Soporte Técnico Hiperlocal y Calidez Humana:</strong> Asistencia técnica inmediata brindada por el equipo de ingeniería con tiempos de respuesta menores a 15 minutos en horarios críticos.
</div>

<!-- 3. ARTICULACIÓN EN FASES ITIL -->
<h1>3. Articulación de la Estrategia en las Fases del Ciclo de Vida del Servicio TI (ITIL)</h1>
<p>
  Para consolidar el enfoque de gestión de servicios, articulamos la estrategia a través de las cinco fases de ITIL (AXELOS, 2019; Steinberg, 2011):
</p>
<p>
  <strong>3.1. Estrategia del Servicio (Service Strategy):</strong> Alinea las tecnologías con el modelo de negocio de Monchis Café. Gestiona el portafolio de servicios (clasificando servicios activos frente a futuros módulos en desarrollo), modela los costos financieros y analiza la demanda para dimensionar servidores durante las horas pico matutinas (8:00 a 11:00 hrs).<br><br>
  <strong>3.2. Diseño del Servicio (Service Design):</strong> Traduce los objetivos estratégicos en soluciones técnicas concretas. Formaliza Acuerdos de Nivel de Servicio (SLA: disponibilidad &ge; 99.9 %, resolución de incidentes en barra &le; 60 min), diseña la seguridad perimetral (JWT stateless, 2FA gerencial y Google reCAPTCHA) y establece planes de continuidad del negocio (ITSCM) con respaldos diarios cifrados.<br><br>
  <strong>3.3. Transición del Servicio (Service Transition):</strong> Asegura que los servicios se desplieguen sin alterar la operación en barra. Integra pipelines automatizados de DevOps en GitHub Actions, pruebas exhaustivas TDD con Vitest, Supertest y Playwright, control riguroso de cambios mediante pull requests y capacitación práctica al personal de barra antes de la puesta en marcha.<br><br>
  <strong>3.4. Operación del Servicio (Service Operation):</strong> Garantiza la estabilidad diaria del servicio en mostrador mediante una Mesa de Ayuda (Service Desk) escalonada (Nivel 0 cajero, Nivel 1 soporte remoto, Nivel 2 ingeniería de software), gestión de eventos mediante endpoints de salud (/api/health) y resolución ágil de incidentes con monitoreo constante de colas RabbitMQ.<br><br>
  <strong>3.5. Mejora Continua del Servicio (Continual Service Improvement - CSI):</strong> Aplica el ciclo Deming (Plan-Do-Check-Act) mediante revisiones trimestrales de KPIs, encuestas de satisfacción a baristas y comensales, y optimización continua de consultas de base de datos para preservar tiempos de respuesta menores a 400 milisegundos.
</p>

<!-- 4. CONCLUSIONES -->
<h1>4. Conclusiones Generales</h1>
<p>
  El diseño de esta estrategia integral de servicios tecnológicos para <strong>Monchis Café</strong> demuestra con rigor que el valor de la informática no radica en la complejidad técnica aislada, sino en su capacidad para habilitar metas de negocio tangibles y resolver problemas humanos concretos. Articular las cinco fases de ITIL permitió transformar los obstáculos cotidianos de un establecimiento gastronómico —filas lentas en caja, descuadres contables, pérdida de frescura en insumos orgánicos y licencias comerciales asfixiantes— en una oferta de servicios diferenciada, altamente rentable y ecológicamente comprometida.
</p>
<p>
  La inversión inicial de $28,480 MXN y el gasto operativo de $4,850 MXN mensuales se amortizan con creces mediante la reducción del 85 % en mermas de café, la aceleración de cobro en barra y el ahorro de más de $36,000 MXN anuales frente al licenciamiento privativo. Asimismo, la vinculación con los Objetivos de Desarrollo Sostenible (ODS 8 y 12) confiere a Monchis Café una identidad ética y atractiva para las nuevas generaciones de consumidores. Para nuestro equipo de estudiantes de Ingeniería en Computación de la Universidad de Guadalajara, este proyecto consolida un aprendizaje fundamental: el verdadero ingeniero de software trasciende la escritura de código para convertirse en un estratega y arquitecto de servicios capaz de entregar soluciones tecnológicas confiables, viables y transformadoras para su comunidad.
</p>

<!-- 5. REFERENCIAS -->
<h1>5. Referencias Bibliográficas</h1>
<div class="ref-item">AXELOS. (2019). <i>ITIL foundation: ITIL 4 edition</i>. TSO (The Stationery Office).</div>
<div class="ref-item">Bass, L., Weber, I., & Zhu, L. (2015). <i>DevOps: A software architect's perspective</i>. Addison-Wesley.</div>
<div class="ref-item">International Organization for Standardization, & International Electrotechnical Commission. (2018). <i>Information technology — Service management — Part 1: Service management system requirements</i> (ISO/IEC Standard No. 20000-1:2018). ISO/IEC. https://www.iso.org/standard/70636.html</div>
<div class="ref-item">International Organization for Standardization, & International Electrotechnical Commission. (2022). <i>Information security, cybersecurity and privacy protection — Information security management systems — Requirements</i> (ISO/IEC Standard No. 27001:2022). ISO/IEC. https://www.iso.org/standard/82875.html</div>
<div class="ref-item">Kerzner, H. (2022). <i>Project management: A systems approach to planning, scheduling, and controlling</i> (13th ed.). John Wiley & Sons.</div>
<div class="ref-item">Kim, G., Humble, J., Debois, P., & Willis, J. (2016). <i>The DevOps handbook: How to create world-class agility, reliability, and security in technology organizations</i>. IT Revolution Press.</div>
<div class="ref-item">Newman, S. (2021). <i>Building microservices: Designing fine-grained systems</i> (2nd ed.). O'Reilly Media.</div>
<div class="ref-item">Steinberg, R. (2011). <i>ITIL service strategy</i> (2011 ed.). TSO (The Stationery Office).</div>
<div class="ref-item">Van Bon, J., de Jong, A., Kolthof, A., Pieper, M., Tjassing, R., van der Veen, A., & Verheijen, T. (2008). <i>IT service management: An introduction based on ITIL V3</i>. Van Haren Publishing.</div>

</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Plantilla HTML generada en: {html_path}")

# Compilación a PDF con Google Chrome Headless
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_repo}",
    html_path
]

print("Compilando entregable PDF con Chrome Headless...")
subprocess.run(cmd, check=True)
print(f"PDF generado exitosamente en el repositorio: {pdf_repo}")

shutil.copyfile(pdf_repo, pdf_downloads)
print(f"Copia del PDF colocada en carpeta Descargas del usuario: {pdf_downloads}")
