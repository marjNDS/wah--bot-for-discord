import discord
from discord.ext import commands
import random
import configparser
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
# FUNÇÕES AUXILIARES
######################

# FUNCOES PARA ROLAGEM

# retorna um vetor de x números aleatórios num intervalo de [1, y]
async def dice(before, after):
    diceResults = []
    for _ in range(before):
        diceResults.append(random.randint(1, after))
    return diceResults


# rola vários dados
async def dices(repeat, before, after):
    dicesResults = []
    for _ in range(repeat):
        dicesResults.append(await dice(before, after))
    return dicesResults


# destaca dados maximos e minimos
async def checkMaxMin(val, after):
    string = ''
    if val == after:
        string += "**"
        string += str(val)
        string += "**"
    elif val == 1:
        string += "*"
        string += str(val)
        string += "*"
    else:
        string += str(val)

    return string


# destaca criticos
async def checkCrit(before, after, val):
    if before == 1 and after == 20:
        if val == 20:
            return "\n**Critical success!**\n"
        elif val == 1:
            return "\n**Critical fail!**\n"
    else:
        return ""


# transforma os resultados dos dados para uma string formatada para o discord
async def diceToString(diceList, after, total):
    string = f"**`{total}`** ← ("
    for element in diceList[:-1]:
        temp = await checkMaxMin(element, after)
        string += temp
        string += ", "
    string += await checkMaxMin(diceList[-1], after)
    string += ')'

    return string


# transforma a string para comportar multiplas rolagens
async def dicesToString(diceLists):
    string = ''
    for row in diceLists:
        string += row
        string += '\n'
    return string


# retorna uma lista com: before, after, ops a partir de uma string
async def stripStr(string):
    before = ''
    after = ''
    ops = ''
    opsTotal = 0

    ops = list(string.partition('d'))
    before = ops[0]
    before = before or '1'  # fornece um valor padrão quando a string é vazia
    ops = ops[2]

    idx = -1
    for char in ops:
        if char.isdigit():
            after += char
        else:
            idx = ops.find(char)
            break

    if idx > 0:
        ops = ops[idx:]
    else:
        ops = ''

    # A função all() em Python retorna True se todos os elementos de uma sequência são verdadeiros (ou se a sequência está vazia). Se pelo menos um elemento for falso, all() retorna False.
    isSafe = all(c.isdigit() or c in ['+', '-'] for c in ops)

    if isSafe and ops:
        opsTotal = eval(ops)

    arr = [int(before), int(after), ops, opsTotal]
    return arr


#######################
#    COMANDO DADOS
######################


@bot.command(pass_context=True, aliases=['r'])
async def roll(ctx, string: str):
    before, after, ops, opsTotal = await stripStr(str(string))

    diceResult = await dice(before, after)
    total = sum(diceResult) + opsTotal
    rollsString = await diceToString(diceResult, after, total)

    await ctx.send(f" **{ctx.author.mention}'s rollin'! :game_die: **\n"
                   f"**Dado {before}d{after}:** \n{rollsString}{ops}\n"
                   )

    await ctx.message.delete()


@bot.command(pass_context=True, aliases=['rm'])
async def rollMultiple(ctx, times: int, string: str):
    before, after, ops, opsTotal = await stripStr(str(string))
    dicesResult = await dices(times, before, after)

    rollsString = []
    total = 0

    for row in dicesResult:
        total = sum(row) + opsTotal
        rollsString.append(await diceToString(row, after, total))

    rollsString = await dicesToString(rollsString)

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
