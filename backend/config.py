import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar el .env del backend de forma consistente, sin depender del cwd
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_BASE_DIR, '.env'))


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == '':
        raise RuntimeError(f"Falta la variable de entorno requerida: {name} (defínela en backend/.env)")
    return value

class Config:
    """Configuración base"""
    SECRET_KEY = _require_env('SECRET_KEY')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'academia.db')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # Configuración JWT
    JWT_SECRET_KEY = _require_env('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_HOURS', '1')))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES_DAYS', '7')))
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
