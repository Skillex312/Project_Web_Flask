from flask import Flask, render_template, request, jsonify
from Conexion_bd import ConexionBD


app = Flask(__name__)
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/sign')
def showSign():
    return render_template('sign.html')

@app.route('/validar_login', methods=['POST'])
def valida_login():
    # Obtener los valores de los campos de entrada desde la solicitud POST
    username = request.form['username']
    password = request.form['password']

    print('username:', username)
    print('password:', password)
    # Conectar a la base de datos
    conexion = ConexionBD('localhost', 'root', 'M4f3s1t43312.', 'academia')

    # Ejecutar una consulta para obtener el usuario con el nombre de usuario y la contraseña proporcionados
    consulta = "SELECT * FROM Usuarios WHERE ID = %s AND Password = %s"
    parametros = (username, password)
    resultado = conexion.ejecutar_consulta(consulta, parametros) 

    # Validar las credenciales
    if resultado:
        print("Usuario encontrado")
        return jsonify({'valid': True})
    else:
        print("Usuario no encontrado")
        return jsonify({'valid': False})

if __name__ == "__main__":
    app.run()
