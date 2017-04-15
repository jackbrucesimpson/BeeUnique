import numpy as np
import cv2
import os
import sys

from Processor import Stream
from Processor import FrameOverlayer

def main():
    if len(sys.argv) != 4:
        print("Need input video, path to database file, and number of frames to store in memory")
        sys.exit(1)

    video_path = sys.argv[1]
    database_file_path = sys.argv[2]
    num_frames_thread_queue = int(sys.argv[3])

    stream = Stream(video_path=video_path, queue_size=num_frames_thread_queue).start()
    fo = FrameOverlayer(video_path=video_path, database_file_path = database_file_path)

    while stream.processing_frames():
        frame = stream.read()
        overlaid_frame = fo.overlay_frame(frame)
        cv2.imshow('frame', overlaid_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()
