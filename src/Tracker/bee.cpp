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
