from typing import Dict
from models.student import Student
from utils.responses import success_response, error_response

class StudentController:
    """Controlador de estudiantes - Maneja la lógica de negocio de estudiantes"""
    
    @staticmethod
    def get_student_data(student_id: str) -> Dict:
        """
        Obtiene los datos completos de un estudiante
        
        Args:
            student_id: ID del estudiante
            
        Returns:
            Diccionario con los datos del estudiante
        """
        try:
            student = Student.get_by_id(student_id)
            
            if not student:
                return error_response(
                    message="Estudiante no encontrado",
                    status_code=404
                )
            
            # Obtener datos relacionados
            attendance = student.get_attendance()
            payments = student.get_payments()
            
            return success_response(
                data={
                    **student.to_dict(),
                    'asistencia': attendance,
                    'pagos': payments
                }
            )
            
        except Exception as e:
            print(f"❌ Error al obtener datos del estudiante: {e}")
            return error_response(
                message="Error al obtener datos del estudiante",
                status_code=500
            )
    
    @staticmethod
    def get_all_students() -> Dict:
        """
        Obtiene la lista de todos los estudiantes
        
        Returns:
            Diccionario con la lista de estudiantes
        """
        try:
            students = Student.get_all()
            return success_response(
                data={
                    'students': [s.to_dict() for s in students],
                    'total': len(students)
                }
            )
        except Exception as e:
            print(f"❌ Error al listar estudiantes: {e}")
            return error_response(
                message="Error al obtener lista de estudiantes",
                status_code=500
            )
    
    @staticmethod
    def create_student(student_data: Dict) -> Dict:
        """
        Crea un nuevo estudiante
        
        Args:
            student_data: Diccionario con los datos del nuevo estudiante
            
        Returns:
            Diccionario con el resultado de la operación
        """
        try:
            # Validar campos requeridos
            required_fields = ['id', 'nombre', 'apellido', 'fecha_nacimiento']
            missing_fields = [field for field in required_fields if field not in student_data]
            
            if missing_fields:
                return error_response(
                    message=f"Campos requeridos faltantes: {', '.join(missing_fields)}",
                    status_code=400,
                    errors={'missing_fields': missing_fields}
                )
            
            # Crear estudiante
            if Student.create(student_data):
                return success_response(
                    message="Estudiante creado exitosamente",
                    status_code=201
                )
            else:
                return error_response(
                    message="Error al crear estudiante",
                    status_code=500
                )
                
        except Exception as e:
            print(f"❌ Error al crear estudiante: {e}")
            return error_response(
                message="Error al crear estudiante",
                status_code=500
            )
    
    @staticmethod
    def update_student_status(student_id: str, new_status: str) -> Dict:
        """
        Actualiza el estado de un estudiante
        
        Args:
            student_id: ID del estudiante
            new_status: Nuevo estado del estudiante
            
        Returns:
            Diccionario con el resultado de la operación
        """
        try:
            student = Student.get_by_id(student_id)
            
            if not student:
                return error_response(
                    message="Estudiante no encontrado",
                    status_code=404
                )
            
            if student.update_status(new_status):
                return success_response(
                    message="Estado actualizado exitosamente",
                    data={'new_status': new_status}
                )
            else:
                return error_response(
                    message="Error al actualizar estado",
                    status_code=500
                )
                
        except Exception as e:
            print(f"❌ Error al actualizar estado: {e}")
            return error_response(
                message="Error al actualizar estado del estudiante",
                status_code=500
            )
