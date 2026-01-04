from flask import Blueprint, request, jsonify
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_controller = AuthController()

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint de inicio de sesión
    
    Espera un JSON con:
    {
        "username": "ID_del_usuario",
        "password": "contraseña"
    }
    
    Retorna:
    {
        "success": true,
        "message": "Inicio de sesión exitoso",
        "data": {
            "user": {
                "id": "ID_usuario",
                "nombre": "Nombre Usuario",
                "tipo": "Estudiante|Instructor|Administrador|DBA"
            }
        }
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'message': 'No se enviaron datos',
            'status_code': 400
        }), 400
    
    username = data.get('username')
    password = data.get('password')
    
    result = auth_controller.login(username, password)
    return jsonify(result), result.get('status_code', 200)

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Endpoint de cierre de sesión
    
    Retorna:
    {
        "success": true,
        "message": "Sesión cerrada exitosamente"
    }
    """
    result = AuthController.logout()
    return jsonify(result), result.get('status_code', 200)

@auth_bp.route('/verify/<user_id>', methods=['GET'])
def verify_user(user_id):
    """
    Endpoint para verificar si un usuario existe
    
    Args:
        user_id: ID del usuario en la URL
        
    Retorna:
    {
        "success": true,
        "message": "Usuario encontrado",
        "data": {
            "user": {...}
        }
    }
    """
    result = AuthController.verify_user(user_id)
    return jsonify(result), result.get('status_code', 200)
