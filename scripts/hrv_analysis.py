import sys
import os
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from preprocessing import preprocess_signal  
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")  
def calculate_hrv_metrics(ppg_signal, fs=30):
    """
    Calculate HRV metrics from a PPG signal.

    Parameters:
    - ppg_signal (np.ndarray): 1D array of PPG signal.
    - fs (int): Sampling frequency of the PPG signal (default is 30 Hz).

    Returns:
    - tuple: (RMSSD, SDNN) values calculated from the PPG signal.
    """
   

    filtered_signal = preprocess_signal(ppg_signal)  
    peaks, _ = find_peaks(filtered_signal, distance=fs//4)  

    if len(peaks) < 2:
        raise ValueError("Not enough peaks detected to calculate HRV metrics.")

    ibi = np.diff(peaks) / fs  # Inter-Beat Intervals in seconds
    rmssd = np.sqrt(np.mean(np.square(np.diff(ibi))))  # RMSSD calculation
    sdnn = np.std(ibi)  # SDNN calculation

    return rmssd, sdnn


