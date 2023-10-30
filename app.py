from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from Conexion_bd import ConexionBD

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'DESCONocido312',
    'database': 'academia'
}

def obtener_datos_estudiante(username):
    try:
        # Conectar a la base de datos
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar(db_config['host'], db_config['user'], db_config['password'])
        cursor = connection.cursor
        consulta = """
                    SELECT Estudiantes.Nombre, Estudiantes.Apellido, Estudiantes.Rango_Marcial
                    FROM Estudiantes
                    INNER JOIN Usuarios ON Usuarios.ID_Estudiante = Estudiantes.ID_Estu
                    WHERE Usuarios.ID = %s
                    """
        cursor.execute(consulta, (username,))
        datos_estudiante = cursor.fetchone()

        return datos_estudiante

    except mysql.connector.Error as err:
        print("Error de base de datos: {}".format(err))
        return None


def obtener_datos_instructor(username):
    try:
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar(db_config['host'], db_config['user'], db_config['password'])
        cursor = connection.cursor
        consulta = """
            SELECT instructores.Nombre, instructores.Apellido, instructores.Rango_Marcial
            FROM instructores
            INNER JOIN Usuarios ON Usuarios.ID_Instructor = Instructores.ID_Instruc
            WHERE Usuarios.ID = %s
        """
        cursor.execute(consulta, (username,))
        datos_instructor = cursor.fetchone()

        return datos_instructor
    except mysql.connector.Error as err:
        print("Error de base de datos: {}".format(err))
        return None


def autenticar_usuario(username, password):
    try:
        # Conectar a la base de datos pasando los valores de configuración
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar(db_config['host'], db_config['user'], db_config['password'])
        cursor = connection.cursor
        consulta = "SELECT Tipo FROM Usuarios WHERE ID = %s AND Contrasena = %s"
        parametros = (username, password)
        cursor.execute(consulta, parametros)
        resultado = cursor.fetchone()

        if resultado:
            tipo = resultado[0]
            if tipo == 'Estudiante':
                datos_estudiante = obtener_datos_estudiante(username)
                if datos_estudiante:
                    nombre_estudiante = datos_estudiante[0]
                    apellido_estudiante = datos_estudiante[1]
                    rango_marcial_estudiante = datos_estudiante[2]
                    return render_template('home_login_est.html', nombre_estudiante=nombre_estudiante, apellido_estudiante=apellido_estudiante, rango_marcial_estudiante=rango_marcial_estudiante)
                
            elif tipo == 'Instructor':
                datos_instructor = obtener_datos_instructor(username)
                if datos_instructor:
                    nombre_instructor = datos_instructor[0]
                    apellido_instructor = datos_instructor[1]
                    rango_marcial_instructor = datos_instructor[2]
                    return render_template('home_login_ins.html', nombre_instructor=nombre_instructor, apellido_instructor=apellido_instructor,rango_marcial_instructor=rango_marcial_instructor)
                
            elif tipo == 'Administrador':
                return render_template('home_login_adm.html')
            
            elif tipo == 'DBA':
                # Recuperar la información de los administradores
                administradores = obtener_administradores()

                if administradores:
                    return render_template('home_login_dba.html', administradores=administradores)
                else:
                    return redirect(url_for('error'))
        else:
            return redirect(url_for('error'))

    except mysql.connector.Error as err:
        print("Error de base de datos: {}".format(err))
        return redirect(url_for('error'))

def obtener_administradores():
    try:
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar(db_config['host'], db_config['user'], db_config['password'])
        cursor = connection.cursor
        consulta = "SELECT ID, Nombre FROM Usuarios WHERE Tipo = 'Administrador'"
        cursor.execute(consulta)
        administradores = cursor.fetchall()
        return administradores
    except mysql.connector.Error as err:
        print("Error de base de datos: {}".format(err))
        return None

def obtener_estado_estudiante(id_estudiante):
    try:
        # Conectar a la base de datos
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar(db_config['host'], db_config['user'], db_config['password'])
        cursor = connection.cursor

        # Realizar la consulta para obtener el estado del estudiante
        consulta = """
                    SELECT Estudiantes.Estado
                    FROM Estudiantes
                    INNER JOIN Usuarios ON Usuarios.ID_Estudiante = Estudiantes.ID_Estu
                    WHERE Usuarios.ID = %s
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



@app.route("/")
def main():
    return render_template('index.html')

@app.route('/sign')
def showSign():
    return render_template('sign.html')

@app.route('/validar_login', methods=['POST'])
def validar_login():
    # Obtener los valores de los campos de entrada desde la solicitud POST
    username = request.form.get('nombre')
    password = request.form.get('contrasena')

    resultado = autenticar_usuario(username, password)
    return resultado


@app.route('/ver_administradores')
def ver_administradores():
    try:
        # Conectar a la base de datos y obtener administradores
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar(db_config['host'], db_config['user'], db_config['password'])
        cursor = connection.cursor
        consulta = "SELECT ID, Nombre FROM Usuarios WHERE Tipo = 'Administrador'"
        cursor.execute(consulta)
        administradores = cursor.fetchall()

        if administradores:
            return render_template('home_login_dba.html', administradores=administradores)
        else:
            return redirect(url_for('error'))
    except mysql.connector.Error as err:
        print("Error de base de datos: {}".format(err))
        return redirect(url_for('error'))

# Define una ruta para acceder a la página de administradores
@app.route('/administradores')
def administradores():
    return redirect(url_for('ver_administradores'))

@app.route('/agregar_administrador', methods=['POST'])
def agregar_administrador():
    if request.method == 'POST':
        id_new_admin = request.form['id_new_admin']
        name_new_admin = request.form['name_new_admin']
        password_new_admin = request.form['password_new_admin']

        try:
            # Conectar a la base de datos pasando los valores de configuración
            connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
            connection.conectar(db_config['host'], db_config['user'], db_config['password'])
            cursor = connection.cursor

            # Realizar la inserción en la base de datos
            consulta = "INSERT INTO Usuarios (ID, Nombre, Contrasena, Tipo) VALUES (%s, %s, %s, 'Administrador')"
            parametros = (id_new_admin, name_new_admin, password_new_admin)
            cursor.execute(consulta, parametros)
            
            # Ahora, realiza el commit usando la conexión a la base de datos
            connection.connection.commit()
            
            # Después de agregar al administrador, redirecciona a la página de administradores
            return redirect(url_for('ver_administradores'))
        except mysql.connector.Error as err:
            print("Error de base de datos: {}".format(err))
            return redirect(url_for('error'))

    return redirect(url_for('error'))


@app.route('/modificar_administrador', methods=['POST'])
def modificar_administrador():
    if request.method == 'POST':
        findadmin = request.form['findadmin']
        id_mod_admin = request.form['id_mod_admin']
        name_mod_admin = request.form['name_mod_admin']
        password_mod_admin = request.form['password_mod_admin']

        try:
            # Conectar a la base de datos pasando los valores de configuración
            connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
            connection.conectar(db_config['host'], db_config['user'], db_config['password'])
            cursor = connection.cursor

            # Verificar si el administrador existe antes de modificarlo
            consulta_buscar = "SELECT * FROM Usuarios WHERE ID = %s AND Tipo = 'Administrador'"
            cursor.execute(consulta_buscar, (findadmin,))
            administrador_existente = cursor.fetchone()

            if administrador_existente:
                # Realizar la actualización en la base de datos
                consulta_modificar = "UPDATE Usuarios SET ID = %s, Nombre = %s, Contrasena = %s WHERE ID = %s"
                parametros = (id_mod_admin, name_mod_admin, password_mod_admin, findadmin)
                cursor.execute(consulta_modificar, parametros)

                # Ahora, realiza el commit usando la conexión a la base de datos
                connection.connection.commit()

                # Después de modificar al administrador, redirecciona a la página de administradores
                return redirect(url_for('ver_administradores'))
            else:
                return "El administrador que intentas modificar no existe."

        except mysql.connector.Error as err:
            print("Error de base de datos: {}".format(err))
            return redirect(url_for('error'))

    return redirect(url_for('error'))


@app.route('/eliminar_administrador', methods=['POST'])
def eliminar_administrador():
    if request.method == 'POST':
        findadmin = request.form['findadmin']

        try:
            # Conectar a la base de datos pasando los valores de configuración
            connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
            connection.conectar(db_config['host'], db_config['user'], db_config['password'])
            cursor = connection.cursor

            # Verificar si el administrador existe antes de eliminarlo
            consulta_buscar = "SELECT * FROM Usuarios WHERE ID = %s AND Tipo = 'Administrador'"
            cursor.execute(consulta_buscar, (findadmin,))
            administrador_existente = cursor.fetchone()

            if administrador_existente:
                # Realizar la eliminación en la base de datos
                consulta_eliminar = "DELETE FROM Usuarios WHERE ID = %s"
                cursor.execute(consulta_eliminar, (findadmin,))

                # Ahora, realiza el commit usando la conexión a la base de datos
                connection.connection.commit()

                # Después de eliminar al administrador, redirecciona a la página de administradores
                return redirect(url_for('ver_administradores'))
            else:
                return "El administrador que intentas eliminar no existe."

        except mysql.connector.Error as err:
            print("Error de base de datos: {}".format(err))
            return redirect(url_for('error'))

    return redirect(url_for('error'))


@app.route('/consultar_estado_estudiante', methods=['POST'])
def consultar_estado_estudiante():
    if request.method == 'POST':
        id_estudiante = request.form['findest']
        estado_estudiante = obtener_estado_estudiante(id_estudiante) 
        if estado_estudiante is not None:
            # Renderiza la plantilla 'home_login_adm.html' y pasa el estado del estudiante
            return render_template('home_login_adm.html', estado_estudiante=estado_estudiante)
        else:
            mensaje_error = "El estudiante no se encuentra en la base de datos."
            return render_template('home_login_adm.html', mensaje_error=mensaje_error)
    else:
        return redirect(url_for('error'))

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == "__main__":
    app.run()
