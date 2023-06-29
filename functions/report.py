from datetime import datetime
import calendar
import shelve
from .tracker import TrackerFunctions, Tracker, SessionInfo, SessionTracker

class Report:
    def __init__(self):
        pass

    #relative functions

    def calculate_time_difference(self, start_time, end_time):
        format_string = '%Y-%m-%dT%H:%M:%S'
        start_datetime = datetime.strptime(start_time, format_string)
        end_datetime = datetime.strptime(end_time, format_string)
        time_difference = end_datetime - start_datetime
        hours = time_difference.seconds // 3600
        minutes = (time_difference.seconds % 3600) // 60
        seconds = time_difference.seconds % 60
        formatted_difference = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        return formatted_difference
    
    def calculate_usage(self, rate, time):
        format_string = '%H:%M:%S'
        duration = datetime.strptime(time, format_string)-datetime.strptime("0", "%H")
        hours = duration.total_seconds() % 60
        total = int(float(rate)*hours)
        return total
    
    def generate_report(self, user_id):
        trackers = Tracker.filter_by(user_id=user_id)
        # with shelve.open(f'tracker{year}{month}') as db:
        #     for i in db:
        #         if db[i]['user'] == user:
        #             usetime = self.calculate_time_difference(db[i]['time_start'], db[i]['time_end'])
        #             usage = self.calculate_usage(db[i]['rate'], usetime)
        #             date = db[i]['time_start'][0:10]
        #             dict = {
        #                 'item':db[i]['item'],
        #                 'date':date,
        #                 'duration':usetime,
        #                 'usage':usage
        #             }
        #             items.append(dict)
        return items
    
    def generate_datapoints(self, list):
        x_axis = []
        y_axis = []
        total = 0
        year = datetime.now().year
        month = datetime.now().strftime("%m")
        current_date = datetime.now().strftime("%d")
        num_days = calendar.monthrange(year, int(month))[1]
        for i in range(1, num_days+1):
            if i <= int(current_date):
                records = list
                count = 0
                for record in records:
                    if int(record['date'][8:10]) == int(i):
                        total += int(record['usage'])
                        list.pop(count)
                    else:
                        count += 1
                y_axis.append(total)
            date = int(f'{i:02d}')
            x_axis.append(int(date))
        return x_axis, y_axis
    
        
