import cv2 
import numpy as np 
import datetime
from ultralytics import YOLO
import torch
from id_line_annotator import IdLineAnnotator
import supervision as sv 

#CSV_RESULT_PATH = 'dataset'
CSV_RESULT_PATH = '/content/drive/MyDrive/may1csv'

class VideoPlayer():
    class_to_str = {2:'car',3:'motorcycle',5:'bus',7:'truck'}

    def __init__(self, model = 'yolov8x.pt'):
        self.cap = cv2.VideoCapture() 
        self.video_time = None 
        self.video_path = None 

        self.line_zones = dict()
        self.points = []

        self.transport = dict() #хранит пересечения транспорта
        self.data = []
        
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = YOLO(model).to(device)
        self.model.fuse()       
    
    def set_playlist(self,playlist):
        self.playlist = playlist
        self.__run_video()

    def __run_video(self):
        if self.playlist:
            path, start_time = self.playlist[0]
            self.cap = cv2.VideoCapture(path)

            self.start_video_time = datetime.datetime.fromisoformat(start_time)
            self.video_path = path
            self.playlist.pop(0)
        
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
        results = self.model.track(source=frame,
                                    persist = True, 
                                    verbose=False,
                                    show=False,
                                    classes = [2,3,5,7], #car,motorcycle, bus, truck
                                    tracker='bytetrack.yaml')
        frame = results[0].plot()

        detections = sv.Detections.from_ultralytics(results[0])
        self.__lines_count(detections)

        return frame
    
    def __lines_count(self, detections:sv.Detections):
        
        if detections.tracker_id is not None:
            for line_id in self.line_zones.keys():
                lz = self.line_zones[line_id]
                crossed_in, crossed_out = lz.trigger(detections)
                crossed = crossed_in | crossed_out
                
                crossed_info = zip(detections[crossed].tracker_id, detections[crossed].class_id)

                for obj_id, class_id in crossed_info:
                    if obj_id not in self.transport.keys():
                        class_name = VideoPlayer.class_to_str[class_id]
                        self.transport[obj_id] = {'from':line_id, 'class':class_name}
                    else:
                        self.transport[obj_id]['to'] = line_id
                        self.transport[obj_id]['time'] = self.video_time  
                        self.data.append(self.transport[obj_id])


    def __display_lines(self,frame):
        line_annotator = IdLineAnnotator(thickness=2, text_thickness=2, text_scale=1)
        for line_id in self.line_zones.keys():
            lz = self.line_zones[line_id]
            frame = line_annotator.annotate(frame=frame, line_counter=lz, id = line_id)
        return frame 


    def __save_data(self):
        import csv
        import re
        import os
        headers = ['time','from', 'to', 'class']
        if self.data:            
            file_name = re.match(r'.+/(.*)\.mp4', self.video_path).group(1)
            print("SAVED",self.video_time,file_name)
            with open(f'{CSV_RESULT_PATH}/{file_name}.csv','a') as f:
                dw = csv.DictWriter(f,fieldnames=headers)
                if not os.path.isfile(f'{CSV_RESULT_PATH}/{file_name}.csv'):
                    dw.writeheader()
                dw.writerows(self.data)
                self.data.clear()
            


    def generate_frames(self):
        frame_num = 0
        while self.cap.isOpened():
            
            ret, frame = self.cap.read()
            
            if not ret and self.playlist:
                self.__save_data()
                self.__run_video()
                frame_num = 0 
                continue 

            if not ret:
                self.__save_data()
                return
            
            #minutes_of_video = self.cap.get(cv2.CAP_PROP_POS_MSEC)//1000
            #cv2.putText(frame,str(minutes_of_video//60)+":"+str(minutes_of_video%60),(25,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)

            if frame_num % 2000 == 0:
                print('CHECKPOINT')
                self.__save_data()

            frame = self.__display_time(frame)
            frame = self.__predict_frame(frame)
            frame = self.__display_lines(frame)

            
            frame_num += 1
            
            compression_level = 30
            buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY, compression_level])[1]
            frame = buffer.tobytes()
        
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
       
        
   
