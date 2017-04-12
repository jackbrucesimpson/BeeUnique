from utilities import get_video_filename
from db import DB
import pandas as pd
import cv2

class FrameOverlayer:
    def __init__(self, video_path, database_file_path):
        self.frame_counter = 0
        self.offset = 10
        video_filename = get_video_filename(video_path)
        db = DB(database_file_path)
        video_id, dt = db.get_video_id_start_datetime(video_filename)
        bees_df, paths_df = db.get_bees_paths_dfs(video_id)
        self.bees_paths_df = pd.merge(bees_df, paths_df, on='BEE_ID')
        db.close_conn()

    def overlay_frame(self, frame):
        frame_df = self.bees_paths_df[self.bees_paths_df['FRAME_NUM']==self.frame_counter]
        frame_num_text = 'Frame: ' + str(self.frame_counter)
        cv2.putText(frame, frame_num_text, (40, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
        for row in frame_df.itertuples():
            cv2.rectangle(frame, (int(row.X-15), int(row.Y-15)), (int(row.X+15), int(row.Y+15)), (0,255,0), 2)
            frame_class_bee_class_text = "{} {} {}".format(row.CLASSIFIED, row.CLASS_CLASSIFIED, row.BEE_ID)
            cv2.putText(frame, frame_class_bee_class_text, (int(row.X + self.offset), int(row.Y + self.offset)), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

        resized_frame = cv2.resize(frame, (1280, 720));
        self.frame_counter += 1
        return resized_frame
