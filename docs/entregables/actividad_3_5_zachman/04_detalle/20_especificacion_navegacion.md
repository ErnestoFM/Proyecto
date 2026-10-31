# Nivel 4: DETALLE — Foco: CÓMO
## Especificación de Casos de Uso y Prototipo de Navegación — Monchis Café

**Proyecto:** Monchis Café (Gestión Web Segura para Cafetería Orgánica y Comercial)  
**Equipo:** Equipo 2  
**Autor:** Ernesto Hatuey Fierro Medina  
**Asignatura:** Proyecto Integrador de Desarrollo de Software  
**Profesor:** Dr. Gabriel Navarro Salcedo  
**Institución:** Centro Universitario de Tonalá — Universidad de Guadalajara  

---

### 1. Fundamento Teórico y Conceptual

En la ingeniería web y el diseño de aplicaciones interactivas, la arquitectura de navegación describe la estructura y las reglas lógicas que permiten al usuario moverse a través de las diferentes pantallas y estados del sistema sin desorientarse ni acceder a secciones no autorizadas (Garzotto et al., 1993). Como explican Pressman y Maxim (2021), el diseño de navegación no se reduce a poner enlaces en una barra superior; exige modelar los grafos de navegación (*site maps*), las rutas públicas indexables para posicionamiento en motores de búsqueda (SEO) y los guardianes de navegación (*Navigation Guards*) que interceptan y protegen las rutas privadas mediante tokens criptográficos.

Dentro de la Matriz de Zachman (1987), la celda **Detalle - Cómo** aborda la especificación física y navegacional (*Physical Process & Navigation Model / Builder's View*). En este nivel del constructor, traducimos la lógica de los casos de uso en el mapa exacto de transiciones de pantalla implementadas en **Vue Router 4** para el frontend de **Monchis Café**. Aquí se formaliza cómo viaja el usuario entre el catálogo público prerenderizado (`vite-ssg`), el punto de venta protegido (`/pos`) y el panel administrativo con autenticación de doble factor (`/admin`).

---

### 2. Mapa y Grafo de Navegación del Sistema (Vue Router)

El sistema clasifica sus pantallas en dos dominios claramente separados: **Rutas Públicas Prerenderizadas** (optimizadas para SEO con Schema.org y meta tags dinámicos) y **Rutas Privadas Protegidas** (Single Page Application con `noindex, nofollow` y guardianes RBAC):

```
+=======================================================================================+
|                             ÁRBOL DE NAVEGACIÓN WEB                                   |
+=======================================================================================+
| 1. RUTAS PÚBLICAS (Prerenderizadas con vite-ssg):                                     |
|    /                  --> Landing Page (Historia, propuesta de valor orgánico)        |
|    /menu              --> Catálogo digital de café de especialidad y alimentos        |
|    /rewards           --> Información del programa de fidelización y ODS 12           |
|    /nosotros          --> Origen de cooperativas campesinas y sustentabilidad         |
|    /contacto          --> Ubicación geográfica (Google Maps) y canales de atención    |
|    /login             --> Formulario de acceso seguro con Google reCAPTCHA            |
|    /registro          --> Alta de clientes en Rewards con captura de parámetros UTM  |
+---------------------------------------------------------------------------------------+
| 2. RUTAS PRIVADAS (Protegidas por Navigation Guards RBAC):                            |
|    /pos               --> Terminal de cobro (Requiere rol: CAJERO o ADMIN)            |
|    /admin             --> Panel gerencial (Requiere rol: ADMIN + 2FA validado)        |
|    /perfil            --> Consulta de sellos y configuración de cuenta (CLIENTE/STAFF)|
+=======================================================================================+
```

---

### 3. Diagrama de Transición de Navegación y Guardianes de Ruta

El siguiente diagrama modela cómo el guardián global de navegación (`router.beforeEach`) evalúa el estado de autenticación y los permisos del usuario antes de permitir el acceso a cada pantalla:

```
[ Visitante en Internet ]
         |
         v
+------------------+     ¿Ruta Pública? (/, /menu, /rewards)
| Petición de Ruta | -----------------------------------------> [ Carga Vista Pública (HTML SSG) ]
+------------------+
         |
         | ¿Ruta Protegida? (/pos, /admin, /perfil)
         v
+------------------------+      (NO)
| ¿Existe Access Token   | --------------> [ Redirige a /login con redirectUrl ]
| válido en Pinia Store? |
+------------------------+
         | (SÍ)
         v
+------------------------+      (NO)
| ¿El rol del usuario    | --------------> [ Redirige a /403 Prohibido o /pos ]
| cumple la matriz RBAC? |
+------------------------+
         | (SÍ)
         +---- (Si ruta es /admin y falta 2FA) ---> [ Despliega Modal Desafío TOTP ]
         |                                                    | (Código Válido)
         |                                                    v
         +----------------------------------------> [ Carga Pantalla Solicitada ]
```

---

### 4. Especificación Detallada de Eventos en Interfaz de Mostrador

Para maximizar la ergonomía y la velocidad en la terminal del Punto de Venta (`/pos`), la interacción en pantalla responde a eventos físicos y de teclado capturados globalmente:

| Evento / Atajo | Elemento de Interfaz | Acción Técnica en el Frontend | Resultado Observable en Pantalla |
| :--- | :--- | :--- | :--- |
| **Pulsación `F2`** | Teclado físico de caja | Dispara la función `posStore.cobrarOrden()` | Abre el modal de confirmación de pago y coloca el foco en el campo de efectivo. |
| **Pulsación `Escape`** | Teclado físico de caja | Dispara la función `posStore.limpiarCarrito()` | Vacia la orden en curso tras pedir confirmación rápida al cajero. |
| **Lectura de Código** | Escáner óptico USB/HID | Listener global de eventos `keydown` con buffer | Detecta el prefijo numérico (ej. `7501001`), busca el producto y lo suma a la orden en < 50 ms. |
| **Check Bono Ecológico**| Casilla táctil en orden | Activa bandera reactiva `termoReusable: true` | Descuenta -\$5.00 MXN del total o activa la notificación de sellos dobles ODS 12. |
| **Selección de Pago** | Botones de forma de pago | Modifica la variable reactiva `metodoPago` | Despliega campos específicos (cálculo de cambio para efectivo, o voucher para SPEI/Tarjeta). |
| **Expiración de Token** | Interceptor Axios/Fetch | Emite petición a `/api/auth/refresh` | Si la cookie `httpOnly` es válida, renueva el Access Token en memoria sin parpadeo de pantalla. |

---

### 5. Justificación Práctica en el Proyecto

Diseñar con rigor el prototipo y la mecánica de navegación es lo que garantiza una experiencia de usuario fluida y segura. Como señalan Garzotto et al. (1993), una aplicación web comercial no puede depender de que el usuario "adivine" cómo regresar o qué botón presionar. En Monchis Café, contar con atajos de teclado (`F2`, `Esc`) e integración nativa con lectores de códigos de barra permite que el barista atienda a toda velocidad sin tocar el ratón. Asimismo, la protección estricta mediante *Navigation Guards* asegura que ningún cliente curioso pueda asomarse al panel de administración o al punto de venta simplemente escribiendo la URL en su navegador.

---

### 6. Referencias Bibliográficas

1. **Garzotto, F., Paolini, P., & Schwabe, D. (1993).** HDM—A model-based approach to hypertext application design. *ACM Transactions on Information Systems (TOIS)*, 11(1), 1–26. https://doi.org/10.1145/151480.151483
2. **Pressman, R. S., & Maxim, B. R. (2021).** *Ingeniería de software: un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
3. **Zachman, J. A. (1987).** A framework for information systems architecture. *IBM Systems Journal*, 26(3), 276–292. https://doi.org/10.1147/sj.263.0276

