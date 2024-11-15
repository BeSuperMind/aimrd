import cv2
import numpy as np
import time

def capture_ppg_signal(duration=30, fps=30):
    cap = cv2.VideoCapture(0)
    signal = []
    
    total_frames = duration * fps
    frame_count = 0
    start_time = time.time()  

    while frame_count < total_frames:
        ret, frame = cap.read()
        if not ret:
            break
        
        green_channel = frame[:, :, 1]  
        mean_intensity = np.mean(green_channel)
        signal.append(mean_intensity)

        cv2.imshow('PPG Signal Capture', frame)
        
        
        elapsed_time = time.time() - start_time
        remaining_time = duration - elapsed_time
        print(f"Remaining time: {max(0, remaining_time):.1f} seconds", end='\r')  # Display remaining time

        frame_count += 1
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    return np.array(signal)