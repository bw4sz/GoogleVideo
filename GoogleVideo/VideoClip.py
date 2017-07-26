from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from google.cloud.gapic.videointelligence.v1beta1 import enums
from google.cloud.gapic.videointelligence.v1beta1 import (
    video_intelligence_service_client)
from google.cloud.proto.videointelligence.v1beta1 import video_intelligence_pb2

#Set Google Credentials and Properties
##Cloud Video Properties
video_client = (video_intelligence_service_client.
                         VideoIntelligenceServiceClient())
features = [enums.Feature.LABEL_DETECTION]
video_context = video_intelligence_pb2.VideoContext()
video_context.stationary_camera = True
video_context.label_detection_mode = video_intelligence_pb2.FRAME_MODE        

class VideoClip:
    
    def __init__(self,video_context=video_context,features=features,video_client=video_client):
        
        self.bucket=None #Bucket authenticated destination
        self.begin=None #Start Time
        self.end=None # End Time
        self.frame_rate=None #Frame Rate
        self.orginal_path=None #Full video 
        self.gcs_path=None #Desired GCS path

    def ffmpeg(self):
        self.local_path=ffmpeg_extract_subclip(self.original_path, self.begin, self.end, targetname=self.local_path)
    
    def upload(self):
    
        #Upload clip to google cloud
        #construct filename
        splitname=os.path.split(clip)
        filename=splitname[len(splitname)-1]
        blob = self.bucket.blob("VideoMeerkat" + "/" + filename.lower())
        
        self.gcs_path='gs://' + self.bucket.name +"/"+ blob.name
        
        if not blob.exists():
            blob.upload_from_filename(filename=clip)                        
            #upload to gcp                
            print("Uploaded " + clip)
    
    def label(self):
        
        operation = video_client.annotate_video(self.gcs_path, features, video_context=video_context)
        print('\nProcessing video for label annotations:')
    
        while not operation.done():
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(15)
    
        print('\nFinished processing.')
    
        self.results = operation.result().annotation_results[0]
        
        for i, label in enumerate(self.results.label_annotations):
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
            for description in label.description:
                for location in label.locations:
                    self.parsed_labels.append(description, location.segment.start_time_offset,location.segment.end_time_offset,location.confidence)
        return self.parsed_labels        
        
            
