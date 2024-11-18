import json
import base64
import cv2
import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.staticfiles import finders
from tensorflow.keras.models import load_model

class VideoConsumerDL(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.capture = None
        self.stream_running = False

        combined_model_raw = finders.find('emotion_eye_combined_model_with_200_epochs.h5')
        face_detection_harrcascade_file = finders.find('haarcascade_frontalface_default.xml')
        leye_detecttion_harrcascade_file = finders.find('haarcascade_lefteye_2splits.xml')
        reye_detecttion_harrcascade_file = finders.find('haarcascade_righteye_2splits.xml')

        self.combined_model = load_model(combined_model_raw)
        self.faceDetect= cv2.CascadeClassifier(face_detection_harrcascade_file)
        self.leye = cv2.CascadeClassifier(leye_detecttion_harrcascade_file)
        self.reye= cv2.CascadeClassifier(reye_detecttion_harrcascade_file)

        self.font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        self.score = 0
        self.moving_count = 0
        self.stationary_count = 0
        self.labels_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise'}
        
        self.movement_threshold = 15
        self.prev_face_position = None
        self.state = 'Not moving'
        self.frame_count = 0

        self.current_face_position = None
        self.x, self.y, self.w, self.h = None, None, None, None  # Initialize face coordinates
        self.Audio_guidance = ''

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
        print('Data recieved in DL')
        if 'frame_data' in data:
            # Decode the received frame from base64
            frame_data = data['frame_data']
            img_data = base64.b64decode(frame_data)
            nparr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Process the frame (for example, face detection)
            processed_frame, Audio = self.predict_EEM(frame) # Emotion, Eye State, Movement

            # Encode the processed frame back to base64
            _, buffer = cv2.imencode('.jpg', processed_frame)
            processed_frame_base64 = base64.b64encode(buffer).decode('utf-8')

            # Send the processed frame back to the frontend
            await self.send(text_data=json.dumps({
                'processed_frame': processed_frame_base64,
                'Audio': Audio
            }))

    def predict_EEM(self, frame):
            self.Audio_guidance = ''
            self.frame_count += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.faceDetect.detectMultiScale(gray, 1.3, 3)
            left_eye = self.leye.detectMultiScale(gray)
            right_eye = self.reye.detectMultiScale(gray)

            

            for (self.x, self.y, self.w, self.h) in faces:
                print(faces)
                self.current_face_position = (self.x, self.y, self.w, self.h)
                sub_face_img = gray[self.y:self.y+self.h, self.x:self.x+self.w]
                resized_face = cv2.resize(sub_face_img, (48, 48))
                normalized_face = resized_face / 255.0
                reshaped_face = np.reshape(normalized_face, (1, 48, 48, 1))
                break

            if len(faces) == 0:
                reshaped_face = np.zeros((1, 48, 48, 1))

            eye_img = None
            for (lx, ly, lw, lh) in left_eye:
                eye_img = gray[ly:ly+lh, lx:lx+lw]
                eye_img = cv2.resize(eye_img, (24, 24))
                eye_img = eye_img / 255.0
                eye_img = np.reshape(eye_img, (1, 24, 24, 1))
                break

            if eye_img is None:
                for (rx, ry, rw, rh) in right_eye:
                    eye_img = gray[ry:ry+rh, rx:rx+rw]
                    eye_img = cv2.resize(eye_img, (24, 24))
                    eye_img = eye_img / 255.0
                    eye_img = np.reshape(eye_img, (1, 24, 24, 1))
                    break

            if eye_img is None:
                eye_img = np.zeros((1, 24, 24, 1))

            emotion_output, eye_output = self.combined_model.predict([reshaped_face, eye_img])
            emotion_label = np.argmax(emotion_output, axis=1)[0]
            emotion_text = self.labels_dict[emotion_label]
            eye_state = 'Close' if eye_output[0] < 0.5 else 'Open'

            if eye_state == 'Close':
                if self.x is not None and self.y is not None:
                    cv2.putText(frame, "Concentrating", (self.x, self.y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    
            else:
                if self.x is not None and self.y is not None:
                    cv2.putText(frame, "Not Concentrating", (self.x, self.y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
                    self.Audio_guidance = 'Keep your eyes closed and be with your breath'

            if self.current_face_position is not None:
                (self.x, self.y, self.w, self.h) = self.current_face_position
                cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (255, 0, 0), 2)

                if self.prev_face_position is not None:
                    distance = np.linalg.norm(np.array(self.current_face_position[:2]) - np.array(self.prev_face_position[:2]))
                    if distance > self.movement_threshold:
                        self.state = 'Moving'
                        color = (0, 0, 255)
                        self.moving_count += 1
                        self.Audio_guidance = 'Please stay still, be wit your breath'
                    else:
                        self.state = 'Not moving'
                        color = (0, 255, 0)
                        self.stationary_count += 1
                       
                else:
                    self.state = 'Not moving'

                self.prev_face_position = self.current_face_position

            else:
                self.state = 'Not moving'
                self.prev_face_position = None

            if self.x is not None and self.y is not None:
                cv2.putText(frame, f"Emotion: {emotion_text}, Eyes: {eye_state}, State: {self.state}", (self.x, self.y - 30), self.font, 0.8, (0, 255, 255), 2)

            

            return frame, self.Audio_guidance
    
