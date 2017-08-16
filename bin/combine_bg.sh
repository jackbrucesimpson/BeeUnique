#!/usr/bin/env bash
set -u
set -e

source setup.sh

python2 ../src/combine_bg.py $EXPERIMENT_DIRECTORY
