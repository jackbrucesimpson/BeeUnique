#include "bee.h"

#include <unordered_map>

const int MIN_NUM_RECENT_CLASSIFICATIONS = 10;
const int HALF_MIN_NUM_RECENT_CLASSIFICATIONS = MIN_NUM_RECENT_CLASSIFICATIONS / 2;

Bee::Bee (int id) : identity (id) {}

void Bee::append_point (Point p) {
    last_point = p;
    recent_path.push_back(p);
}

Point Bee::get_last_point () {
    return last_point;
}

void Bee::set_class_classified(int new_class) {
    class_classified = new_class;
}

int Bee::get_class_classified () const {
    return class_classified;
}

int Bee::get_id () const {
    return identity;
}

std::vector<Point> Bee::get_path () {
    return path;
}

std::vector<Point> Bee::get_recent_path () {
    return recent_path;
}

std::vector<frame_classified> Bee::get_classifications () {
    return classifications;
}

std::vector<frame_classified> Bee::get_recent_classifications () {
    return recent_classifications;
}

bool Bee::get_is_deleted () {
    return is_deleted;
}

bool Bee::get_is_merged_into_other_bee () {
    return is_merged_into_other_bee;
}

void Bee::delete_bee () {
    is_deleted = true;
}

void Bee::merge_delete_bee () {
    is_merged_into_other_bee = true;
    is_deleted = true;
}

void Bee::transfer_bee_path_classifications (std::vector<Point> new_points, std::vector<frame_classified> new_frame_classifieds) {
    merge_recent_points_classifications ();
    path.insert(path.end (), new_points.begin (), new_points.end ());
    classifications.insert(classifications.end (), new_frame_classifieds.begin (), new_frame_classifieds.end ());
    last_point = path.back ();
}

int Bee::append_frame_classified_classify_bee (frame_classified fc) {
    recent_classifications.push_back (fc);
    int num_recent_classifications = recent_classifications.size ();
    // break as soon as class reaches more than 50%, else keep trying
    if (num_recent_classifications > MIN_NUM_RECENT_CLASSIFICATIONS) {
        std::unordered_map<int, int> class_classified_count_map;
        for (int i = 0; i < num_recent_classifications; i++) {
            class_classified_count_map[recent_classifications[i].classified]++;
            if (class_classified_count_map[recent_classifications[i].classified] > HALF_MIN_NUM_RECENT_CLASSIFICATIONS) {
                return recent_classifications[i].classified;
            }
        }
        merge_recent_points_classifications ();
    }
    return UNKNOWN_CLASS;
}

void Bee::delete_recent_points_classifications () {
    recent_path.clear ();
    recent_classifications.clear ();
    last_point = path.back ();
}

void Bee::merge_recent_points_classifications () {
    path.insert (path.end (), recent_path.begin (), recent_path.end ());
    classifications.insert(classifications.end (), recent_classifications.begin (), recent_classifications.end ());
    recent_path.clear ();
    recent_classifications.clear ();
}

void Bee::append_flattened_28x28_tag_matrices (std::vector<int> flattened_28x28_tag_matrix) {
    flattened_28x28_tag_matrices.push_back (flattened_28x28_tag_matrix);
}

std::vector<std::vector<int>> Bee::get_flattened_28x28_tag_matrices () {
    return flattened_28x28_tag_matrices;
}
