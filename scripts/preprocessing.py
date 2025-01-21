import numpy as np
from scipy.signal import butter, filtfilt

def preprocess_signal(ppg_signal, lowcut=0.7, highcut=3.5, fs=30, order=5):
    # Normalize signal to zero mean and unit variance (optional)
    ppg_signal = (ppg_signal - np.mean(ppg_signal)) / np.std(ppg_signal)
    
    # Design the bandpass filter
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    
    # Apply the bandpass filter
    filtered_signal = filtfilt(b, a, ppg_signal)
    
    return filtered_signal
