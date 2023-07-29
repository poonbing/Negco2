# Python Modules
from flask import render_template, request, session, current_app
from flask_login import current_user, login_required
from app import limiter
# Local Modules
from app.report import bp
from .utils import ReportFunctions
from flask_login import current_user, login_required



@bp.route("/tracker_report", methods=['GET', 'POST'])
@login_required
@limiter.limit('2/second')
def report():
    report_util = ReportFunctions()
    user = current_user.id
    print(user)
    report = report_util.check_report(user)
    print(report)
    if report == 'Failed':
        return render_template("error/500.html"), 500
    else:
        datapoint = report_util.retrieve_data_points(user)
        print(datapoint)
        trackers = report_util.retrieve_all_tracker_records(user)
        print(trackers)
        return render_template('report/report.html', datapoints=datapoint, trackers=trackers)

