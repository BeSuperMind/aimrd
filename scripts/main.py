import time
import pandas as pd
import pickle
import warnings
import os
from video_capture import capture_ppg_signal
from hrv_analysis import calculate_hrv_metrics
from feedback_system import provide_feedback
from realTimeGraph import PlotGraph

warnings.filterwarnings("ignore", category=UserWarning)

# File paths for storing the data
file_path1 = r"hrv_with_actualCondition.csv"
headers = ["RMSSD", "SDNN", "condition", "actualCondition"]

df = pd.DataFrame(columns=headers)
df.to_csv("graphHrv.csv", index=False)


def monitor_meditation_session(total_duration):
    interval=30
    intervals = total_duration // interval
    conditions = []  # To store conditions for each interval
    rmssd_values = []
    sdnn_values = []

    for i in range(intervals):
        print(f"Starting interval {i + 1} of {intervals}")
        
        ppg_signal = capture_ppg_signal(duration=interval)
        rmssd, sdnn = calculate_hrv_metrics(ppg_signal)
        
        rmssd_values.append(rmssd)
        sdnn_values.append(sdnn)
        
        print(f"Interval {i + 1}: RMSSD = {rmssd:.4f}, SDNN = {sdnn:.4f}")
        
        # Provide feedback based on the HRV metrics
        condition = provide_feedback(rmssd, sdnn)
        conditions.append(condition)
        
        time.sleep(1)  
    print("Meditation session complete. Thank you for participating!")
    
    while True:
        try:
            user_state = int(input("Enter your mental state (1 for stressed, 0 for calm): "))
            if user_state in [0, 1]:
                break
            else:
                print("Invalid input. Please enter 1 or 0.")
        except ValueError:
            print("Invalid input. Please enter a numeric value (1 or 0).")
    
    save_data(rmssd_values, sdnn_values, conditions, user_state)

def save_data(rmssd_values, sdnn_values, conditions, actual_condition):
    data_to_save = []
    for rmssd, sdnn, condition in zip(rmssd_values, sdnn_values, conditions):
        data_to_save.append({'RMSSD': rmssd*100, 'SDNN': sdnn*100, 'condition': condition, 'actualCondition': actual_condition})
    
    # Save the data to CSV
    df = pd.DataFrame(data_to_save)
    df.to_csv(file_path1, mode='a', index=False, header=not os.path.exists(file_path1))
    df.to_csv("graphHrv.csv", mode='a', index=False, header=not os.path.exists("graphHrv.csv"))

try:
     duration_minutes = int(input("Enter your meditation duration in minutes: "))
     total_duration = duration_minutes * 60  

     print(f"Starting meditation session for {duration_minutes} minutes with feedback every 30 seconds.")
     monitor_meditation_session(total_duration,)
     PlotGraph()
except ValueError:
    print("Invalid input. Please enter a numeric value for the meditation duration.")
