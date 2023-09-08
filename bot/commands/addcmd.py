#!addcmd (name) (message)
#name becomes ailas

from modules.database import db_context
from kick import Message

async def addcmd(msg: Message):
    args = msg.content.replace("!addcmd ","").split(" ")
    command_name = args[0]
    message_value = ' '.join(args[1:])
    
    if not message_value:
        msg.chatroom.send("usage !addcmd (name) (message)")
        return

    async with db_context as db:
        commands_collection = db.commands
        command = await commands_collection.find_one({"name": command_name})
        if command:
            msg.chatroom.send(f"The command {command_name} already exists.")
            return

        alias_command = await commands_collection.find_one({"aliases": command_name})
        if alias_command:
            msg.chatroom.send(f"The command {command_name} already exists as an alias.")
            return

        new_command = {
            "cooldown": 0,
            "cost": 0,
            "message": message_value,
            "permission": 0,
            "enabled": True,
            "aliases": [command_name],
            "name": command_name,
            "file": False,
            "cooldowntype": "user"
        }
        await commands_collection.insert_one(new_command)
        msg.chatroom.send(f"Command !{command_name} has been successfully added.")
    return
