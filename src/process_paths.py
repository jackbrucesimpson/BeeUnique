import numpy as np
import cv2
import os
import sys

from Processor import read_coordinates_file, get_video_filename
from Paths import ProcessPaths

def main():
    json_file = sys.argv[1]
    video_datetime = get_video_filename(json_file)
    coord_df = read_coordinates_file(json_file)
    coord_df_sorted = coord_df.sort_values('frame_nums', ascending=True)

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
