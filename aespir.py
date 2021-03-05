#Tyler Dolph 2019-2021
#=======================================#
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
import ffmpeg
from discord.ext import commands
import random
import time
import os, os.path
import urllib.request
import asyncio
from concurrent.futures import ThreadPoolExecutor
import psutil
import socket
import json
#=======================================# from data.json
with open('data.json') as file: data = json.load(file)
PREFIX = data['prefix']
TOKEN = data['token']
#=======================================# funky variables
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
filestuff = ['.gif','.png','.jpg','.mov','.mp4','.mp3','.webp']
escape_dict={'\n':r''}
start=time.time()
client = commands.Bot(command_prefix = PREFIX)
#=======================================# counters
totalCommands = 0
#=======================================# gets rid of unfresh and unrad characters that we don't want
def raw(text):
    new_string=''
    for char in text:
        try: new_string+=escape_dict[char]
        except KeyError: new_string+=char
    return new_string
#=======================================# yeehaw
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="my prefix is a squiggly"))
    #await client.change_presence(activity=discord.CustomActivity(name="my prefix is a squiggly line"))
    print('Aespir is ready')
#=======================================# note: maybe move sus and dad to seperate functions. maybe.
@client.event 
async def on_message(message):
    await client.process_commands(message)
    if message.author == client.user: return
    msg = message.content.lower()
#=======================================# sus (an evil command. wretched.)
    sus = ['sus','among','amogus','amogos','vent','imposter']
    for word in sus:
        if word in msg:
            await message.channel.send('sus!!!')
            await cmdlog('sus')
#=======================================# dad
    dadmsg = msg.replace(",","")
    imList = ['i\'m ','im ','i am ']
    for im in imList:
        if im in dadmsg:
            msgList = dadmsg.split(im)
            if len(msgList) > 1: person = msgList[1]
            else: person = msgList[0]
            await message.channel.send('hi ' + person +', '+im+'dad!')
            await cmdlog('imdad')
            return
#=======================================# note: maybe move to a text file
client.remove_command('help')
@client.command()
async def help(ctx):
    await ctx.send('''```aespir v0.4, prefix \''''+PREFIX+''''\n---\ncommands: 
ping (pong!)
stats (for nerds!)
flip (a coin)
8ball {your question}
echo {your message}
uwu {your text} (uwu)
meme (yes)
addmeme {media attachment or link} (more memes!!!)
cute (absolutely)
addcute {media attachment or link} (more puppies!!!)
bubblewrap {custom message, defaults to pop} (hehe)
hellfire {password} {custom message, defaults to something fun} (NO)
roulette (russian!)
roulettespin (spins the chamber, if you're into that sort of thing)
roulettebutwithasemiautomaticpistol (not a good idea)
gay {message (optional)} (gay gay homosexual gay)
pingme (pings you after a randomized timer. why would you use this?????)
whoami (was for testing, left it in)
invite (yes please)
sourcecode (i'm open source!)```''')
    await cmdlog('help')
#=======================================# pong!
@client.command()
async def ping(ping):
    await ping.send(f'pong! {round(client.latency*1000)}ms')
    await cmdlog('pong!')
#=======================================# fancy
@client.command(pass_context=True)
async def stats(ping):
    await ping.send(f'''```system stats-----
    hostname: {socket.gethostname()}
    latency: {round(client.latency*1000)}ms
    uptime: {time.strftime("%H:%M:%S", time.gmtime(time.time() - psutil.boot_time()))}
    CPU: {psutil.cpu_percent()}%
    RAM: {psutil.virtual_memory().percent}%
    public ip: 7
bot stats--------
    client: {client.user}
    runtime: {time.strftime("%H:%M:%S", time.gmtime(time.time() - start))}
    commands since startup: {totalCommands}
    currently active in {len(client.guilds)} servers```''')
    await cmdlog('stats')
#=======================================# oooOOOOOOooooooO
@client.command(aliases =['8ball'])
async def _8ball(ctx,*,question):
    responses = [ 'It is certain.','It is decidedly so.','Without a doubt.','Yes - definitely.','You may rely on it.',
                  'As I see it, yes.','Most likely.','Outlook good.','Yes.','Signs point to yes.','Reply hazy, try again.',
                  'Ask again later.','Better not tell you now.','Cannot predict now.','Concentrate and ask again.',
                  'Don\'t count on it.','My reply is no.','My sources say no.','Outlook not so good.','Very doubtful.']
    random.seed(question)
    await ctx.send(f'```Question: {question}\nAnswer: {random.choice(responses)}```')
    await cmdlog('8ball')
#=======================================# I wrote this one awhile ago and can barely read it. I will never touch it again, it is too scary.
@client.command() 
async def uwu(ctx,*,text):
    replaceWithW=['l','r']
    vowels = ['a','e','i','o','u']
    for letter in replaceWithW: 
        text = text.replace(letter, 'w')
        text = text.replace(letter.upper(), 'W')
    text = text.replace('ov', 'uv')
    text = text.replace('Ov', 'Uv')
    letternum = 0
    for letter in text:
        if (letter == 'n' or letter == 'N') and text[letternum+1] in vowels: text = text[0:letternum+1]+'y'+text[letternum+1:len(text)]
        letternum+=1
    await ctx.send(f'{text}')
    await cmdlog('uwu')
#=======================================# makes the bot say things
@client.command() 
async def echo(ctx,*,text):
    await ctx.send(text)
    await cmdlog('echo')
#=======================================# why would you do this
@client.command(pass_context=True) 
async def pingme(ctx):
    await ctx.send('will do!')
    await cmdlog('pingme1')
    await asyncio.sleep(random.randint(300,1200))
    await ctx.send(ctx.message.author.mention)
    await cmdlog('pingme2')
#=======================================# pop
@client.command()
async def bubblewrap(ctx,*,pop='pop'):
    await ctx.send(("|| "+pop+" ||") * int(2000/((len(pop)+6))))
    await cmdlog('bwrap')
#=======================================# a coin! the first command that I made, besides ping, I think.
@client.command()
async def flip(ctx):
    coin = ['heads','tails']
    await ctx.send(f'you flipped {random.choice(coin)}!')
    await cmdlog('flip')
#=======================================# shuffles a list of images. gets them from the folder to add any new ones
async def shuffleImages(folder):
    imglist = os.listdir(f'.\\'+folder)
    random.shuffle(imglist)
    print('shuffled the '+folder)
    return(imglist)
#=======================================# there are some good ones in there
memelists = {}
memecounters = {}
@client.command()
async def meme(ctx): #memes yeyeye
    global memelists
    global memecounters
    (memecounters[ctx.channel.id], memelists[ctx.channel.id]) = await sendImage(ctx, memelists, memecounters, 'your meme, good lad', 'memes')
    await cmdlog('meme')
#=======================================# kittens!
cutelists = {}
cutecounters = {}
@client.command()
async def cute(ctx): #kittens yeyeye
    global cutelists
    global cutecounters
    (cutecounters[ctx.channel.id], cutelists[ctx.channel.id]) = await sendImage(ctx, cutelists, cutecounters, 'your cute image, good lad', 'cute')
    await cmdlog('cute')
#=======================================# the guts of ~cute and ~meme
async def sendImage(ctx, lists, counters, message, folder):
    id = ctx.channel.id
    if id not in counters:
        counters[id]=0
        lists[id] = await shuffleImages(folder)
    imagelist = lists[id]
    counter = counters[id]
    await ctx.send(message,file=discord.File('.\\'+folder+'\\'+imagelist[counter]))
    if counter >= len(imagelist)-1: 
        counter = 0
        imagelist = await shuffleImages(folder)
    else: counter+=1
    return counter, imagelist
#=======================================# gets a good number to name an image for ~addmeme and ~addcute
async def imageNum(directory):
    num = 0
    for img in os.listdir(directory):
        newNum = int(img.split('.')[0])
        if newNum > num:
            num = newNum
    return num+1
#=======================================# yes yes
@client.command() 
async def addmeme(ctx, link = ''):
    await addimage(ctx, link, 'memes')
    await cmdlog('addmeme')
#=======================================# more kittens
@client.command() 
async def addcute(ctx, link = ''):
    await addimage(ctx, link, 'cute')
    await cmdlog('addcute')
#=======================================# embeds images for ~meme and ~cute
async def image(ctx, sent, folder, message):
    await ctx.send(message,file=discord.File('.\\'+folder+'\\'+sent))
#=======================================# downloads an image, used for ~addmeme and ~addcute
async def addimage(ctx, link, folder):
    global user_agent 
    headers={'User-Agent':user_agent,}
    if ctx.message.attachments: link = ctx.message.attachments[0].url
    islink = False
    if link:
        for end in filestuff:
            if end in link[len(link)-len(end):len(link)]: islink = True
    if islink:
        request=urllib.request.Request(link, None, headers)
        response = urllib.request.urlopen(request)
        data = response.read()
        newImg = open('.\\'+folder+'\\'+str(await imageNum('.\\'+folder))+'.'+link.split('.')[-1], "wb")
        newImg.write(data)
        newImg.close()
        await ctx.send('```your media has been added to the collection :)```')
    else: await ctx.send('```woah there buckaroo, not so fast. we only want media attachments and links in these parts, \'yahear.```')
#=======================================# russian!
chambers = {}
@client.command(pass_context=True)
async def roulette(ctx):
    global chambers
    id = ctx.channel.id
    if id not in chambers: chambers[id] = -1
    pos = chambers[id]
    if pos < 0: pos = random.randint(0,5)
    if pos == 0: await ctx.send('```bang!```')
    else: await ctx.send('```click...```')
    chambers[id]-=1
    await cmdlog('roulette')
#=======================================# brr
@client.command()
async def roulettespin(ctx):
    global chambers
    chambers[ctx.channel.id] = random.randint(0,5)
    await ctx.send('```haha chamber go spin```')
    await cmdlog('spin')
#=======================================# async terminal input, only used for botcontrol so far
async def inputAsync(prompt: str = ''):
    with ThreadPoolExecutor(1, 'ainput') as executor:
        return (await asyncio.get_event_loop().run_in_executor(executor, input, prompt)).rstrip()
#=======================================# botcontrol, name is funky to avoid copying. idk, this is mostly for me to mess around with.
@client.command()
async def vjirnblisiahnvoia(ctx,*,password = ''):
    await cmdlog('control')
    if(password == ''): 
        await ctx.message.delete()
        while True:
            msg = await inputAsync()
            if msg == "exit": break
            await ctx.send(msg)
#=======================================# yes.
@client.command()
async def invite(ctx):
    link = 'https://discord.com/oauth2/authorize?client_id=459165488572792832&scope=bot'
    await ctx.send('okay, here ya go! ^-^\n'+link)
    await cmdlog('invite')
#=======================================# fresh from the vine
@client.command()
async def sourcecode(ctx):
    link = 'https://github.com/radicalspaghetti/Aespir'
    await ctx.send('okay, here ya go! ^-^\n'+link)
    await cmdlog('source')
#=======================================# do not do this
@client.command()
async def roulettebutwithasemiautomaticpistol(ctx):
    await ctx.send('```bang!```')
    await cmdlog('rip')
#=======================================# very scientific
@client.command(pass_context=True)
async def gay(ctx,*,userString = None):
    if userString == None: userString = str(ctx.message.author.mention)
    userString = userString.replace('!','')
    random.seed(userString+userString)
    num = int(random.random()*101)
    if num > 95: num = 100
    if num < 5: num = 0
    if userString == ctx.message.author.mention: await ctx.send('you are '+ str(num) +'%'+ ' gay')
    else: await ctx.send(userString + ' is ' + str(num) +'%'+ ' gay')
    await cmdlog('gay')
#=======================================# was for testing purposes; i'll just keep it in
@client.command(pass_context=True)
async def whoami(ctx):
    await ctx.send('you are '+ ctx.message.author.name + ", id "+ str(ctx.message.author.id))
    cmdlog('whoami')
#=======================================# an absolute garbage command
async def hellfireLoop(ctx, message):
    await ctx.send(message)
    await asyncio.sleep(5)
    await cmdlog('lol')
#=======================================# voice channel stuff
@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    voice = discord.VoiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio('RobotRock.mp3'), after=lambda e:  print('done', e))
    await cmdlog('join')
#=======================================#
@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect(force=True)
    await cmdlog('leave')
#=======================================# very poggers
async def cmdlog(msg):
    global totalCommands
    totalCommands+=1
    print(msg+' '*((8-len(msg))+1)+str(round(client.latency*1000))+'ms')
#=======================================# opening the token and running the client
print('connecting...')
try: client.run(TOKEN)
except Exception: input('error, most likely bad token passed. press enter to exit.')

#
#░░░░░░░░░░░▄▀▄▀▀▀▀▄▀▄░░░░░░░░░░░░░░░░░░ 
#░░░░░░░░░░░█░░░░░░░░▀▄░░░░░░▄░░░░░░░░░░ 
#░░░░░░░░░░█░░▀░░▀░░░░░▀▄▄░░█░█░░░░░░░░░ 
#░░░░░░░░░░█░▄░█▀░▄░░░░░░░▀▀░░█░░░░░░░░░ 
#░░░░░░░░░░█░░▀▀▀▀░░░░░░░░░░░░█░░░░░░░░░ 
#░░░░░░░░░░█░░░░░░░░░░░░░░░░░░█░░░░░░░░░ 
#░░░░░░░░░░█░░░░░░░░░░░░░░░░░░█░░░░░░░░░ 
#░░░░░░░░░░░█░░▄▄░░▄▄▄▄░░▄▄░░█░░░░░░░░░░ 
#░░░░░░░░░░░█░▄▀█░▄▀░░█░▄▀█░▄▀░░░░░░░░░░ 
#░░░░░░░░░░░░▀░░░▀░░░░░▀░░░▀░░░░░░░░░░░░ 
#╔═════════════════════════════════════╗
#║ * You feel like you're going to     ║
#║ have a ruff time.                   ║
#║                                     ║
#╚═════════════════════════════════════╝
#┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
#│/ FIGHT| │ ) PET | |6 ITEM | |X MERCY| 
#└───────┘ └───────┘ └───────┘ └───────┘