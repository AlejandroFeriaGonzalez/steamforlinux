# Usar una imagen base oficial de Python
FROM python:3.12-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requerimientos y el archivo pyproject.toml al contenedor
COPY requirements.txt pyproject.toml ./

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt



# Copiar el resto del código de la aplicación al contenedor
COPY ./src /app/src
# COPY templates/ ./templates/
# COPY static/ ./static/

# Copiar el archivo .env al contenedor
# COPY .env /app/.env

# Exponer el puerto en el que la aplicación correrá
# EXPOSE 8000

# Comando para correr la aplicación
CMD ["fastapi", "run", "src/main.py", "--port", "8080"]

# docker run --env-file .env  -p 80:80 steamforlinux