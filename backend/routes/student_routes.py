from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from controllers.student_controller import StudentController
from middlewares.auth_middleware import (
    admin_required,
    instructor_required,
    own_data_or_admin
)

student_bp = Blueprint('student', __name__, url_prefix='/api/students')

@student_bp.route('/', methods=['GET'])
@instructor_required
def get_all_students():
    """
    Endpoint para obtener todos los estudiantes
    
    Requiere: Rol Instructor o Administrador
    Headers: Authorization: Bearer <access_token>
    
    Retorna:
    {
        "success": true,
        "data": {
            "students": [...],
            "total": 10
        }
    }
    """
    result = StudentController.get_all_students()
    return jsonify(result), result.get('status_code', 200)

@student_bp.route('/<student_id>', methods=['GET'])
@own_data_or_admin
def get_student(student_id):
    """
    Endpoint para obtener un estudiante específico
    
    Requiere: Autenticación JWT
    - Administradores/Instructores: pueden ver cualquier estudiante
    - Estudiantes: solo pueden ver sus propios datos
    
    Args:
        student_id: ID del estudiante en la URL
        
    Retorna:
    {
        "success": true,
        "data": {
            "id": "...",
            "nombre": "...",
            "apellido": "...",
            "rango_marcial": "...",
            "estado": "...",
            "asistencia": [...],
            "pagos": [...]
        }
    }
    """
    result = StudentController.get_student_data(student_id)
    return jsonify(result), result.get('status_code', 200)

@student_bp.route('/', methods=['POST'])
@admin_required
def create_student():
    """
    Endpoint para crear un nuevo estudiante
    
    Requiere: Rol Administrador
    Headers: Authorization: Bearer <access_token>
    
    Espera un JSON con:
    {
        "id": "ID_estudiante",
        "nombre": "Nombre",
        "apellido": "Apellido",
        "fecha_nacimiento": "YYYY-MM-DD",
        "direccion": "Dirección (opcional)",
        "telefono": "Teléfono (opcional)",
        "correo": "email@example.com (opcional)",
        "rango_marcial": "Blanco (opcional, default: Blanco)",
        "estado": "Activo (opcional, default: Activo)"
    }
    
    Retorna:
    {
        "success": true,
        "message": "Estudiante creado exitosamente"
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'message': 'No se enviaron datos',
            'status_code': 400
        }), 400
    
    result = StudentController.create_student(data)
    return jsonify(result), result.get('status_code', 200)

@student_bp.route('/<student_id>/status', methods=['PUT'])
@instructor_required
def update_student_status(student_id):
    """
    Endpoint para actualizar el estado de un estudiante
    
    Requiere: Rol Instructor o Administrador
    Headers: Authorization: Bearer <access_token>
    
    Args:
        student_id: ID del estudiante en la URL
        
    Espera un JSON con:
    {
        "new_status": "Activo|Inactivo|Suspendido"
    }
    
    Retorna:
    {
        "success": true,
        "message": "Estado actualizado exitosamente",
        "data": {
            "new_status": "Activo"
        }
    }
    """
    data = request.get_json()
    
    if not data or 'new_status' not in data:
        return jsonify({
            'success': False,
            'message': 'El campo new_status es requerido',
            'status_code': 400
        }), 400
    
    new_status = data.get('new_status')
    result = StudentController.update_student_status(student_id, new_status)
    return jsonify(result), result.get('status_code', 200)
