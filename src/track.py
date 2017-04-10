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
    fp = FrameProcessor(video_path=sys.argv[1], output_directory = sys.argv[2], experiment_name = sys.argv[3], is_training = bool(int(sys.argv[4])))

    while stream.processing_frames():
        frame = stream.read()
        enough_frames_to_process = fp.append_frame_increment_counter(frame)
        if enough_frames_to_process:
            fp.parallel_process_frames()

    if len(fp.list_frames) > 0:
        fp.parallel_process_frames()
    fp.output_data()

if __name__ == "__main__":
    main()
