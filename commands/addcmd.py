#!addcmd (name) (message)
#name becomes ailas

from commands.commands import commands
from core.database import db_context
from kick import Message
from globals import client, commands, commands_dir


async def reload_commands(new_command):
    async with db_context as db:
        command_docs = await db.commands.find().to_list(length=None)
        total_commands = len(command_docs)
        loaded_commands = 0
        print(f"!{new_command} added Reloading Commands")
        for command_doc in command_docs:
            #print(f"{command_doc['name']} with aliases: {', '.join(command_doc['aliases'])}")
            for alias in command_doc['aliases']:
                commands[alias] = command_doc['_id']
        print(f" Successfully reloaded {total_commands} commands")


async def addcmd(msg: Message):
    args = msg.content.replace("!addcmd ","").split(" ")
    command_name = args[0]
    message_value = ' '.join(args[1:])
    
    if not message_value:
        await msg.chatroom.send("usage !addcmd (name) (message)")
        return

    async with db_context as db:
        commands_collection = db.commands
        command = await commands_collection.find_one({"name": command_name})
        if command:
            await msg.chatroom.send(f"The command {command_name} already exists.")
            return

        alias_command = await commands_collection.find_one({"aliases": command_name})
        if alias_command:
            await msg.chatroom.send(f"The command {command_name} already exists as an alias.")
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
        await reload_commands(args[0])
        await msg.chatroom.send(f"Command !{command_name} has been successfully added.")

    return
