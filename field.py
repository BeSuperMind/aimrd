import cv2
import numpy as np
from text_to_speech import text_to_speech_async
from tensorflow.keras.models import load_model

class Demo:

    async def demo_field(self, video, mixer):
        movement_threshold = 10

        combined_model = load_model('emotion_eye_combined_model_with_200_epochs.h5')

        faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        leye = cv2.CascadeClassifier('haar cascade files/haarcascade_lefteye_2splits.xml')
        reye = cv2.CascadeClassifier('haar cascade files/haarcascade_righteye_2splits.xml')

        # Initialize variables for eye detection
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        score = 0

        # initialize variables for plotting the graph
        moving_count = 0
        stationary_count = 0

        # Emotion labels and eye status labels
        labels_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise'}

        # Initialize variables for face movement detection
        prev_face_position = None
        state = 'Not moving'
        frame_count = 0
        while True:
            ret, frame = video.read()
            frame_count += 1
            print('Camera is opening')
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
                eye_img = cv2.resize(eye_img, (24, 24))  # Resize eye to 24x24
                eye_img = eye_img / 255.0  # Normalize pixel values
                eye_img = np.reshape(eye_img, (1, 24, 24, 1))  # Reshape for model input
                break  # Take the first detected left eye

            # If no left eye detected, try right eye
            if eye_img is None:
                for (rx, ry, rw, rh) in right_eye:
                    eye_img = gray[ry:ry+rh, rx:rx+rw]
                    eye_img = cv2.resize(eye_img, (24, 24))  # Resize eye to 24x24
                    eye_img = eye_img / 255.0  # Normalize pixel values
                    eye_img = np.reshape(eye_img, (1, 24, 24, 1))  # Reshape for model input
                    break  # Take the first detected right eye

            # If no eyes detected, set a default eye image (like closed eyes)
            if eye_img is None:
                eye_img = np.zeros((1, 24, 24, 1))  # If no eye detected, use blank input

            # Model prediction
            emotion_output, eye_output = combined_model.predict([reshaped_face, eye_img])
            print('Predicting emotions')
            # Extract the emotion prediction
            emotion_label = np.argmax(emotion_output, axis=1)[0]
            emotion_text = labels_dict[emotion_label]
            print('emotions predicted')
            # Extract the eye state prediction
            eye_state = 'Close' if eye_output[0] < 0.5 else 'Open'  # Adjusted threshold for closed eyes

            # Check for concentration based on eye state
            if eye_state == 'Close':
                score = max(score - 1, 0)
                cv2.putText(frame, "Concentrating", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)  
            else:
                score += 1
                cv2.putText(frame, "Not Concentrating", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            print('Eye state checked')
            score = min(score, 7)
            # Trigger alarm if score exceeds threshold
            try:
                print('Checking condition of alarm to be played')
                if score >= 5:
                    await text_to_speech_async('Please concentrate.', mixer)
            except Exception as e:
                print(f'Audio error encountered: {e}')
            print('Alarm checked')

            # Movement detection logic
            if current_face_position is not None:
                # Draw bounding box around detected face
                (x, y, w, h) = current_face_position
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # Check if the face is moving by comparing its current and previous positions
                if prev_face_position is not None:
                    # Calculate the movement (Euclidean distance)
                    distance = np.linalg.norm(np.array(current_face_position[:2]) - np.array(prev_face_position[:2]))

                    # If the distance is above the threshold, mark as 'Moving'
                    if distance > movement_threshold:  # You can adjust the threshold based on your needs
                        state = 'Moving'
                        color = (0, 0, 255)  # Red
                        moving_count += 1
                        await text_to_speech_async('Please stop moving.', mixer)  # Trigger speech async
                    else:
                        state = 'Not moving'
                        color = (0, 255, 0)  # Green
                        stationary_count += 1
                else:
                    state = 'Not moving'  # Initial state when there is no previous position

                # Update the previous face position
                prev_face_position = current_face_position

            else:
                state = 'Not moving'
                prev_face_position = None

            # Display emotion, eye state, and movement state
            cv2.putText(frame, f"Emotion: {emotion_text}, Eyes: {eye_state}, State: {state}", (x, y - 30), font, 0.8, (0, 255, 255), 2)

            # Show frame
            cv2.imshow("Frame", frame)
            print('Ending part')

            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                video.release()
                cv2.destroyAllWindows()
                break
        
            print('Program ended')
            return