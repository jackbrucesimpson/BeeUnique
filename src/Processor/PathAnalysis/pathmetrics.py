import os

import networkx as nx
from scipy import ndimage
import numpy as np

from Processor.Utils.fileutils import read_all_processed_paths_files
from Processor.Utils.imageutils import combine_night_day_bg, calc_distance, calc_distance, increment_dict_key_value
from Processor.Utils.splitdatatime import SplitDataTime
from Processor.Utils.graphics import plot_heatmaps, plot_heatmaps_bg_image
from Processor.Utils import constants

class PathMetrics:
    def __init__(self, experiment_directory):
        self.experiment_directory = experiment_directory
        self.video_date_time_list = []
        processed_paths_dir = os.path.join(self.experiment_directory, 'processed')
        video_dt_bees_json = read_all_processed_paths_files(processed_paths_dir)
        tag_class_metrics_grouped_by_video = self.group_all_data_by_tag_class(video_dt_bees_json)
        self.tag_class_metrics_per_video = self.calc_video_path_metrics(tag_class_metrics_grouped_by_video)

    def group_all_data_by_tag_class(self, video_dt_bees_json):
        tag_class_metrics_grouped_by_video = {tag_class: [] for tag_class in constants.TAG_CLASS_NAMES.keys()}
        for dt_bee_json in video_dt_bees_json:
            self.video_date_time_list.append(dt_bee_json['date_time'])
            tag_class_each_video = {tag_class: [] for tag_class in constants.TAG_CLASS_NAMES.keys()}
            for bee_json in dt_bee_json['bees_json']:
                tag_class = bee_json['tag_class']
                if tag_class != constants.QUEEN_CLASS:######################################################################
                    continue######################################################################################
                for path_index in range(len(bee_json['start_frame_nums'])):
                    start_frame_num = bee_json['start_frame_nums'][path_index]
                    x_path = bee_json['x_paths'][path_index]
                    y_path = bee_json['y_paths'][path_index]
                    tag_class_each_video[tag_class].append({'start_frame_num': start_frame_num, 'x_path': x_path, 'y_path': y_path})

            for tag_class in tag_class_each_video.keys():
                tag_class_metrics_grouped_by_video[tag_class].append(sorted(tag_class_each_video[tag_class], key=lambda k: k['start_frame_num']))

        return tag_class_metrics_grouped_by_video


    def group_all_data_by_tag_class(self, video_dt_bees_json):
        tag_class_metrics_grouped_by_video = {tag_class: [] for tag_class in constants.TAG_CLASS_NAMES.keys()}
        for dt_bee_json in video_dt_bees_json:
            self.video_date_time_list.append(dt_bee_json['date_time'])
            tag_class_each_video = {tag_class: [] for tag_class in constants.TAG_CLASS_NAMES.keys()}
            for bee_json in dt_bee_json['bees_json']:
                tag_class = bee_json['tag_class']
                if tag_class != constants.QUEEN_CLASS:######################################################################
                    continue######################################################################################
                for path_index in range(len(bee_json['start_frame_nums'])):
                    start_frame_num = bee_json['start_frame_nums'][path_index]
                    x_path = bee_json['x_paths'][path_index]
                    y_path = bee_json['y_paths'][path_index]
                    tag_class_each_video[tag_class].append({'start_frame_num': start_frame_num, 'x_path': x_path, 'y_path': y_path})

            for tag_class in tag_class_each_video.keys():
                sorted_tag_class_paths_in_video = sorted(tag_class_each_video[tag_class], key=lambda k: k['start_frame_num'])
                vm = VideoMetrics()
                vm.add_paths_data(sorted_tag_class_paths_in_video)
                tag_class_metrics_grouped_by_video[tag_class].append(vm)

        return tag_class_metrics_grouped_by_video

    def calc_video_path_metrics(self, tag_class_metrics_grouped_by_video):
        tag_class_metrics_per_video = {tag_class: [] for tag_class in constants.TAG_CLASS_NAMES.keys()}
        for tag_class in tag_class_metrics_grouped_by_video.keys():
            for each_video_paths in tag_class_metrics_grouped_by_video[tag_class]:
                vm = VideoMetrics() #### check
                for path in each_video_paths:
                    start_frame_num = path['start_frame_num']
                    x_path = path['x_path']
                    y_path = path['y_path']

                    vm.append_path(start_frame_num, x_path, y_path)



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
        all_coords_heatmap = np.zeros((constants.NUM_Y_CELLS, constants.NUM_X_CELLS))
        tag_class_presence_heatmap = np.zeros((constants.NUM_Y_CELLS, constants.NUM_X_CELLS))
        for yx_coord in cells_visited.keys():
            if yx_coord[1] == constants.NUM_X_CELLS:
                all_coords_heatmap[(yx_coord[0], constants.NUM_X_CELLS - 1)] += cells_visited[yx_coord]
                tag_class_presence_heatmap[(yx_coord[0], constants.NUM_X_CELLS - 1)] += 1
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
