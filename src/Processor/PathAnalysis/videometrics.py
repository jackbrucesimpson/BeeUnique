

class VideoMetrics:

    def __init__(self, date_time):
        self.date_time = date_time

        self.cells_visited_speed_groups = {'all': {}, 'moving': {}, 'motionless_short': {}, 'motionless_long': {}}
        distances_per_second_window = []
        seconds_spent_in_perimeter = []
        consecutive_seconds_motionless = []
        long_stay_perimeter_coord_data = []
        
