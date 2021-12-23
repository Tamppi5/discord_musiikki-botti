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
    except AttributeError:
        await ctx.send("Sinun on liityttävä puhekanavalle")
        return
    except: pass
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
        video = search(haku)
        info_dict = ydl.extract_info(video, download=False)
        video_title = info_dict.get('title', None)
        duration = info_dict.get('duration', None)
        await ctx.send(duration)
        if duration > 1200:
            await ctx.send(":MullaEiOlePaitaa:")
            return
        ydl.download(video)
        await ctx.send("Nyt bängää: " + video_title)


    for file in os.listdir("./"):
        if (file.endswith(".mp3")) and not (file.startswith("bababooey")):
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio('song.mp3'))

@client.command()
async def leave(ctx):
    try:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        try: voice.stop()
        except: pass

        voice.play(discord.FFmpegPCMAudio('bababooey.mp3'))
        time.sleep(1)

        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("bruh")
    except Exception: await ctx.send("bruh en ole edes puhekanavalla")

@client.command()
async def pause(ctx):
    try:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.pause()
    except:
        await ctx.send("Ei soi mitään veli")

@client.command()
async def resume(ctx):
    try:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.resume()
    except:
        await ctx.send("your mom gay")

@client.command()
async def stop(ctx):
    try:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.stop()
    except:
        await ctx.send("ei soi mitään veli")



client.run('OTIyNDc2MjM2OTgxMjcyNjU2.YcCA8Q.iXbNBmST7R0eCk0yQIbWugyOjdQ')