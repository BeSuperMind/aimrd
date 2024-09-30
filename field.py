import cv2
import time 

class BlueField:
    def __init__(self):
        self.max_boundary_x1 = None
        self.max_boundary_y1 = None
        self.max_boundary_x2 = None
        self.max_boundary_y2 = None

    def create_field(self, video, face_detect):
        """Function to capture video for 5 seconds and create the blue field based on max distance."""
        start_time = time.time()

        while time.time() - start_time <= 5:
            ret, frame = video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detect.detectMultiScale(gray, 1.3, 3)
            
            for x, y, w, h in faces:
                # Set initial boundaries based on the first detected face
                if self.max_boundary_x1 is None:
                    self.max_boundary_x1, self.max_boundary_y1 = x, y
                    self.max_boundary_x2, self.max_boundary_y2 = x + w, y + h
                else:
                    # Update the maximum rectangle boundaries dynamically
                    self.max_boundary_x1 = min(self.max_boundary_x1, x)
                    self.max_boundary_y1 = min(self.max_boundary_y1, y)
                    self.max_boundary_x2 = max(self.max_boundary_x2, x + w)
                    self.max_boundary_y2 = max(self.max_boundary_y2, y + h)

            # Draw the blue rectangle dynamically
            if self.max_boundary_x1 is not None:
                cv2.rectangle(frame, 
                              (self.max_boundary_x1, self.max_boundary_y1), 
                              (self.max_boundary_x2, self.max_boundary_y2), 
                              (255, 0, 0), 
                              2)

            # Display text while creating the blue field
            cv2.putText(frame, "Creating Field", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.imshow("Frame", frame)
            
            # Exit on 'q' key press during the field creation
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        print(f"Max coordinates for blue field: ({self.max_boundary_x1}, {self.max_boundary_y1}), ({self.max_boundary_x2}, {self.max_boundary_y2})")
        return (self.max_boundary_x1, self.max_boundary_y1), (self.max_boundary_x2, self.max_boundary_y2)

