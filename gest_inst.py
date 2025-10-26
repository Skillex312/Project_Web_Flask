from Conexion_bd import ConexionBD
import sqlite3

database_name = 'academia.db'

class Instructor:
    def obtener_datos_instructor(self, id_instructor):
        try:
            connection = ConexionBD(database_name)
            consulta = """
                        SELECT i.Nombre, i.Apellido, i.Rango_Marcial
                        FROM Instructores i
                        JOIN Usuarios u ON u.ID = i.ID_Instruc
                        WHERE u.ID = ?
                    """
            return connection.obtener_uno(consulta, (id_instructor,))
        except sqlite3.Error as err:
            print(f"Error de base de datos: {err}")
            return None

    def obtener_pagos_instructor(self, id_instructor):
        try:
            connection = ConexionBD(database_name)
            consulta = """
                        SELECT Fecha, Concepto, Monto
                        FROM Pagos
                        WHERE ID_Instructor = ?
                    """
            return connection.obtener_resultados(consulta, (id_instructor,))
        except sqlite3.Error as err:
            print(f"Error de base de datos: {err}")
            return []
