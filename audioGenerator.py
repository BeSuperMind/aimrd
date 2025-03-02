from gtts import gTTS

# Text messages for each audio file
texts = {
    "concentrate.mp3": "Please concentrate",
    "moving.mp3": "Please stop moving",
    "drowsy.mp3": "Hey you can't sleep during meditation"
}

# Generate and save each audio file
for filename, text in texts.items():
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    print(f"Saved {filename} with message: '{text}'")

print("Audio files generated successfully.")
