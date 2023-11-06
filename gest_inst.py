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

class Instructor:
    def obtener_datos_instructor(self, id_instructor):
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar()
        cursor = connection.conexion.cursor()
        consulta = """
                    SELECT instructores.Nombre, instructores.Apellido, instructores.Rango_Marcial
                    FROM instructores
                    INNER JOIN Usuarios ON Usuarios.ID = Instructores.ID_Instruc
                    WHERE Usuarios.ID = %s
                """
        cursor.execute(consulta, (id_instructor,))
        datos_instructor = cursor.fetchone()

        return datos_instructor
    
    def obtener_pagos_instructor(self, id_instructor):
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar()
        cursor = connection.conexion.cursor()
        consulta = """
                    SELECT Fecha, Concepto, Monto
                    FROM pagos
                    WHERE ID_Instructor = %s
                """
        cursor.execute(consulta, (id_instructor,))
        pagos_instructor = cursor.fetchall()

        return pagos_instructor
