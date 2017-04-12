import numpy as np
import cv2
import os
import sys

from Processor import Stream
from Processor import segment_frame

def main():
    if len(sys.argv) != 2:
        print("Need input video")
        sys.exit(1)

    stream = Stream(video_path=sys.argv[1], queue_size=256).start()
    frame_counter = 0

    while stream.processing_frames():
        frame = stream.read()
        segmented_frame = segment_frame((frame_counter, frame))

        resized_frame = cv2.resize(segmented_frame, (1280, 720))

        cv2.imshow('frame', resized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()
