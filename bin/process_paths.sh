#!/usr/bin/env bash
set -u
set -e

OVERWRITE_PROCESSED=0

source setup.sh

JSON_FILE_ARRAY=("$EXPERIMENT_DIRECTORY/raw/*.json")
for JSON_FILENAME_PATH in $JSON_FILE_ARRAY; do
    python2 ../src/process_paths.py $JSON_FILENAME_PATH $EXPERIMENT_DIRECTORY $OVERWRITE_PROCESSED
done
