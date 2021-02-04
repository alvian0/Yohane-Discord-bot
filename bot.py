import discord
import random as rand
from discord.ext import commands, tasks
import json
from googleapiclient.discovery import build
from itertools import cycle
from googletrans import Translator
import googletrans
from jikanpy import Jikan
import requests
from imgurpython import ImgurClient
from discord import Spotify, Activity, Game, Streaming, CustomActivity, ActivityType
import asyncio
from imagur import *
import os
import qrcode
from pokedex import pokedex
import pypokedex
import pokebase

token = os.environ.get('token')
imagur_id = os.environ.get('imgur_id')
imagur_secret = os.environ.get('imgur_secret')
yt_api = os.environ.get('youtube_api')

#imgur client
imagur = ImgurClient(
    client_id=str(imagur_id),
    client_secret=str(imagur_secret)
    )

#pokemon
pokedex = pokedex.Pokedex(version = 'v1')

#mal client
mal = Jikan()

#translate client
translator = Translator()

#change client status cycle
status = cycle(['.help', 'everyone on this server', 'hentai', 'Alvian', 'love live', 'anime', 'nhentai.net', '.help',
    'minecraft', 'how i was made', 'Aqours', 'Guilty Kiss', 'how good i am', 'myself', 'my source code'])

#youtube client
youtube1 = build('youtube', 'v3',developerKey=str(yt_api))

#check user is me?
def is_me(ctx):
    if ctx.author.id == 570972163058958336:
        return True
    else:
        return False

#change server prefix
def cmd_prefix(client, message):
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)
    try:
        return prefixes[str(message.guild.id)]
    except:
        return "."

#get server prefix
async def serv_prefix(g_id):
    prefixes_i_supose = json.loads(open('prefix.json').read())
    try:
        return str(prefixes_i_supose[str(g_id)])
    except:
        return "."

#get mal user data
async def mal_list(id):
    try:
        list_i_supose = json.loads(open('mal.json').read())

        return str(list_i_supose[str(id)])
    except:
        return "vboabfouaf83gf297gfq93gfq9fgqggfq836fq386"

#get yt user data
async def yt_list(id):
    try:
        list_i_supose = json.loads(open('yt.json').read())

        return str(list_i_supose[str(id)])
    except:
        return "pft"

#discord client
tents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = cmd_prefix, help_command=None, intents = tents)

#doing something when join a guild/server
@client.event
async def on_guild_join(guild):
    #add server prefix into a file
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)
    
    prefixes[str(guild.id)] = '.'

    with open('prefix.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    
    #sending message when join a server
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Hey there! someone has add me into this server lol')
        break

#do something when leave the server
@client.event
async def on_guild_remove(guild):
    #remove server prefix from the file
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)
    
    prefixes.pop(str(guild.id))

    with open('prefix.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

#change server prefix
@client.command()
@commands.check(is_me)
async def prefix(ctx, new_prefix : str):
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)
    
    prefixes[str(ctx.guild.id)] = new_prefix

    with open('prefix.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    prefixes_desune = json.loads(open('prefix.json').read())

    await ctx.send("server prefix changed into **{}**".format(new_prefix))

@prefix.error
async def prefix_error(ctx, error):
    i = await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.CheckFailure):
        await ctx.send("you don't have permission to use this commands")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{i}prefix (new prefix)')
    elif isinstance(error, commands.missingPermissions):
        await ctx.send("you don't have permission to use this commands")

#on bot online
@client.event
async def on_ready():
    change_status.start()
    #chan = client.get_channel(702845878746087505)
    #await chan.send('im online')
    print('Bot is now Online')

#help command
@client.command()
async def help(ctx):
    i = await serv_prefix(g_id=ctx.guild.id)

    embed = discord.Embed(tittle = "Help",
        description = f"server prefix **{i}**" +
            f"\nuse `{i}command (category)` to see help for each category"+
            f"\nuse `{i}example (command name)` to see example for each command"+
            f"\nuse `{i}prefix (new prefix)` to change server prefix",
        colour = 0x2f64ad
    )

    embed.add_field(name="fun",
        value=
            "`ask` `repeat` `slap`  `ping` `punch` `waifurate` `hug` `f` `meme` `random` `image` `reddit`",
        inline=False
    )
    embed.add_field(name="anime",
        value=
            "`animetop` `mangatop` `maluser` `anime` `manga`",
        inline=False
        )
    embed.add_field(name="utility",
        value=
            "`command` `example` `math` `translate` `userinfo` `choose` `youtube`  `avatar` `avatarserver` "+
            "`server` `roll` `spotify` `nickname` `addrole` `createrole` `removerole` `kick` `link` `unlink` "+
            "`ban` `unban` `activity` `countdown` `prefix` `qrcode`",
        inline=False
    )
    embed.add_field(name='pokemon',
        value=
            '`pokedex` `evostone` `region` `pokemoncount` `stats` `compare` `move` `items` `abilities` ' +
            '`location` `league`'
    )
            
    embed.set_footer(text = "Yohane ~ sama command list")
    embed.set_author(name = "yohane ~ sama",
        icon_url = f"https://cdn.discordapp.com/attachments/702845878746087505/771349042818711592/d5dd6ae45aa41c4ebe78f8b531787c80.png")
    await ctx.send(embed = embed)

#command help for each category
@client.command()
async def command(ctx, *, category : str):
    if category == "fun":
        embed = discord.Embed(colour = 0x2f64ad)

        embed.add_field(
            name="help for fun command",
            value=
                "`ask` : ask me something and i wil answer it"+
                "\n`repeat` : repeat anything that you say"+
                "\n`slap` : slap someone"+
                "\n`ping` : check my connection"+
                "\n`punch` : punch someone"+
                "\n`hug` : hug someone"+
                "\n`waifurate` : rate your waifu"+
                "\n`f` : give respect"+
                "\n`meme` : get some memes"+
                "\n`random` : get random image"+
                "\n`image` : search an image"+
                "\n`reddit` : get something from reddit",
            inline=False
            )
        embed.set_footer(text = "fun commands")
        embed.set_author(name = "yohane ~ sama",
            icon_url = f"https://cdn.discordapp.com/attachments/702845878746087505/771349042818711592/d5dd6ae45aa41c4ebe78f8b531787c80.png")
        await ctx.send(embed = embed)

    elif category == "anime":
        embed = discord.Embed(colour = 0x2f64ad)

        embed.add_field(
            name="help for anime command",
            value=
                "`anime` : get anime information"+
                "\n`manga` : get manga information (doujin not include)"+
                "\n`animetop` : get information about top 5 anime on myanimelist"+
                "\n`mangatop` : get information about top 5 manga on myanimelist"+
                "\n`maluser` : get myanimelist user information",
            inline=False
        )
        embed.set_footer(text = "anime commands")
        embed.set_author(name = "yohane ~ sama",
            icon_url = f"https://cdn.discordapp.com/attachments/702845878746087505/771349042818711592/d5dd6ae45aa41c4ebe78f8b531787c80.png")
        await ctx.send(embed = embed)

    elif category == "utility":
        embed = discord.Embed(colour = 0x2f64ad)

        embed.add_field(
            name="help for Utility command",
            value=
                "`command` : show help for each category"+
                "\n`example` : show command example"+
                "\n`math` : doing some simple math"+
                "\n`translate` : translate your message"+
                "\n`choose` : choosing you choices"+
                "\n`roll` : roll a dice"+
                "\n`avatar` : get user avatar"+
                "\n`avatarserver` : get server icon"+
                "\n`server` : get server information"+
                "\n`youtube` : get channel information"+
                "\n`spotify` : check user spotify activity, only work if the user playing music on spotify"+
                "\n`userinfo` : get user information"+
                "\n`nickname` : change someone nickname"+
                "\n`createrole` : create role and add role to someone"+
                "\n`addrole` : add role to someone"+
                "\n`removerole` : remove role from someone"+
                "\n`kick` : kick someone from the server"+
                "\n`ban` : banned someone from the server"+
                "\n`unban` : unban someone from the server"+
                "\n`activity` : check user activity"+
                "\n`countdown` : start countdown"+
                "\n`prefix` : change server prefix"+
                "\n`qrcode` : generate qrcode",
            inline=False
        )
        embed.set_footer(text = "utility commands")
        embed.set_author(name = "yohane ~ sama",
            icon_url = f"https://cdn.discordapp.com/attachments/702845878746087505/771349042818711592/d5dd6ae45aa41c4ebe78f8b531787c80.png")
        await ctx.send(embed = embed)
    else:
        raise commands.CommandError

@command.error
async def command_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send('category not found')

#youtube command
@client.command()
async def youtube(ctx, idyt : str=None):
    data = await yt_list(id=ctx.author.id)
    if idyt:
        try:
            response = youtube1.channels().list(
                part = 'snippet,statistics',
                id = idyt
            )

            result = response.execute()

            embed = discord.Embed(titel = "youtube", colour = 0x2f64ad)
            embed.add_field(name = "subscriberCount", value=f"{result['items'][0]['statistics']['subscriberCount']}", inline=False)
            embed.add_field(name = "view count", value=f"{result['items'][0]['statistics']['viewCount']}", inline=False)
            embed.add_field(name = "videoCount", value=f"{result['items'][0]['statistics']['videoCount']}", inline=False)
            embed.set_thumbnail(url= f"{result['items'][0]['snippet']['thumbnails']['default']['url']}")
            embed.set_footer(text=f"request by : {ctx.author}")
            embed.set_author(name = f"{result['items'][0]['snippet']['title']}",
                icon_url = f"{result['items'][0]['snippet']['thumbnails']['default']['url']}")

            await ctx.send(embed = embed)
        except KeyError:
            await ctx.send("invalid channel id or maybe you type channel id wrong")
    else:
        try:
            response = youtube1.channels().list(
                part = 'snippet,statistics',
                id = data
            )

            result = response.execute()

            embed = discord.Embed(titel = "youtube", colour = 0x2f64ad)
            embed.add_field(name = "subscriberCount", value=f"{result['items'][0]['statistics']['subscriberCount']}", inline=False)
            embed.add_field(name = "view count", value=f"{result['items'][0]['statistics']['viewCount']}", inline=False)
            embed.add_field(name = "videoCount", value=f"{result['items'][0]['statistics']['videoCount']}", inline=False)
            embed.set_thumbnail(url= f"{result['items'][0]['snippet']['thumbnails']['default']['url']}")
            embed.set_footer(text=f"request by : {ctx.author}")
            embed.set_author(name = f"{result['items'][0]['snippet']['title']}",
                icon_url = f"{result['items'][0]['snippet']['thumbnails']['default']['url']}")

            await ctx.send(embed = embed)
        except KeyError:
            i = await serv_prefix(g_id=ctx.guild.id)
            await ctx.send(f"invalid channel id or maybe you haven't linked your channel id use `{i}link yt (your channel id)`")

@youtube.error
async def yt_error(ctx, error):
    i= await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'`{i}youtube (channel id)`')

#chang status every minute
@tasks.loop(minutes=1)
async def change_status():
    zactivity = discord.Activity(type=discord.ActivityType.watching, name=next(status))
    sats = discord.Status.idle
    await client.change_presence(status=sats,activity=zactivity)

@client.event
async def on_command_error(ctx, error):
    i = await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'command not found\nuse `{i}help` to see all commands', delete_after=15)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("you don't have permission to use this commands" )

#when someone join server
@client.event
async def on_member_join(member):
    print(f"{member} has joined the server")
    await member.send(f"wellcome to the server **{member}**")

#someone leave the server
@client.event
async def on_member_remove(member):
    print(f"{member} has left the server")
    await member.send(f"Bye **{member}**")

#get user avatar
@client.command()
async def avatar(ctx , member : discord.Member = None):
    member = member or ctx.author

    if 'server' in str(member):
        print('lol')

    _title = [" use this for some reason",
        " look at this trash",
        " what an cool image",
        " what is this",]
    __title = rand.choice(_title)

    embed = discord.Embed(
        description = f"{member.mention}" + __title,
        colour = 0x2f64ad
    )
    embed.set_image(
        url="{}".format(member.avatar_url)
    )
    embed.set_footer(
        text=
            "request by : {}".format(ctx.author),
            icon_url="{}".format(ctx.author.avatar_url)
    )

    await ctx.send(embed = embed)

@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send('user not found')

#send server icon
@client.command()
async def avatarserver(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        description = 'this server use this for some reason',
        colour = 0x2f64ad
    )
    embed.set_image(url=guild.icon_url)
    embed.set_footer(
        text='request by : {}'.format(ctx.author),
        icon_url=ctx.author.avatar_url
    )

    await ctx.send(embed=embed)

#get server information
@client.command()
async def server(ctx):
    guild = ctx.guild
    name_server = guild.name
    icon_server = guild.icon_url
    create_server = guild.created_at
    owner_server = guild.owner.name
    total_member_server = guild.member_count
    guild_id = guild.id
    desc = guild.description
    owner_id = guild.owner_id
    region = guild.region
    max_member = guild.max_members
    verification = guild.verification_level
    drole = guild.default_role
    role = guild.roles
    emoji_limit = guild.emoji_limit
    file_limit = guild.filesize_limit
    emoji = guild.emojis
    chanel = guild.text_channels
    bitrate_limit = guild.bitrate_limit
    voice_channel = guild.voice_channels

    file_limit_size = file_limit / 1024 / 1024

    embed = discord.Embed(title = name_server, description = guild.description, colour = 0x2f64ad)
    embed.add_field(name = "server information",
        value = f"▸server name : {name_server}"+
            f"\n▸server id : {guild_id}"+
            f"\n▸server region : {region}"+
            f"\n▸server description : {desc}"+
            f"\n▸created at : {create_server}"+
            f"\n▸server owner : {owner_server}"+
            f"\n▸server owner id : {owner_id}"+
            f"\n▸total member : {total_member_server}"+
            f"\n▸max member count : {max_member}"+
            f"\n▸verification level : {verification}"+
            f"\n▸file size limit : {file_limit_size} mb"+
            f"\n▸bitrate limit : {bitrate_limit}"+
            f"\n▸default role : {drole}"+
            f"\n▸emoji limit : {emoji_limit}"+
            "\n▸roles : "+ ", ".join(map(str, role))+
            f"\n▸text channel : " + ", ".join(map(str, chanel))+
            f"\n▸voice channel : " + ", ".join(map(str, voice_channel)),
        inline = False)
    embed.set_author(name = f"Yohane ~ sama",
        icon_url = f"https://cdn.discordapp.com/attachments/702845878746087505/771349042818711592/d5dd6ae45aa41c4ebe78f8b531787c80.png")
    embed.set_thumbnail(url = guild.icon_url)
    embed.set_footer(text="request by : {}".format(ctx.author), icon_url="{}".format(ctx.author.avatar_url))

    await ctx.send(embed = embed)

#spam command
@client.command()
@commands.has_permissions(manage_messages=True)
async def spam(ctx, * ,times : int):
    if times > 69:
        await ctx.send('the maximum count of spam is 69')
    else:
        await ctx.send("send something that you want to spam")
        msg = await client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=30)

        i = 0
        while i < times:
            await ctx.send(f'{msg.content}')
            i += 1

@spam.error
async def spam_error(ctx, error):
    i = await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'`{i}spam (how much spam you want)`')
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("you don't have permission to do this")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("you don't have permission to do this")
    else:
        await ctx.send("you don't have permission to do this")

#repeat anything that user send
@client.command()
async def repeat(ctx, * , message : str):
    r_test = ['test', 'TeSt', 'tEsT', '**stop testing**']

    if 'you' and 'dumb' in  message.split():
        await ctx.send('**NO U**')
    elif 'im' and 'dumb' in message.split():
        await ctx.send('we know')
    elif 'gay' in message.split():
        await ctx.send('we know')
    elif 'broken'and 'bot' in message.split():
        await ctx.send("**NO U**")
    elif 'yoshiko' in message.split():
        await ctx.send('**YOHANE**')
    elif 'test'or 'Test'or 'tEst'or 'teSt'or 'tesT'or 'TeSt'or 'tEsT'or'TEST'or 'teST'or 'TEst' in message.split():
        await ctx.send(rand.choice(r_test))
    else:
        await ctx.send(message)

@repeat.error
async def repeat_error(ctx, error):
    i = await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.CommandError):
        await ctx.send(f'`{i}repeat (say something here)`')

#slap someone trough the internet
@client.command()
async def slap(ctx,* , nama : discord.Member=None):
    nama = nama or ctx.author
    slap = ["https://i.imgur.com/Kx9hgVl.gif",
            "https://i.imgur.com/Fo7S7tk.gif",
            "https://i.imgur.com/Z5klLFr.gif",
            "https://i.imgur.com/U4WNfhk.gif"]

    if nama is ctx.author:
        embed = discord.Embed(title = "", description = ctx.author.mention + " you slap yourself",
            colour = 0x2f64ad)
        embed.set_image(url = rand.choice(slap))
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(title = "" , description = ctx.author.mention + " you slap " + 
            f"{nama.mention}",colour = 0x2f64ad)
        embed.set_image(url = rand.choice(slap))
        await ctx.send(embed = embed)

@slap.error
async def slap_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('`put someone name or tag him/her`')

#punch command for fun xd
@client.command()
async def punch(ctx, *, nama : discord.Member=None):
    nama = nama or ctx.author
    punch_list = ['','']

    if nama is ctx.author:
        embed = discord.Embed(title = "", description = ctx.author.mention + " you punch yourself",
            colour = 0x2f64ad)
        embed.set_image(url = rand.choice(punch_list))
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(title = "" , description = ctx.author.mention + " you punch " + f"{nama.mention}",
            colour = 0x2f64ad)
        embed.set_image(url = rand.choice(punch_list))
        await ctx.send(embed = embed)

@punch.error
async def punch_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('`put someone name or tag him/her`')

#response when get some message
@client.event
async def on_message(message):
    bad_word = ["nigga"]
    msg = message.content.lower()

    if any(word in msg.split() for word in bad_word):
        await message.channel.purge(limit=1)
        await message.channel.send("bad word detected", delete_after = 5)

    if not message.author.bot:
        if msg == "hi":
            channel = message.channel
            await channel.send(f'{message.author.mention} Hi')
        elif msg == 'hallo':
            channel = message.channel
            await channel.send('hallo')
        elif msg == 'nani':
            channel = message.channel
            await channel.send(":question:")
        elif msg == 'bye':
            channel = message.channel
            await channel.send("cya")
        elif 'broken bot' in msg.split():
            channel = message.channel
            await channel.send('**NO U**')
        elif message.content.lower() == 'f':
            channel = message.channel
            await channel.send('F')
        elif client.user.mention in message.content.split():
            channel = message.channel
            await channel.send("did u call me")
        elif message.content.lower() == "test":
            channel = message.channel
            mess = await channel.send("tested", delete_after=5)
            await asyncio.sleep(1)
            await mess.add_reaction('👍')
    await client.process_commands(message)

#chech bot latency
@client.command()
async def ping(ctx):
    await ctx.send(f'lol {round( client.latency * 1000)} ms')

#roll a dice
@client.command()
async def roll(ctx, dice = 0, sides = 0):
    i = await serv_prefix(g_id=ctx.guild.id)
    if dice == 0 and sides == 0:
        await ctx.send(f"`{i}roll (total dice) (dice sides)`")
    else :
        dice = [str (rand.choice(range(1, sides + 1)))
            for _ in range (dice)]
        await ctx.send(', '.join(dice))

#choose some choice
@client.command()
async def choose(ctx , *, message : str):
    result = message.split(',')
    pilih = rand.choice(result)
    await ctx.send(pilih)

@choose.error
async def choose_error(ctx, error):
    i = await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'`{i}choose (example, example2, etc.)`')

#simplae math calculation
@client.command()
async def math(ctx, a1 : float, method = "", a2 : float = None):
    i = await serv_prefix(g_id=ctx.guild.id)
    if a1 == 0.0 and method == "" and a2 == 0.0:
        await ctx.send(f"`{i}math (first number) (method) (second number)`")
    elif method == "+":
        a3 = a1 + a2
        await ctx.send(f"{a1} + {a2} = {a3}")
    elif method == "-":
        a3 = a1 - a2
        await ctx.send(f"{a1} - {a2} = {a3}")
    elif method == "/":
        a3 = a1 / a2
        await ctx.send(f"{a1} / {a2} = {a3}")
    elif method == "*":
        a3 = a1 + a2
        await ctx.send(f"{a1} * {a2} = {a3}")

@math.error
async def math_eror(ctx, error):
    i = await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.CommandError):
        await ctx.send(f"`{i}math (first number) (method) (second number)`")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"`{i}math (first number) (method) (second number)`")

#fun asking commands
@client.command()
async def ask(ctx, *, question = ""):
    i = await serv_prefix(g_id=ctx.guild.id)
    if question == "":
            await ctx.send(f'`{i}ask (question)`')

    else:
        resposes = ["It is certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Better not tell you now.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "Don't count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Outlook not so good.",
                    "Very doubtful."]
        await ctx.send(f'{rand.choice(resposes)}')

@ask.error
async def ask_error(ctx, error):
    i = await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.CommandError):
        await ctx.send(f'`{i}ask (question)`')

#get information about top anime on myanimelist
@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def animetop(ctx):

    result = mal.top('anime', page=1)

    embed = discord.Embed(colour = 0x2f64ad)
    embed.add_field(
        name=f"1.{result['top'][0]['title']}",
        value=
            f"▸type : {result['top'][0]['type']}"+
            f"\n▸score : {result['top'][0]['score']}"+
            f"\n▸episodes : {result['top'][0]['episodes']}"+
            f"\n▸Aired : {result['top'][0]['start_date']} to {result['top'][0]['end_date']}"+
            f"\n▸mal page : {result['top'][0]['url']}",
        inline=False
    )
    embed.add_field(
        name=f"2.{result['top'][1]['title']}",
        value=
            f"▸type : {result['top'][1]['type']}"+
            f"\n▸score : {result['top'][1]['score']}"+
            f"\n▸episodes : {result['top'][1]['episodes']}"+
            f"\n▸Aired : {result['top'][1]['start_date']} to {result['top'][1]['end_date']}"+
            f"\n▸mal page : {result['top'][1]['url']}",
        inline=False
    )
    embed.add_field(
        name=f"3.{result['top'][2]['title']}",
        value=
            f"▸type : {result['top'][2]['type']}"+
            f"\n▸score : {result['top'][2]['score']}"+
            f"\n▸episodes : {result['top'][2]['episodes']}"+
            f"\n▸Aired : {result['top'][2]['start_date']} to {result['top'][2]['end_date']}"+
            f"\n▸mal page : {result['top'][2]['url']}",
        inline=False
    )
    embed.add_field(
        name=f"4.{result['top'][3]['title']}",
        value=
            f"▸type : {result['top'][3]['type']}"+
            f"\n▸score : {result['top'][3]['score']}"+
            f"\n▸episodes : {result['top'][3]['episodes']}"+
            f"\n▸Aired : {result['top'][3]['start_date']} to {result['top'][3]['end_date']}"+
            f"\n▸mal page : {result['top'][3]['url']}",
        inline=False
    )
    embed.add_field(
        name=f"5.{result['top'][4]['title']}",
        value=
            f"▸type : {result['top'][4]['type']}"+
            f"\n▸score : {result['top'][4]['score']}"+
            f"\n▸episodes : {result['top'][4]['episodes']}"+
            f"\n▸Aired : {result['top'][4]['start_date']} to {result['top'][4]['end_date']}"+
            f"\n▸mal page : {result['top'][4]['url']}",
        inline=False
    )
    embed.set_footer(
        text="based on myanimelist.net",
        icon_url="https://upload.wikimedia.org/wikipedia/commons/7/7a/MyAnimeList_Logo.png"
    )
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/7/7a/MyAnimeList_Logo.png")

    await ctx.send(embed=embed)

@animetop.error
async def animetop_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'You are on cooldown. Try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg, delete_after=error.retry_after)
    else:
        i = await serv_prefix(g_id=ctx.guild.id)
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name="command detail",
            value=
                "to get top reted anime information",
            inline=False
        )
        embed.add_field(
            name="command example",
            value=
               f"just type `{i}animetop`",
            inline=False
        )
        embed.set_image(url=
            "https://cdn.discordapp.com/attachments/779219469650231346/779235681661616148/unknown.png")

        await ctx.send(embed=embed)

#get information about top manga onmyanimelist
@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def mangatop(ctx):

    result = mal.top('manga')

    embed = discord.Embed(colour = 0x2f64ad)
    embed.add_field(
        name=f"1.{result['top'][0]['title']}",
        value=
            f"▸type : {result['top'][0]['type']}"+
            f"\n▸score : {result['top'][0]['score']}"+
            f"\n▸volumes : {result['top'][0]['volumes']}"+
            f"\n▸Aired : {result['top'][0]['start_date']} to {result['top'][0]['end_date']}"+
            f"\n▸mal page : {result['top'][0]['url']}",
        inline=False
    )
    embed.add_field(
        name=f"2.{result['top'][1]['title']}",
        value=
            f"▸type : {result['top'][1]['type']}"+
            f"\n▸score : {result['top'][1]['score']}"+
            f"\n▸volumes : {result['top'][1]['volumes']}"+
            f"\n▸Aired : {result['top'][1]['start_date']} to {result['top'][1]['end_date']}"+
            f"\n▸mal page : {result['top'][1]['url']}",
        inline=False
    )
    embed.add_field(
        name=f"3.{result['top'][2]['title']}",
        value=
            f"▸type : {result['top'][2]['type']}"+
            f"\n▸score : {result['top'][2]['score']}"+
            f"\n▸volumes : {result['top'][2]['volumes']}"+
            f"\n▸Aired : {result['top'][2]['start_date']} to {result['top'][2]['end_date']}"+
            f"\n▸mal page : {result['top'][2]['url']}",
        inline=False
    )
    embed.add_field(
        name=f"4.{result['top'][3]['title']}",
        value=
            f"▸type : {result['top'][3]['type']}"+
            f"\n▸score : {result['top'][3]['score']}"+
            f"\n▸volumes : {result['top'][3]['volumes']}"+
            f"\n▸Aired : {result['top'][3]['start_date']} to {result['top'][3]['end_date']}"+
            f"\n▸mal page : {result['top'][3]['url']}",
        inline=False
    )
    embed.add_field(
        name=f"5.{result['top'][4]['title']}",
        value=
            f"▸type : {result['top'][4]['type']}"+
            f"\n▸score : {result['top'][4]['score']}"+
            f"\n▸volumes : {result['top'][4]['volumes']}"+
            f"\n▸Aired : {result['top'][4]['start_date']} to {result['top'][4]['end_date']}"+
            f"\n▸mal page : {result['top'][4]['url']}",
        inline=False
    )
    embed.set_footer(
        text="based on myanimelist.net",
        icon_url="https://upload.wikimedia.org/wikipedia/commons/7/7a/MyAnimeList_Logo.png"
    )
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/7/7a/MyAnimeList_Logo.png")

    await ctx.send(embed = embed)

@mangatop.error
async def mangatop_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'You are on cooldown. Try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg, delete_after=error.retry_after)
    else:
        i = await serv_prefix(g_id=ctx.guild.id)
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name="command detail",
            value=
                "to get top reted manga information",
            inline=False
        )
        embed.add_field(
            name="command example",
            value=
                f"just type `{i}mangatop`",
            inline=False
        )
        embed.set_image(url=
            "https://cdn.discordapp.com/attachments/779219469650231346/779235681661616148/unknown.png")

        await ctx.send(embed=embed)

#get mal user information
@client.command()
async def maluser(ctx,* , user : str=None):
    data = await mal_list(id=ctx.author.id)
    if user:
        result = mal.user(username=user)

        embed = discord.Embed(colour = 0x2f64ad)
        embed.set_thumbnail(url=f"{result['image_url']}")
        embed.set_author(name=f"{result['username']} profile on Myanimelist", icon_url=f"{result['image_url']}")
        embed.add_field(name="profile",
            value=
                f"▸username : {result['username']}"+
                f"\n▸user id : {result['user_id']}"+
                f"\n▸gender : {result['gender']}"+
                f"\n▸birthday : {result['birthday']}"+
                f"\n▸location : {result['location']}"+
                f"\n▸joined at : {result['joined']}"+
                f"\n▸last online : {result['last_online']}",
            inline=False
            )
        embed.add_field(name="anime stats",
            value=
                f"▸days watched : {result['anime_stats']['days_watched']}"+
                f"\n▸average score : {result['anime_stats']['mean_score']}"+
                f"\n▸curently watching : {result['anime_stats']['watching']}"+
                f"\n▸completed : {result['anime_stats']['completed']}"+
                f"\n▸on hold : {result['anime_stats']['on_hold']}"+
                f"\n▸plan to watch : {result['anime_stats']['plan_to_watch']}"+
                f"\n▸rewatched : {result['anime_stats']['rewatched']}"+
                f"\n▸total episode watched : {result['anime_stats']['episodes_watched']}"
            )
        embed.add_field(name=f"manga stats",
            value=
                f"▸days read : {result['manga_stats']['days_read']}"+
                f"\n▸average score : {result['manga_stats']['mean_score']}"+
                f"\n▸curently reading : {result['manga_stats']['reading']}"+
                f"\n▸completed : {result['manga_stats']['completed']}"+
                f"\n▸on hold : {result['manga_stats']['on_hold']}",
            inline=False
            )
        embed.set_footer(text=f"request by : {ctx.author}",
            icon_url=f"{ctx.author.avatar_url}")

        await ctx.send(embed = embed)
    else:
        result = mal.user(username=data)

        embed = discord.Embed(colour = 0x2f64ad)
        embed.set_thumbnail(url=f"{result['image_url']}")
        embed.set_author(name=f"{result['username']} profile on Myanimelist", icon_url=f"{result['image_url']}")
        embed.add_field(name="profile",
            value=
                f"▸username : {result['username']}"+
                f"\n▸user id : {result['user_id']}"+
                f"\n▸gender : {result['gender']}"+
                f"\n▸birthday : {result['birthday']}"+
                f"\n▸location : {result['location']}"+
                f"\n▸joined at : {result['joined']}"+
                f"\n▸last online : {result['last_online']}",
            inline=False
            )
        embed.add_field(name="anime stats",
            value=
                f"▸days watched : {result['anime_stats']['days_watched']}"+
                f"\n▸average score : {result['anime_stats']['mean_score']}"+
                f"\n▸curently watching : {result['anime_stats']['watching']}"+
                f"\n▸completed : {result['anime_stats']['completed']}"+
                f"\n▸on hold : {result['anime_stats']['on_hold']}"+
                f"\n▸plan to watch : {result['anime_stats']['plan_to_watch']}"+
                f"\n▸rewatched : {result['anime_stats']['rewatched']}"+
                f"\n▸total episode watched : {result['anime_stats']['episodes_watched']}"
            )
        embed.add_field(name=f"manga stats",
            value=
                f"▸days read : {result['manga_stats']['days_read']}"+
                f"\n▸average score : {result['manga_stats']['mean_score']}"+
                f"\n▸curently reading : {result['manga_stats']['reading']}"+
                f"\n▸completed : {result['manga_stats']['completed']}"+
                f"\n▸on hold : {result['manga_stats']['on_hold']}",
            inline=False
            )
        embed.set_footer(text=f"request by : {ctx.author}",
            icon_url=f"{ctx.author.avatar_url}")

        await ctx.send(embed = embed)

@maluser.error
async def maluser_error(ctx, error):
    i = await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'`{i}maluser (username)`')
    else:
        await ctx.send('user not found')

#get anime information
@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def anime(ctx, *, anime : str):
    result = mal.search('anime', query=anime)

    embe = discord.Embed(colour = 0x2f64ad)
    embe.set_author(name=f'Result for {anime}')
    embe.add_field(name='Anime detail',
        value=
            f"▸anime name : {result['results'][0]['title']}"+
            f"\n▸type : {result['results'][0]['type']}"+
            f"\n▸episodes : {result['results'][0]['episodes']}"+
            f"\n▸score : {result['results'][0]['score']}"+
            f"\n▸rated : {result['results'][0]['rated']}"+
            f"\n▸mal id : {result['results'][0]['mal_id']}"+
            f"\n▸mal page : {result['results'][0]['url']}",
        inline=False
        )
    embe.add_field(name='synopsis',
        value=
            f"{result['results'][0]['synopsis']}",
        inline=False
        )
    embe.set_thumbnail(url=f"{result['results'][0]['image_url']}")
    embe.set_footer(text=f"request by : {ctx.author}", icon_url=f"{ctx.author.avatar_url}")

    await ctx.send(embed = embe)

@anime.error
async def anime_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'You are on cooldown. Try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg, delete_after=error.retry_after)
    elif isinstance(error, commands.MissingRequiredArgument):
        i = await serv_prefix(g_id=ctx.guild.id)
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name="command detail",
            value=
                "to get anime information",
            inline=False
        )
        embed.add_field(
            name="command example",
            value=
                f"`{i}anime (anime name)`",
            inline=False
        )
        embed.set_image(url=
            "https://cdn.discordapp.com/attachments/779219469650231346/779235537067311104/unknown.png")

        await ctx.send(embed=embed)
    else:
        await ctx.send('anime not found or maybe you type the anime title wrong')

#get information about manga
@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def manga(ctx, *, anime : str):
    result = mal.search('manga', query=anime)

    embe = discord.Embed(colour = 0x2f64ad)
    embe.set_author(name=f'Result for {anime}')
    embe.add_field(name='Manga detail',
        value=
            f"▸manga name : {result['results'][0]['title']}"+
            f"\n▸type : {result['results'][0]['type']}"+
            f"\n▸total chapter : {result['results'][0]['chapters']}"+
            f"\n▸total volume : {result['results'][0]['volumes']}"+
            f"\n▸score : {result['results'][0]['score']}"+
            f"\n▸mal id : {result['results'][0]['mal_id']}"+
            f"\n▸mal page : {result['results'][0]['url']}",
        inline=False
        )
    embe.add_field(name='synopsis',
        value=
            f"{result['results'][0]['synopsis']}",
        inline=False
        )
    embe.set_thumbnail(url=f"{result['results'][0]['image_url']}")
    embe.set_footer(text=f"request by : {ctx.author}", icon_url=f"{ctx.author.avatar_url}")

    await ctx.send(embed = embe)

@manga.error
async def manga_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'You are on cooldown. Try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg, delete_after=error.retry_after)
    elif isinstance(error, commands.MissingRequiredArgument):
        i = await serv_prefix(g_id=ctx.guild.id)
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name="command detail",
            value=
                "to get manga information",
            inline=False
        )
        embed.add_field(
            name="command example",
            value=
                f"`{i}manga (manga name)`",
            inline=False
        )
        embed.set_image(url=
            "https://cdn.discordapp.com/attachments/779219469650231346/779236001109245952/unknown.png")

        await ctx.send(embed=embed)
    else:
        await ctx.send('manga not found or maybe you type the manga title wrong')

#rate your waifu lol
@client.command()
async def waifurate(ctx, *, waifu : str):
    check : str = waifu.lower()

    if 'yohane' in waifu.lower():
        await ctx.send('**10/10**')
    elif 'jojo' in waifu.lower():
        await ctx.send('**100/10**')
    elif 'speedwagon' in check.split():
        await ctx.send("error can't give rating because speedwagon was the best waifu")
    elif 'kakyoin' in waifu.split():
        await ctx.send('kakyoin...')
    elif "@" in list(waifu):
        await ctx.send('are you gay?')
    else:
        await ctx.send(f'i give your waifu rate : {rand.randrange(4,11)}/10')

@waifurate.error
async def waifurate_error(ctx, error):
    i = await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'`{i}waifurate (you waifu name here)`')
    else:
        await ctx.send(f'`{i}waifurete (your waifu name here)`')

#get user information command
@client.command()
async def userinfo(ctx, member : discord.Member = None):
    name = member or ctx.author
    display_name = name.display_name
    avatar = name.avatar_url
    join_at = name.created_at
    uid = name.id
    statuss = name.status

    embed = discord.Embed(colour = 0x2f64ad)
    embed.add_field(
        name="user info",
        value=
            "username : {}".format(name)+
            "\ndisplay name : {}".format(display_name)+
            "\nid : {}".format(uid)+
            "\nstatus : {}".format(statuss)+
            "\njoin discord on : {}".format(join_at),
        inline=False
    )
    embed.set_thumbnail(url="{}".format(avatar))
    embed.set_footer(text='request by : {}'.format(ctx.author), icon_url='{}'.format(ctx.author.avatar_url))

    await ctx.send(embed = embed)

@userinfo.error
async def userinfo_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("please specify user by tag him/her")

#hug someone
@client.command()
async def hug(ctx, user : discord.Member=None):
    user = user or ctx.author
    chose = ["https://i.imgur.com/b9vyEPL.gif",
        "https://cdn.weeb.sh/images/SknauOQwb.gif",
        "https://cdn.weeb.sh/images/SJByY_QwW.gif",
        "https://cdn.weeb.sh/images/BkotddXD-.gif",
        "https://cdn.weeb.sh/images/ryjJFdmvb.gif",
        "https://cdn.weeb.sh/images/BJF5_uXvZ.gif",
        "https://cdn.weeb.sh/images/BysjuO7D-.gif",
        "https://cdn.weeb.sh/images/ByuHsvu8z.gif",
        "https://cdn.weeb.sh/images/SJfEks3Rb.gif",
        "https://cdn.weeb.sh/images/BJ0UovdUM.gif",
        "https://cdn.weeb.sh/images/Hk3ox0tYW.gif",
        "https://cdn.weeb.sh/images/r1bAksn0W.gif",
        "https://cdn.weeb.sh/images/SywetdQvZ.gif",
        "https://cdn.weeb.sh/images/HkRwnuyuW.gif",
        "https://cdn.weeb.sh/images/HkQs_dXPZ.gif",
        "https://cdn.weeb.sh/images/rJ_slRYFZ.gif",
        "https://i.imgur.com/o8aa5Dl.gif"]
    if user is ctx.author:
        embed = discord.Embed(title = "", description = ctx.author.mention + " hug yourself huh?",
            colour = 0x2f64ad)
        embed.set_image(url = rand.choice(chose))
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(title = "" , description = ctx.author.mention + " you hug " + f"{user.mention}",
            colour = 0x2f64ad)
        embed.set_image(url = rand.choice(chose))
        await ctx.send(embed = embed)

@hug.error
async def hug_error(ctx, error):
    if isinstance(error, commands.missingRequiredArgument):
        await ctx.send("plese specify user by tag him/her")

#change user nickname
@client.command(pass_context=True)
async def nickname(ctx, member : discord.Member, *, name : str):
    if member.id is ctx.guild.owner_id:
        await ctx.send('you cannot change server owner nickname')
    elif member.id == 570972163058958336:
        if ctx.author.id == 570972163058958336:
            if name == 'reset':
                users : discord.User = member
                original_name = users.name
                await member.edit(nick=original_name)
                await ctx.send("{} nickname was back to normal".format(member.mention))
            else:
                await member.edit(nick=name)
                await ctx.send("nickname was change for {}".format(member.mention))
        else:
            raise commands.BadArgument
    elif name == 'reset':
        users : discord.User = member
        original_name = users.name
        await member.edit(nick=original_name)
        await ctx.send("{} nickname was back to normal".format(member.mention))
    else:
        await member.edit(nick=name)
        await ctx.send("nickname was change for {}".format(member.mention))

@nickname.error
async def nickname_error(ctx, error):
    i = await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"`{i}nickname (tag a user) (new nickname)`")
    else:
        await ctx.send("you don't have permission to change this user nickname")

#f command
@client.command()
async def f(ctx, *, reason : str = ""):
    if reason == "":
        await ctx.send("{} need respect".format(ctx.author.mention))
        await ctx.send(":regional_indicator_f:")
    else:
        await ctx.send(f"{ctx.author.mention} need respect\nreason : {reason}")
        await ctx.send(":regional_indicator_f:")

@f.error
async def f_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send("f")
    else:
        await ctx.send("f")

#make and add role to someone
@client.command()
@commands.has_permissions(manage_roles = True)
async def createrole(ctx, user : discord.Member, *,role_name : str):
    guild = ctx.guild
    await guild.create_role(name = "{}".format(role_name))
    roles = discord.utils.get(ctx.guild.roles, name= role_name)
    await user.add_roles(roles)
    await ctx.send(f"{role_name} has been created and give it to {user.mention}")

@createrole.error
async def createrole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        i = await serv_prefix(g_id=ctx.guild.id)
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(name="example",
            value=
                f"{i}createrole (tag a user here) (role name)"+
                f"\n{i}createrole @who example "
            )
        await ctx.send(embed = embed)

#add role to someone
@client.command()
@commands.has_permissions(manage_roles = True)
async def addrole(ctx, user : discord.Member, *,role_name : str):
    roles = discord.utils.get(ctx.guild.roles, name= role_name)
    await user.add_roles(roles)
    await ctx.send(f"{user.mention} get a role {role_name}")

@addrole.error
async def addrole_error(ctx, error):
    i = await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(name="example",
            value=
                f"{i}addrole (tag a user here) (role name)"+
                f"\n{i}addrole @who example "
            )
        await ctx.send(embed = embed)

#remove role from someone
@client.command()
@commands.has_permissions(manage_roles = True)
async def removerole(ctx, user : discord.Member, *,role_name : str):
    roles = discord.utils.get(ctx.guild.roles, name= role_name)
    await user.remove_roles(roles)
    await ctx.send(f"{role_name} has been removed from {user.mention}")

@removerole.error
async def removerole_error(ctx, error):
    i = await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(name="example",
            value=
                f"{i}removerole (tag a user here) (role name)"+
                f"\n{i}removerole @who example "
            )
        await ctx.send(embed = embed)

#kick someone from server
@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.Member, *,reason : str):
    await user.kick(reason=reason)
    await ctx.send(f"**{user.mention}** has been kicked because {reason}")

@kick.error
async def kick_error(ctx, error):
    i = await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(name="example",
            value=
                f"{i}kick (tag a user here) (reason why you kick the user)"+
                f"\n{i}kick @who spam to much message"
            )
        await ctx.send(embed = embed)

#ban someone
@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.Member, *, reason : str):
    await user.ban(reason=reason)
    await ctx.send(f"**{user.mention}** has been banned because {reason}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("you need to tag a user give me a reason why you kick the user")

#unban a user
@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, *,member):
    banned_list = await ctx.guild.bans()
    user_name, user_discriminator = member.split('#')

    for banned_user in banned_list:
        user = banned_user.user

        if (user.name, user.discriminator) == (user_name, user_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} unbanned, you are free now")
            return

@unban.error
async def unban_error(ctx, error):
    i = await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"input the user in the command for example `{i}unban user#1234`")

#check what user listening on spotify
@client.command()
async def spotify(ctx, user: discord.Member=None, *, method : str = None):
    user = user or ctx.author

    for activity in user.activities:
        if isinstance(activity, Spotify):
            if method.lower() == 'album cover':
                embeds = discord.Embed(description = 'album cover the user currently listening to' ,colour = 0x2f64ad)
                embeds.set_image(
                    url=f"{activity.album_cover_url}"
                )
                await ctx.send(embed = embeds)
                break

            embed = discord.Embed(colour = 0x2f64ad)
            embed.add_field(name=f"{user} is listening to",
                value=
                    f"\n▸title : **{activity.title}**"+
                    f"\n▸artist : **{activity.artist}**"+
                    f"\n▸album : **{activity.album}**"+
                    f"\n▸duration : **{activity.duration}**",
                inline=False
                )
            embed.set_thumbnail(url=f"{activity.album_cover_url}")
            await ctx.send(embed=embed)

#check user activity
@client.command()
async def activity(ctx, user : discord.Member=None):
    user = user or ctx.author

    if user.activities[0].type == ActivityType.playing:
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name=f"{user} is playing",
            value=
                f"▸game : {user.activities[0].name}"+
                f"\n▸start playing on : {user.activities[0].start}",
            )
        await ctx.send(embed = embed)

    elif user.activities[0].type == ActivityType.listening:
        if user.activities[1].type == ActivityType.playing:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    embed = discord.Embed(colour = 0x2f64ad)
                    embed.add_field(
                        name=f"playing a game",
                        value=
                            f"▸game name : {user.activities[1].name}"+
                            f"\n▸start playing on : {user.activities[1].start}",
                        inline=False
                        )
                    embed.add_field(name=f"and listening to",
                        value=
                            f"▸song title : {activity.title}"+
                            f"\n▸artist : {activity.artist}"+
                            f"\n▸album : {activity.album}"+
                            f"\n▸duration : {activity.duration}",
                        inline=False
                        )
                    await ctx.send(embed=embed)
        else:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    embed = discord.Embed(colour = 0x2f64ad)
                    embed.add_field(name=f"{user} is listening to",
                        value=
                            f"\n▸title : **{activity.title}**"+
                            f"\n▸artist : **{activity.artist}**"+
                            f"\n▸album : **{activity.album}**"+
                            f"\n▸duration : **{activity.duration}**",
                        inline=False
                        )
                    embed.set_thumbnail(url=f"{activity.album_cover_url}")
                    await ctx.send(embed=embed)
    elif user.activities[0].type == ActivityType.streaming:
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name=f"{user} is streaming",
            value=
                f"▸title : {user.activities[0].name}"+
                f"\n▸platform : {user.activities[0].platform}"+
                f"\n▸stream url : {user.activities[0].url}",
        )
        await ctx.send(embed = embed)

    else:
        await ctx.send("this user is doing nothing")

#example command
@client.command()
async def example(ctx, *, cmd_name : str = None):
    cmd_name = cmd_name or "example"
    i = await serv_prefix(g_id=ctx.guild.id)

    if cmd_name.lower() == "example":
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name="command detail",
            value=
                "This command is to see examples of how to use each command"
        )
        embed.add_field(
            name="command example",
            value=
                "example command for command `example`\n"+
                "\nto use this command : "+
                f"\n`{i}example (command name)`"+
                "\nusage example :"+
                f"\n`{i}example help`"
        )

        await ctx.send(embed=embed)

    elif cmd_name.lower() == "help":
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name="command detail",
            value=
                "This command is to see all commands that exist",
            inline=False
        )
        embed.add_field(
            name="command example",
            value=
                f"just type `{i}help`",
            inline=False
        )
        embed.set_image(url=
            "https://cdn.discordapp.com/attachments/779219469650231346/779230428438855680/unknown.png")

        await ctx.send(embed=embed)
    
    elif cmd_name.lower() == "anime":
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name="command detail",
            value=
                "to get anime information",
            inline=False
        )
        embed.add_field(
            name="command example",
            value=
                f"`{i}anime (anime name)`",
            inline=False
        )
        embed.set_image(url=
            "https://cdn.discordapp.com/attachments/779219469650231346/779235537067311104/unknown.png")

        await ctx.send(embed=embed)

    elif cmd_name.lower() == "animetop":
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name="command detail",
            value=
                "to get top reted anime information",
            inline=False
        )
        embed.add_field(
            name="command example",
            value=
                f"just type `{i}animetop`",
            inline=False
        )
        embed.set_image(url=
            "https://cdn.discordapp.com/attachments/779219469650231346/779235681661616148/unknown.png")

        await ctx.send(embed=embed)
    
    elif cmd_name.lower() == "mangatop":
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name="command detail",
            value=
                "to get top reted manga information",
            inline=False
        )
        embed.add_field(
            name="command example",
            value=
                f"just type `{i}mangatop`",
            inline=False
        )
        embed.set_image(url=
            "https://cdn.discordapp.com/attachments/779219469650231346/779235681661616148/unknown.png")

        await ctx.send(embed=embed)

    elif cmd_name.lower() == "manga":
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name="command detail",
            value=
                "to get manga information",
            inline=False
        )
        embed.add_field(
            name="command example",
            value=
                f"`{i}manga (manga name)`",
            inline=False
        )
        embed.set_image(url=
            "https://cdn.discordapp.com/attachments/779219469650231346/779236001109245952/unknown.png")

        await ctx.send(embed=embed)
    else:
        raise commands.CommandError

@example.error
async def example_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send("command not found or maybe you type it wrong")

#countdown command
@client.command(aliases=['ctd'])
async def countdown(ctx, time : int = None):
    time = time or 3

    if time > 300:
        await ctx.send("maximum countdown time is 300 seconds")

    elif time > 10:
        i = time
        while i > 0:
            while i > 5:
                await ctx.send("{} seconds to go".format(i))
                i -= 5
                await asyncio.sleep(5)

            while i <= 5 and i > 0:
                await ctx.send("{}".format(i))
                i -= 1
                await asyncio.sleep(1)
        await ctx.send("Go !!!")  

    else:
        while time > 0:
            await ctx.send("{}".format(time))
            time -= 1
            await asyncio.sleep(1)

        await ctx.send("Go !!!")

#meme commands
@client.command()
async def meme(ctx):
    result = memes()
    await ctx.send(result)

#get random image from imgur
@client.command()
async def random(ctx):
    result = imgrandom()
    await ctx.send(result)

#search some image
@client.command()
async def image(ctx, item : str):
    result = images(items=item)
    await ctx.send(result)

#get something from subreddit
@client.command()
async def reddit(ctx, items : str):
    result = subreddit(subreddit_name=items)
    await ctx.send(result)

#reload cog
@client.command()
@commands.check(is_me)
async def reload(ctx):
    msg = await ctx.send('Loading')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.unload_extension(f"cogs.{filename[:-3]}")
            await asyncio.sleep(1)
            await msg.edit(content = 'Loading.')
            client.load_extension(f"cogs.{filename[:-3]}")
            await asyncio.sleep(1)
            await msg.edit(content = 'Loading..')
            await asyncio.sleep(1)
            await msg.edit(content = 'Cog reloaded')

#unload cog
@client.command()
@commands.check(is_me)
async def unload(ctx):
    msg = await ctx.send('Loading')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.unload_extension(f"cogs.{filename[:-3]}")
    await asyncio.sleep(1)
    await msg.edit(content='Cog unloaded')

#load cog
@client.command()
@commands.check(is_me)
async def load(ctx):
    msg = await ctx.send('Loading')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f"cogs.{filename[:-3]}")
    await asyncio.sleep(1)
    await msg.edit(content='Cog loaded')

@client.command()
async def link(ctx, type : str, *, something : str):
    if type.lower() == 'yt':
        with open('yt.json', 'r') as f:
            linked = json.load(f)

        linked[str(ctx.author.id)] = something

        with open('yt.json', 'w') as f:
            json.dump(linked, f, indent=4)
    
    elif type.lower() == 'mal':
        with open('mal.json', 'r') as f:
            mal_linked = json.load(f)
        
        mal_linked[str(ctx.author.id)] = something

        with open('mal.json', 'w') as f:
            json.dump(mal_linked, f, indent=4)
    else:
        await ctx.send("linked type not found")

    await ctx.send(f'linked **{something}** to {ctx.author.mention}')

@link.error
async def link_error(ctx, error):
    i = await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{i}link (yt or mal) (channel id or myanimelist username)")

@client.command()
async def unlink(ctx, type : str):
    if type.lower() == 'yt':
        with open('yt.json', 'r') as f:
            linked = json.load(f)

        linked.pop(str(ctx.author.id))

        with open('yt.json', 'w') as f:
            json.dump(linked, f, indent=4)
    elif type.lower() == 'mal':
        with open('mal.json', 'r') as f:
            mal_linked = json.load(f)
        
        mal_linked.pop(str(ctx.author.id))

        with open('mal.json', 'w') as f:
            json.dump(mal_linked, f, indent=4)
    else:
        await ctx.send("linked type not found")

    await ctx.send(f'unlinked {type} from {ctx.author.mention}')

@unlink.error
async def unlink_error(ctx, error):
    i = await serv_prefix(g_id=ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{i}unlink (yt or mal)")

#generate qrcode
@client.command(name='qrcode')
async def _qrcode(ctx, *, data : str = None):
    img = qrcode.make(data=data)
    img.save('result.png')

    #open result file and send it
    with open('result.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)
        f.close()
    
    #remove the file after sending the result
    await asyncio.sleep(1)
    os.remove('result.png')

@_qrcode.error
async def _qrcode_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('i need a data to generate qrcode')

@client.command(name = 'pokedex')
async def _pokemon(ctx, *, name : str):
    pokemon = pokedex.get_pokemon_by_name(name)

    try:
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name = 'pokemon detail',
            value= 
                '▸Name : {}'.format(pokemon[0]['name'])+
                '\n▸Number : No.{}'.format(pokemon[0]['number'])+
                '\n▸Generation : Gen {}'.format(pokemon[0]['gen'])+
                '\n▸Species : {}'.format(pokemon[0]['species'])+
                '\n▸Types : ' + ', '.join(map(str, pokemon[0]['types']))+
                '\n▸Height : {}'.format(pokemon[0]['height'])+
                '\n▸Weight : {}'.format(pokemon[0]['weight'])+
                '\n▸Family : ' + ', '.join(map(str,pokemon[0]['family']['evolutionLine']))+
                '\n▸Evolution Stage : {}'.format(pokemon[0]['family']['evolutionStage'])+
                '\n▸Abilities : ' + ', '.join(map(str, pokemon[0]['abilities']['normal']))+
                '\n▸Hidden Abilities : '+ ', '.join(map(str, pokemon[0]['abilities']['hidden']))+
                '\n▸Egg Group : ' + ', '.join(map(str, pokemon[0]['eggGroups']))+
                '\n▸Mythical : {}'.format(pokemon[0]['mythical'])+
                '\n▸Legendary : {}'.format(pokemon[0]['legendary'])+
                '\n▸Ultra Beast : {}'.format(pokemon[0]['ultraBeast'])+
                '\n▸Description : {}'.format(pokemon[0]['description']),
            inline=False
        )

        embed.set_thumbnail(url='{}'.format(pokemon[0]['sprite']))
        embed.set_footer(text='request by : {}'.format(ctx.author),
            icon_url = '{}'.format(ctx.author.avatar_url)
            )

        await ctx.send(embed = embed)

    except:
        await ctx.send('pokemon not found or maybe you type the pokemon name wrong', delete_after = 30)

@_pokemon.error
async def _pokemon_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        ctx.send('please specify pokemon name')

@client.command(name = 'evostone')
async def _evostone(ctx, stone : str = None):
    if stone:
        try:
            evolutionstone = pokedex.get_evolution_stone(stone)
            embed = discord.Embed(colour = 0x2f64ad)
            embed.add_field(
                name='{}'.format(evolutionstone['name']),
                value=
                    '▸Also know as : {}'.format(evolutionstone['aka'])+
                    '\n▸Effect : \n-' + '\n-'.join(map(str, evolutionstone['effects']))
            )
            embed.set_thumbnail(url='{}'.format(evolutionstone['sprite']))
            embed.set_footer(
                text='request by : {}'.format(ctx.author),
                icon_url='{}'.format(ctx.author.avatar_url)
            )

            await ctx.send(embed = embed)
        except:
            await ctx.send('evolution stone not found or maybe you type it wrong', delete_after = 30)
    else:
        evolutionstone = pokedex.get_evolution_stones()
        i = await serv_prefix(g_id=ctx.guild.id)
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name='Evelution Stones',
            value=
                '▸' + '\n▸'.join(map(str, evolutionstone))
        )
        embed.add_field(
            name='for detail use',
            value=f'`{i}evostone` `evolution stone name`',
            inline=False
        )
        embed.set_footer(
            text='request by : {}'.format(ctx.author),
            icon_url='{}'.format(ctx.author.avatar_url)
        )

        await ctx.send(embed = embed)

@client.command(name = 'league')
async def _region(ctx, *, region_name : str = None):
    if region_name:
        try:
            league = pokedex.get_league(region_name)
            embed = discord.Embed(colour = 0x2f64ad)
            embed.add_field(
                name='{}'.format(league['name']),
                value=
                    '▸Region : {}'.format(league['region'])+
                    '\n▸Badges Required : {}'.format(league['badgesRequired'])+
                    '\n▸Badges : \n-' + '\n-'.join(map(str, league['badges'])),
                inline=False
            )
            embed.set_footer(
                text='request by : {}'.format(ctx.author),
                icon_url='{}'.format(ctx.author.avatar_url)
            )

            await ctx.send(embed = embed)
        except:
            await ctx.send('region not found or maybe you type it wrong')
    else:
        league = pokedex.get_leagues()
        i = await serv_prefix(g_id=ctx.guild.id)
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name='Region League List',
            value='▸' + '\n▸'.join(map(str, league)),
            inline=False
        )
        embed.add_field(
            name='To Get Detail use',
            value=f'`{i}region` `region league name`',
            inline=False
        )
        embed.set_footer(
            text='request by : {}'.format(ctx.author),
            icon_url='{}'.format(ctx.author.avatar_url)
        )

        await ctx.send(embed = embed)

@client.command(name = 'pokemoncount')
async def _pokecount(ctx):
    count = pokedex.get_pokemon_counts()
    embed = discord.Embed(colour = 0x2f64ad)
    embed.add_field(
        name='Pokemon Count',
        value=
            '▸Generation 1 : {}'.format(count['gen1'])+
            '\n▸Generation 2 : {}'.format(count['gen2'])+
            '\n▸Generation 3 : {}'.format(count['gen3'])+
            '\n▸Generation 4 : {}'.format(count['gen4'])+
            '\n▸Generation 5 : {}'.format(count['gen5'])+
            '\n▸Generation 6 : {}'.format(count['gen6'])+
            '\n▸Generation 7 : {}'.format(count['gen7'])+
            '\n▸Total : {}'.format(count['total']),
        inline=False
    )
    embed.set_footer(
        text='request by : {}'.format(ctx.author),
        icon_url='{}'.format(ctx.author.avatar_url)
    )
    await ctx.send(embed = embed)

@client.command(name = 'stats')
async def _stats(ctx, *, pname : str):
    try:
        pokemon = pypokedex.get(name = pname)
        __pokemon = pokedex.get_pokemon_by_name(pname)
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name='Pokemon Base Stats',
            value=
                '▸Pokemon Name : {}'.format(pokemon.name)+
                '\n▸Pokemon type : {}'.format(', '.join(map(str, pokemon.types)))+
                '\n▸Base exp : {}'.format(pokemon.base_experience)+
                '\n▸Abilities : ' + ', '.join(map(str, __pokemon[0]['abilities']['normal']))+
                '\n▸Hidden Abilities : '+ ', '.join(map(str, __pokemon[0]['abilities']['hidden'])),
            inline=False
        )
        embed.add_field(
            name='Battle Base Stats',
            value=
                '▸HP : {}'.format(pokemon.base_stats.hp)+
                '\n▸Attack : {}'.format(pokemon.base_stats.attack)+
                '\n▸Defense : {}'.format(pokemon.base_stats.defense)+
                '\n▸Sp Atk : {}'.format(pokemon.base_stats.sp_atk)+
                '\n▸SP Def : {}'.format(pokemon.base_stats.sp_def)+
                '\n▸Speed : {}'.format(pokemon.base_stats.speed)+
                '\n----------------------\n▸Total : {}'.format(
                    pokemon.base_stats.hp + 
                    pokemon.base_stats.attack+
                    pokemon.base_stats.defense+
                    pokemon.base_stats.sp_atk+
                    pokemon.base_stats.sp_def+
                    pokemon.base_stats.speed
                    )
        )
        embed.set_thumbnail(
            url='{}'.format(__pokemon[0]['sprite'])
        )
        embed.set_footer(
            text='request by : {}'.format(ctx.author),
            icon_url='{}'.format(ctx.author.avatar_url)
        )

        await ctx.send(embed = embed)
    except:
        await ctx.send('pokemon not found or maybe you type the pokemon name wrong', delete_after = 30)

@_stats.error
async def stats_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('please specify pokemon name')

@client.command(name = 'compare')
async def _comp(ctx, pokemon1 : str, pokemon2 : str):
    try:
        _pokemon1 = pypokedex.get(name = pokemon1)
        _pokemon2 = pypokedex.get(name = pokemon2)

        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name = f'{_pokemon1.name.capitalize()} and {_pokemon2.name.capitalize()}',
            value='Stats comparison',
            inline=False
        )
        embed.add_field(
            name='{} Stats'.format(_pokemon1.name.capitalize()),
            value=
                '▸HP : {}'.format(_pokemon1.base_stats.hp)+
                '\n▸Attack : {}'.format(_pokemon1.base_stats.attack)+
                '\n▸Defense : {}'.format(_pokemon1.base_stats.defense)+
                '\n▸Sp Atk : {}'.format(_pokemon1.base_stats.sp_atk)+
                '\n▸SP Def : {}'.format(_pokemon1.base_stats.sp_def)+
                '\n▸Speed : {}'.format(_pokemon1.base_stats.speed)+
                '\n-------------------\n▸Total : {}'.format(
                    _pokemon1.base_stats.hp + 
                    _pokemon1.base_stats.attack+
                    _pokemon1.base_stats.defense+
                    _pokemon1.base_stats.sp_atk+
                    _pokemon1.base_stats.sp_def+
                    _pokemon1.base_stats.speed
                ),
            inline=True
        )
        embed.add_field(
            name='{} Stats'.format(_pokemon2.name.capitalize()),
            value=
                '▸HP : {}'.format(_pokemon2.base_stats.hp)+
                '\n▸Attack : {}'.format(_pokemon2.base_stats.attack)+
                '\n▸Defense : {}'.format(_pokemon2.base_stats.defense)+
                '\n▸Sp Atk : {}'.format(_pokemon2.base_stats.sp_atk)+
                '\n▸SP Def : {}'.format(_pokemon2.base_stats.sp_def)+
                '\n▸Speed : {}'.format(_pokemon2.base_stats.speed)+
                '\n-------------------\n▸Total : {}'.format(
                    _pokemon2.base_stats.hp + 
                    _pokemon2.base_stats.attack+
                    _pokemon2.base_stats.defense+
                    _pokemon2.base_stats.sp_atk+
                    _pokemon2.base_stats.sp_def+
                    _pokemon2.base_stats.speed
                ),
            inline=True
        )
        embed.set_footer(
            text='request by : {}'.format(ctx.author),
            icon_url='{}'.format(ctx.author.avatar_url)
        )

        await ctx.send(embed=embed)
    except:
        await ctx.send('pokemon not found or maybe you type it wrong')

@_comp.error
async def comp_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('please specify pokemon name')

@client.command()
async def move(ctx, *, movename : str):
    try:
        movename = movename.replace(' ', '-')
        moves = pokebase.move(movename)
        move_desc = moves.effect_entries[0].short_effect.split()
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name='Move Detail',
            value=
                '▸Move Name : {}'.format(moves.name.replace('-', ' ').capitalize())+
                '\n▸Accuracy : {}'.format(moves.accuracy)+
                '\n▸Power : {}'.format(moves.power)+
                '\n▸Pp : {}'.format(moves.pp)+
                '\n▸Move Type : {}'.format(moves.type.name)+
                '\n▸Target : {}'.format(moves.target.name.replace('-', ' ').capitalize())+
                '\n▸Description : {}'.format(moves.effect_entries[0].short_effect.replace('$effect_chance%', '')),
            inline=False
        )
        embed.set_footer(
            text='request by : {}'.format(ctx.author),
            icon_url='{}'.format(ctx.author.avatar_url)
        )

        await ctx.send(embed=embed)
    except:
        await ctx.send('move not found or maybe you type it wrong')

@move.error
async def move_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('please specify move name')

@client.command()
async def items(ctx, *, itemName : str):
    try:
        itemss = pokebase.item(itemName.replace(' ', '-').lower())
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name='Item Detail',
            value=
                '▸Item Name : {}'.format(itemss.name.replace('-', ' ').capitalize())+
                '\n▸Cost : {}'.format(itemss.cost)+
                '\n▸Category : {}'.format(itemss.category.name)+
                '\n▸Description : {}'.format(itemss.flavor_text_entries[0].text),
            inline=False
        )
        embed.set_thumbnail(
            url='{}'.format(itemss.sprites.default)
        )
        embed.set_footer(
            text='request by : {}'.format(ctx.author),
            icon_url='{}'.format(ctx.author.avatar_url)
        )

        await ctx.send(embed=embed)
    except:
        await ctx.send('item not found or maye you type it wrong')

@items.error
async def _items_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('please specify items name')

@client.command()
async def abilities(ctx, *, abilitiesName : str):
    try:
        ability = pokebase.ability(abilitiesName.replace(' ', '-').lower())
        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name='Abilities Detail',
            value=
                '▸Name : {}'.format(ability.name.capitalize().replace('-', ' '))+
                '\n▸Effect : \n{}'.format(ability.effect_entries[1].effect),
            inline=False
        )
        embed.set_footer(
            text='request by : {}'.format(ctx.author),
            icon_url='{}'.format(ctx.author.avatar_url)
        )

        await ctx.send(embed=embed)
    except:
        await ctx.send('abilities not found or maybe you type it wrong')

@abilities.error
async def _abilities_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('please specify abilities name')

@client.command(name = 'location')
async def _loc(ctx, *, location : str):
    location = location.replace(' ', '-').lower()

    locations = pokebase.location(location)
    locations_area = pokebase.location_area(locations.areas[0].name)

    encounter = []
    pokemon = []

    i = 0
    while i < len(locations_area.encounter_method_rates):
        encounter.append(locations_area.encounter_method_rates[i].encounter_method.name.replace('-', ' ').capitalize())
        i += 1

    j = 0
    while j < len(locations_area.pokemon_encounters):
        pokemon.append(locations_area.pokemon_encounters[j].pokemon.name.replace('-', ' ').capitalize())
        j += 1

    embed = discord.Embed(colour = 0x2f64ad)
    embed.add_field(
        name='Location Details',
        value=
            '▸Name : {}'.format(locations.name.replace('-', ' ').capitalize())+
            '\n▸Ragion : {}'.format(locations.region.name.capitalize())+
            '\n▸Generation : {}'.format(locations.game_indices[0].generation.name.replace('-', ' ').capitalize())+
            '\n▸Pokemon encounter : ' + ', '.join(pokemon)+
            '\n▸Encounter Method : ' + ', '.join(encounter),
        inline=False
    )
    embed.set_footer(
        text='request by : {}'.format(ctx.author),
        icon_url='{}'.format(ctx.author.avatar_url)
    )

    await ctx.send(embed=embed)

@client.command(name = 'region')
async def _regions(ctx, region_ : str):
    try:
        region_ = region_.lower()
        _region = pokebase.region(region_)
        city = []
        landmarks = []
        route = []
        i = 0
        while i < len(_region.locations):
            k : str = _region.locations[i].name.replace('-', ' ').capitalize()

            if k.endswith('city'):
                city.append(f'`{k}`')
            elif k.endswith('town'):
                city.append(f'`{k}`')
            elif k.startswith(_region.name.capitalize() + ' route'):
                route.append(f'`{k}`')
            else:
                landmarks.append(f'`{k}`')

            i += 1

        embed = discord.Embed(colour = 0x2f64ad)
        embed.add_field(
            name='Region Details',
            value=
                '▸Region Name : {}'.format(_region.name.capitalize())+
                '\n▸Main Generation : {}'.format(_region.main_generation.name.replace('-', ' ').capitalize()),
            inline=False
        )
        embed.add_field(
            name='City and Town',
            value=
                ' '.join(city),
            inline=False
        )
        embed.add_field(
            name='Route',
            value=
                ' '.join(route),
            inline=False
        )
        embed.add_field(
            name='Landmarks Part 1',
            value=
                ' '.join(landmarks[:len(landmarks)//2]),
            inline=False
        )
        embed.add_field(
            name='Landmarks Part 2',
            value=
                ' '.join(landmarks[len(landmarks)//2:]),
            inline=False
        )
        embed.set_footer(
            text='request by : {}'.format(ctx.author),
            icon_url='{}'.format(ctx.author.avatar_url)
        )

        await ctx.send(embed=embed)
    except:
        await ctx.send('region not found or maybe you type it wrong')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(str(token))