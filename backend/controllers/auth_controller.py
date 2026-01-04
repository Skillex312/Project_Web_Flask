from typing import Dict
from models.user import User
from utils.responses import success_response, error_response
from Conexion_bd import ConexionBD
from gest_estu import Estudiante
from gest_inst import Instructor
import sqlite3

class AuthController:
    """Controlador de autenticación - Maneja la lógica de login/logout"""
    
    def __init__(self, database_name='academia.db'):
        self.database_name = database_name
    
    def login(self, username: str, password: str) -> Dict:
        """
        Procesa el inicio de sesión de un usuario
        
        Args:
            username: ID del usuario
            password: Contraseña del usuario
            
        Returns:
            Diccionario con el resultado de la autenticación
        """
        connection = None
        try:
            # Validar que los campos no estén vacíos
            if not username or not password:
                return error_response(
                    message="Usuario y contraseña son requeridos",
                    status_code=400
                )
            
            # Conectar a la base de datos
            connection = ConexionBD(self.database_name)
            connection.conectar()
            
            # Buscar usuario en la base de datos
            consulta = "SELECT Tipo FROM Usuarios WHERE ID = ? AND Contrasena = ?"
            parametros = (username, password)
            resultado = connection.obtener_uno(consulta, parametros)
            
            if not resultado:
                return error_response(
                    message="Credenciales inválidas",
                    status_code=401
                )
            
            tipo = resultado[0]
            
            # Preparar datos del usuario
            user_data = {
                'id': username,
                'tipo': tipo
            }
            
            # Agregar datos específicos según el tipo de usuario
            if tipo == 'Estudiante':
                user_data.update(self._get_student_data(username))
            elif tipo == 'Instructor':
                user_data.update(self._get_instructor_data(username))
            elif tipo == 'Administrador':
                user_data['role'] = 'admin'
            elif tipo == 'DBA':
                user_data['role'] = 'dba'
            
            return success_response(
                data={'user': user_data},
                message="Inicio de sesión exitoso"
            )
                
        except sqlite3.Error as err:
            print(f"❌ Error de base de datos: {err}")
            return error_response(
                message="Error en la base de datos",
                status_code=500
            )
        except Exception as e:
            print(f"❌ Error en login: {e}")
            return error_response(
                message="Error interno del servidor",
                status_code=500
            )
        finally:
            if connection:
                connection.cerrar_conexion()
    
    def _get_student_data(self, username: str) -> Dict:
        """Obtiene datos específicos del estudiante"""
        try:
            estudiante = Estudiante()
            datos = estudiante.obtener_datos_estudiante(username)
            if datos:
                nombre, apellido, rango_marcial = datos
                return {
                    'nombre': nombre,
                    'apellido': apellido,
                    'rango_marcial': rango_marcial
                }
        except Exception as e:
            print(f"⚠️ Error obteniendo datos de estudiante: {e}")
        return {}
    
    def _get_instructor_data(self, username: str) -> Dict:
        """Obtiene datos específicos del instructor"""
        try:
            instructor = Instructor()
            datos = instructor.obtener_datos_instructor(username)
            if datos:
                nombre, apellido, rango_marcial = datos
                return {
                    'nombre': nombre,
                    'apellido': apellido,
                    'rango_marcial': rango_marcial
                }
        except Exception as e:
            print(f"⚠️ Error obteniendo datos de instructor: {e}")
        return {}
    
    @staticmethod
    def logout() -> Dict:
        """
        Procesa el cierre de sesión
        
        Returns:
            Diccionario confirmando el cierre de sesión
        """
        return success_response(
            message="Sesión cerrada exitosamente"
        )
    
    @staticmethod
    def verify_user(user_id: str) -> Dict:
        """
        Verifica si un usuario existe en el sistema
        
        Args:
            user_id: ID del usuario a verificar
            
        Returns:
            Diccionario con el resultado de la verificación
        """
        try:
            if User.exists(user_id):
                user = User.get_by_id(user_id)
                return success_response(
                    data={'user': user.to_dict()},
                    message="Usuario encontrado"
                )
            else:
                return error_response(
                    message="Usuario no encontrado",
                    status_code=404
                )
        except Exception as e:
            print(f"❌ Error al verificar usuario: {e}")
            return error_response(
                message="Error al verificar usuario",
                status_code=500
            )
