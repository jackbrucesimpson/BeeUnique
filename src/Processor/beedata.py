from image_utils import increment_dict_key_value
from constants import *

class BeeData:

    bee_id = 0

    def __init__(self, classification):

        self.start_frame_num_all_paths = []
        self.list_of_all_x_paths = []
        self.list_of_all_y_paths = []

        self.consensus_grouped_classifications = []
        self.num_classifications_in_group = 0

        self.class_counts_path = {UNKNOWN_CLASS: 0, GAP_CLASS: 0}
        self.add_classification(classification)

    def get_most_freq_class_pred(self, section_classifications):
        num_classifications = len(section_classifications)
        num_mixed = section_classifications.count(MIXED_CLASS)
        num_unknown = section_classifications.count(UNKNOWN_CLASS)
        num_mixed_unknown = num_mixed + num_unknown
        num_known = num_classifications - num_mixed_unknown

        if num_classifications < 2:
            return UNKNOWN_CLASS
        elif num_mixed > 1:
            return MIXED_CLASS
        elif num_mixed_unknown > 2:
            return UNKNOWN_CLASS
        elif num_known <= num_mixed_unknown:
            return UNKNOWN_CLASS
        else:
            section_count_dict = {MIXED_CLASS: 0, UNKNOWN_CLASS: 0}
            for classification in section_classifications:
                section_count_dict = increment_dict_key_value(section_count_dict, classification)

            del section_count_dict[MIXED_CLASS]
            del section_count_dict[UNKNOWN_CLASS]

            percent_section_count_dict = {c: float(section_count_dict[c]) / num_known for c in section_count_dict}
            most_freq_class_pred = max(section_count_dict, key=section_count_dict.get)

            if percent_section_count_dict[most_freq_class_pred] > 0.5:
                return most_freq_class_pred
            else:
                return MIXED_CLASS

    def add_classification(self, classification):
        self.num_classifications_in_group += 1
        self.class_counts_path = increment_dict_key_value(self.class_counts_path, classification)

        if self.num_classifications_in_group == NUM_GROUP_CLASSIFICATIONS:
            self.identify_freq_class_path_group()
            self.num_classifications_in_group = 0

    def identify_freq_class_path_group(self):
        num_unknown_gaps_classified = self.class_counts_path[UNKNOWN_CLASS] + self.class_counts_path[GAP_CLASS]
        num_remaining_classified = self.num_classifications_in_group - num_unknown_gaps_classified
        if self.num_classifications_in_group < MIN_NUM_CLASSIFIED_GROUP or num_remaining_classified < MIN_NUM_CLASSIFIED_GROUP:
            self.consensus_grouped_classifications.append(UNKNOWN_CLASS)
        else:
            del self.class_counts_path[UNKNOWN_CLASS]
            del self.class_counts_path[GAP_CLASS]
            percent_class_counts_path = {c: float(self.class_counts_path[c]) / num_remaining_classified for c in self.class_counts_path}
            most_freq_class_pred = max(percent_class_counts_path, key=percent_class_counts_path.get)
            if percent_class_counts_path[most_freq_class_pred] > CLASS_CONF_THRESH:
                self.consensus_grouped_classifications.append(most_freq_class_pred)
            else:
                self.consensus_grouped_classifications.append(MIXED_CLASS)

        self.current_group_tags = []
        self.class_counts_path = {UNKNOWN_CLASS: 0, GAP_CLASS: 0}

    def identify_uncertain_region(self, list_classifications):
        is_uncertain_region = False
        num_mixed = list_classifications.count(MIXED_CLASS)
        num_unknown = list_classifications.count(UNKNOWN_CLASS)
        if num_mixed > 1 or num_unknown > 3 or num_mixed + num_unknown > 3:
            is_uncertain_region = True
        return is_uncertain_region


    def get_index_prev_class(self, current_path_index, current_section_pred, classifications_list):
        while True:
            if current_section_pred != classifications_list[current_path_index]:
                return current_path_index
            else:
                current_path_index -= 1

    def merge_group_classifications_into_sections(self):
        num_grouped_classifications = len(self.consensus_grouped_classifications)
        num_concurrent_mixed = 0
        num_concurrent_unknown = 0
        is_unknown_path_section = False
        self.class_path_end_index = []
        self.classes_in_path = []
        prev_classification = None

        for i in range(0, num_grouped_classifications, NUM_GROUPS_IN_SECTION):
            current_section = self.consensus_grouped_classifications[i:i+NUM_GROUPS_IN_SECTION]
            current_section_pred = self.get_most_freq_class_pred(current_section)

            if current_section_pred == MIXED_CLASS:
                num_concurrent_mixed += 1
            elif current_section_pred == UNKNOWN_CLASS:
                num_concurrent_unknown += 1
            else:
                num_concurrent_mixed_unknown = num_concurrent_mixed + num_concurrent_unknown
                current_prev_pred_same = current_section_pred == prev_classification

                if current_prev_pred_same:
                    if num_concurrent_mixed > 2 or num_concurrent_mixed_unknown > 6:
                        is_unknown_path_section = True
                else:
                    if num_concurrent_mixed > 1 or num_concurrent_mixed_unknown > 3:
                        is_unknown_path_section = True

                if is_unknown_path_section and prev_classification is None:
                    prev_classification = UNKNOWN_CLASS

                if prev_classification is None:
                    prev_classification = current_section_pred
                    current_prev_pred_same = True

                if not current_prev_pred_same or is_unknown_path_section:
                    # covers case where there's gap or new class
                    prev_class_index = self.get_index_prev_class(i,  current_section_pred, self.consensus_grouped_classifications)
                    self.class_path_end_index.append(prev_class_index * NUM_GROUP_CLASSIFICATIONS)
                    if is_unknown_path_section:
                        self.classes_in_path.append(UNKNOWN_CLASS)
                    else:
                        self.classes_in_path.append(prev_classification)

                prev_classification = current_section_pred
                num_concurrent_mixed = 0
                num_concurrent_unknown = 0
                is_unknown_path_section = False

        num_concurrent_mixed_unknown = num_concurrent_mixed + num_concurrent_unknown
        if prev_classification is None:
            self.classes_in_path.append(UNKNOWN_CLASS)
            self.class_path_end_index.append(num_grouped_classifications * NUM_GROUP_CLASSIFICATIONS)
        elif num_concurrent_mixed_unknown == 0 or num_concurrent_mixed < 3 and num_concurrent_mixed_unknown < 7:
            self.classes_in_path.append(prev_classification)
            self.class_path_end_index.append(num_grouped_classifications * NUM_GROUP_CLASSIFICATIONS)
        else:
            final_section = self.consensus_grouped_classifications[num_grouped_classifications-(num_concurrent_mixed_unknown*NUM_GROUPS_IN_SECTION):num_grouped_classifications]
            current_section_pred = self.get_most_freq_class_pred(final_section)
            prev_class_index = self.get_index_prev_class(num_grouped_classifications-1,  current_section_pred, self.consensus_grouped_classifications)
            self.class_path_end_index.append(prev_class_index * NUM_GROUP_CLASSIFICATIONS)
            self.classes_in_path.append(prev_classification)

            self.class_path_end_index.append(num_grouped_classifications * NUM_GROUP_CLASSIFICATIONS)
            self.classes_in_path.append(UNKNOWN_CLASS)

    def gen_separate_tag_class_bees(self):
        num_coords = 0
        path_class_index = 0
        bee_paths_index_starts = 0
        bee_tags_in_path = []

        class_x_path_coords = None
        class_y_path_coords = None
        class_path_start_frame_num = None

        list_class_x_path_coords = []
        list_class_y_path_coords = []
        list_class_path_start_frame_nums = []

        for paths_index in range(len(self.list_of_all_x_paths)):
            class_x_path_coords = self.list_of_all_x_paths[paths_index]
            class_y_path_coords = self.list_of_all_y_paths[paths_index]
            class_path_start_frame_num = self.start_frame_num_all_paths[paths_index]
            for coord_index in range(len(self.list_of_all_x_paths[paths_index])):
                if num_coords > self.class_path_end_index[path_class_index]:
                    list_class_x_path_coords.append(class_x_path_coords[:coord_index])
                    list_class_y_path_coords.append(class_y_path_coords[:coord_index])
                    list_class_path_start_frame_nums.append(class_path_start_frame_num)
                    bee_tag_data = {'bee_id': self.bee_id, 'tag_class': self.classes_in_path[path_class_index], 'x_paths': list_class_x_path_coords, 'y_paths': list_class_y_path_coords, 'start_frame_nums': list_class_path_start_frame_nums}
                    self.bee_id += 1
                    bee_tags_in_path.append(bee_tag_data)

                    class_path_start_frame_num += coord_index
                    class_x_path_coords = class_x_path_coords[coord_index:]
                    class_y_path_coords = class_y_path_coords[coord_index:]
                    list_class_x_path_coords = []
                    list_class_y_path_coords = []
                    list_class_path_start_frame_nums = []

                    path_class_index += 1

                num_coords += 1

            list_class_x_path_coords.append(class_x_path_coords)
            list_class_y_path_coords.append(class_y_path_coords)
            list_class_path_start_frame_nums.append(class_path_start_frame_num)

        bee_tag_data = {'bee_id': self.bee_id, 'tag_class': self.classes_in_path[path_class_index], 'x_paths': list_class_x_path_coords, 'y_paths': list_class_y_path_coords, 'start_frame_nums': list_class_path_start_frame_nums}
        self.bee_id += 1
        bee_tags_in_path.append(bee_tag_data)

        return bee_tags_in_path
