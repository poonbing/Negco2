from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
migrate = Migrate(db, render_as_batch=True)
mail = Mail()
csrf = CSRFProtect()
login_manager = LoginManager()
jwt = JWTManager()
oauth = OAuth()


oauth.register(
    name="google",
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    name="azure",
    client_id=Config.AZURE_CLIENT_ID,
    client_secret=Config.AZURE_CLIENT_SECRET,
    api_base_url="https://graph.microsoft.com/",
    server_metadata_url="https://login.microsoftonline.com/f8cdef31-a31e-4b4a-93e4-5f571e91255a/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
