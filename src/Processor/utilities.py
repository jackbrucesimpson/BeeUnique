import cv2
import os
import pandas as pd
import numpy as np
from datetime import datetime

def segment_frame(counter_frame):
    rect_dims = 15
    frame_num, frame = counter_frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    smoothed_frame = cv2.GaussianBlur(gray_frame, (9, 9), 0)

    grad_x = cv2.Sobel(smoothed_frame, cv2.CV_16S, 1, 0, ksize=3, scale=1.5, delta=0, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(smoothed_frame, cv2.CV_16S, 0, 1, ksize=3, scale=1.5, delta=0, borderType=cv2.BORDER_DEFAULT)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    scharr = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    ret, thresh = cv2.threshold(scharr, 70, 255, 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13, 13))
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    tag_locs = []
    tag_images = []

    contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 100:
            centre, width_height, rotation = cv2.minAreaRect(cnt)
            tag_locs.append({'x': centre[0], 'y': centre[1], 'frame_num': frame_num})
            if width_height[0] > 27 and abs(width_height[0] - width_height[1]) < 4 and width_height[0] < 100:
                extracted_tag_matrix = gray_frame[int(centre[1])-rect_dims:int(centre[1])+rect_dims, int(centre[0])-rect_dims:int(centre[0])+rect_dims]
                tag_images.append(extracted_tag_matrix)
            else:
                tag_images.append(None)

    return pd.DataFrame({'frame_num': frame_num, 'tag_locs': tag_locs, 'tag_images': tag_images})

def get_video_filename(video_path):
    head, tail = os.path.split(video_path)
    str_date_time = os.path.splitext(tail)[0]
    #dt = datetime.strptime(str_date_time, "%Y-%m-%d_%H-%M-%S")
    return str_date_time

def create_experiment_directory(output_directory, experiment_name):
    experiment_directory = os.path.join(output_directory, experiment_name)
    if not os.path.exists(experiment_directory):
        os.makedirs(experiment_directory)
    return experiment_directory

def create_tag_directory(experiment_directory, bee_id):
    tag_directory = os.path.join(experiment_directory, bee_id)
    if not os.path.exists(tag_directory):
        os.makedirs(tag_directory)
    return tag_directory
