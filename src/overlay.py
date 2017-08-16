import numpy as np
import cv2
import os
import sys

from Processor import Stream
from Processor import FrameOverlayer

from Processor.file_utils import get_video_filename

def main():
    if len(sys.argv) != 6:
        print("Incorrect arguments")
        sys.exit(1)

    video_path = sys.argv[1]
    coord_file_path = sys.argv[2]
    create_video = bool(int(sys.argv[3]))
    output_video_file = sys.argv[4]
    num_frames_thread_queue = int(sys.argv[5])

    if create_video:
        video_filename = get_video_filename(video_path)
        fourcc = cv2.cv.CV_FOURCC('X','V','I','D')#cv2.cv.CV_FOURCC(*'mp4v')
        out = cv2.VideoWriter(output_video_file, fourcc, fps=20.0, frameSize=(3840, 2160), isColor=True)

    stream = Stream(video_path=video_path, queue_size=num_frames_thread_queue).start()
    fo = FrameOverlayer(video_path=video_path, coord_file_path = coord_file_path)

    while stream.processing_frames():
        frame = stream.read()
        overlaid_frame = fo.overlay_frame(frame)
        resized_frame = cv2.resize(overlaid_frame, (1280, 720));
        cv2.imshow('frame', resized_frame)
        if cv2.waitKey(1) == ord('q'):
            break

        if create_video:
            out.write(overlaid_frame)

    if create_video:
        out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
