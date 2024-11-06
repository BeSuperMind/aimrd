from video_capture import capture_ppg_signal
from hrv_analysis import calculate_hrv_metrics
from feedback_system import provide_feedback
from preprocessing import preprocess_signal
from realTimeGraph import PlotGraph
import os
import time

# if __name__ == "__main__":
#     ppg_signal = capture_ppg_signal(duration=30)
#     filtered_ppg_signal = preprocess_signal(ppg_signal)
#     rmssd, sdnn = calculate_hrv_metrics(filtered_ppg_signal)
#     print(f"RMSSD: {rmssd:.4f}, SDNN: {sdnn:.4f}")
#     provide_feedback(rmssd,sdnn)
       
def monitor_meditation_session(total_duration, interval=30):
    intervals = total_duration // interval
    for i in range(intervals):
        print(f"Starting interval {i + 1} of {intervals}")
        
        ppg_signal = capture_ppg_signal(duration=interval)
        
        filtered_ppg_signal = preprocess_signal(ppg_signal)
        rmssd, sdnn = calculate_hrv_metrics(filtered_ppg_signal)
        
        print(f"Interval {i + 1}: RMSSD = {rmssd:.4f}, SDNN = {sdnn:.4f}")
        
        provide_feedback(rmssd, sdnn)

        time.sleep(1)
        
    print("Meditation session complete. Thank you for participating!")

if __name__ == "__main__":
   
    try:
        duration_minutes = int(input("Enter your meditation duration in minutes: "))
        total_duration = duration_minutes * 60  

        print(f"Starting meditation session for {duration_minutes} minutes with feedback every 30 seconds.")
        monitor_meditation_session(total_duration=total_duration, interval=30)
        PlotGraph()
    except ValueError:
        print("Invalid input. Please enter a numeric value for the meditation duration.")  