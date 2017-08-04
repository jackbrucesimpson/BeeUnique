#!/usr/bin/env bash

set -u
set -e

FILENAME_PATH="/media/jack/IDs/2017-02-14_23-32-00.mp4"
JSON_FILE_PATH="/home/jack/Data/Caffeine_Unique_Tags/json/2017-02-14_23-32-00.json"
CREATE_VIDEO=0 #1: True, 0: False
OUTPUT_VIDEO_FILE="/home/jack/Data/Caffeine_Unique_Tags/test.avi"

NUM_FRAMES_THREAD_QUEUE=256

python ../src/overlay.py $FILENAME_PATH $JSON_FILE_PATH $CREATE_VIDEO $OUTPUT_VIDEO_FILE $NUM_FRAMES_THREAD_QUEUE
