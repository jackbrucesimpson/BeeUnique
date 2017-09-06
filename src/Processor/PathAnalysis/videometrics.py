from Processor.Utils.imageutils import calc_distance, gen_gap_coords, increment_dict_key_value
from Processor.Utils import constants

class VideoMetrics:

    def __init__(self):
        self.tag_class_seen = False

        self.frame_num_first_path_starts = None
        self.frame_nums_left_video_after_last_path_ends = None

        self.x_paths = []
        self.y_paths = []
        self.path_gap_data = []

        # motionless_data:
        self.current_window = {'yx_cell_coords': [], 'coords': [], 'start_coord': {'x': None, 'y': None}, 'seconds_motionless': 0}
        self.current_perimeter = {'seconds_present': 0, 'yx_cell_coords': [], 'coords': [],
                                'start_coord': {'x': None, 'y': None}, 'center_coord': {'x': None, 'y': None},
                                'distances_per_second': [], 'motionless_data': []}

        self.all_distances_per_second_window = []
        self.all_motionless_data = []

        self.all_perimeter_data = []
        self.cells_visited_speed_groups = {'all': {}, 'moving': {}, 'motionless': {}}

    def merge_video_metrics(self, vm):
        if vm.tag_class_seen == False:
            gap_data = {'absent_in_video': True, 'num_frames_path_gap': constants.NUM_FRAMES_IN_VIDEO}
            self.path_gap_data.append(gap_data)
            return None
        elif self.tag_class_seen == False or len(self.path_gap_data) == 0:
            self.tag_class_seen = True
        else:
            last_path_gap = self.path_gap_data[-1]
            if not last_path_gap['absent_in_video']:
                last_x_path_prev_video = self.x_paths[-1]
                last_y_path_prev_video = self.y_paths[-1]
                fist_x_path_current_video = vm.x_paths[0]
                fist_y_path_current_video = vm.y_paths[0]

                prev_video_last_x = last_x_path_prev_video[-1]
                prev_video_last_y = last_y_path_prev_video[-1]
                current_video_first_x = fist_x_path_current_video[0]
                current_video_first_y = fist_y_path_current_video[0]
                num_frames_path_gap = self.frame_nums_left_video_after_last_path_ends + vm.frame_num_first_path_starts

                gap_data = self.calc_path_gap(num_frames_path_gap, prev_video_last_x, prev_video_last_y, current_video_first_x, current_video_first_y)
                if gap_data['same_location_disappeared'] and num_frames_path_gap < constants.MAX_FRAME_GAP_BETWEEN_VIDEOS:
                    generated_coord_gaps = gen_gap_coords(current_video_first_x, current_video_first_y, prev_video_last_x, prev_video_last_y, num_frames_path_gap)
                    self.x_paths[-1].extend(generated_coord_gaps['x'])
                    self.y_paths[-1].extend(generated_coord_gaps['y'])
                    self.x_paths[-1].extend(vm.x_paths[0])
                    self.y_paths[-1].extend(vm.y_paths[0])
                    del vm.x_paths[0]
                    del vm.y_paths[0]
                else:
                    self.path_gap_data.append(gap_data)

        self.x_paths.extend(vm.x_paths)
        self.y_paths.extend(vm.y_paths)
        self.path_gap_data.extend(vm.path_gap_data)

        self.frame_nums_left_video_after_last_path_ends = vm.frame_nums_left_video_after_last_path_ends

    def add_paths_data(self, paths_data):
        num_paths = len(paths_data)
        if num_paths > 0:
            self.tag_class_seen = True
        else:
            return None

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
                    num_frames_path_gap = paths_data[ii]['start_frame_num'] - path_end_frame_num
                    #print(len(x_path), len(paths_data[ii]['x_path']))
                    gap_data = self.calc_path_gap(num_frames_path_gap, x_path[-1], y_path[-1], paths_data[ii]['x_path'][0], paths_data[ii]['y_path'][0])
                    self.path_gap_data.append(gap_data)
                    break

                ii += 1

            self.frame_nums_left_video_after_last_path_ends = constants.NUM_FRAMES_IN_VIDEO - path_end_frame_num
            self.x_paths.append(x_path)
            self.y_paths.append(y_path)

            if self.frame_num_first_path_starts is None:
                self.frame_num_first_path_starts = start_frame_num

            i = ii

    def calc_path_gap(self, num_frames_path_gap, prev_x, prev_y, new_x, new_y):
        distance = calc_distance(prev_x, prev_y, new_x, new_y)
        same_location_disappeared = True
        if distance > constants.DOUBLE_TAG_DIAMETER:
            same_location_disappeared = False

        gap_data = {'prev_x': prev_x, 'prev_y': prev_y, 'new_x': new_x,
                    'new_y': new_y, 'num_frames_path_gap': num_frames_path_gap,
                    'distance_prev_new_coord': distance,
                    'same_location_disappeared': same_location_disappeared,
                    'absent_in_video': False}
        return gap_data

    def calc_metrics(self):
        if not self.tag_class_seen:
            return None

        self.current_perimeter['start_coord'] = {'x': self.x_paths[0][0], 'y': self.y_paths[0][0]}

        for path_index in range(len(self.x_paths)):
            x_path = self.x_paths[path_index]
            y_path = self.y_paths[path_index]

            frame_counter = 0
            for i in range(len(x_path)):
                x, y = x_path[i], y_path[i]
                x_cell, y_cell = int(x / constants.X_BINS), int(y / constants.Y_BINS)
                yx_cell_coord = (y_cell, x_cell)

                frame_counter += 1
                if frame_counter == 1:
                    self.current_window['start_coord'] = {'x': x, 'y': y}
                if frame_counter % constants.FPS == 0:
                    window_distance = calc_distance(x, y, self.current_window['start_coord']['x'], self.current_window['start_coord']['y'])

                    perimeter_distance = calc_distance(x, y, self.current_perimeter['start_coord']['x'], self.current_perimeter['start_coord']['y'])

                    self.speed_metrics(x, y, window_distance, perimeter_distance)

                    self.all_distances_per_second_window.append(window_distance)
                    self.current_perimeter['distances_per_second'].append(window_distance)

                    frame_counter = 0

                self.current_window['yx_cell_coords'].append(yx_cell_coord)
                self.current_perimeter['yx_cell_coords'].append(yx_cell_coord)

                self.current_window['coords'].append({'x': x, 'y': y})
                self.current_perimeter['coords'].append({'x': x, 'y': y})

            if self.current_window['seconds_motionless'] > 0:
                self.speed_metrics(end_of_path=True)

        if self.current_perimeter['seconds_present'] > constants.MIN_NUM_SECONDS_SPENT_IN_AREA:
            coord_center_index = int(len(self.current_perimeter['coords']) / 2)
            self.current_perimeter['center_coord'] = self.current_perimeter['coords'][coord_center_index]
            self.all_perimeter_data.append(self.current_perimeter)

    def speed_metrics(self, x=None, y=None, window_distance=None, perimeter_distance=None, end_of_path=False):
        if end_of_path or window_distance > constants.HALF_TAG_DIAMETER:
            if self.current_window['seconds_motionless'] < 1:
                speed_group = 'moving'
            else:
                speed_group = 'motionless'

            for yx in self.current_window['yx_cell_coords']:
                self.cells_visited_speed_groups[speed_group] = increment_dict_key_value(self.cells_visited_speed_groups[speed_group], yx)
                self.cells_visited_speed_groups['all'] = increment_dict_key_value(self.cells_visited_speed_groups['all'], yx)

            coord_center_index = int(len(self.current_window['coords']) / 2)
            motionless_data = {'center_coord': self.current_window['coords'][coord_center_index], 'seconds_motionless': self.current_window['seconds_motionless']}
            self.all_motionless_data.append(motionless_data)
            self.current_perimeter['motionless_data'].append(motionless_data)

            self.current_window = {'yx_cell_coords': [], 'coords': [], 'start_coord': {'x': x, 'y': y}, 'seconds_motionless': 0}

        else:
             self.current_window['seconds_motionless'] += 1

        self.current_perimeter['seconds_present'] += 1
        if not end_of_path and perimeter_distance > constants.PERIMETER_RADIUS and self.current_perimeter['seconds_present'] > constants.MIN_NUM_SECONDS_SPENT_IN_AREA:

            coord_center_index = int(len(self.current_perimeter['coords']) / 2)
            self.current_perimeter['center_coord'] = self.current_perimeter['coords'][coord_center_index]

            self.all_perimeter_data.append(self.current_perimeter)
            self.current_perimeter = {'seconds_present': 0, 'yx_cell_coords': [], 'coords': [],
                                    'start_coord': {'x': x, 'y': y}, 'center_coord': {'x': None, 'y': None},
                                    'distances_per_second': [], 'motionless_data': []}
