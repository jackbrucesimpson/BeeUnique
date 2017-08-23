#!/usr/bin/env bash
set -u
set -e

source setup.sh

python2 ../src/calc_metrics.py $EXPERIMENT_DIRECTORY
