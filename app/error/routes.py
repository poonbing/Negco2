# Python Modules
from flask import render_template

# Local Modules
from app.error import bp


@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html"), 404


@bp.app_errorhandler(500)
def page_not_found(e):
    return render_template("error/500.html"), 500
