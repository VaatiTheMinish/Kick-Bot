from kick import Message

from modules.tts import texttospeach

async def tts(msg: Message):
    await texttospeach(msg)