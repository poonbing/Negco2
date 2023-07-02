from flask import Blueprint

bp = Blueprint("password_recovery", __name__)

from app.password_recovery import routes
