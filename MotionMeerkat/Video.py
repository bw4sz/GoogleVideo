import label
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
        vidname=os.path.basename(path)
        print "Checking if %s exists" %(vidname)
        self.local_file="staging/" + vidname
        if not os.path.isfile(self.local_file):
            print "Downloading..."
            #download
    def write(self):
        
        #play video
        cap = cv2.VideoCapture(self.local_file)
        
        while(cap.isOpened()):
            ret, frame = cap.read()        
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        
        
        
        
        