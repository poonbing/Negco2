# Python Modules
from sqlalchemy import desc, and_
from collections import defaultdict
from datetime import datetime
import uuid
import ast
# Local Modules
from ..extensions import db
from ..models import Tracker, SessionInfo, Report


class TrackerFunctions:
    def __init__(self):
        pass

    # session operators

    def get_all_session_of_tracker(self, user_id):
        trackers = SessionInfo.query.filter_by(active_sessions=user_id).all()
        if trackers is None:
            return []
        return trackers

    def get_session_information(self, user_id, name):
        session_info = SessionInfo.query.filter(
            and_(SessionInfo.active_sessions == user_id, SessionInfo.name == name)
        ).first()
        return session_info

    def check_user_tracker_existence(self, user_id):
        session_info = SessionInfo.query.filter(SessionInfo.active_sessions == user_id).first()
        if session_info is None:
            return False
        return session_info is not None

    def check_session_information(self, user_id, name):
        session_info = SessionInfo.query.filter(
            and_(SessionInfo.active_sessions == user_id, SessionInfo.name == name)
        ).all()
        if session_info is None:
            return False
        return session_info is not None

    def create_session_information(self, user_id, name, item, rate):
        if user_id is None:
            raise ValueError("active_sessions cannot be None")
        id = str(uuid.uuid4())
        print(user_id)
        session_info = SessionInfo(id=id, active_sessions=user_id, name=name, item=item, session_id="None", session_start="None", rate=rate)
        db.session.add(session_info)
        db.session.commit()
        return id

    def start_session(self, user_id, name, session_id, start_time):
        session_info = SessionInfo.query.filter(
            and_(SessionInfo.active_sessions == user_id, SessionInfo.name == name)
        ).first()
        if session_info is None:
            return False
        session_info.session_id = session_id
        session_info.session_start = start_time
        db.session.commit()
        return "Success"

    def end_session(self, user_id, name):
        session_info = SessionInfo.query.filter(
            and_(SessionInfo.active_sessions == user_id, SessionInfo.name == name)
        ).first()
        if session_info is None:
            return False
        session_info.session_id = "None"
        session_info.session_start = "None"
        db.session.commit()

    def delete_session_information(self, user_id, name):
        session_info = SessionInfo.query.filter(
            and_(SessionInfo.active_sessions==user_id, SessionInfo.name==name)
        ).first()
        if session_info is None:
            return "Failed"
        db.session.delete(session_info)
        db.session.commit()

    def update_session_information(self, user_id, old_name, name, item, rate):
        session_info = SessionInfo.query.filter(
            and_(SessionInfo.active_sessions==user_id, SessionInfo.name==old_name)
        ).first()
        if session_info is None:
            print("Failed")
            return "Failed"
        session_info.name = name
        session_info.item = item
        session_info.rate = rate
        db.session.commit()
        return "Success"

    # tracker operators

    def get_tracker_session(self, tracker_id):
        tracker = Tracker.query.get(tracker_id)
        return tracker

    def get_all_trackers(self, user_id):
        dictionary = []
        items = self.get_all_session_of_tracker(user_id)
        for i in items:
            item = i.item
            trackers = Tracker.query.filter(and_(Tracker.user_id == user_id, Tracker.item == item)).all()
            dictionary[item] = trackers
        return dictionary

    def start_tracker(self, user_id, name, item, rate):
        old_tracker = Tracker.query.filter(and_(Tracker.user_id==user_id, Tracker.name==name, Tracker.item==item)).order_by(desc(Tracker.start_time)).first()
        if old_tracker != None:
            old_tracker.edit_token = 0
        id = str(uuid.uuid4())
        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        new_tracker = Tracker(
            id=id,
            user_id=user_id,
            name=name,
            item=item,
            rate=rate,
            start_time=current_time,
            end_time=None,
        )
        db.session.add(new_tracker)
        db.session.commit()
        return id, current_time

    def end_tracker(self, id, user_id):
        try:
            tracker = Tracker.query.get(id)
            if not tracker:
                print("Tracker not found!")
                return
            report = self.check_report(user_id, tracker.name)
            start_time = datetime.strptime(tracker.start_time, "%Y-%m-%dT%H:%M:%S")
            current_time = datetime.now()
            tracker.end_time = current_time.strftime("%Y-%m-%dT%H:%M:%S")
            total_usage = round(float(tracker.rate) / 60 * (current_time - start_time).total_seconds() / 60, 5)           
            if report:
                self.update_report(user_id, tracker.name, total_usage)
            else:
                self.create_new_report(user_id, tracker.name, tracker.item, total_usage)
            total_report = self.check_report(user_id, 'Total')
            if total_report:
                self.update_report(user_id, 'Total', total_usage)
            else:
                self.create_new_report(user_id, 'Total', 'Total', total_usage)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("An error occurred:", str(e))
            raise

    def update_report(self, user_id, name, total_usage):
        report = self.check_report(user_id, name)
        report.total_usage += total_usage
        current_day = datetime.now().day
        datapoint = list(report.datapoint)
        datapoint += [0] * (current_day - len(datapoint))
        datapoint[current_day - 1] += total_usage
        report.datapoint = datapoint

    def create_new_report(self, user_id, name, item, total_usage):
        current_month = datetime.now().strftime('%m')
        current_year = datetime.now().year
        current_day = datetime.now().day
        datapoints = [0] * current_day
        datapoints[current_day - 1] = total_usage
        goals = {
            'Total': 927.5,
            'Air Conditioning': 630,
            'Shower': 180,
            'Laundry': 20,
            'Cooking': 90,
            'Lighting': 7.5
        }
        new_report = Report(
            id=str(uuid.uuid4()),
            related_user=user_id,
            item_name=name,
            item_type=item,
            month=current_month,
            year=current_year,
            total_usage=total_usage,
            energy_goals=goals[item],
            datapoint=datapoints
        )
        db.session.add(new_report)

    def delete_tracker_record(self, user_id, tracker):
        report = self.check_report(user_id, tracker.name)
        total_report = self.check_report(user_id, 'Total')
        try:
            end_time = datetime.strptime(tracker.end_time, "%Y-%m-%dT%H:%M:%S")
            total_usage = round((float(tracker.rate)/60)*int(round((end_time - datetime.strptime(tracker.start_time, "%Y-%m-%dT%H:%M:%S")).total_seconds()/60)),5)
            end_date = end_time.day
            report.total_usage -= total_usage
            list = ast.literal_eval(report.datapoint)
            list[end_date] -= total_usage
            report.datapoint = list
            total_report.total_usage -= total_usage
            list2 = ast.literal_eval(total_report.datapoint)
            list2[end_date] -= total_usage
            total_report.datapoint = list2
        except TypeError:
            pass
        db.session.delete(tracker)
        db.session.commit()

    def check_report(self, user_id, item_name):
        month = datetime.now().month
        year = datetime.now().year
        report = Report.query.filter(
            and_(Report.related_user == user_id, Report.item_name == item_name, Report.month == month, Report.year == year)
        ).first()
        if report is None:
            return False
        return report