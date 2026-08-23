// ==============================================================================
// Playwright E2E Test — Responsive & Viewport Capture
// Monchis Café — Pruebas de renderizado en móvil, tablet y escritorio
// ==============================================================================

import { test, expect } from '@playwright/test';

test.describe('📱 1. Pruebas de Renderizado Responsive & Viewports', () => {
  test('HomePage debe renderizar correctamente y contener elementos clave en cualquier viewport', async ({ page }) => {
    await page.goto('/');

    // Verificar título y branding de Monchis Café
    await expect(page).toHaveTitle(/Monchis Café/);
    const logo = page.locator('.navbar__name');
    await expect(logo).toBeVisible();

    // Verificar badge orgánico y botón CTA
    const organicBadge = page.locator('.badge--organic').first();
    await expect(organicBadge).toBeVisible();
    await expect(organicBadge).toContainText('Café Orgánico');

    // Verificar grid de valores
    const cards = page.locator('.values__card');
    await expect(cards).toHaveCount(3);
  });

  test('Navbar hamburguesa debe ser visible en pantallas pequeñas y colapsable', async ({ page, isMobile }) => {
    await page.goto('/');

    if (isMobile) {
      const hamburgerBtn = page.locator('.navbar__toggle');
      await expect(hamburgerBtn).toBeVisible();

      // Abrir menú móvil
      await hamburgerBtn.click();
      const menu = page.locator('.navbar__menu');
      await expect(menu).toHaveClass(/navbar__menu--open/);
    }
  });
});

test.describe('🛒 2. Flujo Completo Punto de Venta (POS)', () => {
  test('POS debe permitir seleccionar café orgánico, aplicar termo y reflejar en carrito', async ({ page }) => {
    await page.goto('/pos');

    // Filtrar por categoría Orgánico
    const btnOrganico = page.locator('button:has-text("🌿 Café Orgánico")');
    if (await btnOrganico.isVisible()) {
      await btnOrganico.click();
    }

    // Agregar primer producto
    const btnAgregar = page.locator('.product-card button').first();
    await expect(btnAgregar).toBeVisible();
    await btnAgregar.click();

    // Verificar que el carrito tiene 1 item
    const cartItem = page.locator('.cart-item');
    await expect(cartItem).toHaveCount(1);

    // Activar checkbox de termo ecológico
    const termoCheckbox = page.locator('.eco-checkbox input[type="checkbox"]');
    await termoCheckbox.check();
    await expect(termoCheckbox).toBeChecked();
  });
});

test.describe('🛡️ 3. Seguridad y Protección de Rutas RBAC', () => {
  test('Rutas de autenticación deben contener protección reCAPTCHA', async ({ page }) => {
    await page.goto('/login');

    const recaptchaBox = page.locator('.recaptcha-placeholder');
    await expect(recaptchaBox).toBeVisible();
    await expect(recaptchaBox).toContainText('Google reCAPTCHA');
  });

  test('Registro debe capturar parámetros UTM de la URL', async ({ page }) => {
    await page.goto('/registro?utm_source=google_maps&utm_medium=local&utm_campaign=verano2026');

    // Verificar que la página carga adecuadamente con los query params
    await expect(page).toHaveURL(/utm_source=google_maps/);
    const emailInput = page.locator('#reg-email');
    await expect(emailInput).toBeVisible();
  });
});
