from kick import Message

from core.tts import texttospeach

async def tts(msg: Message):
    await texttospeach(msg)