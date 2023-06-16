from flask import Flask, render_template, redirect, url_for, request, session
import shelve
from datetime import datetime
import uuid
from functions.tracker import Tracker

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET': 
        return render_template('index.html')

@app.route('/track', methods=['GET', 'POST'])
def track():
    if 'item' in request.form:
        item = request.form.get('item')
        rate = request.form.get('rate')
        user = request.form.get('user')
        key = request.form.get('key')
        start_time = request.form.get('time')
        print(item, rate, user, key, start_time)
        if key == 'None':
            print(f'create entry, {item}')
            tracker_id = str(uuid.uuid4())
            current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            year = datetime.now().year
            month = datetime.now().strftime("%m")
            with shelve.open(f'tracker{year}{month}') as tracker_db:
                tracker_db[tracker_id] = {
                    'user':user,
                    'item': item, 
                    'rate':rate, 
                    'time_start': current_time, 
                    'time_end': None}
            with shelve.open('user') as user_db:
                timers = user_db[user]
                timers[item] = [tracker_id, current_time]
                user_db[user] = timers
            return render_template('tracker.html', user = user, keylist = timers)
        elif key != 'None':
            print(f'close entry, {item}, {key}')
            current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            year = datetime.now().year
            month = datetime.now().strftime("%m")
            with shelve.open(f'tracker{year}{month}') as tracker_db:
                instance = tracker_db[key]
                instance['time_end'] = current_time
                tracker_db[key] = instance
            with shelve.open('user') as user_db:
                timers = user_db[user]
                timers[item] = [None, None]
                user_db[user] = timers
            return render_template('tracker.html', user = user, keylist = timers)
    if 'user_id' in request.form:
        user = request.form.get('user_id')
        with shelve.open('user') as user_db:
            if user in user_db:
                timers = user_db[user]
            else:
                user_db[user] = {'Aircon':[None, None],
                                'Shower':[None, None],
                                'Lights':[None, None]}
                timers = user_db[user]
        return render_template('tracker.html', user = user, keylist = timers)

@app.route('/report', methods=['GET', 'POST'])
def generate_report():
    if request.method == 'POST':
        user = request.form.get('user')
        x_axis, y_axis = Tracker.generate_datapoints(Tracker.generate_report(user))
        items = Tracker.generate_report(user)
        return render_template('report.html', list=items, x = x_axis, y = y_axis)


if __name__ == '__main__':
    app.run(debug = True)