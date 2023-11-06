from flask import Flask, render_template, request, redirect, url_for
from Conexion_bd import ConexionBD
from gest_estu import Estudiante
from gest_inst import Instructor
from gest_admin import Administrador
from gest_dba import DBA
import mysql.connector


app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'DESCONocido312',
    'database': 'academia'
}

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
                    registros_asistencia = obtener_registros_asistencia_estudiante(username)
                    pagos_estudiante = obtener_pagos_estudiante(username)  # Nueva línea para obtener los pagos
                    return render_template('home_login_est.html', nombre_estudiante=nombre_estudiante, apellido_estudiante=apellido_estudiante, rango_marcial_estudiante=rango_marcial_estudiante, registros_asistencia=registros_asistencia, pagos_estudiante=pagos_estudiante)
                
            elif tipo == 'Instructor':
                datos_instructor = obtener_datos_instructor(username)
                if datos_instructor:
                    nombre_instructor = datos_instructor[0]
                    apellido_instructor = datos_instructor[1]
                    rango_marcial_instructor = datos_instructor[2]
                    pagos_instructor = obtener_pagos_instructor(username)  # Nueva línea para obtener los pagos
                    return render_template('home_login_ins.html', nombre_instructor=nombre_instructor, apellido_instructor=apellido_instructor, rango_marcial_instructor=rango_marcial_instructor, pagos_instructor=pagos_instructor)

                
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
    
# Ruta Estudiantes

def obtener_datos_estudiante(username):
    try:
        estudiante = Estudiante()
        datos_estudiante = estudiante.obtener_datos_estudiante(username)
        return datos_estudiante
    except mysql.connector.Error as err:
        print("Error de base de datos: {}".format(err))
        return None
    
def obtener_registros_asistencia_estudiante(username):
    try:
        estudiante = Estudiante()
        registros_asistencia = estudiante.obtener_registros_asistencia_estudiantes(username)
        return registros_asistencia
    except mysql.connector.Error as err:
        print("Error de base de datos: {}".format(err))
        return None
    
def obtener_pagos_estudiante(username):
    try:
        estudiante = Estudiante()
        pagos_estudiante = estudiante.obtener_pagos_estudiante(username)
        return pagos_estudiante
    except mysql.connector.Error as err:
        print("Error de base de datos: {}".format(err))
        return None
    
# Ruta Instructores

def obtener_datos_instructor(username):
    try:
        instructor = Instructor()
        datos_instructor = instructor.obtener_datos_instructor(username)
        return datos_instructor
    except mysql.connector.Error as err:
        print("Error de base de datos: {}".format(err))
        return None

def obtener_pagos_instructor(username):
    try:
        instructor = Instructor()
        pagos_instructor = instructor.obtener_pagos_instructor(username)
        return pagos_instructor
    except mysql.connector.Error as err:
        print("Error de base de datos: {}".format(err))
        return None
    
# Ruta Administradores

@app.route('/consultar_estado_estudiante', methods=['POST'])
def consultar_estado_estudiante():
    if request.method == 'POST':
        id_estudiante = request.form['findest']
        estado_estudiante = Administrador.obtener_estado_estudiante(id_estudiante)
        nombre_estudiante = Administrador.obtener_nombre_estudiante(id_estudiante)
        if estado_estudiante is not None and nombre_estudiante is not None:
            return render_template('home_login_adm.html', estado_estudiante=estado_estudiante, nombre_estudiante=nombre_estudiante)
        else:
            print("El estudiante no se encuentra en la base de datos.")
            return render_template('home_login_adm.html', estado_estudiante=estado_estudiante, nombre_estudiante=nombre_estudiante)
    else:
        return redirect(url_for('error'))
    
@app.route('/cambiar_estado_estudiante', methods=['POST'])
def cambiar_estado_estudiante():
    id_estudiante = request.form['id_estudiante']
    nuevo_estado = request.form['nuevo_estado']
    try:
        administrador = Administrador()
        mensaje = administrador.cambiar_estado_estudiante(id_estudiante, nuevo_estado)
        if mensaje == "Estado del estudiante actualizado":
            return render_template('home_login_adm.html', mensaje=mensaje)
        else:
            return render_template('home_login_adm.html', mensaje=mensaje)

    except mysql.connector.Error as err:
        print("Error de base de datos: {}".format(err))
        return redirect(url_for('error'))
    
@app.route('/agregar_estudiante', methods=['POST'])
def agregar_estudiante():
    # Obtener los datos del formulario
    id_estudiante = request.form['id_estudiante']
    nombre_estudiante = request.form['nombre_estudiante']
    apellido_estudiante = request.form['apellido_estudiante']
    fecha_nacimiento = request.form['fecha_nacimiento']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    correo_elec = request.form['correo_elec']
    rango_marcial = ''  # Establecemos como NULL
    estado = 'Activo'  # Puedes cambiar el estado predeterminado si lo deseas
    historial_asis = ''  # Establecemos como NULL
    historial_pagos = ''  # Establecemos como NULL

    mensaje1 = Administrador.agregar_estudiante(id_estudiante, nombre_estudiante, apellido_estudiante, fecha_nacimiento, direccion, telefono, correo_elec, rango_marcial, estado, historial_asis, historial_pagos)
    return render_template('home_login_adm.html', mensaje1=mensaje1)

@app.route('/agregar_instructor', methods=['POST'])
def agregar_instructor():
    id_instructor = request.form['id_instructor']
    nombre_instructor = request.form['nombre_instructor']
    apellido_instructor = request.form['apellido_instructor']
    rango_marcial = request.form['rango_marcial']  

    mensaje2 = Administrador.agregar_instructor(id_instructor, nombre_instructor, apellido_instructor, rango_marcial)
    return render_template('home_login_adm.html', mensaje2=mensaje2)

# Ruta DBA

@app.route('/administradores')
def administradores():
    return redirect(url_for('ver_administradores'))

@app.route('/ver_administradores')
def ver_administradores():
    try:
        administradores = obtener_administradores()
        if administradores:
            return render_template('home_login_dba.html', administradores=administradores)
        else:
            return redirect(url_for('error'))
    except mysql.connector.Error as err:
        print("Error de base de datos: {}".format(err))
        return redirect(url_for('error'))

def obtener_administradores():
    try:
        administradores = DBA.ver_administrador()
        return administradores
    except mysql.connector.Error as err:
        print("Error de base de datos: {}".format(err))
        return None

@app.route('/agregar_administrador', methods=['POST'])
def agregar_administrador():
    id_new_admin = request.form['id_new_admin']
    name_new_admin = request.form['name_new_admin']
    password_new_admin = request.form['password_new_admin']

    dba = DBA()
    dba.agregar_admin(id_new_admin, name_new_admin, password_new_admin)
    return redirect(url_for('ver_administradores'))

@app.route('/modificar_administrador', methods=['POST'])
def modificar_administrador():
    if request.method == 'POST':
        findadmin = request.form['findadmin']
        id_mod_admin = request.form['id_mod_admin']
        name_mod_admin = request.form['name_mod_admin']
        password_mod_admin = request.form['password_mod_admin']

        dba = DBA()
        dba.modificar_admin(findadmin, id_mod_admin, name_mod_admin, password_mod_admin)
        return redirect(url_for('ver_administradores'))

@app.route('/eliminar_administrador', methods=['POST'])
def eliminar_administrador():
    findadmin = request.form['findadmin']
    # Después de eliminar al administrador, redirecciona a la página de administradores
    dba = DBA()
    dba.eliminar_admin(findadmin)
    return redirect(url_for('ver_administradores'))


@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == "__main__":
    app.run()
