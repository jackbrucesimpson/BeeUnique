import sys

from Processor.file_utils import get_video_filename, create_dir_check_exists, read_coordinates_file
from Processor.image_utils import classify_df_tags

def main():
    csv_file_path = sys.argv[1]

    bees_df, file_extension = read_coordinates_file(csv_file_path)
    bees_classified_df_sorted = classify_df_tags(bees_df)
    bees_classified_df_sorted.to_csv(csv_file_path, index=False)

if __name__ == "__main__":
    main()
