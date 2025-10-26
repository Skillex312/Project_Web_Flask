from Conexion_bd import ConexionBD
import sqlite3

database_name = 'academia.db'

class Administrador:
    @staticmethod
    def obtener_estado_estudiante(id_estudiante):
        try:
            connection = ConexionBD(database_name)
            consulta = """
                        SELECT Estado
                        FROM Estudiantes
                        WHERE ID_estu = ?
                        """
            resultado = connection.obtener_uno(consulta, (id_estudiante,))
            return resultado[0] if resultado else None
        except sqlite3.Error as err:
            print(f"Error de base de datos: {err}")
            return None

    @staticmethod
    def obtener_nombre_estudiante(id_estudiante):
        try:
            connection = ConexionBD(database_name)
            consulta = """
                        SELECT Nombre
                        FROM Estudiantes
                        WHERE ID_estu = ?
                    """
            resultado = connection.obtener_uno(consulta, (id_estudiante,))
            return resultado[0] if resultado else None
        except sqlite3.Error as err:
            print(f"Error de base de datos: {err}")
            return None

    def cambiar_estado_estudiante(self, id_estudiante, nuevo_estado):
        try:
            connection = ConexionBD(database_name)
            consulta_verificacion = "SELECT * FROM Estudiantes WHERE ID_estu = ?"
            estudiante_exis = connection.obtener_uno(consulta_verificacion, (id_estudiante,))

            if estudiante_exis:
                consulta_actualizacion = """
                                UPDATE Estudiantes 
                                SET Estado = ? 
                                WHERE ID_Estu = ?
                                """
                parametros = (nuevo_estado, id_estudiante)
                connection.ejecutar_consulta(consulta_actualizacion, parametros)
                return "El estado del estudiante ha sido modificado exitosamente."
            else:
                return "El estudiante que intentas modificar no existe."
        except sqlite3.Error as err:
            print(f"Error de base de datos: {err}")
            return "Error al actualizar el estado del estudiante."

    @staticmethod
    def agregar_estudiante(id, nombre, apellido, fecha, direccion, telefono, correo, rango, estado, historial_asis, historial_pagos):
        try:
            connection = ConexionBD(database_name)
            insercion_estudiante = """
                        INSERT INTO Estudiantes (ID_Estu, Nombre, Apellido, Fecha_de_Nacimiento, Direccion, Telefono, Correo_Elec, Rango_Marcial, Estado, Historial_Asis, Historial_Pagos) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
                        """
            parametros_estudiante = (id, nombre, apellido, fecha, direccion, telefono, correo, rango, estado, historial_asis, historial_pagos)
            connection.ejecutar_consulta(insercion_estudiante, parametros_estudiante)

            insercion_usuario = """
                            INSERT INTO Usuarios (ID, Nombre, Contrasena, Tipo) 
                            VALUES (?, ?, ?, 'Estudiante')
                            """
            parametros_usuario = (id, nombre, id)  # Contraseña igual al ID
            connection.ejecutar_consulta(insercion_usuario, parametros_usuario)
            return "El estudiante ha sido agregado exitosamente."
        except sqlite3.Error as err:
            print(f"Error de base de datos: {err}")
            return "Error al agregar al estudiante."

    @staticmethod
    def agregar_instructor(id, nombre, apellido, rango):
        try:
            connection = ConexionBD(database_name)
            insercion_instructor = """
                        INSERT INTO Instructores (ID_Instruc, Nombre, Apellido, Rango_Marcial)
                        VALUES (?, ?, ?, ?)
                        """
            parametros_instructor = (id, nombre, apellido, rango)
            connection.ejecutar_consulta(insercion_instructor, parametros_instructor)

            insercion_usuario = """
                            INSERT INTO Usuarios (ID, Nombre, Contrasena, Tipo)
                            VALUES (?, ?, ?, 'Instructor')
                            """
            parametros_usuario = (id, nombre, id) # Contraseña igual al ID
            connection.ejecutar_consulta(insercion_usuario, parametros_usuario)
            return "El instructor ha sido agregado exitosamente."
        except sqlite3.Error as err:
            print(f"Error de base de datos: {err}")
            return "Error al agregar al instructor."
