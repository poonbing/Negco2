# Python Modules
from flask import render_template, request, session

# Local Modules
from app.tracker import bp
from .utils import TrackerFunctions


@bp.route("/track", methods=["GET", "POST"])
def track():
    tracker = TrackerFunctions()
    try:
        user = session["user"]
        print(user)
    except:  # updated
        user = request.form.get("user_id")
        session["user"] = user
        if tracker.check_for_session_tracker(user) is False:
            tracker.create_session_tracker(user)
            tracker.create_session_information(user, "Guest Shower", "Shower", 1500)
            tracker.create_session_information(
                user, "Room Air Con", "Air Conditioning", 2500
            )
            tracker.create_session_information(user, "LED Lights", "LED Light", 10)
        timers = tracker.get_all_session_of_tracker(user)
        print(timers, user)
        return render_template("tracker.html", keylist=timers)
    if "start_tracker" in request.form:  # updated
        user = session["user"]
        name = request.form.get("name")
        item = request.form.get("item")
        rate = request.form.get("rate")
        key = tracker.get_session_information(user, name).session_id
        if key == "None":
            tracker_id, start_time = tracker.start_tracker(user, name, item, rate)
            tracker.start_session(user, name, tracker_id, start_time)
        else:
            tracker.end_session(user, name)
            tracker.end_tracker(key)
        timers = tracker.get_all_session_of_tracker(user)
        return render_template("tracker.html", keylist=timers)
    if "item_form" in request.form:  # updated
        index = request.form.get("item_index")
        item = request.form.get("new_item")
        rate = request.form.get("new_rate")
        name = request.form.get("new_name")
        method = request.form.get("form_action")
        if method == "update":
            tracker.update_session_information(user, index, name, item, rate)
        elif method == "create":
            tracker.create_session_information(user, name, item, rate)
        timers = tracker.get_all_session_of_tracker(user)
        return render_template("tracker.html", keylist=timers)
    if "delete" in request.form:  # updated
        index = request.form.get("index")
        tracker.delete_session_information(user, index)
        timers = tracker.get_all_session_of_tracker(user)
        return render_template("tracker.html", keylist=timers)
    else:  # updated
        timers = tracker.get_all_session_of_tracker(user)
        return render_template("tracker.html", keylist=timers)
