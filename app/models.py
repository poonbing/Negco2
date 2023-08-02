# Python Modules
from datetime import datetime, timedelta
from flask_login import UserMixin
from sqlalchemy import CheckConstraint
from secrets import token_hex
from flask_serialize import FlaskSerializeMixin
import json
from uuid import uuid4
from bcrypt import hashpw, gensalt, checkpw
from itsdangerous import URLSafeTimedSerializer as Serializer
import pickle
import logging
# Local Modules
from .extensions import db
from config import Config

# Mixins
###############################################################


class CRUDMixin:
    def save(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        db.session.commit()


class AccountManagementMixin:
    def increment_login_attempts(self):
        self.login_attempts += 1
        if self.login_attempts >= 3:
            self.lock_account()
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


class RolesAndPermissionsMixin:
    def is_admin(self):
        return self.role == "admin"

    def has_role(self, required_role):
        return self.role == required_role


class ResetPasswordsMixin:
    def get_reset_token(self, expires_sec=1800):
        s = Serializer("your_secret_key_here")
        payload = {"user_id": self.id}
        serialized_payload = pickle.dumps(payload)
        # Convert bytes to a JSON-serializable format (e.g., string)
        token = serialized_payload.decode("latin1")
        return token

    @staticmethod
    def verify_reset_token(token):
        s = Serializer("your_secret_key_here")
        try:
            # Convert the token back to bytes (reverse of the get_reset_token method)
            serialized_payload = token.encode("latin1")
            user_id = pickle.loads(serialized_payload)["user_id"]
        except:
            return None
        return User.query.get(user_id)


# Relations
####################################################


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    session_token = db.Column(db.String(100), unique=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"))
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))

    def __init__(self, user_id, last_activity, ip_address, user_agent):
        self.session_token = token_hex(32)
        self.user_id = user_id
        self.last_activity = last_activity
        self.ip_address = ip_address
        self.user_agent = user_agent

    def update_last_activity(self):
        self.last_activity = datetime.utcnow()
        db.session.commit()


class User(
    db.Model,
    UserMixin,
    AccountManagementMixin,
    RolesAndPermissionsMixin,
    ResetPasswordsMixin,
):
    __tablename__ = "users"

    id = db.Column(db.String(36), nullable=False, primary_key=True)
    profile_picture = db.Column(db.LargeBinary(length=(2**32) - 1))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    gender = db.Column(db.String(10), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.INTEGER, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    login_attempts = db.Column(db.INTEGER, default=0)
    locked = db.relationship("LockedUser", backref="user", uselist=False)

    __table_args__ = (
        CheckConstraint(gender.in_(["male", "female"]), name="check_gender"),
        CheckConstraint(
            role.in_(["admin", "editor", "user", "oauth"]), name="check_role"
        ),
    )

    def __init__(
        self,
        username,
        password,
        role,
        email,
        gender,
        first_name,
        last_name,
        age,
        phone,
    ):
        self.id = str(uuid4())[:8]
        self.username = username
        self.password = hashpw(password.encode("utf-8"), gensalt())
        self.role = role
        self.email = email
        self.gender = gender
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.phone = phone

    def check_password(self, password):
        return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))


class OAuthUser(UserMixin, db.Model):
    __tablename__ = "oauth_users"

    id = db.Column(db.String(36), primary_key=True)
    provider = db.Column(db.String(50), nullable=False)
    provider_id = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(100))
    access_token = db.Column(db.String(256))
    profile_picture_url = db.Column(db.String(256))

    def __init__(
        self,
        provider,
        provider_id,
        email=None,
        username=None,
        access_token=None,
        profile_picture_url=None,
    ):
        self.id = str(uuid4())[:8]
        self.provider = provider
        self.provider_id = provider_id
        self.email = email
        self.username = username
        self.access_token = access_token
        self.profile_picture_url = profile_picture_url

    __table_args__ = (
        db.PrimaryKeyConstraint("id", "provider"),
        {},
    )


class LockedUser(db.Model):
    __tablename__ = "locked_users"

    id = db.Column(db.String(36), nullable=False, primary_key=True)
    user_id = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=False, unique=True
        db.String(36), db.ForeignKey("users.id"), nullable=False, unique=True
    )
    locked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_locked(self):
        lock_duration = timedelta(hours=1)
        return self.locked_at + lock_duration > datetime.utcnow()


class APIKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=False, unique=True
    )
    expiration_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id):
        self.key = str(uuid4())
        self.user_id = user_id
        self.expiration_time = datetime.utcnow() + timedelta(days=365)

    @property
    def has_expired(self):
        return datetime.utcnow() > self.expiration_time


class Tracker(db.Model):
    __tablename__ = "tracker"
    # sql model
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=False, unique=True
    )
    name = db.Column(db.String(45), nullable=False)
    item = db.Column(db.String(45), nullable=False)
    rate = db.Column(db.INTEGER, nullable=False)
    start_time = db.Column(db.String(20), nullable=False)
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
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "item": self.item,
            "rate": self.rate,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }


class SessionInfo(db.Model):
    __tablename__ = "session_info"

    id = db.Column(db.String(36), primary_key=True, nullable=False, unique=True)
    active_sessions = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=False, unique=True
    )
    name = db.Column(db.String(45), nullable=False)
    item = db.Column(db.String(45), nullable=False)
    session_id = db.Column(db.String(36))
    session_start = db.Column(db.String(20))
    rate = db.Column(db.INTEGER, nullable=False)

    def __init__(self, id, active_sessions, name, item, session_id, session_start, rate):
        self.id = id
        self.active_sessions = active_sessions
        self.name = name
        self.item = item
        self.session_id = session_id
        self.session_start = session_start
        self.rate = rate

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "item": self.item,
            "session_id": self.session_id,
            "session_start": self.session_start,
            "rate": self.rate,
        }


class Report(db.Model):
    __tablename__ = "report"

    id = id = db.Column(db.String(36), primary_key=True, unique=True)
    related_user = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    item_name = db.Column(db.String(45), nullable=False)
    month = db.Column(db.String(2), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    total_usage = db.Column(db.INTEGER)
    energy_goals = db.Column(db.INTEGER)
    datapoint = db.Column(db.JSON)

    def __init__(self, id, related_user, item_name, month, year, total_usage, energy_goals, datapoint):
        self.id = id
        self.related_user = related_user
        self.item_name = item_name
        self.month = month
        self.year = year
        self.total_usage = total_usage
        self.energy_goals = energy_goals
        self.datapoint = datapoint

    def to_dict(self):
        return {
            "id": self.id,
            "related_user": self.related_user,
            "item_name": self.item_name,
            "month": self.month,
            "year": self.year,
            "total_usage": self.total_usage,
            "energy_goals": self.energy_goals,
            "datapoint": self.datapoint
        }


class Articles(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.String(36), primary_key=True, unique=True)
    title = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.today)
    writer = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(50), unique=True, nullable=False)
    paragraph = db.Column(db.String(20000), nullable=False)

    def time_ago(self):
        time_difference = datetime.now() - self.date_added
        if time_difference.days > 0:
            return f"{time_difference.days} days ago"
        elif time_difference.seconds >= 3600:
            hours = time_difference.seconds // 3600
            return f"{hours} hours ago"
        elif time_difference.seconds >= 60:
            minutes = time_difference.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "Just now", 


class Products(db.Model):
    __tablename__ = "products"

    id = db.Column(db.String(36), primary_key=True, unique=True)
    brand = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(800), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    offer = db.Column(db.Integer)
    image = db.Column(db.String(50), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.today)
    offered_price = db.Column(db.Numeric(precision=10, scale=2))
    rating_score = db.Column(db.Integer)
    rating_count = db.Column(db.Integer)

    def rating_result(self):
        if self.rating_count == None:
            rating_result = 0
            return rating_result
        else:
            rating_result = (self.rating_score / (self.rating_count*5))*5

        return round(rating_result, 1)



class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.String(36), primary_key=True, unique=True)
    product_id = db.Column(db.String(36), db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2))

    user_id = db.Column(
        db.String(36), db.ForeignKey("users.id"), unique=True, nullable=False
    )
    product = db.relationship("Products", backref="cart_items")


class Comment(db.Model):
    __tablename__ = "content"

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, unique=True)
    post_id = db.Column(db.INTEGER, db.ForeignKey("posts.id"), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    commenter = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=False, unique=True
    )
    post = db.relationship("Post", back_populates="comments")


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    topic_id = db.Column(db.INTEGER, db.ForeignKey("topics.id"), nullable=False)
    poster = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=False, unique=True
    )
    topic = db.relationship("Topic", back_populates="posts")
    content = db.Column(db.Text(length=1000000), nullable=False)
    comments = db.relationship("Comment", back_populates="post")
    image = db.Column(db.LargeBinary(length=(2**32) - 1), nullable=True)


class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.INTEGER, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    posts = db.relationship("Post", back_populates="topic")


class Report(db.Model):
    __tablename__ = "report"

    id = id = db.Column(db.String(36), primary_key=True, unique=True)
    related_user = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    item_name = db.Column(db.String(45), nullable=False)
    month = db.Column(db.String(2), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    total_usage = db.Column(db.INTEGER)
    energy_goals = db.Column(db.INTEGER)
    datapoint = db.Column(db.JSON)

    def __init__(
        self,
        id,
        related_user,
        item_name,
        month,
        year,
        total_usage,
        energy_goals,
        datapoint,
    ):
        self.id = id
        self.related_user = related_user
        self.item_name = item_name
        self.month = month
        self.year = year
        self.total_usage = total_usage
        self.energy_goals = energy_goals
        self.datapoint = datapoint

    def to_dict(self):
        return {
            "id": self.id,
            "related_user": self.related_user,
            "item_name": self.item_name,
            "month": self.month,
            "year": self.year,
            "total_usage": self.total_usage,
            "energy_goals": self.energy_goals,
            "datapoint": self.datapoint,
        }


class Report(db.Model):
    __tablename__ = "report"

    id = id = db.Column(db.String(36), primary_key=True, unique=True)
    related_user = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    item_name = db.Column(db.String(45), nullable=False)
    month = db.Column(db.String(2), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    total_usage = db.Column(db.INTEGER)
    energy_goals = db.Column(db.INTEGER)
    datapoint = db.Column(db.JSON)

    def __init__(
        self,
        id,
        related_user,
        item_name,
        month,
        year,
        total_usage,
        energy_goals,
        datapoint,
    ):
        self.id = id
        self.related_user = related_user
        self.item_name = item_name
        self.month = month
        self.year = year
        self.total_usage = total_usage
        self.energy_goals = energy_goals
        self.datapoint = datapoint

    def to_dict(self):
        return {
            "id": self.id,
            "related_user": self.related_user,
            "item_name": self.item_name,
            "month": self.month,
            "year": self.year,
            "total_usage": self.total_usage,
            "energy_goals": self.energy_goals,
            "datapoint": self.datapoint,
        }


class Checkout(db.Model, FlaskSerializeMixin):
    __tablename__ = 'checkout'
    id = db.Column(db.String(36), primary_key=True, unique=True)
    user_id = user_id = db.Column(
        db.INTEGER, db.ForeignKey("users.id"), unique=True, nullable=False
    )
    product_list = db.Column(db.String(255), db.ForeignKey("products.id"), nullable=False)
    product_price = db.Column(db.String(255))
    product_quantity = db.Column(db.String(255))
    total_cost = db.Column(db.Numeric(precision=10, scale=2))
    payment_date = db.Column(db.DateTime, default=datetime.today)


    
class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.INTEGER, primary_key=True, nullable=False, autoincrement=True)
    timestamp = db.Column(db.DateTime, default = db.func.current_timestamp())
    log_text = db.Column(db.String, nullable=False)