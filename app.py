import os
import time
from flask import Flask, request, jsonify, send_file, render_template
import yt_dlp
import uuid

app = Flask(__name__)

# Carpeta para almacenar archivos descargados temporalmente
DOWNLOADS_DIRECTORY = "./downloads"

# Crear la carpeta de descargas si no existe
if not os.path.exists(DOWNLOADS_DIRECTORY):
    os.makedirs(DOWNLOADS_DIRECTORY)

# Función para manejar la descarga de video, con opciones múltiples de formato y compatibilidad con iPhone.
def download_video(video_url, video_format="mp4"):
    """ Descargar video y procesar en función de la selección del usuario """
    # Generar un ID único para el archivo descargado
    video_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOADS_DIRECTORY, f'{video_id}.%(ext)s')

    # Configurar múltiples opciones de calidad y formato de descarga
    if video_format == "mp4":
        ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'}
    elif video_format == "mp4_low":
        ydl_opts = {'format': 'worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst[ext=mp4]/worst'}
    elif video_format == "webm":
        ydl_opts = {'format': 'bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best'}
    elif video_format == "audio_only":
        ydl_opts = {'format': 'bestaudio', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]}
    elif video_format == "apple_best":
        ydl_opts = {'format': 'best[ext=mp4]', 'postprocessor_args': ['-c:v', 'libx264', '-c:a', 'aac', '-movflags', 'faststart']}
    else:
        ydl_opts = {'format': 'bestvideo+bestaudio'}

    # Propiedades generales de salida
    ydl_opts.update({
        'outtmpl': output_template,
        'merge_output_format': video_format  # Forzar formato de salida mp4/m4a según lo elegido
    })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Verificar archivo descargado en la carpeta
        for file in os.listdir(DOWNLOADS_DIRECTORY):
            if file.startswith(video_id):
                return os.path.join(DOWNLOADS_DIRECTORY, file)

    except Exception as e:
        return str(e)


# Registro del historial de descargas
def registrar_descarga(video_url, archivo, formato, es_audio=False):
    miniatura = f'/static/music_thumbnail.png' if es_audio else f'/static/video_thumbnail.png'
    with open("descargas.txt", "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}|{video_url}|{archivo}|{miniatura}|{formato}|{'audio' if es_audio else 'video'}\n")

# Mostrar el historial de todas las descargas
@app.route('/historial')
def mostrar_historial():
    historial = []
    try:
        with open("descargas.txt", "r") as f:
            for linea in f.readlines():
                fecha, enlace, archivo, miniatura, formato, tipo = linea.strip().split('|')
                historial.append({
                    'archivo': archivo,
                    'miniatura': miniatura,
                    'fecha': fecha,
                    'formato': formato,
                    'esAudio': tipo == 'audio'
                })
        return jsonify(historial)
    except FileNotFoundError:
        return jsonify(historial)

# Página principal que muestra la interfaz HTML
@app.route("/")
def home():
    return render_template("index.html")

# Ruta de la API para manejar la solicitud de descarga
@app.route("/download", methods=["POST"])
def download():
    try:
        req_data = request.get_json()
        video_url = req_data.get("video_url")
        video_format = req_data.get("format", "mp4")  # Formato extraíble del frontend

        if not video_url:
            return jsonify({"success": False, "error": "No se ha proporcionado una URL válida."})

        # Procesamos la descarga según el formato solicitado
        video_path = download_video(video_url, video_format)
        es_audio = video_format == 'audio_only'

        if video_path and os.path.exists(video_path):
            # Registrar la descarga en el historial
            registrar_descarga(video_url, os.path.basename(video_path), video_format, es_audio)
            return jsonify({"success": True, "downloadUrl": f"/download_file?file={os.path.basename(video_path)}"})
        else:
            return jsonify({"success": False, "error": "Error al descargar el video."})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Ruta para proveer el archivo descargado al navegador
@app.route("/download_file")
def download_file():
    file_name = request.args.get("file")
    file_path = os.path.join(DOWNLOADS_DIRECTORY, file_name)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "Archivo no encontrado", 404

# Ejecutar el servidor Flask en el puerto 1000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1000, debug=True)