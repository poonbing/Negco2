from sqlalchemy import and_
from sqlalchemy.sql import func
from collections import defaultdict
from datetime import datetime
import uuid

# Local Modules
from ..extensions import db
from ..models import Tracker, Report

class ReportFunctions:
    def __init__(self):
        pass

    def check_report(self, user_id, item_name):
        month = datetime.now().month
        year = datetime.now().year
        report = Report.query.filter(
            and_(Report.related_user == user_id, Report.item_name == item_name, Report.month == month, Report.year == year)
        ).first()
        if report is None:
            return "Failed"
        return report
    
    def retrieve_data_points(self, user_id):
        dict = {}
        month = datetime.now().month
        year = datetime.now().year
        report = Report.query.filter(
            and_(Report.related_user == user_id, Report.month == month, Report.year == year)
        ).all()
        if report is None:
            return "Failed"
        for entry in report:
            if entry.name == 'total':
                dict['total'] = entry.datapoint
        for entry in report:
            if entry.name != 'total':
                dict[entry.name] = entry.datapoint
        return dict
    
    def retrieve_all_tracker_records(self, user_id):
        month = datetime.now().strftime('%m')
        year = str(datetime.now().year)
        dict = {}
        tracker = Tracker.query.filter(and_(Tracker.user_id==user_id, func.substring(Tracker.end_time, 1, 4)==year, func.substring(Tracker.end_time, 6, 2) == month)).all()
        for entry in tracker:
            total_usage = int(tracker.rate)*int(round((datetime.strptime(entry.end_time, "%Y-%m-%dT%H:%M:%S") - datetime.strptime(entry.start_time, "%Y-%m-%dT%H:%M:%S")).total_seconds()/60))
            dict[entry.name].append({'name':entry.name, 'start_time':entry.start_time, 'end_time':entry.end_time, 'rate':entry.rate, 'total_usgae':total_usage})
            dict['total'].append({'name':entry.name, 'start_time':entry.start_time, 'end_time':entry.end_time, 'rate':entry.rate, 'total_usgae':total_usage})
        return dict