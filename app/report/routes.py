# Python Modules
from flask import render_template, request, session, current_app
from flask_login import current_user, login_required
from app import limiter
# Local Modules
from app.report import bp
from .utils import ReportFunctions
from flask_login import current_user, login_required
import json
from datetime import datetime
import calendar



@bp.route("/tracker_report", methods=['GET', 'POST'])
@login_required
@limiter.limit('2/second')
def report():
    report_util = ReportFunctions()
    user = current_user.id
    report = report_util.check_report(user)
    if report == 'Failed':
        return render_template("error/500.html"), 500
    else:
        datapoint, list_names = report_util.retrieve_data_points(user)
        nested_list = []
        for lists in datapoint:
            nested_list.append(lists)
        nested_json_list = json.dumps(nested_list)
        nested_json_name = json.dumps(list_names)
        num_days = calendar.monthrange(datetime.now().year, datetime.now().month)[1]
        trackers = report_util.retrieve_all_tracker_records(user)
        return render_template('report/report.html', datapoints=nested_json_list, name_list=nested_json_name, n=len(list_names), trackers=trackers, num_days=num_days, target=report.energy_goals)

