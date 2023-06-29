import os
from flask import Flask, render_template, redirect, url_for, request, session
from functions.tracker import TrackerFunctions
from functions.report import Report
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship
import uuid



app = Flask(__name__)
app.config['SECRET_KEY'] = 'app security project'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Negco_Admin:Forehead_Gang@it2555.mysql.database.azure.com/tracker'
engine = create_engine("mysql+pymysql://Negco_Admin:Forehead_Gang@it2555.mysql.database.azure.com/tracker", echo=True)
db = SQLAlchemy(app)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        session.pop('user', None)
        return render_template('index.html')


@app.route('/track', methods=['GET', 'POST'])
def track():
    tracker = TrackerFunctions()
    try:
        user = session['user']
    except: #updated
        user = request.form.get('user_id')
        session['user'] = user
        timers = tracker.get_all_session_of_tracker(user)
        return render_template('tracker.html', keylist=timers)
    if 'start_tracker' in request.form: #updated
        name = request.form.get('name')
        rate = request.form.get('rate')
        key = request.form.get('key')
        tracker_id, start_time = tracker.start_tracker(user, name, rate)
        tracker.start_session(user, name, tracker_id, start_time)
        timers = tracker.get_all_session_of_tracker(user)
        return render_template('tracker.html', keylist=timers)
    if 'item_form' in request.form: #updated
        index = request.form.get('item_index')
        item = request.form.get('new_item')
        rate = int(request.form.get('new_rate'))
        name = request.form.get('new_name')
        method = request.form.get('form_action')
        if method == 'update':
            tracker.update_session_information(user, index, name, item, rate)
        elif method == 'create':
            tracker.create_session_information(user, name, item, rate)
        timers = tracker.get_all_session_of_tracker(user)
        return render_template('tracker.html', keylist=timers)
    if 'delete' in request.form: #updated
        index = request.form.get('index')
        tracker.delete_session_information(user, index)
        timers = tracker.get_all_session_of_tracker(user)
        return render_template('tracker.html', keylist=timers)
    else: #updated
        timers = tracker.get_all_session_of_tracker(user)
        return render_template('tracker.html', keylist=timers)


@app.route('/report', methods=['GET', 'POST'])
def generate_report(): #updated
    report = TrackerFunctions()
    if request.method == 'POST':
        user = session['user']
        items = report.generate_report(user)
        x_axis, y_axis = report.generate_datapoints(items)
        return render_template('report.html', list=items, x=x_axis, y=y_axis)


if __name__ == '__main__':
    app.run(debug=True)
