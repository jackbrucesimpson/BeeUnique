import os

from file_utils import read_all_processed_paths_files
from image_utils import combine_night_day_bg
from splitdatatime import SplitDataTime

from constants import *

class PathMetrics:
    def __init__(self, experiment_directory):
        self.experiment_directory = experiment_directory
        self.night_day_tag_paths = None
        self.night_day_bg_images = None

        processed_paths_dir = os.path.join(self.experiment_directory, 'processed')
        video_dt_paths = read_all_processed_paths_files(processed_paths_dir)
        self.night_day_tag_paths = self.group_paths_night_day_periods(video_dt_paths)

    def generate_night_day_bgs(self):
        image_directory_path = os.path.join(self.experiment_directory, 'background')
        self.night_day_bg_images = combine_night_day_bg(image_directory_path)

    def group_paths_night_day_periods(self, video_dt_paths):
        sdt_paths = SplitDataTime()
        for dt_path in video_dt_paths:
            date_time = dt_path['date_time']
            tag_class_paths_time_period = {k: [] for k in tag_class_names.keys()}
            for bee in dt_path['paths']:
                for path_index in range(len(bee['x_paths'])):
                    tag_class_paths_time_period[bee['tag_class']].append({'x_path': bee['x_paths'][path_index], 'y_path': bee['y_paths'][path_index]})
            sdt_paths.add_date_time_data(date_time, tag_class_paths_time_period)

        night_day_paths_hourly_grouped = sdt_paths.sort_data_into_time_period()
        night_day_tag_paths = self.merge_tag_class_paths_into_night_day_groups(night_day_paths_hourly_grouped)

        return night_day_tag_paths

    def merge_tag_class_paths_into_night_day_groups(self, night_day_path_lists):
        night_day_tag_paths = {'day': [], 'night': []}
        for night_day in night_day_path_lists.keys():
            #print(night_day)
            night_or_day_grouped_hours = night_day_path_lists[night_day]
            #print(len(night_or_day_grouped_hours))
            for list_night_day_period_hours in night_or_day_grouped_hours:
                merged_tag_class_paths = {k: [] for k in tag_class_names.keys()}
                #print(len(list_night_day_period_hours))
                for tag_class_paths in list_night_day_period_hours:
                    for tag_class in tag_class_paths.keys():
                        merged_tag_class_paths[tag_class].extend(tag_class_paths[tag_class])
                night_day_tag_paths[night_day].append(merged_tag_class_paths)

        return night_day_tag_paths

    #def 
