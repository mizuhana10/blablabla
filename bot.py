# bot.py

import discord
from discord.ext import commands

import config
import music_downloader
import music_player
import queue_manager  

intents = discord.Intents.all()
intents.messages = True  
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)
queue = {}
queue_list = {}

@bot.command()
async def play(ctx, url: str):
    await music_player.play(bot, ctx, url, queue, queue_list, music_downloader)

@bot.command()
async def list(ctx):
    await queue_manager.list_queue(ctx, queue_list)

@bot.command()
async def skip(ctx):
    await music_player.skip(ctx)

bot.run(config.TOKEN)
