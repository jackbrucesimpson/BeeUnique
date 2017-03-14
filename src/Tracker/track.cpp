#include "track.h"

#include <math.h>

#define BEST_MATCH_FRAMES_SINCE_LAST_SEEN 1000
#define CLOSEST_MATCH_DISTANCE 100000
#define FRAMES_BEFORE_EXTINCTION 75
#define SEARCH_SURROUNDING_AREA 200
#define SEARCH_EXPANSION_BY_FRAME 20
#define MIN_CLOSENESS_BEFORE_DELETE 30
#define UNKNOWN_CLASS 0


Track::Track () {}


void Track::track_frames_batch (std::vector<std::vector<point>> all_contour_locations, std::vector<std::vector<loc_index_classified>> all_classified_loc_indexes) {
    for (int i = 0; i < all_contour_locations.size (); i++) {
        std::vector<int> contour_classifications = extract_contour_classifications (all_classified_loc_indexes[i], all_contour_locations[i].size ());
        track_frame (all_contour_locations[i], contour_classifications);
    }
}

void Track::track_frame (std::vector<point> contour_locations, std::vector<int> contour_classifications) {
    for (int i = 0; i < contour_locations.size (); i++) {
        bool new_bee_found = identify_past_location(contour_locations, contour_classifications[i], i);
        if (new_bee_found) {
            Bee new_bee = Bee(bee_id_counter);
            bee_id_counter++;
            new_bee.append_point(contour_locations[i]);
            if (contour_classifications[i] != UNKNOWN_CLASS) {
                struct frame_classified fc; fc.classified = contour_classifications[i]; fc.frame_num = frame_num;
                new_bee.append_frame_classified_classify_bee (fc);
            }
            all_bees.push_back(new_bee);
        }
    }
    frame_num++;
}

std::vector<int> Track::extract_contour_classifications (std::vector<loc_index_classified> classified_loc_indexes, int num_contours) {
    std::vector<int> contour_classifications;
    int j = 0;
    for (int i = 0; i < num_contours; i++) {
        if (i == classified_loc_indexes[j].loc_index) {
            contour_classifications.push_back (classified_loc_indexes[j].classified);
            j++;
        }
        else {
            contour_classifications.push_back(UNKNOWN_CLASS);
        }
    }
    return contour_classifications;
}

bool Track::identify_past_location (std::vector<point> contour_locations, int contour_classification, int contour_index) {
    bool new_bee_found = true;

    if (all_bees.empty ()) {
        return new_bee_found;
    }

    point current_tag_contour = contour_locations[contour_index];

    for (int i = 0; i < all_bees.size (); i++) {
        if (all_bees[i].get_is_deleted ()) {
            continue;
        }

        point last_frame_loc_of_bee = all_bees[i].get_last_point();
        int frames_since_last_seen = frame_num - last_frame_loc_of_bee.frame_num;
        bool better_match_available = false;

        if (frames_since_last_seen > FRAMES_BEFORE_EXTINCTION){
            if (all_bees[i].get_class_classified() == UNKNOWN_CLASS){
                all_bees[i].delete_bee ();
            }
            continue;
        }

        float closeness_bee_current_contour = euclidian_distance (current_tag_contour, last_frame_loc_of_bee);
        if (closeness_bee_current_contour < SEARCH_SURROUNDING_AREA && closeness_bee_current_contour < frames_since_last_seen * SEARCH_EXPANSION_BY_FRAME) {
            for (int j = 0; j < all_bees.size (); j++) {
                if (contour_index != j) {
                    float closeness_to_other_tag = euclidian_distance (contour_locations[j], last_frame_loc_of_bee);
                    if (closeness_to_other_tag < closeness_bee_current_contour) {
                        better_match_available = true;
                        break;
                    }
                }
            }

            if (!better_match_available) {
                all_bees[i].append_point (current_tag_contour);
                if (contour_classification != UNKNOWN_CLASS) {
                    struct frame_classified fc; fc.classified = contour_classification; fc.frame_num = frame_num;
                    int new_class_predicted = all_bees[i].append_frame_classified_classify_bee(fc);
                    int bee_current_class = all_bees[i].get_class_classified ();
                    if (new_class_predicted != UNKNOWN_CLASS and new_class_predicted != bee_current_class) {
                        merge_bee_classifications (new_class_predicted, bee_current_class, i);
                    }
                }

                new_bee_found = false;
                return new_bee_found;
            }
        }

    }
    return new_bee_found;
}

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
             Bee new_bee = Bee(bee_id_counter);
             new_bee.transfer_bee_path_classifications(all_bees[bee_index].get_path (), all_bees[bee_index].get_classifications ());
             all_bees.push_back (new_bee);
             bee_id_counter += 1;
             all_bees[bee_index].delete_recent_points_classifications ();
         }
    }
}

std::vector<bee_frame_data> Track::get_tracked_bees_current_frame (int current_frame) {
    std::vector<bee_frame_data> bee_frame_data_current_frame;
    for (int i = 0; i < all_bees.size (); i++) {
        if (!all_bees[i].get_is_deleted ()) {
            point last_point = all_bees[i].get_last_point ();
            if (last_point.frame_num == current_frame) {
                int tag_classification = UNKNOWN_CLASS;
                std::vector<frame_classified> recent_classifications = all_bees[i].get_recent_classifications ();
                if (recent_classifications.size() > 0 && recent_classifications.back().frame_num == current_frame) {
                    tag_classification = recent_classifications.back ().classified;
                }
                else {
                    std::vector<frame_classified> classifications = all_bees[i].get_classifications ();
                    if (classifications.size () > 0 and classifications.back().frame_num == current_frame) {
                        tag_classification = recent_classifications.back ().classified;
                    }
                }

                struct bee_frame_data bee_data; bee_data.x = last_point.x; bee_data.y = last_point.y; bee_data.bee_classified = all_bees[i].get_class_classified (); bee_data.current_frame_classified = tag_classification;
                bee_frame_data_current_frame.push_back(bee_data);
            }
        }
    }
    return bee_frame_data_current_frame;
}

void Track::training_track_frame (std::vector<point> contour_locations, std::vector<loc_index_classified> classified_loc_indexes, std::vector<int> flattened_28x28_tag_matrix) {

}

float Track::euclidian_distance (point p1, point p2) {
    const float delta_x = p1.x - p2.x;
    const float delta_y = p1.y - p2.y;
    return sqrt (pow (delta_x, 2) + pow (delta_y, 2));
}
