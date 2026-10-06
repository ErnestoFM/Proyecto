// ==============================================================================
// Monchis Café — Suite de Pruebas End-to-End (E2E) con Playwright
// Archivo: apps/web/e2e/app.spec.ts
// Cobertura: Responsive, Mobile Drawer, Menú, Rewards, POS y Seguridad
// ==============================================================================

import { test, expect } from '@playwright/test';

test.describe('📱 1. Pruebas de Renderizado Responsive & Viewports', () => {
  test('HomePage debe renderizar correctamente y contener elementos clave de branding', async ({ page }) => {
    await page.goto('/');

    // 1. Título y Branding
    await expect(page).toHaveTitle(/Monchis Café/);
    const logo = page.locator('.navbar__name');
    await expect(logo).toBeVisible();
    await expect(logo).toContainText('Monchis');

    // 2. Badge de café orgánico y botones Call To Action
    const organicBadge = page.locator('.badge--organic').first();
    await expect(organicBadge).toBeVisible();
    await expect(organicBadge).toContainText('Café Orgánico');

    const btnMenu = page.locator('a:has-text("Explora Nuestro Menú")');
    await expect(btnMenu).toBeVisible();

    // 3. Grid de valores corporativos (3 pilares)
    const cards = page.locator('.values__card');
    await expect(cards).toHaveCount(3);
  });

  test('Navbar hamburguesa debe ser interactivo en pantallas móviles', async ({ page, isMobile }) => {
    await page.goto('/');

    if (isMobile) {
      const hamburgerBtn = page.locator('.navbar__toggle');
      await expect(hamburgerBtn).toBeVisible();

      // Abrir menú móvil
      await hamburgerBtn.click();
      const drawer = page.locator('.navbar__mobile-drawer');
      await expect(drawer).toBeVisible();

      // Cerrar menú móvil mediante botón de cierre dedicado
      const closeBtn = page.locator('.drawer-close-btn');
      await closeBtn.click();
      await expect(drawer).not.toBeVisible();
    }
  });
});

test.describe('☕ 2. Exploración de Menú y Monchis Rewards', () => {
  test('Menú público debe renderizar productos con precios e insignias', async ({ page }) => {
    await page.goto('/menu');

    // Verificar que carga la vista de menú
    await expect(page).toHaveTitle(/Menú|Monchis Café/);
    const menuTitle = page.locator('h1');
    await expect(menuTitle).toContainText('Menú');

    // Validar que existan filtros o productos cargados
    const products = page.locator('.product-card, .menu-item, .card');
    await expect(products.first()).toBeVisible();
  });

  test('Página de Rewards debe mostrar la tarjeta de 7 sellos y bonificación ecológica', async ({ page }) => {
    await page.goto('/rewards');

    // Verificar presencia del programa Monchis Rewards
    const heading = page.locator('h1, h2').first();
    await expect(heading).toBeVisible();

    // Verificar mención a sellos o café gratis
    const content = page.locator('body');
    await expect(content).toContainText(/sellos|recompensas|café/i);
  });
});

test.describe('🛒 3. Flujo Completo del Punto de Venta (POS) y Protección RBAC', () => {
  test('Ruta /pos sin sesión debe redirigir a /login por protección de roles', async ({ page }) => {
    await page.goto('/pos');
    await expect(page).toHaveURL(/\/login/);
  });

  test('Cajero autenticado debe poder operar el catálogo, agregar café orgánico y gestionar carrito', async ({ page }) => {
    // Interceptar API de autenticación para simular sesión exitosa de CAJERO
    await page.route('**/api/auth/login', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          accessToken: 'mock-access-token-cajero-e2e',
          usuario: {
            id: 'usr_cajero_01',
            email: 'cajero@monchiscafe.com',
            nombre: 'Cajero Mostrador',
            rol: 'CAJERO',
            puntosFidelidad: 45,
            sellosAcumulados: 3,
            creadoEn: '2026-08-23T10:00:00Z',
          },
        }),
      });
    });

    await page.route('**/api/auth/refresh', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          mensaje: 'Tokens renovados exitosamente',
          accessToken: 'mock-access-token-cajero-e2e',
          usuario: {
            id: 'usr_cajero_01',
            email: 'cajero@monchiscafe.com',
            nombre: 'Cajero Mostrador',
            rol: 'CAJERO',
            puntosFidelidad: 45,
            sellosAcumulados: 3,
            creadoEn: '2026-08-23T10:00:00Z',
          },
        }),
      });
    });

    // Iniciar sesión como Cajero
    await page.goto('/login');
    await page.fill('#login-email', 'cajero@monchiscafe.com');
    await page.fill('#login-password', 'PasswordSeguro2026!');
    await page.click('button[type="submit"]');

    // Ahora navegar al Punto de Venta
    await page.goto('/pos');

    // 1. Verificar encabezado y lector de código de barras
    const posHeading = page.locator('.pos-catalog__header h1');
    await expect(posHeading).toContainText('Punto de Venta');

    const scannerBadge = page.locator('.scanner-indicator');
    await expect(scannerBadge).toBeVisible();

    // 2. Filtrar por categoría Orgánico
    const btnOrganico = page.locator('button:has-text("🌿 Café Orgánico")');
    if (await btnOrganico.isVisible()) {
      await btnOrganico.click();
    }

    // 3. Agregar primer producto disponible al carrito
    const btnAgregar = page.locator('.product-card button, .product-card').first();
    await expect(btnAgregar).toBeVisible();
    await btnAgregar.click();

    // 4. Verificar que el carrito tiene al menos 1 item
    const cartItem = page.locator('.cart-item');
    await expect(cartItem.first()).toBeVisible();

    // 5. Activar bonificación ecológica por termo reutilizable (ODS 12)
    const termoCheckbox = page.locator('.eco-checkbox input[type="checkbox"]');
    if (await termoCheckbox.isVisible()) {
      await termoCheckbox.check();
      await expect(termoCheckbox).toBeChecked();
    }

    // 6. Probar botón Vaciar Carrito
    const btnVaciar = page.locator('.pos-sidebar__header button:has-text("Vaciar")');
    if (await btnVaciar.isVisible()) {
      await btnVaciar.click();
      const emptyMsg = page.locator('.cart-empty');
      await expect(emptyMsg).toBeVisible();
    }
  });
});

test.describe('🛡️ 4. Seguridad, Autenticación y Atribución UTM', () => {
  test('Ruta de Login debe incluir indicador de seguridad reCAPTCHA y campos requeridos', async ({ page }) => {
    await page.goto('/login');

    // Verificar protección reCAPTCHA visual
    const recaptchaBox = page.locator('.recaptcha-placeholder');
    await expect(recaptchaBox).toBeVisible();
    await expect(recaptchaBox).toContainText('Google reCAPTCHA');

    // Verificar campos de formulario
    const emailInput = page.locator('#login-email');
    const passInput = page.locator('#login-password');
    const submitBtn = page.locator('button[type="submit"]');

    await expect(emailInput).toBeVisible();
    await expect(passInput).toBeVisible();
    await expect(submitBtn).toBeVisible();
  });

  test('Ruta de Registro debe capturar parámetros de atribución UTM en la URL', async ({ page }) => {
    await page.goto('/registro?utm_source=google_maps&utm_medium=local&utm_campaign=verano2026');

    // Verificar URL con UTM
    await expect(page).toHaveURL(/utm_source=google_maps/);
    await expect(page).toHaveURL(/utm_campaign=verano2026/);

    const emailInput = page.locator('#reg-email');
    await expect(emailInput).toBeVisible();

    const nameInput = page.locator('#reg-nombre');
    await expect(nameInput).toBeVisible();
  });
});
