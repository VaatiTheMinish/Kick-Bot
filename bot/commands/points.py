
from kick import Message
from modules.points import showpoints
import globals

async def fetch_and_process(username):
    try:
        print("YES")
        user = await globals.client.fetch_user(username)
        user_id = int(user.id)  # Convert user.id to an integer
        return user_id
    except:
        print("Exception")
        username = username.replace("-", "_").replace("_", "-")
        user = await globals.client.fetch_user(username)
        user_id = int(user.id)
        return user_id

async def points(msg: Message):

    if msg.content != "!points":
        messageargs = msg.content.replace("!points ", "").split(" ")
        username = messageargs[0].replace("@","")
        user = await fetch_and_process(username)
        result = await showpoints(user)
        if "No record" in result:
            result = f"@{username} has no points"        

        await msg.chatroom.send(result)
        return
    else:
        result = await showpoints(msg.author.id)
        if "No record" in result:
            result = f"@{msg.author.slug} has no points"

        await msg.chatroom.send(result)

