import argparse 
import Video

def MotionMeerkat(path,keep=True,vidpath="",write=False):

    #create instance
    video_instance=Video.Video(path,vidpath=vidpath,keep=keep,write=write)

    #send to google for labels
    video_instance.label()  
    
    #download file to play locally
    video_instance.download()
    
    #show video with annotations
    video_instance.show()
    
    #cleanup video staging file
    video_instance.cleanup()
      
#run if called directly from command line
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-gcs_uri', help='The Google Cloud Storage URI of the video.')
    parser.add_argument('-gcs_uri', help='The local file directory to save annotated video')    
    parser.add_argument('-keep', help='Should the downloaded file be kept after analysis?',action="store_true")  
    parser.add_argument('-write', help='Should a annotated video file be written',action="store_true")    
    parser.add_argument('-show', help='Show annotations within program video',action="store_true")    
    
    args = parser.parse_args()    
    MotionMeerkat(args.gcs_uri)
