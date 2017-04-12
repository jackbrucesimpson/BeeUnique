#!/usr/bin/env bash

set -u
set -e

filename_path="/Users/jacksimpson/Data/beeunique/raw/2017-02-14_22-22-15.mp4"

python ../src/segment.py $filename_path
