from Conexion_bd import ConexionBD
import mysql.connector

db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'DESCONocido312',
            'database': 'academia'
        }

class ConexionBD:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conexion = None

    def conectar(self):
        self.conexion = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

class Estudiante:

    def obtener_datos_estudiante(self, id_estudiante):
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar()
        cursor = connection.conexion.cursor()
        consulta = """
                    SELECT estudiantes.Nombre, estudiantes.Apellido, estudiantes.Rango_Marcial 
                    FROM estudiantes
                    INNER JOIN Usuarios ON Usuarios.ID = Estudiantes.ID_Estu
                    WHERE Usuarios.ID = %s
                    """
        cursor.execute(consulta, (id_estudiante,))
        datos_estudiante = cursor.fetchone()

        return datos_estudiante
    
    def obtener_registros_asistencia_estudiantes(self, id_estudiante):
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar()
        cursor = connection.conexion.cursor()
        consulta = """
            SELECT Fecha, ID_Instructor, Estado
            FROM asistencia
            WHERE ID_Estudiante = %s
        """
        cursor.execute(consulta, (id_estudiante,))
        registros_asistencia = cursor.fetchall()

        return registros_asistencia
    
    def obtener_pagos_estudiante(self, id_estudiante):
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar()
        cursor = connection.conexion.cursor()
        consulta = """
            SELECT Fecha, Concepto, Monto
            FROM pagos
            WHERE ID_Estudiante = %s
        """
        cursor.execute(consulta, (id_estudiante,))
        pagos_estudiante = cursor.fetchall()

        return pagos_estudiante
