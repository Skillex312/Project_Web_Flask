import axios, { AxiosInstance, AxiosError } from 'axios';

/**
 * URL base de la API
 * Se obtiene de las variables de entorno o usa localhost por defecto
 */
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

/**
 * Instancia configurada de axios para hacer peticiones a la API
 */
export const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 segundos
});

/**
 * Interceptor para agregar el token de autenticación a todas las peticiones
 */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * Interceptor para manejar errores de respuesta
 */
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // Si el error es 401 (no autorizado), cerrar sesión
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    
    // Mejorar el mensaje de error
    if (error.response) {
      // El servidor respondió con un código de error
      console.error('Error de respuesta:', error.response.data);
    } else if (error.request) {
      // La petición fue hecha pero no hubo respuesta
      console.error('No se recibió respuesta del servidor');
    } else {
      // Algo pasó al configurar la petición
      console.error('Error al configurar la petición:', error.message);
    }
    
    return Promise.reject(error);
  }
);

/**
 * Función helper para verificar si el backend está disponible
 */
export const checkApiHealth = async (): Promise<boolean> => {
  try {
    // Llamar al endpoint de health check
    const response = await axios.get(`${API_BASE_URL}/health`, { timeout: 5000 });
    return response.data.status === 'ok';
  } catch (error) {
    console.error('Backend no disponible:', error);
    return false;
  }
};
