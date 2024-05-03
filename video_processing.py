import cv2 
import supervision as sv 
import numpy as np 

class VideoPlayer():
    black_image = img = 255*(np.ones((350, 700, 3), dtype = np.uint8))

    def __init__(self):
        self.cap = cv2.VideoCapture() 

    def run_video(self, path):
        self.cap = cv2.VideoCapture(path)

    def generate_frames(self):
        
        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if not ret:
                frame = VideoPlayer.black_image
                self.cap.release()
                
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

