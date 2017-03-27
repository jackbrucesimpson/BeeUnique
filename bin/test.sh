#!/usr/bin/env bash

filename_path="/Users/jacksimpson/Data/beeunique/raw/2017-02-14_22-22-15.mp4"
OUTPUT_DIRECTORY="/Users/jacksimpson/Data/beeunique/output"
train_or_track="train" # alternative is track

python ../src/extract_train_tags.py $filename_path $OUTPUT_DIRECTORY $train_or_track