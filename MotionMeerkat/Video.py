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
        labels=label.main(self.path)
        label.label_parse(labels)
    
    def download(self):
        #check if path exists
        #if not download file
        vidname=os.path.basename(self.path)
        print "Checking if %s exists" %(vidname)
        self.local_file="staging/" + vidname
        if not os.path.isfile(self.local_file):
            print "Downloading..."
            #download
    
    def write(self):
        #play video
        cap = cv2.VideoCapture(self.local_file)
        
        #vidcap.set(cv2.CAP_PROP_POS_MSEC,20000) 
        while(cap.isOpened()):
            ret, frame = cap.read()  
            
            #get time
            msec=cap.get(cv2.CAP_PROP_POS_MSEC)
            print(msec)
            
            #which labels fall into this time
            
            #write label
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,"I'm a label",(10,500), font, 1,(255,255,255),2)            
            
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        
        
        
        
        