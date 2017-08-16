import pandas as pd
import cv2
import json

from file_utils import read_coordinates_file, convert_json_paths_to_df
from constants import *

class FrameOverlayer:
    def __init__(self, video_path, coord_file_path):
        self.frame_counter = 0
        self.offset = -20

        self.bees_paths, file_extension = read_coordinates_file(coord_file_path)
        if file_extension == 'json':
            self.bees_paths = convert_json_paths_to_df(self.bees_paths)

    def overlay_frame(self, frame):
        frame_df = self.bees_paths[self.bees_paths['frame_nums']==self.frame_counter]
        frame_num_text = 'Frame: ' + str(self.frame_counter)
        cv2.putText(frame, frame_num_text, (40, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
        for row in frame_df.itertuples():
            cv2.rectangle(frame, (int(row.x-15), int(row.y-15)), (int(row.x+15), int(row.y+15)), (0,255,0), 2)
            frame_class_bee_class_text = tag_class_names[row.classifications]

            cv2.putText(frame, frame_class_bee_class_text, (int(row.x + self.offset), int(row.y + self.offset)), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

        self.frame_counter += 1
        return frame
