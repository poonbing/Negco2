# Python Modules
from flask import Blueprint
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_login import current_user

# Local Modules
from ..extensions import db, OAuth

bp = Blueprint("auth", __name__)

google_blueprint = make_google_blueprint(
    client_id="43510388979-2l3aedm3mce7trakvl09n9rcblcm1lco.apps.googleusercontent.com",
    client_secret="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",
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
    # storage=SQLAlchemyStorage(
    #     OAuth,
    #     db.session,
    #     user=current_user,
    # ),
)

github_blueprint = make_github_blueprint(
    client_id="e9d685f8558a7a584761",
    client_secret="048a2b47fc787386a4037d4690d69bcd387ba351",
    scope="user:email",
    # storage=SQLAlchemyStorage(
    #     OAuth,
    #     db.session,
    #     user=current_user,
    # ),
)

from app.auth import routes
