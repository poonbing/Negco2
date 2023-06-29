import os
from flask import render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from ..models import User
from config import Config
from app.user import bp
from PIL import Image
import secrets

from ..extensions import db


@bp.route("/settings", methods=["GET", "POST"])
def settings():
    if "username" in session:
        username = session["username"]
        user = User.query.filter_by(username=username).first()

        if request.method == "POST":
            if request.files.get("profile_picture"):
                profile_picture = save_picture(request.files["profile_picture"])
                user.profile_picture = profile_picture

            if request.form.get("first_name"):
                user.first_name = request.form.get("first_name")
            if request.form.get("last_name"):
                user.last_name = request.form.get("last_name")
            if request.form.get("phone"):
                user.phone = request.form.get("phone")
            if request.form.get("gender"):
                user.gender = request.form.get("gender")
            if request.form.get("email"):
                user.email = request.form.get("email")
            if request.form.get("password"):
                new_password = request.form.get("password")
                confirm_password = request.form.get("confirm_password")
                if new_password == confirm_password:
                    user.password = new_password
                else:
                    error_message = "Password and confirm password do not match."
                    return render_template(
                        "user/settings.html",
                        username=username,
                        user=user,
                        error_message=error_message,
                    )

            db.session.commit()

            success_message = "User information updated successfully!"
            return render_template(
                "user/settings.html",
                username=username,
                user=user,
                success_message=success_message,
            )
        else:
            return render_template("user/settings.html", user=user)
    else:
        return redirect(url_for("login.login"))


@bp.route("/dashboard")
def dashboard():
    if "username" in session:
        username = session["username"]
        return render_template("user/dashboard.html", username=username)
    else:
        return redirect(url_for("login.login"))


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
