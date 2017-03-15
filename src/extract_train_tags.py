import numpy as np
import cv2
import os
import time
from Tracker import Stream
from Tracker import FrameProcessor
#from Tracker import Track

data_dir = os.environ.get('DATA_DIR', None)
raw_dir = os.path.join(data_dir, 'beeunique/raw')
output_dir = os.path.join(data_dir, 'beeunique/output')
input_video_file = os.path.join(raw_dir, '2017-02-14_22-22-15.mp4')

def main():
    stream = Stream(video_path=input_video_file, queue_size=256).start()
    fp = FrameProcessor(output_directory = output_dir, is_training=True)

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
