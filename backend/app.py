from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from Conexion_bd import ConexionBD
from gest_estu import Estudiante
from gest_inst import Instructor
from gest_admin import Administrador
from gest_dba import DBA
import sqlite3

# Importar blueprints
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir peticiones desde el frontend

# Configuración de la base de datos
app.config['DATABASE_NAME'] = 'academia.db'
database_name = 'academia.db'

# Registrar blueprints de la API REST
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)

# ============= RUTAS WEB (para compatibilidad con templates HTML) =============
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/sign')
def showSign():
    return render_template('sign_in.html')

@app.route('/validar_login', methods=['POST'])
def validar_login():
    username = request.form.get('nombre')
    password = request.form.get('contrasena')

    resultado = autenticar_usuario(username, password)
    return resultado

def autenticar_usuario(username, password):
    try:
        connection = ConexionBD(database_name)
        connection.conectar()
        
        consulta = "SELECT Tipo FROM Usuarios WHERE ID = ? AND Contrasena = ?"
        parametros = (username, password)
        resultado = connection.obtener_uno(consulta, parametros)

        if resultado:
            tipo = resultado[0]
            if tipo == 'Estudiante':
                datos_estudiante = obtener_datos_estudiante(username)
                if datos_estudiante:
                    nombre_estudiante, rango_estudiante, condicion_estudiante = datos_estudiante
                    registros_asistencia = obtener_registros_asistencia_estudiante(username)
                    pagos_estudiante = obtener_pagos_estudiante(username)
                    return render_template('home_login_est.html', nombre_estudiante=nombre_estudiante, rango_estudiante=rango_estudiante, condicion_estudiante=condicion_estudiante, registros_asistencia=registros_asistencia, pagos_estudiante=pagos_estudiante)
                
            elif tipo == 'Instructor':
                datos_instructor = obtener_datos_instructor(username)
                if datos_instructor:
                    nombre_instructor, apellido_instructor, rango_marcial_instructor = datos_instructor
                    pagos_instructor = obtener_pagos_instructor(username)
                    return render_template('home_login_ins.html', nombre_instructor=nombre_instructor, apellido_instructor=apellido_instructor, rango_marcial_instructor=rango_marcial_instructor, pagos_instructor=pagos_instructor)

            elif tipo == 'Administrador':
                return render_template('home_login_adm.html')
            
            elif tipo == 'DBA':
                administradores = obtener_administradores()
                if administradores:
                    return render_template('home_login_dba.html', administradores=administradores)
                else:
                    return redirect(url_for('error'))
        else:
            return redirect(url_for('error'))

    except sqlite3.Error as err:
        print(f"Error de base de datos: {err}")
        return redirect(url_for('error'))
    finally:
        if connection:
            connection.cerrar_conexion()

# Funciones auxiliares para las rutas web
def obtener_datos_estudiante(username):
    estudiante = Estudiante()
    return estudiante.obtener_datos_estudiante(username)

def obtener_datos_instructor(username):
    instructor = Instructor()
    return instructor.obtener_datos_instructor(username)

def obtener_registros_asistencia_estudiante(username):
    estudiante = Estudiante()
    return estudiante.obtener_registros_asistencia_estudiantes(username)

def obtener_pagos_estudiante(username):
    estudiante = Estudiante()
    return estudiante.obtener_pagos_estudiante(username)

def obtener_pagos_instructor(username):
    instructor = Instructor()
    return instructor.obtener_pagos_instructor(username)

def obtener_administradores():
    dba = DBA()
    return dba.ver_administrador()

# ============= API REST ENDPOINTS =============
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'API funcionando correctamente'}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
