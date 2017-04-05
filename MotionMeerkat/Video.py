import label
import os
import time
import cv2
import numpy

class Video:
    def __init__(self,path):
        self.time = time.time()
        self.path = path
    
    def label(self):
        self.labels=label.main(self.path)
        label.label_parse(self.labels)
    
    def download(self):
        #check if path exists
        #if not download file
        vidname=os.path.basename(self.path)
        print "Checking if %s exists" %(vidname)
        self.local_file="staging/" + vidname
        if not os.path.isfile(self.local_file):
            print "Downloading..."
            #download
    
    def show(self,write=False):
        
        #write filename TODO
        if write:
            vidname=os.path.basename(self.path)
            self.annotated_file="staging/annotated_" + vidname
            
        #play video
        cap = cv2.VideoCapture(self.local_file)
        
        #vidcap.set(cv2.CAP_PROP_POS_MSEC,20000) 
        while True:
            ret, frame = cap.read()  
            
            #get time, API returns in microseconds, opencv in milliseconds
            msec=cap.get(cv2.CAP_PROP_POS_MSEC)*1000
            print(msec)
            
            #which labels fall into this time
            labels_to_write=list()
            
            labelData = self.labels['response']['annotationResults'][0]['labelAnnotations']
            for frame_label in labelData:
                if 'locations' not in frame_label:
                    print ('Error in label detection: ' + frame_label['description'])
                else:
                    locations = frame_label['locations']
                    for location in locations:
                        if 'segment' not in location:
                            print 'Missing segment.'
                        else:
                            segment = location['segment']
                            startTime = segment.get('startTimeOffset', '0')
                            endTime = segment.get('endTimeOffset', '0')
                            if msec > int(startTime) and msec < int(endTime):
                                labels_to_write.append(str(frame_label['description']))

            #write labels
            font = cv2.FONT_HERSHEY_SIMPLEX
            
            #position counter
            pcount=0
            for text in labels_to_write:
                cv2.putText(frame,text,(10,100 + 40 * pcount), font, 1,(0,0,0),2)            
                pcount=pcount+1
                
            cv2.imshow('frame',frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
        
        
        
        
        
        