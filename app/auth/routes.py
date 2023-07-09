# Python Modules
from flask import render_template, request, redirect, session, url_for
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

# Local Modules
from app.auth import bp
from ..models import User, Session
from ..extensions import login_manager, db


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
                return render_template("auth/login.html", error=error)
            elif user.check_password(password):
                if False:
                    # if not xcaptcha.verify():
                    error = "xCaptcha verification failed. Please try again."
                    return render_template("auth/login.html", error=error)

                ip_address = request.remote_addr
                time_of_login = datetime.now()
                user_agent = request.user_agent.string

                # Create a new session and save it to the database
                session = Session(
                    user_id=user.id, ip_address=ip_address, user_agent=user_agent
                )
                db.session.add(session)
                db.session.commit()

                user.reset_login_attempts()
                login_user(user)
                return redirect(url_for("management.dashboard"))
            else:
                user.increment_login_attempts()
                if user.login_attempts >= 3:
                    user.lock_account()
                    error = "Account locked. Contact the admin for assistance."
                    return render_template("auth/login.html", error=error)
        error = "Invalid username or password."
        return render_template("auth/login.html", error=error)

    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        email = request.form.get("email")
        gender = request.form.get("gender")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        age = request.form.get("age")
        phone = request.form.get("phone")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = "Username already exists. Please choose a different username."
            return render_template("auth/signup.html", error=error)

        if password != confirm_password:
            error = "Passwords do not match. Please try again."
            return render_template("auth/signup.html", error=error)

        new_user = User(
            username=username,
            password=password,
            role="user",
            email=email,
            gender=gender,
            first_name=first_name,
            last_name=last_name,
            age=age,
            phone=phone,
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html")
