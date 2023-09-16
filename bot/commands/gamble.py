from modules.points import setpoints, viewpoints
from kick import Message
import random
import time

cooldown_dict = {}  # dictionary to store last gamble time for each user

async def gamble(msg: Message):

    gamble_str = msg.content.replace('!gamble ', '')
    if gamble_str.lower() == 'all':
        gamble_amount = await viewpoints(msg.author.id)
    else:
        gamble_amount = int(gamble_str)

    # Get the user's points
    points = await viewpoints(msg.author.id)

    # Check if the user has enough points
    if points >= gamble_amount:
        # Subtract the gamble amount from the user's points
        await setpoints(msg.author.id, points - gamble_amount)

        # Determine if the user wins or loses (50/50 chance)
        win = random.choice([True, False, False, False, False])

        if win:
            # If the user wins, calculate a random gain percentage (0-100%)
            gain_percentage = random.random()
            # Add the gamble amount plus the gain to the user's points
            win_amount = int(gamble_amount * (1 + gain_percentage))
            await setpoints(msg.author.id, points + win_amount)
            await msg.chatroom.send(f"@{msg.author} You won! Your new points total is {await viewpoints(msg.author.id)}")
        else:
            # If the user loses, calculate a random loss percentage (0-100%)
            loss_percentage = random.random()
            # Subtract the gamble amount minus the loss from the user's points
            loss_amount = int(gamble_amount * (1 - loss_percentage))
            await setpoints(msg.author.id, points - loss_amount)
            await msg.chatroom.send(f" @{msg.author} You lost! Your new points total is {await viewpoints(msg.author.id)}")
    else:
        await msg.chatroom.send(f"@{msg.author} You don't have enough points to gamble this amount.")
