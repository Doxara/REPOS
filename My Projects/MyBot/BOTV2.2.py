import asyncio
import os
import glob
import time

import discord
import yt_dlp as youtube_dl
from discord import ClientException
import discord.opus

from discord.ext import commands

white_list_of_IDs = [320093583237578762, 1125097962951954452, 1140202779789492345]

intents = discord.Intents().all()  # Подключаем "Разрешения"

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix=';;',
                   description='Relatively simple music bot example',
                   intents=intents)

# Suppress noise about console usage from errors
# youtube_dl.utils.bug_reports_message = lambda: ''
# discord.opus.load_opus('opus')

songNames = []

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': f'%(id)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': True,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):

        loop = loop or asyncio.get_event_loop()
        if (not stream):
            print('начинаю скачивать дату')
        else:
            print('беру данные без скачки')
        try:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
            print('скачал дату')
        except Exception as err:
            print("ERROR on from url:", err)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        print(data.keys())

        print('преперю файл')
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        print('filename =', os.curdir + '/' + filename)
        print('songNames =', songNames)

        # возвращаю название файла и видео
        return os.curdir + '/' + filename, data['title'], data['duration']


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}
        self.setup()
        self.ctx = None

    def setup(self):

        self.song_queue[0]={}
        self.song_queue[0]['songs'] = []
        self.song_queue[0]['songs'].append({})

        print(self.song_queue.keys(), self.song_queue.values(), len(self.song_queue[0]['songs']))
        print('song_queue: ', self.song_queue)

    async def check_queue(self, ctx, mes, er):
        if (mes == 'afterPlay'):
            print('err=', er)
        print('check queue')
        print(mes)
        songsInQueue = len(self.song_queue[ctx.guild.id]["songs"])
        print(f'кол-во песен в очереди: {songsInQueue}')
        if songsInQueue > 0: print('url in self.song_queue[songs][0] - ', "url" in self.song_queue[ctx.guild.id]['songs'][0])
        if songsInQueue > 0 and 'url' in self.song_queue[ctx.guild.id]['songs'][0]:
            print('стоплю ctx.voice_client.stop()')
            if mes == 'afterPlay':
                await self.play_song(ctx, self.song_queue[ctx.guild.id]['songs'][0]['url'])
            else:
                ctx.voice_client.stop()
                return

            print('delete from queue')
            print('queue:', self.song_queue[ctx.guild.id]['songs'])
            if len(self.song_queue[ctx.guild.id]['songs']) != 0:
                self.song_queue[ctx.guild.id]['songs'].pop(0)
            print('queue after del:', self.song_queue[ctx.guild.id]['songs'])
            print('SUCCESFULL')
        else:
            files_for_del = []
            all_formats = ['webm', 'mp3', '3gp', 'aac', 'flv', 'm4a', 'mp4', 'ogg', 'wav']
            for format_of_file in all_formats:
                finded_paths = glob.glob(f'*.{format_of_file}')
                files_for_del += finded_paths
            try:
                for file_to_del in files_for_del:
                    os.remove(file_to_del)
            except Exception as err:
                print('os except: ', err)

            await ctx.send('Музыка кончилась.')

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL(
            {"format": "bestaudio", "quiet": True}).extract_info(f"ytsearch{amount}:{song}", download=False,
                                                                 ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None
        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    def after_play(self, error):

        print('After play отработал')
        if error is not None:
            print('Error in after play: ', error)
        self.bot.loop.create_task(self.check_queue(self.ctx, 'afterPlay', error))

    async def play_song(self, ctx, url):
        if not ctx.guild.id in self.song_queue:
            self.song_queue[ctx.guild.id]={}
            self.song_queue[ctx.guild.id]['songs'] = [{}]



        async with ctx.typing():
            fileName, songName, dur = await YTDLSource.from_url(url, loop=self.bot.loop)

        print(f'получил: {songName} под названием файла {fileName}')
        print('очередь: ', self.song_queue[ctx.guild.id]['songs'])
        print('длина ее из play_song = ', len(self.song_queue[ctx.guild.id]['songs']))

        songDur = time.strftime("%H:%M:%S", time.gmtime(dur))
        await ctx.send(f"Сейчас играет: {songName}\nДлительность: {songDur}")

        print('playing')
        print('Текущий каталог - ', os.curdir)

        # audio = discord.FFmpegAudio(executable="ffmpeg", source=fileName)
        audio = discord.FFmpegOpusAudio(executable="ffmpeg", source=fileName)

        # audio = discord.FFmpegPCMAudio(executable="ffmpeg", source=fileName)
        print('FFmpegPCMAudio - OK')
        audio_trans = audio
        # audio_trans = discord.PCMVolumeTransformer(audio)
        print('PCMVolumeTransformer - OK')

        # await ctx.voice_client.play(source=audio_trans,
        #                            after=lambda error: self.bot.loop.create_task(
        #                                self.check_queue(ctx, 'afterPlay', error)))
        # await discord.VoiceClient.play(ctx.voice_client, source=audio_trans,
        #                         after=lambda error: self.bot.loop.create_task(
        #                             self.check_queue(ctx, 'afterPlay', error)))
        # print('voice_client.play - OK')
        # ctx.voice_client.source.volume = 0.5
        # print('voice_client.source.volume - OK')
        try:
            # discord.VoiceClient.play(ctx.voice_client, source=audio_trans,
            #                         after=lambda error: self.bot.loop.create_task(
            #                             self.check_queue(ctx, 'afterPlay', error)))

            print('audio_trans is opus - ', audio_trans.is_opus())
            print('audio_trans - ', audio_trans.__str__())
            print('audio_trans size of ', audio_trans.__sizeof__())

            # ctx.voice_client.play(source=audio)
            ctx.voice_client.play(source=audio_trans,
                                  after=lambda error: self.bot.loop.create_task(
                                      self.check_queue(ctx, 'afterPlay', error)))

            # self.ctx = ctx
            # ctx.voice_client.play(audio_trans,
            #                      after=self.after_play)

            print('voice_client.play - OK')
            ctx.voice_client.source.volume = 0.5
            print('voice_client.source.volume - OK')
        except ClientException as err:
            print("ClientException:", err)
        except TypeError as err:
            print('TypeError = ', err)
            print('TypeError args = ', err.args)
        except discord.OpusNotLoaded as err:
            print('OpusNotLoaded = ', err)
            print('OpusNotLoaded args = ', err.args)
        except Exception as err:
            print('хз че стало ваще ', err)

        print('play_song is over')

    @commands.command()
    async def delFiles(self, ctx):
        global white_list_of_IDs
        if not ctx.guild.id in white_list_of_IDs:
            return await ctx.send("Извини, я не работаю на вашем сервере")
        commandd = "delete"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")

        if ctx.voice_client == None or not ctx.voice_client.is_playing():
            print('начинаю удалять файлы')
            files_for_del = []
            all_formats = ['webm', 'mp3', '3gp', 'aac', 'flv', 'm4a', 'mp4', 'ogg', 'wav']
            for format_of_file in all_formats:
                finded_paths = glob.glob(f'*.{format_of_file}')
                files_for_del += finded_paths
            print(f'Буду удалять {len(files_for_del)} файлов')
            try:
                for file_to_del in files_for_del:
                    os.remove(file_to_del)
                print('удалил файлы')
            except Exception as err:
                print('os except: ', err)
        else:
            print('Не могу удалять файлы. На данный момент они используются')
            await ctx.send('Не могу удалять файлы. На данный момент они используются')
        print('Закончил удаление')

    @commands.command()
    @commands.is_owner()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def oskip(self, ctx):
        global white_list_of_IDs
        if not ctx.guild.id in white_list_of_IDs:
            return await ctx.send("Извини, я не работаю на вашем сервере")

        commandd = "oskip"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")

        await ctx.send("Скип силой")
        ctx.voice_client.stop()
        await self.check_queue(ctx, 'oskip')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def join(self, ctx):
        global white_list_of_IDs
        if not ctx.guild.id in white_list_of_IDs:
            return await ctx.send("Извини, я не работаю на вашем сервере")
        print(f'GUILD id = {ctx.guild.id}')

        commandd = "join"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")

        if ctx.author.voice is None:
            return await ctx.send(
                "Для начала в зайди в войс")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        try:
            await ctx.author.voice.channel.connect()
        except Exception as err:
            print(err)

    @commands.command()
    async def play(self, ctx, *, song=None):
        global white_list_of_IDs
        if not ctx.guild.id in white_list_of_IDs:
            return await ctx.send("Извини, я не работаю на вашем сервере")
        commandd = "play"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(" ")

        print('check song')
        if song is None:
            print('\tFAIL')
            return await ctx.send("Песню то напиши после play")
        print('\tOK')

        print('Voice check')
        if ctx.voice_client is None:
            print('\tFAIL')
            return await ctx.send("Я в войсе должен быть, введи join")
        print('\tOK')

        print('check is URL')
        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            print('\t\tNO URL')
            await ctx.send("Начинаю поиск")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Не ну тут уже как бы мы тут здесь уже наши полномочия всё")

            song = result[0]
            print('\t\tfind OK')
        print('\tsong is OK')

        # take title song
        _, songName, songLength = await YTDLSource.from_url(song, stream=True)

        print('пытался получить название песни')

        print('\tcheck SOURCE')
        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id]['songs'])
            print('in play len(queue) = ', queue_len)

            print('voice_client.source is not None')

            print('\t\tADD SONG')
            if queue_len < 100:
                if queue_len == 1:
                    print(f'song_queue = {self.song_queue[ctx.guild.id]}')
                    print(f'добавил {song}')
                    if 'url' in self.song_queue[ctx.guild.id]['songs'][0]:
                        temp_dict = {}
                        temp_dict['url'] = song
                        temp_dict['name'] = songName
                        temp_dict['songLength'] = songLength
                        self.song_queue[ctx.guild.id]['songs'].append(temp_dict)
                        print(f'song_queue = {self.song_queue[ctx.guild.id]}')
                        return await ctx.send(
                            f"Сейчас играет трек, поэтому добавил {songName} в очередь с номером: {queue_len + 1}.")
                    else:
                        self.song_queue[ctx.guild.id]['songs'][0]['url'] = song
                        self.song_queue[ctx.guild.id]['songs'][0]['name'] = songName
                        self.song_queue[ctx.guild.id]['songs'][0]['songLength'] = songLength
                        print(f'song_queue = {self.song_queue[ctx.guild.id]}')
                        return await ctx.send(
                            f"Сейчас играет трек, поэтому добавил {songName} в очередь с номером: {queue_len}.")
                else:
                    print(f'song_queue = {self.song_queue[ctx.guild.id]}')
                    print(f'добавил {song}')
                    temp_dict = {}
                    temp_dict['url'] = song
                    temp_dict['name'] = songName
                    temp_dict['songLength'] = songLength
                    print('создал темп дикт = ', temp_dict)
                    self.song_queue[ctx.guild.id]['songs'].append(temp_dict)
                    print(f'song_queue = {self.song_queue[ctx.guild.id]}')
                    return await ctx.send(
                        f"Сейчас играет трек, поэтому добавил {songName} в очередь с номером: {queue_len + 1}.")
                print('\tOK')
            else:
                print('\tFAIL')
                return await ctx.send(
                    "Какие нахуй 100 треков? Я столько держать не буду")

        print('вызвал play_song')
        await self.play_song(ctx, song)

    @commands.command()
    async def queue(self, ctx):
        global white_list_of_IDs
        if not ctx.guild.id in white_list_of_IDs:
            return await ctx.send("Извини, я не работаю на вашем сервере")

        commandd = "queue"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(self.song_queue, type(self.song_queue))
        print(len(self.song_queue[ctx.guild.id]['songs']))

        if len(self.song_queue[ctx.guild.id]['songs']) == 1:
            if not 'name' in self.song_queue[ctx.guild.id]['songs'][0]:
                return await ctx.send("А песен тут нет.")

        timeSum = 0
        for it in self.song_queue[ctx.guild.id]['songs']:
            timeSum += it['songLength']

        queueDur = time.strftime("%H:%M:%S", time.gmtime(timeSum))

        embed = discord.Embed(title="ОЧЕРЕДЬ ШАРМАНКИ", description="", colour=discord.Color.green().dark_gold())
        i = 1
        print('calc embed')
        # print(type(self.song_queue), len(self.song_queue.values()), len(self.song_queue.keys()))

        if len(self.song_queue[ctx.guild.id]['songs']) < 10:
            print('начал перебор ', self.song_queue[ctx.guild.id]['songs'])
            if len(self.song_queue[ctx.guild.id]['songs']) == 1 and not 'url' in self.song_queue[ctx.guild.id]['songs'][0] or len(
                    self.song_queue[ctx.guild.id]['songs']) == 0:
                embed.description += 'Очередь пустая'
                embed.set_footer(text="Можешь добавить песни с помощью команды play")
            else:
                for name in self.song_queue[ctx.guild.id]['songs']:
                    print(f'im in cicle i={i}')
                    durSong = time.strftime("%H:%M:%S", time.gmtime(name['songLength']))
                    embed.description += f"{i}) {name['name']}  [{durSong}]\n"
                    i += 1
                print('end of cicle')
                embed.set_footer(text=f"Длительность: {queueDur}")
        else:
            for name in self.song_queue[ctx.guild.id]['songs']:
                print(f'im in cicle i={i}')
                embed.description += f"{i}) {name['name']}\n"
                i += 1
                if i == 10:
                    break
            div = (len(self.song_queue[ctx.guild.id]['songs']) - 9) % 10
            if div == 1:
                embed.set_footer(text=f"...еще {div} песня")
            if 1 < div < 5:
                embed.set_footer(text=f"...еще {div} песни")
            if div > 4 or div == 0:
                embed.set_footer(text=f"...еще {div} песен")

            print('end of cicle')
        await ctx.send(embed=embed)
        print('закончил')

    @commands.command()
    async def pause(self, ctx):
        global white_list_of_IDs
        if not ctx.guild.id in white_list_of_IDs:
            return await ctx.send("Извини, я не работаю на вашем сервере")
        ctx.voice_client.pause()
        await ctx.send("*На паузе -* ⏸️")

    @commands.command()
    @commands.is_owner()
    async def stop(self, ctx):
        global white_list_of_IDs
        if not ctx.guild.id in white_list_of_IDs:
            return await ctx.send("Извини, я не работаю на вашем сервере")
        self.song_queue[ctx.guild.id]['songs'] = []
        ctx.voice_client.stop()
        await ctx.send("Всё остановил")

    @commands.command()
    async def resume(self, ctx):
        global white_list_of_IDs
        if not ctx.guild.id in white_list_of_IDs:
            return await ctx.send("Извини, я не работаю на вашем сервере")
        ctx.voice_client.resume()
        await ctx.send("*Поехали! -* ▶️")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def leave(self, ctx):
        global white_list_of_IDs
        if not ctx.guild.id in white_list_of_IDs:
            return await ctx.send("Извини, я не работаю на вашем сервере")
        commandd = "leave"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(" ")
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send("А я не в войсе, чел...")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def search(self, ctx, *, song=None):
        global white_list_of_IDs
        if not ctx.guild.id in white_list_of_IDs:
            return await ctx.send("Извини, я не работаю на вашем сервере")
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
    async def skip(self, ctx):
        global white_list_of_IDs
        if not ctx.guild.id in white_list_of_IDs:
            return await ctx.send("Извини, я не работаю на вашем сервере")
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
                             description="**80% голосов и мы это скипнем**",
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


async def main():
    async with bot:
        await bot.add_cog(Music(bot))

        tokenBot = 'MTEzNzM2MzU1MTcwNzcyNTg4NA.GjNMBv.uUPSdOd2wrQ6Jc7IivdoJeD8A7bpziAslP8U3U'
        print('Token create')
        print('bot started')
        await bot.start(tokenBot)

asyncio.run(main())
