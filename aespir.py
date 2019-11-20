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
    await ctx.send('```aespir v.0 - prefix \'-\'\n---\ncommands:\nping\nflip\n8ball {your question}\nmeme\nhellfire {password} {custom message} :)\nmemeadd {a link to your meme}```')
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
    await ctx.send(f'```Question: {question}\nAnswer: {random.choice(responses)}```')
    print(f'8ball    {round(client.latency*1000)}ms')

@client.command()
async def flip(ctx):
    coin = ['heads','tails']
    await ctx.send(f'```you flipped {random.choice(coin)}!```')
    print(f'flip     {round(client.latency*1000)}ms')

@client.command()
async def meme(ctx): #memes yeyeye
     memes = open("memes.txt","r")
     oof = "shrek is hot"
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


filestuff = ['.gif','.png','.jpg','.mov','.mp4','.mp3']
@client.command() #command to add  m e m e s
async def memeadd(ctx,*,link):
    islink = False
    bruh = False
    for end in filestuff:
        if end in link: islink = True
    memes = open("memes.txt","a")
    for aaa in escape_dict:
        if aaa in link: bruh = True
    if islink and not bruh:
        memes.write('\n'+link)
        await ctx.send('your meme has been added to the collection :)')
    else:
        await ctx.send('woah there buckaroo, not so fast. we only want meme links in these parts, \'yahear.')
    memes.close()
    print(f'addmeme  {round(client.latency*1000)}ms')



escape_dict={'\b':r'','\c':r'','\f':r'','\n':r'','\r':r'','\t':r'','\v':r'',
             '\'':r'','\"':r'','\0':r'','\1':r'','\2':r'',
             '\3':r'','\4':r'','\5':r'','\6':r'','\7':r'','\8':r'','\9':r''}

@client.command()
async def hellfire(ctx,passwordinp,*,message = '@everyone'):
    hellfile = open("hellpassword.txt","r+") #get the token from token.txt
    passwords = ''
    read_line = 'sansundertale'
    password = raw(str(hellfile.readline()))
    while read_line != '':
        read_line = raw(str(hellfile.readline()))
        passwords += read_line.replace(' ','') + '\n'
    if passwordinp == password and password != '':
        await ctx.send('hellfire accepted. commencing...')
        i = 0
        hellfile.truncate(0)
        hellfile.seek(0)
        hellfile.write(passwords)
        hellfile.close()
        while i < 3:
            await ctx.send(message)
            print(f'hellfire {round(client.latency*1000)}ms')
            i += 1
    elif password == '':
        await ctx.send('hellfire denied, no password set.')
        hellfile.close()
        print(f'hellfire denied, no password set. set one in hellfire.txt.')
    else:
        await ctx.send('hellfire denied.')
        hellfile.close()
            


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
tokenfile.close()
def clientrun():
    global token
    print('readying with token '+token)
    try:
        client.run(token)
    except Exception:
        input('error, bad token passed. press enter to exit.')
clientrun()
