import time
import random

from core.points import setpoints, viewpoints
from core.cooldown import command_cooldown
from kick import Message


slot_emojis = ["🍌", "🍎", "🍒"] # The list of emoji emojis
mincost = 100 #how much it should cost to use the command

async def slots(msg: Message):

    # Extract the bet amount and the number of lines from the message
    parts = msg.content.split(' ', 2)
    if len(parts) == 1:
        await msg.chatroom.send(f"@{msg.author} Usage: !slots [amount] (1-5)")
        return
    elif len(parts) < 3:
        _, bet_str = parts
        lines_str = '1'  # default value
    else:
        _, bet_str, lines_str = parts

    lines = int(lines_str)

    # Set the maximum number of lines
    max_lines = 5
    if lines > max_lines:
        await msg.chatroom.send(f"@{msg.author} The maximum number of lines is {max_lines}.")
        return

    if bet_str.lower() == 'all':
        bet_amount = await viewpoints(msg.author.id)
    else:
        bet_amount = int(bet_str)

    # Set the minimum bet amount
    min_bet_amount = mincost
    if bet_amount < min_bet_amount:
        await msg.chatroom.send(f"@{msg.author} The minimum bet amount is {min_bet_amount} points.")
        return

    total_cost = bet_amount * lines

    # Get the user's points
    points = await viewpoints(msg.author.id)

    # Check if the user has enough points
    if points >= total_cost:
        # Generate the slot machine result
        result = [[random.choice(slot_emojis) for _ in range(3)] for _ in range(lines)]

        # Calculate the winnings
        winnings = calculate_winnings(result, bet_amount)

        # If the user wins, add the winnings to the user's points. Otherwise, subtract the bet amount.
        if winnings > 0:
            await setpoints(msg.author.id, points + winnings)
        else:
            await setpoints(msg.author.id, points - bet_amount)

        # Send the result to the chatroom
        result_str = ' | '.join(' '.join(line) for line in result)
        virwpoints = round(await viewpoints(msg.author.id))
        await msg.chatroom.send("@{} Your slot machine result is: {} | Your new points total is {}".format(msg.author, result_str, virwpoints))
    else:
        await msg.chatroom.send(f"@{msg.author} You don't have enough points to play this slot machine.")


def calculate_winnings(result, bet_amount):
    # Calculate the winnings based on the slot machine result
    winnings = 0
    for line in result:
        if line.count(line[0]) == len(line):  # all emojis in the line are the same
            winnings += bet_amount * 2  # the user wins twice the bet amount for each winning line
    return winnings
