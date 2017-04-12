#!/usr/bin/env bash

set -u
set -e

#/Volumes/ID2/2017-02-24_18-34-23.mp4
#/media/jack/ID2/2017-02-19_07-33-44.mp4
#/home/jack/Data/beeunique/output
filename_path="/Users/jacksimpson/Data/beeunique/raw/2017-02-14_22-22-15.mp4"
OUTPUT_DIRECTORY="/Users/jacksimpson/Data/beeunique/output"
TRAINING=1 # 0:False, 1:True
EXPERIMENT_NAME='Caffeine_Unique_Tags'

python ../src/track.py $filename_path $OUTPUT_DIRECTORY $EXPERIMENT_NAME $TRAINING
