import os
import discord
import random
from discord.utils import get
import youtube_dl
from discord.ext import commands
from dotenv import load_dotenv
import ffmpeg
import pyttsx3

# For tts
engine = pyttsx3.init()
engine.setProperty('rate', 150)    # Speed percent (can go over 100)
engine.setProperty('volume', 0.9)

# Loading the env file which stores token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(bot.user.name + " has joined \n")

@bot.command(pass_context = True,aliases = ['l','lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients,guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send("Bye Frandz")
    else:
        print("I'm not in the channel.")
        await ctx.send("I dont think I am in a voice channel")

@bot.command(pass_context = True,aliases = ['baja','bajao','p'])
async def play(ctx,url:str):

    # Joining voice channel
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients,guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)

    else:
        voice = await channel.connect()

    # Downloading and playing the song
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file.")

    except PermissionError:
        print("Tried to delete but a song is being already played.")
        await ctx.send("Bhai already ek gaana baj raha hai.")
        return

    # voice = get(bot.voice_clients,guild = ctx.guild)

    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192'
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downlaoding audio now\n")
        ydl.download([url])

    # changing name of the song
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print("Renaming file : {file}\n")
            os.rename(file,"song.mp3")

    voice.play(discord.FFmpegPCMAudio(executable=r"C:\ffmpeg\bin\ffmpeg.exe" ,source="song.mp3"),after=lambda e: print(f"{name} has finished playing."))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.5

    newname = name.rsplit("-",2)
    await  ctx.send(f"Playing : {newname[0]}")
    print("playing\n")

@bot.command(pass_context = True,aliases = ['bhrata ruko','ruk'])
async def pause(ctx):
    voice = get(bot.voice_clients,guild = ctx.guild)

    if voice.is_playing():
        print("Pausing music:")
        voice.pause()
        await ctx.send("Music paused.")
    else:
        print("No music playing:")
        voice.pause()
        await ctx.send("Gana baj raha hota toh pause karta na.")

@bot.command(pass_context = True,aliases = ['res','continue'])
async def resume(ctx):
    voice = get(bot.voice_clients,guild = ctx.guild)

    if voice.is_paused():
        print("Resuming music:")
        voice.resume()
        await ctx.send("Kar diya resume.")
    else:
        print("Music is not paused.")
        await ctx.send("Goli beta masti nai.")

@bot.command(pass_context = True,aliases = ['band kar','band'])
async def stop(ctx):
    voice = get(bot.voice_clients,guild = ctx.guild)
    if voice and voice.is_playing():
        print("Music Stopped")
        voice.stop()
        await ctx.send("Shhhh....")
    else:
        print("No music playing.")
        await ctx.send("Kuch nahi baj raha.....")

@bot.command(pass_context = True,aliases = ['bol','bolo','say'])
async def tts(ctx):
    engine.say(ctx.message.content[5:])
    engine.runAndWait()

@bot.event
async def on_member_join(member):
    await member.create_dm()    #to create a direct message channel
    await member.dm_channel.send(f'Aur {member.name}, kya haal hai!')    #used that channel to .send() a direct message to that new member.
    # await member.send("Aur bhai kya haal hai")
    engine.say(f"Aur bhai {member.name}... Kiyaa haal hai? ")
    engine.runAndWait()
    #await suspends the execution of the surrounding coroutine until the execution of each coroutine has finished.
#
# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
#
#     mes = ['Lets play Ludo!','We can play monopoly','Have you played skribble?']
#
#     if 'kuch khelna hai' in message.content.lower():
#         response = random.choice(mes)
#         await message.channel.send(response)

bot.run(TOKEN)
