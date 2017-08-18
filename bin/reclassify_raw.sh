#!/usr/bin/env bash
set -u
set -e

source setup.sh

JSON_FILE_ARRAY=("$EXPERIMENT_DIRECTORY/raw/*.json")
for JSON_FILENAME_PATH in $JSON_FILE_ARRAY; do
    python2 ../src/reclassify_raw.py $JSON_FILENAME_PATH
done
