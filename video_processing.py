import cv2 
import numpy as np 
import datetime
from ultralytics import YOLO
import torch

class VideoPlayer():

    def __init__(self, model = 'yolov8n.pt'):
        self.cap = cv2.VideoCapture() 
        self.video_time = None 

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = YOLO(model).to(device)
        self.model.fuse()


    def run_video(self, path,start_time):
        self.cap = cv2.VideoCapture(path)
        self.start_video_time = start_time

    def __display_time(self, frame):
        elapsed_miliseconds = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        self.video_time = self.start_video_time + datetime.timedelta(milliseconds=elapsed_miliseconds)
        cv2.putText(frame,str(self.video_time),(25,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
        return frame 
    
    def __predict_frame(self, frame):
        results = self.model.track(source=frame,
                                    persist = True, 
                                    verbose=False,
                                    show=False,
                                    classes = [2,3,5,7], #car,motorcycle, bus, truck
                                    tracker='bytetrack.yaml')
        frame = results[0].plot()
        return frame
    

    def generate_frames(self):
        while self.cap.isOpened():

            ret, frame = self.cap.read()
            
            if not ret:
                return 
            
            frame = self.__predict_frame(frame)
            frame = self.__display_time(frame)
            

            compression_level = 30
            buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY, compression_level])[1]
            frame = buffer.tobytes()
        
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

   
