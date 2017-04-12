#!/usr/bin/env bash
set -u
set -e

VIDEO_DIRECTORY="/media/jack/ID2"
OUTPUT_DIRECTORY="/home/jack/Data/beeunique/output"
TRAINING=0 # 0:False, 1:True
EXPERIMENT_NAME='Caffeine_Unique_Tags'
file_array=("$VIDEO_DIRECTORY/*.mp4")

for filename_path in $file_array; do
    python ../src/track.py $filename_path $OUTPUT_DIRECTORY $EXPERIMENT_NAME $TRAINING
done
