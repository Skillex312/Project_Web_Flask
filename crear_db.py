import sqlite3

def crear_base_de_datos():
    try:
        conn = sqlite3.connect('academia.db')
        cursor = conn.cursor()

        # Crear tabla Usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuarios (
                ID TEXT PRIMARY KEY,
                Nombre TEXT NOT NULL,
                Contrasena TEXT NOT NULL,
                Tipo TEXT NOT NULL
            )
        ''')

        # Crear tabla Estudiantes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Estudiantes (
                ID_Estu TEXT PRIMARY KEY,
                Nombre TEXT NOT NULL,
                Apellido TEXT NOT NULL,
                Fecha_de_Nacimiento TEXT,
                Direccion TEXT,
                Telefono TEXT,
                Correo_Elec TEXT,
                Rango_Marcial TEXT,
                Estado TEXT,
                Historial_Asis TEXT,
                Historial_Pagos TEXT,
                FOREIGN KEY (ID_Estu) REFERENCES Usuarios(ID)
            )
        ''')

        # Crear tabla Instructores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Instructores (
                ID_Instruc TEXT PRIMARY KEY,
                Nombre TEXT NOT NULL,
                Apellido TEXT NOT NULL,
                Rango_Marcial TEXT,
                FOREIGN KEY (ID_Instruc) REFERENCES Usuarios(ID)
            )
        ''')

        # Crear tabla Asistencia
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Asistencia (
                ID_Asistencia INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_Estudiante TEXT,
                Fecha TEXT,
                ID_Instructor TEXT,
                Estado TEXT,
                FOREIGN KEY (ID_Estudiante) REFERENCES Estudiantes(ID_Estu),
                FOREIGN KEY (ID_Instructor) REFERENCES Instructores(ID_Instruc)
            )
        ''')

        # Crear tabla Pagos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pagos (
                ID_Pago INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_Estudiante TEXT,
                Fecha TEXT,
                Concepto TEXT,
                Monto REAL,
                ID_Instructor TEXT,
                FOREIGN KEY (ID_Estudiante) REFERENCES Estudiantes(ID_Estu),
                FOREIGN KEY (ID_Instructor) REFERENCES Instructores(ID_Instruc)
            )
        ''')

        conn.commit()
        print("Base de datos y tablas creadas exitosamente.")

    except sqlite3.Error as e:
        print(f"Error al crear la base de datos: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    crear_base_de_datos()
