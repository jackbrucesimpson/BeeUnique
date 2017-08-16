#!/usr/bin/env bash
set -u
set -e

EXPERIMENT_DIRECTORY="/Users/jacksimpson/Data/Caffeine_Unique_Tags"

CSV_FILE_ARRAY=("$EXPERIMENT_DIRECTORY/csv/*.csv")
for CSV_FILENAME_PATH in $CSV_FILE_ARRAY; do
    python2 ../src/process_paths.py $CSV_FILENAME_PATH $EXPERIMENT_DIRECTORY
done
