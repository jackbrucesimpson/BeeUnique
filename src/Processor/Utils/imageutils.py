
import os
import math

import cv2
import glob
import numpy as np
import uuid

from fileutils import create_dir_check_exists, get_video_datetime
import constants

def calc_distance(x1, y1, x2, y2):
    x_dist = (x2 - x1)
    y_dist = (y2 - y1)
    return math.sqrt(x_dist * x_dist + y_dist * y_dist)

def increment_dict_key_value(dict_counter, key, num_increment=1):
    if key in dict_counter.keys():
        dict_counter[key] += num_increment
    else:
        dict_counter[key] = num_increment

def output_df_tag_images(bees_df, experiment_dir_path, video_datetime, reduce_images, bee_ids_to_output_images=None):
    image_output_directory = create_dir_check_exists(experiment_dir_path, 'training_images')

    grouped_bee_id = bees_df.groupby('bee_id')
    for bee_id, df_bee_id in grouped_bee_id:
        if bee_ids_to_output_images is not None and bee_id not in bee_ids_to_output_images:
            continue
        file_image_output_directory = create_dir_check_exists(image_output_directory, video_datetime)
        output_training_images(bee_id, list(df_bee_id['frame_nums']), list(df_bee_id['flattened_28x28_tag_matrices']), \
                                file_image_output_directory, reduce_images)

def output_training_images(bee_id, frame_nums, flattened_28x28_tag_matrices, file_image_output_directory, reduce_images):
    bees_tag_directory = create_dir_check_exists(file_image_output_directory, str(bee_id))
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

def gen_gap_coords(x1, y1, x2, y2, difference_prev_frame):
    x_diff_per_frame = (x2 - x1) / float(difference_prev_frame)
    y_diff_per_frame = (y2 - y1) / float(difference_prev_frame)

    gap_coords = {'x': [], 'y': []}
    for gap in range(1, difference_prev_frame + 1):
        x_gap_coord = x2 - x_diff_per_frame * gap
        y_gap_coord = y2 - y_diff_per_frame * gap
        gap_coords['x'].append(x_gap_coord)
        gap_coords['y'].append(y_gap_coord)

    return gap_coords

def sort_data_into_time_period(video_dt_data):
    video_dt_data_sorted = sorted(video_dt_data, key=lambda k: k['date_time'])

    is_night = True
    constants.NIGHT_HOURS = [19, 20, 21, 22, 23, 0, 1, 2, 3, 4, 5, 6]

    current_data_list = []
    night_data_lists = []
    day_data_lists = []
    for dt_data in video_dt_data_sorted:
        hour = dt_data['date_time'].hour
        hour_data = dt_data['data']
        if is_night:
            if hour in constants.NIGHT_HOURS:
                current_data_list.append(hour_data)
            else:
                night_data_lists.append(current_data_list)
                current_data_list = [hour_data]
                is_night = False
        else:
            if hour not in constants.NIGHT_HOURS:
                current_data_list.append(hour_data)
            else:
                day_data_lists.append(current_data_list)
                current_data_list = [hour_data]
                is_night = True

    if len(current_data_list) > 0:
        if is_night:
            night_data_lists.append(current_data_list)
        else:
            day_data_lists.append(current_data_list)
        current_data_list = []

    return {'night': night_data_lists, 'day': day_data_lists}

def combine_night_day_bg(image_directory_path, averaged_img_directory=None, output_image_files=False):
    if image_directory_path[-1] != '/':
        image_directory_path += '/'

    video_dt_data = []
    for bg_image_file in glob.glob(image_directory_path + '*.png'):
        image = cv2.imread(bg_image_file, cv2.IMREAD_GRAYSCALE)
        video_dt = get_video_datetime(bg_image_file)
        video_dt_data.append({'date_time': video_dt, 'data': image})

    night_day_data_lists = sort_data_into_time_period(video_dt_data)
    night_day_images = {'night': [], 'day': []}
    for night_or_day in night_day_data_lists.keys():
        night_or_day_count = 0
        night_or_day_id = {'night': '_0_', 'day': '_1_'}
        for time_group in night_day_data_lists[night_or_day]:
            bg_image = time_group[0].astype(np.float64)
            num_images_averaged = 1
            for im in time_group[1:]:
                bg_image += im.astype(np.float64)
                num_images_averaged += 1
            norm_img = bg_image / num_images_averaged
            norm_img = norm_img.astype(np.uint8)
            night_day_images[night_or_day].append(norm_img)
            if output_image_files:
                image_filename = str(night_or_day_count) + night_or_day_id[night_or_day] + night_or_day + '.png'
                file_output = os.path.join(averaged_img_directory, image_filename)
                cv2.imwrite(file_output, norm_img)
                night_or_day_count += 1

    return night_day_images
