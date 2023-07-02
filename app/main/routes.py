from flask import render_template, request, redirect, session, url_for
from app.main import bp
from ..models import User


@bp.route("/")
def home():
    if "username" in session:
        return redirect(url_for("user.dashboard"))
    return redirect(url_for("login.login"))
