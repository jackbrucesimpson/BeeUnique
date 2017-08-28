import sys
import os

from Processor import PathMetrics
from Processor.graphics import plot_path_bg, plot_histogram
from Processor.file_utils import create_dir_check_exists
from Processor.constants import *

def main():
    experiment_directory = sys.argv[1]

    plots_dir = create_dir_check_exists(experiment_directory, 'plots')
    path_bg_dir = create_dir_check_exists(plots_dir, 'path_bg')
    distances_per_second_window_dir = create_dir_check_exists(plots_dir, 'distances_per_second_window')
    seconds_spent_in_perimeter_dir = create_dir_check_exists(plots_dir, 'seconds_spent_in_perimeter')

    heatmaps_dir = create_dir_check_exists(plots_dir, 'heatmaps')
    pm = PathMetrics(experiment_directory)
    pm.generate_night_day_bgs()
    tag_class_night_day_metrics = pm.group_bee_data_into_nights_days(pm.tag_class_metrics_per_video)


    bee = tag_class_night_day_metrics[QUEEN_CLASS]
    for night_day in bee.keys():
        night_or_day_count = 0
        night_or_day_id = {'night': '_0_', 'day': '_1_'}
        for i in range(len(bee[night_day])):
            metrics = bee[night_day][i]
            bg_image = pm.night_day_bg_images[night_day][i]
            #.zfill(3)
            time_period_str = str(night_or_day_count) + night_or_day_id[night_day] + night_day

            file_name = os.path.join(path_bg_dir, time_period_str + '.png')
            plot_path_bg(metrics['x_paths'], metrics['y_paths'], bg_image, file_name)

            file_name = os.path.join(distances_per_second_window_dir, time_period_str + '.png')
            plot_histogram(metrics['distances_per_second_window'], 'Distance per second', file_name)

            file_name = os.path.join(seconds_spent_in_perimeter_dir, time_period_str + '.png')
            plot_histogram(metrics['seconds_spent_in_perimeter'], 'Seconds spent in perimeter', file_name)

            for speed_group in metrics['cells_visited_speed_groups'].keys():
                speed_group_heatmap_dir = create_dir_check_exists(heatmaps_dir, speed_group)
                file_name = os.path.join(speed_group_heatmap_dir, time_period_str)
                all_coords_spread, class_presence_spread = pm.calc_heatmaps(metrics['cells_visited_speed_groups'][speed_group], bg_image, file_name)

            night_or_day_count += 1

if __name__ == "__main__":
    main()
