from libcpp.vector cimport vector

cdef extern from "structures.h":
    struct point:
        float x
        float y
        int frame_num

    struct loc_index_classified:
        int loc_index
        int classified

    struct loc_index_flat_tag:
        int loc_index
        vector[int] flattened_28x28_tag_matrix

    struct bee_frame_data:
        float x
        float y
        int bee_classified
        int current_frame_classified

    struct frame_classified:
        int frame_num
        int classified

    struct all_bee_data:
        int id
        int class_classified
        vector[point] path
        vector[frame_classified] classifications

cdef extern from "track.h":
    cdef cppclass Track:
        Track() except +
        void track_frames_batch (vector[vector[point]], vector[vector[loc_index_classified]])
        void track_frame (vector[point], vector[int])
        void training_track_frame (vector[point], vector[loc_index_flat_tag])
        vector[bee_frame_data] get_tracked_bees_current_frame (int)
        vector[all_bee_data] get_all_bees_data ()

cdef class PyTrack:
    cdef Track track
    def __cinit__(self):
        self.track = Track()
    def track_frames_batch(self, all_contour_locations, all_classified_loc_indexes):
        self.track.track_frames_batch(all_contour_locations, all_classified_loc_indexes)
    def track_frame(self, contour_locations, contour_classifications):
        self.track.track_frame(contour_locations, contour_classifications)
    def training_track_frame(self, contour_locations, flat_tag_loc_indexes):
        self.track.training_track_frame(contour_locations, flat_tag_loc_indexes)
    def get_tracked_bees_current_frame(self, current_frame):
        bee_frame_data = self.track.get_tracked_bees_current_frame (current_frame)
        return bee_frame_data
    def get_all_bees(self):
        return self.track.get_all_bees_data()
