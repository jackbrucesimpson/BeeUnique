#include "track.h"

#include <math.h>
#include <iostream>

#define FRAMES_BEFORE_EXTINCTION 60
#define SEARCH_SURROUNDING_AREA 60
#define SEARCH_EXPANSION_BY_FRAME 30
#define MIN_CLOSENESS_BEFORE_DELETE 1
#define FPS 20
#define UNKNOWN_CLASS -1


Track::Track () {}

void Track::track_frame (std::vector<PointXY> contour_locations, std::vector<int> contour_classifications, int frame_num) {
    video_frame_num = frame_num;
    for (int i = 0; i < contour_locations.size (); i++) {

        bool found_bee_previously = identify_past_location(contour_locations, contour_classifications[i], i);

        if (!found_bee_previously) {
            Bee new_bee = Bee (contour_locations[i], contour_classifications[i], video_frame_num);
            all_bees.push_back(new_bee);
        }

    } // outer contours loop
}

bool Track::identify_past_location (std::vector<PointXY> contour_locations, int contour_classification, int contour_index) {
    bool found_bee_previously = false;
    int bee_best_match_index = 0;
    float closest_match_distance = 100000;
    PointXY current_tag_contour = contour_locations[contour_index];

    for (int i = 0; i < all_bees.size (); i++) {
        if (all_bees[i].get_is_deleted ()) {
            continue;
        }
        PointXY last_point = all_bees[i].get_last_point ();
        int last_frame_num = all_bees[i].get_last_frame_num ();
        int frames_since_last_seen = video_frame_num - last_frame_num;

        if (frames_since_last_seen > FRAMES_BEFORE_EXTINCTION) {
            all_bees[i].delete_bee ();
            continue;
        }

        float closeness_bee_current_contour = euclidian_distance (current_tag_contour, last_point);
        if (closeness_bee_current_contour > SEARCH_SURROUNDING_AREA) {
            continue;
        }

        bool better_match_other_contour = false;
        for (int j = 0; j < contour_locations.size (); j++) {
            if (contour_index == j) {
                continue;
            }
            float closeness_bee_other_contour = euclidian_distance (contour_locations[j], last_point);
            if (closeness_bee_other_contour < closeness_bee_current_contour) {
                better_match_other_contour = true;
                break;
            }
        } // contours loop

        if (!better_match_other_contour && closeness_bee_current_contour < closest_match_distance) {
            bee_best_match_index = i;
            found_bee_previously = true;
        }

    } // all_bees loop

    if (found_bee_previously) {
        all_bees[bee_best_match_index].append_point (current_tag_contour, contour_classification, video_frame_num);
    }

    return found_bee_previously;

} // bool Track::identify_past_location

std::vector<OutputBeeData> Track::get_all_bees_data () {
    std::vector <OutputBeeData> all_bees_data;
    for (int i = 0; i < all_bees.size (); i++) {
        struct OutputBeeData bee_data;
        bee_data.path = all_bees[i].get_path ();
        bee_data.classified = all_bees[i].get_classified ();
        bee_data.frame_nums = all_bees[i].get_frame_nums ();
        bee_data.flattened_28x28_tag_matrices = all_bees[i].get_flattened_28x28_tag_matrices ();
        all_bees_data.push_back (bee_data);
    }
    return all_bees_data;
}

float Track::euclidian_distance (PointXY p1, PointXY p2) {
    const float delta_x = p1.x - p2.x;
    const float delta_y = p1.y - p2.y;
    return sqrt (pow (delta_x, 2) + pow (delta_y, 2));
}

void Track::training_track_frame (std::vector<PointXY> contour_locations, std::vector<std::vector<int>> flattened_28x28_tag_matrices, int frame_num) {
    video_frame_num = frame_num;

    for (int i = 0; i < contour_locations.size (); i++) {
        bool found_bee_previously = training_identify_past_location(contour_locations, flattened_28x28_tag_matrices[i], i);
        if (!found_bee_previously) {
            Bee new_bee = Bee (contour_locations[i], UNKNOWN_CLASS, video_frame_num);
            if (flattened_28x28_tag_matrices[i].size() > 0) {
                new_bee.append_flattened_28x28_tag_matrices(flattened_28x28_tag_matrices[i]);
            }
            all_bees.push_back(new_bee);
        }
    }

}

bool Track::training_identify_past_location (std::vector<PointXY> contour_locations, std::vector<int> flattened_28x28_tag_matrix, int contour_index) {
    bool found_bee_previously = false;
    int bee_best_match_index = 0;
    float closest_match_distance = 100000;
    PointXY current_tag_contour = contour_locations[contour_index];

    for (int i = 0; i < all_bees.size (); i++) {
        if (all_bees[i].get_is_deleted ()) {
            continue;
        }

        PointXY last_point = all_bees[i].get_last_point ();
        int last_frame_num = all_bees[i].get_last_frame_num ();
        int frames_since_last_seen = video_frame_num - last_frame_num;

        if (frames_since_last_seen > FRAMES_BEFORE_EXTINCTION) {
            all_bees[i].delete_bee ();
            continue;
        }

        float closeness_bee_current_contour = euclidian_distance (current_tag_contour, last_point);
        if (closeness_bee_current_contour > SEARCH_SURROUNDING_AREA) {
            continue;
        }

        bool better_match_other_contour = false;
        for (int j = 0; j < contour_locations.size (); j++) {
            if (contour_index == j) {
                continue;
            }
            float closeness_bee_other_contour = euclidian_distance (contour_locations[j], last_point);
            if (closeness_bee_other_contour < closeness_bee_current_contour) {
                better_match_other_contour = true;
                break;
            }
            // if is_training, delete bee if too close to another
            else if (closeness_bee_other_contour < MIN_CLOSENESS_BEFORE_DELETE) {
                all_bees[i].delete_bee ();
            }
        } // contours loop

        if (!better_match_other_contour && closeness_bee_current_contour < closest_match_distance) {
            bee_best_match_index = i;
            found_bee_previously = true;
        }

    } // all_bees loop

    if (found_bee_previously) {
        all_bees[bee_best_match_index].append_point (current_tag_contour, UNKNOWN_CLASS, video_frame_num);
        if (flattened_28x28_tag_matrix.size() > 0) {
            all_bees[bee_best_match_index].append_flattened_28x28_tag_matrices (flattened_28x28_tag_matrix);
        }
    }

    return found_bee_previously;

} // bool Track::identify_past_location
