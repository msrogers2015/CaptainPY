import discord
from discord.ext import commands

class basic(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self, ctx):
        print(f'We have logged in as {self.client.user}')       
    

def setup(client):
    client.add_cog(basic(client))
