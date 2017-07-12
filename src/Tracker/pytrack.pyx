from libcpp.vector cimport vector

cdef extern from "structures.h":
    struct PointXY:
        float x
        float y

    struct OutputBeeData:
        vector[PointXY] xy
        vector[int] frame_nums
        vector[vector[int]] flattened_28x28_tag_matrices

cdef extern from "track.h":
    cdef cppclass Track:
        Track() except +
        void track_frame (vector[PointXY], vector[vector[int]], int)
        vector[OutputBeeData] get_all_bees_data ()

cdef class PyTrack:
    cdef Track track
    def __cinit__(self):
        self.track = Track()
    def track_frame(self, contour_locations, flattened_28x28_tag_matrices, frame_num):
        self.track.track_frame(contour_locations, flattened_28x28_tag_matrices, frame_num)
    def get_all_bees_data(self):
        return self.track.get_all_bees_data()
