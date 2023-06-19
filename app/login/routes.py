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
        if user:
            if user.is_account_locked():
                error = "Account locked. Contact the admin for assistance."
                return render_template("login/login.html", error=error)
            elif user.password == password:
                if not xcaptcha.verify():
                    error = "xCaptcha verification failed. Please try again."
                    return render_template("login/login.html", error=error)
                user.reset_login_attempts()
                session["username"] = username
                return redirect(url_for("user.dashboard"))
            else:
                user.increment_login_attempts()
                if user.login_attempts >= 3:
                    user.lock_account()
                    error = "Account locked. Contact the admin for assistance."
                    return render_template("login/login.html", error=error)
        error = "Invalid username or password."
        return render_template("login/login.html", error=error)

    return render_template("login/login.html")


@bp.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login.login"))
