from Processor.Utils.fileutils import read_json
from Processor.Utils.imageutils import calc_distance, gen_gap_coords

from Processor.Utils import constants

def group_all_data_by_tag_class(video_dt_json_filename):
    tag_class_metrics_grouped_by_video = {tag_class: [] for tag_class in constants.TAG_CLASS_NAMES.keys() if tag_class != constants.UNKNOWN_CLASS}

    video_date_time_list = []

    for dt_bee_json_filename in video_dt_json_filename:
        print('Processed', dt_bee_json_filename['date_time'])
        video_date_time_list.append(dt_bee_json_filename['date_time'])
        tag_class_each_video = {tag_class: [] for tag_class in tag_class_metrics_grouped_by_video}

        bees_json = read_json(dt_bee_json_filename['bees_json_filename'])
        for bee_json in bees_json:
            tag_class = bee_json['tag_class']
            if tag_class == constants.UNKNOWN_CLASS:
                continue

            for path_index in range(len(bee_json['start_frame_nums'])):
                start_frame_num = bee_json['start_frame_nums'][path_index]
                x_path = bee_json['x_paths'][path_index]
                y_path = bee_json['y_paths'][path_index]
                if len(x_path) > 0:
                    tag_class_each_video[tag_class].append({'start_frame_num': start_frame_num, 'x_path': x_path, 'y_path': y_path})

        for tag_class in tag_class_each_video.keys():
            sorted_tag_class_paths_in_video = sorted(tag_class_each_video[tag_class], key=lambda k: k['start_frame_num'])

            paths = categorise_paths_data(sorted_tag_class_paths_in_video)
            tag_class_metrics_grouped_by_video[tag_class].append(paths)

    return (tag_class_metrics_grouped_by_video, video_date_time_list)

def merge_grouped_night_day_video_metrics(tag_class, night_day_grouped_video_metrics):
    merged_night_day_grouped_video_metrics = {'night': [], 'day': []}
    for night_day in night_day_grouped_video_metrics.keys():
        for night_day_time_period_group in night_day_grouped_video_metrics[night_day]:

            merged_video_paths = []
            for video_paths in night_day_time_period_group:
                merged_video_paths = merge_video_paths(merged_video_paths, video_paths)

            if merged_video_paths[-1]['num_frames'] < 1:
                del merged_video_paths[-1]

            merged_night_day_grouped_video_metrics[night_day].append(merged_video_paths)

    return merged_night_day_grouped_video_metrics

def categorise_paths_data(paths_data):
    paths = []

    num_paths = len(paths_data)
    if num_paths == 0:
        entire_video_gap_data = {'is_gap': True, 'prev_next_path_same_loc_disappeared': False, 'num_frames': constants.NUM_FRAMES_IN_VIDEO}
        paths.append(entire_video_gap_data)
        return paths

    start_frame_num = paths_data[0]['start_frame_num']
    x_path = paths_data[0]['x_path']
    y_path = paths_data[0]['y_path']
    path_length = len(x_path)
    path_end_frame_num = start_frame_num + path_length

    start_video_gap_data = {'is_gap': True, 'prev_next_path_same_loc_disappeared': False, 'num_frames': start_frame_num - 1}
    paths.append(start_video_gap_data)

    i = 0
    while i < num_paths:
        start_frame_num = paths_data[i]['start_frame_num']
        x_path = paths_data[i]['x_path']
        y_path = paths_data[i]['y_path']
        path_length = len(x_path)
        path_end_frame_num = start_frame_num + path_length

        # check that you don't have overlapping paths
        ii = i + 1
        while ii < num_paths:
            if path_end_frame_num > paths_data[ii]['start_frame_num']:
                if path_length < len(paths_data[ii]['x_path']):
                    start_frame_num = paths_data[ii]['start_frame_num']
                    x_path = paths_data[ii]['x_path']
                    y_path = paths_data[ii]['y_path']
                    path_length = len(x_path)
                    path_end_frame_num = start_frame_num + path_length
            else:
                break

            ii += 1

        paths.append({'is_gap': False, 'x_path': x_path, 'y_path': y_path, 'num_frames': path_length})
        if ii < num_paths:
            num_frames_path_gap = paths_data[ii]['start_frame_num'] - path_end_frame_num
            gap_data = calc_path_gap(num_frames_path_gap, x_path[-1], y_path[-1], paths_data[ii]['x_path'][0], paths_data[ii]['y_path'][0])
            paths.append(gap_data)

        i = ii

    end_video_gap_data = {'is_gap': True, 'prev_next_path_same_loc_disappeared': False, 'num_frames': constants.NUM_FRAMES_IN_VIDEO - path_end_frame_num - 1}
    paths.append(end_video_gap_data)

    return paths

def merge_video_paths(merged_video_paths, video_paths):
    # entire video gap
    if len(video_paths) == 1:
        if len(merged_video_paths) == 0:
            merged_video_paths.append(video_paths[0])
        else:
            merged_video_paths[-1]['num_frames'] += video_paths[0]['num_frames']
        return merged_video_paths
    # check if no paths or only gap paths stored so far
    # if so, delete first gap if bee was seen from the beginning
    if len(merged_video_paths) < 2:
        if video_paths[0]['num_frames'] < 1:
            del video_paths[0]
        merged_video_paths.extend(video_paths)
    else:
        # see amount of time in last gap prev vid and first gap current video
        # decide whether to delete last or first gap or merge
        num_frames_path_gap = merged_video_paths[-1]['num_frames'] + video_paths[0]['num_frames']
        prev_video_last_x = merged_video_paths[-2]['x_path'][-1]
        prev_video_last_y = merged_video_paths[-2]['y_path'][-1]
        current_video_first_x = video_paths[1]['x_path'][0]
        current_video_first_y = video_paths[1]['y_path'][0]
        gap_data = calc_path_gap(num_frames_path_gap, prev_video_last_x, prev_video_last_y, current_video_first_x, current_video_first_y)

        # delete gaps
        del merged_video_paths[-1]
        del video_paths[0]

        if gap_data['prev_next_path_same_loc_disappeared']:
            generated_coord_gaps = gen_gap_coords(current_video_first_x, current_video_first_y, prev_video_last_x, prev_video_last_y, num_frames_path_gap)
            merged_video_paths[-1]['x_path'].extend(generated_coord_gaps['x'] + video_paths[0]['x_path'])
            merged_video_paths[-1]['y_path'].extend(generated_coord_gaps['y'] + video_paths[0]['y_path'])
            merged_video_paths[-1]['num_frames'] = len(merged_video_paths[-1]['x_path'])
            del video_paths[0]
        else:
            merged_video_paths.append(gap_data)

        merged_video_paths.extend(video_paths)

    return merged_video_paths

def calc_path_gap(num_frames_path_gap, prev_x, prev_y, new_x, new_y):
    distance = calc_distance(prev_x, prev_y, new_x, new_y)
    prev_next_path_same_loc_disappeared = True
    if distance > constants.TRIPLE_TAG_DIAMETER:
        prev_next_path_same_loc_disappeared = False

    gap_data = {'is_gap': True, 'prev_next_path_same_loc_disappeared': prev_next_path_same_loc_disappeared, 'num_frames': num_frames_path_gap}
    if prev_next_path_same_loc_disappeared:
        gap_data['x'] = new_x
        gap_data['y'] = new_y

    return gap_data
