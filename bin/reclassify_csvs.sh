#!/usr/bin/env bash
set -u
set -e

EXPERIMENT_DIRECTORY="/Users/jacksimpson/Data/Caffeine_Unique_Tags"

CSV_FILE_ARRAY=("$EXPERIMENT_DIRECTORY/csv/*.csv")
for CSV_FILENAME_PATH in $CSV_FILE_ARRAY; do
    python2 ../src/reclassify_csv.py $CSV_FILENAME_PATH
done
