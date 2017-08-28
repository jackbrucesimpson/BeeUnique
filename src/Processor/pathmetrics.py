import os
import networkx as nx
from scipy import ndimage
import numpy as np

from file_utils import read_all_processed_paths_files
from image_utils import combine_night_day_bg, calc_distance, calc_distance, increment_dict_key_value
from splitdatatime import SplitDataTime
from graphics import plot_heatmaps, plot_heatmaps_bg_image

from constants import *

class PathMetrics:
    def __init__(self, experiment_directory):
        self.experiment_directory = experiment_directory
        self.video_date_time_list = []
        processed_paths_dir = os.path.join(self.experiment_directory, 'processed')
        video_dt_bees_json = read_all_processed_paths_files(processed_paths_dir)
        tag_class_paths_grouped_by_video = self.group_all_data_by_tag_class(video_dt_bees_json)
        self.tag_class_metrics_per_video = self.calc_video_path_metrics(tag_class_paths_grouped_by_video)

    def group_all_data_by_tag_class(self, video_dt_bees_json):
        tag_class_paths_grouped_by_video = {tag_class: [] for tag_class in tag_class_names.keys()}
        for dt_bee_json in video_dt_bees_json:
            self.video_date_time_list.append(dt_bee_json['date_time'])
            tag_class_each_video = {tag_class: [] for tag_class in tag_class_names.keys()}
            for bee_json in dt_bee_json['bees_json']:
                tag_class = bee_json['tag_class']
                if tag_class != QUEEN_CLASS:######################################################################
                    continue######################################################################################
                for path_index in range(len(bee_json['start_frame_nums'])):
                    start_frame_num = bee_json['start_frame_nums'][path_index]
                    x_path = bee_json['x_paths'][path_index]
                    y_path = bee_json['y_paths'][path_index]
                    tag_class_each_video[tag_class].append({'start_frame_num': start_frame_num, 'x_path': x_path, 'y_path': y_path})

            for tag_class in tag_class_each_video.keys():
                tag_class_paths_grouped_by_video[tag_class].append(sorted(tag_class_each_video[tag_class], key=lambda k: k['start_frame_num']))

        return tag_class_paths_grouped_by_video

    def calc_video_path_metrics(self, tag_class_paths_grouped_by_video):
        tag_class_metrics_per_video = {tag_class: [] for tag_class in tag_class_names.keys()}
        for tag_class in tag_class_paths_grouped_by_video.keys():
            for video_paths in tag_class_paths_grouped_by_video[tag_class]:
                cells_visited_speed_groups = {'all': {}, 'moving': {}, 'motionless_short': {}, 'motionless_long': {}}
                distances_per_second_window = []
                seconds_spent_in_perimeter = []
                consecutive_seconds_motionless = []
                long_stay_perimeter_coord_data = []
                x_paths = []
                y_paths = []
                for path in video_paths:
                    start_frame_num = path['start_frame_num']
                    x_path = path['x_path']
                    y_path = path['y_path']
                    x_paths.append(x_path)
                    y_paths.append(y_path)

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
                        x_cell, y_cell = int(x / X_BINS), int(y / Y_BINS)
                        yx_cell_coord = (y_cell, x_cell)
                        current_perimeter_yx_cell_coords.append(yx_cell_coord)
                        current_window_yx_cell_coords.append(yx_cell_coord)

                        frame_counter += 1
                        if frame_counter == 1:
                            start_window_coord = (x, y)
                            if perimeter_coord is None:
                                perimeter_coord = (x, y)
                        if frame_counter % FPS == 0:
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
                        for yx in current_window_yx_cell_coords:
                            cells_visited_speed_groups[speed_group] = increment_dict_key_value(cells_visited_speed_groups[speed_group], yx)
                            cells_visited_speed_groups['all'] = increment_dict_key_value(cells_visited_speed_groups['all'], yx)

                        consecutive_seconds_motionless.append(seconds_motionless_counter)


                    if perimeter_counter > 30:
                        long_stay_perimeter_coord_data.append({'x': perimeter_coord[0], 'y': perimeter_coord[1], 'seconds_spent_in_perimeter': perimeter_counter, 'current_perimeter_window_distances': current_perimeter_window_distances, 'current_perimeter_yx_cell_coords': current_perimeter_yx_cell_coords})

                tag_class_metrics_per_video[tag_class].append({'x_paths': x_paths, 'y_paths': y_paths, 'distances_per_second_window': distances_per_second_window, 'cells_visited_speed_groups': cells_visited_speed_groups, 'seconds_spent_in_perimeter': seconds_spent_in_perimeter, 'consecutive_seconds_motionless': consecutive_seconds_motionless})
        return tag_class_metrics_per_video

    def group_bee_data_into_nights_days(self, tag_class_metrics_per_video):
        tag_class_night_day_metrics = {}
        for tag_class in tag_class_metrics_per_video.keys():
            sdt_paths = SplitDataTime()
            for i, video_metrics in enumerate(tag_class_metrics_per_video[tag_class]):
                date_time = self.video_date_time_list[i]
                sdt_paths.add_date_time_data(date_time, video_metrics)
            night_day_grouped_video_metrics = sdt_paths.sort_data_into_time_period()
            merged_night_day_grouped_video_metrics = self.merge_grouped_night_day_video_metrics(night_day_grouped_video_metrics)
            tag_class_night_day_metrics[tag_class] = merged_night_day_grouped_video_metrics

        return tag_class_night_day_metrics

    def merge_grouped_night_day_video_metrics(self, night_day_grouped_video_metrics):
        merged_night_day_grouped_video_metrics = {'night': [], 'day': []}
        for night_day in night_day_grouped_video_metrics.keys():
            for night_day_time_period_group in night_day_grouped_video_metrics[night_day]:
                merged_video_metrics = {'x_paths': [], 'y_paths': [], 'distances_per_second_window': [], 'cells_visited_speed_groups': {'all': {}, 'moving': {}, 'motionless_short': {}, 'motionless_long': {}}, 'seconds_spent_in_perimeter': [], 'consecutive_seconds_motionless': []}
                for video_metrics in night_day_time_period_group:
                    merged_video_metrics['x_paths'].extend(video_metrics['x_paths'])
                    merged_video_metrics['y_paths'].extend(video_metrics['y_paths'])
                    merged_video_metrics['consecutive_seconds_motionless'].extend(video_metrics['consecutive_seconds_motionless'])
                    merged_video_metrics['seconds_spent_in_perimeter'].extend(video_metrics['seconds_spent_in_perimeter'])
                    merged_video_metrics['distances_per_second_window'].extend(video_metrics['distances_per_second_window'])
                    for speed_group in video_metrics['cells_visited_speed_groups'].keys():
                        for yx_coord in video_metrics['cells_visited_speed_groups'][speed_group].keys():
                            merged_video_metrics['cells_visited_speed_groups'][speed_group] = increment_dict_key_value(merged_video_metrics['cells_visited_speed_groups'][speed_group], yx_coord, video_metrics['cells_visited_speed_groups'][speed_group][yx_coord])
                merged_night_day_grouped_video_metrics[night_day].append(merged_video_metrics)
        return merged_night_day_grouped_video_metrics

    def generate_night_day_bgs(self):
        image_directory_path = os.path.join(self.experiment_directory, 'background')
        self.night_day_bg_images = combine_night_day_bg(image_directory_path)

    def calc_heatmaps(self, cells_visited, bg_image, file_name):
        all_coords_heatmap = np.zeros((NUM_Y_CELLS, NUM_X_CELLS))
        tag_class_presence_heatmap = np.zeros((NUM_Y_CELLS, NUM_X_CELLS))
        for yx_coord in cells_visited.keys():
            if yx_coord[1] == NUM_X_CELLS:
                all_coords_heatmap[(yx_coord[0], NUM_X_CELLS - 1)] += cells_visited[yx_coord]
                tag_class_presence_heatmap[(yx_coord[0], NUM_X_CELLS - 1)] += 1
            else:
                all_coords_heatmap[yx_coord] += cells_visited[yx_coord]
                tag_class_presence_heatmap[yx_coord] += 1

        norm_all_coords_heatmap = all_coords_heatmap / all_coords_heatmap.sum()
        norm_tag_class_presence_heatmap = tag_class_presence_heatmap / tag_class_presence_heatmap.sum()

        all_coords_spread = self.calc_spread(norm_all_coords_heatmap)
        class_presence_spread = self.calc_spread(norm_tag_class_presence_heatmap)

        plot_heatmaps_bg_image(norm_all_coords_heatmap, bg_image, 100, 'All Coords Spread: ' + str(all_coords_spread), file_name +'_all_coords.png')
        plot_heatmaps_bg_image(norm_tag_class_presence_heatmap, bg_image, 100, 'Presence Spread: ' + str(class_presence_spread), file_name +'_presence.png')

        return (all_coords_spread, class_presence_spread)

    def calc_spread(self, norm_heatmap):
        centre = ndimage.measurements.center_of_mass(norm_heatmap)
        spread = 0
        for y_c in range(0, norm_heatmap.shape[0]):
            for x_c in range(0, norm_heatmap.shape[1]):
                spread += calc_distance(x_c, y_c, centre[1], centre[0]) * norm_heatmap[y_c, x_c]

        return spread

    def calc_speeds(self):
        pass

    def calc_idle_percentage(self):
        pass

    def calc_networks(self):
        pass
