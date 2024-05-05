import supervision as sv 

class LineZonesCounter:
    def __init__(self):
        self.lines = dict()
        # для каждого id транспорта хранит id линии которые пересек транспорт 
        self.transport = dict() 


    def lines_count(self, time, detections:sv.Detections):
        if detections.tracker_id is not None:

            for line_id in self.line_zones.keys():
                lz = self.line_zones[line_id]
                crossed_in, crossed_out = lz.trigger(detections)
                crossed = crossed_in | crossed_out
                
                crossed_info = zip(detections[crossed].tracker_id, detections[crossed].class_id)

                for obj_id, class_id in crossed_info:
                    if obj_id not in self.transport.keys():
                        self.transport[obj_id] = {'from':line_id, 'class':class_id}
                    else:
                        self.transport[obj_id]['to'] = line_id
                        self.transport[obj_id]['time'] = time  
            
            print(self.transport)