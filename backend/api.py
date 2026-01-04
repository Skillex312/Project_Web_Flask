from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
import os

def create_app(config_name='default'):
    """
    Factory Pattern para crear la aplicación Flask
    
    Args:
        config_name: Nombre de la configuración a usar (development, production, default)
        
    Returns:
        Instancia de Flask configurada
    """
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])

    # Inicializar JWT
    jwt = JWTManager(app)

    # Callbacks de JWT para manejo de errores
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'success': False,
            'message': 'Token expirado',
            'error': 'token_expired'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'success': False,
            'message': 'Token inválido',
            'error': 'invalid_token'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'success': False,
            'message': 'Token de acceso requerido',
            'error': 'authorization_required'
        }), 401
    
    # Configurar CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Registrar blueprints (rutas)
    from routes.auth_routes import auth_bp
    from routes.student_routes import student_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    
    # Rutas de salud y bienvenida
    @app.route('/')
    def index():
        """Ruta de bienvenida"""
        return jsonify({
            'message': '🥋 Bienvenido a Martial House API',
            'version': '1.0.0',
            'status': 'online',
            'endpoints': {
                'health': '/health',
                'auth': '/api/auth',
                'students': '/api/students'
            }
        })
    
    @app.route('/health')
    @app.route('/api/health')
    def health():
        """Ruta para verificar el estado del servidor"""
        return jsonify({
            'status': 'ok',
            'message': 'API funcionando correctamente',
            'database': app.config['DATABASE_NAME']
        })
    
    # Manejador de errores 404
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Endpoint no encontrado',
            'status_code': 404
        }), 404
    
    # Manejador de errores 500
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor',
            'status_code': 500
        }), 500
    
    return app

if __name__ == '__main__':
    # Obtener el entorno (development o production)
    env = os.getenv('FLASK_ENV', 'development')
    
    # Crear la aplicación
    app = create_app(env)
    
    # Mensaje de inicio
    print("\n" + "="*60)
    print("🥋 MARTIAL HOUSE - API REST")
    print("="*60)
    print(f"🌍 Entorno: {env}")
    print(f"🗄️  Base de datos: {app.config['DATABASE_NAME']}")
    print(f"🔗 CORS habilitado para: {', '.join(app.config['CORS_ORIGINS'])}")
    print(f"🚀 Servidor corriendo en: http://localhost:5000")
    print("="*60 + "\n")
    
    # Ejecutar el servidor
    app.run(
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=5000
    )
