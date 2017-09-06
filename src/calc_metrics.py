import sys
import os

from Processor.PathAnalysis.pathmetrics import PathMetrics
from Processor.Utils.graphics import plot_path_bg, plot_histogram, plot_line
from Processor.Utils.fileutils import create_dir_check_exists
from Processor.Utils import constants

def main():
    experiment_directory = sys.argv[1]

    plots_dir = create_dir_check_exists(experiment_directory, 'plots')
    path_bg_dir = create_dir_check_exists(plots_dir, 'path_bg')
    distances_per_second_window_dir = create_dir_check_exists(plots_dir, 'distances_per_second_window')
    seconds_spent_in_perimeter_dir = create_dir_check_exists(plots_dir, 'seconds_spent_in_perimeter')
    consecutive_seconds_motionless_dir = create_dir_check_exists(plots_dir, 'consecutive_seconds_motionless')
    consecutive_seconds_motionless_path_dir = create_dir_check_exists(plots_dir, 'consecutive_seconds_motionless_path')

    heatmaps_dir = create_dir_check_exists(plots_dir, 'heatmaps')
    pm = PathMetrics(experiment_directory)
    pm.group_bee_data_into_nights_days()
    pm.generate_night_day_bgs()

    bee = pm.tag_class_night_day_metrics[constants.QUEEN_CLASS]
    for night_day in bee.keys():
        print(night_day)
        night_or_day_count = 0
        night_or_day_id = {'night': '_0_', 'day': '_1_'}
        for i in range(len(bee[night_day])):
            print(i)
            metrics = bee[night_day][i]
            bg_image = pm.night_day_bg_images[night_day][i]

            time_period_str = str(night_or_day_count) + night_or_day_id[night_day] + night_day

            file_name = os.path.join(path_bg_dir, time_period_str + '.png')
            plot_path_bg(metrics.x_paths, metrics.y_paths, bg_image, file_name)

            file_name = os.path.join(distances_per_second_window_dir, time_period_str + '.png')
            plot_histogram(metrics.all_distances_per_second_window, 'Distance per second', file_name)

            #file_name = os.path.join(seconds_spent_in_perimeter_dir, time_period_str + '.png')
            #plot_histogram(metrics['seconds_spent_in_perimeter'], 'Seconds spent in perimeter', file_name)

            seconds_motionless = []
            for motionless_data in metrics.all_motionless_data:
                seconds_motionless.append(motionless_data['seconds_motionless'])

            file_name = os.path.join(consecutive_seconds_motionless_dir, time_period_str + '.png')
            plot_histogram(seconds_motionless, 'Consecutive seconds motionless', file_name)

            file_name = os.path.join(consecutive_seconds_motionless_path_dir, time_period_str + '.png')
            plot_line(range(len(seconds_motionless)), seconds_motionless, 'Consecutive seconds motionless', 'Seconds in paths', 'Seconds motionless', 0, constants.SECONDS_IN_HOUR, file_name)

            for speed_group in metrics.cells_visited_speed_groups.keys():
                speed_group_heatmap_dir = create_dir_check_exists(heatmaps_dir, speed_group)
                file_name = os.path.join(speed_group_heatmap_dir, time_period_str)
                all_coords_spread, class_presence_spread = pm.calc_heatmaps(metrics.cells_visited_speed_groups[speed_group], bg_image, file_name)


            night_or_day_count += 1

if __name__ == "__main__":
    main()
