#include "bee.h"
#include "track.h"
#include "structures.h"

#include <iostream>

int
main (int argc, char *argv[]) {

    struct point p; p.x = 11; p.y = 12; p.frame_num = 13;

    Bee new_bee(1);
    new_bee.append_point(p);

    Track track;
    track.append_bee(new_bee);
    Bee old_bee = track.get_bee();

    std::cout << old_bee.get_id() << std::endl;
    std::cout << old_bee.get_last_point().x << std::endl;
    return 0;
}
