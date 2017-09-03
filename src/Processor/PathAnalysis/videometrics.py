from Processor.Utils.imageutils import calc_distance
from Processor.Utils import constants

class VideoMetrics:

    def __init__(self):
        self.tag_class_seen_in_video = False
        self.frame_num_first_path_starts = None
        self.frame_nums_left_video_after_last_path_ends = None
        self.first_x_coord = None
        self.first_y_coord = None
        self.last_x_coord = None
        self.last_y_coord = None

        self.path_gap_data = []
        self.path_gap_data_same_spot = []

        self.x_paths = []
        self.y_paths = []


        self.cells_visited_speed_groups = {'all': {}, 'moving': {}, 'motionless_short': {}, 'motionless_long': {}}

        distances_per_second_window = []
        seconds_spent_in_perimeter = []
        consecutive_seconds_motionless = []
        long_stay_perimeter_coord_data = []




    def add_paths_data(self, paths_data):
        num_paths = len(paths_data)
        if num_paths > 0:
            self.tag_class_seen_in_video = True

        i = 0
        while i < len(paths_data):
            start_frame_num = paths_data[i]['start_frame_num']
            x_path = paths_data[i]['x_path']
            y_path = paths_data[i]['y_path']
            path_length = len(x_path)
            end_frame_num = start_frame_num + path_length

            # check that you don't have overlapping paths
            ii = i + 1
            while ii < num_paths:
                if end_frame_num > paths_data[ii]['start_frame_num']:
                    if path_length < len(paths_data[ii]['x_path']):
                        start_frame_num = paths_data[ii]['start_frame_num']
                        x_path = paths_data[ii]['x_path']
                        y_path = paths_data[ii]['y_path']
                        path_length = len(x_path)
                        end_frame_num = start_frame_num + path_length
                else:
                    num_frames_path_gap = paths_data[ii]['start_frame_num'] - end_frame_num
                    distance = calc_distance(x_path[-1], y_path[-1], paths_data[ii]['x_path'][0], paths_data[ii]['y_path'][0])
                    if distance > constants.DOUBLE_TAG_DIAMETER:
                        gap_data = {'prev_x': x_path[-1], 'prev_y': y_path[-1], 'new_x': paths_data[ii]['x_path'][0], 'new_y': paths_data[ii]['y_path'][0], 'num_frames_path_gap': num_frames_path_gap, 'frame_num_disappeared': end_frame_num}
                        self.path_gap_data.append(gap_data)
                    else:
                        gap_data = {'prev_x': x_path[-1], 'prev_y': y_path[-1], 'new_x': paths_data[ii]['x_path'][0], 'new_y': paths_data[ii]['y_path'][0], 'num_frames_path_gap': num_frames_path_gap, 'frame_num_disappeared': end_frame_num}
                        self.path_gap_data_same_spot.append(gap_data)
                    break

                ii += 1

            self.frame_nums_left_video_after_last_path_ends = constants.NUM_FRAMES_IN_VIDEO - end_frame_num
            self.last_x_coord = x_path[-1]
            self.last_y_coord = y_path[-1]
            self.x_paths.append(x_path)
            self.y_paths.append(y_path)

            if self.frame_num_first_path_starts is None:
                self.frame_num_first_path_starts = start_frame_num
                self.first_x_coord = x_path[0]
                self.first_y_coord = y_path[0]

            i = ii


    def process_path(self.):
        perimeter_coord = None
        perimeter_counter = 0
        current_perimeter_yx_cell_coords = []
        current_perimeter_window_distances = []
        seconds_motionless_counter = 0

        start_window_coord = None
        current_window_yx_cell_coords = []
        frame_counter = 0

        for i in range(len(x_path)):
            x, y = x_path[i], y_path[i]
            x_cell, y_cell = int(x / constants.X_BINS), int(y / constants.Y_BINS)
            yx_cell_coord = (y_cell, x_cell)
            current_perimeter_yx_cell_coords.append(yx_cell_coord)
            current_window_yx_cell_coords.append(yx_cell_coord)

            frame_counter += 1
            if frame_counter == 1:
                start_window_coord = (x, y)
                if perimeter_coord is None:
                    perimeter_coord = (x, y)
            if frame_counter % constants.FPS == 0:
                window_distance = calc_distance(x, y, start_window_coord[0], start_window_coord[1])
                distances_per_second_window.append(window_distance)
                current_perimeter_window_distances.append(window_distance)

                if window_distance > 10:
                    if seconds_motionless_counter == 0:
                        speed_group = 'moving'
                    elif seconds_motionless_counter < 120:
                        speed_group = 'motionless_short'
                    else:
                        speed_group = 'motionless_long'
                        if seconds_motionless_counter > 900:
                            print(seconds_motionless_counter, self.video_date_time_list[c])

                    for yx in current_window_yx_cell_coords:
                        cells_visited_speed_groups[speed_group] = increment_dict_key_value(cells_visited_speed_groups[speed_group], yx)
                        cells_visited_speed_groups['all'] = increment_dict_key_value(cells_visited_speed_groups['all'], yx)

                    consecutive_seconds_motionless.append(seconds_motionless_counter)
                    current_window_yx_cell_coords = []
                    seconds_motionless_counter = 0
                else:
                    seconds_motionless_counter += 1

                frame_counter = 0

                perimeter_counter += 1
                perimeter_distance = calc_distance(x, y, perimeter_coord[0], perimeter_coord[1])
                if perimeter_distance > 200:
                    seconds_spent_in_perimeter.append(perimeter_counter)
                    if perimeter_counter > 30:
                        long_stay_perimeter_coord_data.append({'x': perimeter_coord[0], 'y': perimeter_coord[1], 'seconds_spent_in_perimeter': perimeter_counter, 'current_perimeter_window_distances': current_perimeter_window_distances, 'current_perimeter_yx_cell_coords': current_perimeter_yx_cell_coords})
                    perimeter_coord = (x, y)
                    perimeter_counter = 0
                    current_perimeter_yx_cell_coords = []

        if seconds_motionless_counter > 0:
            if seconds_motionless_counter < 120:
                speed_group = 'motionless_short'
            else:
                speed_group = 'motionless_long'
                if seconds_motionless_counter > 900:
                    print(seconds_motionless_counter, self.video_date_time_list[c])
            for yx in current_window_yx_cell_coords:
                cells_visited_speed_groups[speed_group] = increment_dict_key_value(cells_visited_speed_groups[speed_group], yx)
                cells_visited_speed_groups['all'] = increment_dict_key_value(cells_visited_speed_groups['all'], yx)

            consecutive_seconds_motionless.append(seconds_motionless_counter)


        if perimeter_counter > 30:
            long_stay_perimeter_coord_data.append({'x': perimeter_coord[0], 'y': perimeter_coord[1], 'seconds_spent_in_perimeter': perimeter_counter, 'current_perimeter_window_distances': current_perimeter_window_distances, 'current_perimeter_yx_cell_coords': current_perimeter_yx_cell_coords})
