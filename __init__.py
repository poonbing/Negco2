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
    if 'start_tracker' in request.form:
        print('create')
        item = request.form.get('item')
        rate = request.form.get('rate')
        key = request.form.get('key')
        user = session['user']
        Tracker().update_tracker_session(item, rate, user, key)
        timers = Tracker().get_active_trackers(user)
        return render_template('tracker.html', user = user, keylist = timers)
    if 'user_id' in request.form:
        user = request.form.get('user_id')
        session['user'] = user
        timers = Tracker().get_active_trackers(user)
        return render_template('tracker.html', user = user, keylist = timers)
    else:
        user = session['user']
        timers = Tracker().get_active_trackers(user)
        return render_template('tracker.html', user = user, keylist = timers)

@app.route('/report', methods=['GET', 'POST'])
def generate_report():
    if request.method == 'POST':
        user = session['user']
        x_axis, y_axis = Report().generate_datapoints(Report().generate_report(user))
        items = Report().generate_report(user)
        return render_template('report.html', list=items, x = x_axis, y = y_axis)


if __name__ == '__main__':
    app.run(debug = True)