import multiprocessing
import cv2
import collections
import operator
import os
from datetime import datetime

from bgimage import BGImage
from utilities import segment_frame, get_video_filename
from pytrack import Tracker

class FrameProcessor:
    def __init__(self, video_path, output_directory, is_training):
        self.is_training = is_training
        self.video_filename = get_video_filename(video_path)
        self.output_directory = output_directory
        self.bg_image = BGImage()
        self.tracker = Tracker()

        self.list_frames_batch = []
        self.frame_counter = 0

        self.num_frames_batch_process = 100
        self.n_processes = 4
        self.chunksize = 1

    def append_frame_increment_counter(self, frame):
        self.list_frames_batch.append((self.frame_counter, frame))
        self.frame_counter += 1

        # check to add frame to background average
        if self.frame_counter % self.frame_bg_sample_freq == 0:
            self.bg_image.update_bg_average_image(frame)

        # check if enough frames to process
        if self.frame_counter % self.num_frames_batch_process == 0:
            return True
        else:
            return False

    def parallel_process_frames(self):
        processes = multiprocessing.Pool(processes=self.n_processes)
        frames_output_dfs = processes.map(func=segment_frame, iterable=self.list_frames_batch, chunksize=self.chunksize)
        processes.close()
        processes.join()

        df = pd.concat(frames_output_dfs, ignore_index=True)=
        if self.is_training:
            self.training_track(df)
        else:
            self.track(df)

        self.list_frames_batch = []

    def training_track(self, df):
        df['tag_images_flat'] = df['tag_images'].apply(lambda x: x.flatten().tolist() if x is not np.nan else [])
        for i in range(df['frame_num'].min(), df['frame_num'].max() + 1):
            df_frame_num = df[df['frame_num']==i]
            tracker.training_track_frame(list(df_frame_num['tag_locs']), list(df_frame_num['tag_images_flat']))

    def track(self, df):
        df_tags_predicted = df[df['tag_images'].notnull()]
        df_tags_predicted['tag_classes'] = 0
        df_tags_not_predicted = df[df['tag_images'].isnull()]
        df_tags_not_predicted['tag_classes'] = 0

        df_classified = pd.concat([df_tags_predicted, df_tags_not_predicted], ignore_index=True)

        all_tag_locs = []
        all_tag_classifications = []
        for i in range(df_classified['frame_num'].min(), df_classified['frame_num'].max() + 1):
            df_frame_num = df_classified[df_classified['frame_num']==i]
            all_tag_locs.append(list(df_frame_num['tag_locs']))
            all_tag_classifications.append(list(df_frame_num['tag_classes']))

        tracker.track(all_tag_locs, all_tag_classifications)
