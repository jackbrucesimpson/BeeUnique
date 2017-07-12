#include "bee.h"

#include <iostream>

Bee::Bee (PointXY initial_location, int frame_num, std::vector<int> flattened_28x28_tag_matrix) {
    append_point(initial_location, frame_num, flattened_28x28_tag_matrix);
}

void Bee::append_point (PointXY p, int frame_num, std::vector<int> flattened_28x28_tag_matrix) {
    path.push_back(p);
    frame_nums.push_back(frame_num);
    flattened_28x28_tag_matrices.push_back (flattened_28x28_tag_matrix);
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

std::vector<int> Bee::get_frame_nums () {
    return frame_nums;
}

bool Bee::get_is_deleted () {
    return is_deleted;
}

void Bee::delete_bee () {
    is_deleted = true;
}

std::vector<std::vector<int>> Bee::get_flattened_28x28_tag_matrices () {
    return flattened_28x28_tag_matrices;
}
