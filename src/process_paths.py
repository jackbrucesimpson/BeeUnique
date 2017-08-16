import numpy as np
import cv2
import os
import sys
import json

from Processor.file_utils import get_video_filename, create_dir_check_exists, read_coordinates_file
from Processor.image_utils import increment_dict_key_value
from Processor import ProcessPaths
from Processor.constants import *

def main():
    csv_file = sys.argv[1]
    experiment_directory = sys.argv[2]

    video_datetime = get_video_filename(csv_file)
    json_directory = create_dir_check_exists(experiment_directory, 'json')
    json_file_path = os.path.join(json_directory, video_datetime + '.json')

    bees_df, file_extension = read_coordinates_file(csv_file)

    #all_bee_individual_path_broken_up_by_tag_class = []
    all_bees_identified_by_tag = []
    bee_ids_with_long_unknowns = []

    class_num_frames_tracked_dict = {}

    grouped_bee_id = bees_df.groupby('bee_id')
    for bee_id, df_bee_id in grouped_bee_id:
        pp = ProcessPaths(video_datetime)
        bee_paths_list_broken_up_by_class = pp.process_paths(df_bee_id)
        bee_path_classes_num_frames_tracked = pp.get_class_num_frames_tracked(bee_paths_list_broken_up_by_class)

        for bee in bee_paths_list_broken_up_by_class:
            all_bees_identified_by_tag.append(bee)


        for bee_path_class in bee_path_classes_num_frames_tracked:
            class_num_frames_tracked_dict = increment_dict_key_value(class_num_frames_tracked_dict, \
                                            bee_path_class['tag_class'], bee_path_class['num_frames_tracked'])

            if bee_path_class['tag_class'] == UNKNOWN_CLASS:
                if bee_path_class['num_frames_tracked'] > NUM_UNKNOWNS_IN_PATH_THRESHOLD:
                    bee_ids_with_long_unknowns.append(bee_id)

    #if len(bee_ids_with_long_unknowns) > 1:
        #


    print(class_num_frames_tracked_dict)
    print(bee_ids_with_long_unknowns)

    with open(json_file_path, 'w') as json_output:
        json.dump(all_bees_identified_by_tag, json_output)

if __name__ == "__main__":
    main()
