from utilities import get_video_filename

class FrameOverlayer:
    def __init__(self, video_path, database_file_path):
        video_filename = get_video_filename(video_path)
        self.db = DB(database_file_path)
        video_id = db.get_video_id(video_filename)
        self.bees_df, paths_df, frame_classifications_df = get_bees_paths_frame_classifications_in_video(video_id)
        self.grouped_paths_df = paths_df.groupby(paths_df['FRAME_NUM'])
        self.grouped_frame_classifications_df = frame_classifications_df.groupby(frame_classifications_df['FRAME_NUM'])
        self.frame_counter = 0

    def overlay_frame(self, frame):
        current_frame_path_df = self.grouped_paths_df.get_group(self.frame_counter)
        current_frame_classifications_df = self.grouped_frame_classifications_df.get_group(self.frame_counter)



        self.bees_df['BEE_ID']
        current_frame_coords_df = self.paths_df[[self.paths_df'FRAME_NUM'] == self.frame_counter]
        current_frame_classification_df = self.frame_classifications_df[[self.frame_classifications_df'FRAME_NUM'] == self.frame_counter]



        def overlay_frame(self, frame, tracked_bees):
        for bee in tracked_bees:
            cv2.rectangle(frame, (int(bee['x']-14), int(bee['y']-14)), (int(bee['x']+14), int(bee['y']+14)), (0,255,0), 2)
            #bee['bee_classification'], bee['current_tag_classification']
            return frame

        resized_overlaid_frame = cv2.resize(overlaid_frame, (1280, 720));
        self.frame_counter += 1
        return resized_overlaid_frame
