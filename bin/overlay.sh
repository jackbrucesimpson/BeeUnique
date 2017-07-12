#!/usr/bin/env bash

set -u
set -e

#/Volumes/ID2/2017-02-24_18-34-23.mp4
#/media/jack/ID2/2017-02-19_07-33-44.mp4
#/Users/jacksimpson/Data/beeunique/raw/2017-02-14_22-22-15.mp4
#/home/jack/Data/beeunique/output/Caffeine_Unique_Tags/Caffeine_Unique_Tags.db
#/Volumes/ID3/2017-02-24_22-02-57.mp4
FILENAME_PATH="/Users/jacksimpson/Data/beeunique/raw/2017-02-14_22-22-15.mp4"
CSV_FILE_PATH="/Users/jacksimpson/Data/Caffeine_Unique_Tags/2017-02-14_22-22-15.csv"
CREATE_VIDEO=1 #1: True, 0: False
OUTPUT_VIDEO_FILE="/Users/jacksimpson/Data/Caffeine_Unique_Tags/test.mp4"

NUM_FRAMES_THREAD_QUEUE=256

python ../src/overlay.py $FILENAME_PATH $CSV_FILE_PATH $CREATE_VIDEO $OUTPUT_VIDEO_FILE $NUM_FRAMES_THREAD_QUEUE
