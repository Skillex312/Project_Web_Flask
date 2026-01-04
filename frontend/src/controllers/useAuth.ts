import { useState, useEffect } from 'react';
import { authService } from '../services/authService';
import { User, LoginCredentials } from '../models/User';

/**
 * Hook personalizado para manejar la autenticación
 * 
 * Este hook encapsula toda la lógica de autenticación y proporciona:
 * - Estado del usuario actual
 * - Funciones para login/logout
 * - Estados de carga y error
 */
export const useAuth = (onLoginSuccess?: () => void) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  /**
   * Al montar el componente, verificar si hay un usuario en localStorage
   */
  useEffect(() => {
    const currentUser = authService.getCurrentUser();
    if (currentUser) {
      setUser(currentUser);
    }
  }, []);

  /**
   * Función para iniciar sesión
   */
  const login = async (credentials: LoginCredentials) => {
    setLoading(true);
    setError('');

    try {
      const response = await authService.login(credentials);

      if (response.success && response.data) {
        const userData = response.data.user;
        setUser(userData);
        authService.saveUser(userData);

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
  };

  /**
   * Función para cerrar sesión
   */
  const logout = async () => {
    try {
      await authService.logout();
      setUser(null);
    } catch (err) {
      console.error('Error al cerrar sesión:', err);
      // Aún así limpiar el estado local
      setUser(null);
    }
  };

  /**
   * Función para verificar si el usuario está autenticado
   */
  const isAuthenticated = (): boolean => {
    return user !== null;
  };

  return {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated,
  };
};
