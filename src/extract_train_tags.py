import numpy as np
import cv2
import os
import sys

from Processor import Stream
from Processor import FrameProcessor

def main():
    if len(sys.argv) != 4:
        print("Need input video and output directory")
        sys.exit(1)

    input_video_file = sys.argv[1]
    output_dir = sys.argv[2]
    if sys.argv[3] == 'train':
        is_training = True
    elif sys.argv[3] == 'track':
        is_training = True
    else:
        print("Please indicate if you want to 'train' or 'track'")
        sys.exit(1)

    stream = Stream(video_path=input_video_file, queue_size=256).start()
    fp = FrameProcessor(video_path=input_video_file, output_directory = output_dir, is_training=is_training)

    while stream.processing_frames():
        frame = stream.read()
        enough_frames_to_process = fp.append_frame_increment_counter(frame)
        if enough_frames_to_process:
            fp.parallel_process_frames()

    if len(fp.list_frames) > 0:
        fp.parallel_process_frames()
    fp.output_background_image()

if __name__ == "__main__":
    main()
