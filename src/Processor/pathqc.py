import os

import matplotlib
matplotlib.use("Agg")
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from Processor.image_utils import increment_dict_key_value, get_json_file_output_tag_images
from file_utils import create_dir_check_exists
from constants import *

class PathQC:
    def __init__(self, video_datetime, experiment_directory):
        self.video_datetime = video_datetime
        self.experiment_directory = experiment_directory
        self.class_num_frames_tracked_dict = {}
        self.bee_ids_with_long_unknowns = []

    def get_class_num_frames_tracked(self, bee_tags_in_path):
        path_class_frames_tracked_list = []
        for bee in bee_tags_in_path:
            tag_class = bee['tag_class']
            num_frames_tracked = 0
            for path_index in range(len(bee['x_paths'])):
                num_frames_tracked += len(bee['x_paths'][path_index])
            path_class_frames_tracked_list.append({'tag_class': tag_class, 'num_frames_tracked': num_frames_tracked})

            return path_class_frames_tracked_list

    def find_unknown_and_path_lens_in_bee_classes_split_from_path(self, original_path_bee_id, bee_paths_list_broken_up_by_class):
        bee_path_classes_num_frames_tracked = self.get_class_num_frames_tracked(bee_paths_list_broken_up_by_class)

        for bee_path_class in bee_path_classes_num_frames_tracked:
            self.class_num_frames_tracked_dict = increment_dict_key_value(self.class_num_frames_tracked_dict, \
                                            bee_path_class['tag_class'], bee_path_class['num_frames_tracked'])

            if bee_path_class['tag_class'] == UNKNOWN_CLASS:
                if bee_path_class['num_frames_tracked'] > NUM_UNKNOWNS_IN_PATH_THRESHOLD:
                    self.bee_ids_with_long_unknowns.append(original_path_bee_id)

    def output_tag_images_unknown_paths(self, reduce_images):
        self.bee_ids_with_long_unknowns = set(self.bee_ids_with_long_unknowns)
        raw_json_filepath = os.path.join(self.experiment_directory, 'raw', self.video_datetime + '.json')
        get_json_file_output_tag_images(raw_json_filepath, self.experiment_directory, self.video_datetime, reduce_images, self.bee_ids_with_long_unknowns)

    def gen_qc_plot(self):
        qc_dir = create_dir_check_exists(self.experiment_directory, 'qc')
        qc_plot_filename = os.path.join(qc_dir, self.video_datetime + '.png')

        tag_classes_present = self.class_num_frames_tracked_dict.keys()
        tag_classes_present_names = [tag_class_names[tag_class] for tag_class in tag_classes_present]
        num_frames_tag_class_present = [self.class_num_frames_tracked_dict[tag_class] for tag_class in tag_classes_present]

        plt.figure()
        plt.bar(range(len(num_frames_tag_class_present)), num_frames_tag_class_present)
        plt.xticks(range(len(tag_classes_present_names)), tag_classes_present_names, rotation=90)
        plt.ylim(0, NUM_FRAMES_IN_VIDEO)
        plt.xlabel("Tag Class Name")
        plt.ylabel("Number of Frames Present")
        plt.title('Number of Frames Tracked by Tag Class')
        plt.savefig(qc_plot_filename)
        plt.clf()
        plt.close()
