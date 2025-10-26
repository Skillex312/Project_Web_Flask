import sqlite3

class ConexionBD:
    def __init__(self, database):
        self.database = database
        self.connection = None
        self.cursor = None

    def conectar(self):
        try:
            self.connection = sqlite3.connect(self.database)
            self.cursor = self.connection.cursor()
            print("Conexión exitosa a SQLite")
        except sqlite3.Error as error:
            print("Error al conectarse a SQLite:", error)
            raise

    def ejecutar_consulta(self, consulta, parametros=None):
        if not self.cursor:
            self.conectar()

        if parametros:
            self.cursor.execute(consulta, parametros)
        else:
            self.cursor.execute(consulta)
        
        if self.connection:
            self.connection.commit()

    def obtener_resultados(self, consulta, parametros=None):
        if not self.cursor:
            self.conectar()
        
        if parametros:
            self.cursor.execute(consulta, parametros)
        else:
            self.cursor.execute(consulta)
        
        return self.cursor.fetchall()

    def obtener_uno(self, consulta, parametros=None):
        if not self.cursor:
            self.conectar()
        
        if parametros:
            self.cursor.execute(consulta, parametros)
        else:
            self.cursor.execute(consulta)
        
        return self.cursor.fetchone()

    def cerrar_conexion(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
