# modified from pyimagesearch tutorial

import sys
import numpy as np
import cv2
import time

from threading import Thread
if sys.version_info >= (3, 0):
    from queue import Queue
else:
    from Queue import Queue

class Stream:
    def __init__(self, video_path, queue_size=256):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stream = cv2.VideoCapture(video_path)
        self.streaming = True
        self.frames_queued = True

        # initialize the queue used to store frames read from
        # the video file
        self.Q = Queue(maxsize=queue_size)

    def start(self):
        # start a thread to read frames from the file video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):

        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            #if self.stopped:
                #return

            # otherwise, ensure the queue has room in it
            if not self.Q.full():
                # read the next frame from the file
                (grabbed, frame) = self.stream.read()

                # if the `grabbed` boolean is `False`, then we have
                # reached the end of the video file
                if not grabbed:
                    self.stop_streaming()
                    return

                # add the frame to the queue
                self.Q.put(frame)

    def read(self):
        # return next frame in the queue
        if self.Q.qsize() > 0:
            return self.Q.get()
        elif self.streaming:
            time.sleep(2)
            return self.Q.get()
        else:
            self.frames_queued = False

    def processing_frames(self):
        return self.frames_queued

    def stop_streaming(self):
        self.streaming = False
