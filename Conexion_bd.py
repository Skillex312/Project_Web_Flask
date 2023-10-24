import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="M4f3s1t43312.",
  port=3306,
  database="academia"
)

"""
# Get data

mysql = "select * from usuarios"
mycursor = mydb.cursor()
mycursor.execute(mysql)
myresult = mycursor.fetchall()

# Do something

df = pd.DataFrame()
for x in myresult:
  df2 = pd.DataFrame(list[x]).T
  df = pd.concat([df, df2])
  
df.to_html('/home_login')
"""




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
