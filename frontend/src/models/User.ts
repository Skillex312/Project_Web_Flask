/**
 * Tipos de usuario en el sistema
 */
export enum UserType {
  STUDENT = 'Estudiante',
  INSTRUCTOR = 'Instructor',
  ADMIN = 'Administrador',
  DBA = 'DBA'
}

/**
 * Interfaz de Usuario
 */
export interface User {
  id: string;
  nombre?: string;
  apellido?: string;
  tipo: UserType;
  rango_marcial?: string;
  role?: string;
}

/**
 * Credenciales para login
 */
export interface LoginCredentials {
  username: string;
  password: string;
}

/**
 * Respuesta de autenticación
 */
export interface AuthResponse {
  success: boolean;
  message: string;
  data?: {
    user: User;
  };
  status_code?: number;
}
