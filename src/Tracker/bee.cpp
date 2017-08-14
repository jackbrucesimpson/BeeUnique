#include "bee.h"

#include <iostream>

Bee::Bee (float x, float y, int frame_num, int tag_matrix_index) {
    append_point(x, y, frame_num, tag_matrix_index);
}

void Bee::append_point (float x, float y, int frame_num, int tag_matrix_index) {
    x_path.push_back(x);
    y_path.push_back(y);
    frame_nums.push_back(frame_num);
    tag_matrix_indices.push_back (tag_matrix_index);
}

float Bee::get_last_x () {
    return x_path.back();
}

float Bee::get_last_y () {
    return y_path.back();
}

int Bee::get_last_frame_num () {
    return frame_nums.back();
}

std::vector<float> Bee::get_x_path () {
    return x_path;
}

std::vector<float> Bee::get_y_path () {
    return y_path;
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

std::vector<int> Bee::get_tag_matrix_indices () {
    return tag_matrix_indices;
}
