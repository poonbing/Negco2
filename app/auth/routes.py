# Python Modules
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from sqlalchemy import or_
from datetime import datetime

# Local Modules
from app.auth import bp
from .utils import init_and_commit
from ..models import User, Session
from ..forms import LoginForm, SignUpForm
from ..extensions import login_manager


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@bp.route("/login", methods=["GET", "POST"])
def login():
    xcaptcha = bp.xcaptcha
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter(
            or_(User.username == username, User.email == username)
        ).first()

        if user.is_account_locked():
            flash("Account locked. Contact the admin for assistance.", "error")
        elif not xcaptcha.verify():
            flash("xCaptcha verification failed. Please try again.", "error")
        else:
            if user and user.check_password(password):
                session_attributes = {
                    "user_id": user.id,
                    "last_activity": datetime.now(),
                    "ip_address": request.remote_addr,
                    "user_agent": request.user_agent.string,
                }

                init_and_commit(Session, session_attributes)

                user.reset_login_attempts()
                login_user(user)

                return redirect(url_for("management.dashboard"))
            else:
                user.increment_login_attempts()
                flash("Invalid username or password.", "error")

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        email = form.email.data
        gender = form.gender.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        age = form.age.data
        phone = form.phone.data

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash(
                "Username already exists. Please choose a different username.", "error"
            )

        elif password != confirm_password:
            flash("Passwords do not match. Please try again.", "error")

        else:
            user_attributes = {
                "user_id": 6,
                "username": username,
                "password": password,
                "role": "user",
                "email": email,
                "gender": gender,
                "first_name": first_name,
                "last_name": last_name,
                "age": age,
                "phone": phone,
            }
            init_and_commit(User, user_attributes)

            return redirect(url_for("auth.login"))

    return render_template("auth/signup.html", form=form)
