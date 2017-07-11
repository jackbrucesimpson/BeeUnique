#include "bee.h"

#include <iostream>

Bee::Bee (PointXY initial_location, int classification, int frame_num) {
    append_point(initial_location, classification, frame_num);
}

void Bee::append_point (PointXY p, int classification, int frame_num) {
    path.push_back(p);
    classified.push_back(classification);
    frame_nums.push_back(frame_num);
}

PointXY Bee::get_last_point () {
    return path.back();
}

int Bee::get_last_frame_num () {
    return frame_nums.back();
}

std::vector<PointXY> Bee::get_path () {
    return path;
}

std::vector<int> Bee::get_classified () {
    return classified;
}

std::vector<int> Bee::get_frame_nums () {
    return frame_nums;
}

bool Bee::get_is_deleted () {
    return is_deleted;
}

void Bee::delete_bee () {
    is_deleted = true;
}

void Bee::append_flattened_28x28_tag_matrices (std::vector<int> flattened_28x28_tag_matrix) {
    flattened_28x28_tag_matrices.push_back (flattened_28x28_tag_matrix);
}

std::vector<std::vector<int>> Bee::get_flattened_28x28_tag_matrices () {
    return flattened_28x28_tag_matrices;
}
