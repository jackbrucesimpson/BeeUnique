import multiprocessing
import cv2
import collections
import operator
import os
import sys
from datetime import datetime
import uuid

from bgimage import BGImage
from utilities import segment_frame, get_video_filename, create_experiment_directory, create_tag_directory
from db import DB
from pytrack import Tracker

class FrameProcessor:
    def __init__(self, video_path, output_directory, experiment_name, is_training):
        self.is_training = is_training
        self.video_filename = get_video_filename(video_path)
        self.experiment_directory = create_experiment_directory(output_directory, experiment_name)
        self.experiment_name = experiment_name
        self.bg_image = BGImage()
        self.tracker = Tracker()
        # frame nums for 5 minute training segments 0-5, 15-20, 30-35, 45-50 minutes @ 20 fps
        self.train_5_min_segment = ((0, 6000), (18000, 24000), (36000, 42000), (54000, 60000))
        self.segment_index = 0

        self.list_frames_batch = []
        self.frame_counter = 0

        self.num_frames_batch_process = 100
        self.n_processes = 4
        self.chunksize = 1

    def append_frame_increment_counter(self, frame):
        # if training, only process 4 blocks of 5 minutes from video
        if self.is_training:
            if self.frame_counter >= self.train_5_min_segment[self.segment_index][0] and self.frame_counter <= self.train_5_min_segment[self.segment_index][1]:
                pass
            else:
                if self.frame_counter > self.train_5_min_segment[self.segment_index][0]:
                    if len(self.train_5_min_segment) < self.segment_index:
                        self.segment_index += 1
                        self.frame_counter += 1
                        self.parallel_process_frames()
                        return False
                    else:
                        print('Finishing training processing of video')
                        sys.exit(0)
                else:
                    self.frame_counter += 1
                    return False

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

        df = pd.concat(frames_output_dfs, ignore_index=True)
        if self.is_training:
            self.training_track(df)
        else:
            self.track(df)

        self.list_frames_batch = []

    def training_track(self, df):
        df['tag_images_flat'] = df['tag_images'].apply(lambda x: x.flatten().tolist() if x is not np.nan else [])
        for i in range(df['frame_num'].min(), df['frame_num'].max() + 1):
            df_frame_num = df[df['frame_num']==i]
            tracker.training_track_frame(list(df_frame_num['tag_locs']), list(df_frame_num['tag_images_flat']), i)

    def track(self, df):
        df_tags_predicted = df[df['tag_images'].notnull()]
        df_tags_predicted['tag_classes'] = 0
        df_tags_not_predicted = df[df['tag_images'].isnull()]
        df_tags_not_predicted['tag_classes'] = 0

        df_classified = pd.concat([df_tags_predicted, df_tags_not_predicted], ignore_index=True)

        all_tag_locs = []
        all_tag_classifications = []
        all_frame_nums_batch = []
        for i in range(df_classified['frame_num'].min(), df_classified['frame_num'].max() + 1):
            df_frame_num = df_classified[df_classified['frame_num']==i]
            all_tag_locs.append(list(df_frame_num['tag_locs']))
            all_tag_classifications.append(list(df_frame_num['tag_classes']))
            all_frame_nums_batch.append(i)

        tracker.track_frames_batch(all_tag_locs, all_tag_classifications, all_frame_nums_batch)

    def output_data (self):
        self.bg_image.output_background_image(self.experiment_directory, self.video_filename)
        db_filename = self.experiment_name + '.db'
        database_file_path = os.path.join(self.experiment_directory, db_filename)
        db = DB(database_file_path)
        db.video_id = self.insert_video_info(self.experiment_name, self.video_filename)

        all_bees_data = tracker.get_all_bees_data()
        for bee in all_bees_data:
            bee_id = db.insert_bee(bee['class_classified'])
            for point in bee['path']:
                db.insert_path(bee_id, point['x'], point['y'], point['frame_num'])
            for frame_classified in bee['classifications']:
                db.insert_classifications(bee_id, frame_classified['classified'], frame_classified['frame_num'])

            if self.is_training:
                tag_directory = create_tag_directory(self.experiment_directory, bee['id'])
                for flattened_28x28_tag_matrix in bee['flattened_28x28_tag_matrices']:
                    tag_matrix = np.array(flattened_28x28_tag_matrix, dtype=uint8).reshape(28, 28)
                    tag_filename = uuid.uuid4().hex + '.png'
                    output_tag_image_path = os.path.join(tag_directory, tag_filename)
                    cv2.imwrite(output_tag_image_path, tag_matrix)

        db.close_conn()
