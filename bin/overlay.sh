#!/usr/bin/env bash

set -u
set -e

#/Volumes/ID2/2017-02-24_18-34-23.mp4
filename_path="/Users/jacksimpson/Data/beeunique/raw/2017-02-14_22-22-15.mp4"
database_file_path="/Users/jacksimpson/Data/beeunique/output/Caffeine_Unique_Tags/Caffeine_Unique_Tags.db"

python ../src/overlay.py $filename_path $database_file_path
