FROM python:3.9

# Instalación de FFmpeg
RUN apt-get update \
    && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Resto de tu Dockerfile (copiar código, instalar dependencias Python, etc.)
COPY . /app
WORKDIR /app

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar el bot
CMD ["python", "main.py"]
