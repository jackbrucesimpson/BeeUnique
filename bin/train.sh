#!/usr/bin/env bash

VIDEO_DIRECTORY="/Users/jacksimpson/Data/beehome/raw"
OUTPUT_DIRECTORY=""
NUM_VIDEOS_PROCESS_PARALLEL=3

file_array=("$VIDEO_DIRECTORY/*.mp4")
file_num=0

for filename_path in $file_array; do
    file_num=$((file_num + 1))
    #python ../src/extract_train_tags.py $filename_path $OUTPUT_DIRECTORY &

    if [ $((file_num % NUM_VIDEOS_PROCESS_PARALLEL)) = 0 ]; then
        wait
       echo expression evaluated as true
    fi
    echo $filename_path

done

echo $file_num
