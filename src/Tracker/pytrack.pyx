from libcpp.vector cimport vector

cdef extern from "structures.h":
    struct Point:
        float x
        float y
        int frame_num
        int classified

    struct FrameClassified:
        int frame_num
        int classified

    struct OutputBeeData:
        int class_classified
        vector[Point] path
        vector[vector[int]] flattened_28x28_tag_matrices

cdef extern from "track.h":
    cdef cppclass Track:
        Track() except +
        void track_frames_batch (vector[vector[Point]], vector[vector[int]], vector[int])
        void training_track_frame (vector[Point], vector[vector[int]], int)
        vector[OutputBeeData] get_all_bees_data ()

cdef class PyTrack:
    cdef Track track
    def __cinit__(self):
        self.track = Track()
    def track_frames_batch(self, all_contour_locations, all_contour_classifications, all_frame_nums_batch):
        self.track.track_frames_batch(all_contour_locations, all_contour_classifications, all_frame_nums_batch)
    def training_track_frame(self, contour_locations, flattened_28x28_tag_matrices, frame_num):
        self.track.training_track_frame(contour_locations, flattened_28x28_tag_matrices, frame_num)
    def get_all_bees_data(self):
        return self.track.get_all_bees_data()
