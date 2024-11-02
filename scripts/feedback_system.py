import time
import pandas as pd
import pickle
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Modify the function to include dynamic threshold setting

model_file = 'ppgStress.pkl'
with open(model_file, 'rb') as file:
    model = pickle.load(file)

def provide_feedback(rmssd,sdnn, baseline_rmssd=None):
    """
    Provide feedback based on RMSSD value.
    
    Parameters:
    - rmssd (float): The calculated RMSSD value in seconds.
    - baseline_rmssd (float, optional): The user's baseline RMSSD if available.
    - population (str): The target population ("general", "athlete", "older", etc.).
    """
   
   
    
    # Convert RMSSD to milliseconds
    if rmssd < 1: 
        rmssd = rmssd * 100

    input_data = pd.DataFrame({'RMSSD': [rmssd],"SDNN":[sdnn]})

    prediction = model.predict(input_data)[0]


    if prediction == 1:  
        print(f"Stress detected! RMSSD ({rmssd:.2f} ms).")
        breathing_guidance()
        return 'stress'
    else:  # Assuming '0' indicates calm
        print(f"You are calm. RMSSD ({rmssd:.2f} ms). Keep going.")
        return 'calm'

   

def breathing_guidance():
    """
    Guide the user through a breathing exercise to reduce stress.
    """
    print("Let's take a few deep breaths together:")
    for _ in range(3):  # Suggest 3 deep breaths
        print("Inhale deeply through your nose for 4 seconds...")
        time.sleep(4)  # Simulating the inhale duration
        print("Hold for 4 seconds...")
        time.sleep(4)  # Simulating the hold duration
        print("Exhale slowly through your mouth for 6 seconds...")
        time.sleep(6)  # Simulating the exhale duration
    print("Great job! You can return to your activity.")


