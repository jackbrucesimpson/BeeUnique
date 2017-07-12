#!/usr/bin/env bash
set -u
set -e

#/Volumes/ID3
#/media/jack/ID2
#/home/jack/Data/beeunique/output
#/Users/jacksimpson/Data/beeunique/raw
VIDEO_DIRECTORY="/Volumes/ID2"
OUTPUT_DIRECTORY="/Users/jacksimpson/Data"
EXPERIMENT_NAME="Caffeine_Unique_Tags"
TRAINING=0 # 0:False, 1:True

NUM_FRAMES_THREAD_QUEUE=256
NUM_FRAMES_BATCH_PROCESS=100
N_PROCESSES=8
CHUNKSIZE=2

#FILE_ARRAY=("$VIDEO_DIRECTORY/*.mp4")
FILE_ARRAY=("/Users/jacksimpson/Data/beeunique/raw/2017-02-14_22-22-15.mp4")

for FILENAME_PATH in $FILE_ARRAY; do
    python ../src/track.py $FILENAME_PATH $OUTPUT_DIRECTORY $EXPERIMENT_NAME $TRAINING $NUM_FRAMES_THREAD_QUEUE $NUM_FRAMES_BATCH_PROCESS $N_PROCESSES $CHUNKSIZE
done
