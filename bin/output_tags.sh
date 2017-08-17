#!/usr/bin/env bash
set -u
set -e

source setup.sh

REDUCE_IMAGES=1

CSV_FILE_ARRAY=("$EXPERIMENT_DIRECTORY/csv/*.csv")
for CSV_FILENAME_PATH in $CSV_FILE_ARRAY; do
    python2 ../src/output_tags.py $CSV_FILENAME_PATH $EXPERIMENT_DIRECTORY $REDUCE_IMAGES
done
