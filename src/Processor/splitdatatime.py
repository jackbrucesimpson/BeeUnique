class SplitDataTime():
    def __init__(self):
        self.video_dt_data = []

    def add_date_time_data(self, date_time, data):
        self.video_dt_data.append({'date_time': date_time, 'data': data})

    def sort_data_into_time_period(self):
        video_dt_data_sorted = sorted(self.video_dt_data, key=lambda k: k['date_time'])

        is_night = True
        night_hours = [19, 20, 21, 22, 23, 0, 1, 2, 3, 4, 5, 6]

        current_data_list = []
        night_data_lists = []
        day_data_lists = []
        for dt_data in video_dt_data_sorted:
            hour = dt_data['date_time'].hour
            hour_data = dt_data['data']
            if is_night:
                if hour in night_hours:
                    current_data_list.append(hour_data)
                else:
                    night_data_lists.append(current_data_list)
                    current_data_list = [hour_data]
                    is_night = False
            else:
                if hour not in night_hours:
                    current_data_list.append(hour_data)
                else:
                    day_data_lists.append(current_data_list)
                    current_data_list = [hour_data]
                    is_night = True

        if len(current_data_list) > 0:
            if is_night:
                night_data_lists.append(current_data_list)
            else:
                day_data_lists.append(current_data_list)
            current_data_list = []

        return {'night': night_data_lists, 'day': day_data_lists}
