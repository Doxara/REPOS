import asyncio
import yt_dlp as youtube_dl

import discord  # Подключаем библиотеку
from discord.ext import commands, tasks

from dotenv import load_dotenv
import os
import random

load_dotenv()

intents = discord.Intents().all()  # Подключаем "Разрешения"
client = discord.Client(intents=intents)
# Задаём префикс и интенты
bot = commands.Bot(command_prefix=';;', intents=intents)

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'song.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
        self.songName = ''

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        global ytdl
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        print('data[title]:', data['title'])
        print(type(data))
        print(list(data.keys()))
        cls.songName = data['title']
        for (dirpath, dirnames, filenames) in os.walk(os.curdir):
            print(filenames)
            break
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        print(type(filename), filename)
        return filename


# @bot.command()
# async def rand(ctx, *arg):
#    await ctx.reply(random.randint(0, 100))
#

# С помощью декоратора создаём первую команду
@bot.command()
async def ping(ctx):
    await ctx.send('pong')


isPlaying = False


@bot.command(help='Бот зайдет к тебе в гс')
async def joinVoice(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{}, ты не в войсе, чел.".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        try:
            await channel.connect()
        except Exception as err:
            print(err)
            if (err == 'Already connected to a voice channel.'):
                await ctx.send("Уже в войсе, чел...")


@bot.command(help='Отпустить бота домой')
async def leaveVoice(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("Бот не в войсе, чел.")


def next_song(ctx):
    ctx.send("Закончил петь.")


@bot.command(help='Включить музыку')
async def playYT(ctx, url):
    if (url == None):
        return
    global isPlaying

    if ctx.message.author.voice:
        channel = ctx.message.author.voice.channel
        try:
            await channel.connect()
        except Exception as err:
            print(err)

    voice_client = ctx.message.guild.voice_client
    print(voice_client)
    # if not voice_client.is_connected():
    #    channel = ctx.message.author.voice.channel
    #    await channel.connect()

    if voice_client.is_playing():
        await ctx.send('Бот уже проигрывает музыку чел')
    else:
        isPlaying = True
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client
            async with ctx.typing():
                filename = await YTDLSource.from_url(url, loop=bot.loop)
                #print(filename)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
                # voice_channel.play(discord.FFmpegPCMAudio(source=filename))

            await ctx.send('**Щас играет:** {}'.format(YTDLSource.songName))
        except Exception as err:
            print(err)

            print(err.args)
            if (err == 'Already playing audio.'):
                await ctx.send("Музыка уже играет!")
            else:
                await ctx.send("Какая-то ошибка, чувак.")
    isPlaying = False


@bot.command(name='pauseYT', help='Это остановить песню')
async def pauseYT(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("Бот молчит как рыба, чел...")


@bot.command(name='resumeYT', help='Возобновить трек')
async def resumeYT(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("Бот молчит как рыба, чел... Введи playYT чтобы он начал играть")


@bot.command(name='stopYT', help='Остановочка песни')
async def stopYT(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("Бот молчит и ничего не играет, нуууу")


# hiWithMe = False
# iterA = 0
#
# @bot.event
# async def on_message(ctx):
#    global iterA, isPlaying, hiWithMe
#    channel = ctx.channel
#
#    #voicechannel = ctx.author.voice
#
#    if (iterA < 2 and ctx.author != bot.user):
#        print(ctx.author.name)
#        if(ctx.author.name == 'metkiy_djo'):
#            if (not hiWithMe):
#                await channel.send('Приветствую тебя, мой господин')
#                hiWithMe = True
#        else:
#            await channel.send('Привет, левый чел')
#        iterA+=1

iterDjo = 0



tokenBot = 'MTEzNzM2MzU1MTcwNzcyNTg4NA.GyJhjv.dlqTbFvx7dTyy8I8Z41_3VNJCirGNYt0VbvhGo'
print('Run Bot')
bot.run(tokenBot)
print('End of program')
