import discord
from discord.ext import commands
import random

client = commands.Bot(command_prefix = '-')

@client.event
async def on_ready():
    print('aespir is ready')

client.remove_command('help')
@client.command()
async def help(ctx): #a custom yet garbage help command
    await ctx.send('*aespir v.0*\n**commands:**\nping\n8ball {your question}\nmeme\naddmeme {a link to your meme}\n')
    print(f'help     {round(client.latency*1000)}ms')

@client.command()
async def ping(ping): #pong!
    await ping.send(f'pong! {round(client.latency*1000)}ms')
    print(f'pong     {round(client.latency*1000)}ms')

@client.command(aliases =['8ball']) #an 8ball command idk
async def _8ball(ctx,*,question):
    responses = [ 'It is certain.','It is decidedly so.','Without a doubt.','Yes - definitely.','You may rely on it.',
                  'As I see it, yes.','Most likely.','Outlook good.','Yes.','Signs point to yes.','Reply hazy, try again.',
                  'Ask again later.','Better not tell you now.','Cannot predict now.','Concentrate and ask again.',
                  'Don\'t count on it.','My reply is no.','My sources say no.','Outlook not so good.','Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
    print(f'8ball    {round(client.latency*1000)}ms')

@client.command()
async def meme(ctx): #memes yeyeye
     memes = open("memes.txt","r")
     oof = "AAAAH"
     memeslist = []
     while oof != '':
         oof = raw(str(memes.readline()))
         memeslist.append(oof)
     sentmeme = '{\'\'}'
     while sentmeme == '{\'\'}' or sentmeme == '':
         sentmeme = random.choice(memeslist)
     await ctx.send('your meme, good lad- '+sentmeme)
     memes.close()
     print(f'meme     {round(client.latency*1000)}ms')

@client.command() #command to add  m e m e s
async def addmeme(ctx,*,link):
    memes = open("memes.txt","a")
    memes.write('\n'+link)
    await ctx.send('your meme has been added to the collection :)')
    print(f'addmeme  {round(client.latency*1000)}ms')

    
escape_dict={'':r'','\b':r'','\c':r'','\f':r'','\n':r'','\r':r'','\t':r'','\v':r'','\'':r'','\"':r'','\0':r'','\1':r'','\2':r'',
             '\3':r'','\4':r'','\5':r'','\6':r'','\7':r'','\8':r'','\9':r''}

def raw(text):
    #gets rid of unfresh and unrad characters that we don't want
    new_string=''
    for char in text:
        try: new_string+=escape_dict[char]
        except KeyError: new_string+=char
    #new_string = new_string[:-3]
    return new_string

tokenfile = open("token.txt","r") #get the token from token.txt
token = raw(str(tokenfile.readline()))
print('readying with token '+token)
client.run(token)
