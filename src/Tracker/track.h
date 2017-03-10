#include "Bee.h"
#include "structures.h"

#include <vector>


#ifndef __TRACK_H__
#define __TRACK_H__

class Track {
public:
    Track();

    void append_bee (Bee new_bee);

    Bee get_bee ();

private:
    std::vector<Bee> all_bees;
    int bee_id_counter = 0;
    int frame_num = 0;
};

#endif /* __TRACK_H__ */
