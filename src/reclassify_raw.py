import sys

from Processor.file_utils import get_video_filename, create_dir_check_exists
from Processor.image_utils import classify_df_tags

def main():
    json_file_path = sys.argv[1]

    bees_df = pd.read_json(json_file_path)
    bees_classified_df_sorted = classify_df_tags(bees_df)
    bees_classified_df_sorted.to_json(json_file_path, index=False)

if __name__ == "__main__":
    main()
