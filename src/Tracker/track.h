#include "Bee.h"
#include "structures.h"

#include <vector>


#ifndef __TRACK_H__
#define __TRACK_H__

class Track {
public:
    Track();

    void track_frames_batch (std::vector<std::vector<point>> all_contour_locations, std::vector<std::vector<loc_index_classified>> all_classified_loc_indexes);

    void track_frame (std::vector<point> contour_locations, std::vector<int> contour_classifications);

    void training_track_frame (std::vector<point> contour_locations, std::vector<loc_index_classified> classified_loc_indexes, std::vector<int> flattened_28x28_tag_matrix);

    int extract_contour_classifications (std::vector<loc_index_class> classified_loc_indexes, int num_contours);

    bool identify_past_location (std::vector<point> contour_locations, int contour_classification, int contour_index);

    void merge_bee_classifications (int new_class_predicted, int bee_current_class, int bee_index);

    std::vector<bee_frame_data> get_tracked_bees_current_frame (int current_frame);

    float euclidian_distance (point p1, point p2);

private:
    std::vector<Bee> all_bees;
    int bee_id_counter = 0;
    int frame_num = 0;
};

#endif /* __TRACK_H__ */
