from sqlalchemy import and_
from sqlalchemy.sql import func
from datetime import datetime
import random
# Local Modules
from ..extensions import db
from ..models import Tracker, Report, Report_Reviews

class ReportFunctions:
    def __init__(self):
        pass

    def check_report(self, user_id):
        month = datetime.now().month
        year = datetime.now().year
        report = Report.query.filter(
            and_(Report.related_user == user_id, Report.month == month, Report.year == year)
        ).first()
        if report is None:
            return "Failed"
        return report
    
    def find_report(self, user_id, item_name):
        month = datetime.now().month
        year = datetime.now().year
        report = Report.query.filter(
            and_(Report.related_user == user_id, Report.item_name == item_name, Report.month == month, Report.year == year)
        ).first()
        if report is None:
            return False
        return report
    
    def retrieve_data_points(self, user_id):
        list = []
        list2 = []
        month = datetime.now().month
        year = datetime.now().year
        report = Report.query.filter(
            and_(Report.related_user == user_id, Report.month == month, Report.year == year)
        ).all()
        if report is None:
            return "Failed"
        for entry in report:
            if entry.item_name != 'Total':
                list.append(entry.datapoint)
                list2.append(entry.item_name)
        return list, list2
    
    def retrieve_all_tracker_records(self, user_id):
        month = datetime.now().strftime('%m')
        year = str(datetime.now().year)
        dict = {}
        tracker = Tracker.query.filter(and_(Tracker.user_id==user_id, func.substring(Tracker.end_time, 1, 4)==year, func.substring(Tracker.end_time, 6, 2) == month)).all()
        for entry in tracker:
            timer = int(round((datetime.strptime(entry.end_time, "%Y-%m-%dT%H:%M:%S") - datetime.strptime(entry.start_time, "%Y-%m-%dT%H:%M:%S")).total_seconds()/60))
            total_usage = (float(entry.rate)/60)*timer
            try:
                dict[entry.name].append({'id': entry.id, 'name':entry.name, 'item':entry.item, 'use_time':timer, 'rate':entry.rate, 'total_usage':total_usage, 'start_time':entry.start_time, 'end_time':entry.end_time, 'edit_token':entry.edit_token})
            except:
                dict[entry.name] = [{'id': entry.id, 'name':entry.name, 'item':entry.item, 'use_time':timer, 'rate':entry.rate, 'total_usage':total_usage, 'start_time':entry.start_time, 'end_time':entry.end_time, 'edit_token':entry.edit_token}]
            try:
                dict['total'].append({'id': entry.id, 'name':entry.name, 'item':entry.item, 'use_time':timer, 'rate':entry.rate, 'total_usage':total_usage, 'start_time':entry.start_time, 'end_time':entry.end_time, 'edit_token':entry.edit_token})
            except:
                dict['total'] = [{'id': entry.id, 'name':entry.name, 'item':entry.item, 'use_time':timer, 'rate':entry.rate, 'total_usage':total_usage, 'start_time':entry.start_time, 'end_time':entry.end_time, 'edit_token':entry.edit_token}]
        return dict
    
    def edit_tracker_record(self, user, name, item, start_time, new_end_time):
        tracker_record = Tracker.query.filter(and_(Tracker.user_id==user, Tracker.name==name, Tracker.item==item, Tracker.start_time==start_time)).first()
        if tracker_record is None:
            return 'Failed'
        elif tracker_record.edit_token == 0:
            return 'Failed'
        tracker_record.edit_token = 0
        old_end_time = datetime.strptime(tracker_record.end_time, "%Y-%m-%dT%H:%M:%S")
        tracker_record.end_time = new_end_time
        new_end_time = datetime.strptime(new_end_time, "%Y-%m-%dT%H:%M:%S")
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
        print(old_end_time)
        old_usage = (float(tracker_record.rate)/60)*int(round((old_end_time - start_time).total_seconds()/60))
        new_usage = (float(tracker_record.rate)/60)*int(round((new_end_time - start_time).total_seconds()/60))
        print(old_usage, new_usage)
        self.update_old_report(user, name, old_usage, old_end_time.day)
        self.update_new_report(user, name, new_usage, new_end_time.day)
        db.session.commit()
        return tracker_record.id
    
    def update_old_report(self, user_id, name, total_usage, date):
        report = self.find_report(user_id, name)
        total_usage2 = total_usage + report.total_usage
        report.total_usage = total_usage2
        datapoint = list(report.datapoint)
        datapoint += [0] * (int(date) - len(datapoint))
        datapoint[int(datetime.now().day) - 1] -= total_usage
        report.datapoint = datapoint
        db.session.commit()
    
    def update_new_report(self, user_id, name, total_usage, date):
        report = self.find_report(user_id, name)
        total_usage2 = total_usage + report.total_usage
        report.total_usage = total_usage2
        datapoint = list(report.datapoint)
        datapoint += [0] * (int(date) - len(datapoint))
        datapoint[int(datetime.now().day) - 1] += total_usage
        report.datapoint = datapoint
        db.session.commit()

    def replace_position(self, items, item):
        items.append(item)
        items.sort(key=lambda x: x[1], reverse=True)
        return items[:3]

    def generate_review(self, user_id):
        all_reports = Report.query.filter(Report.related_user==user_id).all()
        top_items = []
        for report in all_reports:
            if report.item_type != 'Total':
                item = [report.item_type, report.total_usage]
                top_items = self.replace_position(top_items, item)
        ordinal = {0: '', 1: 'second', 2: 'third'}
        output = []
        for index, item in enumerate(top_items):
            review = Report_Reviews.query.filter(Report_Reviews.item_type==item[0]).first()
            if review:
                suggestions = [review.suggestion1, review.suggestion2, review.suggestion3]
                suggestions.pop(random.randint(0, 2))
                review_text = f"""Item {item[0]}'s Energy Usage Currently is the {ordinal[index]} highest, at {item[1]} kWh (KiloWatt/Hour). 
                                <br>Here are some ways to improve on your energy usage:
                                <br>1. {suggestions[0]}
                                <br>2. {suggestions[1]}"""
                output.append(review_text)
        return output
                