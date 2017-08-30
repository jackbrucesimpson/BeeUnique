import os
import sys

from Processor.Utils.fileutils import create_dir_check_exists
from Processor.Utils.imageutils import combine_night_day_bg

def main():
    datetime_images_dict = {}
    experiment_directory = sys.argv[1]
    image_directory_path = os.path.join(experiment_directory, 'background/')
    averaged_img_directory = create_dir_check_exists(experiment_directory, 'night_day_background')
    output_image_files = True
    night_day_bg_images = combine_night_day_bg(image_directory_path, averaged_img_directory, output_image_files)

if __name__ == "__main__":
    main()
