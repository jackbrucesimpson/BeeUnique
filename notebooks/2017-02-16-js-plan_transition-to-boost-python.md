# Plan Transition from pure C++ to Boost Python
## Analysis in Notebook
- How to break down transition to Python code for tracking program

### Video and metadata
- Path to file
- Extract date metadata
- Option to give more data about experiment
- Enter weather data?

### Reading frames
- Use [threading](http://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/) to keep reading in frames
- Process frames as separate function processes
- Pass each frame to tracker method, include frame num in video

### Each frame
- Threshold, morph operations, identify contours
- Correctly sized contours for each frame are passed back to main process
- Classify all of the contours
- Decide whether to update tag type being tracked based on this info
- Euclidian distance function is implemented in C++