from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func, ForeignKey, create_engine, ARRAY
from sqlalchemy.orm import sessionmaker, relationship
import uuid
from collections import defaultdict
import calendar

app = Flask('__main__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Negco_Admin:Forehead_Gang@it2555.mysql.database.azure.com/tracker'
engine = create_engine("mysql+pymysql://Negco_Admin:Forehead_Gang@it2555.mysql.database.azure.com/tracker", echo=True)
Session = sessionmaker(bind=engine)
db_session = Session()
db = SQLAlchemy(app)

class Tracker(db.Model):
    __tablename__ = 'tracker'
    #sql model
    id = db.Column(db.String(36), primary_key = True, unique = True)
    user_id = db.Column(db.String(36), nullable = False, unique = True)
    # user_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    # user = db.relationship('User', backref = db.backref('tracker', lazy = True))
    name = db.Column(db.String(20), nullable = False)
    type = db.Column(db.String(20), nullable = False)
    rate = db.Column(db.FLOAT(7,4), nullable = False)
    start_time = db.Column(db.DateTime, nullable = False)
    end_time = db.Column(db.DateTime)

    def __init__(self, id, user, item, rate, start_time, end_time):
        self.id = id
        self.user = user
        self.item = item
        self.rate = rate
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            'id': self.id,
            'user_id':self.user_id,
            'item': self.item,
            'rate': self.rate,
            'start_time': self.start_time,
            'end_time': self.end_time
        }

class SessionTracker(db.Model):
    __tablename__ = 'session_tracker'
    #sql model
    user_id = db.Column(db.String(36), primary_key = True)
    active_sessions = db.Column(ARRAY(db.String), nullable = False)

    def __init__(self, user_id, session_info=None):
        self.user_id = user_id
        self.session_info = session_info or []

    def add_session_info(self, data):
        self.session_info.append(data)
    
    def to_dict(self):
        return {
            'user_id':self.user_id,
            'active_session':self.active_sessions
        }

class SessionInfo:
    def __init__(self, name, item, session_id, session_start, rate):
        self.name = name
        self.item = item
        self.session_id = session_id
        self.session_start = session_start
        self.rate = rate

    def to_dict(self):
        return{
            'name': self.name,
            'item': self.item,
            'session_id': self.session_id,
            'session_start':self.session_start,
            'rate':self.rate
        }
class TrackerFunctions:
    def __init__(self):
        pass

    # session operators
    def get_session_tracker(self, user_id):
        sessions = SessionTracker.query.get(user_id)
        return sessions.to_dict()

    def get_all_session_of_tracker(self, user_id):
        trackers = SessionTracker.query.get(user_id)
        if trackers is None:
            return []
        session_entries = trackers.active_sessions.all()
        return session_entries

    def check_for_session_tracker(self, user_id):
        session_tracker = SessionTracker.query.filter_by(user_id=user_id).first()
        return session_tracker is not None

    def create_session_tracker(self, user_id):
        new_session = SessionTracker(user_id)
        db.session.add(new_session)
        db.session.commit()
        return new_session
    
    def check_session_information(self, user_id, name):
        session_tracker = SessionTracker.query.get(user_id)
        if session_tracker is None:
            return False
        session_info = session_tracker.active_sessions.filter_by(name=name).first()
        return session_info is not None

    def create_session_information(self, user_id, name, item, rate):
        session_info = SessionInfo(name, item, None, None, rate)
        session_tracker = SessionTracker.query.get(user_id)
        session_tracker.active_sessions.append(session_info)
        db.session.commit()
        return session_info
    
    def start_session(self, user_id, name, session_id, start_time):
        session_tracker = SessionTracker.query.get(user_id)
        if session_tracker is None:
            return False
        session_info = session_tracker.active_sessions.filter_by(name=name).first()
        session_info.session_id = session_id
        session_info.start_time = start_time
        db.session.commit()

    def end_session(self, user_id, name):
        session_tracker = SessionTracker.query.get(user_id)
        if session_tracker is None:
            return False
        session_info = session_tracker.active_sessions.filter_by(name=name).first()
        session_info.session_id = None
        session_info.start_time = None
        db.session.commit()

    def delete_session_information(self, user_id, name):
        session_tracker = SessionTracker.query.get(user_id)
        if session_tracker is None:
            return 'Failed'
        session_info = session_tracker.active_sessions.filter_by(name=name).first()
        if session_info is None:
            return 'Failed'
        db.session.delete(session_info)
        db.session.commit()

    def update_session_information(self, user_id, old_name, name, item, rate):
        sessiontracker = SessionTracker.query.get(user_id)
        if sessiontracker is None:
            return 'Failed'
        session_info = sessiontracker.active_sessions.filter_by(name=old_name).first()
        if session_info is None:
            return 'Failed'
        session_info.name = name
        session_info.item = item
        session_info.rate = rate
        db.session.commit()
        return 'Success'
    #tracker operators

    def get_tracker_session(self, tracker_id):
        tracker = Tracker.query.get(tracker_id)
        return tracker

    def start_tracker(self, user, item, rate):
        id = uuid.uuid4()
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        new_tracker = Tracker(id, user, item, rate, current_time, None)
        db.session.add(new_tracker)
        db.session.commit()
        return id, current_time

    def end_tracker(self, id):
        tracker = Tracker.query.get(id)
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        tracker.end_time = current_time
        db.session.commit()

    def delete_tracker_record(self, tracker):
        db.session.delete(tracker)
        db.session.commit

    # report generation

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
        trackers = Tracker.filter_by(user_id=user_id).all()
        items = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        for tracker in trackers:
            usetime = self.calculate_time_difference(tracker.start_time, tracker.end_time)
            usage = self.calculate_usage(tracker.rate, usetime)
            date = tracker.start_time[0:10]
            items[date][tracker.item]['duration'] += usetime
            items[date][tracker.item]['usage'] += usage
            items[date]['total']['duration'] += usetime
            items[date]['total']['usage'] += usage
        return items
    
    def generate_datapoints(self, list):
        x_axis = []
        y_axis = []
        total = 0
        for i in list:
            total += list[i]['total']['usage']
            y_axis.append(total)
            x_axis.append(i)
        return x_axis, y_axis
    
