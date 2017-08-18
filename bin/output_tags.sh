#!/usr/bin/env bash
set -u
set -e

source setup.sh

REDUCE_IMAGES=1

JSON_FILE_ARRAY=("$EXPERIMENT_DIRECTORY/raw/*.json")
for JSON_FILENAME_PATH in $JSON_FILE_ARRAY; do
    python2 ../src/output_tags.py $JSON_FILENAME_PATH $EXPERIMENT_DIRECTORY $REDUCE_IMAGES
done
