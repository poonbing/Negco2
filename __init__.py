import os
from flask import Flask, render_template, redirect, url_for, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func, ForeignKey, create_engine, ARRAY, and_
from sqlalchemy.orm import sessionmaker, relationship
from collections import defaultdict
from datetime import datetime
import uuid



app = Flask(__name__)
app.config['SECRET_KEY'] = 'app security project'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Negco_Admin:Forehead_Gang@it2555.mysql.database.azure.com/tracker'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
# engine = create_engine("mysql+pymysql://Negco_Admin:Forehead_Gang@it2555.mysql.database.azure.com/tracker", echo=True)
# Session = sessionmaker(bind=engine)
# db_session = Session()
Session(app)
db = SQLAlchemy(app)



class Tracker(db.Model):
    __tablename__ = 'tracker'
    #sql model
    id = db.Column(db.String(36), primary_key = True, unique = True)
    user_id = db.Column(db.String(36), nullable = False)
    name = db.Column(db.String(45), nullable = False)
    item = db.Column(db.String(45), nullable = False)
    rate = db.Column(db.INTEGER, nullable = False)
    start_time = db.Column(db.String(20), nullable = False)
    end_time = db.Column(db.String(20))

    def __init__(self, id, user_id, name, item, rate, start_time, end_time):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.item = item
        self.rate = rate
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'item': self.item,
            'rate': self.rate,
            'start_time': self.start_time,
            'end_time': self.end_time
        }

class SessionTracker(db.Model):
    __tablename__ = 'session_tracker'
    #sql model
    user_id = db.Column(db.String(36), primary_key = True, unique = True)
    active_sessions = relationship('SessionInfo', backref='session_tracker')

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

class SessionInfo(db.Model):
    __tablename__ = 'session_info'

    id = db.Column(db.String(36), primary_key = True, unique = True)
    active_sessions = db.Column(db.String(45), ForeignKey('session_tracker.user_id'))
    name = db.Column(db.String(45), nullable = False)
    item = db.Column(db.String(45), nullable = False)
    session_id = db.Column(db.String(36), nullable = False)
    session_start = db.Column(db.String(20))
    rate = db.Column(db.INTEGER, nullable = False)

    def __init__(self, id, user_id, name, item, session_id, session_start, rate):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.item = item
        self.session_id = session_id
        self.session_start = session_start
        self.rate = rate

    def to_dict(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
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
        trackers = SessionInfo.query.filter_by(active_sessions=user_id).all()
        if trackers is None:
            return []
        return trackers

    def check_for_session_tracker(self, user_id):
        session_tracker = SessionTracker.query.filter_by(user_id=user_id).first()
        return session_tracker is not None

    def create_session_tracker(self, user_id):
        new_session = SessionTracker(user_id)
        db.session.add(new_session)
        db.session.commit()
        return new_session

    def get_session_information(self, user_id, name):
        session_info = SessionInfo.query.filter(and_(SessionInfo.active_sessions == user_id, SessionInfo.name == name)).first()
        return session_info

    def check_session_information(self, user_id, name):
        session_info = SessionInfo.query.filter(and_(SessionInfo.active_sessions == user_id, SessionInfo.name == name)).all()
        if session_info is None:
            return False
        return session_info is not None

    def create_session_information(self, user_id, name, item, rate):
        id = str(uuid.uuid4())
        session_info = SessionInfo(id, user_id, name, item, 'None', 'None', rate)
        session_tracker = SessionTracker.query.get(user_id)
        session_tracker.active_sessions.append(session_info)
        db.session.add(session_info)
        db.session.commit()
        return id
    
    def start_session(self, user_id, name, session_id, start_time):
        session_tracker = SessionTracker.query.get(user_id)
        if session_tracker is None:
            return False
        session_info = SessionInfo.query.filter(and_(SessionInfo.active_sessions == user_id, SessionInfo.name == name)).first()
        session_info.session_id = session_id
        session_info.session_start = start_time
        db.session.commit()
        return 'Success'

    def end_session(self, user_id, name):
        session_tracker = SessionTracker.query.get(user_id)
        if session_tracker is None:
            return False
        session_info = SessionInfo.query.filter(and_(SessionInfo.active_sessions == user_id, SessionInfo.name == name)).first()
        session_info.session_id = 'None'
        session_info.session_start = 'None'
        db.session.commit()

    def delete_session_information(self, user_id, name):
        session_info = SessionInfo.query.filter(and_(SessionInfo.active_sessions == user_id, SessionInfo.name == name)).first()
        if session_info is None:
            return 'Failed'
        db.session.delete(session_info)
        db.session.commit()

    def update_session_information(self, user_id, old_name, name, item, rate):
        sessiontracker = SessionTracker.query.get(user_id)
        if sessiontracker is None:
            return 'Failed'
        session_info = SessionInfo.query.filter(and_(SessionInfo.active_sessions == user_id, SessionInfo.name == old_name)).first()
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

    def start_tracker(self, user_id, name, item, rate):
        id = str(uuid.uuid4())
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        new_tracker = Tracker(id=id, user_id=user_id, name=name, item=item, rate=rate, start_time=current_time, end_time=None)
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
        return formatted_difference, time_difference.seconds
    
    def calculate_usage(self, rate, time):
        format_string = '%H:%M:%S'
        duration = datetime.strptime(time, format_string)-datetime.strptime("0", "%H")
        hours = duration.total_seconds() % 60
        total = int(float(rate)*hours)
        return total
    
    def generate_report(self, user_id):
        trackers = Tracker.query.filter_by(user_id=user_id).all()
        items = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        for tracker in trackers:
            time, usetime = self.calculate_time_difference(tracker.start_time, tracker.end_time)
            usage = self.calculate_usage(tracker.rate, time)
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
            y_axis.append(str(total))
            x_axis.append(i)
        return x_axis, y_axis



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        session.pop('user', None)
        print(TrackerFunctions().get_all_session_of_tracker('1'))
        return render_template('index.html')


@app.route('/track', methods=['GET', 'POST'])
def track():
    tracker = TrackerFunctions()
    try:
        user = session['user']
        print(user)
    except: #updated
        user = request.form.get('user_id')
        session['user'] = user
        if tracker.check_for_session_tracker(user) is False:
            tracker.create_session_tracker(user)
            tracker.create_session_information(user, 'Guest Shower', 'Shower', 1500)
            tracker.create_session_information(user, 'Room Air Con', 'Air Conditioning', 2500)
            tracker.create_session_information(user, 'LED Lights', 'LED Light', 10)
        timers = tracker.get_all_session_of_tracker(user)
        print(timers, user)
        return render_template('tracker.html', keylist=timers)
    if 'start_tracker' in request.form: #updated
        user = session['user']
        name = request.form.get('name')
        item = request.form.get('item')
        rate = request.form.get('rate')
        key = tracker.get_session_information(user, name).session_id
        if key == 'None':
            tracker_id, start_time = tracker.start_tracker(user, name, item, rate)
            tracker.start_session(user, name, tracker_id, start_time)
        else:
            tracker.end_session(user, name)
            tracker.end_tracker(key)
        timers = tracker.get_all_session_of_tracker(user)
        return render_template('tracker.html', keylist=timers)
    if 'item_form' in request.form: #updated
        index = request.form.get('item_index')
        item = request.form.get('new_item')
        rate = int(request.form.get('new_rate'))
        name = request.form.get('new_name')
        method = request.form.get('form_action')
        if method == 'update':
            tracker.update_session_information(user, index, name, item, rate)
        elif method == 'create':
            tracker.create_session_information(user, name, item, rate)
        timers = tracker.get_all_session_of_tracker(user)
        return render_template('tracker.html', keylist=timers)
    if 'delete' in request.form: #updated
        index = request.form.get('index')
        tracker.delete_session_information(user, index)
        timers = tracker.get_all_session_of_tracker(user)
        return render_template('tracker.html', keylist=timers)
    else: #updated
        timers = tracker.get_all_session_of_tracker(user)
        return render_template('tracker.html', keylist=timers)


@app.route('/report', methods=['GET', 'POST'])
def generate_report(): #updated
    report = TrackerFunctions()
    if request.method == 'POST':
        user = session['user']
        items = report.generate_report(user)
        x_axis, y_axis = report.generate_datapoints(items)
        for date in items:
            split_total = items[date].pop('total')
        print(x_axis)
        print(y_axis)
        return render_template('report.html', list=items, total=split_total, x=x_axis, y=y_axis)


if __name__ == '__main__':
    app.run(debug=True)
