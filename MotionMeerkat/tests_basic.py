import MotionMeerkat
import os

#Run defaults
# Serice account credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/Ben/Dropbox/Google/MeerkatReader-9fbf10d1e30c.json"

#Test 1
#defaults, no download, video file supplied locally in git repo
MotionMeerkat.MotionMeerkat(path='gs://api-project-773889352370-ml/Videos/jantest.mp4',keep=False,write=False,vidpath="C:/Users/Ben/Dropbox/GoogleCloud")

#Test 2
#A new private file in my gcs bucket, reads the service account credentials, deletes file when done.
#MotionMeerkat.MotionMeerkat("gs://api-project-773889352370-ml/Videos/shark.avi",write=True,vidpath="C:/Users/Ben/Dropbox/GoogleCloud")

#Test 3
#A new public file in someone else's gcs bucket, deletes file when done.
#MotionMeerkat.MotionMeerkat("gs://cloud-ml-sandbox/video/chicago.mp4",write=True,vidpath="C:/Users/Ben/Dropbox/GoogleCloud")

#Test 4
#A low quality file with several scene changes.
#MotionMeerkat.MotionMeerkat("gs://api-project-773889352370-ml/Videos/CostaRicaCloudForest.avi",write=True,vidpath="C:/Users/Ben/Dropbox/GoogleCloud")
