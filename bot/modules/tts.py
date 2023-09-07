# TTD Command V1.4 | Made by Ryohei
# usage !tts (message) or tts on every message
# Permission: Anyone

import asyncio
import functools
import os
import random
import string
import subprocess
import re
import emoji
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import unicodedata
import pygame

from kick import Message
from gtts import gTTS

from modules.cooldown import command_cooldown
from modules.database import db_context


pygame.mixer.init()



#The Old tts command/module 
#This code works it just currently doesnt use the database for settings

#anti spam related settings for the tts!
#cost = 0 #how much the !tts command should cost, set this to 0 if you wish to use tts per message rather then the command
#and or if you just dont want it to cost anything
numberspam = 500 #set how many numbers a message can contain before the message will be skipped
maxmsgchars = 500 #set how long a message can be before the message will be skipped
cooldown_duration = 3  # cooldown duration in seconds


# Global variables (shouldnt change these below)
currently_playing = False
queue = []
cooldown_dict = {} 

def sync_generate_and_play_audio(text, language, temp_filename):
    tts = gTTS(text=text, lang=language)
    tts.save(temp_filename)
    pygame.mixer.music.load(temp_filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # Optionally, add a pygame.time delay here
        continue

async def generate_and_play_audio(text, language, temp_filename):
    thing = functools.partial(sync_generate_and_play_audio, text, language, temp_filename)
    await asyncio.get_event_loop().run_in_executor(None, thing)

async def play_from_queue():
    global currently_playing

    while queue:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        if not currently_playing:
            currently_playing = True
            nextTTS = queue.pop(0)
            temp_folder = "temp"
            os.makedirs(temp_folder, exist_ok=True)
            filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".mp3"
            temp_filename = os.path.join(temp_folder, filename)
            await generate_and_play_audio(nextTTS, "en", temp_filename)
            currently_playing = False
        await asyncio.sleep(0.5)

async def skip_audio():
    if pygame.mixer.music.get_busy():  # Check if any audio is playing
        pygame.mixer.music.stop()  # Stop that audio
        await play_from_queue()  # Start playing the next audio in the queue

async def texttospeach(msg: Message):
    async with db_context as db:
        tts = await db.general.find_one({"name": "tts"}, {"_id": 0})

    if await command_cooldown(msg.author.id, "tts", tts['cooldown']):
        return

    if tts['type'] == 'off':
        return
    elif tts['type'] == "chat":
        await texttoseach(msg)
    else:
        await texttoseach(msg)

async def texttoseach(msg: Message):

    #{'name': 'tts', 'type': 'chat', 'cooldown': 39, 'maxnumbers': 20, 'maxtext': 500, 'vip': 1.2}

    #if await command_cooldown(msg.author.id, "tts", 10):
    #    return

    #if cost == 0 or (cost != 0 and await viewpoints(msg.author.id) < cost):
    #    await msg.chatroom.send(f'@{msg.author} You do not have enough points')
    #    return

    global currently_playing
    global queue

    text = msg.content.replace("!tts", "")
    pattern = r'\[emote:\d+:(.*?)\]'
    text = re.sub(pattern, r'\1', text)
    message = emoji.demojize(text)

    if not sum(c.isdigit() for c in message) <= numberspam: #skip a message if it has more numbers then what is set
        return
    message = message[:maxmsgchars]
    #if len(message) > maxmsgchars:
    #    return

    language = "en"
    if msg.author:
        speech_text = f"{msg.author} said {message}"
    else:
        speech_text = message

    queue.append(speech_text)

    if not currently_playing:
        await play_from_queue()

    return
