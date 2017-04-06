import label
import os
import time
import cv2
import numpy
from google.cloud import storage
import urllib

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
            
            #if google cloud path
            
            if self.path[0:3] == "gs:":
                
                #bucket name
                bucket_name=self.path.split("/")[2]
                
                #file path
                f=p.split("/")[3:]
                source_blob_name='/'.join(f)
                
                destination_file_name=self.local_file
                
                #download from gcp
                label.download_blob(bucket_name, source_blob_name, 
                                   destination_file_name)
            else:
                #Any arbitrary public path 
                urllib.urlretrieve(self.local_file, self.local_file)

            
        #TODO check if its within google cloud, use gcs fuse or its own API, doesn't need . 
    
    def show(self,write=False):
        
        #frame counter
        fcount=0
        
        #play video
        cap = cv2.VideoCapture(self.local_file)
        
        #vidcap.set(cv2.CAP_PROP_POS_MSEC,20000) 
        while True:
            ret, frame = cap.read()  
            
            fcount=fcount+1
        
            #check for end of video
            if not ret:
                break
            #get time, API returns in microseconds, opencv in milliseconds
            msec=cap.get(cv2.CAP_PROP_POS_MSEC)*1000
            
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
                cv2.putText(frame,text,(10,100 + 40 * pcount), font, 1,(255,255,255),2)            
                pcount=pcount+1
               
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            if write:
                vidname=os.path.basename(self.path).split(".")[0]
                #just write a couple known frames to show the group
                if fcount in (10,870,2477):
                    annotated_file="staging/annotated_" + str(fcount) + vidname + ".jpg"                
                    cv2.imwrite(annotated_file, frame)
        
        cap.release()
        cv2.destroyAllWindows()
    
        
        
        
        
        
        