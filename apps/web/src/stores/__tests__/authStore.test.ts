// ==============================================================================
// Auth Store — Pruebas Unitarias TDD (Vitest + Pinia)
// ==============================================================================

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useAuthStore } from '@/stores/authStore';

// Mock global fetch
const mockFetch = vi.fn();
vi.stubGlobal('fetch', mockFetch);

function mockFetchResponse(body: any, status = 200) {
  mockFetch.mockResolvedValueOnce({
    ok: status >= 200 && status < 300,
    status,
    json: () => Promise.resolve(body),
  });
}

describe('useAuthStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    mockFetch.mockReset();
  });

  // ============================
  // Estado Inicial
  // ============================
  describe('Estado inicial', () => {
    it('debe iniciar sin autenticar', () => {
      const auth = useAuthStore();
      expect(auth.isAuthenticated).toBe(false);
      expect(auth.accessToken).toBeNull();
      expect(auth.user).toBeNull();
      expect(auth.isAdmin).toBe(false);
      expect(auth.error).toBeNull();
    });
  });

  // ============================
  // Login
  // ============================
  describe('login()', () => {
    it('debe autenticar exitosamente y guardar token en memoria', async () => {
      const auth = useAuthStore();

      mockFetchResponse({
        accessToken: 'jwt-test-token',
        usuario: { id: '1', nombre: 'Juan', email: 'juan@test.com', rol: 'CLIENTE' },
      });

      const result = await auth.login('juan@test.com', 'password123', 'captcha-token');

      expect(result).toBe(true);
      expect(auth.isAuthenticated).toBe(true);
      expect(auth.accessToken).toBe('jwt-test-token');
      expect(auth.user?.nombre).toBe('Juan');
      expect(auth.userRole).toBe('CLIENTE');
      expect(auth.error).toBeNull();

      // Verificar que fetch se llamó con credentials: 'include' (para cookies httpOnly)
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/auth/login'),
        expect.objectContaining({ credentials: 'include' })
      );
    });

    it('debe manejar error de credenciales incorrectas', async () => {
      const auth = useAuthStore();
      mockFetchResponse({ error: 'Credenciales inválidas' }, 401);

      const result = await auth.login('bad@test.com', 'wrong', 'captcha');

      expect(result).toBe(false);
      expect(auth.isAuthenticated).toBe(false);
      expect(auth.error).toBe('Credenciales inválidas');
    });

    it('debe manejar error de red', async () => {
      const auth = useAuthStore();
      mockFetch.mockRejectedValueOnce(new Error('Network error'));

      const result = await auth.login('test@test.com', 'pass', 'captcha');

      expect(result).toBe(false);
      expect(auth.error).toBe('Error de red al conectar con el servidor');
    });

    it('isLoading debe ser true durante la petición', async () => {
      const auth = useAuthStore();

      let resolvePromise: (value: any) => void;
      mockFetch.mockReturnValueOnce(
        new Promise((resolve) => {
          resolvePromise = resolve;
        })
      );

      const loginPromise = auth.login('test@test.com', 'pass', 'captcha');
      expect(auth.isLoading).toBe(true);

      resolvePromise!({
        ok: true,
        json: () => Promise.resolve({ accessToken: 'tok', usuario: { id: '1', nombre: 'X', email: 'x@x.com', rol: 'CLIENTE' } }),
      });

      await loginPromise;
      expect(auth.isLoading).toBe(false);
    });
  });

  // ============================
  // Register
  // ============================
  describe('register()', () => {
    it('debe registrar exitosamente con parámetros UTM', async () => {
      const auth = useAuthStore();

      mockFetchResponse({
        accessToken: 'jwt-new-user',
        usuario: { id: '2', nombre: 'María', email: 'maria@test.com', rol: 'CLIENTE' },
      });

      const result = await auth.register(
        'María',
        'maria@test.com',
        'password123',
        'captcha',
        { source: 'google_maps', medium: 'organic' }
      );

      expect(result).toBe(true);
      expect(auth.isAuthenticated).toBe(true);
      expect(auth.user?.nombre).toBe('María');

      // Verificar que se enviaron los UTM en el body
      const callBody = JSON.parse(mockFetch.mock.calls[0][1].body);
      expect(callBody.utmSource).toBe('google_maps');
      expect(callBody.utmMedium).toBe('organic');
    });
  });

  // ============================
  // Refresh Token
  // ============================
  describe('refreshSession()', () => {
    it('debe renovar el access token vía refresh cookie', async () => {
      const auth = useAuthStore();
      auth.accessToken = 'old-token';
      auth.user = { id: '1', nombre: 'Test', email: 'test@t.com', rol: 'CLIENTE' } as any;

      mockFetchResponse({ accessToken: 'new-token' });

      const result = await auth.refreshSession();

      expect(result).toBe(true);
      expect(auth.accessToken).toBe('new-token');
    });

    it('debe hacer logout si refresh falla', async () => {
      const auth = useAuthStore();
      auth.accessToken = 'old-token';
      auth.user = { id: '1', nombre: 'Test', email: 'test@t.com', rol: 'CLIENTE' } as any;

      mockFetchResponse({}, 401);

      const result = await auth.refreshSession();

      expect(result).toBe(false);
      expect(auth.isAuthenticated).toBe(false);
      expect(auth.accessToken).toBeNull();
    });
  });

  // ============================
  // Logout
  // ============================
  describe('logout()', () => {
    it('debe limpiar estado completamente', async () => {
      const auth = useAuthStore();
      auth.accessToken = 'valid-token';
      auth.user = { id: '1', nombre: 'Test', email: 'test@t.com', rol: 'ADMIN' } as any;

      mockFetchResponse({});

      await auth.logout();

      expect(auth.accessToken).toBeNull();
      expect(auth.user).toBeNull();
      expect(auth.isAuthenticated).toBe(false);
      expect(auth.isAdmin).toBe(false);
    });
  });

  // ============================
  // Roles
  // ============================
  describe('Computed de roles', () => {
    it('isAdmin debe ser true para rol ADMIN', () => {
      const auth = useAuthStore();
      auth.user = { id: '1', nombre: 'Admin', email: 'admin@t.com', rol: 'ADMIN' } as any;
      expect(auth.isAdmin).toBe(true);
      expect(auth.isCajero).toBe(false);
    });

    it('isCajero debe ser true para rol CAJERO', () => {
      const auth = useAuthStore();
      auth.user = { id: '2', nombre: 'Cajero', email: 'caj@t.com', rol: 'CAJERO' } as any;
      expect(auth.isCajero).toBe(true);
      expect(auth.isAdmin).toBe(false);
    });
  });

  // ============================
  // Auth Headers
  // ============================
  describe('getAuthHeaders()', () => {
    it('debe devolver headers vacíos sin token', () => {
      const auth = useAuthStore();
      expect(auth.getAuthHeaders()).toEqual({});
    });

    it('debe devolver Authorization Bearer con token', () => {
      const auth = useAuthStore();
      auth.accessToken = 'my-jwt';
      expect(auth.getAuthHeaders()).toEqual({ Authorization: 'Bearer my-jwt' });
    });
  });
});
