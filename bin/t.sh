#!/usr/bin/env bash
set -u
set -e

VIDEO_DIRECTORY="/media/jack/IDs"
OUTPUT_DIRECTORY="/home/jack/Data"
EXPERIMENT_NAME="Caffeine_Unique_Tags"
TRAINING=0 # 0:False, 1:True

CSV_FILE_ARRAY=("$OUTPUT_DIRECTORY/$EXPERIMENT_NAME/csv/*.csv")
for CSV_FILENAME_PATH in $CSV_FILE_ARRAY; do
    #python ../src/track.py $CSV_FILENAME_PATH
    echo $CSV_FILENAME_PATH
done
