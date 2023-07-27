from flask import render_template, request, session

from app.report import bp
from .utils import ReportFunctions
from ..extensions import db
from ..models import Tracker, SessionInfo
from flask_login import current_user, login_required


@bp.route("/report", methods=['GET', 'POST'])
@login_required
def report():
    report_util = ReportFunctions()
    user = current_user.id
    report = report_util.check_report(user)
    if report == 'Failed':
        return render_template("error/500.html"), 500
    else:
        datapoint = report_util.retrieve_data_points(user)
        trackers = report_util.retrieve_all_tracker_records(user)
        return render_template('report/report.html', datapoints=datapoint, trackers=trackers)

