import numpy as np
import cv2
import os
import sys

from Processor.file_utils import get_video_filename, create_dir_check_exists, write_json
from Processor.image_utils import increment_dict_key_value
from Processor import ProcessPaths
from Processor.constants import *

def main():
    json_file = sys.argv[1]
    experiment_directory = sys.argv[2]
    overwrite_processed = bool(int(sys.argv[3]))

    video_datetime = get_video_filename(json_file)
    processed_directory = create_dir_check_exists(experiment_directory, 'processed')
    json_file_path = os.path.join(processed_directory, video_datetime + '.json')

    if os.path.exists(json_file_path) and not overwrite_processed:
        print('Video already processed')
        sys.exit(0)

    bees_df = pd.read_json(json_file)

    #all_bee_individual_path_broken_up_by_tag_class = []
    all_bees_identified_by_tag = []
    bee_ids_with_long_unknowns = []

    class_num_frames_tracked_dict = {}

    grouped_bee_id = bees_df.groupby('bee_id')
    for bee_id, df_bee_id in grouped_bee_id:
        pp = ProcessPaths()
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
        #{'video_datetime': [], 'bee_id': []}

    print(class_num_frames_tracked_dict)
    print(bee_ids_with_long_unknowns)

    write_json(json_file_path, all_bees_identified_by_tag)

if __name__ == "__main__":
    main()
