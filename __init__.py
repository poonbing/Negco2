from flask import Flask, render_template, redirect, url_for, request, session
from functions.tracker import Tracker
from functions.report import Report

app = Flask(__name__)
app.config['SECRET_KEY'] = '3d6f45a5fc12445dbac2f59c3b6c7cb1'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        session.pop('user', None)
        return render_template('index.html')


@app.route('/track', methods=['GET', 'POST'])
def track():
    try:
        user = session['user']
    except:
        user = request.form.get('user_id')
        session['user'] = user
        timers = Tracker().get_active_trackers(user)
        return render_template('tracker.html', user=user, keylist=timers)
    if 'start_tracker' in request.form:
        name = request.form.get('name')
        rate = request.form.get('rate')
        key = request.form.get('key')
        Tracker().update_tracker_session(name, rate, user, key)
        timers = Tracker().get_active_trackers(user)
        return render_template('tracker.html', user=user, keylist=timers)
    if 'item_form' in request.form:
        timers = {}
        index = int(request.form.get('item_index'))-1
        item = request.form.get('new_item')
        rate = int(request.form.get('new_rate'))
        name = request.form.get('new_name')
        method = request.form.get('form_action')
        trackers = Tracker().get_active_trackers(user)
        if method == 'update':
            count = 0
            for key in trackers:
                if count == index:
                    timers[name] = [item, rate, None, None]
                else:
                    timers[key] = trackers[key]
                count += 1
        elif method == 'create':
            timers = trackers
            timers[name] = [item, rate, None, None]
        Tracker().set_active_trackers(user, timers)
        return render_template('tracker.html', user=user, keylist=timers)
    if 'delete' in request.form:
        index = request.form.get('index')
        timers = Tracker().get_active_trackers(user)
        count = 0
        timers.pop(index)
        print(timers)
        Tracker().set_active_trackers(user, timers)
        return render_template('tracker.html', user=user, keylist=timers)
    else:
        timers = Tracker().get_active_trackers(user)
        return render_template('tracker.html', user=user, keylist=timers)


@app.route('/report', methods=['GET', 'POST'])
def generate_report():
    report = Report()
    if request.method == 'POST':
        user = session['user']
        x_axis, y_axis = report.generate_datapoints(
            report.generate_report(user))
        items = report.generate_report(user)
        return render_template('report.html', list=items, x=x_axis, y=y_axis)


if __name__ == '__main__':
    app.run(debug=True)
