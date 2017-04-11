from utilities import get_video_filename

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
        frame_df = self.paths_df[self.paths_df['FRAME_NUM']==self.frame_counter]
        for row in bees_paths_df.itertuples():
            cv2.rectangle(frame, (int(row.X-15), int(row.Y-15)), (int(row.X+15), int(row.Y+15)), (0,255,0), 2)
            frame_class_bee_class_text = "{} {}".format(row.CLASSIFIED, row.CLASS_CLASSIFIED)
            cv2.putText(frame, frame_class_bee_class_text, (row.X + self.offset, row.X + self.offset), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

        resized_frame = cv2.resize(frame, (1280, 720));
        self.frame_counter += 1
        return resized_frame
