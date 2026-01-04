/**
 * Interfaz de Estudiante
 */
export interface Student {
  id: string;
  nombre: string;
  hap_kit: number;
  cardio: number;
  krav_maga: number;
  kung_fu: number;
  disciplinas: string[];
  rango: string;
  condicion: string;
  estado: string;
  fecha_registro: string;
}

/**
 * Datos completos del estudiante incluyendo asistencia y pagos
 */
export interface StudentDetails extends Student {
  asistencia: AttendanceRecord[];
  pagos: PaymentRecord[];
}

/**
 * Registro de asistencia
 */
export interface AttendanceRecord {
  fecha: string;
  instructor: string;
  estado: string;
}

/**
 * Registro de pago
 */
export interface PaymentRecord {
  fecha: string;
  concepto: string;
  monto: number;
}

/**
 * Datos para crear un estudiante
 */
export interface CreateStudentData {
  id: string;
  nombre: string;
  hap_kit?: number;
  cardio?: number;
  krav_maga?: number;
  kung_fu?: number;
  rango?: string;
  condicion?: string;
  estado?: string;
  fecha_registro?: string;
}
