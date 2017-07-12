#include "bee.h"
#include "structures.h"

#include <vector>


#ifndef __TRACK_H__
#define __TRACK_H__

class Track {
public:
    Track();

    void track_frame (std::vector<PointXY> contour_locations, std::vector<std::vector<int>> flattened_28x28_tag_matrices, int frame_num);

    std::vector<OutputBeeData> get_all_bees_data ();

private:
    std::vector<Bee> all_bees;
    int video_frame_num = 0;

    bool identify_past_location (std::vector<PointXY> contour_locations, std::vector<int> flattened_28x28_tag_matrix, int contour_index);

    float euclidian_distance (PointXY p1, PointXY p2);
};

#endif /* __TRACK_H__ */
