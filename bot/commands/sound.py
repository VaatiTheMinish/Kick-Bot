from kick import Message
from modules.cooldown import command_cooldown
from modules.points import setpoints, viewpoints, rmpoints


import os
import subprocess
import json


async def sound(msg: Message):
    sender = str(msg.author)
    userid = msg.author.id 
    sound_name = msg.content.replace("!sound", "").strip().split()

    if not sound_name:
        await msg.chatroom.send('Usage !sound (sound name). To view a list of sounds use !listsounds')
        return 

    sound_file = sound_name[0] + ".wav"
    sound_path = os.path.join("sounds", sound_file)

    if os.path.exists(sound_path):
        play_sound(sound_path)
    else:
        await msg.chatroom.send("Sound file not found. To view a list of sounds use !listsounds")

def play_sound(sound_path):
    subprocess.Popen(["ffplay", "-nodisp", "-autoexit", sound_path], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)



