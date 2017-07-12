#include <vector>

#ifndef __STRUCTURES_H__
#define __STRUCTURES_H__

struct PointXY {
    float x;
    float y;
};

struct OutputBeeData {
    std::vector<PointXY> xy;
    std::vector<int> frame_nums;
    std::vector<std::vector<int>> flattened_28x28_tag_matrices;
};

#endif /* __STRUCTURES_H__ */
