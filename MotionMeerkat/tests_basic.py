import MotionMeerkat
import os

#Run defaults
# Serice account credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/Ben/Dropbox/Google/MeerkatReader-9fbf10d1e30c.json"

#Test 1
#defaults, no download, video file supplied locally in git repo
#MotionMeerkat.MotionMeerkat(keep=True)

#Test 2
#A new public file in my gcs bucket, reads the service account credentials, deletes file when done.
MotionMeerkat.MotionMeerkat("gs://api-project-773889352370-ml/Videos/shark.avi")

#Test 3
#A new public file in someone else's gcs bucket, deletes file when done.
MotionMeerkat.MotionMeerkat("gs://api-project-773889352370-ml/Videos/shark.avi")
