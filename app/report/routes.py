# Python Modules
from flask import render_template, request, session, current_app, url_for, redirect, flash
from flask_login import current_user, login_required
from app import limiter
from flask_wtf.csrf import generate_csrf
# Local Modules
from app.report import bp
from .utils import ReportFunctions
from ..forms import TrackerRecordEdit
from flask_login import current_user, login_required
import json
from datetime import datetime
import calendar



@bp.route("/tracker_report", methods=['GET', 'POST'])
@login_required
@limiter.limit('4/second')
def report():
    form = TrackerRecordEdit()
    csrf_token = generate_csrf()
    report_util = ReportFunctions()
    user = current_user.id
    if form.validate_on_submit():
        name = form.name.data
        item = form.item.data
        start_time = form.starttime.data
        new_end_time = form.newendtime.data
        reply = report_util.edit_tracker_record(user, name, item, start_time, new_end_time)
        if reply == 'Failed':
            flash('Tracker Record cannot be edited!', 'error')
            return redirect(url_for('report.report'))
        return redirect(url_for('report.report'))
    else:
        report = report_util.check_report(user)
        if report == 'Failed':
            flash('Report not found as there are no records of tracker use. \n Please use the tracker first before using report ;)', 'error')
            return redirect(url_for('tracker.track'))
        else:
            datapoint, list_names = report_util.retrieve_data_points(user)
            nested_list = []
            for lists in datapoint:
                nested_list.append(lists)
            nested_json_list = json.dumps(nested_list)
            nested_json_name = json.dumps(list_names)
            num_days = calendar.monthrange(datetime.now().year, datetime.now().month)[1]
            trackers = report_util.retrieve_all_tracker_records(user)
            print(list_names)
            return render_template('report/report.html',
                                    form=form,
                                    csrf_token=csrf_token,
                                    names = list_names,
                                    datapoints=nested_json_list,
                                    name_list=nested_json_name,
                                    n=len(list_names),
                                    trackers=trackers,
                                    num_days=num_days,
                                    target=report.energy_goals)