#include "track.h"

#include <math.h>
#include <iostream>

#define FRAMES_BEFORE_EXTINCTION 60
#define SEARCH_SURROUNDING_AREA 60
#define SEARCH_EXPANSION_BY_FRAME 30
#define FPS 20

Track::Track () {}

void Track::track_video (std::vector<int> frame_nums, std::vector<std::vector<float>> x_grouped_by_frame,
                        std::vector<std::vector<float>> y_grouped_by_frame) {

    for (int i = 0; i < frame_nums.size (); i++) {
        track_frame (frame_nums[i], x_grouped_by_frame[i], y_grouped_by_frame[i]);
    }
}

void Track::track_frame (int frame_num, std::vector<float> x_coords, std::vector<float> y_coords) {
    video_frame_num = frame_num;
    for (int i = 0; i < x_coords.size (); i++) {
        bool found_bee_previously = identify_past_location (x_coords, y_coords, i);
        if (!found_bee_previously) {
            Bee new_bee = Bee (x_coords[i], y_coords[i], video_frame_num, tag_matrix_index);
            all_bees.push_back (new_bee);
        }
        tag_matrix_index++;
    }
}

bool Track::identify_past_location (std::vector<float> x_coords, std::vector<float> y_coords, int coord_index) {
    bool found_bee_previously = false;
    int bee_best_match_index = 0;
    float closest_match_distance = 100000;

    for (int i = 0; i < all_bees.size (); i++) {
        if (all_bees[i].get_is_deleted ()) {
            continue;
        }

        float last_x = all_bees[i].get_last_x ();
        float last_y = all_bees[i].get_last_y ();
        int last_frame_num = all_bees[i].get_last_frame_num ();

        int frames_since_last_seen = video_frame_num - last_frame_num;
        if (frames_since_last_seen > FRAMES_BEFORE_EXTINCTION) {
            all_bees[i].delete_bee ();
            continue;
        }

        float closeness_bee_current_coord = euclidian_distance (x_coords[coord_index], y_coords[coord_index],
                                                                last_x, last_y);

        if (closeness_bee_current_coord > SEARCH_SURROUNDING_AREA) {
            continue;
        }

        bool better_match_other_contour = false;
        for (int j = 0; j < x_coords.size (); j++) {
            if (coord_index == j) {
                continue;
            }
            float closeness_bee_other_contour = euclidian_distance (x_coords[j],  y_coords[j],
                                                                    last_x, last_y);

            if (closeness_bee_other_contour < closeness_bee_current_coord) {
                better_match_other_contour = true;
                break;
            }
        } // contours loop

        if (!better_match_other_contour && closeness_bee_current_coord < closest_match_distance) {
            bee_best_match_index = i;
            found_bee_previously = true;
        }

    } // all_bees loop

    if (found_bee_previously) {
        all_bees[bee_best_match_index].append_point (x_coords[coord_index], y_coords[coord_index],
                                                    video_frame_num, tag_matrix_index);
    }

    return found_bee_previously;

}

std::vector<outputbeedata> Track::get_all_bees_data () {
    std::vector <outputbeedata> all_bees_data;
    for (int i = 0; i < all_bees.size (); i++) {
        struct outputbeedata bee_data;
        bee_data.x_path = all_bees[i].get_x_path ();
        bee_data.y_path = all_bees[i].get_y_path ();
        bee_data.frame_nums = all_bees[i].get_frame_nums ();
        bee_data.tag_matrix_indices = all_bees[i].get_tag_matrix_indices ();
        all_bees_data.push_back (bee_data);
    }
    return all_bees_data;
}

float Track::euclidian_distance (float x1, float y1, float x2, float y2) {
    const float delta_x = x1 - x2;
    const float delta_y = y1 - y2;
    return sqrt (pow (delta_x, 2) + pow (delta_y, 2));
}
