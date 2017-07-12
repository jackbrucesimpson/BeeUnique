#include "structures.h"
#include <vector>

#define UNKNOWN_CLASS -1

#ifndef __BEE_H__
#define __BEE_H__

class Bee {
public:
    Bee (PointXY initial_location, int frame_num, std::vector<int> flattened_28x28_tag_matrix);

    void append_point (PointXY p, int frame_num, std::vector<int> flattened_28x28_tag_matrix);

    PointXY get_last_point ();

    int get_last_frame_num ();

    std::vector<PointXY> get_path ();

    std::vector<int> get_frame_nums ();

    bool get_is_deleted ();

    void delete_bee ();

    std::vector<std::vector<int>> get_flattened_28x28_tag_matrices ();

private:
    std::vector<PointXY> path;
    std::vector<int> frame_nums;
    std::vector<std::vector<int>> flattened_28x28_tag_matrices;
    bool is_deleted = false;
};

#endif /* __BEE_H__ */
