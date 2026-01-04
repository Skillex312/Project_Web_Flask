import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';

/**
 * URL base de la API
 * Se obtiene de las variables de entorno o usa localhost por defecto
 */
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// Clave de localStorage para el token
const TOKEN_KEY = 'accessToken';
const REFRESH_TOKEN_KEY = 'refreshToken';

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
 * Flag para evitar múltiples intentos de refresh simultáneos
 */
let isRefreshing = false;
let failedQueue: Array<{
  resolve: (token: string) => void;
  reject: (error: any) => void;
}> = [];

/**
 * Procesa la cola de peticiones fallidas después del refresh
 */
const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token!);
    }
  });
  failedQueue = [];
};

/**
 * Interceptor para agregar el token de autenticación a todas las peticiones
 */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(TOKEN_KEY);
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
 * Interceptor para manejar errores de respuesta con auto-refresh de token
 */
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // Si el error es 401 y no es un retry, intentar refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      // Si ya estamos refrescando, encolar esta petición
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return api(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);

      // Si no hay refresh token, limpiar y redirigir
      if (!refreshToken) {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(REFRESH_TOKEN_KEY);
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(error);
      }

      try {
        // Intentar renovar el token
        const response = await axios.post(
          `${API_BASE_URL}/auth/refresh`,
          {},
          {
            headers: {
              Authorization: `Bearer ${refreshToken}`,
            },
          }
        );

        if (response.data.success && response.data.data?.access_token) {
          const newToken = response.data.data.access_token;
          localStorage.setItem(TOKEN_KEY, newToken);

          // Procesar peticiones en cola
          processQueue(null, newToken);

          // Reintentar la petición original
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          return api(originalRequest);
        } else {
          throw new Error('Refresh failed');
        }
      } catch (refreshError) {
        // Si falla el refresh, limpiar todo y redirigir
        processQueue(refreshError, null);
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(REFRESH_TOKEN_KEY);
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    // Para otros errores, solo log y reject
    if (error.response) {
      console.error('Error de respuesta:', error.response.data);
    } else if (error.request) {
      console.error('No se recibió respuesta del servidor');
    } else {
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
