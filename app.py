from flask import Flask, render_template, request, redirect, url_for
from Conexion_bd import ConexionBD
from gest_estu import Estudiante
from gest_inst import Instructor
from gest_admin import Administrador
from gest_dba import DBA
import sqlite3

app = Flask(__name__)

# Configuración de la base de datos
database_name = 'academia.db'

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
                    nombre_estudiante, apellido_estudiante, rango_marcial_estudiante = datos_estudiante
                    registros_asistencia = obtener_registros_asistencia_estudiante(username)
                    pagos_estudiante = obtener_pagos_estudiante(username)
                    return render_template('home_login_est.html', nombre_estudiante=nombre_estudiante, apellido_estudiante=apellido_estudiante, rango_marcial_estudiante=rango_marcial_estudiante, registros_asistencia=registros_asistencia, pagos_estudiante=pagos_estudiante)
                
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

# Rutas para Estudiantes, Instructores, Administradores y DBA (sin cambios)

if __name__ == "__main__":
    app.run()
