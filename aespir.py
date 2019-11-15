import discord
from discord.ext import commands
import random

client = commands.Bot(command_prefix = '-')

@client.event
async def on_ready():
    print('aespir is ready')

@client.command()
async def ping(ping):
    await ping.send(f'pong! {round(client.latency*1000)}ms')
    print(f'ping! {(client.latency*1000)}ms')

@client.command(aliases =['8ball'])
async def _8ball(ctx,*,question):
    responses = [ 'It is certain.','It is decidedly so.','Without a doubt.','Yes - definitely.','You may rely on it.',
                  'As I see it, yes.','Most likely.','Outlook good.','Yes.','Signs point to yes.','Reply hazy, try again.',
                  'Ask again later.','Better not tell you now.','Cannot predict now.','Concentrate and ask again.',
                  'Don\'t count on it.','My reply is no.','My sources say no.','Outlook not so good.','Very doubtful.']
    await ctx.send(random.choice(responses))
    print(f'8ball command,{(client.latency*1000)}ms')
    
client.run('NjQ0NTk3MTQxOTIyMzgxODI0.Xc2Wmg.v1agv9yAEASTLMMhuOpo1ulSID8') #bot token
