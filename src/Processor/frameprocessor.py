import multiprocessing
import cv2
import collections
import operator
import os
import pandas as pd
import numpy as np
import sys
from datetime import datetime
import uuid

from bgimage import BGImage
from utilities import segment_frame, get_video_filename, create_dir_check_exists
from db import DB
from pytrack import PyTrack

class FrameProcessor:
    def __init__(self, video_path, output_directory, experiment_name, is_training, skip_video_if_in_db, num_frames_batch_process, n_processes, chunksize):
        self.is_training = is_training
        self.video_filename = get_video_filename(video_path)
        self.experiment_directory = create_dir_check_exists(output_directory, experiment_name)
        self.experiment_name = experiment_name
        self.bg_image = BGImage()
        self.pytrack = PyTrack()
        self.train_up_to_frame_num = 9600

        self.list_frames_batch = []
        self.frame_counter = 0

        self.num_frames_batch_process = num_frames_batch_process
        self.n_processes = n_processes
        self.chunksize = chunksize

        db_filename = self.experiment_name + '.db'
        self.database_file_path = os.path.join(self.experiment_directory, db_filename)

        if skip_video_if_in_db and os.path.isfile(self.database_file_path):
            db = DB(self.database_file_path)
            video_id, dt = db.get_video_id_start_datetime(self.video_filename)
            db.close_conn()
            if video_id is not None:
                print('Video previously processed', self.video_filename)
                sys.exit(0)

    def append_frame_process(self, frame):
        self.list_frames_batch.append((self.frame_counter, frame))

        if self.frame_counter % self.bg_image.frame_bg_sample_freq == 0:
            self.bg_image.update_bg_average_image(frame)

        self.frame_counter += 1

        if self.frame_counter % self.num_frames_batch_process == 0:
            self.parallel_process_frames()

            if self.is_training and self.frame_counter > self.train_up_to_frame_num:
                print('Finished tag training extraction of video')
                self.output_data()
                sys.exit(0)

    def parallel_process_frames(self):
        print(self.frame_counter)
        processes = multiprocessing.Pool(processes=self.n_processes)
        frames_output_dfs = processes.map(func=segment_frame, iterable=self.list_frames_batch, chunksize=self.chunksize)
        processes.close()
        processes.join()

        df = pd.concat(frames_output_dfs, ignore_index=True)
        df['tag_classes'] = 0
        if self.is_training:
            self.training_track(df)
        else:
            self.track(df)

        self.list_frames_batch = []

    def training_track(self, df):
        df['tag_images_flat'] = df['tag_images'].apply(lambda x: x.flatten().tolist() if x is not None else [])
        sorted_df = df.sort_values(['frame_num'], ascending=True)
        frame_nums_current_batch = sorted_df['frame_num'].unique()
        for fnum in frame_nums_current_batch:
            df_frame_num = sorted_df[sorted_df['frame_num']==fnum]
            self.pytrack.training_track_frame(list(df_frame_num['tag_locs']), list(df_frame_num['tag_images_flat']), fnum)

    def track(self, df):
        df_tags_predicted = df[df['tag_images'].notnull()]
        df_tags_not_predicted = df[df['tag_images'].isnull()]
        #df_tags_predicted['tag_classes'] = # predict tags

        df_classified = pd.concat([df_tags_predicted, df_tags_not_predicted], ignore_index=True)
        df_classified_sorted = df_classified.sort_values(['frame_num'], ascending=True)
        frame_nums_current_batch = df_classified_sorted['frame_num'].unique()

        batch_frame_output = {'tag_locs':[], 'tag_classes':[], 'frame_num':[]}
        for fnum in frame_nums_current_batch:
            df_frame_num = df_classified_sorted[df_classified_sorted['frame_num']==fnum]
            batch_frame_output['tag_locs'].append(list(df_frame_num['tag_locs']))
            batch_frame_output['tag_classes'].append(list(df_frame_num['tag_classes']))
            batch_frame_output['frame_num'].append(fnum)

        self.pytrack.track_frames_batch(batch_frame_output['tag_locs'], batch_frame_output['tag_classes'], batch_frame_output['frame_num'])

    def output_data (self):
        #self.bg_image.output_bg_image(self.experiment_directory, self.video_filename)

        db = DB(self.database_file_path)

        video_id = db.insert_video_info(self.video_filename)
        bee_id = db.get_next_bee_id(video_id)
        bees_dict = {'BEE_ID': [], 'CLASS_CLASSIFIED': [], 'VIDEO_ID': []}
        paths_df = pd.DataFrame()

        all_bees_data = self.pytrack.get_all_bees_data()
        for bee in all_bees_data:
            bee_path_df = pd.DataFrame.from_records(bee['path'])
            bee_path_df['BEE_ID'] = bee_id
            paths_df = pd.concat([paths_df, bee_path_df], ignore_index=True)
            bees_dict['BEE_ID'].append(bee_id)
            bees_dict['VIDEO_ID'].append(video_id)
            bees_dict['CLASS_CLASSIFIED'].append(bee['class_classified'])

            if self.is_training and len(bee['flattened_28x28_tag_matrices']) > 0:
                tag_directory = create_dir_check_exists(self.experiment_directory, self.video_filename)
                bees_tag_directory = create_dir_check_exists(tag_directory, str(bee_id))
                #bees_tag_directory = create_dir_check_exists(tag_directory, uuid.uuid4().hex)
                for flattened_28x28_tag_matrix in bee['flattened_28x28_tag_matrices']:
                    tag_matrix = np.array(flattened_28x28_tag_matrix, dtype=np.uint8).reshape(28, 28)
                    tag_filename = uuid.uuid4().hex + '.png'
                    output_tag_image_path = os.path.join(bees_tag_directory, tag_filename)
                    cv2.imwrite(output_tag_image_path, tag_matrix)

            bee_id += 1

        bees_df = pd.DataFrame(bees_dict)
        db.insert_bees_and_paths(bees_df, paths_df)

        db.close_conn()
