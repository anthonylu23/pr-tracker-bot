import os
import discord
from discord.ext import commands
from config import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
from helper import *
from plot import *
from rank import *
import emoji

cred = credentials.Certificate(firebase_config)
databaseApp = firebase_admin.initialize_app(cred, {
    'databaseURL' : databaseURL
})

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

ref = db.reference(f"/")

@bot.event
async def on_ready():
    print('Hello! Tracker bot is ready')
    #channel = bot.get_channel(channel_id)
    #await channel.send('Hello! Tracker bot is ready')

@bot.command(pass_context = True) #command to update user's max bench
async def addBench(ctx, num):
    user = str(ctx.message.author.id)
    server = str(ctx.message.guild.id)
    temp = ref.get()
    if temp is None:
        createServer(server)
    elif server not in temp:
        createServer(server)
    prev = ref.child(server)
    prev = prev.get()
    date = datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')
    if prev is None:
        addNewUser(user, server)
    elif user not in prev:
        addNewUser(user, server)
    servRef = ref.child(server)
    userRef = servRef.child(user)
    temp = userRef.get()
    if temp is None:
        userRef.update({
            "bench" : {}
        })
    elif "bench" not in temp:
        userRef.update({
            "bench" : {}
        })
    childRef = userRef.child("bench")
    num = str(num)
    childRef.update({
        date : num
    })
    childRef.update({
        "latest" : num
    })
    update_total(user, server)
    channel_id = ctx.message.channel.id
    channel = bot.get_channel(channel_id)
    await channel.send(emoji.emojize('Added!! Keep up the grind!! :flexed_biceps:'))

@bot.command(pass_context = True) #command to update user's max squat
async def addSquat(ctx, num):
    user = str(ctx.message.author.id)
    server = str(ctx.message.guild.id)
    temp = ref.get()
    if temp is None:
        createServer(server)
    elif server not in temp:
        createServer(server)
    prev = ref.child(server)
    prev = prev.get()
    date = datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')
    if prev is None:
        addNewUser(user, server)
    elif user not in prev:
        addNewUser(user, server)
    servRef = ref.child(server)
    userRef = servRef.child(user)
    temp = userRef.get()
    if temp is None:
        userRef.update({
            "squat" : {}
        })
    elif "squat" not in temp:
        userRef.update({
            "squat" : {}
        })
    childRef = userRef.child("squat")
    num = str(num)
    childRef.update({
        date : num
    })
    childRef.update({
        "latest" : num
    })
    update_total(user, server)
    channel_id = ctx.message.channel.id
    channel = bot.get_channel(channel_id)
    await channel.send(emoji.emojize('Added!! Keep up the grind!! :flexed_biceps:'))

@bot.command(pass_context = True) #command to update user's max deadlift
async def addDeadlift(ctx, num):
    user = str(ctx.message.author.id)
    server = str(ctx.message.guild.id)
    temp = ref.get()
    if temp is None:
        createServer(server)
    elif server not in temp:
        createServer(server)
    prev = ref.child(server)
    prev = prev.get()
    date = datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')
    if prev is None:
        addNewUser(user, server)
    elif user not in prev:
        addNewUser(user, server)
    servRef = ref.child(server)
    userRef = servRef.child(user)
    temp = userRef.get()
    if temp is None:
        userRef.update({
            "deadlift" : {}
        })
    elif "deadlift" not in temp:
        userRef.update({
            "deadlift" : {}
        })
    childRef = userRef.child("deadlift")
    num = str(num)
    childRef.update({
        date : num
    })
    childRef.update({
        "latest" : num
    })
    update_total(user, server)
    channel_id = ctx.message.channel.id
    channel = bot.get_channel(channel_id)
    await channel.send(emoji.emojize('Added!! Keep up the grind!! :flexed_biceps:'))

@bot.command(pass_context = True)
async def myMax(ctx):
    user = ctx.message.author.id
    server_id = ctx.message.guild.id
    channel_id = ctx.message.channel.id
    channel = bot.get_channel(channel_id)

    serverRef = ref.child(str(server_id))
    userRef = serverRef.child(str(user))
    
    if userRef is None:
        benchMax = "0"
        squatMax = "0"
        deadliftMax = "0"
        total = "0"
    else:
        if "bench" not in userRef.get():
            benchMax = "0"
        else:
            benchMax = getMax(user, server_id, "bench")
        if "squat" not in userRef.get():
            squatMax = "0"
        else:
            squatMax = getMax(user, server_id, "squat")
        if "deadlift" not in userRef.get():
            deadliftMax = "0"
        else:
            deadliftMax = getMax(user, server_id, "deadlift")
        total = str(userRef.get()["total"])

    await channel.send(
        "Here are your maxes: \nBench: " + benchMax + "\nSquat: " + squatMax + "\nDeadlift: " + deadliftMax + "\nTotal: " + total
    )

@bot.command(pass_context = True)
async def plotBench(ctx):
    user = str(ctx.message.author.id)
    server_id = str(ctx.message.guild.id)
    channel_id = ctx.message.channel.id
    channel = bot.get_channel(channel_id)
    userPlot(user, server_id, "bench")
    with open('plot.png', 'rb') as f:
        picture = discord.File(f)
    await channel.send(file=picture)
    os.remove('plot.png')

@bot.command(pass_context = True)
async def plotSquat(ctx):
    user = str(ctx.message.author.id)
    server_id = str(ctx.message.guild.id)
    channel_id = ctx.message.channel.id
    channel = bot.get_channel(channel_id)
    userPlot(user, server_id, "squat")
    with open('plot.png', 'rb') as f:
        picture = discord.File(f)
    await channel.send(file=picture)
    os.remove('plot.png')

@bot.command(pass_context = True)
async def plotDeadlift(ctx):
    user = str(ctx.message.author.id)
    server_id = str(ctx.message.guild.id)
    channel_id = ctx.message.channel.id
    channel = bot.get_channel(channel_id)
    userPlot(user, server_id, "deadlift")
    with open('plot.png', 'rb') as f:
        picture = discord.File(f)
    await channel.send(file=picture)
    os.remove('plot.png')

@bot.command(pass_context = True)
async def plotTotal(ctx):
    user = str(ctx.message.author.id)
    server_id = str(ctx.message.guild.id)
    channel_id = ctx.message.channel.id
    channel = bot.get_channel(channel_id)
    userPlotAll(user, server_id)
    with open('plot.png', 'rb') as f:
        picture = discord.File(f)
    await channel.send(file=picture)
    os.remove('plot.png')

@bot.command(pass_context = True)
async def serverPlot(ctx):
    user = str(ctx.message.author.id)
    server_id = str(ctx.message.guild.id)
    channel_id = ctx.message.channel.id
    channel = bot.get_channel(channel_id)
    serverPlotAll(server_id)
    with open('plot.png', 'rb') as f:
        picture = discord.File(f)
    await channel.send(file=picture)
    os.remove('plot.png')

@bot.command(pass_context = True)
async def rankTotal(ctx):
    user = str(ctx.message.author.id)
    server_id = str(ctx.message.guild.id)
    channel_id = ctx.message.channel.id
    channel = bot.get_channel(channel_id)
    lst = formList(server_id, "total")
    res = ""
    counter = 1
    for i in lst:
        username = bot.get_user(i[0]).display_name
        if i[0] == int(user):
            username = "**" + bot.get_user(i[0]).display_name + "**"
        res = res + str(counter) + ": " + username + " - " + str(i[1]) + "lbs\n"
        counter += 1
    await channel.send(res)

@bot.command(pass_context = True)
async def rankBench(ctx):
    user = str(ctx.message.author.id)
    server_id = str(ctx.message.guild.id)
    channel_id = ctx.message.channel.id
    channel = bot.get_channel(channel_id)
    lst = formList(server_id, "bench")
    res = ""
    counter = 1
    for i in lst:
        username = bot.get_user(i[0]).display_name
        if i[0] == int(user):
            username = "**" + bot.get_user(i[0]).display_name + "**"
        res = res + str(counter) + ": " + username + " - " + str(i[1]) + "lbs\n"
        counter += 1
    await channel.send(res)

@bot.command(pass_context = True)
async def rankSquat(ctx):
    user = str(ctx.message.author.id)
    server_id = str(ctx.message.guild.id)
    channel_id = ctx.message.channel.id
    channel = bot.get_channel(channel_id)
    lst = formList(server_id, "squat")
    res = ""
    counter = 1
    for i in lst:
        username = bot.get_user(i[0]).display_name
        if i[0] == int(user):
            username = "**" + bot.get_user(i[0]).display_name + "**"
        res = res + str(counter) + ": " + username + " - " + str(i[1]) + "lbs\n"
        counter += 1
    await channel.send(res)

@bot.command(pass_context = True)
async def rankDeadlift(ctx):
    user = str(ctx.message.author.id)
    server_id = str(ctx.message.guild.id)
    channel_id = ctx.message.channel.id
    channel = bot.get_channel(channel_id)
    lst = formList(server_id, "deadlift")
    res = ""
    counter = 1
    for i in lst:
        username = bot.get_user(i[0]).display_name
        if i[0] == int(user):
            username = "**" + bot.get_user(i[0]).display_name + "**"
        res = res + str(counter) + ": " + username + " - " + str(i[1]) + "lbs\n"
        counter += 1
    await channel.send(res)

bot.run(BOT_TOKEN)