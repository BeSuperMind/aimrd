import time
import pandas as pd
import pickle
import warnings
import os
warnings.filterwarnings("ignore", category=UserWarning)

# Define the file path and load the existing CSV data
file_path = r"C:\Users\sam\CODEs\aimrd\hrv_with_actualCondition.csv"

# Load the model
model_file = 'ppgStress.pkl'
with open(model_file, 'rb') as file:
    model = pickle.load(file)

def provide_feedback(rmssd, sdnn, baseline_rmssd=None):
    """
    Provide feedback based on RMSSD and SDNN values.
    
    Parameters:
    - rmssd (float): The calculated RMSSD value in seconds.
    - sdnn (float): The calculated SDNN value.
    - baseline_rmssd (float, optional): The user's baseline RMSSD if available.
    """
   
    # Convert RMSSD to milliseconds if needed
    if rmssd < 1: 
        rmssd = rmssd * 100

    input_data = pd.DataFrame({'RMSSD': [rmssd], "SDNN": [sdnn]})
    prediction = model.predict(input_data)[0]

    # Determine the condition based on the prediction
    if prediction == 1:  
        condition = 1
        print(f"Stress detected! RMSSD ({rmssd:.2f} ms).")
        breathing_guidance()
    else:
        print(f"You are calm. RMSSD ({rmssd:.2f} ms). Keep going.")
        condition = 0
    
    # Get user input for actual condition
    while True:
        try:
            user_state = int(input("Enter your mental state (1 for stressed, 0 for calm): "))
            if user_state in [0, 1]:
                break
            else:
                print("Invalid input. Please enter 1 or 0.")
        except ValueError:
            print("Invalid input. Please enter a numeric value (1 or 0).")

    # Prepare data to save
    data_to_save = {'RMSSD': rmssd, 'SDNN': sdnn, 'condition': condition, 'actualCondition': user_state}
    df = pd.DataFrame([data_to_save])

    # Append to CSV file
    df.to_csv(file_path, mode='a', index=False, header=not os.path.exists(file_path))
    
    return condition

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