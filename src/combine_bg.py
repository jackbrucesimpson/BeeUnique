import os
import sys

import numpy as np
import cv2
import glob
from datetime import datetime

from Processor import get_video_datetime, create_dir_check_exists

def main():
    datetime_images_dict = {}

    experiment_directory = '/home/jack/Data/Caffeine_Unique_Tags'
    image_directory_path = os.path.join(experiment_directory, 'background') + '/'

    for bg_image_file in glob.glob(image_directory_path + '*.png'):
        video_dt = get_video_datetime(bg_image_file)
        video_date = video_dt.date()
        image = cv2.imread(bg_image_file, cv2.IMREAD_GRAYSCALE)
        if video_date in datetime_images_dict.keys():
            datetime_images_dict[video_date].append(image)
        else:
            datetime_images_dict[video_date] = [image]

    for date in datetime_images_dict.keys():
        bg_image = datetime_images_dict[date][0].astype(np.float64)
        num_images_averaged = 1
        for im in datetime_images_dict[date][1:]:
            bg_image += im.astype(np.float64)
            num_images_averaged += 1
        norm_img = bg_image / num_images_averaged
        norm_img = norm_img.astype(np.uint8)

        image_filename = str(date) + '.png'
        averaged_img_directory = create_dir_check_exists(experiment_directory, 'daily_background')
        file_output = os.path.join(averaged_img_directory, image_filename)
        cv2.imwrite(file_output, norm_img)

if __name__ == "__main__":
    main()
