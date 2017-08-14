#include "structures.h"
#include <vector>

#ifndef __BEE_H__
#define __BEE_H__

class Bee {
public:
    Bee (float x, float y, int frame_num, int tag_matrix_index);
    void append_point (float x, float y, int frame_num, int tag_matrix_index);

    float get_last_x ();
    float get_last_y ();
    int get_last_frame_num ();

    std::vector<float> get_x_path ();
    std::vector<float> get_y_path ();
    std::vector<int> get_frame_nums ();

    bool get_is_deleted ();
    void delete_bee ();

    std::vector<int> get_tag_matrix_indices ();

private:
    std::vector<float> x_path;
    std::vector<float> y_path;
    std::vector<int> frame_nums;
    std::vector<int> tag_matrix_indices;
    bool is_deleted = false;
};

#endif /* __BEE_H__ */
