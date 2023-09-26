import configparser
import logging
from core.database import db_context
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from kick import Credentials, Message, User, Livestream, Chatroom
from globals import Client


config = configparser.ConfigParser()
config.read("config.ini")
channel = str(config.get("botcredentials", "channel"))
scheduler = AsyncIOScheduler()

minchat_counts = {}

async def database():
    async with db_context as db:
        events = await db.event_messages.find().to_list(None)
    return events

async def handle_message():
    events = await database()
    for event in events:
        event_name = event['name']
        if event_name not in minchat_counts:
            minchat_counts[event_name] = 0
        min_chat = event['min_chat']
        minchat_counts[event_name] += 1
    logging.info(f"Min chat count {minchat_counts}")


async def sendmsg(chatroom: Chatroom, event):
    logging.info(f" Min chat count:: {minchat_counts}")
    event_name = event['name']
    minchat = minchat_counts.get(event_name, 0)  # Get the minchat count for the event name
    if minchat > event['min_chat']:
        await chatroom.send(event['message'])
        minchat_counts[event_name] = 0  # Reset the minchat count for the event name
    else:
        logging.info(f"Event {event_name} skipped due to less than {event['min_chat']} messages")
        return

async def remove_event(args, msg):
    event_name = args[1]
    async with db_context as db:
        commands_collection = db.event_messages
        event = await commands_collection.find_one({"name": event_name})
        if not event:
            await msg.chatroom.send(f"No event found with name {event_name}")
            return

        await commands_collection.delete_one({'name': event_name})
        scheduler.remove_job(event_name)
        await msg.chatroom.send(f"Event {event_name} has been successfully removed.")
    return

async def edit_event(args, msg):
    event_name = args[1]
    new_message = ' '.join(args[2:])
    async with db_context as db:
        commands_collection = db.event_messages
        event = await commands_collection.find_one({"name": event_name})
        if not event:
            await msg.chatroom.send(f"No event found with name {event_name}")
            return
        await commands_collection.update_one({'name': event_name}, {'$set': {'message': new_message}})
        scheduler.remove_job(event_name)
        await register_job(event_name, msg.chatroom, event, delay=10*60)
    return (f"Event {event_name} has been successfully edited and restarted.")


async def new_job(msg: Message):
    chatroom: Chatroom
    #['!eventmessage', 'add', 'test', 'this', 'is', 'a', 'text', 'event', 'message']
    
    args = msg.content.replace("!eventmessage ","").split(" ")
    print(args)

    event_name = args[1]
    event_message = ' '.join(args[2:])
    async with db_context as db:
        commands_collection = db.event_messages
        event = await commands_collection.find_one({"name": event_name})
        if event:
            await msg.chatroom.send(f"The event {event_name} already exists.")
            return

        new_command = {
            "enabled": True,
            "message": event_message,
            "time": 10,
            "min_chat": 5,
            "name": event_name  
        }

        await commands_collection.insert_one(new_command)
        await msg.chatroom.send(f"event {event_name} has been successfully added and has been started")
        await register_job(event_name, msg.chatroom, event, delay=10*60)
    return


async def register_job(job_id: str, chatroom, event, delay: int):
    if not scheduler.get_job(job_id):
        scheduler.add_job(
            sendmsg,
            'interval',
            seconds=delay,
            name=job_id,
            id=job_id,
            args=(chatroom, event)
        )
        print(f"Sucessfully started event: {job_id}")
    else:
        print(f"Event already exists with id {job_id}")

async def list_jobs():
    jobs = scheduler.get_jobs()
    active_jobs = {job.name: 'active' for job in jobs}

    async with db_context as db:
        commands_collection = db.event_messages
        db_jobs = await commands_collection.find({}).to_list(None)
        for job in db_jobs:
            if job["name"] not in active_jobs:
                active_jobs[job["name"]] = 'disabled'

    job_status_list = [f'{name} ({status})' for name, status in active_jobs.items()]
    return job_status_list


async def pause_job(job_id: str):
    if scheduler.get_job(job_id):
        scheduler.pause_job(job_id)
        async with db_context as db:
            events = db.event_messages
            await events.update_one({'name': job_id}, {'$set': {'enabled': False}})
        status = (f"Stopped: {job_id} and disabled it")
        return status
    else:
        status = (f"No event found with id {job_id}")
        return status


async def load_events_from_db(chatroom: Chatroom):

    events = await database()
    for event in events:
        if event['enabled']:  # Only add jobs for enabled events
            name = event['name']
            print(f"Loaded event: {name}")
            # For testing comment out the '*60' to make it send in seconds
            delay = event['time'] * 60 #Convert minutes to seconds

            # Generate a unique ID for the job
            job_id = f"{name}"
            #job_id, chatroom, message, delay, minchat
            #await add_job(chatroom, event, delay)
            await register_job(job_id, chatroom, event, delay)

    if not scheduler.running:
        scheduler.start()