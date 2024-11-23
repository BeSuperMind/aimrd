import sys
import os
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from preprocessing import preprocess_signal  
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")  
def calculate_hrv_metrics(ppg_signal):
    fs=30
    filtered_signal = preprocess_signal(ppg_signal)  
    peaks, _ = find_peaks(filtered_signal, distance=fs//2) 
    rr_intervals = np.diff(peaks) / fs  #
    heart_rate = 60 / rr_intervals  # Beats per minute (BPM)
    hr_mean=np.mean(heart_rate)
    #print(f"Estimated Heart Rate: {heart_rate:.2f} BPM") 
    print(f"Mean Heart Rate: {hr_mean:.2f} BPM") 

    if len(peaks) < 2:
        raise ValueError("Not enough peaks detected to calculate HRV metrics.")

    ibi = rr_intervals
    rmssd = np.sqrt(np.mean(np.square(np.diff(ibi)))) 
    sdnn = np.std(ibi)  

    return rmssd, sdnn,hr_mean


