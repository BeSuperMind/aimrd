import cv2
import asyncio
import numpy as np
from tensorflow.keras.models import load_model
from graph import plot_graph
from text_to_speech import text_to_speech, text_to_speech_async  
from pygame import mixer
from drowziness import DrowsinessCheck
from start import starter

# Initialize pygame mixer and load alarm sound
mixer.init()

# Load the new combined model for emotion and eye detection
combined_model = load_model('emotion_eye_combined_model_with_200_epochs.h5')

# Load Haar Cascade classifiers for face and eye detection
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
leye = cv2.CascadeClassifier('haar cascade files/haarcascade_lefteye_2splits.xml')
reye = cv2.CascadeClassifier('haar cascade files/haarcascade_righteye_2splits.xml')

# Initialize variables for eye detection
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
count = 0
score = 0

# Initialize variables for plotting the graph
moving_count = 0
stationary_count = 0

# Emotion labels and eye status labels
labels_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise'}

# Initialize variables for face movement detection
prev_face_position = None
state = 'Not moving'

# Function to detect drowsiness
async def handle_drowsiness(frame, mixer, drowsy_detect):
    drowsy_check = await drowsy_detect.g_vision(frame)
    
    if 'Drowsy' in drowsy_check and 'Not Drowsy' not in drowsy_check:
        text_to_speech("Hey, you can't sleep during meditation")
    elif drowsy_check is None:
        print('Skipping drowsiness check as it is already in progress or not detected.')
    else:
        print('Drowsiness not detected.')

# Main loop for detection and prediction
async def main_loop(mixer):
    global prev_face_position, font, count, score, moving_count, stationary_count
    movement_threshold = 10

    await text_to_speech_async("Let's start meditating. Opening camera, make yourself ready.")
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        print("Error: Could not open camera.")
        return 

    drowsy_detect = DrowsinessCheck()

    try:
        frame_count = 0
        while True:
            ret, frame = video.read()
            frame_count += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces
            faces = faceDetect.detectMultiScale(gray, 1.3, 3)
            left_eye = leye.detectMultiScale(gray)
            right_eye = reye.detectMultiScale(gray)

            # Initialize face position for movement detection
            current_face_position = None

            for (x, y, w, h) in faces:
                current_face_position = (x, y, w, h)
                sub_face_img = gray[y:y+h, x:x+w]
                resized_face = cv2.resize(sub_face_img, (48, 48))
                normalized_face = resized_face / 255.0
                reshaped_face = np.reshape(normalized_face, (1, 48, 48, 1))
                break

            if len(faces) == 0:
                reshaped_face = np.zeros((1, 48, 48, 1))  # Default blank face if none detected

            # Eye input processing
            eye_img = None  # Initialize as None

            # Process left eye
            for (lx, ly, lw, lh) in left_eye:
                eye_img = gray[ly:ly+lh, lx:lx+lw]
                eye_img = cv2.resize(eye_img, (24, 24))
                eye_img = eye_img / 255.0
                eye_img = np.reshape(eye_img, (1, 24, 24, 1))
                break

            # If no left eye detected, try right eye
            if eye_img is None:
                for (rx, ry, rw, rh) in right_eye:
                    eye_img = gray[ry:ry+rh, rx:rx+rw]
                    eye_img = cv2.resize(eye_img, (24, 24))
                    eye_img = eye_img / 255.0
                    eye_img = np.reshape(eye_img, (1, 24, 24, 1))
                    break

            if eye_img is None:
                eye_img = np.zeros((1, 24, 24, 1))

            # Model prediction
            emotion_output, eye_output = combined_model.predict([reshaped_face, eye_img])
            emotion_label = np.argmax(emotion_output, axis=1)[0]
            emotion_text = labels_dict[emotion_label]
            eye_state = 'Close' if eye_output[0] < 0.5 else 'Open'

            if eye_state == 'Close':
                score = max(score - 1, 0)
                cv2.putText(frame, "Concentrating", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)  
            else:
                score += 1
                cv2.putText(frame, "Not Concentrating", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            score = min(score, 7)

            try:
                if score >= 5:
                    await text_to_speech_async('Please concentrate.')
            except Exception as e:
                print(f'Audio error encountered: {e}')

            # Movement detection logic
            if current_face_position is not None:
                (x, y, w, h) = current_face_position
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                if prev_face_position is not None:
                    distance = np.linalg.norm(np.array(current_face_position[:2]) - np.array(prev_face_position[:2]))

                    if distance > movement_threshold:
                        state = 'Moving'
                        color = (0, 0, 255)
                        moving_count += 1
                        await text_to_speech('Please stop moving.')
                    else:
                        state = 'Not moving'
                        color = (0, 255, 0)
                        stationary_count += 1
                else:
                    state = 'Not moving'

                prev_face_position = current_face_position

            else:
                state = 'Not moving'
                prev_face_position = None

            cv2.putText(frame, f"Emotion: {emotion_text}, Eyes: {eye_state}, State: {state}", (x, y - 30), font, 0.8, (0, 255, 255), 2)
            cv2.imshow("Frame", frame)

            if frame_count % 30 == 0:
                await handle_drowsiness(frame, mixer, drowsy_detect)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                video.release()
                cv2.destroyAllWindows()
                break

        plot_graph(stationary_count, moving_count)

    except Exception as e:
        print(f'Error Encounter: {e}')

async def app(mixer):
    response = starter(mixer)
    if response == 'started':
        await main_loop(mixer)
    elif response == '503':
        print('No internet connection.')
    elif response == 'error':
        print('Some error encountered.')
    elif response == 'exit':
        print('Exiting...')
        exit()
    else:
        pass

asyncio.run(app(mixer))
