import pickle
import joblib
import time
import pandas as pd
import os
import warnings
import pyttsx3
warnings.filterwarnings("ignore", category=UserWarning)

# Load the model
# model_file = 'ppgStress.pkl'
# with open(model_file, 'rb') as file:
#     model = pickle.load(file)

loaded_model = joblib.load(r'rfWesad.pkl')

def provide_feedback(rmssd, sdnn,hr_mean):
    # Convert RMSSD to milliseconds if needed
    # if rmssd < 1: 
    rmssd = (rmssd * 1000)/2
    sdnn = (sdnn * 1000)/2
    # Prepare input for the model
    # input_data = pd.DataFrame({'RMSSD': [rmssd], "SDNN": [sdnn]})
    # prediction = model.predict(input_data)[0]

    input_data = pd.DataFrame({'HR_mean':[hr_mean],'RMSSD': [rmssd], "SDNN": [sdnn]})
    prediction = loaded_model.predict(input_data)[0]
    
    if prediction == 0:  
        condition = 1  # Stress detected
        print(f"Stress detected! RMSSD ({rmssd:.2f} ms).")
        play_voice_prompt()
        # breathing_guidance()
    else:
        condition = 0  # Calm
    return condition

def play_voice_prompt():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)    # Speed of speech
    engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)
    engine.say("Take a deep breath")
    engine.runAndWait()

