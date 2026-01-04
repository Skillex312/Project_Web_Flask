from typing import Optional, Dict
import bcrypt
from .database import Database
from config import Config

class User:
    """Modelo de Usuario - Representa un usuario del sistema"""
    
    def __init__(self, user_id: str, password: str, tipo: str, nombre: str = ""):
        self.user_id = user_id
        self.password = password  # Este es el hash, no la contraseña en texto plano
        self.tipo = tipo
        self.nombre = nombre
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Genera un hash bcrypt de la contraseña
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            Hash bcrypt de la contraseña
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verifica si una contraseña coincide con su hash
        
        Args:
            password: Contraseña en texto plano
            hashed_password: Hash bcrypt almacenado
            
        Returns:
            True si coinciden, False en caso contrario
        """
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False
    
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
                SELECT ID, Contrasena, Tipo, Nombre 
                FROM Usuarios 
                WHERE ID = ?
            """
            result = db.fetch_one(query, (username,))
            
            if result:
                stored_password = result['Contrasena']
                
                # Verificar contraseña
                # Soporta tanto contraseñas hasheadas (bcrypt) como texto plano (legacy)
                is_valid = False
                
                # Intentar verificar como hash bcrypt
                if stored_password.startswith('$2'):  # bcrypt hash prefix
                    is_valid = User.verify_password(password, stored_password)
                else:
                    # Contraseña en texto plano (legacy) - comparación directa
                    is_valid = (password == stored_password)
                    
                    # Si es válida, migrar a bcrypt automáticamente
                    if is_valid:
                        User._migrate_password_to_bcrypt(username, password)
                
                if is_valid:
                    return User(
                        user_id=result['ID'],
                        password=stored_password,
                        tipo=result['Tipo'],
                        nombre=result['Nombre']
                    )
            return None
    
    @staticmethod
    def _migrate_password_to_bcrypt(user_id: str, plain_password: str) -> bool:
        """
        Migra una contraseña de texto plano a bcrypt
        
        Args:
            user_id: ID del usuario
            plain_password: Contraseña en texto plano
            
        Returns:
            True si la migración fue exitosa
        """
        try:
            hashed = User.hash_password(plain_password)
            with Database(Config.DATABASE_NAME) as db:
                query = "UPDATE Usuarios SET Contrasena = ? WHERE ID = ?"
                db.execute_query(query, (hashed, user_id))
                print(f"✅ Contraseña migrada a bcrypt para usuario: {user_id}")
                return True
        except Exception as e:
            print(f"⚠️ Error migrando contraseña: {e}")
            return False
    
    @staticmethod
    def update_password(user_id: str, new_password: str) -> bool:
        """
        Actualiza la contraseña de un usuario (hasheada con bcrypt)
        
        Args:
            user_id: ID del usuario
            new_password: Nueva contraseña en texto plano
            
        Returns:
            True si la actualización fue exitosa
        """
        try:
            hashed = User.hash_password(new_password)
            with Database(Config.DATABASE_NAME) as db:
                query = "UPDATE Usuarios SET Contrasena = ? WHERE ID = ?"
                db.execute_query(query, (hashed, user_id))
                return True
        except Exception as e:
            print(f"❌ Error actualizando contraseña: {e}")
            return False
    
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
