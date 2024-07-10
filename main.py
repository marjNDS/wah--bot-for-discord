import discord
from discord.ext import commands
import random
import configparser
import dice

# memes: https://imgur.com/a/eATq2Lq


config = configparser.ConfigParser()
config.read('config.ini')
token = config.get('Config', 'token')

bot = commands.Bot(command_prefix=">", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Wah! I'm Online! :3")
# TODO: 1. Arrumar o print pra só printar todos os dados caso tenha 2 ou mais; 2. Dar um jeito no crit check


#######################
#    COMANDO DADOS
######################


@bot.command(pass_context=True, aliases=['r'])
async def roll(ctx, string: str):
    before, after, ops, opsTotal = await dice.strip_str(str(string))

    diceResult = await dice.dice(before, after)
    total = sum(diceResult) + opsTotal
    rollsString = await dice.dice_to_string(diceResult, after, total)

    await ctx.send(f" **{ctx.author.mention}'s rollin'! :game_die: **\n"
                   f"**Dado {before}d{after}:** \n{rollsString}{ops}\n"
                   )

    await ctx.message.delete()


@bot.command(pass_context=True, aliases=['rm'])
async def rollMultiple(ctx, times: int, string: str):
    before, after, ops, opsTotal = await dice.strip_str(str(string))
    dicesResult = await dice.dices(times, before, after)

    rollsString = []
    total = 0

    for row in dicesResult:
        total = sum(row) + opsTotal
        rollsString.append(await dice.dice_to_string(row, after, total))

    rollsString = await dice.dices_to_string(rollsString)

    await ctx.send(f" **{ctx.author.mention}'s rollin'! :game_die: **\n"
                   f"**{times} dados {before}d{after}{ops}:** \n{rollsString}\n"
                   )

    await ctx.message.delete()


#######################
#    MEMES
######################

@bot.command(aliases=['perdi', 'argumento', 'perdiargumento'])
async def meme_perdiNoArgumento(ctx):
    await ctx.send('https://i.imgur.com/NdHaAT1.jpg')


@bot.command(aliases=['mopaz'])
async def meme_moPaz(ctx):
    await ctx.send('https://i.imgur.com/dkdYXQB.png')


@bot.command(name="vove")
async def meme_voVe(ctx):
    await ctx.send('https://i.imgur.com/eKmpgjP.png')


@bot.command(aliases=['gato1', 'caradegato'])
async def meme_gato1(ctx):
    await ctx.send('https://i.imgur.com/PJVax9l.png')


@bot.command(aliases=['gato2', 'gatoseriously'])
async def meme_gato2(ctx):
    await ctx.send('https://i.imgur.com/u6dOft7.png')


@bot.command(aliases=['gato3', 'gatotriste'])
async def meme_gato3(ctx):
    await ctx.send('https://i.imgur.com/8vXl23h.png')


@bot.command(name="sully2")
async def meme_sully1(ctx):
    await ctx.send('https://i.imgur.com/52SYdv9.png')


@bot.command(aliases=['sully', 'hum'])
async def meme_sully2(ctx):
    await ctx.send('https://i.imgur.com/e5AqVnm.jpg')


@bot.command(name="poro")
async def meme_poro(ctx):
    await ctx.send('https://i.imgur.com/YiWW9bk.png')


@bot.command(aliases=['gato4', 'tom', 'numsei'])
async def meme_tom(ctx):
    await ctx.send('https://i.imgur.com/kSvktSF.png')


@bot.command(aliases=['emotional', 'emotionaldamage'])
async def meme_emotional(ctx):
    await ctx.send('https://i.imgur.com/2MfDILx.gif')


bot.run(token)
