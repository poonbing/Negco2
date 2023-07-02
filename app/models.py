# Python Modules
from datetime import datetime, timedelta
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


# Local Modules
from .extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    profile_picture = db.Column(db.String(200), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    role = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    gender = db.Column(db.String(10))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    phone = db.Column(db.String(15))
    login_attempts = db.Column(db.Integer, default=0)

    locked = db.relationship("LockedUser", backref="user", uselist=False)

    def __init__(
        self, username, password, role, email, gender, first_name, last_name, age, phone
    ):
        self.username = username
        self.password = password
        self.role = role
        self.email = email
        self.gender = gender
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.phone = phone

    def check_password(self, password):
        return self.password == password

    def increment_login_attempts(self):
        self.login_attempts += 1
        db.session.commit()

    def reset_login_attempts(self):
        self.login_attempts = 0
        db.session.commit()

    def lock_account(self):
        if not self.locked:
            locked_user = LockedUser(user_id=self.id)
            db.session.add(locked_user)
            db.session.commit()

    def unlock_account(self):
        if self.locked:
            self.reset_login_attempts()
            db.session.delete(self.locked)
            db.session.commit()

    def is_account_locked(self):
        return self.locked is not None and self.locked.is_locked()

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False


class LockedUser(db.Model):
    __tablename__ = "locked_users"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    locked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_locked(self):
        lock_duration = timedelta(hours=1)
        return self.locked_at + lock_duration > datetime.utcnow()

class Tracker(db.Model):
    __tablename__ = 'tracker'
    #sql model
    id = db.Column(db.String(36), primary_key = True, unique = True)
    user_id = db.Column(db.String(36), nullable = False)
    name = db.Column(db.String(45), nullable = False)
    item = db.Column(db.String(45), nullable = False)
    rate = db.Column(db.INTEGER, nullable = False)
    start_time = db.Column(db.String(20), nullable = False)
    end_time = db.Column(db.String(20))

    def __init__(self, id, user_id, name, item, rate, start_time, end_time):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.item = item
        self.rate = rate
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'item': self.item,
            'rate': self.rate,
            'start_time': self.start_time,
            'end_time': self.end_time
        }
    
class SessionTracker(db.Model):
    __tablename__ = 'session_tracker'
    #sql model
    user_id = db.Column(db.String(36), primary_key = True, unique = True)
    active_sessions = relationship('SessionInfo', backref='session_tracker')

    def __init__(self, user_id, session_info=None):
        self.user_id = user_id
        self.session_info = session_info or []

    def add_session_info(self, data):
        self.session_info.append(data)
    
    def to_dict(self):
        return {
            'user_id':self.user_id,
            'active_session':self.active_sessions
        }

class SessionInfo(db.Model):
    __tablename__ = 'session_info'

    id = db.Column(db.String(36), primary_key = True, unique = True)
    active_sessions = db.Column(db.String(45), ForeignKey('session_tracker.user_id'))
    name = db.Column(db.String(45), nullable = False)
    item = db.Column(db.String(45), nullable = False)
    session_id = db.Column(db.String(36), nullable = False)
    session_start = db.Column(db.String(20))
    rate = db.Column(db.INTEGER, nullable = False)

    def __init__(self, id, user_id, name, item, session_id, session_start, rate):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.item = item
        self.session_id = session_id
        self.session_start = session_start
        self.rate = rate

    def to_dict(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'item': self.item,
            'session_id': self.session_id,
            'session_start':self.session_start,
            'rate':self.rate
        }