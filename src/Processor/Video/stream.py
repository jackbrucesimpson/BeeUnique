# modified from pyimagesearch

import sys
import numpy as np
import cv2
import time

from threading import Thread
if sys.version_info >= (3, 0):
    from queue import Queue
else:
    from Queue import Queue

class Stream(object):
    def __init__(self, video_path, queue_size):
        self.video_stream = cv2.VideoCapture(video_path)
        self.is_streaming = True
        self.Q = Queue(maxsize=queue_size)

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while True:
            if not self.Q.full():
                read_successful, frame = self.video_stream.read() # get next frame
                if not read_successful:
                    self.is_streaming = False
                    break
                self.Q.put(frame)

    def read(self):
        return self.Q.get()

    def processing_frames(self):
        if not self.Q.empty():
            return True
        else:
            num_times_slept = 0
            while self.is_streaming:
                time.sleep(2)
                num_times_slept += 1
                if num_times_slept > 5:
                    print('Problem accessing video')
                    sys.exit(1)
                if not self.Q.empty():
                    return True
            return False
