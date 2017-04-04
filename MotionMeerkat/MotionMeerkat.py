import argparse 
import Video

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-gcs_uri', help='The Google Cloud Storage URI of the video.',default='gs://api-project-773889352370-ml/Videos/jantest.mp4')
    args = parser.parse_args()
    video_instance=Video.Video(args.gcs_uri)
    video_instance.label()   
