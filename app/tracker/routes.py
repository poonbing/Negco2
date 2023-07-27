# Python Modules
from flask import render_template, request, session

# Local Modules
from app.tracker import bp
from .utils import TrackerFunctions
from ..extensions import db
from ..models import Tracker, SessionInfo, Report
from flask_login import current_user


@bp.route("/track", methods=["GET", "POST"])
def track():
    tracker = TrackerFunctions()
    user_id = current_user.id
    if "start_tracker" in request.form:  # updated
        name = request.form.get("name")
        item = request.form.get("item")
        rate = request.form.get("rate")
        key = tracker.get_session_information(user_id, name).session_id
        if key == "None":
            tracker_id, start_time = tracker.start_tracker(user_id, name, item, rate)
            tracker.start_session(user_id, name, tracker_id, start_time)
        else:
            tracker.end_session(user_id, name)
            tracker.end_tracker(key, user_id)
        timers = tracker.get_all_session_of_tracker(user_id)
        return render_template("tracker/tracker.html", keylist=timers)
    if "item_form" in request.form:  # updated
        index = request.form.get("item_index")
        item = request.form.get("new_item")
        rate = request.form.get("new_rate")
        name = request.form.get("new_name")
        method = request.form.get("form_action")
        if method == "update":
            tracker.update_session_information(user_id, index, name, item, rate)
        elif method == "create":
            tracker.create_session_information(user_id, name, item, rate)
        timers = tracker.get_all_session_of_tracker(user_id)
        return render_template("tracker/tracker.html", keylist=timers)
    if "delete" in request.form:  # updated
        index = request.form.get("index")
        tracker.delete_session_information(user_id, index)
        timers = tracker.get_all_session_of_tracker(user_id)
        return render_template("tracker/tracker.html", keylist=timers)
    else:  # updated
        print(user_id)
        if tracker.check_user_tracker_existence(user_id) is False:
            print(user_id)
            tracker.create_session_information(user_id, "Guest Shower", "Shower", 1500)
            tracker.create_session_information(user_id, "Room Air Con", "Air Conditioning", 2500)
            tracker.create_session_information(user_id, "LED Lights", "LED Light", 10)
        timers = tracker.get_all_session_of_tracker(user_id)
        return render_template("tracker/tracker.html", keylist=timers)
