import { api } from './api';
import { ApiResponse } from '../models/ApiResponse';
import { Student, StudentDetails, CreateStudentData } from '../models/Student';

/**
 * Servicio de estudiantes
 * Maneja todas las operaciones relacionadas con estudiantes
 */
export const studentService = {
  /**
   * Obtiene todos los estudiantes
   */
  getAll: async (): Promise<ApiResponse<{ students: Student[]; total: number }>> => {
    const response = await api.get<ApiResponse<{ students: Student[]; total: number }>>('/students/');
    return response.data;
  },

  /**
   * Obtiene un estudiante por su ID con todos sus detalles
   */
  getById: async (studentId: string): Promise<ApiResponse<StudentDetails>> => {
    const response = await api.get<ApiResponse<StudentDetails>>(`/students/${studentId}`);
    return response.data;
  },

  /**
   * Crea un nuevo estudiante
   */
  create: async (studentData: CreateStudentData): Promise<ApiResponse> => {
    const response = await api.post<ApiResponse>('/students/', studentData);
    return response.data;
  },

  /**
   * Actualiza el estado de un estudiante
   */
  updateStatus: async (studentId: string, newStatus: string): Promise<ApiResponse> => {
    const response = await api.put<ApiResponse>(`/students/${studentId}/status`, {
      new_status: newStatus,
    });
    return response.data;
  },
};
