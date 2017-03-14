from libcpp.vector cimport vector

cdef extern from "structures.h":
    struct point:
        float x
        float y
        int frame_num

    struct loc_index_classified:
        int loc_index
        int classified

    struct bee_frame_data:
        float x
        float y
        int bee_classified
        int current_frame_classified


cdef extern from "track.h":
    cdef cppclass Track:
        Track() except +
        void track_frames_batch (vector[vector[point]] all_contour_locations, vector[vector[loc_index_classified]] all_classified_loc_indexes)
        void track_frame (vector[point] contour_locations, vector[int] contour_classifications)
        void training_track_frame (vector[point] contour_locations, vector[loc_index_classified] classified_loc_indexes, vector[int] flattened_28x28_tag_matrix)
        vector[bee_frame_data] get_tracked_bees_current_frame (int current_frame)

cpdef test():
    b = new Bee(21)
    print(b.get_class_classified())
    print(b.get_id())

    cdef point p
    p.x = 11
    p.y = 12
    p.frame_num = 13
    b.append_point(p)
    print(b.get_last_point())

cdef class PyTrack:
    cdef Track track
    def __cinit__(self):
        self.track = track()
    def track_frames_batch(all_contour_locations, all_classified_loc_indexes):
        self.track.track_frames_batch(all_contour_locations, all_classified_loc_indexes)
