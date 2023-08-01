from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_talisman import Talisman
from authlib.integrations.flask_client import OAuth
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate(db, render_as_batch=True)
mail = Mail()
csrf = CSRFProtect()
login_manager = LoginManager()
jwt = JWTManager()
oauth = OAuth()
