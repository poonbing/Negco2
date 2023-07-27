# Python Modules
from sqlalchemy import and_
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
            and_(SessionInfo.active_sessions == user_id, SessionInfo.name == name)
        ).first()
        if session_info is None:
            return "Failed"
        db.session.delete(session_info)
        db.session.commit()

    def update_session_information(self, user_id, old_name, name, item, rate):
        session_info = SessionInfo.query.filter(
            and_(SessionInfo.active_sessions == user_id, SessionInfo.name == old_name)
        ).first()
        if session_info is None:
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
        report = self.check_report(user_id, tracker.name)
        total_report = self.check_report(user_id, 'total')
        tracker = Tracker.query.get(id)
        current_date = int(datetime.now().day)
        start_time = datetime.strptime(tracker.start_time, "%Y-%m-%dT%H:%M:%S")
        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        tracker.end_time = current_time
        current_time = datetime.strptime(current_time, "%Y-%m-%dT%H:%M:%S")
        total_usage = int(tracker.rate)*int(round((current_time - start_time).total_seconds()/60))
        if report != "Failed":
            report.total_usage += total_usage
            list = ast.literal_eval(report.datapoint)
            if len(list) < current_date:
                list.append(total_usage)
            elif len(list) >= current_date:
                list[current_date] += total_usage
            report.datapoint = list
            total_report.total_usage += total_usage
            list2 = ast.literal_eval(total_report.datapoint)
            if len(list2) < current_date:
                list2.append(total_usage)
            elif len(list2) >= current_date:
                list2[current_date] += total_usage
            total_report.datapoint = list2
        else:
            current_month = datetime.now().strftime('%m')
            current_year = datetime.now().year
            list = []
            for i in range(current_date):
                list.append(0)
            list[current_date] += total_usage
            new_report = Report(id=str(uuid.uuid4()), related_user=user_id, item_name=tracker.name, month=current_month, year=current_year, total_usage=total_usage, energy_goals=53160, datapoint=list)
            db.session.add(new_report)
            total_report = Report(id=str(uuid.uuid4()), related_user=user_id, item_name='total', month=current_month, year=current_year, total_usage=total_usage, energy_goals=53160, datapoint=list)
            db.session.add(total_report)
        db.session.commit()

    def delete_tracker_record(self, user_id, tracker):
        report = self.check_report(user_id, tracker.name)
        total_report = self.check_report(user_id, 'total')
        try:
            end_time = datetime.strptime(tracker.end_time, "%Y-%m-%dT%H:%M:%S")
            total_usage = int(tracker.rate)*int(round((end_time - datetime.strptime(tracker.start_time, "%Y-%m-%dT%H:%M:%S")).total_seconds()/60))
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
        db.session.commit

    def check_report(self, user_id, item_name):
        month = datetime.now().month
        year = datetime.now().year
        report = Report.query.filter(
            and_(Report.related_user == user_id, Report.item_name == item_name, Report.month == month, Report.year == year)
        ).first()
        if report is None:
            return "Failed"
        return report