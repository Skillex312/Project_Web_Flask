import sqlite3
from typing import Optional, List, Tuple, Any

class Database:
    """Clase para manejo de conexión a base de datos SQLite con patrón Singleton"""
    
    _instance: Optional['Database'] = None
    
    def __new__(cls, db_name: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection: Optional[sqlite3.Connection] = None
    
    def connect(self) -> None:
        """Establece conexión con la base de datos"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row  # Para acceder por nombre de columna
            print(f"✅ Conexión exitosa a {self.db_name}")
        except sqlite3.Error as e:
            print(f"❌ Error al conectar a la base de datos: {e}")
            raise
    
    def disconnect(self) -> None:
        """Cierra la conexión a la base de datos"""
        if self.connection:
            self.connection.close()
            print("🔌 Conexión cerrada")
    
    def execute_query(self, query: str, params: Tuple = ()) -> None:
        """
        Ejecuta una consulta sin retorno (INSERT, UPDATE, DELETE)
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros de la consulta
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"❌ Error ejecutando query: {e}")
            raise e
    
    def fetch_one(self, query: str, params: Tuple = ()) -> Optional[sqlite3.Row]:
        """
        Retorna un solo registro
        
        Args:
            query: Consulta SQL SELECT
            params: Parámetros de la consulta
            
        Returns:
            Un registro o None si no existe
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            cursor.close()
            return result
        except sqlite3.Error as e:
            print(f"❌ Error en fetch_one: {e}")
            raise e
    
    def fetch_all(self, query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        """
        Retorna todos los registros
        
        Args:
            query: Consulta SQL SELECT
            params: Parámetros de la consulta
            
        Returns:
            Lista de registros
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results
        except sqlite3.Error as e:
            print(f"❌ Error en fetch_all: {e}")
            raise e
    
    def __enter__(self):
        """Context manager - entrada"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager - salida"""
        self.disconnect()
