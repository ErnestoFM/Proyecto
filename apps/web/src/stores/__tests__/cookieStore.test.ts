// ==============================================================================
// Cookie Store — Pruebas Unitarias TDD (Vitest + Pinia)
// ==============================================================================

import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useCookieStore } from '@/stores/cookieStore';

describe('useCookieStore (Consentimiento y Ajustes de Cookies)', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    localStorage.clear();
  });

  it('Debe inicializar con cookies necesarias activas e inmutables', () => {
    const store = useCookieStore();
    expect(store.preferencias.necesarias).toBe(true);
    expect(store.haRespondido).toBe(false);
  });

  it('Debe guardar y persistir preferencias personalizadas en localStorage', () => {
    const store = useCookieStore();
    store.guardarPreferencias({ analitica: true, marketing: false });

    expect(store.preferencias.analitica).toBe(true);
    expect(store.preferencias.marketing).toBe(false);
    expect(store.preferencias.necesarias).toBe(true);
    expect(store.haRespondido).toBe(true);

    // Cargar en nuevo store
    const store2 = useCookieStore();
    store2.cargarPreferencias();
    expect(store2.preferencias.analitica).toBe(true);
  });

  it('Debe aceptar todas las cookies correctamente', () => {
    const store = useCookieStore();
    store.aceptarTodas();

    expect(store.preferencias.analitica).toBe(true);
    expect(store.preferencias.marketing).toBe(true);
    expect(store.preferencias.necesarias).toBe(true);
    expect(store.haRespondido).toBe(true);
  });

  it('Debe rechazar cookies opcionales manteniendo necesarias', () => {
    const store = useCookieStore();
    store.rechazarOpcionales();

    expect(store.preferencias.analitica).toBe(false);
    expect(store.preferencias.marketing).toBe(false);
    expect(store.preferencias.necesarias).toBe(true);
    expect(store.haRespondido).toBe(true);
  });
});
