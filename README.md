# BeeUnique

Program to track bees with unique tags.

## Setup

### Dependencies
- Requires Linux/MacOS
- Python 2
- OpenCV 2

### Ubuntu Installation

#### System packages
`sudo apt-get install libopencv-dev python-opencv`

#### Python numeric libraries
`pip install numpy matplotlib pandas scipy sklearn  h5py `

#### Machine Learning Libraries

If you want to set these libraries up to run on the GPU, please follow the steps at the bottom of this page rather than running the command below.

`pip install tensorflow keras`

### Building & Running
- Execution scripts are located in the `bin` directory
- Run the `build.sh` script to compile the tracking library
- Run `track.sh` to run the tracking program on videos after you edit it to change these variables:
    - `VIDEO_DIRECTORY` - set to the directory video files are stored in
    - `OUTPUT_DIRECTORY` - set to where you want to write your data out to
- Run `overlay.sh`to see how well the tracker did on a video. You can quit the window by pressing 'q' and you'll need to edit the following variables:
    - `FILENAME_PATH` - set to the path of the video you want to see
    - `CSV_FILE_PATH` - set to the path of the csv file that was output by the tracking program
    - `CREATE_VIDEO` - 1 (True) or 0 (False): Outputs 4K video of overlaid footage but slows down the program
    - `OUTPUT_VIDEO_FILE` - set to the path and filename of the video you wish to output

### Running Machine Learning Libraries on the GPU

If you want to set this up to run on the GPU, then you need to have a machine with an Nvidia GPU and some additional libraries installed.

#### Install CUDA
Go to the [CUDA download](https://developer.nvidia.com/cuda-downloads) page and download the local deb file.

Install the file with the following command (you may have to change the filename).  

```
sudo dpkg -i cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64.deb`
sudo apt-get update
sudo apt-get install cuda
```

Add the following lines to your `.profile` file in your home directory and then load it with `source .profile`

```
export PATH=/usr/local/cuda-8.0/bin${PATH:+:${PATH}}

export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64\
                         ${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```

#### Install CUDNN

Download CUDNN 5.1 (Tensorflow has issues with versions > 6) and once you've extracted the file, navigate into the extracted directory and run the following commands

```
sudo cp -P include/cudnn.h /usr/local/cuda-8.0/include
sudo cp -P lib64/libcudnn* /usr/local/cuda-8.0/lib64
```

#### Install Python Libraries

```
pip install tensorflow-gpu keras
```
