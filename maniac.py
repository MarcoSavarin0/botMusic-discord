import discord
from discord.ext import commands
import os
import asyncio
import yt_dlp
from dotenv import load_dotenv
import urllib.parse
import urllib.request
import re
from collections import defaultdict

def run_bot():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    client = commands.Bot(command_prefix=".", intents=intents)

    queues = defaultdict(list)
    voice_clients = {}
    vote_disconnect = defaultdict(list)
    vote_next = defaultdict(list)
    
    youtube_base_url = 'https://www.youtube.com/'
    youtube_results_url = youtube_base_url + 'results?'
    youtube_watch_url = youtube_base_url + 'watch?v='
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)

    ffmpeg_options = {
        'executable': 'ffmpeg', 
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn -filter:a "volume=0.25"'
    }

    @client.event
    async def on_ready():
        print(f'{client.user} is now jamming')

    async def play_next(ctx):
        if queues[ctx.guild.id]:
            link = queues[ctx.guild.id].pop(0)
            await play(ctx, link=link)
        else:
            await asyncio.sleep(60)
            if ctx.guild.id in voice_clients and not voice_clients[ctx.guild.id].is_playing():
                await disconnect(ctx)

    @client.command(name="poneme")
    async def play(ctx, *, link):
        try:
            voice_client = voice_clients.get(ctx.guild.id)
            if not voice_client:
                voice_client = await ctx.author.voice.channel.connect()
                voice_clients[ctx.guild.id] = voice_client
        except Exception as e:
            await ctx.send(f"Error connecting to voice channel: {e}")
            return

        try:
            if youtube_base_url not in link:
                query_string = urllib.parse.urlencode({'search_query': link})
                content = urllib.request.urlopen(youtube_results_url + query_string)
                search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())
                link = youtube_watch_url + search_results[0]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))
            song = data['url']
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)

            if voice_client.is_playing():
                queues[ctx.guild.id].append(link)
                await ctx.send(f"Added to queue: {data['title']}")
            else:
                voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))
                await ctx.send(f"Now playing: {data['title']}")
        except Exception as e:
            await ctx.send(f"Error playing song: {e}")

    @client.command(name="limpia_cola")
    async def clear_queue(ctx):
        if ctx.guild.id in queues:
            queues[ctx.guild.id].clear()
            await ctx.send("Queue cleared")
        else:
            await ctx.send("Queue is already empty")

    @client.command(name="para")
    async def pause(ctx):
        try:
            voice_clients[ctx.guild.id].pause()
            await ctx.send("Playback paused")
        except Exception as e:
            await ctx.send(f"Error pausing: {e}")

    @client.command(name="segui")
    async def resume(ctx):
        try:
            voice_clients[ctx.guild.id].resume()
            await ctx.send("Playback resumed")
        except Exception as e:
            await ctx.send(f"Error resuming: {e}")

    @client.command(name="cola")
    async def queue(ctx, *, url):
        queues[ctx.guild.id].append(url)
        await ctx.send("Added to queue")

    @client.command(name="juira")
    async def disconnect(ctx):
        try:
            if ctx.author.guild_permissions.administrator:
                await force_disconnect(ctx)
            else:
                if ctx.author.id not in vote_disconnect[ctx.guild.id]:
                    vote_disconnect[ctx.guild.id].append(ctx.author.id)
                    await ctx.send(f"{ctx.author.name} voted to disconnect. {len(vote_disconnect[ctx.guild.id])}/{required_votes(ctx)} votes needed.")
                    if len(vote_disconnect[ctx.guild.id]) >= required_votes(ctx):
                        await force_disconnect(ctx)
                else:
                    await ctx.send("You have already voted to disconnect.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @client.command(name="prosima")
    async def next(ctx):
        try:
            if ctx.author.guild_permissions.administrator:
                await force_next(ctx)
            else:
                if ctx.author.id not in vote_next[ctx.guild.id]:
                    vote_next[ctx.guild.id].append(ctx.author.id)
                    await ctx.send(f"{ctx.author.name} voted to skip. {len(vote_next[ctx.guild.id])}/{required_votes(ctx)} votes needed.")
                    if len(vote_next[ctx.guild.id]) >= required_votes(ctx):
                        await force_next(ctx)
                else:
                    await ctx.send("You have already voted to skip.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @client.command(name="lista")
    async def listqueue(ctx):
        try:
            if ctx.guild.id in queues and queues[ctx.guild.id]:
                queue_list = []
                for link in queues[ctx.guild.id]:
                    if youtube_base_url in link:
                        data = await asyncio.get_event_loop().run_in_executor(None, lambda: ytdl.extract_info(link, download=False))
                        title = data.get("title", "Unknown title")
                        queue_list.append(title)
                    else:
                        queue_list.append(link)
                await ctx.send(f"Queue ({len(queue_list)} songs):\n" + "\n".join(queue_list))    
            else:
                await ctx.send("Queue is empty")
        except Exception as e:
            await ctx.send(f"Error displaying queue: {e}")

    @client.command(name="ayudame")
    async def help(ctx):
        embed = discord.Embed(title="Ayuda - Comandos del Bot de Música",
                              description="Aquí están los comandos disponibles:",
                              color=discord.Color.blue())

        embed.add_field(name="poneme", value="Reproduce una canción.", inline=False)
        embed.add_field(name="limpia_cola", value="Limpia la cola de reproducción.", inline=False)
        embed.add_field(name="para", value="Pausa la reproducción actual.", inline=False)
        embed.add_field(name="segui", value="Reanuda la reproducción pausada.", inline=False)
        embed.add_field(name="lista", value="Muestra las canciones en la cola de reproducción.", inline=False)
        embed.add_field(name="juira", value="Desconecta el bot del canal de voz.", inline=False)
        embed.add_field(name="prosima", value="Salta a la siguiente canción en la cola.", inline=False)

        await ctx.send(embed=embed)

    async def force_disconnect(ctx):
        try:
            if ctx.guild.id in voice_clients:
                await voice_clients[ctx.guild.id].disconnect()
                del voice_clients[ctx.guild.id]
                await ctx.send("Me desconecté con swag!")
            else:
                await ctx.send("No estoy conectado a ningún canal de voz!")
        except Exception as e:
            await ctx.send(f"Error: {e}")
        finally:
            vote_disconnect[ctx.guild.id].clear()

    async def force_next(ctx):
        try:
            if ctx.guild.id in queues and queues[ctx.guild.id]:
                if voice_clients[ctx.guild.id].is_playing():
                    voice_clients[ctx.guild.id].stop()
                link = queues[ctx.guild.id].pop(0)
                await play(ctx, link=link)
            else:
                await ctx.send("No hay más canciones en mi cola")
        except Exception as e:
            await ctx.send(f"Error: {e}")
        finally:
            vote_next[ctx.guild.id].clear()

    def required_votes(ctx):
        voice_channel = ctx.author.voice.channel
        listeners = len(voice_channel.members)
        return max(1, int(listeners / 2))

    client.run(TOKEN)
