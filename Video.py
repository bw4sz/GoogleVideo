import label

class Video:
    def __init__(self,path):
        self.time = time.time()
        self.path = path
    def label(self):
        label.main(self.path)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-gcs_uri', help='The Google Cloud Storage URI of the video.',default='gs://api-project-773889352370-ml/Videos/jantest.mp4')
    args = parser.parse_args()
    main(args.gcs_uri)