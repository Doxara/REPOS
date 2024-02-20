import asyncio
import glob
import os

import pafy
import discord
import yt_dlp as youtube_dl

from discord.ext import commands

intents = discord.Intents().all()  # Подключаем "Разрешения"

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix=';;',
                   description='Relatively simple music bot example',
                   intents=intents)

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

songNames = []

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': f'%(id)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
delIsSucces = False

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):

        loop = loop or asyncio.get_event_loop()
        print('начинаю скачивать дату')


        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        print('скачал дату')


        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        print('преперю файл')

        global songNames
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        print('filename =', filename)
        print('songNames =', songNames)

        songNames.append(data['title'])

        return filename


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # ----------------NEW--------------------------
        print('create song_queue')
        self.song_queue = {}
        print('calc setup')
        self.setup()
        print('OK')

    def setup(self):
        self.song_queue['guild.id'] = []
        self.song_queue['ctx.guild.id'] = []
        print(self.song_queue.keys(),self.song_queue.keys(), len(self.song_queue['ctx.guild.id']))

    async def check_queue(self, ctx):
        print('check queue')
        if len(self.song_queue['ctx.guild.id']) > 0:
            print('стоплю ctx.voice_client.stop()')
            ctx.voice_client.stop()

            global songNames
            songNames.pop(0)

            print(f'ok\nplay song - {self.song_queue["ctx.guild.id"][0][1]}')
            await self.play_song(ctx, self.song_queue['ctx.guild.id'][0][0])
            print('OK\ndelete from queue')
            self.song_queue['ctx.guild.id'].pop(0)
            print('SUCCESFULL')
        else:
            await ctx.send('Музыка кончилась.')
    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL(
            {"format": "bestaudio", "quiet": True}).extract_info(f"ytsearch{amount}:{song}", download=False,
                                                                 ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None
        global songNames
        songNames.append(info['title'])

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    # async def play(self, ctx, *, query):
    #    """Plays a file from the local filesystem"""
    #
    #    print('начинаю включать')
    #    print('тип query',type(query))
    #
    #    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))

    #    ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
    #
    #    await ctx.send('Now playing: {}'.format(query))

    #async with ctx.typing():

    # print('закачиваю с юрл')
    #        player = await YTDLSource.from_url(url, loop=self.bot.loop)
    #        print('вычисляю войс')
    #        server = ctx.message.guild
    #        voice_channel = server.voice_client
    #        print('включаю звук')
    #        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=player))

    async def play_song(self, ctx, song):
        print(f'calc url: {song}')
        url = song
        print('calc player')

        player = await YTDLSource.from_url(url, loop=self.bot.loop)

        #loop = self.bot.loop
        #data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        #if 'entries' in data:
        #    data = data['entries'][0]
        #self.songName = data['title']
        global songNames

        await ctx.send(f"Щас бацает: {self.song_queue['ctx.guild.id'][1]}")
        print('playing')
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=player)),
                              after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5



    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("*На паузе -* ⏸️")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("*Поехали! -* ▶️")

    @commands.command()
    @commands.is_owner()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def oskip(self, ctx):
        commandd = "oskip"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(" ")
        await ctx.send("Скип силой")
        ctx.voice_client.stop()
        await self.check_queue(ctx)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def join(self, ctx):
        commandd = "join"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(" ")
        if ctx.author.voice is None:
            return await ctx.send(
                "Ты не войсе, полудурок")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def leave(self, ctx):
        commandd = "leave"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(" ")
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send("А я не в войсе, чел...")

    @commands.command()
    async def play(self, ctx, *, song=None):
        commandd = "play"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(" ")
        print('SONG')
        if song is None:
            print('\tFAIL')
            return await ctx.send("Песню то напиши после play")
        print('\tOK')

        print('Voice')
        if ctx.voice_client is None:
            print('\tFAIL')
            return await ctx.send("Я в войсе должен быть, введи join")
        print('\tOK')

        print('URL')
        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            print('\t\tNO URL')
            await ctx.send("Не ссылкой получается. Ну щас найдем")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Не ну тут уже как бы мы тут здесь уже наши полномочия всё")

            song = result[0]
            print('\t\tOK')
        print('\tOK')

        print('\tSOURCE')
        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue)
            if queue_len != 0:
                queue_len = len(self.song_queue['ctx.guild.id'])

            print('voice_client.source is not None')

            print('\t\tADD SONG')
            if queue_len < 100:
                print('ctx.guild.id = ', ctx.guild.id)

                self.song_queue['ctx.guild.id'][0].append(song)
                global songNum
                songNum+=1
                print('\tOK')
                return await ctx.send(
                    f"Сейчас играет трек, поэтому добавил в очередь с номером: {queue_len + 1}.")
            else:
                print('\tFAIL')
                return await ctx.send(
                    "Какие нахуй 100 треков? Я столько держать не буду")

        print('PLAY')
        await self.play_song(ctx, song)
        print('\tOK')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def search(self, ctx, *, song=None):
        commandd = "search"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(" ")
        if song is None: return await ctx.send("Песню приложи к команде")

        await ctx.send("Щас найдем твою песенку")

        info = await self.search_song(5, song)

        embed = discord.Embed(title=f"Че нашел по этой вот теме -> '{song}':",
                              description="*Можешь отсюда ссылку брать на песню твою*\n",
                              colour=discord.Color.green())

        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"Это первые {amount} штук, что я нашел.")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def queue(self, ctx):
        commandd = "queue"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(self.song_queue, type(self.song_queue))
        print(len(self.song_queue['ctx.guild.id']))

        if len(self.song_queue['ctx.guild.id']) == 0:
            return await ctx.send("А песен тут нет.")


        embed = discord.Embed(title="ОЧЕРЕДЬ ШАРМАНКИ", description="", colour=discord.Color.green().dark_gold())
        i = 1
        print('calc embed')
        #print(type(self.song_queue), len(self.song_queue.values()), len(self.song_queue.keys()))
        for url in self.song_queue['ctx.guild.id'][0]:
            print(f'im in cicle i={i}')
            embed.description += f"{i}) {url}\n"

            i += 1
        print('end of cicle')

        embed.set_footer(text="От души, брат")
        await ctx.send(embed=embed)
        print('закончил')

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def adskip(self, ctx):
        commandd = "adskip"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(" ")
        await ctx.send("Скип какой-то шняги")
        ctx.voice_client.stop()
        await self.check_queue(ctx)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def skip(self, ctx):
        commandd = "skip"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(" ")
        if ctx.voice_client is None:
            return await ctx.send("Я молчком, чел...")

        if ctx.author.voice is None:
            return await ctx.send("Ты сам то не войсе. Зайди войс, там и поговорим")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("Нет у меня песен для тебя")

        poll = discord.Embed(title=f"ГОЛОСОВАНИЕ ЗА СКИП - {ctx.author.name}#{ctx.author.discriminator}",
                             description="**80% голосов и мы это скипнет**",
                             colour=discord.Color.blue())
        poll.add_field(name="Скип", value=":white_check_mark:")
        poll.add_field(name="Не трожь", value=":no_entry_sign:")
        poll.set_footer(text="ГОЛОСОВАНИЕ КОНЧИТСЯ ЧЕРЕЗ 5 секунд")

        poll_msg = await ctx.send(
            embed=poll)  # only returns temporary message, we need to get the cached message to get the reactions
        poll_id = poll_msg.id

        await poll_msg.add_reaction(u"\u2705")  # yes
        await poll_msg.add_reaction(u"\U0001F6AB")  # no

        await asyncio.sleep(5)  # 5 seconds to vote

        poll_msg = await ctx.channel.fetch_message(poll_id)

        votes = {u"\u2705": 0, u"\U0001F6AB": 0}
        reacted = []

        for reaction in poll_msg.reactions:
            if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                        votes[reaction.emoji] += 1

                        reacted.append(user.id)

        skip = False

        if votes[u"\u2705"] > 0:
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (
                    votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.79:  # 80% or higher
                skip = True
                embed = discord.Embed(title="Ну поехали дальше",
                                      description="***Большая часть проголосовали за скип.Скипаем ***",
                                      colour=discord.Color.green())

        if not skip:
            embed = discord.Embed(title="Ну давайте дальше слушаем",
                                  description="*Видимо все хотят продолжать слушать. Так что слушаем**",
                                  colour=discord.Color.red())

        embed.set_footer(text="КОНЧИЛОСЬ ГОЛОСОВАНИЕ")

        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice_client.stop()
            await self.check_queue(ctx)

    #----------------OLD-------------------------
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{ctx.message.author.name}, Pong')

    @commands.command()
    async def joinVoice(self, ctx):
        print('Захожу')
        channel = ctx.message.author.voice.channel
        try:
            await channel.connect()
        except Exception as err:
            await ctx.send("Не могу зайти")

    #@commands.command()
    #async def join(self, ctx, *, channel: discord.VoiceChannel):
    #    """Joins a voice channel"""
    #    print('Захожу')
    #    if channel == None:
    #        await ctx.send("Не могу зайти в войс")
    #        return
    #    if ctx.voice_client is not None:
    #        return await ctx.voice_client.move_to(channel)
#
    #    await channel.connect()
#
    #@commands.command()


    #@commands.command()
    #async def yt(self, ctx, *, url):
    #    """Plays from a url (almost anything youtube_dl supports)"""
#
    #    print('включаю YT')
    #    async with ctx.typing():
    #        print('закачиваю с юрл')
    #        player = await YTDLSource.from_url(url, loop=self.bot.loop)
    #        print('вычисляю войс')
    #        server = ctx.message.guild
    #        voice_channel = server.voice_client
    #        print('включаю звук')
    #        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=player))
#
    #    await ctx.send('Now playing: {}'.format(player.title))
#
    #@commands.command()
    #async def stream(self, ctx, *, url):
    #    """Streams from a url (same as yt, but doesn't predownload)"""

    #    async with ctx.typing():
    #        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
    #        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    #    await ctx.send('Now playing: {}'.format(player.title))

    #@commands.command()
    #async def volume(self, ctx, volume: int):
    #    """Changes the player's volume"""

    #    if ctx.voice_client is None:
    #        return await ctx.send("Not connected to a voice channel.")

    #    ctx.voice_client.source.volume = volume / 100
    #    await ctx.send("Changed volume to {}%".format(volume))

    #@commands.command()
    #async def stop(self, ctx):
    #    """Stops and disconnects the bot from voice"""
#
    #    await ctx.voice_client.disconnect()
#
    #@play.before_invoke
    #@yt.before_invoke
    #@stream.before_invoke
    #async def ensure_voice(self, ctx):
    #    if ctx.voice_client is None:
    #        if ctx.author.voice:
    #            await ctx.author.voice.channel.connect()
    #        else:
    #            await ctx.send("You are not connected to a voice channel.")
    #            raise commands.CommandError("Author not connected to a voice channel.")
    #    elif ctx.voice_client.is_playing():
    #        ctx.voice_client.stop()

iterDjo = 0

@client.event
async def on_ready():
    print('А вот и я тут')

@bot.listen()
async def on_message(ctx):
    global iterDjo
    author = ctx.message.author
    if iterDjo < 2 and ctx.message.author == 'metkiy_djo':
        if iterDjo == 0:
            await ctx.send('Да, мой повелитель')
        else:
            await ctx.send('Как скажешь, босс')
        iterDjo+=1

async def main():
    async with bot:
        await bot.add_cog(Music(bot))
        cog = bot.get_cog('Music')
        commands = cog.get_commands()

        #for it in commands:
            #print(it.name)
            #await bot.get_channel(bot.owner_id).send(it.name)


        tokenBot = 'MTEzNzM2MzU1MTcwNzcyNTg4NA.GyJhjv.dlqTbFvx7dTyy8I8Z41_3VNJCirGNYt0VbvhGo'
        print('Token create')
        await bot.start(tokenBot)
        print('bot started')




asyncio.run(main())

#tokenBot = 'MTEzNzM2MzU1MTcwNzcyNTg4NA.GyJhjv.dlqTbFvx7dTyy8I8Z41_3VNJCirGNYt0VbvhGo'
#bot.run(tokenBot)








'''
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # ----------------NEW--------------------------
        self.song_queue = {}
        self.setup()

    def setup(self):
        self.song_queue['guild.id'] = []
        self.song_queue['ctx.guild.id'] = []
        print(self.song_queue.keys(),self.song_queue.keys(), len(self.song_queue['ctx.guild.id']))

    async def check_queue(self, ctx):
        print('check queue')
        if len(self.song_queue['ctx.guild.id']) > 0:
            print('стоплю ctx.voice_client.stop()')
            ctx.voice_client.stop()

            global songNames
            songNames.pop(0)

            print(f'ok\nplay song - {self.song_queue["ctx.guild.id"][0][1]}')
            await self.play_song(ctx, self.song_queue['ctx.guild.id'][0][0])
            print('OK\ndelete from queue')
            self.song_queue['ctx.guild.id'].pop(0)
            print('SUCCESFULL')
        else:
            await ctx.send('Музыка кончилась.')
    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL(
            {"format": "bestaudio", "quiet": True}).extract_info(f"ytsearch{amount}:{song}", download=False,
                                                                 ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None
        global songNames
        songNames.append(info['title'])

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, url):

        fileName, songName = await YTDLSource.from_url(url, loop=self.bot.loop)
        print(f'получил: {songName} под названием файла {fileName}')

        await ctx.send(f"Щас бацает: {songName}")
        print('playing')
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=fileName)),
                              after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5



    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("*На паузе -* ⏸️")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("*Поехали! -* ▶️")

    @commands.command()
    @commands.is_owner()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def oskip(self, ctx):
        commandd = "oskip"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(" ")
        await ctx.send("Скип силой")
        ctx.voice_client.stop()
        await self.check_queue(ctx)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def join(self, ctx):
        commandd = "join"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")

        if ctx.author.voice is None:
            return await ctx.send(
                "Для начала в зайди в войс")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def leave(self, ctx):
        commandd = "leave"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(" ")
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send("А я не в войсе, чел...")

    @commands.command()
    async def play(self, ctx, *, song=None):
        commandd = "play"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(" ")
        print('SONG')
        if song is None:
            print('\tFAIL')
            return await ctx.send("Песню то напиши после play")
        print('\tOK')

        print('Voice')
        if ctx.voice_client is None:
            print('\tFAIL')
            return await ctx.send("Я в войсе должен быть, введи join")
        print('\tOK')

        print('URL')
        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            print('\t\tNO URL')
            await ctx.send("Не ссылкой получается. Ну щас найдем")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Не ну тут уже как бы мы тут здесь уже наши полномочия всё")

            song = result[0]
            print('\t\tOK')
        print('\tOK')

        print('\tSOURCE')
        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue)
            if queue_len != 0:
                queue_len = len(self.song_queue['ctx.guild.id'])

            print('voice_client.source is not None')

            print('\t\tADD SONG')
            if queue_len < 100:
                print('ctx.guild.id = ', ctx.guild.id)

                self.song_queue['ctx.guild.id'][0].append(song)
                global songNum
                songNum+=1
                print('\tOK')
                return await ctx.send(
                    f"Сейчас играет трек, поэтому добавил в очередь с номером: {queue_len + 1}.")
            else:
                print('\tFAIL')
                return await ctx.send(
                    "Какие нахуй 100 треков? Я столько держать не буду")

        print('PLAY')
        await self.play_song(ctx, song)
        print('\tOK')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def search(self, ctx, *, song=None):
        commandd = "search"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(" ")
        if song is None: return await ctx.send("Песню приложи к команде")

        await ctx.send("Щас найдем твою песенку")

        info = await self.search_song(5, song)

        embed = discord.Embed(title=f"Че нашел по этой вот теме -> '{song}':",
                              description="*Можешь отсюда ссылку брать на песню твою*\n",
                              colour=discord.Color.green())

        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"Это первые {amount} штук, что я нашел.")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def queue(self, ctx):
        commandd = "queue"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(self.song_queue, type(self.song_queue))
        print(len(self.song_queue['ctx.guild.id']))

        if len(self.song_queue['ctx.guild.id']) == 0:
            return await ctx.send("А песен тут нет.")


        embed = discord.Embed(title="ОЧЕРЕДЬ ШАРМАНКИ", description="", colour=discord.Color.green().dark_gold())
        i = 1
        print('calc embed')
        #print(type(self.song_queue), len(self.song_queue.values()), len(self.song_queue.keys()))
        for url in self.song_queue['ctx.guild.id'][0]:
            print(f'im in cicle i={i}')
            embed.description += f"{i}) {url}\n"

            i += 1
        print('end of cicle')

        embed.set_footer(text="От души, брат")
        await ctx.send(embed=embed)
        print('закончил')

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def adskip(self, ctx):
        commandd = "adskip"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(" ")
        await ctx.send("Скип какой-то шняги")
        ctx.voice_client.stop()
        await self.check_queue(ctx)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def skip(self, ctx):
        commandd = "skip"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(" ")
        if ctx.voice_client is None:
            return await ctx.send("Я молчком, чел...")

        if ctx.author.voice is None:
            return await ctx.send("Ты сам то не войсе. Зайди войс, там и поговорим")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("Нет у меня песен для тебя")

        poll = discord.Embed(title=f"ГОЛОСОВАНИЕ ЗА СКИП - {ctx.author.name}#{ctx.author.discriminator}",
                             description="**80% голосов и мы это скипнет**",
                             colour=discord.Color.blue())
        poll.add_field(name="Скип", value=":white_check_mark:")
        poll.add_field(name="Не трожь", value=":no_entry_sign:")
        poll.set_footer(text="ГОЛОСОВАНИЕ КОНЧИТСЯ ЧЕРЕЗ 5 секунд")

        poll_msg = await ctx.send(
            embed=poll)  # only returns temporary message, we need to get the cached message to get the reactions
        poll_id = poll_msg.id

        await poll_msg.add_reaction(u"\u2705")  # yes
        await poll_msg.add_reaction(u"\U0001F6AB")  # no

        await asyncio.sleep(5)  # 5 seconds to vote

        poll_msg = await ctx.channel.fetch_message(poll_id)

        votes = {u"\u2705": 0, u"\U0001F6AB": 0}
        reacted = []

        for reaction in poll_msg.reactions:
            if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                        votes[reaction.emoji] += 1

                        reacted.append(user.id)

        skip = False

        if votes[u"\u2705"] > 0:
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (
                    votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.79:  # 80% or higher
                skip = True
                embed = discord.Embed(title="Ну поехали дальше",
                                      description="***Большая часть проголосовали за скип.Скипаем ***",
                                      colour=discord.Color.green())

        if not skip:
            embed = discord.Embed(title="Ну давайте дальше слушаем",
                                  description="*Видимо все хотят продолжать слушать. Так что слушаем**",
                                  colour=discord.Color.red())

        embed.set_footer(text="КОНЧИЛОСЬ ГОЛОСОВАНИЕ")

        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice_client.stop()
            await self.check_queue(ctx)

    #----------------OLD-------------------------
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{ctx.message.author.name}, Pong')

    @commands.command()
    async def joinVoice(self, ctx):
        print('Захожу')
        channel = ctx.message.author.voice.channel
        try:
            await channel.connect()
        except Exception as err:
            await ctx.send("Не могу зайти")

async def main():
    async with bot:
        await bot.add_cog(Music(bot))

        tokenBot = 'MTEzNzM2MzU1MTcwNzcyNTg4NA.GyJhjv.dlqTbFvx7dTyy8I8Z41_3VNJCirGNYt0VbvhGo'
        print('Token create')
        print('bot started')
        await bot.start(tokenBot)


asyncio.run(main())


'''