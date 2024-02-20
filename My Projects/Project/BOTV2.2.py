import asyncio
import os
import glob

import discord
import yt_dlp as youtube_dl

from discord.ext import commands

white_list_of_IDs = [320093583237578762]

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
    'logtostderr': True,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
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

        print('преперю файл')
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        print('filename =', filename)
        print('songNames =', songNames)

        #возвращаю название файла и видео
        return filename, data['title']

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}
        self.setup()

    def setup(self):
        self.song_queue['songs'] = []
        self.song_queue['songs'].append({})

        print(self.song_queue.keys(),self.song_queue.values(), len(self.song_queue['songs']))
        print('song_queue: ', self.song_queue)

    async def check_queue(self, ctx,mes):
        print('check queue')
        print(mes)
        if len(self.song_queue['songs']) > 0:

            print('стоплю ctx.voice_client.stop()')
            if mes == 'afterPlay':
                await self.play_song(ctx, self.song_queue['songs'][0]['url'])
            else:
                ctx.voice_client.stop()
                return

            print('delete from queue')
            print('queue:', self.song_queue['songs'])
            if len(self.song_queue['songs']) != 0:
                self.song_queue['songs'].pop(0)
            print('queue after del:', self.song_queue['songs'])
            print('SUCCESFULL')
        else:
            files_for_del = []
            all_formats = ['webm', 'mp3', '3gp', 'aac', 'flv', 'm4a', 'mp4', 'ogg', 'wav']
            for format_of_file in all_formats:
                finded_paths = glob.glob(f'*.{format_of_file}')
                files_for_del += finded_paths
            for file_to_del in files_for_del:
                os.remove(file_to_del)

            await ctx.send('Музыка кончилась.')

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL(
            {"format": "bestaudio", "quiet": True}).extract_info(f"ytsearch{amount}:{song}", download=False,
                                                                 ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None
        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, url):
        fileName, songName = await YTDLSource.from_url(url, loop=self.bot.loop)
        print(f'получил: {songName} под названием файла {fileName}')
        print('очередь: ',self.song_queue['songs'])
        print('длина ее из play_song = ', len(self.song_queue['songs']))

        await ctx.send(f"Сейчас играет: {songName}")

        print('playing')
        print('Текущий каталог - ',os.curdir)
        try:
            ctx.voice_client.play(
                discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=fileName)),
                after=lambda error: self.bot.loop.create_task(self.check_queue(ctx, 'afterPlay')))
            ctx.voice_client.source.volume = 0.5
        except OSError as err:
            print("OS error:", err)
        except Exception as err:
            print('ERROR = ', err)
            print('ERROR args = ', err.args)

    @commands.command()
    @commands.is_owner()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def oskip(self, ctx):
        global white_list_of_IDs
        if ctx.guild.id != white_list_of_IDs[0]:
            return await ctx.send("Извини, я не работаю на вашем сервере")

        if discord.Guild.id != 1:
            pass
        commandd = "oskip"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")

        await ctx.send("Скип силой")
        ctx.voice_client.stop()
        await self.check_queue(ctx, 'oskip')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def join(self, ctx):
        global white_list_of_IDs
        if ctx.guild.id != white_list_of_IDs[0]:
            return await ctx.send("Извини, я не работаю на вашем сервере")
        print(f'GUILD id = {ctx.guild.id}')

        commandd = "join"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")

        if ctx.author.voice is None:
            return await ctx.send(
                "Для начала в зайди в войс")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    @commands.command()
    async def play(self, ctx, *, song=None):
        global white_list_of_IDs
        if ctx.guild.id != white_list_of_IDs[0]:
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

        #take title song
        _, songName = await YTDLSource.from_url(song,stream=True)
        print('пытался получить название песни')


        print('\tcheck SOURCE')
        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue['songs'])
            print('in play len(queue) = ', queue_len)

            print('voice_client.source is not None')

            print('\t\tADD SONG')
            if queue_len < 100:
                if queue_len == 1:
                    print(f'song_queue = {self.song_queue}')
                    print(f'добавил {song}')
                    if 'url' in self.song_queue['songs'][0]:
                        temp_dict = {}
                        temp_dict['url'] = song
                        temp_dict['name'] = songName
                        self.song_queue['songs'].append(temp_dict)
                        print(f'song_queue = {self.song_queue}')
                        return await ctx.send(
                            f"Сейчас играет трек, поэтому добавил {songName} в очередь с номером: {queue_len+1}.")
                    else:
                        self.song_queue['songs'][0]['url'] = song
                        self.song_queue['songs'][0]['name'] = songName
                        print(f'song_queue = {self.song_queue}')
                        return await ctx.send(
                            f"Сейчас играет трек, поэтому добавил {songName} в очередь с номером: {queue_len}.")
                else:
                    print(f'song_queue = {self.song_queue}')
                    print(f'добавил {song}')
                    temp_dict = {}
                    temp_dict['url'] = song
                    temp_dict['name'] = songName
                    print('создал темп дикт = ', temp_dict)
                    self.song_queue['songs'].append(temp_dict)
                    print(f'song_queue = {self.song_queue}')
                    return await ctx.send(
                        f"Сейчас играет трек, поэтому добавил {songName} в очередь с номером: {queue_len+1}.")
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
        if ctx.guild.id != white_list_of_IDs[0]:
            return await ctx.send("Извини, я не работаю на вашем сервере")

        commandd = "queue"
        print(f"{ctx.author.name}, {ctx.author.id} used command " + commandd + " used at ")
        print(self.song_queue, type(self.song_queue))
        print(len(self.song_queue['songs']))

        if len(self.song_queue['songs']) == 1:
            if not 'name' in self.song_queue['songs'][0]:
                return await ctx.send("А песен тут нет.")

        embed = discord.Embed(title="ОЧЕРЕДЬ ШАРМАНКИ", description="", colour=discord.Color.green().dark_gold())
        i = 1
        print('calc embed')
        # print(type(self.song_queue), len(self.song_queue.values()), len(self.song_queue.keys()))


        if len(self.song_queue['songs']) < 10:
            print('начал перебор ', self.song_queue['songs'])
            if len(self.song_queue['songs']) == 1 and not 'url' in self.song_queue['songs'][0] or len(self.song_queue['songs']) == 0:
                embed.description += 'Очередь пустая'
                embed.set_footer(text="Можешь добавить песни с помощью команды play")
            else:
                for name in self.song_queue['songs']:
                    print(f'im in cicle i={i}')
                    embed.description += f"{i}) {name['name']}\n"
                    i += 1
                print('end of cicle')
                embed.set_footer(text="Конец списка")
        else:
            for name in self.song_queue['songs']:
                print(f'im in cicle i={i}')
                embed.description += f"{i}) {name['name']}\n"
                i += 1
                if i == 10:
                    break
            div = (len(self.song_queue['songs'])-9) % 10
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
        if ctx.guild.id != white_list_of_IDs[0]:
            return await ctx.send("Извини, я не работаю на вашем сервере")
        ctx.voice_client.pause()
        await ctx.send("*На паузе -* ⏸️")

    @commands.command()
    @commands.is_owner()
    async def stop(self, ctx):
        global white_list_of_IDs
        if ctx.guild.id != white_list_of_IDs[0]:
            return await ctx.send("Извини, я не работаю на вашем сервере")
        self.song_queue['songs'] = []
        ctx.voice_client.stop()
        await ctx.send("Всё остановил")

    @commands.command()
    async def resume(self, ctx):
        global white_list_of_IDs
        if ctx.guild.id != white_list_of_IDs[0]:
            return await ctx.send("Извини, я не работаю на вашем сервере")
        ctx.voice_client.resume()
        await ctx.send("*Поехали! -* ▶️")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def leave(self, ctx):
        global white_list_of_IDs
        if ctx.guild.id != white_list_of_IDs[0]:
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
        if ctx.guild.id != white_list_of_IDs[0]:
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
        if ctx.guild.id != white_list_of_IDs[0]:
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

        tokenBot = 'MTEzNzM2MzU1MTcwNzcyNTg4NA.GyJhjv.dlqTbFvx7dTyy8I8Z41_3VNJCirGNYt0VbvhGo'
        print('Token create')
        print('bot started')
        await bot.start(tokenBot)

asyncio.run(main())
