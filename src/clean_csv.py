import numpy as np
import cv2
import os
import sys

from Processor import read_coordinates_file

def main():
    csv_file = sys.argv[1]
    coord_df = read_coordinates_file(csv_file)

if __name__ == "__main__":
    main()
