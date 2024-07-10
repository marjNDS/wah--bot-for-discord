import random


async def dice(before, after):
    """
    Rolls a die in a 'before d after' format. Exemple: 2d6, 1d20, 4d4.
    :param before: the number of dices to be rolled
    :param after: the number of faces of the dice
    :return: returns a list of the random numbers rolled.
    """
    dice_results = []
    for _ in range(before):
        dice_results.append(random.randint(1, after))
    return dice_results


async def dices(repeat, before, after):
    """
    Rolls dice in a 'before d after' format, repeat is the number of times each roll will be done. Exemple: 3 * 2d6,
    2 * 1d20,  10 * 4d4.
    :param repeat: Number of times this set of rolls will be executed.
    :param before: the number of dices to be rolled
    :param after: the number of faces of the dice
    :return: returns a list of lists of the random numbers rolled, each list corresponds to a set of results.
    """
    dices_results = []
    for _ in range(repeat):
        dices_results.append(await dice(before, after))
    return dices_results


async def check_max_min(val, after):
    """
    checks if a value corresponds to a maximum or a minimum in a die.
    :param val: the value to be checked
    :param after: the maximum value it can be
    :return: a string formatted for discord with bold maximums and itallic minimums
    """
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
async def check_crit(before, after, val):
    """
    If the die is in 1d20 format and the value is a maximum or minimum, returns a string declaring critical success
    or failure
    :param before: the number of dices to be rolled
    :param after: the number of faces of the dice
    :param val: the value being tested
    :return: a string formatted for discord with critical failure or critical success or an empty string
    """
    if before == 1 and after == 20:
        if val == 20:
            return "\n**Critical success!**\n"
        elif val == 1:
            return "\n**Critical fail!**\n"
    else:
        return ""


async def dice_to_string(dice_list, after, total):
    """
    Transforms a list of die results into a formatted string for discord.
    :param dice_list: the list of dice results
    :param after: the number of faces in the die
    :param total: the roll that was given as input (exemple: 2d6)
    :return: a formatted string with the results.
    """
    string = f"**`{total}`** ← ("
    for element in dice_list[:-1]:
        temp = await check_max_min(element, after)
        string += temp
        string += ", "
    string += await check_max_min(dice_list[-1], after)
    string += ')'

    return string


async def dices_to_string(dice_lists):
    """
    Transforms a list of lists of dice into a formatted string for discord.
    :param dice_lists: the list of lists of dice
    :return: string formatted for discord with the dice results.
    """
    string = ''
    for row in dice_lists:
        string += row
        string += '\n'
    return string


async def strip_str(string):
    """
    Transforms a dice string into a list of variables necessary to process them into random numbers.
    :param string: Dice represented in the before d after format.
    Examples of input strings:
    2d6
    d20
    4d100
    :return: Returns a list of: [before, after, operations, operations total] used to roll the dice
    """
    before = ''
    after = ''
    ops = ''
    ops_total = 0

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

    # A função all() em Python retorna True se todos os elementos de uma sequência são verdadeiros (ou se a sequência
    # está vazia). Se pelo menos um elemento for falso, all() retorna False.
    is_safe = all(c.isdigit() or c in ['+', '-'] for c in ops)

    if is_safe and ops:
        ops_total = eval(ops)

    arr = [int(before), int(after), ops, ops_total]
    return arr
