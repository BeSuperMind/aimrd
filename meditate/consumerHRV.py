import json
import base64
import cv2
import numpy as np
import pickle
import pandas as pd
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.staticfiles import finders
from scipy.signal import butter, filtfilt
from scipy.signal import find_peaks
from django.contrib.staticfiles import finders
import pickle
import pandas as pd

class VideoConsumerHRV(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.capture = None
        self.stream_running = False
        self.frameCount = 0
        self.signal = []
        self.filtered_signal = []
        self.model_file = finders.find('ppgStress.pkl')
        with open(self.model_file, 'rb') as file:
            self.model = pickle.load(file)
        self.Audio_text = ''
        self.rmssd_values = []
        self.sdnn_values = []



    async def connect(self):
        self.group_name = 'video_group'

        # Join the WebSocket group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

        # Start video capture
        self.capture = cv2.VideoCapture(0)  # 0 for default camera
        self.stream_running = True

    async def disconnect(self, close_code):
        # Stop video streaming
        self.stream_running = False
        if self.capture:
            self.capture.release()

        # Destroy OpenCV window when disconnected
        cv2.destroyAllWindows()

        # Leave the WebSocket group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if 'frame_data' in data:
            # Decode the received frame from base64
            frame_data = data['frame_data']
            img_data = base64.b64decode(frame_data)
            nparr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Process the frame (for example, face detection)
            processed_frame, Audio = self.analyse_HRV(frame=frame)

            
            Audio == '' if self.Audio_text == 0 else self.Audio_text

            # Encode the processed frame back to base64
            _, buffer = cv2.imencode('.jpg', processed_frame)
            processed_frame_base64 = base64.b64encode(buffer).decode('utf-8')

            # Send the processed frame back to the frontend
            await self.send(text_data=json.dumps({
                'processed_frame': processed_frame_base64,
                'Audio': Audio
            }))

    def analyse_HRV(self, frame):
        print(self.frameCount)
        self.frameCount += 1
        green_channel = frame[:, :, 1]  
        mean_intensity = np.mean(green_channel)
        self.signal = np.append(self.signal, mean_intensity)
        cv2.putText(frame, "Concentrating", (50,50) ,cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        if self.frameCount> 901:
            self.frameCount = self.frameCount % 900

        if self.frameCount > 900:
            self.signal = np.array(self.signal)
            signal_to_process = self.signal
            self.filtered_signal = self.preprocess_signal(signal_to_process)
            peaks, _ = find_peaks(self.filtered_signal, 7) 
            ibi = np.diff(peaks) / 30  # Inter-Beat Intervals in seconds
            rmssd = np.sqrt(np.mean(np.square(np.diff(ibi))))  # RMSSD calculation
            sdnn = np.std(ibi)  # SDNN calculation 

            self.rmssd_values.append(rmssd)
            self.sdnn_values.append(sdnn)
            self.mode = self.predict_HRV(rmssd, sdnn)
            return  frame , self.mode
        
        return frame, None
        

    def preprocess_signal(self,ppg_signal):
   
        nyquist = 0.5 * 30 # interval seconds
        low = 0.7 / nyquist # 0.7 low cut
        high = 3.5 / nyquist # 3.5 high cut
        b, a = butter(5, [low, high], btype='band') # order
        filtered_signal = filtfilt(b, a, ppg_signal)
        return filtered_signal

    def predict_HRV(self, rmssd, sdnn):
            # Prepare input for the model
        input_data = pd.DataFrame({'RMSSD': [rmssd], "SDNN": [sdnn]})
        prediction = self.model.predict(input_data)[0]

        # Determine the condition based on the prediction
        if prediction == 1:  
            condition = 1  # Stress detected
            print(f"Stress detected! RMSSD ({rmssd:.2f} ms).")
            self.Audio_text = 'Keep your attention to your breath'
            # breathing_guidance()
        else:
            print(f"You are calm. RMSSD ({rmssd:.2f} ms). Keep going.")
            condition = 0  # Calm

        return condition, 

   