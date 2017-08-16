#!/usr/bin/env bash
set -u
set -e

EXPERIMENT_DIRECTORY="/Users/jacksimpson/Data/Caffeine_Unique_Tags"

python2 ../src/combine_bg.py $EXPERIMENT_DIRECTORY
