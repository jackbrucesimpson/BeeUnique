#include <vector>

#ifndef __STRUCTURES_H__
#define __STRUCTURES_H__

struct point {
    float x;
    float y;
    int frame_num;
};

struct loc_index_classified {
    int loc_index;
    int classified;
};

struct loc_index_flat_tag {
    int loc_index;
    std::vector<int> flattened_28x28_tag_matrix;
};

struct frame_classified {
    int frame_num;
    int classified;
};

struct bee_frame_data {
    float x;
    float y;
    int bee_classified;
    int current_frame_classified;
};

struct all_bee_data {
    int id;
    int class_classified;
    std::vector<point> path;
    std::vector<frame_classified> classifications;
};

#endif /* __STRUCTURES_H__ */
