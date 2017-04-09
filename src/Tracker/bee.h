#include "structures.h"
#include <vector>

#define UNKNOWN_CLASS 0

#ifndef __BEE_H__
#define __BEE_H__

class Bee {
public:
    Bee ();

    void append_point (Point p);

    Point get_last_point ();

    void set_class_classified (int new_class);

    int get_class_classified () const;

    int get_id () const;

    std::vector<Point> get_path ();

    std::vector<Point> get_recent_path ();

    std::vector<FrameClassified> get_classifications ();

    std::vector<FrameClassified> get_recent_classifications ();

    bool get_is_deleted ();

    bool get_is_merged_into_other_bee ();

    void delete_bee ();

    void merge_delete_bee ();

    void transfer_bee_path_classifications (std::vector<Point> new_points, std::vector<FrameClassified> new_frame_classifieds);

    int append_frame_classified_classify_bee (FrameClassified fc);

    void delete_recent_points_classifications ();

    void merge_recent_points_classifications ();

    void append_flattened_28x28_tag_matrices (std::vector<int> flattened_28x28_tag_matrix);

    std::vector<std::vector<int>> get_flattened_28x28_tag_matrices ();

private:
    int identity;
    Point last_point;
    std::vector<Point> path;
    std::vector<Point> recent_path;
    std::vector<FrameClassified> classifications;
    std::vector<FrameClassified> recent_classifications;

    std::vector<std::vector<int>> flattened_28x28_tag_matrices;

    int class_classified = UNKNOWN_CLASS;
    bool is_deleted = false;
    bool is_merged_into_other_bee = false;
};

#endif /* __BEE_H__ */
