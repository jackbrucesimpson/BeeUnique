#!/usr/bin/env bash

set -u
set -e

cd ../src/Tracker
python2 setup.py build_ext --inplace
rm pytrack.cpp
rm -rf build

mv pytrack.so ../Processor/Video/pytrack.so
