from flask import Blueprint

bp = Blueprint("recovery", __name__)

from app.recovery import routes
