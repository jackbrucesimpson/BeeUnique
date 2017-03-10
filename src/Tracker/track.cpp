#include "track.h"

Track::Track () {}

void Track::append_bee (Bee new_bee) {
    bee_id_counter++;
    all_bees.push_back(new_bee);
}

Bee Track::get_bee () {
    return all_bees.back();
}
