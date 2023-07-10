# Python Modules
from flask import redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required
from functools import wraps
from PIL import Image
import secrets
import os

# Local Modules
from app.management import bp
from ..models import User, LockedUser, Session
from ..extensions import db
from ..forms import SettingsForm
from ..models import User
from config import Config


def admin_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            return redirect(url_for("management.dashboard"))
        return view_func(*args, **kwargs)

    return decorated_view


@bp.route("/show_users", methods=["GET"])
@login_required
@admin_required
def show_users():
    all_users = User.query.all()
    return render_template("management/users.html", users=all_users)


@bp.route("/locked-accounts", methods=["GET", "POST"])
@login_required
@admin_required
def locked_accounts():
    if request.method == "POST":
        locked_account_ids = request.form.getlist("unlock_account")
        for account_id in locked_account_ids:
            user = User.query.get(account_id)
            if user:
                user.unlock_account()

        return redirect(url_for("management.locked_accounts"))

    locked_accounts = User.query.join(LockedUser).all()

    return render_template(
        "management/lockedAccounts.html", locked_accounts=locked_accounts
    )


@bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    user = current_user

    sessions = Session.query.filter_by(user_id=user.id).all()
    form = SettingsForm()

    if form.validate_on_submit():
        if form.profile_picture.data:
            profile_picture = save_picture(form.profile_picture.data)
            user.profile_picture = profile_picture

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone = form.phone.data
        user.gender = form.gender.data
        user.email = form.email.data

        new_password = form.password.data
        confirm_password = form.confirm_password.data
        if new_password and new_password == confirm_password:
            user.password = new_password
        elif new_password and new_password != confirm_password:
            error_message = "Password and confirm password do not match."
            return render_template(
                "management/settings.html",
                user=user,
                sessions=sessions,
                form=form,
                error_message=error_message,
            )

        db.session.commit()

        success_message = "User information updated successfully!"
        return render_template(
            "management/settings.html",
            user=user,
            sessions=sessions,
            form=form,
            success_message=success_message,
        )

    return render_template(
        "management/settings.html",
        user=user,
        sessions=sessions,
        form=form,
    )


@bp.route("/<int:no>/settings", methods=["GET", "POST"])
@login_required
def admin_settings(no):
    if current_user.role != "admin" and current_user.id != no:
        abort(403)

    user = User.query.get(no)
    sessions = Session.query.filter_by(user_id=user.id).all()
    form = SettingsForm()

    if form.validate_on_submit():
        if form.profile_picture.data:
            profile_picture = save_picture(form.profile_picture.data)
            user.profile_picture = profile_picture

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone = form.phone.data
        user.gender = form.gender.data
        user.email = form.email.data

        new_password = form.password.data
        confirm_password = form.confirm_password.data
        if new_password and new_password == confirm_password:
            user.password = new_password
        elif new_password and new_password != confirm_password:
            error_message = "Password and confirm password do not match."
            return render_template(
                "management/settings.html",
                user=user,
                sessions=sessions,
                form=form,
                error_message=error_message,
            )

        db.session.commit()

        success_message = "User information updated successfully!"
        return render_template(
            "management/settings.html",
            user=user,
            sessions=sessions,
            form=form,
            success_message=success_message,
        )

    return render_template(
        "management/settings.html",
        user=user,
        sessions=sessions,
        form=form,
    )


@bp.route("/dashboard")
@login_required
def dashboard():
    user = current_user

    return render_template("management/dashboard.html", username=user.username)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(Config.UPLOAD_FOLDER, picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
