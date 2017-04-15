#!/usr/bin/env bash
set -u
set -e

#/Volumes/ID3
#/media/jack/ID2
#/home/jack/Data/beeunique/output
VIDEO_DIRECTORY="/Volumes/ID3"
OUTPUT_DIRECTORY="/Users/jacksimpson/Data/beeunique/output"
EXPERIMENT_NAME='Caffeine_Unique_Tags'
TRAINING=1 # 0:False, 1:True
SKIP_VIDEO_IF_IN_DB=1 # 0:False, 1:True

NUM_FRAMES_THREAD_QUEUE=256
NUM_FRAMES_BATCH_PROCESS=100
N_PROCESSES=8
CHUNKSIZE=2

file_array=("$VIDEO_DIRECTORY/*.mp4")

for FILENAME_PATH in $file_array; do
    python ../src/track.py $FILENAME_PATH $OUTPUT_DIRECTORY $EXPERIMENT_NAME $TRAINING $SKIP_VIDEO_IF_IN_DB $NUM_FRAMES_THREAD_QUEUE $NUM_FRAMES_BATCH_PROCESS $N_PROCESSES $CHUNKSIZE
done
