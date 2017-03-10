# Structuring Tracking Program
- How to organise unique tag program rewrite
- Initial run to extract and classify tags
- Second program run implements tracker

## All Videos
- Pass program directory with videos
- Order the videos by datetime, get weather info from time
- Process each video

## Each Video
### Segmentation and prediction
- Read video
- Count num frames, update background image and count num frames gone into that (divide by this at the end)
- Start processes to process frames in batches, returning:
    - Frame number
    - x,y coordinates of all points
    - Tag matrices to be classified with ID made up of frame number and x,y coordinates
    - Check if pixels are bright due to the light being turned on/weird objects: keep track of contour sizes/shapes
- Batch predict tag types

### Tracking
- Implement bipartite matching
- Can use info about past and present location of tag to improve predictions
- Identify if tag which disappeared reappears near location of disappearance and log
- How to deal with close interactions
- Maybe implement as single threaded C++ program

### Result
- Every hour of experiment forms hash I can query

## Training Model
- Extract paths, write png tag images to directory to be labelled
- Version of tracking program that uses old tracking system to extract bee id based on continuous path
- Process and train
- Maybe add 'unknown' class for darker images/bad angles/occlusion

## Programs to create
- GUI popup to see how well segmentation is working
- Program to track tags and extract individuals for training
- Final tracking and prediction software