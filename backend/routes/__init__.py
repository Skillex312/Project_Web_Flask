"""Módulo de rutas"""
from .auth_routes import auth_bp
from .student_routes import student_bp

__all__ = ['auth_bp', 'student_bp']
