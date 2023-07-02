# Python Modules
from datetime import datetime, timedelta
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


# Local Modules
from .extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.INTEGER, nullable = False, primary_key=True)
    profile_picture = db.Column(db.String(200), unique=True)
    username = db.Column(db.String(50), nullable = False, unique=True)
    password = db.Column(db.String(50), nullable = False)
    role = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique=True)
    gender = db.Column(db.String(10), nullable = False)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    age = db.Column(db.INTEGER, nullable = False)
    phone = db.Column(db.String(15), nullable = False)
    login_attempts = db.Column(db.INTEGER, default=0)

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

    id = db.Column(db.INTEGER, nullable = False, primary_key=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey("users.id"), nullable = False, unique=True)
    locked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_locked(self):
        lock_duration = timedelta(hours=1)
        return self.locked_at + lock_duration > datetime.utcnow()

class Tracker(db.Model):
    __tablename__ = 'tracker'
    #sql model
    id = db.Column(db.String(36), primary_key = True, unique = True)
    user = db.Column(db.INTEGER, nullable = False)
    name = db.Column(db.String(45), nullable = False)
    item = db.Column(db.String(45), nullable = False)
    rate = db.Column(db.INTEGER, nullable = False)
    start_time = db.Column(db.String(20), nullable = False)
    end_time = db.Column(db.String(20))

    def __init__(self, id, user, name, item, rate, start_time, end_time):
        self.id = id
        self.user = user
        self.name = name
        self.item = item
        self.rate = rate
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user,
            'name': self.name,
            'item': self.item,
            'rate': self.rate,
            'start_time': self.start_time,
            'end_time': self.end_time
        }

class SessionInfo(db.Model):
    __tablename__ = 'session_info'

    id = db.Column(db.String(36), primary_key = True, nullable = False, unique = True)
    active_sessions = db.Column(db.String(45), ForeignKey('session_tracker.user_id'), nullable = False)
    name = db.Column(db.String(45), nullable = False)
    item = db.Column(db.String(45), nullable = False)
    session_id = db.Column(db.String(36))
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