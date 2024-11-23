import pickle
import time
import pandas as pd
import os
import warnings
import pyttsx3
warnings.filterwarnings("ignore", category=UserWarning)

# Load the model
model_file = 'ppgStress.pkl'
with open(model_file, 'rb') as file:
    model = pickle.load(file)

def provide_feedback(rmssd, sdnn):
    """
    This function provides feedback based on the RMSSD and SDNN values.
    """
    # Convert RMSSD to milliseconds if needed
    # if rmssd < 1: 
    rmssd = rmssd * 100
    sdnn = sdnn * 100

    # Prepare input for the model
    input_data = pd.DataFrame({'RMSSD': [rmssd], "SDNN": [sdnn]})
    prediction = model.predict(input_data)[0]

  
    if prediction == 1:  
        condition = 1  # Stress detected
        print(f"Stress detected! RMSSD ({rmssd:.2f} ms).")
        play_voice_prompt()
        # breathing_guidance()
    else:
        print(f"You are calm. RMSSD ({rmssd:.2f} ms). Keep going.")
        condition = 0  # Calm

    return condition

def play_voice_prompt():
  
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)    # Speed of speech
    engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)
    engine.say("Take a deep breath")
    engine.runAndWait()

