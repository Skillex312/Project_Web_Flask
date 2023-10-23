from flask import Flask, render_template, request 
from Conexion_bd import ConexionBD
app = Flask(__name__)
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/signin')
def showSignin():
    return render_template('sign_in.html')

"""def validar_login('username, password'):
    conexion = ConexionBD('localhost', 'root', 'DESCONocido312', 'academia')
    consulta = ("SELECT * FROM Usuarios WHERE ID = %s AND Password = %s")
    parametros = (username, password)
    resultado = conexion.ejecutar_consulta(consulta, parametros)
    if resultado:
        print("Usuario encontrado")
        return redirect('/success')
    else:
        print("Usuario no encontrado")
        return redirect('/error')"""

@app.route('/validar_login', methods=['POST'])
def validar_login():
    # Obtener los valores de los campos de entrada
    nombre = request.json['nombre']
    contrasena = request.json['contrasena']

    # Validar las credenciales
    if nombre == 'ID' and contrasena == 'Contrasena':
        resultado = True
    else:
        resultado = False

    # Devolver el resultado de la validación como un objeto JSON
    return {'resultado': resultado}

@app.route('/home_login_exitoso')
def home_login_exitoso():
    return render_template('home_login.html')

@app.route('/home_login_error')
def home_login_error():
    return render_template('error.html')
    
if __name__ == "__main__":
    app.run()
