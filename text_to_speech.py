from gtts import gTTS
import os, time


async def text_to_speech(text, mixer, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")

    # Initialize pygame mixer
    mixer.init()
    mixer.music.load("output.mp3")
    mixer.music.play()

    # Wait until the audio finishes playing
    while mixer.music.get_busy():
        time.sleep(1)  # Sleep for a while to avoid busy-waiting

    # Uninitialize the mixer to release the file
    mixer.quit()

    # Clean up the audio file
    os.remove("output.mp3")

def text_to_speech_sync(text, mixer, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")

    # Initialize pygame mixer
    mixer.init()
    mixer.music.load("output.mp3")
    mixer.music.play()

    # Wait until the audio finishes playing
    while mixer.music.get_busy():
        time.sleep(1)  # Sleep for a while to avoid busy-waiting

    # Uninitialize the mixer to release the file
    mixer.quit()

    # Clean up the audio file
    os.remove("output.mp3")



