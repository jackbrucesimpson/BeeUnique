import numpy as np
import cv2
import os
import sys

from Processor.file_utils import get_video_filename, create_dir_check_exists, read_coordinates_file,
from Processor.image_utils import output_training_images

from Processor import ProcessPaths

def main():
    csv_file = sys.argv[1]
    video_datetime = get_video_filename(csv_file)
    coord_df = read_coordinates_file(csv_file)







    grouped_bee_id = coord_df_sorted.groupby('bee_id')
    for group_name, group_df in grouped_bee_id:
        print(group_name)
        pp = ProcessPaths(video_datetime)
        bd = pp.process_paths(group_df)
        for b in bd:
            del b['xy_paths']
            print(b)

        break

if __name__ == "__main__":
    main()
