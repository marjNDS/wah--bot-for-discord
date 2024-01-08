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


#######################
# FUNCOES FORA DO BOT
######################

# FUNCOES PARA ROLAGEM
def sumString(txt):
    total = 0
    i = 0
    while i < len(txt):
        temp = ''
        # print("no for") #DEBUG
        if txt[i] == '+' or txt[i] == '-':
            op = txt[i]
            i += 1
            while i < len(txt) and txt[i] != '+' and txt[i] != '-':
                temp += txt[i]
                # print(f"Dentro do while. i = {i} txt[i]={txt[i]} temp = {temp}") #DEBUG
                i += 1

            if op == '+':
                total += int(temp)
            elif op == '-':
                total -= int(temp)
    return total


def checkCrit(before, after, result):
    string = ''
    if int(before) == 1 and int(after) == 20 and result == 20:
        string = "**Critical success!**\n"
    elif int(before) == 1 and int(after) == 20 and result == 1:
        string = "**Critical fail!**\n"

    return string


def printDice(vet):
    string = '('
    for i in range(0, len(vet), 1):
        if i < len(vet) - 1:
            string += str(vet[i])
            string += ', '
        else:
            string += str(vet[i])
            string += ')'
    return string


def printDiceSeveral(vet):
    out = ''
    for i in range(0, len(vet), 1):
        out += '('
        for j in range(0, len(vet[i]), 1):
            out += str(vet[i][j])
            if j < len(vet[i]) - 1:
                out += ', '
        out += ') '
    return out


#######################
#    DADOS
######################


@bot.command(pass_context=True, aliases=['r', 'roll'])
async def dice(ctx, string, times=0):
    before = ""
    after = ""
    sum = ""

    checkD = False
    checkOp = False

    for i in range(0, len(string), 1):
        if not checkOp:
            if string[i] == '+' or string[i] == '-':
                checkOp = True
                sum += string[i]
            elif string[i] == 'd':
                checkD = True
            elif not checkD:
                before += string[i]
            else:
                after += string[i]
        else:
            sum += string[i]

    total = 0
    rand = []

    before = before or '1' #fornece um valor padrão quando a string é vazia

    for i in range(0, int(before), 1):
        temp = random.randint(1, int(after))
        total += temp
        if temp == int(after) or temp == 1:
            temp = '**' + str(temp) + '**'

        rand.append(temp)


    await ctx.send(f" **{ctx.author.mention}'s rollin'! :game_die: **\n"
                   f"**Dado {before}d{after}:** {printDice(rand)}{sum}\n"
                   f"{checkCrit(before, after, total)}"
                   f"**Total:** {total + sumString(sum)}")

    await ctx.message.delete()


@bot.command(pass_context=True, aliases=['rm', 'rollm', 'rollmultiple'])
async def diceSeveral(ctx, vezes: int, string):
    before = ""
    after = ""
    sum = ""

    checkD = False
    checkOp = False

    for i in range(0, len(string), 1):
        if not checkOp:
            if string[i] == '+' or string[i] == '-':
                checkOp = True
                sum += string[i]
            elif string[i] == 'd':
                checkD = True
            elif not checkD:
                before += string[i]
            else:
                after += string[i]
        else:
            sum += string[i]
    if before == '':
        before = '1'

    total = 0
    rand = []
    rands = []
    totals = []

    for i in range(0, vezes, 1):
        total = 0
        for j in range(0, int(before), 1):
            temp = random.randint(1, int(after))
            total += temp
            if temp == int(after) or temp == 1:
                temp = '**' + str(temp) + '**'

            rand.append(temp)
        totals.append(total + sumString(sum))
        rands.append(rand)
        rand = []

    await ctx.send(f" **{ctx.author.mention}'s rollin'! :game_die: **\n"
                   f"**{vezes} dados {before}d{after}:** {printDiceSeveral(rands)}{sum}\n"
                   f"**Totais:** {printDice(totals)}")

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
