from Processor.Utils.imageutils import calc_distance, increment_dict_key_value
from Processor.Utils import constants

def calc_path_metrics(night_day_time_period_paths, tag_class):
    all_activity_grouped_by_type = []
    all_distances_per_second_window = []
    all_perimeter_data = []
    all_reappearance_data = []
    cells_visited_speed_groups = {'all': {}, 'moving': {}, 'motionless': {}}
    all_locs_by_sec = {}

    reappearance_data = {'same_loc_disappeared': False, 'num_seconds': 0, 'x': None, 'y': None}
    current_perimeter = {'seconds_present': 0, 'start_coord': {'x': None, 'y': None},
                        'center_coord': {'x': None, 'y': None},
                        'coords': [], 'distances_per_second': [], 'reappearance_data': []}
    current_window = {'yx_cell_coords': [], 'start_coord': {'x': None, 'y': None}, 'seconds_motionless': 0}

    frames_passed_in_time_period = 0
    for path_index in range(len(night_day_time_period_paths)):
        path = night_day_time_period_paths[path_index]
        if path['is_gap']:
            frames_passed_in_time_period += path['num_frames']
            num_seconds = int(round(path['num_frames'] / float(constants.FPS)))
            same_loc_disappeared = path['prev_next_path_same_loc_disappeared']
            all_activity_grouped_by_type.append({'activity': 'absent', 'num_seconds': num_seconds})

            if same_loc_disappeared:
                reappearance_data = {'same_loc_disappeared': same_loc_disappeared, 'num_seconds': num_seconds, 'x': path['x'], 'y': path['y']}
                current_perimeter['reappearance_data'].append(reappearance_data)
                current_perimeter['seconds_present'] += num_seconds
                all_reappearance_data.append(reappearance_data)
            continue

        x_path = path['x_path']
        y_path = path['y_path']
        if current_perimeter['start_coord']['x'] is None:
            current_perimeter['start_coord'] = {'x': x_path[0], 'y': y_path[0]}

        frame_counter = 0
        for i in range(len(x_path)):
            x, y = x_path[i], y_path[i]
            x_cell, y_cell = int(x / constants.X_BINS), int(y / constants.Y_BINS)
            yx_cell_coord = (y_cell, x_cell)

            # store current x,y coord every second
            frames_passed_in_time_period += 1
            if frames_passed_in_time_period % constants.FPS == 0:
                sec_in_time_period = frames_passed_in_time_period / constants.FPS
                all_locs_by_sec[sec_in_time_period] = {'x': x, 'y': y, 'tag_class': tag_class}

            frame_counter += 1
            if frame_counter == 1:
                current_window['start_coord'] = {'x': x, 'y': y}

            if frame_counter % constants.FPS == 0:
                window_distance = calc_distance(x, y, current_window['start_coord']['x'], current_window['start_coord']['y'])
                perimeter_distance = calc_distance(x, y, current_perimeter['start_coord']['x'], current_perimeter['start_coord']['y'])

                if perimeter_distance > constants.PERIMETER_RADIUS:
                    perimeter_metrics(current_perimeter, all_perimeter_data)
                    current_perimeter['start_coord'] = {'x': x, 'y': y}
                else:
                    current_perimeter['seconds_present'] += 1

                all_distances_per_second_window.append(window_distance)
                current_perimeter['distances_per_second'].append(window_distance)

                if window_distance > constants.HALF_TAG_DIAMETER:
                    window_metrics(current_window, cells_visited_speed_groups, all_activity_grouped_by_type)
                else:
                    current_window['seconds_motionless'] += 1

                frame_counter = 0

            current_window['yx_cell_coords'].append(yx_cell_coord)
            current_perimeter['coords'].append({'x': x, 'y': y})

        if current_window['seconds_motionless'] > 0:
            window_metrics(current_window, cells_visited_speed_groups, all_activity_grouped_by_type)

    perimeter_metrics(current_perimeter, all_perimeter_data)

    # return metrics
    return ({
                'all_activity_grouped_by_type': all_activity_grouped_by_type,
                'all_distances_per_second_window': all_distances_per_second_window,
                'all_perimeter_data': all_perimeter_data,
                'all_reappearance_data': all_reappearance_data,
                'cells_visited_speed_groups': cells_visited_speed_groups,
                'all_locs_by_sec': all_locs_by_sec
    })

def window_metrics(current_window, cells_visited_speed_groups, all_activity_grouped_by_type):
    if current_window['seconds_motionless'] < 1:
        speed_group = 'moving'
        all_activity_grouped_by_type.append({'activity': speed_group, 'num_seconds': current_window['seconds_motionless']})
    else:
        speed_group = 'motionless'
        all_activity_grouped_by_type.append({'activity': speed_group, 'num_seconds': current_window['seconds_motionless']})

    for yx in current_window['yx_cell_coords']:
        increment_dict_key_value(cells_visited_speed_groups[speed_group], yx)
        increment_dict_key_value(cells_visited_speed_groups['all'], yx)

    current_window['yx_cell_coords'] = []
    current_window['seconds_motionless'] = 0

def perimeter_metrics(current_perimeter, all_perimeter_data):
    if current_perimeter['seconds_present'] > constants.MIN_NUM_SECONDS_SPENT_IN_AREA:
        coord_center_index = int(len(current_perimeter['coords']) / 2)
        current_perimeter['center_coord'] = current_perimeter['coords'][coord_center_index]
        all_perimeter_data.append(current_perimeter)

    current_perimeter['seconds_present'] = 0
    current_perimeter['start_coord'] = {'x': None, 'y': None}
    current_perimeter['center_coord'] = {'x': None, 'y': None}
    current_perimeter['coords'] = []
    current_perimeter['distances_per_second'] = []
    current_perimeter['reappearance_data'] = []
