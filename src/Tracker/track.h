#include "bee.h"
#include "structures.h"

#include <vector>


#ifndef __TRACK_H__
#define __TRACK_H__

class Track {
public:
    Track();

    void track_video (std::vector<int> frame_nums, std::vector<std::vector<float>> x_grouped_by_frame,
                        std::vector<std::vector<float>> y_grouped_by_frame);

    void track_frame (int frame_num, std::vector<float> x_coords, std::vector<float> y_coords);

    std::vector<outputbeedata> get_all_bees_data ();

private:
    std::vector<Bee> all_bees;
    int video_frame_num = 0;
    int tag_matrix_index = 0;

    bool identify_past_location (std::vector<float> x_coords, std::vector<float> y_coords, int coord_index);

    float euclidian_distance (float x1, float y1, float x2, float y2);
};

#endif /* __TRACK_H__ */
