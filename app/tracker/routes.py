# Python Modules
from flask import render_template, request, redirect, url_for, current_app, flash
from flask_login import current_user, login_required
from app import limiter
from flask_wtf.csrf import generate_csrf
# Local Modules
from app.tracker import bp
from .utils import TrackerFunctions
from ..forms import TrackerInteract



@bp.route("/track", methods=["GET", "POST"])
@login_required
@limiter.limit('2/second')
def track():
    tracker = TrackerFunctions()
    user_id = current_user.id
    form = TrackerInteract()
    csrf_token = generate_csrf()
    try:
        if form.action.data == 'start':
            name = form.name.data
            item = form.item.data[1:-1]
            rate = form.rate.data
            key = tracker.get_session_information(user_id, name).session_id
            if key == "None":
                tracker_id, start_time = tracker.start_tracker(user_id, name, item, rate)
                tracker.start_session(user_id, name, tracker_id, start_time)
            else:
                tracker.end_session(user_id, name)
                tracker.end_tracker(key, user_id)
            return redirect(url_for('tracker.track'))
        elif form.action.data == 'edit':
            name = form.name.data
            item = form.item.data[1:-1]
            rate = form.rate.data
            old_name = form.old_name.data
            old_item = form.old_item.data
            tracker.update_session_information(user_id, old_name, name, item, rate)
            return redirect(url_for('tracker.track'))
        elif form.action.data == 'create':
            name = form.name.data
            item = form.item.data[1:-1]
            rate = form.rate.data
            tracker.create_session_information(user_id, name, item, rate)
            return redirect(url_for('tracker.track'))
        elif form.action.data == 'delete':
            name = form.name.data
            item = form.item.data[1:-1]
            tracker.delete_session_information(user_id, name)
            return redirect(url_for('tracker.track'))
        else:
            if tracker.check_user_tracker_existence(user_id) is False:
                tracker.create_session_information(user_id, "Shower", "Shower", 0.1250)
                tracker.create_session_information(user_id, "Air Conditioning", "Air Conditioning", 0.4167)
                tracker.create_session_information(user_id, "Lighting", "Lighting", 0.0104)
                tracker.create_session_information(user_id, "Washing Machine", "Laundry", 0.1042)
                tracker.create_session_information(user_id, "Electric Stove", "Cooking", 0.1042)
            timers = tracker.get_all_session_of_tracker(user_id)
            return render_template("tracker/tracker.html", keylist=timers, form=form, csrf_token=csrf_token)
    except:
        flash('Form Incomplete!', 'error')
        current_app.logger.info('Tracker Form Incomplete on submission', extra={'user_id': current_user.id, 'address': request.remote_addr, 'page': request.path, 'category':'Incomplete Form'})
        return redirect(url_for('tracker.track'))