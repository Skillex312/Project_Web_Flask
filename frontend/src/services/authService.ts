import { api } from './api';
import { LoginCredentials, AuthResponse, User } from '../models/User';

/**
 * Servicio de autenticación
 * Maneja todas las operaciones relacionadas con login/logout
 */
export const authService = {
  /**
   * Inicia sesión con las credenciales proporcionadas
   */
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/login', credentials);
    return response.data;
  },

  /**
   * Cierra la sesión del usuario
   */
  logout: async (): Promise<void> => {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Error al cerrar sesión:', error);
    } finally {
      // Siempre limpiar el almacenamiento local
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
    }
  },

  /**
   * Obtiene el usuario actual del almacenamiento local
   */
  getCurrentUser: (): User | null => {
    const userStr = localStorage.getItem('user');
    if (!userStr) return null;
    
    try {
      return JSON.parse(userStr);
    } catch (error) {
      console.error('Error al parsear usuario:', error);
      localStorage.removeItem('user');
      return null;
    }
  },

  /**
   * Guarda el usuario en el almacenamiento local
   */
  saveUser: (user: User): void => {
    localStorage.setItem('user', JSON.stringify(user));
  },

  /**
   * Verifica si el usuario está autenticado
   */
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('user');
  },

  /**
   * Verifica si un usuario existe en el sistema
   */
  verifyUser: async (userId: string): Promise<AuthResponse> => {
    const response = await api.get<AuthResponse>(`/auth/verify/${userId}`);
    return response.data;
  },
};
