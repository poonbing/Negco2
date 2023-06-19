from flask import render_template, request, redirect, session, url_for
from app.user import bp
from ..models import User
from ..extensions import db


@bp.route("/dashboard")
def dashboard():
    if "username" in session:
        username = session["username"]
        return render_template("dashboard.html", username=username)
    else:
        return redirect(url_for("login.login"))


@bp.route("/settings", methods=["GET", "POST"])
def settings():
    if "username" in session:
        username = session["username"]
        user = User.query.filter_by(username=username).first()

        if request.method == "POST":
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
                        "settings.html",
                        username=username,
                        user=user,
                        error_message=error_message,
                    )

            db.session.commit()

            success_message = "User information updated successfully!"
            return render_template(
                "settings.html",
                username=username,
                user=user,
                success_message=success_message,
            )
        else:
            return render_template("settings.html", user=user)
    else:
        return redirect(url_for("login.login"))
