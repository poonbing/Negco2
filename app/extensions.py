from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth


db = SQLAlchemy()
migrate = Migrate(db, render_as_batch=True)
mail = Mail()
login_manager = LoginManager()
oauth = OAuth()
