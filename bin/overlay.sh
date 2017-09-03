#!/usr/bin/env bash

set -u
set -e

source setup.sh

VIDEO_FILE_PATH="/media/jack/IDs/2017-02-14_23-32-00.mp4"
ENHANCE_UNTAGGED_BEES=1
RAW=0
CREATE_VIDEO=0
OUTPUT_VIDEO_FILE="/home/jack/Data/Caffeine_Unique_Tags/test.avi"

python2 ../src/overlay.py $VIDEO_FILE_PATH $EXPERIMENT_DIRECTORY $RAW $CREATE_VIDEO $OUTPUT_VIDEO_FILE $ENHANCE_UNTAGGED_BEES $NUM_FRAMES_THREAD_QUEUE
