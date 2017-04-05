import label
import time

class Video:
    def __init__(self,path):
        self.time = time.time()
        self.path = path
    def label(self):
        labels=label.main(self.path)
        label.label_parse(labels)
        
        