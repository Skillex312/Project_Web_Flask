import { useState, useEffect, useCallback } from 'react';
import { authService } from '../services/authService';
import { User, LoginCredentials } from '../models/User';

/**
 * Hook personalizado para manejar la autenticación con JWT
 * 
 * Este hook encapsula toda la lógica de autenticación y proporciona:
 * - Estado del usuario actual
 * - Funciones para login/logout
 * - Estados de carga y error
 * - Verificación de tokens al iniciar
 */
export const useAuth = (onLoginSuccess?: () => void) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true); // true inicial para verificar token
  const [error, setError] = useState<string>('');

  /**
   * Verifica si hay una sesión válida al montar el componente
   */
  useEffect(() => {
    const checkAuth = async () => {
      // Si hay un token, verificar que sigue siendo válido
      if (authService.isAuthenticated()) {
        try {
          // Intentar obtener info del usuario desde el servidor
          const response = await authService.getMe();
          
          if (response.success) {
            // Token válido, cargar usuario del localStorage
            const currentUser = authService.getCurrentUser();
            setUser(currentUser);
          } else {
            // Token inválido, limpiar
            authService.clearTokens();
            setUser(null);
          }
        } catch (err) {
          // Error al verificar (puede ser que el auto-refresh maneje esto)
          // Si aún hay usuario en localStorage, intentar usarlo
          const currentUser = authService.getCurrentUser();
          if (currentUser) {
            setUser(currentUser);
          }
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  /**
   * Función para iniciar sesión
   */
  const login = useCallback(async (credentials: LoginCredentials) => {
    setLoading(true);
    setError('');

    try {
      const response = await authService.login(credentials);

      if (response.success && response.data) {
        const userData = response.data.user;
        setUser(userData);

        // Llamar a la función de éxito si existe
        if (onLoginSuccess) {
          onLoginSuccess();
        }
      } else {
        setError(response.message || 'Error al iniciar sesión');
      }
    } catch (err: any) {
      const errorMessage = 
        err.response?.data?.message || 
        err.message || 
        'Error al conectar con el servidor';
      setError(errorMessage);
      console.error('Error en login:', err);
    } finally {
      setLoading(false);
    }
  }, [onLoginSuccess]);

  /**
   * Función para cerrar sesión
   */
  const logout = useCallback(async () => {
    try {
      await authService.logout();
    } catch (err) {
      console.error('Error al cerrar sesión:', err);
    } finally {
      // Siempre limpiar el estado local
      setUser(null);
      setError('');
    }
  }, []);

  /**
   * Función para verificar si el usuario está autenticado
   */
  const isAuthenticated = useCallback((): boolean => {
    return user !== null && authService.isAuthenticated();
  }, [user]);

  /**
   * Función para refrescar manualmente el token
   */
  const refreshToken = useCallback(async (): Promise<boolean> => {
    try {
      const newToken = await authService.refreshAccessToken();
      return newToken !== null;
    } catch (err) {
      console.error('Error al refrescar token:', err);
      return false;
    }
  }, []);

  /**
   * Limpia el error actual
   */
  const clearError = useCallback(() => {
    setError('');
  }, []);

  return {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated,
    refreshToken,
    clearError,
  };
};
