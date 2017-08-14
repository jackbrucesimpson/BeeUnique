from libcpp.vector cimport vector

cdef extern from "structures.h":
    struct outputbeedata:
        vector[float] x_path
        vector[float] y_path
        vector[int] frame_nums
        vector[int] tag_matrix_indices

cdef extern from "track.h":
    cdef cppclass Track:
        Track() except +
        void track_video (vector[int], vector[vector[float]], vector[vector[float]])
        vector[outputbeedata] get_all_bees_data ()

cdef class PyTrack:
    cdef Track track
    def __cinit__(self):
        self.track = Track ()
    def track_video(self, frame_nums, x_grouped_by_frame, y_grouped_by_frame):
        self.track.track_video (frame_nums, x_grouped_by_frame, y_grouped_by_frame)
    def get_all_bees_data(self):
        return self.track.get_all_bees_data ()
