import os
import pandas as pd
import json
import numpy as np
from datetime import datetime

def get_video_filename(file_path):
    head, tail = os.path.split(file_path)
    str_date_time = os.path.splitext(tail)[0]
    return str_date_time

def get_video_datetime(file_path):
    video_filename = get_video_filename(file_path)
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

def read_json(coord_file_path):
    with open(coord_file_path) as json_file:
        coords_data = json.load(json_file)
    return coords_data

def write_json(json_file_path, json_data):
    with open(json_file_path, 'w') as json_output:
        json.dump(json_data, json_output)

def convert_json_paths_to_df(json_paths_data):
    path_data_dict = {'classifications': [], 'x': [], 'y': [], 'frame_nums': [], 'bee_id': []}

    for bee in json_paths_data:
        bee_id = bee['bee_id']
        classification = bee['tag_class']
        for path_index in range(len(bee['x_paths'])):
            frame_num = bee['start_frame_nums'][path_index]
            for coord_index in range(len(bee['x_paths'][path_index])):
                x = bee['x_paths'][path_index][coord_index]
                y = bee['y_paths'][path_index][coord_index]

                path_data_dict['frame_nums'].append(frame_num)
                path_data_dict['x'].append(x)
                path_data_dict['y'].append(y)

                path_data_dict['bee_id'].append(bee_id)
                path_data_dict['classifications'].append(classification)

                frame_num += 1

    path_data_df = pd.DataFrame(path_data_dict)

    return path_data_df
