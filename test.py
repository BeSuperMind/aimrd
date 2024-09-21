import cv2
import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt

model = load_model('model_file_200epochs.h5')

video = cv2.VideoCapture(0)

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

labels_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise'}

# Initialize variables to store the previous position of the bounding box
prev_x, prev_y, prev_w, prev_h = None, None, None, None

# Threshold for movement detection
movement_threshold = 7

# Counters for time spent in stationary and moving states
stationary_count = 0
moving_count = 0

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

        # Detect movement by comparing the current and previous positions of the face
        if prev_x is not None and prev_y is not None:
            dx = abs(x - prev_x)
            dy = abs(y - prev_y)
            dw = abs(w - prev_w)
            dh = abs(h - prev_h)

            # Check if the change in any direction exceeds the movement threshold
            if dx > movement_threshold or dy > movement_threshold or dw > movement_threshold or dh > movement_threshold:
                moving_count += 1
                cv2.putText(frame, "Moving", (x, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                stationary_count += 1
                cv2.putText(frame, "Stationary", (x, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Draw the bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, labels_dict[label], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Update previous coordinates and size for comparison in the next frame
        prev_x, prev_y, prev_w, prev_h = x, y, w, h

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

# Release the video capture and destroy windows
video.release()
cv2.destroyAllWindows()

# Plotting the stationary and moving time
total_frames = stationary_count + moving_count
stationary_percentage = (stationary_count / total_frames) * 100 if total_frames > 0 else 0
moving_percentage = (moving_count / total_frames) * 100 if total_frames > 0 else 0

# Data for plotting
labels = ['Stationary', 'Moving']
times = [stationary_percentage, moving_percentage]

# Plotting the bar graph
plt.figure(figsize=(6, 4))
plt.bar(labels, times, color=['green', 'red'])
plt.xlabel('State')
plt.ylabel('Time Percentage (%)')
plt.title('Time Spent Stationary vs Moving')
plt.ylim(0, 100)
plt.show()
