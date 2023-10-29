# Flask_app

Este es un proyecto de ejemplo de una aplicación web utilizando el framework Flask de Python.

# Requisitos previos
  - Python 3.x
  - Flask
  - MySQL Connector

# Instalación
  - Clonar el repositorio: git clone https://github.com/usuario/flask_app.git
  - Instalar las dependencias: pip install -r requirements.txt
  - Configurar la base de datos en el archivo app.py
  - Ejecutar la aplicación: python app.py
    
# Uso
  - Acceder a la aplicación en el navegador web: http://localhost:5000
  - Iniciar sesión con un nombre de usuario y contraseña válidos
  - Ver los datos de asistencia de un estudiante específico en la ruta /get_attendance_data

# Estructura del proyecto
  - app.py: archivo principal de la aplicación Flask
  - templates/: directorio que contiene las plantillas HTML de la aplicación
  - static/: directorio que contiene los archivos estáticos (CSS, JavaScript, imágenes, etc.) de la aplicación
  - Conexion_bd.py: archivo que contiene la clase ConexionBD para conectarse a la base de datos
  - visual_estu.py: archivo que contiene la clase VisualEstu para visualizar los datos de asistencia

# Contribución
  - Hacer un fork del repositorio
  - Crear una rama para la nueva funcionalidad: git checkout -b nueva-funcionalidad
  - Hacer los cambios necesarios y hacer commit: git commit -am 'Agregar nueva funcionalidad'
  - Hacer push a la rama: git push origin nueva-funcionalidad
  - Crear un pull request en GitHub

# Créditos
Autor: Maria Fernanda Londoño y Sebastian Ramirez Laserna
Email: m.londono8@utp.edu.co y s.ramirez8@utp.edu.co

# Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.
