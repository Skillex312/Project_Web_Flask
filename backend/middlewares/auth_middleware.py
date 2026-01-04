"""
Middlewares de autenticación y autorización JWT

Este módulo proporciona decoradores para proteger endpoints basándose en:
- Autenticación JWT (usuario logueado)
- Autorización por rol/tipo de usuario

Uso:
    from middlewares import admin_required, roles_required
    
    @app.route('/admin-only')
    @admin_required
    def admin_endpoint():
        ...
    
    @app.route('/staff-only')
    @roles_required(['Administrador', 'Instructor'])
    def staff_endpoint():
        ...
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_identity,
    get_jwt
)


def get_current_user_info():
    """
    Obtiene la información del usuario actual del token JWT
    
    Returns:
        dict: Información del usuario {user_id, tipo, role}
        None: Si no hay token válido
    """
    try:
        verify_jwt_in_request()
        return {
            'user_id': get_jwt_identity(),
            'tipo': get_jwt().get('tipo'),
            'role': get_jwt().get('role')
        }
    except Exception:
        return None


def jwt_required_custom(fn):
    """
    Decorador que requiere autenticación JWT válida.
    Similar a @jwt_required() pero con respuesta personalizada.
    
    Uso:
        @jwt_required_custom
        def my_protected_route():
            ...
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Autenticación requerida',
                'error': str(e)
            }), 401
    return wrapper


def roles_required(allowed_roles):
    """
    Decorador que requiere que el usuario tenga uno de los roles permitidos.
    
    Args:
        allowed_roles: Lista de roles permitidos ['Administrador', 'Instructor', etc.]
    
    Uso:
        @roles_required(['Administrador', 'Instructor'])
        def staff_only_route():
            ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()
                user_tipo = claims.get('tipo', '')
                
                if user_tipo not in allowed_roles:
                    return jsonify({
                        'success': False,
                        'message': f'Acceso denegado. Se requiere uno de estos roles: {", ".join(allowed_roles)}',
                        'error': 'forbidden'
                    }), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': 'Autenticación requerida',
                    'error': str(e)
                }), 401
        return wrapper
    return decorator


def admin_required(fn):
    """
    Decorador que requiere rol de Administrador.
    
    Uso:
        @admin_required
        def admin_only_route():
            ...
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            user_tipo = claims.get('tipo', '')
            
            if user_tipo != 'Administrador':
                return jsonify({
                    'success': False,
                    'message': 'Acceso denegado. Se requiere rol de Administrador',
                    'error': 'forbidden'
                }), 403
            
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Autenticación requerida',
                'error': str(e)
            }), 401
    return wrapper


def instructor_required(fn):
    """
    Decorador que requiere rol de Instructor o Administrador.
    
    Uso:
        @instructor_required
        def instructor_route():
            ...
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            user_tipo = claims.get('tipo', '')
            
            if user_tipo not in ['Instructor', 'Administrador']:
                return jsonify({
                    'success': False,
                    'message': 'Acceso denegado. Se requiere rol de Instructor o Administrador',
                    'error': 'forbidden'
                }), 403
            
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Autenticación requerida',
                'error': str(e)
            }), 401
    return wrapper


def student_required(fn):
    """
    Decorador que requiere que el usuario sea Estudiante (o superior).
    Permite: Estudiante, Instructor, Administrador
    
    Uso:
        @student_required
        def student_or_above_route():
            ...
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            user_tipo = claims.get('tipo', '')
            
            allowed = ['Estudiante', 'Instructor', 'Administrador', 'DBA']
            if user_tipo not in allowed:
                return jsonify({
                    'success': False,
                    'message': 'Acceso denegado',
                    'error': 'forbidden'
                }), 403
            
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Autenticación requerida',
                'error': str(e)
            }), 401
    return wrapper


def own_data_or_admin(fn):
    """
    Decorador que permite acceso si:
    - El usuario es Administrador/Instructor, O
    - El usuario está accediendo a sus propios datos (student_id == user_id)
    
    Requiere que la ruta tenga un parámetro 'student_id'.
    
    Uso:
        @own_data_or_admin
        def get_student(student_id):
            ...
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            user_id = get_jwt_identity()
            user_tipo = claims.get('tipo', '')
            
            # Administradores e instructores tienen acceso total
            if user_tipo in ['Administrador', 'Instructor', 'DBA']:
                return fn(*args, **kwargs)
            
            # Estudiantes solo pueden ver sus propios datos
            student_id = kwargs.get('student_id')
            if student_id and student_id == user_id:
                return fn(*args, **kwargs)
            
            return jsonify({
                'success': False,
                'message': 'Solo puedes acceder a tus propios datos',
                'error': 'forbidden'
            }), 403
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Autenticación requerida',
                'error': str(e)
            }), 401
    return wrapper
