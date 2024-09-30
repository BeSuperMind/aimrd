import cv2
import numpy as np
import asyncio
from keras.models import load_model
import matplotlib.pyplot as plt
from field import BlueField  # Import the BlueField class
from speech import text_to_speech  # Ensure this function is async

# Load the pre-trained model
model = load_model('model_file_200epochs.h5')

# Haar Cascade for face detection
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Emotion labels
labels_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise'}

# Initialize counters
stationary_count = 0
moving_count = 0

# Threshold for movement classification
movement_threshold = 10

# Global variable for speaking detection
speak = False

# Create an async function to handle speaking
async def handle_speech():
    global speak
    if not speak:
        speak = True  # Set speak to True to prevent another thread
        status = await text_to_speech('Please stop moving.')  # Trigger speech
        if status == 200:
            speak = False

# Start video capture
video = cv2.VideoCapture(0)

# Create the BlueField instance and create the field
blue_field = BlueField()
(start_point, end_point) = blue_field.create_field(video, faceDetect)

# Start the actual prediction and state detection after creating the blue field
async def main_loop():
    global stationary_count, moving_count

    while True:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 3)

        for x, y, w, h in faces:
            sub_face_img = gray[y:y+h, x:x+w]
            resized = cv2.resize(sub_face_img, (48, 48))
            normalize = resized / 255.0
            reshaped = np.reshape(normalize, (1, 48, 48, 1))
            result = model.predict(reshaped)
            label = np.argmax(result, axis=1)[0]

            # Drawing the blue rectangle representing the maximum boundary
            cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 2)

            # Check if the face is outside the max distance boundaries
            if (x < start_point[0] or x + w > end_point[0] or 
                y < start_point[1] or y + h > end_point[1]):
                
                moving_count += 1
                await handle_speech()  # Call the speech function asynchronously
                state = "Moving"
                color = (0, 0, 255)  # Red for moving
            else:
                stationary_count += 1
                state = "Stationary"
                color = (0, 255, 0)  # Green for stationary

            # Draw the face rectangle with the appropriate color
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{labels_dict[label]}, {state}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Display the frame
        cv2.imshow("Frame", frame)

        # Exit on 'q' key press
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

# Run the main loop asynchronously
async def run():
    await main_loop()

# Start the asynchronous event loop
asyncio.run(run())

# Release video capture and close windows
video.release()
cv2.destroyAllWindows()

# Plotting stationary vs moving time
total_frames = stationary_count + moving_count
stationary_percentage = (stationary_count / total_frames) * 100 if total_frames > 0 else 0
moving_percentage = (moving_count / total_frames) * 100 if total_frames > 0 else 0

# Plot bar graph
labels = ['Stationary', 'Moving']
times = [stationary_percentage, moving_percentage]

plt.figure(figsize=(6, 4))
plt.bar(labels, times, color=['green', 'red'])
plt.xlabel('State')
plt.ylabel('Time Percentage (%)')
plt.title('Time Spent Stationary vs Moving')
plt.ylim(0, 100)
plt.show()
