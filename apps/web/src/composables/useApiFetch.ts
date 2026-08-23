// ==============================================================================
// useFetch — Composable para peticiones API autenticadas
// ==============================================================================

import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore';

const API_URL = import.meta.env.VITE_API_URL || '';

interface FetchOptions extends Omit<RequestInit, 'headers'> {
  headers?: Record<string, string>;
}

export function useApiFetch<T = any>() {
  const data = ref<T | null>(null);
  const error = ref<string | null>(null);
  const isLoading = ref(false);

  async function execute(endpoint: string, options: FetchOptions = {}) {
    const auth = useAuthStore();
    isLoading.value = true;
    error.value = null;

    try {
      const res = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          ...auth.getAuthHeaders(),
          ...options.headers,
        },
      });

      // Si recibimos 401, intentar refresh y reintentar una vez
      if (res.status === 401) {
        const refreshed = await auth.refreshSession();
        if (refreshed) {
          const retryRes = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
              ...auth.getAuthHeaders(),
              ...options.headers,
            },
          });

          if (!retryRes.ok) {
            const errData = await retryRes.json().catch(() => ({}));
            error.value = errData.error || `Error ${retryRes.status}`;
            return null;
          }

          data.value = await retryRes.json();
          return data.value;
        } else {
          error.value = 'Sesión expirada. Inicia sesión nuevamente.';
          return null;
        }
      }

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        error.value = errData.error || `Error ${res.status}`;
        return null;
      }

      data.value = await res.json();
      return data.value;
    } catch (e: any) {
      error.value = 'Error de red al conectar con el servidor';
      return null;
    } finally {
      isLoading.value = false;
    }
  }

  return { data, error, isLoading, execute };
}
