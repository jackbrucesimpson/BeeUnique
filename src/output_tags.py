import sys

import pandas as pd

from Processor.Utils.fileutils import get_video_filename, create_dir_check_exists
from Processor.Utils.imageutils import output_df_tag_images

def main():
    json_file = sys.argv[1]
    experiment_dir_path = sys.argv[2]
    reduce_images = bool(int(sys.argv[3]))
    video_datetime = get_video_filename(json_file)

    bees_df = pd.read_json(json_file)
    output_df_tag_images(bees_df, experiment_dir_path, video_datetime, reduce_images)

if __name__ == "__main__":
    main()
