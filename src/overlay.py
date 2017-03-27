import numpy as np
import cv2
import os
import sys

from Processor import Stream
from Processor import FrameProcessor

def main():
    if len(sys.argv) != 5:
        print("Need input video, output directory, experiment name, and training arguments")
        sys.exit(1)

    stream = Stream(video_path=sys.argv[1], queue_size=256).start()
    fo = FrameProcessor(video_path=sys.argv[1], database_file_path = sys.arv[2])

    while stream.processing_frames():
        frame = stream.read()
        overlaid_frame = fo.overlay_frame(frame)
        cv2.imshow('frame', overlaid_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()
