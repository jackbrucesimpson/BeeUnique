#!/usr/bin/env bash

set -u
set -e

source setup.sh

#(50, datetime.datetime(2017, 2, 15, 22, 32, 11), 52492, 0, 0)
#(50, datetime.datetime(2017, 2, 16, 15, 32, 24), 56725, 0, 0)
#(50, datetime.datetime(2017, 2, 16, 17, 32, 26), 27879, 0, 0)
#VIDEO_FILE_PATH="/media/jack/IDs/2017-02-17_22-32-48.mp4"

VIDEO_FILE_PATH="/media/jack/IDs/2017-02-16_17-32-26.mp4"
ENHANCE_UNTAGGED_BEES=0
RAW=0
CREATE_VIDEO=0
OUTPUT_VIDEO_FILE="/home/jack/Data/Caffeine_Unique_Tags/test.avi"

python2 ../src/overlay.py $VIDEO_FILE_PATH $EXPERIMENT_DIRECTORY $RAW $CREATE_VIDEO $OUTPUT_VIDEO_FILE $ENHANCE_UNTAGGED_BEES $NUM_FRAMES_THREAD_QUEUE
