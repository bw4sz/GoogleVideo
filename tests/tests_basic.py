from context import MotionMeerkat
import os

#Run defaults
# Serice account credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/Ben/Dropbox/Google/MeerkatReader-9fbf10d1e30c.json"

print MotionMeerkat.__path__
