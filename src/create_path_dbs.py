import sys
import os

import shelve

from Processor.Utils.dbpaths import group_all_data_by_tag_class, merge_grouped_night_day_video_metrics
from Processor.Utils.fileutils import get_processed_paths_video_dt_json_filename, create_dir_check_exists
from Processor.Utils.imageutils import sort_data_into_time_period

def main():
    experiment_directory = sys.argv[1]

    experiment_directory = experiment_directory
    db_dir = create_dir_check_exists(experiment_directory, 'db')
    circadian_db_file = os.path.join(db_dir, 'circadian_metrics.db')

    processed_paths_dir = os.path.join(experiment_directory, 'processed')
    video_dt_json_filename = get_processed_paths_video_dt_json_filename(processed_paths_dir)

    tag_class_metrics_grouped_by_video, video_date_time_list = group_all_data_by_tag_class(video_dt_json_filename)

    circadian_db = shelve.open(circadian_db_file)

    for tag_class in tag_class_metrics_grouped_by_video.keys():
        video_dt_data = []
        bee_data_grouped_by_video = tag_class_metrics_grouped_by_video[tag_class]
        for i, video_metrics in enumerate(bee_data_grouped_by_video):
            date_time = video_date_time_list[i]
            video_dt_data.append({'date_time': date_time, 'data': video_metrics})
        night_day_grouped_video_metrics = sort_data_into_time_period(video_dt_data)
        circadian_db[str(tag_class)] = merge_grouped_night_day_video_metrics(tag_class, night_day_grouped_video_metrics)

    circadian_db.close()

if __name__ == "__main__":
    main()
