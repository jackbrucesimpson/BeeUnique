import numpy as np
import cv2
import os
import sys

from Processor import Stream
from Processor import view_segment_frame

def main():
    '''
    if len(sys.argv) != 4:
        print("Need input video, path to database file, and number of frames to store in memory")
        sys.exit(1)
    '''

    video_path = "/Volumes/ID3/2017-02-24_22-02-57.mp4" #sys.argv[1]

    stream = Stream(video_path=video_path, queue_size=256).start()
    frame_counter = 0

    while stream.processing_frames():
        frame = stream.read()

        segmented_frame = view_segment_frame((frame_counter, frame))
        resized_frame = cv2.resize(segmented_frame, (1280, 720));

        cv2.imshow('frame', resized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_counter += 1

if __name__ == "__main__":
    main()
