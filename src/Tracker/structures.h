#include <vector>

#ifndef __STRUCTURES_H__
#define __STRUCTURES_H__

struct PointXY {
    float x;
    float y;
};

struct OutputBeeData {
    std::vector<PointXY> path;
    std::vector<int> frame_nums;
    std::vector<int> classified;
    std::vector<std::vector<int>> flattened_28x28_tag_matrices;
};

#endif /* __STRUCTURES_H__ */
