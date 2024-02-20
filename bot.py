import discord
from discord.ext import commands

import audio_utils
import config

intents = discord.Intents.all()
intents.messages = True  
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)
songs_queue = {}

@bot.event
async def on_ready():
    print('Bot is ready')

@bot.command()
async def hello(ctx):
    if ctx.author.name == 'domestos228':
        await ctx.send('привет, хуесос ебучий {}'.format(ctx.author.display_name))
    else:
        await ctx.send('привет, {}'.format(ctx.author.display_name))


@bot.command()
async def play(ctx, url=None):
    if ctx.voice_client is None:
        channel = ctx.author.voice.channel
        await channel.connect()
    elif not ctx.voice_client.is_playing() and ctx.voice_client.is_paused() and url is None:
        ctx.voice_client.resume()
        await ctx.send("Аудио воспроизводится снова.")
        return

    if url is None:
        if ctx.voice_client.is_playing():
            await ctx.send("Укажите URL трека или используйте команду !pause, чтобы поставить текущий трек на паузу.")
        else:
            await ctx.send("Нет активного аудио для воспроизведения. Укажите URL трека.")
    else:
        if ctx.guild.id not in songs_queue:
            songs_queue[ctx.guild.id] = []

        if ctx.voice_client.is_playing():
            songs_queue[ctx.guild.id].append(url)
            await ctx.send(f'Трек добавлен в очередь: {url}')
        else:
            await play_audio(ctx, url)

async def play_next(ctx):
    if len(songs_queue[ctx.guild.id]) > 0:
        url = songs_queue[ctx.guild.id].pop(0)
        await play_audio(ctx, url)

async def play_audio(ctx, url):
    if ctx.voice_client is None:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()
    else:
        voice_client = ctx.voice_client

    if not voice_client.is_playing():
        title, audio_stream_url = await audio_utils.get_audio_info(url)
        if audio_stream_url is not None:
            audio_source = discord.FFmpegOpusAudio(audio_stream_url)
            voice_client.play(audio_source, after=lambda e: bot.loop.create_task(play_next(ctx)))
            await ctx.send(f'Сейчас играет : {title}')
        else:
            await ctx.send('Не удалось получить трек')

@bot.command()
async def pause(ctx):
    if ctx.voice_client is None or not ctx.voice_client.is_playing():
        await ctx.send("На данный момент нет активного аудио для постановки на паузу.")
    elif ctx.voice_client.is_paused():
        await ctx.send("Аудио уже на паузе.")
    else:
        ctx.voice_client.pause()
        await ctx.send("Аудио поставлено на паузу.")

@bot.command()
async def skip(ctx):
    if ctx.voice_client is None:
        await ctx.send("Бот не находится в голосовом канале.")
        return
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Воспроизведение остановлено.")
    else:
        await ctx.send("Нет активного аудио для пропуска.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client is None:
        await ctx.send("Бот не находится в голосовом канале.")
        return

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    songs_queue[ctx.guild.id] = []  # Очистка очереди
    await ctx.send("Воспроизведение остановлено, и очередь очищена.")

@bot.command()
async def queue(ctx):
    if ctx.guild.id not in songs_queue or not songs_queue[ctx.guild.id]:
        await ctx.send("Очередь пуста.")
    else:
        queue_list = []
        for url in songs_queue[ctx.guild.id]:
            title, _ = await audio_utils.get_audio_info(url)
            queue_list.append(title)
        queue_info = "\n".join(queue_list)
        await ctx.send(f"Очередь:\n{queue_info}")

bot.run(config.TOKEN)