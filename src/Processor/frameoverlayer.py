import os

import pandas as pd
import cv2

from file_utils import convert_json_paths_to_df, read_json
from constants import *

class FrameOverlayer:
    def __init__(self, video_filename, experiment_directory, is_raw_coords_file):
        self.frame_counter = 0
        self.offset = -20

        if is_raw_coords_file:
            coords_dir = os.path.join(experiment_directory, 'raw')
            coord_file_path = os.path.join(coords_dir, video_filename + '.json')
            self.bees_df = pd.read_json(coord_file_path)
        else:
            # is processed coords file
            coords_dir = os.path.join(experiment_directory, 'processed')
            coord_file_path = os.path.join(coords_dir, video_filename + '.json')
            json_paths_data = read_json(coord_file_path)
            self.bees_df = convert_json_paths_to_df(json_paths_data)

    def overlay_frame(self, frame):
        frame_df = self.bees_df[self.bees_df['frame_nums']==self.frame_counter]
        frame_num_text = 'Frame: ' + str(self.frame_counter)
        cv2.putText(frame, frame_num_text, (40, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
        for row in frame_df.itertuples():
            cv2.rectangle(frame, (int(row.x-15), int(row.y-15)), (int(row.x+15), int(row.y+15)), (0,255,0), 2)
            frame_class_bee_class_text = tag_class_names[row.classifications]

            cv2.putText(frame, frame_class_bee_class_text, (int(row.x + self.offset), int(row.y + self.offset)), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

        self.frame_counter += 1
        return frame
