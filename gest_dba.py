from Conexion_bd import ConexionBD
from flask import render_template
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

class DBA:
    def ver_administrador():
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar()
        cursor = connection.conexion.cursor()
        consulta = """
                    SELECT ID, Nombre 
                    FROM Usuarios 
                    WHERE Tipo = 'Administrador'
                    """
        cursor.execute(consulta)
        administradores = cursor.fetchall()
        return administradores
    
    def agregar_admin(self, id, nombre, contraseña):
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar()
        cursor = connection.conexion.cursor()
        consulta = """
                    INSERT INTO Usuarios(ID, Nombre, Contrasena, Tipo)
                    VALUES(%s, %s, %s, 'Administrador')
                    """
        parametros = (id, nombre, contraseña)
        cursor.execute(consulta, parametros)
        connection.conexion.commit()
    
    def modificar_admin(self, oldid, newid, nombre, contraseña):
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar()
        cursor = connection.conexion.cursor()
        consulta = """
                    SELECT * 
                    FROM Usuarios 
                    WHERE ID = %s AND Tipo = 'Administrador'
                   """
        cursor.execute(consulta, (oldid,))
        admin_exis = cursor.fetchone()

        if admin_exis:
            consultamod = """
                        UPDATE Usuarios 
                        SET ID = %s, Nombre = %s, Contrasena = %s 
                        WHERE ID = %s
                       """
            parametros = (newid, nombre, contraseña, oldid)
            cursor.execute(consultamod, parametros)
            connection.conexion.commit()

    def eliminar_admin(self, id):
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar()
        cursor = connection.conexion.cursor()
        consulta = """
                    SELECT * 
                    FROM Usuarios 
                    WHERE ID = %s AND Tipo = 'Administrador'
                   """
        cursor.execute(consulta, (id,))
        admin_exis = cursor.fetchone()

        if admin_exis:
            eliminacion = """
                            DELETE FROM Usuarios 
                            WHERE ID = %s
                          """
            cursor.execute(eliminacion, (id,))
            connection.conexion.commit()
        else:
            print("No existe el administrador")
