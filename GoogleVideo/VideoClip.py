import sys
import time
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

class VideoClip:
    
    def __init__(self,video_context,features,video_client):
        
        self.video_context=video_context
        self.features=features
        self.video_client=video_client
        
        self.bucket=None #Bucket authenticated destination
        self.begin=None #Start Time
        self.end=None # End Time
        self.frame_rate=None #Frame Rate
        self.original_path=None #Full video
        self.local_path=None #The clipped path variable
        self.gcs_path=None #Desired GCS path

    def ffmpeg(self):
        ffmpeg_extract_subclip(self.original_path, self.begin, self.end, targetname=self.local_path)
    
    def upload(self):
    
        #Upload clip to google cloud
        #construct filename
        splitname=os.path.split(self.local_path)
        filename=splitname[len(splitname)-1]
        blob = self.bucket.blob("VideoMeerkat" + "/" + filename.lower())
        
        self.gcs_path='gs://' + self.bucket.name +"/"+ blob.name
        
        if not blob.exists():
            blob.upload_from_filename(filename=self.local_path)                        
            #upload to gcp                
            print("Uploaded " + self.gcs_path)

    def label(self):
        
        operation = self.video_client.annotate_video(self.gcs_path, self.features, video_context=self.video_context)
        print('\nProcessing video for label annotations:')
    
        while not operation.done():
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(15)
    
        print('\nFinished processing.')
    
        self.result = operation.result().annotation_results[0]
        
        for i, label in enumerate(self.result.label_annotations):
            print('Label description: {}'.format(label.description))
            print('Locations:')
    
            for l, location in enumerate(label.locations):
                positions = 'Entire video'
                if (location.segment.start_time_offset != -1 or
                        location.segment.end_time_offset != -1):
                    positions = '{} to {}'.format(
                        location.segment.start_time_offset / 1000000.0,
                        location.segment.end_time_offset / 1000000.0)
                                            
                print('\t{}: {}'.format(l, positions))
    
            print('\n')

    def parse(self):
        self.parsed_labels=[]
        for label in self.result.label_annotations:
            for location in label.locations:
                self.parsed_labels.append([self.original_path,
                                           self.local_path,
                                           str(label.description), 
                                           location.segment.start_time_offset/1000000.0,
                                           location.segment.end_time_offset/1000000.0,
                                           location.segment.start_time_offset/1000000.0+self.begin,
                                           location.segment.start_time_offset/1000000.0+self.begin,
                                           location.confidence])
        return self.parsed_labels        
        
            
