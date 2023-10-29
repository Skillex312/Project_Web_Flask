import mysql.connector

class ConexionBD:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def conectar(self, host, user, password):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Conexión exitosa")
            else:
                print("Conexión fallida")
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as error:
            print("Error al conectarse a la base de datos: {}".format(error))
            raise

    def ejecutar_consulta(self, consulta, parametros=None):
        if not self.cursor:
            self.conectar()  # Conecta si el cursor no está inicializado

        self.cursor.execute(consulta, parametros)
        return self.cursor.fetchall()

    def cerrar_conexion(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
