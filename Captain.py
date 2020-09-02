#Test coding link https://discord.com/api/oauth2/authorize?client_id=741859314054201446&permissions=470543511&scope=bot

#Import files for use
import os
import random
import discord


#Import specific items from above files
from dotenv import load_dotenv
from discord.ext import commands

#Setting up bot token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#Variables
new_member = 'babyquail'
bot = commands.Bot(command_prefix='-')

#Remove default help command
bot.remove_command('help')

#When the bot is online, print in terminal
@bot.event
async def on_ready():
   print(f'{bot.user.name} has connected to a server')
   await bot.change_presence(
       activity=discord.Activity(type=discord.ActivityType.watching,
       name=str(len(bot.guilds)) + " servers | -help")
    )


#User server interaction events
@bot.event
async def on_member_join(member):
    print(f'{member} has joined a server')

@bot.event
async def on_member_remove(member):
    print(f'{member} has left a server')


#Help Command
@bot.command()
async def help(ctx):
    helpem = discord.Embed(
        title = 'CaptainPy Help',
        description = 'Here are a list of helpful commands I understand',
        color = discord.Color.blue()
    )
    
    helpem.add_field(name='-ping', value='Returns bot latency', inline=False)
    helpem.add_field(name='-purge<number of messages>', value='Deleted specified number of messages(default value is 5)', inline=False)
    helpem.add_field(name='-roll_dice<number of dice><number of sides>', value='Dice roll generator', inline=False)
    helpem.add_field(name='-kick<@member>', value='Kick meantioned member(must be admin)', inline=False)
    helpem.add_field(name='-ban<@member>', value='Ban meantioned member(must be admin)', inline=False)
    helpem.add_field(name='-unban<member>', value='Unbans member via name and descriminator(must be admin)', inline=False)
    helpem.add_field(name='-8ball,-magicball<question>', value='Ask the magic 8 ball a question.', inline=False)
    helpem.add_field(name='-patreon', value='Link to Quail Studio patreon', inline=False)

    await ctx.send(embed=helpem)

'''
#Reaction events
@bot.event
async def on_reaction_add(ctx, reaction, user):
    channel = reaction.message.channel
    await ctx.send_message(channel,'{} has added {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))
@bot.event
async def on_reaction_remove(ctx, reaction, user):
    channel = reaction.message.channel
    await ctx.send_message(channel,'{} has removed {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))
'''




#Ping command to check for latency
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency*1000)}ms')



#Moderator Commands

#Delete messages
@bot.command()
async def purge(ctx, amount=5):
    if amount >= 1:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'{amount} messages deleted')
    else:
        await ctx.send('Please enter a positive number')

#Kick and Ban members
@bot.command()
@commands.has_role('admin')
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kick {member.mention}')

@bot.command()
@commands.has_role('admin')
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Ban {member.mention}')

#Unban a member
@bot.command()
@commands.has_role('admin')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return




'''
#Embeds
@bot.command()
async def showembed(ctx):
    embed = discord.Embed(
        title = 'Title',
        description = 'Description',
        color = discord.Color.blue()
    )
    pic = 'https://upload.wikimedia.org/wikipedia/commons/7/73/Brown_Quail.jpg'
    embed.set_footer(text='This is a footer')
    embed.set_image(url=pic)
    embed.set_thumbnail(url=pic)
    embed.set_author(name='Author Name', icon_url= pic)
    embed.add_field(name='Field Name', value='Field Value', inline=False)
    embed.add_field(name='Field Name', value='Field Value', inline=True)
    embed.add_field(name='Field Name', value='Field Value', inline=True)
    await ctx.send(embed=embed)
'''

#Fun commands
@bot.command(aliases=['8ball', 'magicball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain',
                 'It is decidedly so',
                 'Without a doubt',
                 'Yes - definitely',
                 'You may rely on it',
                 'As i see it, yes',
                 'Most likely',
                 'Outlook good',
                 'Yes',
                 'Signs point to yes',
                 'Reply hazy, try again',
                 'Ask again later',
                 'Better not tell you now',
                 'Connot predict now.',
                 'Concentrate and ask again',
                 'Don\'t count on it',
                 'My reply is no.',
                 'My sources say no',
                 'Outlook not so good',
                 'Very doubtful']
    await ctx.send(f'Question:{question}\n Answer: {random.choice(responses)}')


@bot.command()
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1 )))
        for _ in range(number_of_dice)
    ]

    await ctx.send(', '.join(dice))




'''#Auto Role
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=new_member)
    await member.add_roles(role)
'''



#Profile
@bot.command()
async def profile(ctx,member: discord.Member):
    username = member.display_name
    profile = discord.Embed(
        title = username,
        color = discord.Color.blue()
    )
    profile.set_thumbnail(url='{}'.format(member.avatar_url))    
    
    await ctx.send(embed=profile)



#Qauil Support
@bot.command()
async def patreon(ctx):
    await ctx.send('https://www.patreon.com/quailstudio1')


#Error Handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command')
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'question':
            await ctx.send('Please ask a question')
        if error.param.name == 'number_of_dice':
            await ctx.send('Please specify number of dice and number of sides')
        if error.param.name == 'channel_name':
            await ctx.send('Please name the new channel')




bot.run(TOKEN)
