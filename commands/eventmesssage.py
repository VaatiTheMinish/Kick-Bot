import logging
from kick import Message
from core.event_manager import list_jobs, pause_job, new_job


async def list(args, msg: Message):
    print("listing all event messages")
    active_jobs = await list_jobs()
    formatted_jobs = ', '.join(active_jobs)
    await msg.chatroom.send(f"Active event messages: {formatted_jobs}")
    return

async def add(args, msg: Message):
    await new_job(msg)
    return

async def edit(args, msg: Message):
    event_name = args[1]
    return


async def rm(args, msg: Message):
    event_name = args[1]
    return


async def disable(args, msg: Message):
    #['disable', 'events_discord_reminder']
    job = args[1]
    status =  await pause_job(job)
    print(status)
    await msg.chatroom.send(status)

async def enable(args, msg: Message):
    return

async def info(args, msg: Message):
    await msg.chatroom.send("{Name} is {enabled/disabled} with the following settings. 5 Chat messages, Every 10 Minutes")
    return


subcommannds = {
    "add": add,
    "list": list,
    "edit": edit,
    "disable": disable,
    "enable": enable,
    "rm": rm,
    "info": info
}

async def eventmessage(msg: Message):
    args = msg.content.replace("!eventmessage ","").split(" ")
    if subcommannds.get(args[0], None) != None:
        await subcommannds[args[0]](args, msg)