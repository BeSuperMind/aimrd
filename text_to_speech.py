from gtts import gTTS
import os
import asyncio
from pygame import mixer

mixer.init()
# Asynchronous text-to-speech function
async def text_to_speech_async(text, lang='en'):
    try:
        # Convert text to speech and save to a temporary file
        tts = gTTS(text=text, lang=lang)
        temp_audio_path = "output.mp3"
        tts.save(temp_audio_path)

        # Initialize pygame mixer
        if not mixer.get_init():
            mixer.init()

        # Load and play the audio
        mixer.music.load(temp_audio_path)
        mixer.music.play()

        # Wait for the audio to finish playing asynchronously
        while mixer.music.get_busy():
            await asyncio.sleep(0.1)  # Allow async loop to continue

    except Exception as e:
        print(f"Error in text_to_speech_async: {e}")

    finally:
        # Quit mixer and remove the audio file
        mixer.music.stop()
        mixer.quit()
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

# Synchronous text-to-speech function
def text_to_speech(text, lang='en'):
    try:
        # Convert text to speech and save to a temporary file
        tts = gTTS(text=text, lang=lang)
        temp_audio_path = "output.mp3"
        tts.save(temp_audio_path)

        # Initialize pygame mixer
        if not mixer.get_init():
            mixer.init()

        # Load and play the audio
        mixer.music.load(temp_audio_path)
        mixer.music.play()

        # Wait for the audio to finish playing
        while mixer.music.get_busy():
            pass  # Busy-wait until audio playback completes

    except Exception as e:
        print(f"Error in text_to_speech: {e}")

    finally:
        # Quit mixer and remove the audio file
        mixer.music.stop()
        mixer.quit()
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
