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
from pytrack import PyTrack

class FrameProcessor:
    def __init__(self, video_path, output_directory, experiment_name, is_training, num_frames_batch_process, n_processes, chunksize):
        self.is_training = is_training
        self.video_filename = get_video_filename(video_path)
        self.experiment_directory = create_dir_check_exists(output_directory, experiment_name)
        self.experiment_name = experiment_name
        self.pytrack = PyTrack()
        self.train_up_to_frame_num = 2000
        self.unknown_class = 3

        json_dir = create_dir_check_exists(self.experiment_directory, 'json')
        self.json_filename = os.path.join(json_dir, self.video_filename + '.json')
        bg_image_dir = create_dir_check_exists(self.experiment_directory, 'background')

        self.bg_image = BGImage(bg_image_dir, self.video_filename)

        if os.path.exists(self.json_filename):
            print('Video already processed')
            sys.exit(0)

        if not self.is_training:
            this_dir, this_filename = os.path.split(__file__)
            data_path = os.path.join(this_dir, "data", "model.h5")
            self.model = load_model(data_path)

        self.list_frames_batch = []
        self.frame_counter = 0

        self.num_frames_batch_process = num_frames_batch_process
        self.n_processes = n_processes
        self.chunksize = chunksize

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
        frame_data_list = processes.map(func=segment_frame, iterable=self.list_frames_batch, chunksize=self.chunksize)
        processes.close()
        processes.join()

        sorted_frame_data_list = sorted(frame_data_list, key=lambda x: x['frame_num'])
        for frame_data in sorted_frame_data_list:
            self.pytrack.track_frame(frame_data['xy'], frame_data['flat_tag_matrices'], frame_data['frame_num'])

        self.list_frames_batch = []

    def classify_tags(self, flattened_28x28_tag_matrices):
        tag_image_array = np.array(list(flattened_28x28_tag_matrices))
        tag_image_array_tf_shaped = tag_image_array.reshape(tag_image_array.shape[0], 28, 28, 1)
        tag_image_array_tf_shaped_float = tag_image_array_tf_shaped.astype('float32')
        tag_image_array_tf_shaped_float /= 255
        predict_classes = self.model.predict_classes(tag_image_array_tf_shaped_float)
        return list(predict_classes)

    def output_training_images(self, bee_id, frame_nums, flattened_28x28_tag_matrices):
        training_images_dir = create_dir_check_exists(self.experiment_directory, 'training_images')
        tag_directory = create_dir_check_exists(training_images_dir, self.video_filename)
        bees_tag_directory = create_dir_check_exists(tag_directory, str(bee_id))
        for i, flattened_28x28_tag_matrix in enumerate(flattened_28x28_tag_matrices):
            if len(flattened_28x28_tag_matrix) > 0:
                tag_matrix = np.array(flattened_28x28_tag_matrix, dtype=np.uint8).reshape(28, 28)
                tag_filename = str(frame_nums[i]) + '_' + uuid.uuid4().hex + '.png'
                output_tag_image_path = os.path.join(bees_tag_directory, tag_filename)
                cv2.imwrite(output_tag_image_path, tag_matrix)

    def output_data (self):
        self.bg_image.output_bg_image()

        all_bees_data = self.pytrack.get_all_bees_data()
        bees_dict = {'bee_id': [], 'xy': [], 'frame_nums': [], 'flattened_28x28_tag_matrices': []}
        bee_id = 0
        for bee in all_bees_data:
            bees_dict['bee_id'].extend([bee_id] * len(bee['frame_nums']))
            bee_id += 1
            bees_dict['xy'].extend(bee['xy'])
            bees_dict['frame_nums'].extend(bee['frame_nums'])
            bees_dict['flattened_28x28_tag_matrices'].extend(bee['flattened_28x28_tag_matrices'])

            if self.is_training:
                self.output_training_images(bee_id, bee['frame_nums'], bee['flattened_28x28_tag_matrices'])

        bees_df = pd.DataFrame(bees_dict)
        bees_df['classifications'] = self.unknown_class
        bees_df['flattened_28x28_tag_matrices'] = bees_df['flattened_28x28_tag_matrices'].apply(lambda x: x if len(x) > 0 else None)

        bees_df_tags_predicted = bees_df[bees_df['flattened_28x28_tag_matrices'].notnull()]
        bees_df_tags_not_predicted = bees_df[bees_df['flattened_28x28_tag_matrices'].isnull()]

        if not self.is_training:
            bees_df_tags_predicted['classifications'] = self.classify_tags(bees_df_tags_predicted['flattened_28x28_tag_matrices'])

        bees_classified_df = pd.concat([bees_df_tags_predicted, bees_df_tags_not_predicted], ignore_index=True)

        bees_classified_df.to_json(self.json_filename, orient='records')
