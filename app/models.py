from .extensions import db
from datetime import datetime, timedelta


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
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


class LockedUser(db.Model):
    __tablename__ = "locked_users"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    locked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_locked(self):
        # You can customize the locking conditions here (e.g., time-based lock)
        lock_duration = timedelta(hours=1)
        return self.locked_at + lock_duration > datetime.utcnow()
