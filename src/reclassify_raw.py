import sys

import pandas as pd

from Processor.Utils.fileutils import get_video_filename, create_dir_check_exists
from Processor.Utils.classifier import classify_df_tags
from Processor.Utils import constants

def main():
    json_file_path = sys.argv[1]

    bees_df = pd.read_json(json_file_path)
    bees_df['classifications'] = constants.UNKNOWN_CLASS
    bees_classified = classify_df_tags(bees_df)
    bees_classified.to_json(json_file_path, orient='records')

if __name__ == "__main__":
    main()
