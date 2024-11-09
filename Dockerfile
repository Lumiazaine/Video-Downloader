# Imagen base de Python
FROM python:3.9

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar las dependencias del sistema necesarias para ffmpeg y yt-dlp
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo requirements.txt primero
COPY requirements.txt .

# Instalar las dependencias desde requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install --upgrade yt-dlp

# Copiar toda la aplicación en el contenedor
COPY . .

# Exponer el puerto 1000
EXPOSE 1000

# Ejecutar la aplicación Flask cuando el contenedor se inicie
CMD ["python", "app.py"]