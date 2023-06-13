from flask import render_template, request
from app.main import bp


@bp.route("/mains")
def mains():
    return "<h1>Main</h1>"
