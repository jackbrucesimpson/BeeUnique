#include "bee.h"
#include "structures.h"

#include <vector>


#ifndef __TRACK_H__
#define __TRACK_H__

class Track {
public:
    Track();

    void track_frames_batch (std::vector<std::vector<Point>> all_contour_locations, std::vector<std::vector<int>> all_contour_classifications, std::vector<int> all_frame_nums_batch);

    void track_frame (std::vector<Point> contour_locations, std::vector<int> contour_classifications, int frame_num);

    void training_track_frame (std::vector<Point> contour_locations, std::vector<std::vector<int>> flattened_28x28_tag_matrices, int frame_num);

    std::vector<OutputBeeData> get_all_bees_data ();

private:
    std::vector<Bee> all_bees;
    int video_frame_num = 0;

    bool identify_past_location (std::vector<Point> contour_locations, int contour_classification, int contour_index);

    bool training_identify_past_location (std::vector<Point> contour_locations, std::vector<int> flattened_28x28_tag_matrix, int contour_index);

    void merge_bee_classifications (int new_class_predicted, int bee_current_class, int bee_index);

    float euclidian_distance (Point p1, Point p2);
};

#endif /* __TRACK_H__ */
