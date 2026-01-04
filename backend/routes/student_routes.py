from flask import Blueprint, request, jsonify
from controllers.student_controller import StudentController

student_bp = Blueprint('student', __name__, url_prefix='/api/students')

@student_bp.route('/', methods=['GET'])
def get_all_students():
    """
    Endpoint para obtener todos los estudiantes
    
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
def get_student(student_id):
    """
    Endpoint para obtener un estudiante específico
    
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
def create_student():
    """
    Endpoint para crear un nuevo estudiante
    
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
def update_student_status(student_id):
    """
    Endpoint para actualizar el estado de un estudiante
    
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
