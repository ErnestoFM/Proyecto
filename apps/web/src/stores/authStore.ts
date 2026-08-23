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

  const isAuthenticated = computed(() => !!accessToken.value && !!user.value);
  const userRole = computed<UserRole | null>(() => user.value?.rol ?? null);
  const isAdmin = computed(() => userRole.value === 'ADMIN');
  const isCajero = computed(() => userRole.value === 'CAJERO');

  async function login(email: string, password: string, recaptchaToken: string) {
    isLoading.value = true;
    error.value = null;

    try {
      const res = await fetch(`${API_URL}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include', // Necesario para enviar/recibir cookies httpOnly
        body: JSON.stringify({ email, password, recaptchaToken }),
      });

      const data = await res.json();

      if (!res.ok) {
        error.value = data.error || 'Error al iniciar sesión';
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
    login,
    register,
    refreshSession,
    logout,
    getAuthHeaders,
  };
});
