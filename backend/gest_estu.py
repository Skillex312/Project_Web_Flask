from Conexion_bd import ConexionBD
import sqlite3

database_name = 'academia.db'

class Estudiante:
    def obtener_datos_estudiante(self, id_estudiante):
        try:
            connection = ConexionBD(database_name)
            consulta = """
                        SELECT e.Nombre, e.Rango, e.Condicion
                        FROM Estudiantes e
                        WHERE e.ID_Estu = ?
                        """
            return connection.obtener_uno(consulta, (id_estudiante,))
        except sqlite3.Error as err:
            print(f"Error de base de datos: {err}")
            return None

    def obtener_registros_asistencia_estudiantes(self, id_estudiante):
        try:
            connection = ConexionBD(database_name)
            consulta = """
                SELECT Fecha, ID_Instructor, Estado
                FROM Asistencia
                WHERE ID_Estudiante = ?
            """
            return connection.obtener_resultados(consulta, (id_estudiante,))
        except sqlite3.Error as err:
            print(f"Error de base de datos: {err}")
            return []

    def obtener_pagos_estudiante(self, id_estudiante):
        try:
            connection = ConexionBD(database_name)
            consulta = """
                SELECT Fecha, Concepto, Monto
                FROM Pagos
                WHERE ID_Estudiante = ?
            """
            return connection.obtener_resultados(consulta, (id_estudiante,))
        except sqlite3.Error as err:
            print(f"Error de base de datos: {err}")
            return []
