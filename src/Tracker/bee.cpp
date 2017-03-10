#include "bee.h"

Bee::Bee (int id) : identity (id) {}

void Bee::append_point (point p) {
    last_point = p;
    recent_path.push_back(p);
}

point Bee::get_last_point () {
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

std::vector<point> Bee::get_path () {
    return path;
}

std::vector<point> Bee::get_recent_path () {
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

void Bee::delete_bee() {
    is_deleted = true;
}

//

void Bee::transfer_bee_path_classifications (std::vector<point> new_points, std::vector<frame_classified> new_frame_classifieds) {
    self.merge_recent_points_classifications()
        self.path.insert(self.path.end(), self.new_points.begin(), self.new_points.end())
        self.classifications.insert(self.classifications.end(), self.new_frame_classifieds.begin(), self.new_frame_classifieds.end())
        self.last_point = self.path.back(
}

int Bee::append_frame_classified_classify_bee (frame_classified fc) {
    self.recent_classifications.push_back(fc)
        cdef int num_recent_classifications = self.recent_classifications.size()
        cdef unordered_map[int, int] class_classified_count_map
        cdef int i
        if num_recent_classifications > MIN_NUM_RECENT_CLASSIFICATIONS:
            # break as soon as class reaches more than 50%, else keep trying
            for i in range(num_recent_classifications):
                class_classified_count_map[self.recent_classifications[i].classified] += 1
                if class_classified_count_map[self.recent_classifications[i].classified] > HALF_MIN_NUM_RECENT_CLASSIFICATIONS:
                    return self.recent_classifications[i].classified

            self.merge_recent_points_classifications()
            return UNKNOWN_CLASS

        return UNKNOWN_CLAS
}

void Bee::delete_recent_points_classifications () {
    recent_path.clear();
    recent_classifications.clear();
    last_point = path.back();
}

void Bee::merge_recent_points_classifications () {
    self.path.insert(self.path.end(), self.recent_path.begin(), self.recent_path.end())
        self.classifications.insert(self.classifications.end(), self.recent_classifications.begin(), self.recent_classifications.end())
        self.recent_path.clear()
        self.recent_classifications.clear(
}
