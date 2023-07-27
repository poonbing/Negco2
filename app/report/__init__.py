from flask import Blueprint

bp = Blueprint("report", __name__)

from app.tracker import routes