from flask import render_template, request, redirect, session, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.login import bp
from ..models import User
from ..extensions import login_manager


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


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
            elif user.check_password(password):
                if not xcaptcha.verify():
                    error = "xCaptcha verification failed. Please try again."
                    return render_template("login/login.html", error=error)
                user.reset_login_attempts()
                login_user(user)
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
@login_required
def logout():
    logout_user()
    return redirect(url_for("login.login"))
