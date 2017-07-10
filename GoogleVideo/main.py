import argparse 
import Video

def run(path,keep,write,view,vidpath=""):

    #create instance
    video_instance=Video.Video(path=path,vidpath=vidpath,keep=keep,write=write,view=view)

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
    parser.add_argument('-gcs_uri', help='The local file directory to save annotated video')    
    parser.add_argument('-keep', help='Should the downloaded file be kept after analysis?',action="store_true")  
    parser.add_argument('-write', help='Should a annotated video file be written',action="store_false")    
    parser.add_argument('-view', help='Show annotations within program video',action="store_true")    
    parser.add_argument('-vidpath', help='directory to save annotated video',default="")    
    
    args = parser.parse_args()    
    run(path=args.gcs_uri,keep=args.keep,write=args.write,show=args.show,vidpath=args.vidpath)
