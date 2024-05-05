import cv2 
import numpy as np 
import datetime
from ultralytics import YOLO
import torch
from id_line_annotator import IdLineAnnotator
import supervision as sv 

class VideoPlayer():

    def __init__(self, model = 'yolov8n.pt'):
        self.cap = cv2.VideoCapture() 
        self.video_time = None 

        self.line_zones = dict()
        self.points = []

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = YOLO(model).to(device)
        self.model.fuse()


    def run_video(self, path,start_time):
        self.cap = cv2.VideoCapture(path)
        self.start_video_time = start_time

    def add_line(self,x1,y1,x2,y2,width,height):
        self.add_point(x1,y1,width, height)
        self.add_point(x2,y2,width, height)

    def add_point(self,x,y,width,height):
        orig_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        orig_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        Sx = orig_width/width
        Sy = orig_height/height

        point = sv.Point(x,y)
        point.x = round(Sx * point.x)
        point.y = round(Sy * point.y)
        
        self.points.append(point)

        if len(self.points) == 2:
            lz = sv.LineZone(start=self.points[0], end=self.points[1])
            new_id = len(self.line_zones)
            self.line_zones[new_id] = lz
            self.points.clear()

    def __display_time(self, frame):
        elapsed_miliseconds = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        self.video_time = self.start_video_time + datetime.timedelta(milliseconds=elapsed_miliseconds)
        cv2.putText(frame,str(self.video_time),(25,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
        return frame 
    
    def __predict_frame(self, frame):
        tracker = sv.ByteTrack()
        results = self.model.track(source=frame,
                                    persist = True, 
                                    verbose=False,
                                    show=False,
                                    classes = [2,3,5,7], #car,motorcycle, bus, truck
                                    tracker='bytetrack.yaml')
        frame = results[0].plot()

        detections = sv.Detections.from_ultralytics(results[0])
        detections = tracker.update_with_detections(detections)
        self.__lines_count(detections)

        return frame
    
    def __lines_count(self, detections:sv.Detections):
        for line_id in self.line_zones.keys():
            lz = self.line_zones[line_id]
            crossed_in, crossed_out = lz.trigger(detections)
            print(line_id,':',  lz.in_count, lz.out_count)
            crossed = crossed_in | crossed_out
            #print(line_id, ":", objects_id)

    def __display_lines(self,frame):
        line_annotator = sv.LineZoneAnnotator(thickness=2, text_thickness=2, text_scale=1)
        for line_id in self.line_zones.keys():
            #frame = line_annotator.annotate(frame=frame, line_counter = self.line_zones[line_id], id=line_id)
            lz = self.line_zones[line_id]
            frame = line_annotator.annotate(frame=frame, line_counter=lz)
        return frame 

    def __display_lines2(self,frame):
        line_annotator = IdLineAnnotator(thickness=2, text_thickness=2, text_scale=1)
        for line_id in self.line_zones.keys():
            #frame = line_annotator.annotate(frame=frame, line_counter = self.line_zones[line_id], id=line_id)
            lz = self.line_zones[line_id]
            frame = line_annotator.annotate(frame=frame, line_counter=lz, id = line_id)
        return frame 

    def generate_frames(self):
        while self.cap.isOpened():

            ret, frame = self.cap.read()
            
            if not ret:
                return 
         
            frame = self.__display_time(frame)
            frame = self.__predict_frame(frame)
            frame = self.__display_lines2(frame)
            
            
            compression_level = 30
            buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY, compression_level])[1]
            frame = buffer.tobytes()

            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

   
