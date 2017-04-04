import argparse
import httplib2
import time
import json

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

API_DISCOVERY_FILE = 'video-intelligence-service-discovery-v1beta1.json'
OPERATIONS_DISCOVERY_FILE = 'video-intelligence-operations-discovery.json'

def main(gcs_uri):

    credentials = GoogleCredentials.get_application_default()

    with open(API_DISCOVERY_FILE, 'r') as f:
        doc = f.read()
    video_service = discovery.build_from_document(
        doc, credentials=credentials)

    with open(OPERATIONS_DISCOVERY_FILE, 'r') as f:
        op_doc = f.read()
    op_service = discovery.build_from_document(
        op_doc, credentials=credentials)

    video_service_request = video_service.videos().annotate(
        body={
            'inputUri': gcs_uri,
            'features': ['LABEL_DETECTION']
        })

    response = video_service_request.execute()
    name = response['name']

    op_service_request = op_service.operations().get(name=name)
    response = op_service_request.execute()
    op_start_time = str(response['metadata']['annotationProgress'][0]['startTime'])
    print('Operation {} started: {}'.format(name, op_start_time))

    while True:
        response = op_service_request.execute()
        time.sleep(30)
        if 'done' in response and response['done'] == True:
            break
        else:
            print('Operation processing ...')
    print('The video has been successfully processed.')
    print('')
    labelData = response['response']['annotationResults'][0]['labelAnnotations']
    print ('Video Annotations:')
    for label in labelData:
        if 'locations' not in label:
            print ('Error in label detection: ' + label['description'])
        else:
            print label['description']
            locations = label['locations']
            for location in locations:
                if 'segment' not in location:
                    print 'Missing segment.'
                else:
                    segment = location['segment']
                    startTime = segment.get('startTimeOffset', '0')
                    endTime = segment.get('endTimeOffset', '0')
                    print "  " + startTime + ", " + endTime

    
    

