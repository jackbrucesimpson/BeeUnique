from constants import *

from beedata import BeeData

class ProcessPaths:

    def __init__(self, video_start_datetime):
        self.video_start_datetime = video_start_datetime

    def gen_gap_coords(self, current_xy_coord, prev_xy_coord, difference_prev_frame):
        x1, y1 = current_xy_coord['x'], current_xy_coord['y']
        x2, y2 = prev_xy_coord['x'], prev_xy_coord['y']
        x_diff_per_frame = (x2 - x1) / float(difference_prev_frame)
        y_diff_per_frame = (y2 - y1) / float(difference_prev_frame)

        gap_coords = []
        for gap in range(1, difference_prev_frame + 1):
            x_gap_coord = x2 - x_diff_per_frame * gap
            y_gap_coord = y2 - y_diff_per_frame * gap
            gap_coords.append({'x': x_gap_coord, 'y': y_gap_coord})

        return gap_coords

    def process_paths(self, bee_df):
        xy_list = bee_df['xy'].tolist()
        frame_nums_list = bee_df['frame_nums'].tolist()
        classifications_list = bee_df['classifications'].tolist()
        #flat_tags = bee_df['flattened_28x28_tag_matrices'].tolist()

        bee_data = BeeData(self.video_start_datetime, classifications_list[0])
        start_end_frame_num_path = {'start': frame_nums_list[0],'end': frame_nums_list[0]}
        xy_path = [xy_list[0]]

        for i in range(1, len(xy_list)):
            difference_prev_frame = frame_nums_list[i] - start_end_frame_num_path['end']

            if difference_prev_frame == 1:
                start_end_frame_num_path['end'] = frame_nums_list[i]
                xy_path.append(xy_list[i])
                bee_data.add_classification(classifications_list[i])

            elif difference_prev_frame < MAX_FRAME_GAP_BETWEEN_PATHS:
                start_end_frame_num_path['end'] = frame_nums_list[i]
                generated_coord_gaps = self.gen_gap_coords(xy_list[i], xy_list[i-1], difference_prev_frame)
                fill_path_classifications_gap = ['gap'] * len(generated_coord_gaps)
                fill_path_classifications_gap[-1] = classifications_list[i]
                xy_path.extend(generated_coord_gaps)

                for gap_classification in fill_path_classifications_gap:
                    bee_data.add_classification(gap_classification)
            else:
                bee_data.list_of_all_xy_paths.append(xy_path)
                bee_data.start_end_frame_num_all_paths.append(start_end_frame_num_path)
                xy_path = [xy_list[i]]
                start_end_frame_num_path = {'start': frame_nums_list[i], 'end': frame_nums_list[i]}
                bee_data.add_classification(classifications_list[i])

        if len(xy_path) > 0:
            bee_data.list_of_all_xy_paths.append(xy_path)
            bee_data.start_end_frame_num_all_paths.append(start_end_frame_num_path)
            bee_data.identify_freq_class_path_group()

        bee_data.merge_group_classifications_into_sections()

        bees_identified_by_tag = bee_data.gen_separate_tag_class_bees()

        return bees_identified_by_tag
