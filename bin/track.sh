#!/usr/bin/env bash

set -u
set -e

VIDEO_DIRECTORY="/Users/jacksimpson/Data/beeunique/raw"
OUTPUT_DIRECTORY=""
NUM_VIDEOS_PROCESS_PARALLEL=3

file_array=("$VIDEO_DIRECTORY/*.mp4")
file_num=0

for filename_path in $file_array; do
    file_num=$((file_num + 1))
    echo $filename_path
    #python ../src/track.py $filename_path $OUTPUT_DIRECTORY &

    if [ $((file_num % NUM_VIDEOS_PROCESS_PARALLEL)) = 0 ]; then
        wait
    fi

done
