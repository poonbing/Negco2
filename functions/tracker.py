from datetime import datetime
import shelve
import uuid

class Tracker:
    def __init__(self):
        pass

    #setter & gettter

    def get_active_trackers(self, user):
        try:
            with shelve.open('user') as db:
                data = db[user]
            return data
        except:
            data = {'Air Conditioning':['Aircon', 10, None, None], 'Shower':['Shower', 10, None, None], 'Room Lights':['Lights', 10, None, None]}
            self.set_active_trackers(user, data)
            return data

    def set_active_trackers(self, user, data):
        try:
            with shelve.open('user') as db:
                db[user] = data
        except:
            data = {'Air Conditioning':['Aircon', 10, None, None], 'Shower':['Shower', 10, None, None], 'Room Lights':['Lights', 10, None, None]}
            self.set_active_trackers(user, data)

    def get_tracker_session(self, tracker_id):
        year = datetime.now().year
        month = datetime.now().strftime("%m")
        with shelve.open(f'tracker{year}{month}') as db:
            data = db[tracker_id]
        return data

    def set_tracker_session(self, tracker_id, data):
        year = datetime.now().year
        month = datetime.now().strftime("%m")
        with shelve.open(f'tracker{year}{month}') as db:
            db[tracker_id] = data

    #relative functions

    def stop_active_tracker(self, user, tracker_id):
        tracker_tray = self.get_active_trackers(user)
        for id in tracker_tray:
            if id == tracker_id:
                item = tracker_tray[id][0]
                rate = tracker_tray[id][1]
                tracker_tray[id] = [item, rate, None, None]
                self.set_active_trackers(user, tracker_tray)
                break
        print(f'{tracker_id} tracker defaulted')

    def start_active_tracker(self, user, tracker_id, session_id, rate, start_time):
        tracker_tray = self.get_active_trackers(user)
        for i in tracker_tray:
            item = tracker_tray[i][0]
            if i == tracker_id:
                tracker_tray[i] = [item, rate, session_id, start_time]
                self.set_active_trackers(user, tracker_tray)
                break
        print(f'{tracker_id} tracker started')

    def update_tracker_session(self, item, rate, user, key):
        if key == 'None':
            key = str(uuid.uuid4())
            print(key)
            current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            data = {'user':user, 'item': item,  'rate':rate,  'time_start': current_time,  'time_end': None}
            self.set_tracker_session(key, data)
            self.start_active_tracker(user, item, key, rate, current_time)
        elif key != 'None':
            current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            data = self.get_tracker_session(key)
            data['time_end'] = current_time
            self.set_tracker_session(key, data)
            self.stop_active_tracker(user, item)

