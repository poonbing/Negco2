# Python Modules
from flask import render_template, current_app, redirect, url_for
from flask_wtf.csrf import CSRFError
from flask import flash
# Local Modules
from app.error import bp
from app import limiter


@bp.app_errorhandler(404)
@limiter.limit("4/second")
def page_not_found(e):
    return render_template("error/404.html"), 404


@bp.app_errorhandler(500)
@limiter.limit("4/second")
def page_not_found(e):
    return render_template("error/500.html"), 500

@bp.app_errorhandler(CSRFError)
def handle_csrd_error(e):
    flash('CSRF Token Error. Please Login Again')
    return redirect(url_for("auth.login"))