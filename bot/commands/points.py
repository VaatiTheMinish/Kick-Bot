
from kick import Message
from modules.points import showpoints


async def points(msg: Message):
    result = await showpoints(msg.author.id)
    if "No record" in result:
        result = f"@{msg.author.slug} has no points"        

    await msg.chatroom.send(result)
    
    return
