# BeeUnique

Tracking bees with unique tags

## Setup

### Dependencies
- Requires a Mac/Linux OS
- Python 2
- OpenCV
- Cython

### Build
- run the `build.sh` script in the `bin` directory

## To Do

### File I/O
- [ ] Extract date and time from filename
- [ ] Process weather data at the same time
- [ ] Check if tag area extracted is over edge of frame col/row
- [ ] Filename for CSV and background image
- [x] Write methods to generate and output background image
- [x] Implement threading and multiprocessing to process video

### Tracking
- [x] Implement tracking and bee classes in C++
- [x] Write Cython wrapper
- [ ] Test and debug overlaying on video
- [ ] Test batch processing method
- [ ] Test training method that flattens tags and writes them out
- [ ] Work out ideal number of recent classifications to predict bee class
- [ ] Implement awareness of when bee is near to other bees
- [ ] When bee reappears close to where it disappeared keep note

### Machine Learning
- [ ] Label extracted tags from training images
- [ ] Train Keras model and save it
- [ ] Import into tracking class and use to generate tag predictions
