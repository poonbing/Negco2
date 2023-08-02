# Python Modules
from flask import redirect, url_for, render_template, request, flash
from flask_login import current_user


# Local Modules
from app.recovery import bp
from .utils import access_codes, generate_access_code, send_recovery_email
from ..models import User
from ..extensions import db
from ..forms import ForgotPasswordForm, AccessCodeForm, ResetPasswordForm


@bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if user:
            access_code = generate_access_code()
            access_codes[email] = access_code

            send_recovery_email(email, access_code)

            return redirect(url_for("recovery.enter_access_code", email=email))
        else:
            flash("Invalid email address.", "error")

    return render_template("recovery/forgotPassword.html", form=form)


@bp.route("/enter_access_code", methods=["GET", "POST"])
def enter_access_code():
    email = request.args.get("email")
    if not email or email not in access_codes:
        return redirect(url_for("recovery.forgot_password"))

    form = AccessCodeForm()

    if form.validate_on_submit():
        entered_code = form.access_code.data
        correct_code = access_codes[email]
        if entered_code == correct_code:
            del access_codes[email]
            user = User.query.filter_by(email=email).first()
            token = user.get_reset_token()
            return redirect(url_for("recovery.reset_password", token=token))
        else:
            flash("Invalid access code.", "error")

    return render_template("recovery/accessCode.html", email=email, form=form)


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("management.dashboard"))

    user = User.verify_reset_token(token)

    if user is None:
        flash("That is an invalid or expired token", "error")
        return redirect(url_for("recovery.forgot_password"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        new_password = request.form.get("password")
        user.password = new_password
        db.session.commit()
        return redirect(url_for("auth.login"))

    return render_template("recovery/resetPassword.html", form=form)
