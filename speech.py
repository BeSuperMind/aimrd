import speech_recognition as sr
import requests  
from text_to_speech import text_to_speech_sync

def check_internet_connection():
    """Check if the internet connection is available."""
    try:
        # Ping Google's DNS server to check for internet connection
        requests.get('https://www.google.com/', timeout=5)
        return True
    except requests.ConnectionError:
        return False

def getQuery(mixer):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as mic:
            print(f"\nUsing microphone:")
            recognizer.adjust_for_ambient_noise(mic, duration=0.5)
            audio = recognizer.listen(mic, timeout=5)
            print("Audio captured successfully!")
            text_to_speech_sync('Audio captured successfully!', mixer)

            # Check for internet connectivity before trying to recognize speech
            if check_internet_connection():
                try:
                    text = recognizer.recognize_google(audio)
                    text = text.lower()
                    print(text)
                    return text

                except sr.UnknownValueError:
                    print("Could not understand the audio.")
                    text_to_speech_sync('Could not understand the audio.', mixer)
                    return 'error'

                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition; {e}")
                    text_to_speech_sync(f"Could not request results from Google Speech Recognition; {e}",mixer)
                    return 'error'

            else:
                print("No internet connection.")
                text_to_speech_sync('No internet connection.', mixer)
                return '503'

    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase to start")
        text_to_speech_sync('Listening timed out while waiting for phrase to start', mixer)
        return 'error'

    except Exception as e:
        print(f"An error occurred: {e}")
        return 'error'


