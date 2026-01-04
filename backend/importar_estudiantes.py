import sqlite3
from datetime import datetime

def actualizar_esquema_estudiantes():
    """Actualiza el esquema de la tabla Estudiantes para incluir disciplinas y nuevos campos"""
    try:
        conn = sqlite3.connect('academia.db')
        cursor = conn.cursor()

        # Eliminar tabla antigua si existe y crear nueva con esquema actualizado
        cursor.execute('DROP TABLE IF EXISTS Estudiantes')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Estudiantes (
                ID_Estu TEXT PRIMARY KEY,
                Nombre TEXT NOT NULL,
                Hap_Kit INTEGER DEFAULT 0,
                Cardio INTEGER DEFAULT 0,
                Krav_Maga INTEGER DEFAULT 0,
                Kung_Fu INTEGER DEFAULT 0,
                Rango TEXT,
                Condicion TEXT,
                Fecha_Registro TEXT,
                Estado TEXT DEFAULT 'Activo'
            )
        ''')

        conn.commit()
        print("✅ Esquema de tabla Estudiantes actualizado exitosamente.")
        return conn, cursor

    except sqlite3.Error as e:
        print(f"❌ Error al actualizar esquema: {e}")
        raise

def importar_estudiantes_desde_datos():
    """Importa los estudiantes desde los datos de la captura"""
    
    # Datos extraídos de la captura
    estudiantes = [
        (3827, "Adrián Ramírez", 0, 0, 0, 0, "", "Antiguo"),
        (9465, "Alejandra Durán", 0, 1, 0, 0, "Naranja", "Antiguo"),
        (5039, "Alexa Idalgo", 0, 0, 1, 0, "", "Antiguo"),
        (1296, "Ana Sofia Castillo", 1, 0, 0, 0, "Blanco", "Antiguo"),
        (7754, "Anderson Jimenez", 1, 0, 0, 0, "Rojo", "Antiguo"),
        (6481, "Ángela María Saldarriaga", 0, 0, 1, 0, "", "Antiguo"),
        (158, "Angélica Polanco", 1, 0, 0, 0, "Azul", "Antiguo"),
        (8042, "Anthony Duarte", 1, 0, 0, 0, "", "Antiguo"),
        (2679, "Ashly Mariana Castañeda", 1, 0, 0, 0, "Blanco", "Nuevo"),
        (5508, "Camilo Corrales", 1, 0, 0, 0, "Blanco", "Antiguo"),
        (7310, "Camilo Espinosa", 1, 0, 0, 0, "Negro", "Antiguo"),
        (4176, "Daniel Arenas", 1, 0, 0, 0, "Blanco", "Antiguo"),
        (8921, "Daniel Betancur Castaño", 1, 0, 0, 0, "Amarillo", "Antiguo"),
        (3542, "Daniel Santiago López", 1, 0, 0, 0, "Rojo", "Antiguo"),
        (6330, "Daniela Jimenez Cardona", 1, 0, 0, 0, "Blanco", "Nuevo"),
        (1798, "David Espinosa", 1, 0, 0, 0, "Negro", "Antiguo"),
        (9284, "Felipe Serna", 1, 0, 0, 0, "Rojo", "Antiguo"),
        (4013, "Gabriela Arenas", 1, 0, 0, 0, "Blanco", "Antiguo"),
        (6629, "Gerónimo Grajales", 1, 0, 0, 0, "Verde", "Antiguo"),
        (703, "Isaac Arbelaez", 1, 0, 0, 0, "Amarillo", "Antiguo"),
        (3184, "Isabella Álvarez", 1, 0, 0, 0, "Blanco", "Nuevo"),
        (845, "Isabella Restrepo", 1, 0, 0, 0, "Blanco", "Antiguo"),
        (9520, "Jacobo Ruiz Villada", 1, 0, 0, 0, "Blanco", "Antiguo"),
        (1865, "Jerónimo Loaiza", 1, 0, 0, 0, "Café 2", "Inactivo"),
        (5271, "Jerónimo Parra", 1, 0, 0, 0, "Blanco", "Antiguo"),
        (9436, "Jerónimo Vanegas", 1, 0, 0, 0, "Rojo", "Antiguo"),
        (2710, "Jesús David Aristizabal", 1, 0, 0, 0, "Amarillo", "Antiguo"),
        (5079, "Johan Esteven Aguirre", 1, 0, 0, 0, "Naranja", "Reingreso"),
        (9415, "Jonathan Marín", 1, 0, 0, 0, "Amarillo", "Antiguo"),
        (3740, "José de los Santos Sanchez", 1, 0, 0, 0, "Blanco", "Antiguo"),
        (6183, "Joseph Emiliano Arias", 1, 0, 0, 0, "Verde", "Antiguo"),
        (9324, "Juan Alejandro Largo", 1, 0, 0, 0, "Naranja", "Antiguo"),
        (1639, "Juan Andrés Betancur", 1, 0, 0, 0, "Negro", "Antiguo"),
    ]

    try:
        conn, cursor = actualizar_esquema_estudiantes()
        
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        
        for id_estu, nombre, hap_kit, cardio, krav_maga, kung_fu, rango, condicion in estudiantes:
            cursor.execute('''
                INSERT OR REPLACE INTO Estudiantes 
                (ID_Estu, Nombre, Hap_Kit, Cardio, Krav_Maga, Kung_Fu, Rango, Condicion, Fecha_Registro, Estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (str(id_estu), nombre, hap_kit, cardio, krav_maga, kung_fu, rango, condicion, fecha_actual, 
                  'Inactivo' if condicion == 'Inactivo' else 'Activo'))
        
        conn.commit()
        print(f"✅ {len(estudiantes)} estudiantes importados exitosamente!")
        
        # Verificar importación
        cursor.execute('SELECT COUNT(*) FROM Estudiantes')
        count = cursor.fetchone()[0]
        print(f"📊 Total de estudiantes en la base de datos: {count}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Error al importar estudiantes: {e}")
        raise

if __name__ == '__main__':
    print("🚀 Iniciando importación de estudiantes...")
    importar_estudiantes_desde_datos()
    print("✅ Proceso completado!")
