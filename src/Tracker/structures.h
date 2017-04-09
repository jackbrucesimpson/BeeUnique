#include <vector>

#ifndef __STRUCTURES_H__
#define __STRUCTURES_H__

struct Point {
    float x;
    float y;
    int classified;
    int frame_num;
};

struct FrameClassified {
    int frame_num;
    int classified;
};

struct OutputBeeData {
    int class_classified;
    std::vector<Point> path;
    std::vector<std::vector<int>> flattened_28x28_tag_matrices;
};

#endif /* __STRUCTURES_H__ */
