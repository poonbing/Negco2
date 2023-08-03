# Python Modules
from flask import render_template

# Local Modules
from app.error import bp
from app import limiter

@bp.app_errorhandler(404)
@limiter.limit('4/second')
def page_not_found(e):
    return render_template("error/404.html"), 404


@bp.app_errorhandler(500)
@limiter.limit('4/second')
def page_not_found(e):
    return render_template("error/500.html"), 500
