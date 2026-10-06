// ==============================================================================
// Monchis Café — Auth Store (Pinia) — JWT Stateless
// ==============================================================================

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { UserDTO, UserRole } from '@monchis/shared-types';

const API_URL = import.meta.env.VITE_API_URL || '';

export const useAuthStore = defineStore('auth', () => {
  // Access token se almacena solo en memoria (NUNCA en localStorage)
  const accessToken = ref<string | null>(null);
  const user = ref<UserDTO | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Estado para flujo de Doble Factor (2FA / TOTP)
  const requires2FA = ref(false);
  const tempToken = ref<string | null>(null);

  const isAuthenticated = computed(() => !!accessToken.value && !!user.value);
  const userRole = computed<UserRole | null>(() => user.value?.rol ?? null);
  const isAdmin = computed(() => userRole.value === 'ADMIN');
  const isCajero = computed(() => userRole.value === 'CAJERO');

  async function login(email: string, password: string, recaptchaToken: string, totpCode?: string) {
    isLoading.value = true;
    error.value = null;
    requires2FA.value = false;
    tempToken.value = null;

    try {
      const res = await fetch(`${API_URL}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include', // Necesario para enviar/recibir cookies httpOnly
        body: JSON.stringify({ email, password, recaptchaToken, totpCode }),
      });

      const data = await res.json();

      if (!res.ok) {
        error.value = data.error || 'Error al iniciar sesión';
        return false;
      }

      if (data.requiere2FA) {
        requires2FA.value = true;
        tempToken.value = data.tempToken;
        return true;
      }

      accessToken.value = data.accessToken;
      user.value = data.usuario;
      return true;
    } catch (e: any) {
      error.value = 'Error de red al conectar con el servidor';
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  async function verify2FA(totpCode: string) {
    if (!tempToken.value) {
      error.value = 'No hay sesión de autenticación 2FA pendiente';
      return false;
    }

    isLoading.value = true;
    error.value = null;

    try {
      const res = await fetch(`${API_URL}/api/auth/2fa/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          tempToken: tempToken.value,
          totpCode,
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        error.value = data.error || 'Código 2FA incorrecto';
        return false;
      }

      accessToken.value = data.accessToken;
      user.value = data.usuario;
      requires2FA.value = false;
      tempToken.value = null;
      return true;
    } catch (e: any) {
      error.value = 'Error al verificar código de doble factor';
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  async function setup2FA(): Promise<{ secret: string; otpAuthUrl: string; qrCodeDataUrl: string; dosFactoresActivo: boolean } | null> {
    try {
      const res = await fetch(`${API_URL}/api/auth/2fa/setup`, {
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
        },
        credentials: 'include',
      });
      if (!res.ok) {
        throw new Error('Error al generar configuración 2FA');
      }
      return await res.json();
    } catch (e: any) {
      error.value = e.message;
      return null;
    }
  }

  async function enable2FA(secret: string, totpCode: string) {
    try {
      const res = await fetch(`${API_URL}/api/auth/2fa/enable`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
        },
        credentials: 'include',
        body: JSON.stringify({ secret, totpCode }),
      });
      const data = await res.json();
      if (!res.ok) {
        error.value = data.error || 'Error al activar 2FA';
        return false;
      }
      if (user.value) {
        user.value.dosFactoresActivo = true;
      }
      return true;
    } catch (e: any) {
      error.value = 'Error al activar 2FA';
      return false;
    }
  }

  async function disable2FA(totpCode: string) {
    try {
      const res = await fetch(`${API_URL}/api/auth/2fa/disable`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
        },
        credentials: 'include',
        body: JSON.stringify({ totpCode }),
      });
      const data = await res.json();
      if (!res.ok) {
        error.value = data.error || 'Error al desactivar 2FA';
        return false;
      }
      if (user.value) {
        user.value.dosFactoresActivo = false;
      }
      return true;
    } catch (e: any) {
      error.value = 'Error al desactivar 2FA';
      return false;
    }
  }

  async function register(
    nombre: string,
    email: string,
    password: string,
    recaptchaToken: string,
    utm?: { source?: string; medium?: string; campaign?: string }
  ) {
    isLoading.value = true;
    error.value = null;

    try {
      const res = await fetch(`${API_URL}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          nombre,
          email,
          password,
          recaptchaToken,
          utmSource: utm?.source,
          utmMedium: utm?.medium,
          utmCampaign: utm?.campaign,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        error.value = data.error || 'Error al registrarse';
        return false;
      }

      accessToken.value = data.accessToken;
      user.value = data.usuario;
      return true;
    } catch (e: any) {
      error.value = 'Error de red al conectar con el servidor';
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  async function refreshSession() {
    try {
      const res = await fetch(`${API_URL}/api/auth/refresh`, {
        method: 'POST',
        credentials: 'include',
      });

      if (!res.ok) {
        logout();
        return false;
      }

      const data = await res.json();
      accessToken.value = data.accessToken;
      return true;
    } catch {
      logout();
      return false;
    }
  }

  async function logout() {
    try {
      await fetch(`${API_URL}/api/auth/logout`, {
        method: 'POST',
        credentials: 'include',
      });
    } catch {
      // Silenciamos errores de red en logout
    }
    accessToken.value = null;
    user.value = null;
  }

  function getAuthHeaders(): Record<string, string> {
    if (!accessToken.value) return {};
    return { Authorization: `Bearer ${accessToken.value}` };
  }

  return {
    accessToken,
    user,
    isLoading,
    error,
    isAuthenticated,
    userRole,
    isAdmin,
    isCajero,
    requires2FA,
    tempToken,
    login,
    verify2FA,
    setup2FA,
    enable2FA,
    disable2FA,
    register,
    refreshSession,
    logout,
    getAuthHeaders,
  };
});
