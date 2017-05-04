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
from keras.models import load_model

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
        self.train_up_to_frame_num = 1000

        if not self.is_training:
            this_dir, this_filename = os.path.split(__file__)
            data_path = os.path.join(this_dir, "data", "model.h5")
            self.model = load_model(data_path)


        self.image_class_names = {0: 'Dot_3_Lines', 1: 'RR', 2: 'Queen', 3: 'Leaf', 4: 'ZZ', 5: 'BB', 6: 'DD', 7: 'Peace', 8: 'Pillars', 9: 'HH', 10: 'Ampersand', \
                                  11: 'JJ', 12: 'n', 13: 'Arrow_Hollow', 14: 'Circle_Cross', 15: 'Plant', 16: 'Diamond', 17: 'Hash', 18: 'NN', 19: 'Ankh', 20: 'Question_Mark', \
                                  21: 'TT', 22: 'Trident', 23: 'Asterisk', 24: 'UU', 25: '1', 26: '0', 27: '3', 28: '2', 29: '3_Lines', 30: '4', 31: '7', 32: '6', 33: '5', 34: \
                                  'Omega', 35: 'Umbrella', 36: 'AA', 37: 'SS', 38: 'Circle_Line', 39: 'Radioactive', 40: 'w', 41: 'Tadpole', 42: 'EE', 43: 'Circle_Half', \
                                  44: 'PP', 45: 'GG', 46: 'XX', 47: 'VV', 48: '8', 49: 'Necklace', 50: 'Triangle', 51: 'Dot', 52: 'a', 53: 'Heart', 54: 'b', 55: 'e', \
                                  56: 'Power', 57: 'g', 58: 'f', 59: 'i', 60: 'h', 61: 'Arrow_Line', 62: 'j', 63: 'Plane', 64: '2_Note', 65: 'KK', 66: 'r', 67: 't', \
                                  68: '1_Note', 69: 'y', 70: 'Scissors', 71: 'MM'}

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

            if self.frame_counter > self.is_training and self.frame_counter > self.train_up_to_frame_num:
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
        df['tag_classes'] = -1
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
        df_tags_predicted['tag_classes'] = self.classify_tags(list(df_tags_predicted['tag_images']))

        df_classified = pd.concat([df_tags_predicted, df_tags_not_predicted], ignore_index=True)
        df_classified_sorted = df_classified.sort_values(['frame_num'], ascending=True)
        frame_nums_current_batch = df_classified_sorted['frame_num'].unique()

        for fnum in frame_nums_current_batch:
            df_frame_num = df_classified_sorted[df_classified_sorted['frame_num']==fnum]
            self.pytrack.track_frame(list(df_frame_num['tag_locs']), list(df_frame_num['tag_classes']), fnum)

    def classify_tags(self, tag_images_list):
        tag_image_array = np.array(tag_images_list)
        tag_image_array_tf_shaped = tag_image_array.reshape(tag_image_array.shape[0], 28, 28, 1)
        tag_image_array_tf_shaped_float = tag_image_array_tf_shaped.astype('float32')
        tag_image_array_tf_shaped_float /= 255
        predict_probabilities = self.model.predict_proba(tag_image_array_tf_shaped_float)
        classifications = [np.argmax(p) if np.amax(p) > 0.8 else -1 for p in predict_probabilities]
        return classifications

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
            #print(bee_path_df['classified'])
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
