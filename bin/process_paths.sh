#!/usr/bin/env bash
set -u
set -e

OVERWRITE_PROCESSED=0
OUTPUT_UNKNOWN_TAG_PATH_IMAGES=0

source setup.sh

JSON_FILE_ARRAY=("$EXPERIMENT_DIRECTORY/raw/*.json")
for JSON_FILENAME_PATH in $JSON_FILE_ARRAY; do
    python2 ../src/process_paths.py $JSON_FILENAME_PATH $EXPERIMENT_DIRECTORY $OVERWRITE_PROCESSED $OUTPUT_UNKNOWN_TAG_PATH_IMAGES $REDUCE_IMAGES
done

# group paths into database with paths
python2 ../src/create_path_dbs.py $EXPERIMENT_DIRECTORY
