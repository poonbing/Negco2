# Python Modules
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from datetime import datetime


# Local Modules
from app import limiter
from app.auth import bp
from .utils import not_logged_in_required
from ..models import User, Session, OAuthUser
from ..forms import LoginForm, SignUpForm
from ..extensions import login_manager, oauth, db


@login_manager.user_loader
@limiter.limit("4/second")
def user_loader(user_id):
    user = User.query.get(user_id)

    return user


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth.login"))


@bp.route("/login_with_google")
@limiter.limit("4/second")
def login_with_google():
    redirect_uri = url_for("auth.auth", provider="google", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@bp.route("/login_with_azure")
@limiter.limit("4/second")
def login_with_azure():
    redirect_uri = url_for("auth.auth", provider="azure", _external=True)
    return oauth.azure.authorize_redirect(redirect_uri)


@bp.route("/login", methods=["GET", "POST"])
@not_logged_in_required
@limiter.limit("4/second")
def login():
    xcaptcha = bp.xcaptcha
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter(
            or_(User.username == username, User.email == username)
        ).first()

        if user:
            if user.is_account_locked():
                flash("Account locked. Contact the admin for assistance.", "error")

                current_app.logger.info(
                    f"User Login Failed: Locked User",
                    extra={
                        "user_id": "null",
                        "address": request.remote_addr,
                        "page": request.path,
                        "category": "Login",
                    },
                )
            elif not xcaptcha.verify():
                flash("xCaptcha verification failed. Please try again.", "error")
            elif not user.check_password(password):
                user.increment_login_attempts()
                current_app.logger.info(
                    f"User Login Failed: Incorrect Password",
                    extra={
                        "user_id": "null",
                        "address": request.remote_addr,
                        "page": request.path,
                        "category": "Login",
                    },
                )
                flash("Invalid username or password.", "error")
                current_app.logger.info(
                    f"User Login Failed: Incorrect Password",
                    extra={
                        "user_id": "null",
                        "address": request.remote_addr,
                        "page": request.path,
                        "category": "Login",
                    },
                )
            else:
                sess = Session(
                    user.id,
                    datetime.now(),
                    request.remote_addr,
                    request.user_agent.string,
                )
                current_app.logger.info(
                    f"User Logged In: {user.id}",
                    extra={
                        "user_id": user.id,
                        "address": request.remote_addr,
                        "page": request.path,
                        "category": "Login",
                    },
                )
                db.session.add(sess)
                db.session.commit()

                user.reset_login_attempts()
                login_user(user)

                return redirect(url_for("management.dashboard"))
        else:
            flash("Invalid username or password.", "error")
            current_app.logger.info(
                f"User login Failed: Incorrect Username",
                extra={
                    "user_id": "null",
                    "address": request.remote_addr,
                    "page": request.path,
                    "category": "login",
                },
            )
    return render_template("auth/login.html", form=form)


@bp.route("/auth/<provider>")
@limiter.limit("4/second")
def auth(provider):
    if provider == "google":
        token = oauth.google.authorize_access_token()
        user_info = oauth.google.get(
            "https://www.googleapis.com/oauth2/v3/userinfo"
        ).json()
    elif provider == "azure":
        token = oauth.azure.authorize_access_token()
        user_info = oauth.azure.get("userinfo").json()

    provider_id = user_info.get("sub") if provider == "google" else user_info.get("id")
    email = user_info.get("email")
    print(user_info)
    username = user_info.get("name")
    access_token = token.get("access_token")
    profile_picture_url = (
        user_info.get("picture")
        if provider == "google"
        else user_info.get("avatar_url")
    )

    oauth_user = OAuthUser.query.filter_by(
        provider_id=provider_id, provider=provider
    ).first()

    if not oauth_user:
        user = User(
            username=username,
            password="",
            role="oauth",
            email=email,
            gender="",
            first_name="",
            last_name="",
            age=0,
            phone="",
        )

        oauth_user = OAuthUser(
            provider=provider,
            provider_id=provider_id,
            username=username,
            user_id=user.id,
            email=email,
            access_token=access_token,
            profile_picture_url=profile_picture_url,
        )

        db.session.add(oauth_user)
        db.session.add(user)
        db.session.commit()

    login_user(oauth_user.user)
    return redirect(url_for("management.dashboard"))


@bp.route("/logout")
@login_required
@limiter.limit("4/second")
def logout():
    current_app.logger.info(
        f"User Logged Out: {current_user.id}",
        extra={
            "user_id": current_user.id,
            "address": request.remote_addr,
            "page": request.path,
            "category": "Login",
        },
    )
    logout_user()
    return redirect(url_for("auth.login"))


@bp.route("/signup", methods=["GET", "POST"])
@not_logged_in_required
@limiter.limit("4/second")
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
            user = User(
                username,
                password,
                "user",
                email,
                gender,
                first_name,
                last_name,
                age,
                phone,
            )
            db.session.add(user)
            db.session.commit()
            current_app.logger.info(
                f"User Created: {user.id}",
                extra={
                    "user_id": user.id,
                    "address": request.remote_addr,
                    "page": request.path,
                    "category": "Signup",
                },
            )
            flash("Passwords do not match. Please try again.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/signup.html", form=form)
