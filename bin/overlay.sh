#!/usr/bin/env bash

set -u
set -e

source setup.sh

#/Volumes/JSIMPSON/2017-04-13_16-00-46.mp4
VIDEO_FILE_PATH="/Volumes/JSIMPSON/2017-02-15_06-32-03.mp4"
RAW=1
CREATE_VIDEO=0
OUTPUT_VIDEO_FILE="/home/jack/Data/Caffeine_Unique_Tags/test.avi"

python2 ../src/overlay.py $VIDEO_FILE_PATH $EXPERIMENT_DIRECTORY $RAW $CREATE_VIDEO $OUTPUT_VIDEO_FILE $NUM_FRAMES_THREAD_QUEUE
