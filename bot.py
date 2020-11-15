import discord
import os
from discord.ext import commands
from dotenv import load_dotenv


# Load a env file that contains the discord bot's token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Variables
active_cogs = []
all_cogs = []
inactive_cogs = []
color = 0x5E8AB4
client = commands.Bot(command_prefix="=")


# Load all cogs when starting bot
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        active_cogs.append(filename[:-3])
        all_cogs.append(filename[:-3])
print(all_cogs)



# Command to activate a cog
@client.command()
async def activate(ctx, extension):
    if(extension not in active_cogs):
        client.load_extension(f'cogs.{extension}')
        embed = discord.Embed(title='I have the power!',description=f'{extension} has been activated.', color=color)
        await ctx.send(embed=embed)
        active_cogs.append(extension)
        inactive_cogs.remove(extension)
    else:
        embed = discord.Embed(title='Uh-oh',description=f'{extension} is already active.', color=color)
        await ctx.send(embed=embed)



# Command to activate a cog
@client.command()
async def deactivate(ctx, extension):
    if(extension in active_cogs):
        client.unload_extension(f'cogs.{extension}')
        embed = discord.Embed(title='I feel weak...',description=f'{extension} has been deactivated.', color=color)
        await ctx.send(embed=embed)
        inactive_cogs.append(extension)
        active_cogs.remove(extension)
    else:
        embed = discord.Embed(title='Uh-oh',description=f'{extension} is already deactivated.', color=color)
        await ctx.send(embed=embed)


@client.command()
async def listcogs(ctx):
    embed = discord.Embed(title="Cogs")
    for cog in all_cogs:
        embed.add_field(name=cog, value='\u200b', inline=True)
    return await ctx.send(embed=embed)


@client.command()
async def refresh(ctx, extension):
    if(extension in active_cogs):
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} has been refreshed.')
    else:
        await ctx.send(f'{extension} is not currently active.')


client.run(TOKEN)