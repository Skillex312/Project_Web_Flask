/**
 * Respuesta estándar de la API
 */
export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  status_code?: number;
  errors?: any;
}
