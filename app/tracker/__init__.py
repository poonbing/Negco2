from flask import Blueprint

bp = Blueprint("tracker", __name__)

from app.tracker import routes