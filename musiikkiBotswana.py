import discord
from discord.ext import commands
import yt_dlp
import os
import urllib.request
import re
import time

def search(search):
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search.replace(" ","_"))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return("https://www.youtube.com/watch?v=" + video_ids[0])


client = commands.Bot(command_prefix=".")

@client.command()
async def play(ctx, *, haku : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("käytä stop-komentoa")
        return

    try:
        voice_channel = ctx.author.voice.channel
        await voice_channel.connect()
    except AttributeError: await ctx.send("Käyttäjä ei ole puhekanavalla")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search(haku))
        await ctx.send(info['duration'])
        if info['duration'] > 600:
            return
        else:
            ydl.download([search(haku)])
            for file in os.listdir("./"):
                if (file.endswith(".mp3")) and not (file.startswith("bababooey")):
                    await ctx.send("Nyt bängää: " + file.rpartition(".")[0].rpartition("[")[0])
                    os.rename(file, "song.mp3")

            voice.play(discord.FFmpegPCMAudio('song.mp3'))

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try: voice.stop()
    except: print()

    
    voice.play(discord.FFmpegPCMAudio('bababooey.mp3'))
    time.sleep(1)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("bruh.")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Ei soi mitään veli")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("your mom gay")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()



client.run('OTIyNDc2MjM2OTgxMjcyNjU2.YcCA8Q.iXbNBmST7R0eCk0yQIbWugyOjdQ')