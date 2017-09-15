import sys
import os

from Processor.PathAnalysis.pathmetrics import PathMetrics
from Processor.Utils.graphics import plot_path_bg, plot_histogram, plot_line, plot_barplot
from Processor.Utils.fileutils import create_dir_check_exists
from Processor.Utils import constants

import math

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

    seconds_motionless = []
    dividing_lines = []

    bee = pm.tag_class_night_day_metrics[constants.QUEEN_CLASS]

    night_or_day_count = 1

    for i in range(len(bee['night'])):
        print(i)
        night_metrics = bee['night'][i]
        day_metrics = bee['day'][i]

        for motionless_data in night_metrics.all_motionless_data:
            seconds_motionless.append(motionless_data['seconds_motionless'])

        dividing_lines.append(sum([abs(s) for s in seconds_motionless]))
        #### change

        for motionless_data in day_metrics.all_motionless_data:
            seconds_motionless.append(motionless_data['seconds_motionless'])

        if i == 1:
            break

    time_period_str = "all_night_day"
    file_name = os.path.join(consecutive_seconds_motionless_path_dir, time_period_str + '.png')
    plot_barplot(seconds_motionless, range(len(seconds_motionless)), file_name, 'Consecutive seconds motionless', 'Seconds in time period', 'Seconds motionless', 0, constants.SECONDS_IN_45_MINS, dividing_lines)





if __name__ == "__main__":
    main()
