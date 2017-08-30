import os

from Processor.Utils.imageutils import increment_dict_key_value
from Processor.Utils.fileutils import create_dir_check_exists
from Processor.Utils.graphics import plot_barplot
from Processor.Utils import constants

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

            if bee_path_class['tag_class'] == constants.UNKNOWN_CLASS:
                if bee_path_class['num_frames_tracked'] > constants.NUM_UNKNOWNS_IN_PATH_THRESHOLD:
                    self.bee_ids_with_long_unknowns.append(original_path_bee_id)

    def gen_qc_plot(self):
        qc_dir = create_dir_check_exists(self.experiment_directory, 'qc')
        qc_plot_filename = os.path.join(qc_dir, self.video_datetime + '.png')

        tag_classes_present = self.class_num_frames_tracked_dict.keys()
        tag_classes_present_names = [constants.TAG_CLASS_NAMES[tag_class] for tag_class in tag_classes_present]
        num_frames_tag_class_present = [self.class_num_frames_tracked_dict[tag_class] for tag_class in tag_classes_present]

        plot_barplot(num_frames_tag_class_present, tag_classes_present_names, qc_plot_filename, 'Number of Frames Tracked by Tag Class', 'Tag Class Name', 'Number of Frames Present', 0, constants.NUM_FRAMES_IN_VIDEO)
