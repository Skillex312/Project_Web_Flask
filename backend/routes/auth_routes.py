from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
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

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Endpoint para renovar el access token usando el refresh token
    
    Headers requeridos:
        Authorization: Bearer <refresh_token>
    
    Retorna:
    {
        "success": true,
        "message": "Token renovado exitosamente",
        "data": {
            "access_token": "nuevo_token",
            "token_type": "Bearer"
        }
    }
    """
    current_user_id = get_jwt_identity()
    current_claims = get_jwt()
    
    result = auth_controller.refresh_token(current_user_id, current_claims)
    return jsonify(result), result.get('status_code', 200)

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Endpoint para obtener la información del usuario actual
    
    Headers requeridos:
        Authorization: Bearer <access_token>
    
    Retorna:
    {
        "success": true,
        "data": {
            "user_id": "ID_usuario",
            "tipo": "Tipo de usuario",
            "role": "rol"
        }
    }
    """
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    return jsonify({
        'success': True,
        'data': {
            'user_id': current_user_id,
            'tipo': claims.get('tipo'),
            'role': claims.get('role')
        }
    }), 200
