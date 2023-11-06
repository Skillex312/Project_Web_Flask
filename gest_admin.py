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

class Administrador:
    def obtener_estado_estudiante(id_estudiante):
        try:
            connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
            connection.conectar()
            cursor = connection.conexion.cursor()
            consulta = """
                        SELECT estudiantes.Estado
                        FROM estudiantes
                        WHERE Estudiantes.ID_estu = %s
                        """
            cursor.execute(consulta, (id_estudiante,))
            estado_estudiante = cursor.fetchone()

            if estado_estudiante:
                return estado_estudiante[0]  # Devuelve el estado encontrado
            else:
                return None  # Retorna None si no se encuentra el estado

        except mysql.connector.Error as err:
            print("Error de base de datos: {}".format(err))
            return None
        
    def obtener_nombre_estudiante(id_estudiante):
        try:
            connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
            connection.conectar()
            cursor = connection.conexion.cursor
            consulta = """
                        SELECT estudiantes.Nombre
                        FROM estudiantes
                        WHERE Estudiantes.ID_estu = %s
                    """
            cursor.execute(consulta, (id_estudiante,))
            nombre_estudiante = cursor.fetchone()

            if nombre_estudiante:
                return nombre_estudiante[0]
            else:
                return None

        except mysql.connector.Error as err:
            print("Error de base de datos: {}".format(err))
            return None
        
    def cambiar_estado_estudiante(self, id_estudiante, nuevo_estado):
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar()
        cursor = connection.conexion.cursor()
        consulta = """
                    Select * 
                    FROM estudiantes
                    WHERE ID_estu = %s
                   """
        cursor.execute(consulta, (id_estudiante,))
        estudiante_exis = cursor.fetchone()

        if estudiante_exis:
            actualizacion = """
                            UPDATE Estudiantes 
                            SET Estado = %s 
                            WHERE ID_Estu = %s
                            """
            parametros = (nuevo_estado, id_estudiante)
            cursor.execute(actualizacion, parametros)
            connection.conexion.commit()
            mensaje = ("El estado del estudiante ha sido modificado exitosamente.")
            return mensaje
        else:
            mensaje = ("El estudiante que intentas modificar no existe.")
            return mensaje
        
    def agregar_estudiante(id, nombre, apellido, fecha, direccion, telefono, correo, rango, estado, historial_asis, historial_pagos):
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar()
        cursor = connection.conexion.cursor()
        insercion = """
                    INSERT INTO Estudiantes (ID_Estu, Nombre, Apellido, Fecha_de_Nacimiento, Direccion, Telefono, Correo_Elec, Rango_Marcial, Estado, Historial_Asis, Historial_Pagos) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                    """
        parametros = (id, nombre, apellido, fecha, direccion, telefono, correo, rango, estado, historial_asis, historial_pagos)
        cursor.execute(insercion, parametros)

        inser_usuario = """
                        INSERT INTO Usuarios (ID, Nombre, Contrasena, Tipo) 
                        VALUES (%s, %s, %s, 'Estudiante')
                        """
        parametros_usuario = (id, nombre, id)  # Contraseña igual al ID
        cursor.execute(inser_usuario, parametros_usuario)

        connection.conexion.commit()
        mensaje = ("El estudiante ha sido agregado exitosamente.")
        return mensaje
    
    def agregar_instructor(id, nombre, apellido, rango):
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar()
        cursor = connection.conexion.cursor()
        insercion = """
                    INSERT INTO Instructores (ID_Instruc, Nombre, Apellido, Rango_Marcial)
                    VALUES (%s, %s, %s, %s)
                    """
        parametros = (id, nombre, apellido, rango)
        cursor.execute(insercion, parametros)

        inser_usuario = """
                        INSERT INTO Usuarios (ID, Nombre, Contrasena, Tipo)
                        VALUES (%s, %s, %s, 'Instructor')
                        """
        parametros_usuario = (id, nombre, id) # Contraseña igual al ID
        cursor.execute(inser_usuario, parametros_usuario)

        connection.conexion.commit()
        mensaje = ("El instructor ha sido agregado exitosamente.")
        return mensaje
