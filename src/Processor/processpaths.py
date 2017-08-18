from beedata import BeeData

from constants import *

class ProcessPaths:

    def __init__(self):
        pass

    def gen_gap_coords(self, x1, y1, x2, y2, difference_prev_frame):
        x_diff_per_frame = (x2 - x1) / float(difference_prev_frame)
        y_diff_per_frame = (y2 - y1) / float(difference_prev_frame)

        gap_coords = {'x': [], 'y': []}
        for gap in range(1, difference_prev_frame + 1):
            x_gap_coord = x2 - x_diff_per_frame * gap
            y_gap_coord = y2 - y_diff_per_frame * gap
            gap_coords['x'].append(x_gap_coord)
            gap_coords['y'].append(y_gap_coord)

        return gap_coords

    def get_class_num_frames_tracked(self, bee_tags_in_path):
        path_class_frames_tracked_list = []
        for bee in bee_tags_in_path:
            tag_class = bee['tag_class']
            num_frames_tracked = 0
            for path_index in range(len(bee['x_paths'])):
                num_frames_tracked += len(bee['x_paths'][path_index])
            path_class_frames_tracked_list.append({'tag_class': tag_class, 'num_frames_tracked': num_frames_tracked})

            return path_class_frames_tracked_list

    def process_paths(self, bee_df):
        x_list = bee_df['x'].tolist()
        y_list = bee_df['y'].tolist()
        frame_nums_list = bee_df['frame_nums'].tolist()
        classifications_list = bee_df['classifications'].tolist()

        bee_data = BeeData(classifications_list[0])
        path_frame_num_start = frame_nums_list[0]
        path_frame_num_end = frame_nums_list[0]
        x_path = [x_list[0]]
        y_path = [y_list[0]]

        for i in range(1, len(x_list)):
            difference_prev_frame = frame_nums_list[i] - path_frame_num_end

            if difference_prev_frame == 1:
                path_frame_num_end = frame_nums_list[i]
                x_path.append(x_list[i])
                y_path.append(y_list[i])
                bee_data.add_classification(classifications_list[i])

            elif difference_prev_frame < MAX_FRAME_GAP_BETWEEN_PATHS:
                path_frame_num_end = frame_nums_list[i]
                generated_coord_gaps = self.gen_gap_coords(x_list[i], y_list[i], x_list[i-1], y_list[i-1], difference_prev_frame)
                fill_path_classifications_gap = [GAP_CLASS] * len(generated_coord_gaps)
                fill_path_classifications_gap[-1] = classifications_list[i]
                x_path.extend(generated_coord_gaps['x'])
                y_path.extend(generated_coord_gaps['y'])

                for gap_classification in fill_path_classifications_gap:
                    bee_data.add_classification(gap_classification)
            else:
                bee_data.list_of_all_x_paths.append(x_path)
                bee_data.list_of_all_y_paths.append(y_path)
                bee_data.start_frame_num_all_paths.append(path_frame_num_start)
                x_path = [x_list[i]]
                y_path = [y_list[i]]
                path_frame_num_start = frame_nums_list[i]
                path_frame_num_end = frame_nums_list[i]

                bee_data.add_classification(classifications_list[i])

        if len(x_path) > 0:
            bee_data.list_of_all_x_paths.append(x_path)
            bee_data.list_of_all_y_paths.append(y_path)
            bee_data.start_frame_num_all_paths.append(path_frame_num_start)
            bee_data.identify_freq_class_path_group()

        bee_data.merge_group_classifications_into_sections()

        bees_identified_by_tag = bee_data.gen_separate_tag_class_bees()

        return bees_identified_by_tag
