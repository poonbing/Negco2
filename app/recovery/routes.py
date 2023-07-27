# Python Modules
from flask import redirect, url_for, render_template, request, flash
from flask_mail import Message
from random import randint


# Local Modules
from app.recovery import bp
from ..models import User
from ..extensions import db, mail

access_codes = {}


def generate_access_code():
    return str(randint(100000, 999999))


def send_recovery_email(email, access_code):
    msg = Message("Password Recovery", recipients=[email])
    msg.html = render_template("recovery/emailTemplate.html", access_code=access_code)
    mail.send(msg)


@bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()

        if user:
            access_code = generate_access_code()
            access_codes[email] = access_code

            send_recovery_email(email, access_code)

            return redirect(url_for("recovery.enter_access_code", email=email))
        else:
            flash("Invalid email address.", "error")

    return render_template("recovery/forgotPassword.html")


@bp.route("/enter_access_code", methods=["GET", "POST"])
def enter_access_code():
    email = request.args.get("email")
    if not email or email not in access_codes:
        return redirect(url_for("recovery.forgot_password"))

    if request.method == "POST":
        entered_code = request.form.get("access_code")
        correct_code = access_codes[email]
        if entered_code == correct_code:
            del access_codes[email]
            return redirect(url_for("recovery.reset_password", email=email))
        else:
            flash("Invalid access code.", "error")

    return render_template("recovery/accessCode.html", email=email)


@bp.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    email = request.args.get("email")
    if not email:
        return redirect(url_for("recovery.forgot_password"))

    user = User.query.filter_by(email=email).first()
    if not user:
        return redirect(url_for("recovery.forgot_password"))

    if request.method == "POST":
        new_password = request.form.get("password")
        user.password = new_password
        db.session.commit()
        return redirect(url_for("auth.login"))

    return render_template("recovery/resetPassword.html", email=email)
