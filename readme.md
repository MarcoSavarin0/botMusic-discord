
# 🎵 Bot de Música de Discord 🤖

Este es un bot de Discord diseñado para reproducir canciones en canales de voz. Está basado en funcionalidades desarrolladas a partir de este [video tutorial](https://youtu.be/hHfzHVuRx7k?si=b2lxr5H7xPLgKYGF), adaptado y extendido con funciones adicionales.


## Instalación

Antes de comenzar, asegúrate de tener instalados los siguientes elementos:

- [Docker](https://docs.docker.com/desktop/install/windows-install/)
- [Python](https://www.python.org/downloads/)
- [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) (Opcional si vas a usar Docker)


## Antes de iniciar 

    1. Ve a la [Discord Developer Portal](https://discord.com/developers).
    2. Crea una nueva aplicación.
    3. Dirígete a la sección "Bot" y habilita todos los "Privileged Gateway Intents".
    4. Crea el enlace de invitación en OAuth2.
    5. En "OAuth2 URL Generator", selecciona "Bot", marca todas las opciones de "TEXT PERMISSIONS" y "VOICE PERMISSIONS" excepto la de video.
    6. En la sección "Bot", obtén tu token.




    
## Correrlo localmente

Clona el repositorio

```bash
  git clone https://github.com/MarcoSavarin0/botMusic-discord
```

Dirigite a la carpeta

```bash
  cd botMusic-discord
```

Instala las dependencias

```bash
  pip install -r requirements.txt
```


Crea el archivo `.env` y agrega tu token de Discord:

```bash
 DISCORD_TOKEN=AQUI_TU_TOKEN 
```

### Correrlo en tu maquina (Necesitas ffmpeg instalado y configurado)
 
 Para iniciar el bot 
```bash
 Python main.py
```

### Por si no tenes ffmpeg

#### Opción 1: Construir tu propia imagen Docker
Si deseas modificar el código, sigue estos pasos:
```bash
 Docker build -t nombre_de_la_imagen:tag .
 Docker run -d --name contenedor_bot --env-file .env nombre_de_la_imagen:tag 
```

#### Opción 2: Usar una imagen preconfigurada desde [docker hub](https://hub.docker.com/repository/docker/marcosava/botmusic/general)

```bash
 docker pull marcosava/botmusic:tagname
```
(por ahora esta en v2)







## ¿Queres añadir un bot de música a tu Discord?

Contáctame por Gmail y te enviaré la invitación de mi bot alojado en un servidor.
