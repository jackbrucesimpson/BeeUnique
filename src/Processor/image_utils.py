
import os
import numpy as np
import pandas as pd
import cv2

import uuid
from keras.models import load_model

from file_utils import create_dir_check_exists
from constants import *

def classify_tags(flattened_28x28_tag_matrices):
    this_dir, this_filename = os.path.split(__file__)
    data_path = os.path.join(this_dir, "model.h5")
    model = load_model(data_path)

    tag_image_array = np.array(list(flattened_28x28_tag_matrices))
    tag_image_array_tf_shaped = tag_image_array.reshape(tag_image_array.shape[0], 28, 28, 1)
    tag_image_array_tf_shaped_float = tag_image_array_tf_shaped.astype('float32')
    tag_image_array_tf_shaped_float /= 255
    predict_classes = model.predict_classes(tag_image_array_tf_shaped_float)
    return list(predict_classes)

def classify_df_tags(bees_df):
    if 'classifications' in bees_df.columns:
        del bees_df['classifications']

    bees_df_tags_predicted = bees_df[bees_df['flattened_28x28_tag_matrices'].notnull()]
    bees_df_tags_not_predicted = bees_df[bees_df['flattened_28x28_tag_matrices'].isnull()]

    bees_df_tags_predicted['classifications'] = classify_tags(bees_df_tags_predicted['flattened_28x28_tag_matrices'])
    bees_df_tags_not_predicted['classifications'] = UNKNOWN_CLASS

    bees_classified_df = pd.concat([bees_df_tags_predicted, bees_df_tags_not_predicted], ignore_index=True)
    bees_classified_df_sorted = bees_classified_df.sort_values('frame_nums', ascending=True)
    bees_classified_df_sorted['x'] = bees_df_sorted['x'].astype(int)
    bees_classified_df_sorted['y'] = bees_df_sorted['y'].astype(int)

    return bees_classified_df_sorted

def output_training_images(bee_id, frame_nums, flattened_28x28_tag_matrices, csv_image_output_directory, reduce_images):
    bees_tag_directory = create_dir_check_exists(csv_image_output_directory, str(bee_id))
    tag_images = []
    tag_filenames = []
    for i in range(len(flattened_28x28_tag_matrices)):
        if flattened_28x28_tag_matrices[i] is not None:
            tag_matrix = np.array(flattened_28x28_tag_matrices[i], dtype=np.uint8).reshape(28, 28)
            tag_filename = str(frame_nums[i]) + '_' + uuid.uuid4().hex + '.png'
            output_tag_image_path = os.path.join(bees_tag_directory, tag_filename)
            tag_images.append(tag_matrix)
            tag_filenames.append(output_tag_image_path)

    if reduce_images:
        unique_image_indices = identify_unique_images(tag_images)
        for unique_index in unique_image_indices:
            cv2.imwrite(tag_filenames[unique_index], tag_images[unique_index])
    else:
        for i in range(len(tag_images)):
            cv2.imwrite(tag_filenames[i], tag_images[i])


def identify_unique_images(tag_images):
    unique_images = []
    unique_image_indices = []
    # reverse through list to get most recent unique tag
    num_images_parsed = 0
    for i in range(len(tag_images))[::-1]:
        unseen_image = True
        num_images_parsed += 1
        for unique_image in unique_images:
            err = mse(tag_images[i], unique_image)
            if err < 300:
                unseen_image = False
                break
        if unseen_image:
            unique_images.append(tag_images[i])
            unique_image_indices.append(i)
            # every thousand images clear unique images
            # this let's me find cases where bee paths switched over
        if num_images_parsed % 1000 == 0:
            unique_images = []

    return unique_image_indices

def mse(image1, image2):
    err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
    err /= float(image1.shape[0] * image1.shape[1])
    return err

def segment_frame(counter_frame):
    rect_dims = 14
    frame_num, frame = counter_frame
    frame_height, frame_width, frame_dims = frame.shape
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    smoothed_frame = cv2.GaussianBlur(gray_frame, (9, 9), 0)

    grad_x = cv2.Sobel(smoothed_frame, cv2.CV_16S, 1, 0, ksize=3, scale=1.5, delta=0, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(smoothed_frame, cv2.CV_16S, 0, 1, ksize=3, scale=1.5, delta=0, borderType=cv2.BORDER_DEFAULT)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    scharr = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    ret, thresh = cv2.threshold(scharr, 70, 255, 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(13, 13))
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)


    frame_data = {'frame_num': frame_num, 'x': [], 'y': [], 'tag_matrices': []}

    contours, hierarchy = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        contour_area = cv2.contourArea(cnt)
        if contour_area < 100:
            continue
        if contour_area > 300 and len(cnt) > 8:
            centre, width_height, rotation = cv2.fitEllipse(cnt)
            frame_data['x'].append(centre[0])
            frame_data['y'].append(centre[1])

            if width_height[0] > 23 and width_height[1] > 23 and abs(width_height[0] - width_height[1]) < 5 and width_height[0] < 90 and centre[0] - rect_dims > 0 \
                            and centre[0] + rect_dims < frame_width and centre[1] - rect_dims > 0 and centre[1] + rect_dims < frame_height:
                extracted_tag_matrix = gray_frame[int(centre[1])-rect_dims:int(centre[1])+rect_dims, int(centre[0])-rect_dims:int(centre[0])+rect_dims]
                frame_data['tag_matrices'].append(extracted_tag_matrix)
            else:
                frame_data['tag_matrices'].append(None)

    return frame_data

def increment_dict_key_value(class_dict, classification, num_increment=1):
    if classification in class_dict.keys():
        class_dict[classification] += num_increment
    else:
        class_dict[classification] = num_increment
    return class_dict
