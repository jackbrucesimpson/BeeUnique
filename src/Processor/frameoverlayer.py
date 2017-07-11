from utilities import get_video_filename
from db import DB
import pandas as pd
import cv2

class FrameOverlayer:
    def __init__(self, video_path, database_file_path):
        self.frame_counter = 0
        self.offset = -20
        video_filename = get_video_filename(video_path)
        db = DB(database_file_path)
        video_id, dt = db.get_video_id_start_datetime(video_filename)
        bees_df, paths_df = db.get_bees_paths_dfs(video_id)
        self.bees_paths_df = pd.merge(bees_df, paths_df, on='BEE_ID')
        db.close_conn()

    def overlay_frame(self, frame):

        image_class_names = {0: 'Trident', 1: 'Leaf', 2: 'Note1', 3: 'DD', 4: 'Peace', 5: 'Question', 6: 'Pillars', 7: 'HH', 8: 'Ampersand', 9: 'JJ', 10: 'Notes2', 11: 'Plant', 12: 'Hash', 13: 'Power', 14: '0', 15: 'Ankh', 16: 'TT', 17: 'HollowArrow', 18: 'Asterisk', 19: 'UU', 20: 'Lines3', 21: '1', 22: 'ArrowLine', 23: '3', 24: '2', 25: '5', 26: '4', 27: '7', 28: '6', 29: '8', 30: 'Omega', 31: 'CircleCross', 32: 'AA', 33: 'SS', 34: 'Circle_Line', 35: 'Radioactive', 36: 'Tadpole', 37: 'EE', 38: 'RR', 39: 'PP', 40: 'GG', 41: 'XX', 42: 'ZZ', 43: 'Necklace', 44: 'Triangle', 45: 'Umbrella', 46: 'Dot', 47: 'a', 48: 'Heart', 49: 'e', 50: 'Halfcircle', 51: 'g', 52: 'f', 53: 'KK', 54: 'h', 55: 'Queen', 56: 'Plane', 57: 'n', 58: 'MM', 59: 'r', 60: 'w', 61: 'y', 62: 'Scissors'}

        frame_df = self.bees_paths_df[self.bees_paths_df['FRAME_NUM']==self.frame_counter]
        frame_num_text = 'Frame: ' + str(self.frame_counter)
        cv2.putText(frame, frame_num_text, (40, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
        for row in frame_df.itertuples():
            cv2.rectangle(frame, (int(row.X-15), int(row.Y-15)), (int(row.X+15), int(row.Y+15)), (0,255,0), 2)
            #frame_class_bee_class_text = "{} {} {}".format(row.CLASSIFIED, row.CLASS_CLASSIFIED, row.BEE_ID)

            if row.CLASSIFIED == -1:
                frame_class_bee_class_text = str(row.CLASSIFIED)
            else:
                frame_class_bee_class_text = image_class_names[row.CLASSIFIED]

            cv2.putText(frame, frame_class_bee_class_text, (int(row.X + self.offset), int(row.Y + self.offset)), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

        self.frame_counter += 1
        return frame
