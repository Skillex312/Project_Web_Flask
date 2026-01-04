from typing import Optional, List, Dict
from .database import Database
from config import Config

class Student:
    """Modelo de Estudiante - Representa un estudiante de la academia"""
    
    def __init__(self, student_id: str, nombre: str = "", hap_kit: int = 0,
                 cardio: int = 0, krav_maga: int = 0, kung_fu: int = 0,
                 rango: str = "", condicion: str = "", estado: str = "Activo",
                 fecha_registro: str = ""):
        self.student_id = student_id
        self.nombre = nombre
        self.hap_kit = hap_kit
        self.cardio = cardio
        self.krav_maga = krav_maga
        self.kung_fu = kung_fu
        self.rango = rango
        self.condicion = condicion
        self.estado = estado
        self.fecha_registro = fecha_registro
    
    @staticmethod
    def get_by_id(student_id: str) -> Optional['Student']:
        """
        Obtiene un estudiante por su ID
        
        Args:
            student_id: ID del estudiante
            
        Returns:
            Objeto Student si existe, None en caso contrario
        """
        with Database(Config.DATABASE_NAME) as db:
            query = """
                SELECT ID_Estu, Nombre, Hap_Kit, Cardio, Krav_Maga, Kung_Fu, 
                       Rango, Condicion, Estado, Fecha_Registro
                FROM Estudiantes
                WHERE ID_Estu = ?
            """
            result = db.fetch_one(query, (student_id,))
            
            if result:
                return Student(
                    student_id=result['ID_Estu'],
                    nombre=result['Nombre'],
                    hap_kit=result['Hap_Kit'],
                    cardio=result['Cardio'],
                    krav_maga=result['Krav_Maga'],
                    kung_fu=result['Kung_Fu'],
                    rango=result['Rango'],
                    condicion=result['Condicion'],
                    estado=result['Estado'],
                    fecha_registro=result['Fecha_Registro']
                )
            return None
    
    @staticmethod
    def get_all() -> List['Student']:
        """
        Obtiene todos los estudiantes
        
        Returns:
            Lista de objetos Student
        """
        with Database(Config.DATABASE_NAME) as db:
            query = """
                SELECT ID_Estu, Nombre, Hap_Kit, Cardio, Krav_Maga, Kung_Fu,
                       Rango, Condicion, Estado, Fecha_Registro
                FROM Estudiantes
            """
            results = db.fetch_all(query)
            
            return [
                Student(
                    student_id=row['ID_Estu'],
                    nombre=row['Nombre'],
                    hap_kit=row['Hap_Kit'],
                    cardio=row['Cardio'],
                    krav_maga=row['Krav_Maga'],
                    kung_fu=row['Kung_Fu'],
                    rango=row['Rango'],
                    condicion=row['Condicion'],
                    estado=row['Estado'],
                    fecha_registro=row['Fecha_Registro']
                ) for row in results
            ]
    
    def get_attendance(self) -> List[Dict]:
        """
        Obtiene el historial de asistencia del estudiante
        
        Returns:
            Lista de diccionarios con los registros de asistencia
        """
        with Database(Config.DATABASE_NAME) as db:
            query = """
                SELECT Fecha, Nombre_Instructor, Estado
                FROM Registro_Asistencia
                WHERE ID_Estudiante = ?
                ORDER BY Fecha DESC
            """
            results = db.fetch_all(query, (self.student_id,))
            
            return [
                {
                    'fecha': row['Fecha'],
                    'instructor': row['Nombre_Instructor'],
                    'estado': row['Estado']
                } for row in results
            ]
    
    def get_payments(self) -> List[Dict]:
        """
        Obtiene el historial de pagos del estudiante
        
        Returns:
            Lista de diccionarios con los pagos realizados
        """
        with Database(Config.DATABASE_NAME) as db:
            query = """
                SELECT Fecha, Concepto, Monto
                FROM Pagos
                WHERE ID_Estudiante = ?
                ORDER BY Fecha DESC
            """
            results = db.fetch_all(query, (self.student_id,))
            
            return [
                {
                    'fecha': row['Fecha'],
                    'concepto': row['Concepto'],
                    'monto': row['Monto']
                } for row in results
            ]
    
    def to_dict(self) -> Dict:
        """
        Convierte el estudiante a un diccionario
        
        Returns:
            Diccionario con los datos del estudiante
        """
        # Determinar la disciplina principal
        disciplinas = []
        if self.hap_kit:
            disciplinas.append("Hap Ki Do")
        if self.cardio:
            disciplinas.append("Cardio")
        if self.krav_maga:
            disciplinas.append("Krav Maga")
        if self.kung_fu:
            disciplinas.append("Kung Fu")
        
        return {
            'id': self.student_id,
            'nombre': self.nombre,
            'hap_kit': self.hap_kit,
            'cardio': self.cardio,
            'krav_maga': self.krav_maga,
            'kung_fu': self.kung_fu,
            'disciplinas': disciplinas,
            'rango': self.rango,
            'condicion': self.condicion,
            'estado': self.estado,
            'fecha_registro': self.fecha_registro
        }
    
    @staticmethod
    def create(student_data: Dict) -> bool:
        """
        Crea un nuevo estudiante en la base de datos
        
        Args:
            student_data: Diccionario con los datos del estudiante
            
        Returns:
            True si se creó exitosamente, False en caso contrario
        """
        with Database(Config.DATABASE_NAME) as db:
            query = """
                INSERT INTO Estudiantes 
                (ID_Estu, Nombre, Hap_Kit, Cardio, Krav_Maga, Kung_Fu,
                 Rango, Condicion, Estado, Fecha_Registro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            try:
                db.execute_query(query, (
                    student_data['id'],
                    student_data['nombre'],
                    student_data.get('hap_kit', 0),
                    student_data.get('cardio', 0),
                    student_data.get('krav_maga', 0),
                    student_data.get('kung_fu', 0),
                    student_data.get('rango', ''),
                    student_data.get('condicion', 'Nuevo'),
                    student_data.get('estado', 'Activo'),
                    student_data.get('fecha_registro', '')
                ))
                return True
            except Exception as e:
                print(f"❌ Error al crear estudiante: {e}")
                return False
    
    def update_status(self, new_status: str) -> bool:
        """
        Actualiza el estado del estudiante
        
        Args:
            new_status: Nuevo estado
            
        Returns:
            True si se actualizó exitosamente, False en caso contrario
        """
        with Database(Config.DATABASE_NAME) as db:
            query = """
                UPDATE Estudiantes
                SET Estado = ?
                WHERE ID_Estu = ?
            """
            try:
                db.execute_query(query, (new_status, self.student_id))
                self.estado = new_status
                return True
            except Exception as e:
                print(f"❌ Error al actualizar estado: {e}")
                return False
