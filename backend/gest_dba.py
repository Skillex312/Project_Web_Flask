from Conexion_bd import ConexionBD
import sqlite3

database_name = 'academia.db'

class DBA:
    @staticmethod
    def ver_administrador():
        try:
            connection = ConexionBD(database_name)
            consulta = """
                        SELECT ID, Nombre 
                        FROM Usuarios 
                        WHERE Tipo = 'Administrador'
                        """
            return connection.obtener_resultados(consulta)
        except sqlite3.Error as err:
            print(f"Error de base de datos: {err}")
            return []

    def agregar_admin(self, id, nombre, contraseña):
        try:
            connection = ConexionBD(database_name)
            consulta = """
                        INSERT INTO Usuarios(ID, Nombre, Contrasena, Tipo)
                        VALUES(?, ?, ?, 'Administrador')
                        """
            parametros = (id, nombre, contraseña)
            connection.ejecutar_consulta(consulta, parametros)
        except sqlite3.Error as err:
            print(f"Error de base de datos: {err}")

    def modificar_admin(self, oldid, newid, nombre, contraseña):
        try:
            connection = ConexionBD(database_name)
            consulta_verificacion = "SELECT * FROM Usuarios WHERE ID = ? AND Tipo = 'Administrador'"
            admin_exis = connection.obtener_uno(consulta_verificacion, (oldid,))

            if admin_exis:
                consultamod = """
                            UPDATE Usuarios 
                            SET ID = ?, Nombre = ?, Contrasena = ? 
                            WHERE ID = ?
                           """
                parametros = (newid, nombre, contraseña, oldid)
                connection.ejecutar_consulta(consultamod, parametros)
        except sqlite3.Error as err:
            print(f"Error de base de datos: {err}")

    def eliminar_admin(self, id):
        try:
            connection = ConexionBD(database_name)
            consulta_verificacion = "SELECT * FROM Usuarios WHERE ID = ? AND Tipo = 'Administrador'"
            admin_exis = connection.obtener_uno(consulta_verificacion, (id,))

            if admin_exis:
                eliminacion = "DELETE FROM Usuarios WHERE ID = ?"
                connection.ejecutar_consulta(eliminacion, (id,))
            else:
                print("No existe el administrador")
        except sqlite3.Error as err:
            print(f"Error de base de datos: {err}")
