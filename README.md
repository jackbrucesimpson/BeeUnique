# BeeUnique

Program to track bees with unique tags.

## Running the Programs

Execution scripts are located in the `bin` directory. Instructions for how to modify the variables in them for processing your own data are included below.

You can execute the scripts by running the `bash` command followed by the script name. For example, if you want to run the `track.sh` script described below, you can execute it by running `bash track.sh` in the terminal.

### track.sh

Tracking program that processes videos.

|Variable|Description|
|:-:|:-|
|VIDEO_DIRECTORY|Set to the directory video files are stored in.|
|OUTPUT_DIRECTORY|Set to the directory you want to write your data out to.|
|EXPERIMENT_NAME|Name of your experiment: Will create a directory with the same name in your output directory.|
|TRAINING| Can set to 1 (True) or 0 (False). If set to training mode, the program will terminate after processing 2 mins footage from each video. Does not attempt to classify tags - merely sets them to

### overlay.sh
Overlays tracking and tag pattern classifications onto a video. You can close the window that appears by pressing 'q'.

|Variable|Description|
| :-: |:-|
|FILENAME_PATH|Set to the path of the video you want to see.|
|COORD_FILE_PATH|Set to the path of the csv or json file that was output by the tracking program for that video.|
|CREATE_VIDEO|1 (True) or 0 (False). Outputs a 4K video of overlaid footage but slows down the program.|
|OUTPUT_VIDEO_FILE|Set to the path and filename of the video you wish to output.|

### process_paths.sh

|Variable|Description|
| :-: |:-|
|||
|||
|||

### combine_bg.sh

|Variable|Description|
| :-: |:-|
|||
|||
|||

### reclassify_csv.sh

|Variable|Description|
| :-: |:-|
|||
|||
|||

### output_tags.sh

|Variable|Description|
| :-: |:-|
|||
|||
|||


## Setup

### Dependencies
- Requires Linux/MacOS
- Python 2
- OpenCV 2

### Ubuntu Installation

#### System packages
`sudo apt-get install libopencv-dev python-opencv python-pip exfat-fuse`

#### Python libraries
`pip install numpy matplotlib pandas scipy sklearn cython h5py`

#### Machine Learning Libraries

If you want to set these libraries up to run on the GPU (optional), please follow the steps [here](https://gist.github.com/jackbrucesimpson/854b76ec1a3005af3377f7b22fda1f13) rather than running the command below.

`pip install tensorflow keras`

#### Building

Compile the tracking library in the `bin` directory.

`bash build.sh`
