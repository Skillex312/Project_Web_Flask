from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from Conexion_bd import ConexionBD
from visual_estu import VisualEstu

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'DESCONocido312',
    'database': 'academia'
}

def autenticar_usuario(username, password):
    try:
        # Conectar a la base de datos pasando los valores de configuración
        connection = ConexionBD(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
        connection.conectar(db_config['host'], db_config['user'], db_config['password'])
        cursor = connection.cursor
        consulta = "SELECT * FROM Usuarios WHERE ID = %s AND Contrasena = %s"
        parametros = (username, password)
        cursor.execute(consulta, parametros)
        resultado = cursor.fetchall()

        if resultado:
            return render_template('home_login_est.html')
        else:
            return redirect(url_for('error'))
    except mysql.connector.Error as err:
        print("Error de base de datos: {}".format(err))
        return redirect(url_for('error'))

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

    return autenticar_usuario(username, password)

@app.route('/get_attendance_data', methods=['GET'])
def get_attendance_data():
    return VisualEstu.get_attendance_data_by_id(1)
    
@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == "__main__":
    app.run()
