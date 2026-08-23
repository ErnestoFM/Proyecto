# Especificación Técnica: Sistema de Diseño Pastel y SEO con `vite-ssg`

## 1. Sistema de Diseño (UI/UX) — Monchis Café

La identidad de **Monchis Café** transmite calidez, dulzura y tranquilidad mediante una paleta armónica en tonos pastel que combinan el rosa suave y el café de especialidad.

### 1.1 Tokens de Color y Estilos
* **Rosa Suave (`--color-primary`):** `#F3C9C9`
* **Rosa Terracota (`--color-primary-dark`):** `#D98C7F`
* **Café con Leche (`--color-secondary`):** `#C9A88B`
* **Café Tostado (`--color-secondary-dark`):** `#8C6B52`
* **Crema Cálido (`--color-bg-base`):** `#FAF3ED`
* **Blanco Cálido (`--color-bg-surface`):** `#FFFDFB`
* **Café Oscuro Cálido (`--color-text-main`):** `#4A3B32`
* **Café Grisáceo (`--color-text-muted`):** `#8A7A6D`

### 1.2 Tipografía y Animaciones
* **Títulos:** *Poppins* / *Fraunces* (encabezados redondeados amigables).
* **Cuerpo:** *Nunito* / *Inter* (alta legibilidad en cualquier dispositivo).
* **Animaciones al Scroll:** `@vueuse/motion` para apariciones suaves y `GSAP + ScrollTrigger` para transiciones de imágenes, respetando la directiva de accesibilidad `@media (prefers-reduced-motion: reduce)`.

---

## 2. Estrategia de SEO y Prerenderizado con `vite-ssg`

### 2.1 Enfoque Técnico
Para evitar la sobrecarga de un servidor Node.js permanente para SSR y al mismo tiempo garantizar que Google indexe las páginas públicas completas:
1. **Build Time Prerendering:** `vite-ssg` genera archivos HTML precompilados para `/`, `/nosotros`, `/menu`, `/contacto`.
2. **Hidratación en Cliente:** Al cargar el HTML, Vue toma el control (SPA) permitiendo transiciones ultra rápidas sin recarga de página.
3. **Páginas Privadas Protegidas:** `/pos` y `/admin/*` se cargan puramente en cliente con `<meta name="robots" content="noindex, nofollow">`.

### 2.2 Marcado Estructurado Schema.org (`LocalBusiness` / `CoffeeShop`)
Se incluye un bloque JSON-LD dinámico en la landing con los datos de geolocalización, horarios, menú y enlace a Google Maps para maximizar el SEO local y la captación de tráfico con parámetros UTM.
