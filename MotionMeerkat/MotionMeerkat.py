import argparse 
import Video

def MotionMeerkat(path='gs://api-project-773889352370-ml/Videos/jantest.mp4',keep=True,vidpath=""):

    #create instance
    video_instance=Video.Video(path)

    #send to google for labels
    video_instance.label()  
    
    #download file to play locally
    video_instance.download()
    
    #show video with annotations
    video_instance.show(vidpath,write=True)
    
    #cleanup video staging file
    video_instance.cleanup(keep)
    
    
#run if called directly from command line
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-gcs_uri', help='The Google Cloud Storage URI of the video.')
    parser.add_argument('-keep', help='Should the downloaded file be kept after analysis?',action="store_true")    
    args = parser.parse_args()    
    MotionMeerkat(args.gcs_uri)
