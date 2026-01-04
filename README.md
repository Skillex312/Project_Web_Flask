# Proyecto Final Base de Datos en Flask

## Descripción

Este proyecto es una aplicación web desarrollada en Python utilizando el framework Flask. Se utiliza para gestionar una academia de artes marciales donde todos los integrantes tienen una buena comunicacion por la red. La aplicación se conecta a una base de datos MySQL para almacenar y recuperar datos.

### ✅ Backend API REST (Flask + MVC)
- Arquitectura MVC completa
- Endpoints de autenticación y estudiantes
- Base de datos SQLite
- Respuestas estandarizadas
- CORS configurado

### ✅ Frontend React (TypeScript + Tailwind)
- Servicios API conectados al backend
- Componente Login mejorado con verificación de backend
- Hook personalizado de autenticación (useAuth)
- Modelos TypeScript definidos
- Manejo de errores y estados de carga

## 🚀 Inicio Rápido (5 minutos)

### Paso 1: Preparar el Backend

```bash
# 1. Ir a la carpeta backend
cd backend

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Copiar la base de datos (si no está)
cp ../academia.db .

# 6. Ejecutar el servidor
python api.py
```

✅ **Backend listo en:** http://localhost:5000

---

### Paso 2: Preparar el Frontend

**Abre una NUEVA terminal** (deja el backend corriendo):

```bash
# 1. Ir a la carpeta del frontend
cd frontend

# 2. Instalar dependencias (si no las tienes)
npm install

# 3. Ejecutar el servidor de desarrollo
npm run dev
```

✅ **Frontend listo en:** http://localhost:5173

---

### Paso 3: Probar el Sistema

1. **Abre tu navegador en** http://localhost:5173

2. **Verás el Login con:**
   - ✅ Indicador "Conectado al servidor" (verde)
   - Campos para ID de Usuario y Contraseña

3. **Prueba iniciar sesión con:**
   - **Usuario:** `EST001` (o el ID que tengas en tu BD)
   - **Contraseña:** `password123` (o la que corresponda)

## 🔗 Variables de Entorno

### Backend (`backend/.env`)

```bash
FLASK_ENV=development
SECRET_KEY=clave-secreta
DATABASE_NAME=academia.db
CORS_ORIGINS=http://localhost:5173
```

### Frontend (`frontend/.env`)

```bash
VITE_API_URL=http://localhost:5000/api

## Declaración de derechos

Este proyecto es de código abierto y se proporciona "tal cual", sin garantías de ningún tipo. No se otorga ninguna licencia de propiedad intelectual sobre el proyecto y sus contenidos.

## Créditos
Autor: Maria Fernanda Londoño y Sebastian Ramirez Laserna
Email: m.londono1@utp.edu.co y s.ramirez8@utp.edu.co

## Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.
