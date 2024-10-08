from video_capture import capture_ppg_signal
from hrv_analysis import calculate_hrv_metrics
from feedback_system import provide_feedback

if __name__ == "__main__":
    ppg_signal = capture_ppg_signal(duration=30)
    rmssd, sdnn = calculate_hrv_metrics(ppg_signal)
    print(f"RMSSD: {rmssd:.4f}, SDNN: {sdnn:.4f}")
    provide_feedback(rmssd)
