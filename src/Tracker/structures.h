#ifndef __STRUCTURES_H__
#define __STRUCTURES_H__

struct point {
    float x;
    float y;
    int frame_num;
};

struct loc_index_classified {
    int loc_index;
    int classified;
};

struct frame_classified {
    int frame_num;
    int classified;
};

struct bee_frame_data {
    float x;
    float y;
    int bee_classified;
    int current_frame_classified;
};

#endif /* __STRUCTURES_H__ */
