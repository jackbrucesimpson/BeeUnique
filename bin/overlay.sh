#!/usr/bin/env bash

set -u
set -e

FILENAME_PATH="/media/jack/IDs/2017-02-14_23-32-00.mp4"
CSV_FILE_PATH="/home/jack/Data/Caffeine_Unique_Tags/2017-02-14_23-32-00.csv"
CREATE_VIDEO=1 #1: True, 0: False
OUTPUT_VIDEO_FILE="/home/jack/Data/Caffeine_Unique_Tags/test.avi"

NUM_FRAMES_THREAD_QUEUE=256

python ../src/overlay.py $FILENAME_PATH $CSV_FILE_PATH $CREATE_VIDEO $OUTPUT_VIDEO_FILE $NUM_FRAMES_THREAD_QUEUE
