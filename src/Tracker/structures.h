#include <vector>

#ifndef __STRUCTURES_H__
#define __STRUCTURES_H__

struct outputbeedata {
    std::vector<float> x_path;
    std::vector<float> y_path;
    std::vector<int> frame_nums;
    std::vector<int> tag_matrix_indices;
};

#endif /* __STRUCTURES_H__ */
