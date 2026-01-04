from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from Conexion_bd import ConexionBD
from gest_estu import Estudiante
from gest_inst import Instructor
from gest_admin import Administrador
from gest_dba import DBA
from config import Config
import sqlite3

# Importar blueprints
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp

app = Flask(__name__)

# Configuración de la aplicación
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.JWT_ACCESS_TOKEN_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = Config.JWT_REFRESH_TOKEN_EXPIRES
app.config['JWT_TOKEN_LOCATION'] = Config.JWT_TOKEN_LOCATION
app.config['JWT_HEADER_NAME'] = Config.JWT_HEADER_NAME
app.config['JWT_HEADER_TYPE'] = Config.JWT_HEADER_TYPE

# Inicializar extensiones
CORS(app)  # Habilitar CORS para permitir peticiones desde el frontend
jwt = JWTManager(app)  # Inicializar JWT

# Configuración de la base de datos
app.config['DATABASE_NAME'] = Config.DATABASE_NAME
database_name = Config.DATABASE_NAME

# Callbacks de JWT para manejo de errores
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'success': False,
        'message': 'Token expirado',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'success': False,
        'message': 'Token inválido',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'success': False,
        'message': 'Token de acceso requerido',
        'error': 'authorization_required'
    }), 401

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
