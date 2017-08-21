import sys

import pandas as pd

from Processor.file_utils import get_video_filename, create_dir_check_exists
from Processor.image_utils import get_json_file_output_tag_images

def main():
    json_file = sys.argv[1]
    experiment_dir_path = sys.argv[2]
    reduce_images = bool(int(sys.argv[3]))

    video_datetime = get_video_filename(json_file)
    get_json_file_output_tag_images(json_file, experiment_dir_path, video_datetime, reduce_images)

if __name__ == "__main__":
    main()
