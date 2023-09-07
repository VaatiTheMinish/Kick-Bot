
from kick import Message
from modules.points import addpoints, setpoints, rmpoints
import globals

#args 0 command name
#args 1 subcommand
#args 2 user
#args 3 points

# Separate function to fetch and process variables
async def fetch_and_process(args):
    username = args[2].replace("@", "").lower()
    user = await globals.client.fetch_user(username)
    user_id = int(user.id)  # Convert user.id to an integer
    if len(args) < 4 or args[3] is None:
        points = 0
    else:
        points = int(args[3])
    return username, user_id, points

# Your add function
async def add(args, msg: Message):
    username, user_id, points = await fetch_and_process(args)
    await addpoints(username, user_id, points, False)
    await msg.chatroom.send(f"Added {points} points to {username}")

async def set(args, msg: Message):
    username, userid, points = await fetch_and_process(args)
    await setpoints(userid, points)
    await msg.chatroom.send(f"Set {username}'s points to {points}")
    return

async def rm(args, msg: Message):
    username, userid, points = await fetch_and_process(args)
    await rmpoints(userid, points)
    await msg.chatroom.send(f"Removed {points} points from {username}")
    return

async def reset(args, msg: Message):
    username, userid, points = await fetch_and_process(args)
    await setpoints(userid, 0)
    await msg.chatroom.send(f"Reset {username}'s Points")
    return


subcommannds = {
    "add": add,
    "set": set,
    "rm": rm,
    "reset": reset
}

async def apoints(msg: Message):

    args = msg.content.replace("!editcmd ","").split(" ")
    if subcommannds.get(args[1], None) != None:
        await subcommannds[args[1]](args, msg)