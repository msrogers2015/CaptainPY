import discord
from discord.ext import commands

# Variables
color = 0x5E8AB4

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Ban Commands
    @commands.command(help='Bans the member specified listing any reasons given')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason = reason)
        embed = discord.Embed(title='Ban hammer delivered!',description=f'User {member} has been banned for {reason}.', color=color)
        await ctx.send(embed=embed)
        

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        
        member_name, member_discriminator = member.split('#')
        found_member = False
        for ban_entry in banned_users:
            user = ban_entry.user
            
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(title='Maybe we were too harsh...',description=f'Unbanned: {user.mention}.', color=color)
                await ctx.send(embed=embed)
                found_member = True
            
        if found_member == False:
            await ctx.send(f'{member_name} isn\'t banned.')
            found_member = True


    #Kick Member
    @commands.command(help="Kicks the member specified listing any reasons given")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason = reason)
        embed = discord.Embed(title='Get \'em outta hereya',description=f'User {member} has been given the boot.', color=color)
        await ctx.send(embed=embed)



    # Purge Messages
    @commands.command(help='Delete specified number of messages in current channel')
    @commands.has_permissions(manage_messages=True)
    async def purge(self,ctx, amount=5):
        if amount >= 1:
            await ctx.channel.purge(limit=amount+1)
            embed = discord.Embed(title='Cleaning the streets',description=f'{amount} messages deleted.', color=color)
            await ctx.send(embed=embed, delete_after=2)
        else:
            embed = discord.Embed(title='Uh-oh',description='Please enter a positive value', color=color)
            await ctx.send(embed=embed)



    # Error handling
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please enter required arguements. Use `=help <command>` to see required arguements')


def setup(client):
    client.add_cog(moderation(client))
