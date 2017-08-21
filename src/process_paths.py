import os
import sys

from Processor import PathQC

import pandas as pd

from Processor.file_utils import get_video_filename, create_dir_check_exists, write_json
from Processor.image_utils import output_df_tag_images
from Processor import ProcessPaths

def main():
    json_file = sys.argv[1]
    experiment_directory = sys.argv[2]
    overwrite_processed = bool(int(sys.argv[3]))
    output_unknown_tag_path_images = bool(int(sys.argv[4]))
    reduce_images = bool(int(sys.argv[5]))
    print('Processing ' + json_file)

    video_datetime = get_video_filename(json_file)
    processed_directory = create_dir_check_exists(experiment_directory, 'processed')
    json_file_path = os.path.join(processed_directory, video_datetime + '.json')

    if os.path.exists(json_file_path) and not overwrite_processed:
        print('Video already processed')
        sys.exit(0)

    bees_df = pd.read_json(json_file)
    qc = PathQC(video_datetime, experiment_directory)

    all_bees_identified_by_tag = []

    grouped_bee_id = bees_df.groupby('bee_id')
    for bee_id, df_bee_id in grouped_bee_id:
        pp = ProcessPaths()
        bee_paths_list_broken_up_by_class = pp.process_paths(df_bee_id)

        for bee in bee_paths_list_broken_up_by_class:
            all_bees_identified_by_tag.append(bee)

        qc.find_unknown_and_path_lens_in_bee_classes_split_from_path(bee_id, bee_paths_list_broken_up_by_class)

    if output_unknown_tag_path_images:
        output_df_tag_images(bees_df, experiment_directory, video_datetime, reduce_images, qc.bee_ids_with_long_unknowns)

    qc.gen_qc_plot()

    write_json(json_file_path, all_bees_identified_by_tag)

if __name__ == "__main__":
    main()
