import mysql.connector
from Conexion_bd import ConexionBD
from flask import redirect, url_for, jsonify

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'DESCONocido312',
    'database': 'academia'
}

class VisualEstu:
    def get_attendance_data_by_id(id):
        try:
            # Conectar a la base de datos pasando los valores de configuración
            connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
            connection.conectar(db_config['host'], db_config['user'], db_config['password'])
            cursor = connection.cursor
            cursor.execute("SELECT Fecha, Asistencia.Estado, Instructores.Nombre AS Nombre_Instructor FROM Asistencia INNER JOIN Instructores on Asistencia.ID_Instructor = Instructores.ID_Instruc WHERE ID = %s", (id,))
            resultado = cursor.fetchall()

            if len(resultado) == 0:
                return None
            
            return jsonify(resultado)
        except mysql.connector.Error as err:
            print("Error de base de datos: {}".format(err))
            return redirect(url_for('error'))
