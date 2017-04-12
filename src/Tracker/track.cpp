#include "track.h"

#include <math.h>
#include <iostream>

#define BEST_MATCH_FRAMES_SINCE_LAST_SEEN 1000
#define CLOSEST_MATCH_DISTANCE 100000
#define FRAMES_BEFORE_EXTINCTION 80
#define SEARCH_SURROUNDING_AREA 200
#define SEARCH_EXPANSION_BY_FRAME 20
#define MIN_CLOSENESS_BEFORE_DELETE 60
#define UNKNOWN_CLASS 0


Track::Track () {}

void Track::track_frames_batch (std::vector<std::vector<Point>> all_contour_locations, std::vector<std::vector<int>> all_contour_classifications, std::vector<int> all_frame_nums_batch) {
    for (int i = 0; i < all_contour_locations.size (); i++) {
        track_frame (all_contour_locations[i], all_contour_classifications[i], all_frame_nums_batch[i]);
    }
}

void Track::track_frame (std::vector<Point> contour_locations, std::vector<int> contour_classifications, int frame_num) {
    video_frame_num = frame_num;
    for (int i = 0; i < contour_locations.size (); i++) {

        bool new_bee_found = identify_past_location(contour_locations, contour_classifications[i], i);

        if (new_bee_found) {
            Bee new_bee = Bee ();
            new_bee.append_point (contour_locations[i]);
            if (contour_classifications[i] != UNKNOWN_CLASS) {
                struct FrameClassified fc; fc.classified = contour_classifications[i]; fc.frame_num = video_frame_num;
                new_bee.append_frame_classified_classify_bee (fc);
            }
            all_bees.push_back(new_bee);
        } // if new bee

    } // outer contours loop
}

bool Track::identify_past_location (std::vector<Point> contour_locations, int contour_classification, int contour_index) {
    bool new_bee_found = true;
    bool found_bee_previously = false;
    int bee_best_match_index = 0;
    float closest_match_distance = 100000;
    Point current_tag_contour = contour_locations[contour_index];

    for (int i = 0; i < all_bees.size (); i++) {
        if (all_bees[i].get_is_deleted ()) {
            continue;
        }
        Point last_frame_loc_of_bee = all_bees[i].get_last_point();
        int frames_since_last_seen = video_frame_num - last_frame_loc_of_bee.frame_num;

        if (frames_since_last_seen > FRAMES_BEFORE_EXTINCTION) {
            all_bees[i].delete_bee ();
            continue;
        }

        float closeness_bee_current_contour = euclidian_distance (current_tag_contour, last_frame_loc_of_bee);
        if (closeness_bee_current_contour > SEARCH_SURROUNDING_AREA || closeness_bee_current_contour > frames_since_last_seen * SEARCH_EXPANSION_BY_FRAME) {
            continue;
        }

        bool better_match_other_contour = false;
        for (int j = 0; j < contour_locations.size (); j++) {
            if (contour_index == j) {
                continue;
            }
            float closeness_bee_other_contour = euclidian_distance (contour_locations[j], last_frame_loc_of_bee);
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
        all_bees[bee_best_match_index].append_point (current_tag_contour);
        if (contour_classification != UNKNOWN_CLASS) {
            struct FrameClassified fc; fc.classified = contour_classification; fc.frame_num = video_frame_num;
            int new_class_predicted = all_bees[bee_best_match_index].append_frame_classified_classify_bee (fc);
            int bee_current_class = all_bees[bee_best_match_index].get_class_classified ();
            if (new_class_predicted != UNKNOWN_CLASS and new_class_predicted != bee_current_class) {
                merge_bee_classifications (new_class_predicted, bee_current_class, bee_best_match_index);
            }
        }
    }

    return new_bee_found;

} // bool Track::identify_past_location

void Track::merge_bee_classifications (int new_class_predicted, int bee_current_class, int bee_index) {
    bool no_other_bees_have_class = true;
    for (int i = 0; i < all_bees.size (); i++) {
        if (i != bee_index) {
            int other_bee_class = all_bees[i].get_class_classified ();
            if (new_class_predicted == other_bee_class) {
                // collapse bee into known class, check when last saw known class and where
                if (bee_current_class == UNKNOWN_CLASS) {
                    all_bees[bee_index].merge_recent_points_classifications ();
                    all_bees[i].transfer_bee_path_classifications (all_bees[bee_index].get_path (), all_bees[bee_index].get_classifications ());
                    all_bees[bee_index].merge_delete_bee ();
                }
                else {
                    // known class bee type needs data moved to other known class bee since new class identified
                    all_bees[i].transfer_bee_path_classifications (all_bees[bee_index].get_path (), all_bees[bee_index].get_classifications ());
                    all_bees[bee_index].delete_recent_points_classifications ();
                }
                no_other_bees_have_class = false;
                break;
            }
        }
    }

    if (no_other_bees_have_class) {
         if (bee_current_class == UNKNOWN_CLASS) {
             all_bees[bee_index].set_class_classified (new_class_predicted);
             all_bees[bee_index].merge_recent_points_classifications ();
         }
         else {
             // bee already has different class and no instance of new class has been seen before, create new bee with info since new classification was made
             Bee new_bee = Bee();
             new_bee.transfer_bee_path_classifications(all_bees[bee_index].get_path (), all_bees[bee_index].get_classifications ());
             all_bees.push_back (new_bee);
             all_bees[bee_index].delete_recent_points_classifications ();
         }
    }
}

std::vector<OutputBeeData> Track::get_all_bees_data () {
    std::vector <OutputBeeData> non_merged_bees_data;
    for (int i = 0; i < all_bees.size (); i++) {
        if (!all_bees[i].get_is_merged_into_other_bee ()) {
            all_bees[i].merge_recent_points_classifications ();
            struct OutputBeeData bee_data;
            bee_data.class_classified = all_bees[i].get_class_classified ();
            bee_data.path = all_bees[i].get_path ();
            bee_data.flattened_28x28_tag_matrices = all_bees[i].get_flattened_28x28_tag_matrices ();
            non_merged_bees_data.push_back (bee_data);
        }
    }

    return non_merged_bees_data;
}

float Track::euclidian_distance (Point p1, Point p2) {
    const float delta_x = p1.x - p2.x;
    const float delta_y = p1.y - p2.y;
    return sqrt (pow (delta_x, 2) + pow (delta_y, 2));
}

void Track::training_track_frame (std::vector<Point> contour_locations, std::vector<std::vector<int>> flattened_28x28_tag_matrices, int frame_num) {
    video_frame_num = frame_num;

    for (int i = 0; i < contour_locations.size (); i++) {
        bool new_bee_found = training_identify_past_location(contour_locations, flattened_28x28_tag_matrices[i], i);
        if (new_bee_found) {
            Bee new_bee = Bee ();
            new_bee.append_point (contour_locations[i]);
            if (flattened_28x28_tag_matrices[i].size() > 0) {
                new_bee.append_flattened_28x28_tag_matrices(flattened_28x28_tag_matrices[i]);
            }
            all_bees.push_back(new_bee);
        }
    }

}

bool Track::training_identify_past_location (std::vector<Point> contour_locations, std::vector<int> flattened_28x28_tag_matrix, int contour_index) {
    bool new_bee_found = true;
    bool found_bee_previously = false;
    int bee_best_match_index = 0;
    float closest_match_distance = 100000;
    Point current_tag_contour = contour_locations[contour_index];

    for (int i = 0; i < all_bees.size (); i++) {
        if (all_bees[i].get_is_deleted ()) {
            continue;
        }
        Point last_frame_loc_of_bee = all_bees[i].get_last_point();
        int frames_since_last_seen = video_frame_num - last_frame_loc_of_bee.frame_num;

        if (frames_since_last_seen > FRAMES_BEFORE_EXTINCTION) {
            all_bees[i].delete_bee ();
            continue;
        }

        float closeness_bee_current_contour = euclidian_distance (current_tag_contour, last_frame_loc_of_bee);
        if (closeness_bee_current_contour > SEARCH_SURROUNDING_AREA || closeness_bee_current_contour > frames_since_last_seen * SEARCH_EXPANSION_BY_FRAME) {
            continue;
        }

        bool better_match_other_contour = false;
        for (int j = 0; j < contour_locations.size (); j++) {
            if (contour_index == j) {
                continue;
            }
            float closeness_bee_other_contour = euclidian_distance (contour_locations[j], last_frame_loc_of_bee);
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
        all_bees[bee_best_match_index].append_point (current_tag_contour);
        if (flattened_28x28_tag_matrix.size() > 0) {
            all_bees[bee_best_match_index].append_flattened_28x28_tag_matrices (flattened_28x28_tag_matrix);
        }
        bool new_bee_found = false;
        return new_bee_found;
    }

    return new_bee_found;

} // bool Track::identify_past_location
