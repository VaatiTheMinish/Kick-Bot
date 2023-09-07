from modules.database import db_context
from kick import Message

#  args[0]   args[1]   args[2]
# ['tts', 'cooldown', '1']
#   tts    type          cmd
#

async def tts(args, message: Message):
    print("TTS SETTINGS RAN")
    valid_keys = ["type", "cooldown", "maxtext", "maxnumbers"]

    if args[1] not in valid_keys:
        await message.chatroom.send("Usage !settings tts [type|cooldown|maxtext|maxnumbers]")
        return

    if args[1] == 'type':
        if args[2] == 'chat':
            value = 'chat'
        elif args[2] == 'cmd':
            value = 'cmd'
        elif args[2] == 'off':
            value='off'

    update_operations = {
        'cooldown': (int, 'Invalid value for cooldown. It should be a number.', 'cooldown'),
        'type': (str, "Invalid value for type. It should be one of 'off', 'chat', or 'command'.", 'type'),
        'maxtext': (int, 'Invalid value for maxtext. It should be a number.', 'maxtext'),
        'maxnumbers': (int, 'Invalid value for maxnumbers. It should be a number.', 'maxnumbers')
    }


    check_fn, error_message, field = update_operations[args[1]]

    try:
        value = check_fn(args[2])
    except (ValueError, TypeError):
        await message.chatroom.send(error_message)
        return

    async with db_context as db:
        tts_doc= db.general
        await tts_doc.update_one({'name': 'tts'}, {'$set': {field: value}})
        print(f"{field.capitalize()} updated to: {value}")

    return


async def points(args, message: Message):
    print(args)
    valid_keys = ["points"]

    if args[1] not in valid_keys:
        await message.chatroom.send("Usage !settings points [cooldown|enabled]")
        return

    update_operations = {
        'cooldown': (int, 'Invalid value for cooldown. It should be a number.', 'cooldown'),
        'min': (int, 'Invalid value for min points. It should be a number.', 'min'),
        'max': (int, 'Invalid value for max points. It should be a number.', 'max'),
        'enabled': (bool, 'Invalid value. It should be true or false', 'enabled') 
    }

    check_fn, error_message, field = update_operations[args[1]]

    try:
        value = check_fn(args[2])
    except (ValueError, TypeError):
        await message.chatroom.send(error_message)
        return

    async with db_context as db:
        points_collection = db.general
        await points_collection.update_one({'name': 'tts'}, {'$set': {field: value}})
        print(f"{field.capitalize()} updated to: {value}")

    return

async def pointsmiltiplier(args, message: Message):
    print(args)
    valid_keys = ["founder","subscriber", "moderator", "vip", "og", "default", "broadcaster", "enabled"]

    if not args[1]:
         await message.chatroom.send("Error")

    if args[1] not in valid_keys:
        await message.chatroom.send(f"Usage !settings pointsmiltiplier {valid_keys} [value]")
        return

    # Check if value is provided
    if len(args) < 3:
        await message.chatroom.send(f"You must specify a value for {args[1]}.")
        return

    update_operations = {
        'enabled': (lambda x: x.lower() in ['true', 'false'], "Invalid value for enabled. It should be either True or False."),
    }

    for key in valid_keys[:-1]: # Exclude 'enabled'
        update_operations[key] = (float, 'Invalid value for {}. It should be a number.'.format(key))

    check_fn, error_message = update_operations[args[1]]

    try:
        value = check_fn(args[2])
    except (ValueError, TypeError):
        await message.chatroom.send(error_message)
        return

    async with db_context as db:
        points_collection = db.general
        await points_collection.update_one({'name': 'tts'}, {'$set': {args[1]: value}})
        await message.chatroom.send(f"{args[1].capitalize()} points multiplier updated to: {value}")

    return


modules = {
    "tts": tts,
    "points": points,
    "pointsmiltiplier": pointsmiltiplier
}


async def settings(message: Message):
    split_message = message.content.split(" ", 1)
    if len(split_message) > 1:
        args = split_message[1].split(" ")
        if len(args) > 1 and args[1]:  # check if args[1] exists and is not an empty string
            if modules.get(args[0], None) != None:
                await modules[args[0]](args, message)
            else:
                await message.chatroom.send("Usage !settings [tts|points|pointsmiltiplier]")
        else:
            # handle the case where args[1] is None or an empty string
            await message.chatroom.send("Usage !settings [points|tts|pointsmiltiplier] [setting] [value]")
    else:
        # handle the case where split_message has less than 2 elements
        await message.chatroom.send("Usage !settings [points|tts|pointsmiltiplier] [setting] [value]")