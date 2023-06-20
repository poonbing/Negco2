import os
from flask import render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from ..models import User
from config import Config
from app.user import bp

from ..extensions import db


@bp.route("/settings", methods=["GET", "POST"])
def settings():
    if "username" in session:
        username = session["username"]
        user = User.query.filter_by(username=username).first()

        if request.method == "POST":
            if request.files.get("profile_picture"):
                profile_picture = request.files["profile_picture"]
                if profile_picture.filename != "":
                    filename = secure_filename(profile_picture.filename)
                    profile_picture.save(
                        profile_picture.save(
                            os.path.join(Config.UPLOAD_FOLDER, filename)
                        )
                    )
                    user.profile_picture = filename

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
