from libcpp.vector cimport vector

cdef extern from "structures.h":
    struct Point:
        float x
        float y
        int frame_num

    struct FrameClassified:
        int frame_num
        int classified

    struct OutputBeeData:
        int class_classified
        vector[Point] path
        vector[FrameClassified] classifications
        vector[vector[int]] flattened_28x28_tag_matrices

cdef extern from "track.h":
    cdef cppclass Track:
        Track() except +
        void track_frames_batch (vector[vector[point]], vector[vector[loc_index_classified]])
        void training_track_frame (vector[point], vector[loc_index_flat_tag])
        vector[OutputBeeData] get_all_bees_data ()

cdef class PyTrack:
    cdef Track track
    def __cinit__(self):
        self.track = Track()
    def track_frames_batch(self, all_contour_locations, all_classified_loc_indexes):
        self.track.track_frames_batch(all_contour_locations, all_classified_loc_indexes)
    def training_track_frame(self, contour_locations, flat_tag_loc_indexes):
        self.track.training_track_frame(contour_locations, flat_tag_loc_indexes)
    def get_all_bees(self):
        return self.track.get_all_bees_data()
