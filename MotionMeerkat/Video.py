import label
import os
import time
import cv2
import numpy as np
import urllib

class Video:
    def __init__(self,path,vidpath,keep=False,write=False):
        
        self.time = time.time() # start time
        self.path = path # url to video
        self.vidpath=vidpath # where to save video locally
        self.keep=keep # should video be deleted
        self.write=write #write an annotated video
        
    def label(self):
        self.labels=label.main(self.path)
        label.label_parse(self.labels)
    
    def download(self):
        #check if path exists
        #if not download file
        vidname=os.path.basename(self.path)
        print "Checking if %s exists" %(vidname)
        self.local_file= self.vidpath + vidname
        if not os.path.isfile(self.local_file):
            print "Downloading " + str(self.path)
            
            #if google cloud path
            
            if self.path[0:3] == "gs:":
                
                #bucket name
                bucket_name=self.path.split("/")[2]
                
                #file path
                f=self.path.split("/")[3:]
                source_blob_name='/'.join(f)
                
                destination_file_name=self.local_file
                
                #download from gcp
                label.download_blob(bucket_name, source_blob_name, 
                                   destination_file_name)
                
            else:
                #Any arbitrary public path 
                urllib.urlretrieve(self.path, self.local_file)
            print "Download complete "
    
    def show(self):
        
        #frame counter
        fcount=0

        if self.write:
            
            #load video
            cap = cv2.VideoCapture(self.local_file)            
            
            #Get frame rate
            fr=cap.get(5)
            orig_image = cap.read()[1]  
        
            #Get information about camera and image
            width = np.size(orig_image, 1)
            height = np.size(orig_image, 0)
            frame_size=(width, height)                  
        
            #create videowriter with annotated file name
            vidname=os.path.basename(self.path)
            self.annotated_file= self.vidpath + "/annotated_" + vidname                
            out = cv2.VideoWriter(self.annotated_file,cv2.VideoWriter_fourcc('D','I','V',"X"),float(fr),frame_size)                
            
        #play video
        cap = cv2.VideoCapture(self.local_file)
                
        while True:
            ret, frame = cap.read()  
            
            fcount=fcount+1 # add frame count
        
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
            if self.write:
                out.write(frame)
            
            #show frame - hit q to exit frame
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
    
    def cleanup(self):
        if not self.keep:
            os.remove(self.local_file)
        
        
        
        
        
        