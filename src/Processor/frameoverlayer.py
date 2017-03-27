from utilities import get_video_filename

class FrameOverlayer:
    def __init__(self, video_path, database_file_path):
        video_filename = get_video_filename(video_path)
        self.db = DB(database_file_path)
        self.video_id = db.get_video_id(video_filename)
        self.frame_counter = 0

    def overlay_frame(self, frame):

        def overlay_frame(self, frame, tracked_bees):
        for bee in tracked_bees:
            cv2.rectangle(frame, (int(bee['x']-14), int(bee['y']-14)), (int(bee['x']+14), int(bee['y']+14)), (0,255,0), 2)
            #bee['bee_classification'], bee['current_tag_classification']
            return frame

        resized_overlaid_frame = cv2.resize(overlaid_frame, (1280, 720));
        self.frame_counter += 1
        return resized_overlaid_frame
