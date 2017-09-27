import os
import shelve

import networkx as nx
from scipy import ndimage
import numpy as np

from videometrics import VideoMetrics
from Processor.Utils.fileutils import get_processed_paths_video_dt_json_filename, read_json, create_dir_check_exists
from Processor.Utils.imageutils import combine_night_day_bg, calc_distance, sort_data_into_time_period
from Processor.Utils.graphics import plot_heatmaps_bg_image
from Processor.Utils import constants

class PathMetrics(object):
    def __init__(self, experiment_directory):
        self.experiment_directory = experiment_directory
        db_dir = create_dir_check_exists(experiment_directory, 'db')
        self.video_db_file = os.path.join(db_dir, 'video_metrics.db')
        self.circadian_db_file = os.path.join(db_dir, 'circadian_metrics.db')

        self.video_date_time_list = []
        processed_paths_dir = os.path.join(experiment_directory, 'processed')
        video_dt_json_filename = get_processed_paths_video_dt_json_filename(processed_paths_dir)
        self.group_all_data_by_tag_class(video_dt_json_filename)

    def group_all_data_by_tag_class(self, video_dt_json_filename):
        #tag_class_metrics_grouped_by_video = {tag_class: [] for tag_class in constants.TAG_CLASS_NAMES.keys() if tag_class != constants.UNKNOWN_CLASS}
        tag_class_metrics_grouped_by_video = {constants.QUEEN_CLASS: []}

        for dt_bee_json_filename in video_dt_json_filename:
            print('Processed', dt_bee_json_filename['date_time'])
            self.video_date_time_list.append(dt_bee_json_filename['date_time'])
            tag_class_each_video = {tag_class: [] for tag_class in tag_class_metrics_grouped_by_video}

            bees_json = read_json(dt_bee_json_filename['bees_json_filename'])
            for bee_json in bees_json:
                tag_class = bee_json['tag_class']
                if tag_class != constants.QUEEN_CLASS:
                    continue
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
                vm = VideoMetrics(tag_class)
                vm.add_paths_data(sorted_tag_class_paths_in_video)
                tag_class_metrics_grouped_by_video[tag_class].append(vm)


        video_db = shelve.open(self.video_db_file)
        for tag_class in tag_class_metrics_grouped_by_video.keys():
            video_db[str(tag_class)] = tag_class_metrics_grouped_by_video[tag_class]
        video_db.close()

    def group_bee_data_into_nights_days(self):
        video_db = shelve.open(self.video_db_file)
        circadian_db = shelve.open(self.circadian_db_file)

        for tag_class in video_db.keys():
            video_dt_data = []
            bee_data_grouped_by_video = video_db[str(tag_class)]
            for i, video_metrics in enumerate(bee_data_grouped_by_video):
                date_time = self.video_date_time_list[i]
                video_dt_data.append({'date_time': date_time, 'data': video_metrics})
            night_day_grouped_video_metrics = sort_data_into_time_period(video_dt_data)
            circadian_db[str(tag_class)] = self.merge_grouped_night_day_video_metrics(tag_class, night_day_grouped_video_metrics)

        video_db.close()
        circadian_db.close()

    def merge_grouped_night_day_video_metrics(self, tag_class, night_day_grouped_video_metrics):
        print(tag_class)
        merged_night_day_grouped_video_metrics = {'night': [], 'day': []}
        for night_day in night_day_grouped_video_metrics.keys():
            for night_day_time_period_group in night_day_grouped_video_metrics[night_day]:
                vm_merged = VideoMetrics(tag_class)
                for video_metrics in night_day_time_period_group:
                    vm_merged.merge_video_metrics(video_metrics)
                vm_merged.calc_metrics()
                merged_night_day_grouped_video_metrics[night_day].append(vm_merged)

        return merged_night_day_grouped_video_metrics

    def generate_night_day_bgs(self):
        image_directory_path = os.path.join(self.experiment_directory, 'background')
        self.night_day_bg_images = combine_night_day_bg(image_directory_path)

    def get_bee_circadian_data_by_tag_class(self, tag_class):
        circadian_db = shelve.open(self.circadian_db_file)
        bee_data = circadian_db[str(tag_class)]
        circadian_db.close()

        return bee_data

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
