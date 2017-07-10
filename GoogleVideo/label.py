import argparse
import urllib
import json
from google.cloud import storage
import sys
import time

from google.cloud.gapic.videointelligence.v1beta1 import enums
from google.cloud.gapic.videointelligence.v1beta1 import (
    video_intelligence_service_client)
from google.cloud.proto.videointelligence.v1beta1 import video_intelligence_pb2

def main(path):
    """ Detects labels given a GCS path. """
    video_client = (video_intelligence_service_client.
                    VideoIntelligenceServiceClient())
    features = [enums.Feature.LABEL_DETECTION]
    video_context = video_intelligence_pb2.VideoContext()
    video_context.stationary_camera = True
    video_context.label_detection_mode = video_intelligence_pb2.FRAME_MODE
    operation = video_client.annotate_video(path, features, video_context=video_context)
    print('\nProcessing video for label annotations:')

    while not operation.done():
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(20)

    print('\nFinished processing.')

    results = operation.result().annotation_results[0]

    return(results)

def label_parse(results):
    
    labelData = results.label_annotations
    print ('Video Annotations:')
    for label in labelData:
        print (label.description) 
        for location in label.locations:
                segment = location.segment
                startTime = segment.start_time_offset
                endTime = segment.end_time_offset
                print ("  " + str(startTime) + ", " + str(endTime))
    
def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
    
        blob.download_to_filename(destination_file_name)
    
        print('Blob {} downloaded to {}.'.format(
            source_blob_name,
            destination_file_name))        
    except:
        print("User does not have access to that bucket. Trying public link:")
        gcs_url = 'https://%(bucket)s.storage.googleapis.com/%(file)s' % {'bucket':bucket_name, 'file':source_blob_name}
        urllib.urlretrieve(gcs_url, destination_file_name)
        print ("Download complete")        
    
    

