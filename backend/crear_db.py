import sqlite3
from Conexion_bd import ConexionBD

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

def insertar_usuarios_prueba():
    """Inserta usuarios de prueba en la base de datos"""
    database_name = 'academia.db'
    
    try:
        connection = ConexionBD(database_name)
        connection.conectar()
        
        # Insertar usuarios de prueba
        usuarios = [
            ('EST001', 'Juan Pérez', 'password123', 'Estudiante'),
            ('INS001', 'María González', 'password123', 'Instructor'),
            ('ADM001', 'Carlos Admin', 'password123', 'Administrador'),
            ('DBA001', 'Ana DBA', 'password123', 'DBA')
        ]
        
        for user_id, nombre, password, tipo in usuarios:
            consulta = "INSERT OR IGNORE INTO Usuarios (ID, Nombre, Contrasena, Tipo) VALUES (?, ?, ?, ?)"
            connection.ejecutar_consulta(consulta, (user_id, nombre, password, tipo))
            print(f"✅ Usuario {user_id} insertado correctamente")
        
        # Insertar datos de estudiante
        consulta_est = "INSERT OR IGNORE INTO Estudiantes (ID_Estu, Nombre, Apellido, Rango_Marcial) VALUES (?, ?, ?, ?)"
        connection.ejecutar_consulta(consulta_est, ('EST001', 'Juan', 'Pérez', 'Cinturón Blanco'))
        print("✅ Datos de estudiante insertados")
        
        # Insertar datos de instructor
        consulta_ins = "INSERT OR IGNORE INTO Instructores (ID_Instruc, Nombre, Apellido, Rango_Marcial) VALUES (?, ?, ?, ?)"
        connection.ejecutar_consulta(consulta_ins, ('INS001', 'María', 'González', 'Cinturón Negro'))
        print("✅ Datos de instructor insertados")
        
        print("\n✅ Datos de prueba insertados exitosamente!")
        
    except sqlite3.Error as err:
        print(f"❌ Error al insertar datos: {err}")
    finally:
        if connection:
            connection.cerrar_conexion()

if __name__ == '__main__':
    crear_base_de_datos()
    insertar_usuarios_prueba()
