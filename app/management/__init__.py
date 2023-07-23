from flask import Blueprint

bp = Blueprint("management", __name__)

from app.management import routes
