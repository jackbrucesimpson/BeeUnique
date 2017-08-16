import os
import pandas as pd
import numpy as np
from datetime import datetime

def get_video_filename(video_path):
    head, tail = os.path.split(video_path)
    str_date_time = os.path.splitext(tail)[0]
    return str_date_time

def get_video_datetime(video_path):
    video_filename = get_video_filename(video_path)
    return datetime.strptime(video_filename, "%Y-%m-%d_%H-%M-%S")

def create_dir_check_exists(dir_path, new_dir):
    new_directory = os.path.join(dir_path, new_dir)
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)
    return new_directory

def create_experiment_directory(output_directory, experiment_name):
    experiment_directory = os.path.join(output_directory, experiment_name)
    if not os.path.exists(experiment_directory):
        os.makedirs(experiment_directory)
    return experiment_directory

def create_tag_directory(experiment_directory, bee_id):
    tag_directory = os.path.join(experiment_directory, bee_id)
    if not os.path.exists(tag_directory):
        os.makedirs(tag_directory)
    return tag_directory

def read_coordinates_file(coord_file_path):
    file_extension = coord_file_path.split('.')[-1]
    if file_extension == 'csv':
        df = pd.read_csv(coord_file_path)
        df['flattened_28x28_tag_matrices'] = df['flattened_28x28_tag_matrices'].apply(lambda x: eval(x) if x is not np.nan else None)
    elif file_extension == 'json':
        df = pd.read_json(coord_file_path)
    else:
        print('Unknown coordinate file type - not csv or json')
        sys.exit(0)

    return (df, file_extension)

def convert_json_paths_to_df(json_paths_data):
    path_data_dict = {'classifications': [], 'x': [], 'y': [], 'frame_nums': [], 'bee_id': [], 'video_start_datetime': []}

    for bee in json_paths_data:
        for path_index in range(len(bee['x_paths'])):
            bee_id = bee['bee_id']
            classification = bee['tag_class']
            video_start_datetime = bee['video_start_datetime']
            start_path_frame_num = bee['start_frame_nums']

            for coord_index in range(len(bee['x_paths'][path_index])):
                x = bee['x_paths'][path_index][coord_index]
                y = bee['y_paths'][path_index][coord_index]
                frame_num = start_path_frame_num

                path_data_dict['frame_nums'].append(frame_num)
                path_data_dict['x'].append(x)
                path_data_dict['y'].append(y)

                path_data_dict['bee_id'].append(bee_id)
                path_data_dict['classifications'].append(classification)
                path_data_dict['video_start_datetime'].append(video_start_datetime)

                start_path_frame_num += 1

    path_data_df = pd.DataFrame(path_data_dict)

    return path_data_df
