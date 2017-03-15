#!/usr/bin/env bash

cd ../src/Tracker
python setup.py build_ext --inplace
rm pytrack.cpp
rm -rf build

mv pytrack.so ../Processor/pytrack.so
