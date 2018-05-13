from Processor.Utils.imageutils import calc_distance, gen_gap_coords, increment_dict_key_value
from Processor.Utils import constants

self.current_window = {'yx_cell_coords': [], 'start_coord': {'x': None, 'y': None}, 'seconds_motionless': 0}
        self.current_perimeter = {'seconds_present': 0, 'start_coord': {'x': None, 'y': None}, 'center_coord': {'x': None, 'y': None},
                                'coords': [], 'distances_per_second': [], 'reappearance_data': []}

        self.all_distances_per_second_window = []
        self.all_reappearance_data = []
        self.all_activity_grouped_by_type = []

        self.all_perimeter_data = []
        self.cells_visited_speed_groups = {'all': {}, 'moving': {}, 'motionless': {}}



    def calc_path_metrics(self):
        reappearance_data = {'same_loc_disappeared': False, 'num_seconds': 0, 'x': None, 'y': None}

        for path_index in range(len(self.paths)):
            if self.paths[path_index]['is_gap']:
                absent_path = self.paths[path_index]
                num_seconds = int(absent_path['num_frames'] / float(constants.FPS))
                same_loc_disappeared = absent_path['prev_next_path_same_loc_disappeared']
                self.all_activity_grouped_by_type.append({'activity': 'absent', 'num_seconds': num_seconds})

                if same_loc_disappeared:
                    reappearance_data = {'same_loc_disappeared': same_loc_disappeared, 'num_seconds': num_seconds, 'x': absent_path['x'], 'y': absent_path['y']}
                    self.current_perimeter['reappearance_data'].append(reappearance_data)
                    self.current_perimeter['seconds_present'] += num_seconds
                    self.all_reappearance_data.append(reappearance_data)
                continue

            x_path = self.paths[path_index]['x_path']
            y_path = self.paths[path_index]['y_path']
            if self.current_perimeter['start_coord']['x'] is None:
                self.current_perimeter['start_coord'] = {'x': x_path[0], 'y': y_path[0]}

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

                    if perimeter_distance > constants.PERIMETER_RADIUS:
                        self.perimeter_metrics()
                        self.current_perimeter['start_coord'] = {'x': x, 'y': y}
                    else:
                        self.current_perimeter['seconds_present'] += 1

                    self.all_distances_per_second_window.append(window_distance)
                    self.current_perimeter['distances_per_second'].append(window_distance)

                    if window_distance > constants.HALF_TAG_DIAMETER:
                        self.window_metrics()
                    else:
                        self.current_window['seconds_motionless'] += 1

                    frame_counter = 0

                self.current_window['yx_cell_coords'].append(yx_cell_coord)
                self.current_perimeter['coords'].append({'x': x, 'y': y})

            if self.current_window['seconds_motionless'] > 0:
                self.window_metrics()

        self.perimeter_metrics()

    def window_metrics(self):
        if self.current_window['seconds_motionless'] < 1:
            speed_group = 'moving'
        else:
            speed_group = 'motionless'

        for yx in self.current_window['yx_cell_coords']:
            self.cells_visited_speed_groups[speed_group] = increment_dict_key_value(self.cells_visited_speed_groups[speed_group], yx)
            self.cells_visited_speed_groups['all'] = increment_dict_key_value(self.cells_visited_speed_groups['all'], yx)

        activity_data = {'activity': speed_group, 'num_seconds': self.current_window['seconds_motionless']}
        self.all_activity_grouped_by_type.append(activity_data)

        self.current_window['yx_cell_coords'] = []
        self.current_window['seconds_motionless'] = 0

    def perimeter_metrics(self):
        if self.current_perimeter['seconds_present'] > constants.MIN_NUM_SECONDS_SPENT_IN_AREA:
            coord_center_index = int(len(self.current_perimeter['coords']) / 2)
            self.current_perimeter['center_coord'] = self.current_perimeter['coords'][coord_center_index]
            self.all_perimeter_data.append(self.current_perimeter)

        self.current_perimeter = {'seconds_present': 0, 'start_coord': {'x': None, 'y': None}, 'center_coord': {'x': None, 'y': None},
                                'coords': [], 'distances_per_second': [], 'reappearance_data': []}


    from Processor.Utils.imageutils import combine_night_day_bg
