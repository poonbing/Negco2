from flask import render_template, request, redirect, session, url_for
from app.login import bp
from ..models import User


@bp.route("/login", methods=["GET", "POST"])
def login():
    xcaptcha = bp.xcaptcha
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            if False:
                # if not xcaptcha.verify():
                error = "xCaptcha verification failed. Please try again."
                return render_template("login.html", error=error)
            session["username"] = username
            return redirect(url_for("user.dashboard"))
        else:
            error = "Invalid username or password."
            return render_template("login.html", error=error)

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login.login"))
