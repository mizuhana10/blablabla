import os
import discord
import asyncio

async def play(bot, ctx, url, queue, queue_list, music_downloader):
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        temp_music_folder = 'temp_music'  # Путь к временной папке
        try:
            filename, title = music_downloader.download_music(url, temp_music_folder)
            queue[ctx.guild.id] = queue.get(ctx.guild.id, []) + [filename]
            queue_list[ctx.guild.id] = queue_list.get(ctx.guild.id, []) + [title]

            if ctx.guild.id not in queue:
                queue[ctx.guild.id] = []

            if ctx.voice_client is None:
                vc = await voice_channel.connect()
            else:
                vc = ctx.voice_client

            if not vc.is_playing():
                await play_song(bot, vc, ctx.guild.id, queue, queue_list)  # Исправление здесь
            else:
                await ctx.send("Трек добавлен в очередь.")
        except RuntimeError as e:
            await ctx.send(str(e))
    else:
        await ctx.send("Вы должны находиться в голосовом канале, чтобы воспроизводить музыку.")

async def play_song(bot, vc, guild_id, queue, queue_list):
    if queue[guild_id]:
        filename = queue[guild_id].pop(0)
        vc.play(discord.FFmpegPCMAudio(filename), after=lambda e: on_finish(bot, vc, guild_id, filename, queue, queue_list))
        queue_list[guild_id].pop(0)
    else:
        await asyncio.sleep(600)  # Ожидаем 10 минут (600 секунд)
        await vc.disconnect()

async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        vc = ctx.voice_client
        vc.stop()
    else:
        raise RuntimeError("Сейчас ничего не играет.")

def on_finish(bot, vc, guild_id, filename, queue, queue_list):
    os.remove(filename)
    bot.loop.create_task(play_song(bot, vc, guild_id, queue, queue_list))
