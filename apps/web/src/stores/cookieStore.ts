// ==============================================================================
// Monchis Café — Cookie Consent Store (Pinia)
// ==============================================================================

import { defineStore } from 'pinia';
import { ref } from 'vue';

export interface CookiePreferences {
  necesarias: boolean; // Siempre true (sesión stateless, csrf, seguridad)
  analitica: boolean;  // Google Maps / UTM tracking / estadísticas de visitas
  marketing: boolean;  // Campañas promocionales / Instagram pixel
}

const STORAGE_KEY = 'monchis_cookie_consent_v1';

export const useCookieStore = defineStore('cookie', () => {
  const haRespondido = ref<boolean>(false);
  const preferencias = ref<CookiePreferences>({
    necesarias: true,
    analitica: true,
    marketing: false,
  });

  function cargarPreferencias() {
    if (typeof window === 'undefined') return;
    try {
      const guardado = localStorage.getItem(STORAGE_KEY);
      if (guardado) {
        preferencias.value = { ...preferencias.value, ...JSON.parse(guardado), necesarias: true };
        haRespondido.value = true;
      }
    } catch {
      // Fallback si localStorage está bloqueado
    }
  }

  function guardarPreferencias(nuevasPreferencias: Partial<CookiePreferences>) {
    preferencias.value = {
      ...preferencias.value,
      ...nuevasPreferencias,
      necesarias: true, // Inmutable
    };
    haRespondido.value = true;
    if (typeof window !== 'undefined') {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(preferencias.value));
      } catch {}
    }
  }

  function aceptarTodas() {
    guardarPreferencias({ analitica: true, marketing: true });
  }

  function rechazarOpcionales() {
    guardarPreferencias({ analitica: false, marketing: false });
  }

  return {
    haRespondido,
    preferencias,
    cargarPreferencias,
    guardarPreferencias,
    aceptarTodas,
    rechazarOpcionales,
  };
});
