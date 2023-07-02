import os
from flask import render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from ..models import User
from config import Config
from app.user import bp
from PIL import Image
import secrets
from ..forms import SettingsForm
from flask_login import login_required, current_user  # Import current_user

from ..extensions import db, login_manager


@bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    user = current_user

    form = SettingsForm()
    if request.method == "POST":
        print("reached here")
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
                "user/settings.html",
                username=user.username,
                user=user,
                form=form,
                error_message=error_message,
            )

        db.session.commit()

        success_message = "User information updated successfully!"
        return render_template(
            "user/settings.html",
            username=user.username,
            user=user,
            form=form,
            success_message=success_message,
        )

    return render_template(
        "user/settings.html",
        username=user.username,
        user=user,
        form=form,
    )


@bp.route("/dashboard")
@login_required
def dashboard():
    user = current_user

    return render_template("user/dashboard.html", username=user.username)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(Config.UPLOAD_FOLDER, picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_path
