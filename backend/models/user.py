from typing import Optional, Dict
from .database import Database
from config import Config

class User:
    """Modelo de Usuario - Representa un usuario del sistema"""
    
    def __init__(self, user_id: str, password: str, tipo: str, nombre: str = ""):
        self.user_id = user_id
        self.password = password
        self.tipo = tipo
        self.nombre = nombre
    
    @staticmethod
    def authenticate(username: str, password: str) -> Optional['User']:
        """
        Autentica un usuario con sus credenciales
        
        Args:
            username: ID del usuario
            password: Contraseña del usuario
            
        Returns:
            Objeto User si las credenciales son válidas, None en caso contrario
        """
        with Database(Config.DATABASE_NAME) as db:
            query = """
                SELECT ID, Tipo, Nombre 
                FROM Usuarios 
                WHERE ID = ? AND Contrasena = ?
            """
            result = db.fetch_one(query, (username, password))
            
            if result:
                return User(
                    user_id=result['ID'],
                    password=password,
                    tipo=result['Tipo'],
                    nombre=result['Nombre']
                )
            return None
    
    def to_dict(self) -> Dict:
        """
        Convierte el usuario a un diccionario
        
        Returns:
            Diccionario con los datos del usuario (sin contraseña)
        """
        return {
            'id': self.user_id,
            'nombre': self.nombre,
            'tipo': self.tipo
        }
    
    @staticmethod
    def exists(user_id: str) -> bool:
        """
        Verifica si un usuario existe en la base de datos
        
        Args:
            user_id: ID del usuario a verificar
            
        Returns:
            True si existe, False en caso contrario
        """
        with Database(Config.DATABASE_NAME) as db:
            query = "SELECT 1 FROM Usuarios WHERE ID = ?"
            result = db.fetch_one(query, (user_id,))
            return result is not None
    
    @staticmethod
    def get_by_id(user_id: str) -> Optional['User']:
        """
        Obtiene un usuario por su ID
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Objeto User si existe, None en caso contrario
        """
        with Database(Config.DATABASE_NAME) as db:
            query = "SELECT ID, Contrasena, Tipo, Nombre FROM Usuarios WHERE ID = ?"
            result = db.fetch_one(query, (user_id,))
            
            if result:
                return User(
                    user_id=result['ID'],
                    password=result['Contrasena'],
                    tipo=result['Tipo'],
                    nombre=result['Nombre']
                )
            return None
