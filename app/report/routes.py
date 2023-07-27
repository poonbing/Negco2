from flask import render_template, request, session

from app.report import bp
from .utils import ReportFunctions
from ..extensions import db
from ..models import Tracker, SessionInfo
from flask_login import current_user, login_required


@bp.route("/report", methods=['GET', 'POST'])
@login_required
def report():
    user = current_user.id
    
    return render_template('report/report.html')

