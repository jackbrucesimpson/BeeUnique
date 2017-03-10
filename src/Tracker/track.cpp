#include "track.h"

#include <math.h>

#define BEST_MATCH_FRAMES_SINCE_LAST_SEEN 1000
#define CLOSEST_MATCH_DISTANCE 100000
#define FRAMES_BEFORE_EXTINCTION 75
#define SEARCH_SURROUNDING_AREA 200
#define SEARCH_EXPANSION_BY_FRAME 20
#define MIN_CLOSENESS_BEFORE_DELETE 10
#define MIN_CLOSENESS_BEFORE_DELETE 30
#define UNKNOWN_CLASS 0


Track::Track () {}

void Track::track_frames_batch (std::vector<std::vector<point>> all_contour_locations, std::vector<std::vector<loc_index_classified>> all_classified_loc_indexes) {
    cdef i
        cdef vector[int] contour_classifications
        cdef int num_contours
        for i in range(all_contour_locations.size()):
            num_contours = all_contour_locations[i].size()
            contour_classifications = extract_contour_classifications(all_classified_loc_indexes[i], num_contours)
            self.track_frame(all_contour_locations[i], contour_classifications)
}

void Track::track_frame (std::vector<point> contour_locations, std::vector<int> contour_classifications) {
    cdef int i
       cdef Bee new_bee
       cdef bool new_bee_found
       for i in range(contour_locations.size()):
           new_bee_found = self.identify_past_location(contour_locations, contour_classifications[i], i)
           if new_bee_found:
               new_bee = Bee(self.bee_id_counter)
               self.bee_id_counter += 1
               new_bee.append_point(contour_locations[i])
               if contour_classifications[i] != UNKNOWN_CLASS:
                   new_bee.append_frame_classified_classify_bee(contour_classifications[i])
               self.all_bees.push_back(new_bee)

       self.frame_num +=1
}

int extract_contour_classifications (std::vector<loc_index_class> classified_loc_indexes, int num_contours) {
    cdef vector[int] contour_classifications
        cdef int i, j
        j = 0
        for i in range(num_contours):
            if i == classified_loc_indexes[j].loc_index:
                contour_classifications.push_back(classified_loc_indexes[j].classification)
                j += 1
            else:
                contour_classifications.push_back(UNKNOWN_CLASS)

        return contour_classification
}

bool Track::identify_past_location (std::vector<point> contour_locations, int contour_classification, int contour_index) {
    cdef bool new_bee_found = True

        if self.all_bees.empty():
            return new_bee_found

        cdef int j
        cdef point current_tag_contour
        cdef point last_frame_loc_of_bee
        cdef int frames_since_last_seen
        cdef bool better_match_available
        cdef float closeness_bee_current_contour
        cdef float closeness_to_other_tag
        cdef int new_class_predicted
        cdef int bee_current_class

        cdef int i
        for i in range(all_bees.size()):
            if all_bees[i].get_is_deleted():
                continue

            current_tag_contour = contour_locations[contour_index]
            last_frame_loc_of_bee = all_bees[i].get_last_point()
            frames_since_last_seen = self.frame_num - last_frame_loc_of_bee.frame_seen
            better_match_available = False

            if frames_since_last_seen > FRAMES_BEFORE_EXTINCTION:
                if all_bees[i].get_class_classified() == UNKNOWN_CLASS:
                    all_bees[i].delete_bee(False)
                continue

            closeness_bee_current_contour = self.euclidian_distance(current_tag_contour, last_frame_loc_of_bee)
            if closeness_bee_current_contour < SEARCH_SURROUNDING_AREA and closeness_bee_current_contour < best_match_frames_since_last_seen * SEARCH_EXPANSION_BY_FRAME:
                for j in range(contour_locations.size()):
                    if contour_index != j:
                        closeness_to_other_tag = self.euclidian_distance (contour_locations[j], last_frame_loc_of_bee)
                        if closeness_to_other_tag < closeness_bee_current_contour:
                            better_match_available = True
                            break

                if not better_match_available:
                    all_bees[i].append_point(current_tag_contour)
                    if contour_classification != UNKNOWN_CLASS:
                        new_class_predicted = all_bees[i].append_frame_classified_classify_bee(contour_classifications[j])
                        bee_current_class = all_bees[i].get_class_classified()
                        if new_class_predicted != UNKNOWN_CLASS and new_class_predicted != bee_current_class:
                            merge_bee_classifications(new_class_predicted, bee_current_class, i)

                    new_bee_found = False
                    return new_bee_found

        return new_bee_found
}

void Track::merge_bee_classifications (int new_class_predicted, int bee_current_class, int bee_index) {
    cdef int i
           cdef bool no_other_bees_have_class = True
           cdef Bee new_bee
           cdef int other_bee_class

           for i in range(self.all_bees.size()):
               if i != bee_index:
                   other_bee_class = self.all_bees[i].get_class_classified()
                   if new_class_predicted == other_bee_class:
                       if bee_current_class == UNKNOWN_CLASS:
                           # collapse bee into known class, check when last saw known class and where
                           all_bees[bee_index].merge_recent_points_classifications()
                           all_bees[i].transfer_bee_path_classifications(self.all_bees[bee_index].get_path(), self.all_bees[bee_index].get_classifications())
                           # delete bee and clear path/index
                           all_bees[bee_index].delete_bee(True)
                       else:
                           # known class bee type needs data moved to other known class bee since new class identified
                           all_bees[i].transfer_bee_path_classifications(self.all_bees[bee_index].get_path(), self.all_bees[bee_index].get_classifications())
                           all_bees[bee_index].delete_recent_points_classifications()

                       no_other_bees_have_class = False
                       break
               # set class even if already set
           if no_other_bees_have_class:
               if bee_current_class == UNKNOWN_CLASS:
                   all_bees[bee_index].set_class_classified(new_class_predicted)
                   all_bees[bee_index].merge_recent_points_classifications()
               else:
                   # bee already has different class and no instance of new class has been seen before, create new bee with info since new classification was made
                   new_bee = Bee(self.bee_id_counter)
                   new_bee.transfer_bee_path_classifications(self.all_bees[bee_index].get_path(), self.all_bees[bee_index].get_classifications())
                   self.all_bees.append(new_bee)
                   self.bee_id_counter += 1
                   all_bees[bee_index].delete_recent_points_classifications()
}

std::vector<bee_frame_data> Track::get_tracked_bees_current_frame (int current_frame) {
    cdef i
        cdef vector[point] bee_point_classifications_current_frame
        cdef point last_point
        cdef int tag_classification
        cdef vector[frame_classified] recent_classifications
        cdef vector[frame_classified] classifications
        cdef point_classification classified_point

        for i in range(self.all_bees.size()):
            if not all_bees[i].get_is_deleted():
                last_point = all_bees[i].get_last_point()
                if last_point.frame_num == current_frame:
                    tag_classification = 0
                    recent_classifications = all_bees[i].get_recent_classifications()
                    classifications = all_bees[i].get_classifications()
                    if recent_classifications.size() > 0 and recent_classifications.back().frame_num == current_frame:
                        tag_classification = recent_classifications.back()
                    elif classifications.size() > 0 and classifications.back().frame_num == current_frame:
                        tag_classification = recent_classifications.back()

                    classified_point = point_classification(x=last_point.x, y=last_point.y, bee_classification=all_bees[i].get_class_classified, current_tag_classification=tag_classification)
                    bee_point_classifications_current_frame.push_back(classified_point)

        return bee_point_classifications_current_frame
}

float Track::euclidian_distance (point p1, point p2) {
    const float delta_x = p1.x - p2.x;
    const float delta_y = p1.y - p2.y;
    return sqrt (pow (delta_x, 2) + pow (delta_y, 2);
}
