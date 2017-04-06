import MotionMeerkat
import os

#Run defaults
# Serice account credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/Ben/Dropbox/Google/MeerkatReader-9fbf10d1e30c.json"

#defaults, no download, video file supplied locally in git repo
MotionMeerkat.MotionMeerkat()

#A new public file in my gcs bucket, reads the service account credentials
MotionMeerkat.MotionMeerkat("gs://api-project-773889352370-ml/Videos/garcon_test.avi")