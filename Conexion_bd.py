import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="DESCONocido312",
  database="academia"
)

if mydb.is_connected():
    print("Conexión exitosa a la base de datos")
else:
    print("No se pudo conectar a la base de datos")

print(mydb)