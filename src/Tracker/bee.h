#include "structures.h"
#include <vector>

#define UNKNOWN_CLASS -1

#ifndef __BEE_H__
#define __BEE_H__

class Bee {
public:
    Bee (PointXY initial_location, int classification, int frame_num);

    void append_point (PointXY p, int classification, int frame_num);

    PointXY get_last_point ();

    int get_last_frame_num ();

    std::vector<PointXY> get_path ();

    std::vector<int> get_classified ();

    std::vector<int> get_frame_nums ();

    bool get_is_deleted ();

    void delete_bee ();

    void append_flattened_28x28_tag_matrices (std::vector<int> flattened_28x28_tag_matrix);

    std::vector<std::vector<int>> get_flattened_28x28_tag_matrices ();

private:
    std::vector<PointXY> path;
    std::vector<int> frame_nums;
    std::vector<int> classified;
    std::vector<std::vector<int>> flattened_28x28_tag_matrices;
    bool is_deleted = false;
};

#endif /* __BEE_H__ */
