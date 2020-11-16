import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix = '/')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    print("Bot is online.")

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename != "voice_v1.py":
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

client.run('NzY4OTYwMTM2NDMzMzY5MDg4.X5ID7w.fr7X08Nq_8JHXEsubZCkWXejCh0')
