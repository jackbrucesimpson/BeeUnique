import cv2
import os
import numpy as np

from fileutils import create_dir_check_exists

class BGImage:
    def __init__(self, experiment_directory, video_filename):
        self.bg_image_dir = create_dir_check_exists(experiment_directory, 'background')
        self.video_filename = video_filename

        self.num_frames_averaged = 0
        self.frame_bg_sample_freq = 20
        self.sum_matrix_bg = None

    def update_bg_average_image(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.sum_matrix_bg is None:
            self.sum_matrix_bg = gray_frame.astype(np.float64)
        else:
            self.sum_matrix_bg += gray_frame.astype(np.float64)
        self.num_frames_averaged += 1

    def output_bg_image(self):
        clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(9,9))
        norm_img = self.sum_matrix_bg / self.num_frames_averaged
        norm_img = norm_img.astype(np.uint8)
        clahe_img = clahe.apply(norm_img)

        image_filename = self.video_filename + '.png'
        file_output = os.path.join(self.bg_image_dir, image_filename)
        cv2.imwrite(file_output, clahe_img)
