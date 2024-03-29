#Taylor Dolph 2019-2023
#=======================================#
from asyncio.events import set_child_watcher
from typing_extensions import runtime
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.ext.commands import has_permissions
import random
import time
import os, os.path
import urllib.request
import asyncio
from concurrent.futures import ThreadPoolExecutor
from discord.ext.commands.errors import CommandInvokeError
import psutil
import socket
import json
import sys
from os import system, name, path
import datetime
import string
import youtube_dl
from gpiozero import CPUTemperature
import requests
import aiohttp
from io import BytesIO
#=======================================# from files
#open config file
with open('config.json') as file: config = json.load(file)
#open token file
if path.isfile('token.txt'):
    with open('token.txt') as file: token = json.load(file)
else: 
    token = input('token: ')
    with open('token.txt', 'w') as f: json.dump(token, f)
#open data file
if path.isfile('data.json'):
    with open('data.json') as file: data = json.load(file)
else: 
    data = {'pets':0,'gay':{},'dadlist':[]}
    with open('data.json', 'w') as f: json.dump(data, f)

Token = token
PREFIX = config['prefix']
STARTPETS = data['pets']
COLOR = 0xaad5d3
NULL = "" #???????????????
#=======================================# from dadList.json
#with open('dadList.json') as file: nodadlist = json.load(file)
dadlist = data['dadlist']
#=======================================# funky variables
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
STARTTIME=int(time.time())
client = commands.Bot(command_prefix = PREFIX, intents=discord.Intents.all()) 
channel = NULL #channel that's being watched in the terminal
loop = asyncio.get_event_loop()
#=======================================# counters
totalCommands = 0
TotalMp3s = 0
#=======================================# auihsdaiushda
async def getRuntime(): # not the best way to do this but whatever
    seconds = int(time.time()) - STARTTIME
    minutes = 0
    while seconds >= 60:
        seconds -= 60
        minutes += 1
    hours = 0
    while minutes >= 60:
        minutes -= 60
        hours += 1
    days=0
    while hours >= 24:
        hours -= 24
        days += 1
    return(f'{days}d{hours}h{minutes}m{seconds}s')
#=======================================#
async def updateData():
    global data
    with open("data.json", "w") as jsonFile: json.dump(data, jsonFile)
#=======================================# yeehaw
@client.event
async def on_ready():
    if os.name != 'nt':
        discord.opus.load_opus('opus')
        if not discord.opus.is_loaded():
            raise RunTimeError('Opus failed to load')
    await client.change_presence(activity=discord.Game(name="music!"))
    #await client.change_presence(activity=discord.Activity(name="my prefix is a squiggly line"))
    print('Aespir is ready')
    await inputLoop()
#=======================================# 
@client.event 
async def on_message(message):
    await client.process_commands(message)
    ctx = await client.get_context(message)
    if message.author == client.user or ctx.command: return
    id = message.channel.id
    msg = message.content.lower()
    if('aespir' in msg): 
        await message.add_reaction('❤️')
        await cmdlog('<3')
    if(channel and id==channel.id):
        links = ""
        for attachment in message.attachments:
            links += " ["+attachment.url+"]"
        print("[" + message.author.name + "] " + message.content + links)
#=======================================# dad
    if(id in dadlist):
        dadmsg = msg.replace(",","")
        imList = ['i\'m ','im ','i am ']
        for im in imList:
            if im in dadmsg:
                msgList = dadmsg.split(im)
                if len(msgList) > 1: person = msgList[1]
                else: person = msgList[0]
                await message.channel.send('hi ' + person +', '+im+'dad!')
                await cmdlog("i'm dad")
                return
#=======================================# space!!!!
@client.command(aliases=['astro','nasa','apod'])
async def astronomy(ctx):
    data = requests.get('https://api.nasa.gov/planetary/apod?api_key=ZjEOciDzMmA2h2rCYQKSZPVJ4CRGvEzvmRJaKb98').json()
    if 'copyright' in data: copy = f'\ncopyright '+data['copyright'] 
    else: copy = ''
    text = data['explanation']+'\n'+copy+' '+data['date']
    embed=discord.Embed(title=data['title'], description=text, url='https://apod.nasa.gov/apod/astropix.html', color=COLOR)
    #embed.set_thumbnail(url='https://science.gsfc.nasa.gov/astrophysics/images/goddardsignature2.png')
    embed.set_image(url=data['hdurl'])
    await ctx.send(embed=embed)
    await cmdlog('nasa')
#=======================================# <3
@client.command()
@has_permissions(administrator=True)
async def goawaydad(ctx):
    id = ctx.channel.id
    if id not in dadlist:
        await ctx.send("dad hath already hastened from thine chambers, mine lord...")
        await cmdlog('dadaway f')
        return
    data['dadlist'].remove(id)
    updateData()
    await ctx.send(f'bye {ctx.message.author.name}, i\'m dad!')
    await cmdlog('dadaway')
#=======================================#
@client.command()
@has_permissions(administrator=True)
async def dadjokes(ctx):
    id = ctx.channel.id
    if id in dadlist:
        await ctx.send("dad is already enabled in this channel, silly!")
        await cmdlog('dadback f')
        return
    data['dadlist'].append(id)
    updateData()
    await ctx.send(f'hi {ctx.message.author.name}, i\'m dad!')
    await cmdlog('dadjokes')
#=======================================#
async def dumpJson(filename, data):
    with open(filename, 'w') as f: json.dump(data, f)
#=======================================# note: maybe move to a text file
client.remove_command('help')
@client.command()
async def help(ctx):
#download [d] {link or media attachment} (sends you an mp3)
    embed=discord.Embed(title="Aespir v0.7.1, spagoogi#5559 2019-2021, prefix: "+PREFIX, url="https://discord.com/oauth2/authorize?client_id=459165488572792832&scope=bot",
    description='''***--- recreational discordbottery***
flip (a coin)
8ball {your question}
echo {your message}
uwu [owo] {your text} (uwu)
pop {custom message, defaults to pop} (hehe)
pingme (pings you after a randomized timer. why would you use this?)
quote {user} {message} (find when they said boobie!)
quoteall {user} (slooooooooooooooooooow)
roulette (russian!)
roulettespin (spins the chamber, if you're into that sort of thing)
apod [nasa] (SPACE!!!!)
calc {word, thing} (I did the math....)

***--- media commands***
meme (yes)
addmeme {media attachment} (more memes!!!)
cute (absolutely)
addcute {media attachment} (more puppies!!!)

***--- voice commands*** (new! :D)
join  [j] {voice channel ID, optional} (joins a VC)
leave [l] (leaves the currently joined VC in this server)
play  [p,a] {link or media attachment} (plays a song!)
queue [q] (shows the server's current queue)
skip  [s] {song #, optional} (skips a song in the queue)

***--- bot health and other boring tidbits***
ping (pong!)
stats (for nerds)
help (you're using it right now!!11!!!!1!1!)

***--- admin only***
dadjokes (activates dad jokes, per channel)
goawaydad (removes dad jokes, per channel)
I feel like I should mention that dad jokes are disabled by default

***--- :D***
invite (yes please)
sourcecode (goodie!)
''',
    color=COLOR)
    await ctx.send(embed=embed)
    await cmdlog('help')
#=======================================# pong!
@client.command()
async def ping(ping):
    await ping.send(f'pong! {round(client.latency*1000)}ms')
    await cmdlog('pong!')
#=======================================# yes!!!!!
queues = {}

ydl_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes
    #'postprocessors': [{ #optional but outputs mp3s instead of webms if we need them at some point
    #    'key': 'FFmpegExtractAudio',
    #    'preferredcodec': 'mp3',
    #    'preferredquality': '256',
    #}]
}

ffmpeg_options = { 'options': '-vn' }

ydl = youtube_dl.YoutubeDL(ydl_options)

class ydlSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.id = data.get('id')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, ydl = ydl):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ydl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


"""
@client.command(aliases = ['d'])
async def download(ctx, *, url = ''):
    global TotalMp3s
    await ctx.send(f'I\'m working on your file now, {ctx.message.author.name}! This could take a little while, so I\'ll ping you when it\'s ready.')
    filename = f'aespirdownload#{TotalMp3s}.mp3'
    TotalMp3s+=1
    ydl_options_download = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes
        'postprocessors': [{ #outputs mp3s instead of webms
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '126',}]}
    ydl_download = youtube_dl.YoutubeDL(ydl_options_download)
    async with ctx.typing(): await ydlSource.from_url(url, stream = False, ydl = ydl_download)
    await ctx.send(f'{ctx.message.author.mention}, here\'s your file!', file=discord.File(filename))
    if os.path.isfile(filename): os.remove(filename)
    await cmdlog('download')
"""
    

@client.command(aliases =['add','p','a'])
async def play(ctx, *, url = ''):
    global queues
    id = ctx.guild.id
    if url == '' and ctx.message.attachments != NULL: 
        content_type = ctx.message.attachments[0].content_type
        print(f'content type: {content_type}')
        if 'audio' not in content_type and 'video' not in content_type:
            await ctx.send('Sorry, I can only play audio and video formats! (not images or executables. lol???)')
            return
        url = ctx.message.attachments[0].url


    voice = ctx.voice_client
    if not voice: 
        voice = await join_voice(ctx)
        if id in queues: queues.pop(id)

    async with ctx.typing(): player = await ydlSource.from_url(url, stream = True)
    if id not in queues: queues[id] = [player]
    else: queues[id].append(player)

    text = 'Now playing'
    if voice.is_playing(): text = 'Added to queue'
    else: voice.play(player, after=lambda e: asyncio.run(update_queue(ctx)))
    
    embed=discord.Embed(title=f'{text}: {player.title}', color=0xaad5d3, url=f'https://www.youtube.com/watch?v={player.id}')
    await ctx.send(embed=embed)

    #await ctx.send(f'Now playing: {player.title} https://www.youtube.com/watch?v={queues[id][0].id}')

@client.command(aliases=['j'])
async def join(ctx, id = NULL): 
    if id == NULL: await join_voice(ctx)
    else: 
        channel = client.get_channel(id)
        await channel.connect()

@client.command(aliases=['l'])
async def leave(ctx): await ctx.voice_client.disconnect()

@client.command(aliases=['s'])
async def skip(ctx, num = 0): 
    global queues
    id = ctx.guild.id
    num = int(num)
    if id not in queues:
        await ctx.send("There isn't anything to skip!")
        return
    if num > len(queues[id]) or num < 0:
        await ctx.send("That number isn't in the queue!")
        return
    voice = ctx.voice_client
    if voice and voice.is_playing():
        song = queues[id][num]
        embed=discord.Embed(title=f'Skipped: {song.title}', color=0xaad5d3, url=f'https://www.youtube.com/watch?v={song.id}')
        await ctx.send(embed=embed)
        if num == 0:
            voice.stop()
            await update_queue(ctx)
        else:
            queues[id].pop(num)
    else: await ctx.send("There's nothing to skip!")

@client.command(aliases=['q'])
async def queue(ctx,cmd = NULL,*,dat = NULL):
    global queues
    id = ctx.guild.id
    if id not in queues: 
        await ctx.send("Sorry 'pardner, but there isn't a queue for this server yet. You can make one my adding a song with ~play!")
        return
    songs = queues[id]
    outp = ""
    for i in range(1,len(songs)):
        song = f'{i:02d}: {songs[i].title}\n'
        outp+=song
        if len(outp) > 2000:
            outp = outp[0:-len(song)]
            break
    embed=discord.Embed(title=f'Currently playing: {songs[0].title}', color=0xaad5d3, url=f'https://www.youtube.com/watch?v={songs[0].id}',description = outp)
    await ctx.send(embed=embed)

async def update_queue(ctx):
    global queues
    id = ctx.guild.id
    if id in queues and len(queues[id]) > 1: 
        queues[id].pop(0)
        player = queues[id][0]
        ctx.voice_client.stop()
        ctx.voice_client.play(player, after=lambda e: asyncio.run(update_queue(ctx)))
        embed=discord.Embed(title=f'Now playing: {player.title}', color=0xaad5d3, url=f'https://www.youtube.com/watch?v={player.id}')
        await ctx.send(embed=embed)
    elif id in queues: queues.pop(id)

async def join_voice(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    return discord.utils.get(client.voice_clients, guild=ctx.guild)

async def is_connected(ctx):
    if discord.utils.get(client.voice_clients, guild=ctx.guild) == None: return False
    return True

@client.command()
async def pet(ctx):
    data['pets'] += 1
    await updateData()
    await ctx.send(f"thanks!!!!\nI have been pet a total of {data['pets']} times")
    await cmdlog('pet')
#=======================================# fancy
#uptime: {time.strftime("%H:%M:%S", psutil.boot_time())}
@client.command(pass_context=True)
async def stats(ctx):
    ips = ['in ur mom','in ur dad','outside your window','ohio','7.16.0.216','2','under your bed','ur mums bed','ur dads bed','come outside','1.2.3.4','sex','funky town','ralsei village','miitopia']
    # the core temp check only works on pis,
    # but this check only works if you don't
    # change your host name. I'll fix it later.
    # Maybe. Possibly. Okay probably not
    if socket.gethostname() == 'raspberrypi': # BAD IDEA
        temp = round(CPUTemperature().temperature)
    else: 
        temps = ['extra spicy', 'steamy', 'a hotplate', 'yes', 'frosty', 'ō^Õ', 'TEMPERATURE', 'NULL', '?REDO FROM START', 'help me', 'squagga', 'hellfire','−273.15', '776']
        temp = random.choice(temps)
    
    embed=discord.Embed(title="Stats For Nerds ÓwÒ", url="https://cdn.shopify.com/s/files/1/0014/1962/products/product_DR_ralsei_plush_photo3.png?v=1550098980",
    description=f'''***--- system stats***
network latency: {round(client.latency*1000)}ms
uptime: {await getRuntime()}
CPU usage: {psutil.cpu_percent()}%
core temperature: {temp}°C
RAM usage: {psutil.virtual_memory().percent}%
ipv4 address: {random.choice(ips)}

***--- bot stats***
commands since startup: {totalCommands+1} 
pets since startup: {data['pets']-STARTPETS}
***currently active in {len(client.guilds)} servers***''',
    color=COLOR)
    await ctx.send(embed=embed)
    await cmdlog('stats')
#=======================================#
@client.command(aliases =['8ball'])
async def _8ball(ctx,*,question):
    responses = [ 'It is certain.','It is decidedly so.','Without a doubt.','Yes - definitely.','You may rely on it.',
                  'As I see it, yes.','Most likely.','Outlook good.','Yes.','Signs point to yes.','Reply hazy, try again.',
                  'Ask again later.','Better not tell you now.','Cannot predict now.','Concentrate and ask again.',
                  'Don\'t count on it.','My reply is no.','My sources say no.','Outlook not so good.','Very doubtful.']
    random.seed(question)
    await ctx.send(f'```Question: {question}\nAnswer: {random.choice(responses)}```')
    await cmdlog('8ball')
#=======================================# terrifying
async def split_by_list(txt, seps):
    default_sep = seps[0]
    # we skip seps[0] because that's the default separator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]

@client.command(aliases =['owo']) 
async def uwu(ctx,*,text):
    text = text.lower()
    replaceWithW=['l','r']
    vowels = ['a','e','i','o','u']
    for letter in replaceWithW: text = text.replace(letter, 'w')
    text = text.replace('ov', 'uv')
    letternum = 0
    while letternum < len(text) -1:
        letter = text[letternum]
        nextLetter = text[letternum+1]
        if (letter == 'n') and nextLetter in vowels: text = text[0:letternum+1]+'y'+text[letternum+1:]
        letternum+=1
    owos = ['OwO', 'Owo', 'owO', 'ÓwÓ', 'ÕwÕ', '@w@', 'ØwØ', 'øwø', 'uwu', '☆w☆', '✧w✧', '♥w♥', '゜w゜', '◕w◕', 'ᅌwᅌ', '◔w◔', 'ʘwʘ', '⓪w⓪', 'OvO','ovo']
    punct = ['.',';', ',']
    #i = 0
    textlist = await split_by_list(text, punct)
    text = ""
    for phrase in textlist: 
        phrase = phrase.strip()
        random.seed=phrase
        text += f'{phrase} {random.choice(owos)} '
    await ctx.send(f'{text}')
    await cmdlog('uwu')
#=======================================# 
@client.command() 
async def echo(ctx,*,text):
    await ctx.send(text)
    await cmdlog('echo')
#=======================================# 
@client.command() 
async def tylersimulator(ctx):
    s = ''.join(random.choice(string.ascii_letters) for i in range(random.randint(7,16)))
    arr = [ 'boobie' , 'balls owo', 'whhat??', 'ghhbbb','minecraf c:', 'based', 'the yoinky sploinky', 'beepbop skeebo!', 'SCRUNGLE', 'God Fucking Damn It I Fucking Love The Space Shuttle', s,s,s,s,s,s,s ]
    await ctx.send(random.choice(arr))
    await cmdlog('tyler')
#=======================================# why would you do this
@client.command(pass_context=True) 
async def pingme(ctx):
    await ctx.send('will do!')
    await cmdlog('pingme1')
    await asyncio.sleep(random.randint(300,1200))
    await ctx.send(ctx.message.author.mention)
#=======================================# pop
@client.command()
async def pop(ctx,*,pop='pop'):
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
    imglist = os.listdir(f'{folder}/')
    random.shuffle(imglist)
    #print('shuffled the {folder}')
    return(imglist)
#=======================================# there are some good ones in there, i think
memelists = {}
memecounters = {}
@client.command()
async def meme(ctx): #memes yeyeye
    global memelists
    global memecounters
    (memecounters[ctx.channel.id], memelists[ctx.channel.id]) = await sendImage(ctx, memelists, memecounters, 'your meme, good lad', 'memes', spoiler=False)
    await cmdlog('meme')
#=======================================# kittens!
cutelists = {}
cutecounters = {}
@client.command()
async def cute(ctx): #kittens yeyeye
    global cutelists
    global cutecounters
    (cutecounters[ctx.channel.id], cutelists[ctx.channel.id]) = await sendImage(ctx, cutelists, cutecounters, 'your cute image, good lad', 'cute', spoiler=False)
    await cmdlog('cute')
#=======================================# the guts of ~cute and ~meme
async def sendImage(ctx, lists, counters, message, folder, spoiler):
    id = ctx.channel.id
    if id not in counters:
        counters[id]=0
        lists[id] = await shuffleImages(folder)
    imagelist = lists[id]
    counter = counters[id]
    filename = folder+'/'+imagelist[counter]
    await ctx.send(message,file = discord.File(filename, spoiler=spoiler))
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
async def addmeme(ctx, link = ''): await addimage(ctx, link, 'memes')
@client.command() 
async def addcute(ctx, link = ''): await addimage(ctx, link, 'cute')
#=======================================#
async def nsfwCheck(ctx):
    if not isinstance(ctx.channel, discord.channel.DMChannel) or not ctx.channel.is_nsfw(): return False
    await ctx.send('sorry pardner, you need to be in a NSFW channel or DM to use this command!')
    return True
#=======================================# embeds images for ~meme and ~cute
async def image(ctx, sent, folder, message):
    await ctx.send(message,file=discord.File(folder+'/'+sent))
#=======================================# downloads an image, used for ~addmeme and ~addcute
async def addimage(ctx, url, dir):
    global user_agent 
    headers={'User-Agent':user_agent,}
    isLink = False
    if ctx.message.attachments:
        url = ctx.message.attachments[0].url
        islink = True
    if islink:
        request=urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        data = response.read()
        newImg = open(dir+'/'+str(await imageNum(dir))+'.'+url.split('.')[-1], "wb")
        newImg.write(data)
        newImg.close()
        await ctx.send('```your media has been added to the collection :)```')
    else: await ctx.send('```woah there buckaroo, not so fast. we only want media attachments and links in these parts, \'yahear.```')
    await cmdlog(f'add{dir}')
#=======================================# russian!
chambers = {}
@client.command(pass_context=True)
async def roulette(ctx):
    global chambers
    id = ctx.channel.id
    if id not in chambers: chambers[id] = random.randint(0,5)
    if chambers[id] <= 0:
        await ctx.send('```bang!```')
        chambers[id] = random.randint(0,5)
    else: 
        await ctx.send('```click...```')
        chambers[id]-=1
    await cmdlog('roulette')
#=======================================# brr
@client.command()
async def roulettespin(ctx):
    global chambers
    chambers[ctx.channel.id] = random.randint(0,5)
    await ctx.send('```haha chamber go spin```')
    await cmdlog('spin')
#=======================================# async terminal input
async def inputAsync(prompt: str = ''):
    with ThreadPoolExecutor(1, 'ainput') as executor:
        return (await asyncio.get_event_loop().run_in_executor(executor, input, prompt)).rstrip()
#=======================================# yes
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
#=======================================# very scientific
async def id(mention:str):
    mention = mention.replace("<","")
    mention = mention.replace(">","")
    mention = mention.replace("@","")
    mention = mention.replace("!","")
    return int(mention)

@client.command(pass_context=True)
async def calc(ctx,word,*,thing = None):
    if thing == None: 
        thing = ctx.message.author.mention
    userid = await id(thing)
    thing = str(thing)
    random.seed(thing+word)
    percentage = int(random.random()*101)
    if percentage > 95: percentage = 100
    if percentage < 1: percentage = 1
    user = client.get_user(await id(thing))
    if(user): thing = user.name
    if thing == ctx.message.author.mention: await ctx.send(f'you are {percentage}% {word}')
    else: await ctx.send(f'{thing} is {percentage}% {word}')
    await cmdlog('percent')
#=======================================# was for testing purposes. i dont have the heart to delete it
@client.command(pass_context=True)
async def whoami(ctx):
    await ctx.send('you are '+ ctx.message.author.name + ", id "+ str(ctx.message.author.id))
    cmdlog('whoami')
#=======================================#
@client.command()
async def quoteme(ctx,*,text = ""):
    rawmessages = await ctx.channel.history(oldest_first = False, limit = 10000).flatten()
    messages = []
    for message in rawmessages:
        if(text=="" and message.author==ctx.author and "~quoteme" not in message.content):messages.append(message)
        elif(text!="" and message.author==ctx.author and text in message.content and "~quoteme" not in message.content):messages.append(message)
    if(len(messages)==0): await ctx.send("no message was found with your specifications!")
    else:
        cont = True
        count = 0
        while(cont):
            rand = random.randint(0,len(messages)-1)
            message = messages[rand]
            if(message.content.split() or count > 10): cont = False
            count += 1
        await ctx.send(ctx.message.author.name + ", on "+str(message.created_at.replace(microsecond=0))+", you said \"" + message.content + "\"")
    await cmdlog('quoteme')
#=======================================#
@client.command()
async def quote(ctx,user: discord.User,*,text = ""):
    messages = await ctx.channel.history(oldest_first = False, limit = 100000).flatten()
    messages2 = []
    for message in messages:
        if(text == "" and message.author == user): messages2.append(message)
        elif(text!="" and message.author == user and text in message.content): messages2.append(message)
    messages = messages2
    if(len(messages)>0):
        rand = random.randint(0,len(messages)-1)
        message = messages[rand]
        await ctx.send("on "+str(message.created_at.replace(microsecond=0))+", "+user.name+" said \"" + message.content + "\"")
    else: await ctx.send("no message was found with your specifications!")
    await cmdlog("quote")
#=======================================#
@client.command()
async def quoteall(ctx,user: discord.User,*,text = ""):
    await ctx.send("on it! this might take a minute, so hold on to your hat(s)!")
    print("before search")
    messages = await ctx.channel.history(oldest_first = False, limit = 100000).flatten()
    print("after search")
    messages2 = []
    for message in messages:
        if(text == "" and message.author == user): messages2.append(message)
        elif(text!="" and message.author == user and text.lower() in message.content.lower()): messages2.append(message)
    messages = messages2
    if(len(messages)) == 0: await ctx.send("no message was found with your specifications!")
    elif(len(messages)<4):
        for message in reversed(messages):
            await ctx.send("on "+str(message.created_at.replace(microsecond=0))+", "+user.name+" said \"" + message.content + "\"")
    else:
        basename = "quotes"
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        filename = "_".join([basename, suffix, ".txt"]) 
        #filename = ".\\"+str(uuid.uuid4().hex)+".txt"
        file  = open(filename, "w+", encoding="utf-8") 
        for message in reversed(messages): file.write("on "+str(message.created_at.replace(microsecond=0))+", "+user.name+" said \"" + message.content + "\"\n")
        file.close()
        await ctx.send("here are your quotes! there were too many, so I put them in a file :D",file=discord.File(filename))
        os.remove(filename)
    await cmdlog("quote")
#=======================================# hmmmmnnbnb
async def on_command_error(self, ctx, error): # this is broken. oops!
    ignored = (commands.CommandNotFound, )
    if isinstance(error, ignored): return
    if isinstance(error, commands.DisabledCommand): await ctx.send(f'{ctx.command} is disabled!')
    elif isinstance(error, commands.NoPrivateMessage):
        try: await ctx.author.send(f'{ctx.command} can\'t be used in private messages!')
        except discord.HTTPException: pass
    elif isinstance(error, commands.BadArgument):
        if ctx.command.qualified_name == 'tag list': await ctx.send('I couldn\'t find that member! Try again?')
    else: print(f'ignoring exception in {ctx.command}')
#=======================================# very poggers
doCmdlog = True
async def cmdlog(msg):
    global doCmdlog
    if doCmdlog:
        global totalCommands
        totalCommands+=1
        print(msg+' '*((10-len(msg))+1)+str(round(client.latency*1000))+'ms '+await getRuntime())
#=======================================# clears the screen
def clear():
    if name == 'nt': _ = system('cls')
    else: _ = system('clear')
#=======================================#
async def inputLoop():
    global channel
    controlling = False
    id = 0
    while True:
        inp = await inputAsync()
        cmd = inp.split()
        if(len(cmd)<1): continue
        cmdlen = len(cmd)

        if(cmd[0]=="list" and cmdlen>1):
                if(cmd[1] == "channels" and len(cmd)>2):
                    for chan in client.get_guild(int(cmd[2])).channels:
                        if str(chan.type) == 'text':
                            print(chan.name + "   "+str(chan.id))
                elif(cmd[1]=="servers"):
                    for guild in client.guilds:
                        print(guild.name + "   "+ str(guild.id))
                elif(cmd[1] == "channels"):
                    for guild in client.guilds:
                        for chan in guild.channels:
                            if str(chan.type) == 'text':
                                print(guild.name + "   " + chan.name + "   "+str(chan.id))

        elif(cmd[0]=="watch" and cmdlen>1):
            if(cmd[1]=="none"):
                channel = NULL
                print("no longer watching channel "+ str(id))
                if(controlling):
                    controlling = False
                    print("no longer controlling client in channel "+ str(id))
            else:
                id = cmd[1]
                channel = client.get_channel(id)
                print("now watching channel "+ str(id))

        elif(cmd[0]=="control"):
            if(cmdlen>1 and cmd[1]=="none"):
                controlling = False
                print("no longer controlling client in channel "+ str(id))
            elif(cmdlen>1):
                if(channel): print("no longer watching channel "+ str(id) + "\n" + "now watching channel "+ cmd[1])
                id = int(cmd[1])
                channel = client.get_channel(id)
                controlling = True
                print("now watching channel "+ str(id))
                print("now controlling client in channel "+ str(id))
            elif(channel):
                controlling = True
                print("now controlling client in channel "+ str(id))

        elif(inp == "stop" or inp == "exit"): sys.exit()

        elif(inp == "clear"): clear()

        elif(cmd[0]=="gethistory" and cmdlen>1):
            historychannel = client.get_channel(int(cmd[1]))
            limit = 200
            if(cmdlen>2): limit = int(cmd[2])
            try: 
                messages = await historychannel.history(oldest_first = False, limit = 200).flatten()
                print("\n")
                for msg in reversed(messages):
                    timestamp = ""
                    if(cmdlen>3 and cmd[3]=="true"): timestamp = str(messages[0].created_at.replace(microsecond=0))
                    links = ""
                    for attachment in msg.attachments:
                        links += " ["+attachment.url+"]"
                    print(timestamp + " [" + msg.author.name + "] " + msg.content + links)
            except: print("error reading channel history, most likely lacking permissions")


        elif(cmd[0] == "toggle" and cmd[1]=="logs"): 
            global doCmdlog
            if(cmdlen<=2): doCmdlog = not doCmdlog
            else: doCmdlog = cmd[2].lower() in ("yes", "true", "t", "1")
            print("command logging set to "+ str(doCmdlog))

        elif(channel and controlling): 
            try: await channel.send(inp)
            except: print("error sending message, most likely lacking permissions")

#=======================================# opening the token and running the client
def run(Token):
    print(f'connecting...')
    try: client.run(Token)
    except Exception: 
        Token = input("The client can't run, probably because it has a bad token.\npress enter now to exit, or enter new token now: ").strip()
        if Token != '':
            with open('token.txt', 'w') as f: json.dump(Token, f)
run(Token)


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
