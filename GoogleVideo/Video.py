import cv2
import sys
import subprocess
import math
import os
import numpy as np
import csv
import time
import Crop
from operator import itemgetter
from itertools import groupby
from urlparse import urlparse
from google.cloud import storage
from Geometry import *
from VideoClip import VideoClip

from google.cloud.gapic.videointelligence.v1beta1 import enums
from google.cloud.gapic.videointelligence.v1beta1 import (
    video_intelligence_service_client)
from google.cloud.proto.videointelligence.v1beta1 import video_intelligence_pb2

    
class Video:
    def __init__(self,vid,args):
                
        #start time
        self.start_time=time.time()
        
        #store args from MotionMeerkat
        self.args=args
        self.args.video=vid
        
        #set descriptors
        self.frame_count=0
        
        #Box Annotations dictionary
        self.annotations={}
        
        ##Google Properties##
        #Google Credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = args.google_account
            
        #Set Google Credentials and Properties
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = args.google_account
        
        ##Cloud Video Properties
        self.video_client = (video_intelligence_service_client.VideoIntelligenceServiceClient())
        self.features = [enums.Feature.LABEL_DETECTION]
        self.video_context = video_intelligence_pb2.VideoContext()
        self.video_context.stationary_camera = True
        self.video_context.label_detection_mode = video_intelligence_pb2.FRAME_MODE        
        
        #Google Cloud Storage
        storage_client = storage.Client()
        
        #TODO check if bucket exists.
        self.bucket = storage_client.get_bucket(args.bucket)
                
        #Video clip annontations
        self.clip_labels={}
        
        #create local output directory            
        normFP=os.path.normpath(self.args.input)
        (filepath, filename)=os.path.split(normFP)
        (shortname, extension) = os.path.splitext(filename)
        (_,IDFL) = os.path.split(filepath) 
        
        if self.args.batch:
            self.file_destination=os.path.join(self.args.output,shortname)        
        else:
            self.file_destination=os.path.join(self.args.output,IDFL)
            self.file_destination=os.path.join(self.file_destination,shortname)        

        if not os.path.exists(self.file_destination):
            os.makedirs(self.file_destination)        
            
        ##VIDEO PROPERTIES
        #read video
        self.cap=cv2.VideoCapture(self.args.video)
        
        #set frame frate
        self.frame_rate=round(self.cap.get(5))
        
        #background subtraction
        self.background_instance=self.create_background() 
        
        #Detector almost always returns first frame
        self.IS_FIRST_FRAME = True    
        
        #Motion History, boolean state of Motion
        self.MotionHistory=[]
                
    def analyze(self):
         
        if self.args.show: 
            cv2.namedWindow("Motion_Event")
            cv2.namedWindow("Background")            
            
        while True:

            #read frame
            ret,self.original_image=self.read_frame()
            
            if not ret:
                #end time
                self.end_time=time.time()
                break
            
            self.frame_count+=1
            
            #adapt settings of mogvariance to keep from running away
            self.adapt()
            
            #background subtraction
            self.background_apply()
                                            
            #skip the first frame after adding it to the background.
            if self.IS_FIRST_FRAME:
                print("Skipping first frame")
                self.IS_FIRST_FRAME=False
                self.MotionHistory.append(False)
                continue
            
            #contour analysis
            self.countours=self.find_contour()
            
            #Next frame if no contours
            if len(self.contours) == 0 :
                self.MotionHistory.append(False)
                continue
              
            #bounding boxes
            bounding_boxes = self.cluster_bounding_boxes(self.contours)
            
            #Next frame if no bounding boxes
            if len(bounding_boxes) == 0 :
                self.MotionHistory.append(False)
                continue

            #minimum box size
            width = np.size(self.original_image, 1)
            height = np.size(self.original_image, 0)
            area = width * height
            
            #remove if smaller than min size
            remaining_bounding_box=[]
            
            for bounding_box in bounding_boxes:
                if area * self.args.size < bounding_box.h * bounding_box.w:
                    remaining_bounding_box.append(bounding_box)
            
            #next frame is no remaining bounding boxes
            if len(remaining_bounding_box)==0:
                self.MotionHistory.append(False)
                continue
                            
            self.annotations[self.frame_count] = remaining_bounding_box
            
            #store frame history
            print("Motion")
            self.MotionHistory.append(True)
            
            if self.args.show:
                for bounding_box in remaining_bounding_box:
                    if self.args.draw: 
                        cv2.rectangle(self.original_image, (bounding_box.x, bounding_box.y), (bounding_box.x+bounding_box.w, bounding_box.y+bounding_box.h), (0,0,255), 2)
                    cv2.imshow("Motion_Event", self.original_image)
                    cv2.waitKey(0)
        cv2.destroyAllWindows()            
        
    def read_frame(self):
        
        #read frame
        ret,image=self.cap.read()
        
        if not ret:
            return((ret,image))
        
        #set crop settings if first frame
        if self.IS_FIRST_FRAME:
            if self.args.crop:
                self.roi=Crop.Crop(image,"Crop")            
        if self.args.crop:
            cropped_image=image[self.roi[1]:self.roi[3], self.roi[0]:self.roi[2]]
            return((ret,cropped_image))
        else:
            return((ret,image))
    
    def create_background(self):
        
        self.fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False,varThreshold=float(self.args.mogvariance))
        self.fgbg.setBackgroundRatio(0.95)
            
    def background_apply(self):
        
        #Apply Subtraction
        #self.image = self.fgbg.apply(self.original_image,learningRate=self.args.moglearning)
        self.image = self.fgbg.apply(self.original_image)
        
        #Erode to remove noise, dilate the areas to merge bounded objects
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
        self.image= cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)
    def adapt(self):
        
            #If current frame is a multiple of the 1000 frames
            if self.frame_count % 1000 == 0:                                  
                #get the percent of frames returned in the last 10 minutes
                if (sum([x < self.frame_count-1000 for x in self.annotations.keys()])/1000) > 0.05:
                        
                    #increase tolerance rate
                    self.args.mogvariance+=5
    
                    #add a ceiling
                    if self.args.mogvariance > 120: 
                        self.args.mogvariance = 120
                    print("Adapting to video conditions: increasing MOG variance tolerance to %d" % self.args.mogvariance)

    def find_contour(self):
            _,self.contours,hierarchy = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
            self.contours = [contour for contour in self.contours if cv2.contourArea(contour) > 50]
        
    def cluster_bounding_boxes(self, contours):
        bounding_boxes = []
        for i in range(len(contours)):
            x1,y1,w1,h1 = cv2.boundingRect(contours[i])

            parent_bounding_box = self.get_parent_bounding_box(bounding_boxes, i)
            if parent_bounding_box is None:
                parent_bounding_box = self.BoundingBox(Rect(x1, y1, w1, h1))
                parent_bounding_box.members.append(i)
                bounding_boxes.append(parent_bounding_box)

            for j in range(i+1, len(contours)):
                if self.get_parent_bounding_box(bounding_boxes, j) is None:
                    x2,y2,w2,h2 = cv2.boundingRect(contours[j])
                    rect = Rect(x2, y2, w2, h2)
                    distance = parent_bounding_box.rect.distance_to_rect(rect)
                    if distance < 100:
                        parent_bounding_box.update_rect(self.extend_rectangle(parent_bounding_box.rect, rect))
                        parent_bounding_box.members.append(j)
        return bounding_boxes

    def get_parent_bounding_box(self, bounding_boxes, index):
        for bounding_box in bounding_boxes:
            if index in bounding_box.members:
                return bounding_box
        return None

    def extend_rectangle(self, rect1, rect2):
        x = min(rect1.l_top.x, rect2.l_top.x)
        y = min(rect1.l_top.y, rect2.l_top.y)
        w = max(rect1.r_top.x, rect2.r_top.x) - x
        h = max(rect1.r_bot.y, rect2.r_bot.y) - y
        return Rect(x, y, w, h)    
    
    class BoundingBox:
        def update_rect(self, rect):
            self.rect = rect
            self.x = rect.l_top.x
            self.y = rect.l_top.y
            self.w = rect.width
            self.h = rect.height
            self.time=None

        def __init__(self, rect):
            self.update_rect(rect)
            self.members = []    

    def clip(self):
        
        #find beginning and end segments
        #multiply frame number by frame rate to get timestamp        
        clip_range=ClipLength(self.MotionHistory,self.frame_rate)
        
        ##Clip rules##
        
        #1) If two consecutive clips are within 10 seconds, combine.
        revised_clips=[]
        for index,clip in enumerate(clip_range[:-1]):
            if (clip_range[index][1] - clip_range[index+1][0]) < 10:
                combined=clip_range[index] + clip_range[index+1]
                revised_clips.append([min(combined),max(combined)])
        
        #2 If clip duration is less than 2 second, remove
        revised_clips=[x[(x[1]-x[0] > 2)] for x in revised_clips]
        
        #If no clips after rules
        if len(revised_clips)==0:
            print("No remaining clips")
            return None
        
        #turn back class if needed
        if isinstance(revised_clips[0],float):
            revised_clips=[revised_clips]
            
        #Create clip class
        VideoClips=[]
        for index,clip_info in enumerate(revised_clips):
            cl=VideoClip(video_context=self.video_context,features=self.features,video_client=self.video_client)
            cl.orginal_path=self.args.video #video path on local machine
            cl.begin=clip_info[0] # Begin Time
            cl.end=clip_info[1] #End Time
            cl.frame_rate=self.frame_rate 
            
            #add clip number and set GCS path
            vname,ext=os.path.splitext(self.args.video) 
            cl.local_path=vname+"_"+str(index)+".avi"
            VideoClips.append(cl)
        
        #for each VideoClip, cut segment using FFMPEG, upload to GCS and annotate using cloud video intelligence
        clip_labels=[]
        for clip in VideoClips:
            clip.ffmpeg()
            clip.upload()
            clip.label()
            clip_labels.append(clip.parse())
    
    def write(self):      
        
        #write parameter logs        
        self.output_args=self.file_destination + "/parameters.csv"
        with open(self.output_args, 'w') as f:  
            writer = csv.writer(f,)
            writer.writerows(self.args.__dict__.items())
            
            #Total time
            self.total_min=round((self.end_time-self.start_time)/60,3)
            writer.writerow(["Minutes",self.total_min])
            
            #Frames in file
            writer.writerow(["Total Frames",self.frame_count])
            
            #Frames returned to file
            writer.writerow(["Motion Events",len(self.annotations)])
            
            #Hit rate
            len(self.annotations)
            writer.writerow(["Return rate",float(len(self.annotations)/self.frame_count)])
            
            #Frames per second
            writer.writerow(["Frame processing rate",round(float(self.frame_count)/(self.total_min*60),2)])
        
        #Write frame bounding boxes
        self.output_annotations=self.file_destination + "/bounding_boxes.csv"
        with open(self.output_annotations, 'w') as f:  
            writer = csv.writer(f)
            writer.writerow(["Frame","x","y","h","w"])
            for x in self.annotations.keys():   
                bboxes=self.annotations[x]
                for bbox in bboxes: 
                    writer.writerow([x,bbox.x,bbox.y,bbox.h,bbox.w])

        #Write clip annotations
        self.output_annotations=self.file_destination + "/annotations.csv"
        with open(self.clip_labels, 'w') as f:  
            writer = csv.writer(f)
            for line in self.clip_labels: 
                writer.writerow(line)
                

###Helper Functions#####
                    
def ClipLength(l,frame_rate):
    
    #get first position of Motion
    indexes = [next(group) for key, group in groupby(enumerate(l), key=itemgetter(1))]
    
    #number of frames with Motion
    len_indexes = [len(list(group)) for key, group in groupby(l)]
    
    clip_range=[]
    
    #Create time ranges by dividing frame counts by frame rate
    for position,length in enumerate(len_indexes):
        if indexes[position][1] == True:
            clip_range.append([float(indexes[position][0])/frame_rate,float(indexes[position][0]+length)/frame_rate])
    return clip_range

