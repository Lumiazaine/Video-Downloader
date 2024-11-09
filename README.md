# 🎥 Downloader

Una apliación web hecha para descargar audios y videos, sin anuncios, ni esperas.

## 🚀 Características

- 📥 **Descargar videos**: Guarda tus videos favoritos en tu dispositivo.
- 🎶 **Convertir a MP3**: Extrae el audio de los videos para escucharlos en cualquier momento.
- 🗂️ **Historial de archivos**: Accede a un registro de todos tus archivos descargados.

## 🛠️ Instalación y Ejecución

Sigue estos pasos para construir y ejecutar la aplicación en un contenedor Docker:

### 1. Clonar el Repositorio

Clona este repositorio en tu máquina local para acceder a los archivos del proyecto:

```bash
git clone https://github.com/Lumiazaine/Downloader.git
cd Downloader
```

### 2. Construir el contendor y ejecutarlo

⚙️ A continuación ejecuta los siguentes comandos:

```bash
docker build -t video-downloader-app .
docker run -d -p 1000:1000 --name video-downloader video-downloader-app
```

Una vez hecho, podrás acceder desde http://localhost:1000
