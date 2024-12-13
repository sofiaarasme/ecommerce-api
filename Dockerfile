# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todos los archivos del directorio actual (donde está Dockerfile) al contenedor
COPY . /app

RUN pip install --upgrade pip setuptools

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expone el puerto 8000 para la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]