# 🥋 Martial House - API REST Backend

Backend desarrollado con Flask siguiendo la arquitectura **MVC (Modelo-Vista-Controlador)**.

## 📁 Estructura del Proyecto

```
backend/
├── api.py                      # Punto de entrada (Factory Pattern)
├── config.py                   # Configuraciones del servidor
├── requirements.txt            # Dependencias Python
├── .env                        # Variables de entorno (NO subir a Git)
│
├── models/                     # MODELO - Lógica de datos
│   ├── __init__.py
│   ├── database.py            # Conexión a BD (Singleton)
│   ├── user.py                # Modelo de Usuario
│   └── student.py             # Modelo de Estudiante
│
├── controllers/                # CONTROLADOR - Lógica de negocio
│   ├── __init__.py
│   ├── auth_controller.py     # Autenticación
│   └── student_controller.py  # Gestión de estudiantes
│
├── routes/                     # Rutas de la API (Endpoints)
│   ├── __init__.py
│   ├── auth_routes.py         # /api/auth/*
│   └── student_routes.py      # /api/students/*
│
└── utils/                      # Utilidades
    ├── __init__.py
    └── responses.py           # Respuestas estandarizadas
```

## 🚀 Instalación

### 1. Crear entorno virtual

```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

El archivo `.env` ya está creado con valores por defecto. Puedes modificarlo si es necesario:

```bash
FLASK_ENV=development
SECRET_KEY=mi-clave-super-secreta-cambiar-en-produccion
DATABASE_NAME=academia.db
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### 4. Verificar la base de datos

Asegúrate de que `academia.db` esté en la carpeta `backend/`. Si no existe, cópiala desde la carpeta raíz.

```bash
# Si necesitas copiar la BD
cp ../academia.db .
```

## ▶️ Ejecutar el Servidor

```bash
python api.py
```

Deberías ver algo como:

```
============================================================
🥋 MARTIAL HOUSE - API REST
============================================================
🌍 Entorno: development
🗄️  Base de datos: academia.db
🔗 CORS habilitado para: http://localhost:5173
🚀 Servidor corriendo en: http://localhost:5000
============================================================
```

## 📡 Endpoints Disponibles

### Autenticación

#### `POST /api/auth/login`
Inicia sesión con credenciales.

**Request:**
```json
{
  "username": "EST001",
  "password": "password123"
}
```

**Response (éxito):**
```json
{
  "success": true,
  "message": "Inicio de sesión exitoso",
  "data": {
    "user": {
      "id": "EST001",
      "nombre": "Juan Pérez",
      "tipo": "Estudiante"
    }
  }
}
```

**Response (error):**
```json
{
  "success": false,
  "message": "Credenciales inválidas",
  "status_code": 401
}
```

#### `POST /api/auth/logout`
Cierra la sesión del usuario.

**Response:**
```json
{
  "success": true,
  "message": "Sesión cerrada exitosamente"
}
```

#### `GET /api/auth/verify/<user_id>`
Verifica si un usuario existe.

**Response:**
```json
{
  "success": true,
  "message": "Usuario encontrado",
  "data": {
    "user": {
      "id": "EST001",
      "nombre": "Juan Pérez",
      "tipo": "Estudiante"
    }
  }
}
```

### Estudiantes

#### `GET /api/students/`
Obtiene todos los estudiantes.

**Response:**
```json
{
  "success": true,
  "data": {
    "students": [
      {
        "id": "EST001",
        "nombre": "Juan",
        "apellido": "Pérez",
        "rango_marcial": "Cinturón Negro",
        "estado": "Activo"
      }
    ],
    "total": 1
  }
}
```

#### `GET /api/students/<student_id>`
Obtiene un estudiante con todos sus detalles.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "EST001",
    "nombre": "Juan",
    "apellido": "Pérez",
    "rango_marcial": "Cinturón Negro",
    "estado": "Activo",
    "asistencia": [
      {
        "fecha": "2024-12-01",
        "instructor": "Carlos Rodríguez",
        "estado": "Presente"
      }
    ],
    "pagos": [
      {
        "fecha": "2024-12-01",
        "concepto": "Mensualidad Diciembre",
        "monto": 50.0
      }
    ]
  }
}
```

#### `POST /api/students/`
Crea un nuevo estudiante.

**Request:**
```json
{
  "id": "EST002",
  "nombre": "María",
  "apellido": "García",
  "fecha_nacimiento": "2000-05-15",
  "direccion": "Calle Principal 123",
  "telefono": "555-1234",
  "correo": "maria@email.com",
  "rango_marcial": "Blanco",
  "estado": "Activo"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Estudiante creado exitosamente",
  "status_code": 201
}
```

#### `PUT /api/students/<student_id>/status`
Actualiza el estado de un estudiante.

**Request:**
```json
{
  "new_status": "Inactivo"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Estado actualizado exitosamente",
  "data": {
    "new_status": "Inactivo"
  }
}
```

## 🔍 Rutas de Utilidad

#### `GET /`
Información de bienvenida y endpoints disponibles.

#### `GET /health`
Verifica el estado del servidor.

**Response:**
```json
{
  "status": "ok",
  "message": "API funcionando correctamente",
  "database": "academia.db"
}
```

## 🧪 Probar la API

### Con curl

```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"EST001","password":"pass123"}'

# Obtener estudiantes
curl http://localhost:5000/api/students/

# Verificar salud
curl http://localhost:5000/health
```

### Con Postman/Thunder Client

1. Importa la URL base: `http://localhost:5000`
2. Crea requests para cada endpoint
3. Asegúrate de usar el método HTTP correcto (GET, POST, PUT)

## 🔐 Seguridad

- Las contraseñas están almacenadas en texto plano (SOLO DESARROLLO)
- En producción debes implementar:
  - Hash de contraseñas (bcrypt)
  - JWT para autenticación
  - HTTPS
  - Rate limiting

## 🐛 Troubleshooting

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "Unable to open database file"
```bash
# Verifica que academia.db esté en la carpeta backend
ls -la academia.db

# Si no está, cópiala
cp ../academia.db .
```

### Error: "Address already in use"
El puerto 5000 está ocupado. Cambia el puerto en `api.py`:
```python
app.run(debug=True, port=5001)  # Usar otro puerto
```

### CORS Error desde el frontend
Verifica que el origen esté en `.env`:
```bash
CORS_ORIGINS=http://localhost:5173
```

## 📚 Arquitectura MVC

- **Modelo** (`models/`): Representa los datos y la lógica de acceso a BD
- **Controlador** (`controllers/`): Procesa las peticiones y coordina el flujo
- **Vista** (Frontend): El frontend React consume esta API REST

## 🔄 Próximos Pasos

1. Implementar endpoints para Instructores
2. Implementar endpoints para Administradores
3. Implementar endpoints para DBA
4. Agregar paginación a listados
5. Agregar filtros y búsqueda
6. Implementar autenticación con JWT
7. Agregar validaciones más robustas
8. Implementar logging
9. Agregar tests unitarios

## 📞 Contacto

Para cualquier duda, consulta con el equipo de desarrollo.
