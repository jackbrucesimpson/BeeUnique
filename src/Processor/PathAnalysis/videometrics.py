from Processor.Utils.imageutils import calc_distance, gen_gap_coords, increment_dict_key_value
from Processor.Utils import constants

class VideoMetrics:

    def __init__(self):
        self.paths = []

        self.current_window = {'yx_cell_coords': [], 'coords': [], 'start_coord': {'x': None, 'y': None}, 'seconds_motionless': 0}
        self.current_perimeter = {'seconds_present': 0, 'yx_cell_coords': [], 'coords': [],
                                'start_coord': {'x': None, 'y': None}, 'center_coord': {'x': None, 'y': None},
                                'distances_per_second': [], 'motionless_data': []}

        self.all_distances_per_second_window = []
        self.all_motionless_data = []

        self.all_perimeter_data = []
        self.cells_visited_speed_groups = {'all': {}, 'moving': {}, 'motionless': {}}

    def merge_video_metrics(self, vm):
        #print('num merged paths', len(self.paths))

        # entire video gap
        if len(vm.paths) == 1:
            if len(self.paths) == 0:
                self.paths.append(vm.paths[0])
            else:
                self.paths[-1]['num_frames'] += vm.paths[0]['num_frames']
            return None
        # check if no paths or only gap paths stored so far
        # if so, delete first gap if bee was seen from the beginning
        if len(self.paths) < 2:
            if vm.paths[0]['num_frames'] < 1:
                del vm.paths[0]
            self.paths.extend(vm.paths)
        else:
            # see amount of time in last gap prev vid and first gap current video
            # decide whether to delete last last or first gap or merge
            num_frames_path_gap = self.paths[-1]['num_frames'] + vm.paths[0]['num_frames']
            prev_video_last_x = self.paths[-2]['x_path'][-1]
            prev_video_last_y = self.paths[-2]['y_path'][-1]
            current_video_first_x = vm.paths[1]['x_path'][0]
            current_video_first_y = vm.paths[1]['y_path'][0]
            gap_data = self.calc_path_gap(num_frames_path_gap, prev_video_last_x, prev_video_last_y, current_video_first_x, current_video_first_y)

            del self.paths[-1]
            del vm.paths[0]

            if gap_data['prev_next_path_same_loc_disappeared']:
                generated_coord_gaps = gen_gap_coords(current_video_first_x, current_video_first_y, prev_video_last_x, prev_video_last_y, num_frames_path_gap)
                self.paths[-1]['x_path'].extend(generated_coord_gaps['x'])
                self.paths[-1]['y_path'].extend(generated_coord_gaps['y'])
                self.paths[-1]['x_path'].extend(vm.paths[0]['x_path'])
                self.paths[-1]['y_path'].extend(vm.paths[0]['y_path'])
                self.paths[-1]['num_frames'] = len(self.paths[-1]['y_path'])
            else:
                self.paths.append(gap_data)

            self.paths.extend(vm.paths)

    def add_paths_data(self, paths_data):
        num_paths = len(paths_data)
        if num_paths == 0:
            entire_video_gap_data = {'is_gap': True, 'prev_next_path_same_loc_disappeared': False, 'num_frames': constants.NUM_FRAMES_IN_VIDEO}
            self.paths.append(entire_video_gap_data)
            return None

        start_frame_num = paths_data[0]['start_frame_num']
        x_path = paths_data[0]['x_path']
        y_path = paths_data[0]['y_path']
        path_length = len(x_path)
        path_end_frame_num = start_frame_num + path_length

        start_video_gap_data = {'is_gap': True, 'prev_next_path_same_loc_disappeared': False, 'num_frames': start_frame_num - 1}
        self.paths.append(start_video_gap_data)

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

            self.paths.append({'is_gap': False, 'x_path': x_path, 'y_path': y_path, 'num_frames': path_length})
            if ii < num_paths:
                num_frames_path_gap = paths_data[ii]['start_frame_num'] - path_end_frame_num
                gap_data = self.calc_path_gap(num_frames_path_gap, x_path[-1], y_path[-1], paths_data[ii]['x_path'][0], paths_data[ii]['y_path'][0])
                self.paths.append(gap_data)

            i = ii

        end_video_gap_data = {'is_gap': True, 'prev_next_path_same_loc_disappeared': False, 'num_frames': constants.NUM_FRAMES_IN_VIDEO - path_end_frame_num - 1}
        self.paths.append(end_video_gap_data)

    def calc_path_gap(self, num_frames_path_gap, prev_x, prev_y, new_x, new_y):
        distance = calc_distance(prev_x, prev_y, new_x, new_y)
        prev_next_path_same_loc_disappeared = True
        if distance > constants.DOUBLE_TAG_DIAMETER:
            prev_next_path_same_loc_disappeared = False

        gap_data = {'is_gap': True, 'prev_next_path_same_loc_disappeared': prev_next_path_same_loc_disappeared, 'num_frames': num_frames_path_gap}
        return gap_data

    def calc_metrics(self):

        #if len(self.paths) < 2:
            #return None
        #else:
        if self.paths[-1]['num_frames'] < 1:
            del self.paths[-1]

        for path_index in range(len(self.paths)):
            if not self.paths[path_index]['is_gap']:
                self.current_perimeter['start_coord'] = {'x': self.paths[path_index]['x_path'][0], 'y': self.paths[path_index]['y_path'][0]}

        for path_index in range(len(self.paths)):
            if self.paths[path_index]['is_gap']:
                #double check later
                motionless_data = {'seconds_motionless': -int(self.paths[path_index]['num_frames'] / 20.0)}
                self.all_motionless_data.append(motionless_data)
                continue

            x_path = self.paths[path_index]['x_path']
            y_path = self.paths[path_index]['y_path']

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
