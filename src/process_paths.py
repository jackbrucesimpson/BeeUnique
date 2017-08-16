import numpy as np
import cv2
import os
import sys
import json

from Processor.file_utils import get_video_filename, create_dir_check_exists, read_coordinates_file

from Processor import ProcessPaths

def main():
    csv_file = sys.argv[1]
    experiment_directory = sys.argv[2]

    video_datetime = get_video_filename(csv_file)
    json_directory = create_dir_check_exists(experiment_directory, 'json')
    json_file_path = os.path.join(json_directory, video_datetime + '.json')

    bees_df, file_extension = read_coordinates_file(csv_file)

    all_bees_identified_by_tag = []
    grouped_bee_id = bees_df.groupby('bee_id')
    for bee_id, df_bee_id in grouped_bee_id:
        pp = ProcessPaths(video_datetime)
        bees_identified_by_tag = pp.process_paths(df_bee_id)
        for bee in bees_identified_by_tag:
            all_bees_identified_by_tag.append(bee) ## do qc here

    with open(json_file_path, 'w') as json_output:
        json.dump(all_bees_identified_by_tag, json_output)


if __name__ == "__main__":
    main()
