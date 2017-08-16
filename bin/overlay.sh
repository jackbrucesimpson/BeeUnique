#!/usr/bin/env bash

set -u
set -e

VIDEO_FILE_PATH="/Volumes/JSIMPSON/2017-02-15_04-32-00.mp4"
COORD_FILE_PATH="/Users/jacksimpson/Data/Caffeine_Unique_Tags/csv/2017-02-15_04-32-00.csv"
CREATE_VIDEO=0 #1: True, 0: False
OUTPUT_VIDEO_FILE="/home/jack/Data/Caffeine_Unique_Tags/test.avi"

NUM_FRAMES_THREAD_QUEUE=256

python2 ../src/overlay.py $VIDEO_FILE_PATH $COORD_FILE_PATH $CREATE_VIDEO $OUTPUT_VIDEO_FILE $NUM_FRAMES_THREAD_QUEUE
