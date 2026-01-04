import { api } from './api';
import { LoginCredentials, AuthResponse, User } from '../models/User';

// Claves de localStorage
const TOKEN_KEY = 'accessToken';
const REFRESH_TOKEN_KEY = 'refreshToken';
const USER_KEY = 'user';

/**
 * Servicio de autenticación
 * Maneja todas las operaciones relacionadas con login/logout y tokens JWT
 */
export const authService = {
  /**
   * Inicia sesión con las credenciales proporcionadas
   * Guarda los tokens JWT y datos del usuario
   */
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/login', credentials);
    
    // Si el login fue exitoso, guardar tokens
    if (response.data.success && response.data.data) {
      const { access_token, refresh_token, user } = response.data.data;
      
      if (access_token) {
        localStorage.setItem(TOKEN_KEY, access_token);
      }
      if (refresh_token) {
        localStorage.setItem(REFRESH_TOKEN_KEY, refresh_token);
      }
      if (user) {
        localStorage.setItem(USER_KEY, JSON.stringify(user));
      }
    }
    
    return response.data;
  },

  /**
   * Cierra la sesión del usuario
   * Limpia todos los tokens y datos del localStorage
   */
  logout: async (): Promise<void> => {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Error al cerrar sesión:', error);
    } finally {
      // Siempre limpiar el almacenamiento local
      authService.clearTokens();
    }
  },

  /**
   * Limpia todos los tokens y datos de autenticación
   */
  clearTokens: (): void => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  },

  /**
   * Obtiene el access token actual
   */
  getAccessToken: (): string | null => {
    return localStorage.getItem(TOKEN_KEY);
  },

  /**
   * Obtiene el refresh token actual
   */
  getRefreshToken: (): string | null => {
    return localStorage.getItem(REFRESH_TOKEN_KEY);
  },

  /**
   * Guarda un nuevo access token (usado después del refresh)
   */
  setAccessToken: (token: string): void => {
    localStorage.setItem(TOKEN_KEY, token);
  },

  /**
   * Renueva el access token usando el refresh token
   */
  refreshAccessToken: async (): Promise<string | null> => {
    const refreshToken = authService.getRefreshToken();
    
    if (!refreshToken) {
      return null;
    }

    try {
      // Hacer petición con el refresh token en el header
      const response = await api.post('/auth/refresh', {}, {
        headers: {
          Authorization: `Bearer ${refreshToken}`
        }
      });

      if (response.data.success && response.data.data?.access_token) {
        const newAccessToken = response.data.data.access_token;
        authService.setAccessToken(newAccessToken);
        return newAccessToken;
      }
      
      return null;
    } catch (error) {
      console.error('Error al renovar token:', error);
      // Si falla el refresh, limpiar todo y forzar re-login
      authService.clearTokens();
      return null;
    }
  },

  /**
   * Obtiene el usuario actual del almacenamiento local
   */
  getCurrentUser: (): User | null => {
    const userStr = localStorage.getItem(USER_KEY);
    if (!userStr) return null;
    
    try {
      return JSON.parse(userStr);
    } catch (error) {
      console.error('Error al parsear usuario:', error);
      localStorage.removeItem(USER_KEY);
      return null;
    }
  },

  /**
   * Guarda el usuario en el almacenamiento local
   */
  saveUser: (user: User): void => {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  },

  /**
   * Verifica si el usuario está autenticado (tiene token válido)
   */
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem(TOKEN_KEY) && !!localStorage.getItem(USER_KEY);
  },

  /**
   * Verifica si un usuario existe en el sistema
   */
  verifyUser: async (userId: string): Promise<AuthResponse> => {
    const response = await api.get<AuthResponse>(`/auth/verify/${userId}`);
    return response.data;
  },

  /**
   * Obtiene la información del usuario actual desde el servidor
   */
  getMe: async (): Promise<AuthResponse> => {
    const response = await api.get<AuthResponse>('/auth/me');
    return response.data;
  },
};
