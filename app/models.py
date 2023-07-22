# Python Modules
from datetime import datetime, timedelta
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from secrets import token_hex

# Local Modules
from .extensions import db


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    session_token = db.Column(db.String(100), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
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


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.INTEGER, nullable=False, primary_key=True)
    profile_picture = db.Column(db.LargeBinary(length=(2**32) - 1))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    gender = db.Column(db.String(10), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.INTEGER, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    login_attempts = db.Column(db.INTEGER, default=0)
    locked = db.relationship("LockedUser", backref="user", uselist=False)

    def __init__(
        self,
        user_id,
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
        self.id = user_id
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

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.role == "admin"

    def create_session(self, session_token):
        session = Session(session_token=session_token, user_id=self.id)
        db.session.add(session)
        db.session.commit()

    def get_session(self, session_token):
        return self.sessions.filter_by(session_token=session_token).first()

    def update_session_last_activity(self, session_token):
        session = self.get_session(session_token)
        if session:
            session.update_last_activity()


class OAuthUser(OAuthConsumerMixin, db.Model):
    __tablename__ = "oauth_users"

    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


class RoleMixin(object):
    """This provides implementations for the methods that Flask-RBAC wants
    the role model to have.

    :param name: The name of role.
    """

    roles = {}

    def __init__(self, name=None):
        self.name = name
        if not hasattr(self.__class__, "parents"):
            self.parents = set()
        if not hasattr(self.__class__, "children"):
            self.children = set()
        RoleMixin.roles[name] = self

    def get_name(self):
        """Return the name of this role"""
        return self.name

    def add_parent(self, parent):
        """Add a parent to this role,
        and add role itself to the parent's children set.
        you should override this function if neccessary.

        Example::

            logged_user = RoleMixin('logged_user')
            student = RoleMixin('student')
            student.add_parent(logged_user)

        :param parent: Parent role to add in.
        """
        parent.children.add(self)
        self.parents.add(parent)

    def add_parents(self, *parents):
        """Add parents to this role. Also should override if neccessary.
        Example::

            editor_of_articles = RoleMixin('editor_of_articles')
            editor_of_photonews = RoleMixin('editor_of_photonews')
            editor_of_all = RoleMixin('editor_of_all')
            editor_of_all.add_parents(editor_of_articles, editor_of_photonews)

        :param parents: Parents to add.
        """
        for parent in parents:
            self.add_parent(parent)

    def get_parents(self):
        for parent in self.parents:
            yield parent
            for grandparent in parent.get_parents():
                yield grandparent

    def get_children(self):
        for child in self.children:
            yield child
            for grandchild in child.get_children():
                yield grandchild

    @staticmethod
    def get_by_name(name):
        """A static method to return the role which has the input name.

        :param name: The name of role.
        """
        return RoleMixin.roles.get(name)

    @classmethod
    def get_all(cls):
        """Return all existing roles"""
        return cls.roles


class LockedUser(db.Model):
    __tablename__ = "locked_users"

    id = db.Column(db.INTEGER, nullable=False, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.INTEGER, db.ForeignKey("users.id"), nullable=False, unique=True
    )
    locked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_locked(self):
        lock_duration = timedelta(hours=1)
        return self.locked_at + lock_duration > datetime.utcnow()


class Tracker(db.Model):
    __tablename__ = "tracker"
    # sql model
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.INTEGER, nullable=False, unique=True)
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
    active_sessions = db.Column(db.INTEGER, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    item = db.Column(db.String(45), nullable=False)
    session_id = db.Column(db.String(36))
    session_start = db.Column(db.String(20))
    rate = db.Column(db.INTEGER, nullable=False)

    def __init__(self, id, user_id, name, item, session_id, session_start, rate):
        self.id = id
        self.user_id = user_id
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
            return "Just now"


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


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(36), db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2))

    product = db.relationship("Products", backref="cart_items")


class Comment(db.Model):
    __tablename__ = "content"

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, unique=True)
    post_id = db.Column(db.INTEGER, db.ForeignKey("posts.id"), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    post = db.relationship("Post", back_populates="comments")


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    topic_id = db.Column(db.INTEGER, db.ForeignKey("topics.id"), nullable=False)
    topic = db.relationship("Topic", back_populates="posts")
    content = db.Column(db.Text(length=1000000), nullable=False)
    comments = db.relationship("Comment", back_populates="post")


class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.INTEGER, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    posts = db.relationship("Post", back_populates="topic")
