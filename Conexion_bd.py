import mysql.connector

# Establecer la conexión con la base de datos
class ConexionBD:
  def __init__(self, host, user, password, database):
    try:
      print("Conectando a la base de datos...")
      self.connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
      self.cursor = self.connection.cursor()
    except mysql.connector.Error as error:
      print("Error al conectarse a la base de datos: {}".format(error))
      raise

  def ejecutar_consulta(self, consulta, parametros = None):
    self.cursor.execute(consulta, parametros)
    return self.cursor.fetchall()
