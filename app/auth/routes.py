# Python Modules
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from datetime import datetime
from uuid import uuid4


# Local Modules
from app.auth import bp
from .utils import init_and_commit, not_logged_in_required
from ..models import User, Session, OAuthUser
from ..forms import LoginForm, SignUpForm
from ..extensions import login_manager, oauth, db


@login_manager.user_loader
def user_loader(user_id):
    user = User.query.get(user_id)

    if not user:
        oauth_user_google = OAuthUser.query.get((user_id, "google"))
        if oauth_user_google:
            return oauth_user_google

        oauth_user_azure = OAuthUser.query.get((user_id, "azure"))
        if oauth_user_azure:
            return oauth_user_azure

    return user


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth.login"))


@bp.route("/login_with_google")
def login_with_google():
    redirect_uri = url_for("auth.auth", provider="google", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@bp.route("/login_with_azure")
def login_with_azure():
    redirect_uri = url_for("auth.auth", provider="azure", _external=True)
    return oauth.azure.authorize_redirect(redirect_uri)


@bp.route("/login", methods=["GET", "POST"])
@not_logged_in_required
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
            elif not xcaptcha.verify():
                flash("xCaptcha verification failed. Please try again.", "error")
            elif not user.check_password(password):
                user.increment_login_attempts()
                flash("Invalid username or password.", "error")

                current_app.logger.error(f"Authorization failed for Login")

            else:
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

    return render_template("auth/login.html", form=form)


@bp.route("/auth/<provider>")
def auth(provider):
    if provider == "google":
        token = oauth.google.authorize_access_token()
        user_info = oauth.google.get(
            "https://www.googleapis.com/oauth2/v3/userinfo"
        ).json()
    elif provider == "azure":
        token = oauth.azure.authorize_access_token()
        user_info = oauth.azure.get("userinfo").json()

    user_id = user_info.get("sub") if provider == "google" else user_info.get("id")
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
        provider_id=user_id, provider=provider
    ).first()

    if not oauth_user:
        oauth_user = OAuthUser(
            provider=provider,
            provider_id=user_id,
            username=username,
            email=email,
            access_token=access_token,
            profile_picture_url=profile_picture_url,
        )

        db.session.add(oauth_user)
        db.session.commit()

    login_user(oauth_user)
    return redirect(url_for("management.dashboard"))


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@bp.route("/signup", methods=["GET", "POST"])
@not_logged_in_required
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        print("reached here")
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
