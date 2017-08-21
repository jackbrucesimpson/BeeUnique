import multiprocessing
import os
import pandas as pd
import sys

from file_utils import get_video_filename, create_dir_check_exists
from image_utils import segment_frame, classify_df_tags
from pytrack import PyTrack
from bgimage import BGImage

from constants import *

class FrameProcessor:
    def __init__(self, video_path, output_directory, experiment_name, is_training, overwrite_raw, num_frames_batch_process, n_processes, chunksize):
        self.is_training = is_training
        self.experiment_directory = create_dir_check_exists(output_directory, experiment_name)
        self.train_up_to_frame_num = 2000
        self.num_frames_batch_process = num_frames_batch_process
        self.n_processes = n_processes
        self.chunksize = chunksize
        video_filename = get_video_filename(video_path)

        self.pytrack = PyTrack()
        self.bgimage = BGImage(self.experiment_directory, video_filename)

        json_dir = create_dir_check_exists(self.experiment_directory, 'raw')
        self.json_file_path = os.path.join(json_dir, video_filename + '.json')
        if os.path.exists(self.json_file_path) and not overwrite_raw:
            print('Video already processed')
            sys.exit(0)

        self.all_frames_data = {'frame_counter': 0, 'list_frames_batch': [], 'frame_nums': [],
                                'x_grouped_by_frame': [], 'y_grouped_by_frame': [], 'tag_matrices': []}

    def append_frame_process(self, frame):
        self.all_frames_data['list_frames_batch'].append((self.all_frames_data['frame_counter'], frame))

        if self.all_frames_data['frame_counter'] % self.bgimage.frame_bg_sample_freq == 0:
            self.bgimage.update_bg_average_image(frame)

        self.all_frames_data['frame_counter'] += 1

        if self.all_frames_data['frame_counter'] % self.num_frames_batch_process == 0:
            self.parallel_process_frames()

            if self.is_training and self.all_frames_data['frame_counter'] > self.train_up_to_frame_num:
                print('Finished tag training extraction of video. Number of frames processed:', self.all_frames_data['frame_counter'])
                self.output_data()
                sys.exit(0)

    def parallel_process_frames(self):
        print(self.all_frames_data['frame_counter'])
        processes = multiprocessing.Pool(processes=self.n_processes)
        frame_data_list = processes.map(func=segment_frame, iterable=self.all_frames_data['list_frames_batch'], chunksize=self.chunksize)
        processes.close()
        processes.join()

        sorted_frame_data_list = sorted(frame_data_list, key=lambda x: x['frame_num'])
        for frame_data in sorted_frame_data_list:
            self.all_frames_data['frame_nums'].append(frame_data['frame_num'])
            self.all_frames_data['tag_matrices'].extend(frame_data['tag_matrices'])
            self.all_frames_data['x_grouped_by_frame'].append(frame_data['x'])
            self.all_frames_data['y_grouped_by_frame'].append(frame_data['y'])

        self.all_frames_data['list_frames_batch'] = []

    def output_data (self):
        self.bgimage.output_bg_image()

        self.pytrack.track_video(self.all_frames_data['frame_nums'], self.all_frames_data['x_grouped_by_frame'],
                                self.all_frames_data['y_grouped_by_frame'])

        all_bees_data = self.pytrack.get_all_bees_data()
        bees_dict = {'bee_id': [], 'x': [], 'y': [], 'frame_nums': [], 'flattened_28x28_tag_matrices': []}
        bee_id = 0
        for bee in all_bees_data:
            bees_dict['bee_id'].extend([bee_id] * len(bee['frame_nums']))
            bee_id += 1
            bees_dict['x'].extend(bee['x_path'])
            bees_dict['y'].extend(bee['y_path'])
            bees_dict['frame_nums'].extend(bee['frame_nums'])
            for tag_matrix_index in bee['tag_matrix_indices']:
                tag_matrix = self.all_frames_data['tag_matrices'][tag_matrix_index]
                if tag_matrix is not None:
                    tag_matrix = tag_matrix.flatten().tolist()
                bees_dict['flattened_28x28_tag_matrices'].append(tag_matrix)

        bees_df = pd.DataFrame(bees_dict)
        bees_df['classifications'] = UNKNOWN_CLASS
        bees_df['x'] = bees_df['x'].astype(int)
        bees_df['y'] = bees_df['y'].astype(int)

        if not self.is_training:
            bees_df = classify_df_tags(bees_df)

        bees_df.to_json(self.json_file_path, orient='records')
