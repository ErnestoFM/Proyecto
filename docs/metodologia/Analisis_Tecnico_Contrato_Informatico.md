# Análisis Técnico y Teórico del Contrato Informático (Actividad 3.1)
**Materia:** Administración de Proyectos de Software  
**Docente:** Dr. Gabriel Navarro Salcedo  
**Proyecto:** Monchis Café  
**Equipo:** Ernesto Fierro Moreno, Jazmín Díaz, Héctor Hernández, Oswaldo Millán  

---

## 1. Elementos Formales del Contrato Informático

### 1.1 Elementos de Existencia
1. **Consentimiento:** Acuerdo mutuo expreso, manifestado formalmente por escrito o a través de medios electrónicos (Código de Comercio arts. 89-114 y Código Civil Federal art. 1803).
2. **Objeto:**
   - *Objeto Directo:* Obligaciones recíprocas de hacer (desarrollar, probar, desplegar software) y de dar (pago de honorarios y entrega de código fuente y documentación).
   - *Objeto Indirecto:* La plataforma web y punto de venta para Monchis Café.

### 1.2 Elementos de Validez
1. **Capacidad de las Partes:** Capacidad jurídica y representación legal acreditada de Soluciones Digitales Fierro & Asociados S.A.S. de C.V. y Monchis Café S. de R.L. de C.V.
2. **Ausencia de Vicios:** Exclusión de error técnico, dolo, mala fe o lesión mediante la definición explícita de requerimientos y criterios de aceptación (DoD).
3. **Licitud en el Objeto, Motivo o Fin:** Apego a la Ley Federal del Derecho de Autor (LFDA), Ley Federal de Protección de Datos Personales (LFPDPPP) y no violación de derechos de terceros ni licencias copyleft.
4. **Forma:** Formalidad escrita y onerosa exigida por el art. 30 de la LFDA para la validez de la transmisión de derechos patrimoniales sobre software.

---

## 2. Análisis del Modelo Contractual Institucional (Docente)

- **Fortalezas del modelo:** Buen régimen de retenciones y comprobación fiscal SAT; deslinde de subordinación laboral respecto a auxiliares técnicos.
- **Brechas técnicas identificadas:** Ambigüedad en la definición del software ("aplicación funcional en un host"); estipulación indebida de cesión gratuita de derechos (la LFDA exige onerosidad); ausencia de SLAs y horarios de soporte; ausencia de criterios cuantitativos de aceptación; omisión de gestión de cambios (Change Requests) y omisión de cláusulas de ciberseguridad y protección de datos.

---

## 3. Descripción Técnica del Elemento Seleccionado

- **Elemento:** *El Objeto Contractual, Entregables Técnicos y Criterios Objetivos de Aceptación (Definition of Done).*
- **Justificación Técnica:** El objeto de software es una obligación de resultado medible. En Monchis Café se articula con:
  - Arquitectura Monorepo (Vue 3 + Vite frontend con SEO prerenderizado `vite-ssg`, Next.js API Routes backend, PostgreSQL con Prisma ORM).
  - Orquestación asíncrona con **RabbitMQ y Patrón Saga** sobre `cafeteria.events`, garantizando reversas automáticas de cobro/inventario ante roturas de stock de café orgánico y colas Dead Letter Queue (DLQ).
  - Autenticación Stateless (JWT rotativo en cookies httpOnly, Google reCAPTCHA v2/v3, RBAC y 2FA).
  - Criterios de Aceptación Cuantitativos: Cobertura >80% en pruebas unitarias con Vitest, 100% suites E2E con Playwright en 3 viewports (360px, 768px, 1024px) y escaneo estático SAST libre de vulnerabilidades Críticas/Altas (CVSS/OWASP).

---

*Documento de respaldo teórico para la acreditación académica de la Actividad 3.1.*
