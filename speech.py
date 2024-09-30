import asyncio
from gtts import gTTS
import os
import tempfile
import pygame

async def text_to_speech(text):
    """Convert text to speech and play it asynchronously."""
    # Create temporary audio file
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=True) as temp_audio_file:
        tts.save(f"{temp_audio_file.name}.mp3")
        
        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(f"{temp_audio_file.name}.mp3")
        pygame.mixer.music.play()

        # Wait until the sound has finished playing
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)

    return 200  
