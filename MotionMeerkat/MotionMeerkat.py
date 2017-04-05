import argparse 
import Video

def j():
    print "Hello World"

def MotionMeerkat():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-gcs_uri', help='The Google Cloud Storage URI of the video.',default='gs://api-project-773889352370-ml/Videos/jantest.mp4')
    args = parser.parse_args()
    
    #create instance
    video_instance=Video.Video(args.gcs_uri)

    #send to google for labels
    video_instance.label()  
    
    #download file to play locally
    video_instance.download()
    
    #show video
    video_instance.write()