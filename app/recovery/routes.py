# Python Modules
from flask import redirect, url_for, render_template, request, flash, current_app
from flask_login import current_user, login_required
from app import limiter
from datetime import datetime

# Local Modules
from app.recovery import bp
from .utils import access_codes, generate_access_code, send_recovery_email
from ..models import User
from ..extensions import db
from ..forms import ForgotPasswordForm, AccessCodeForm, ResetPasswordForm
import bleach


@bp.route("/forgot_password", methods=["GET", "POST"])
@limiter.limit("50 per hour")
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        email = bleach.clean(form.email.data)
        user = User.query.filter_by(email=email).first()

        if user:
            access_code, expiration_time = generate_access_code()
            access_codes[email] = (access_code, expiration_time)

            send_recovery_email(email, access_code)
            current_app.logger.info(
                f"Recovery Email Sent: {email}",
                extra={
                    "user_id": user.id,
                    "address": request.remote_addr,
                    "page": request.path,
                    "category": "Password Recovery",
                },
            )
            return redirect(url_for("recovery.enter_access_code", email=email))
        else:
            flash("Invalid email address.", "error")

    return render_template("recovery/forgotPassword.html", form=form)


@bp.route("/enter_access_code", methods=["GET", "POST"])
@limiter.limit("50 per hour")
def enter_access_code():
    email = request.args.get("email")
    if not email or email not in access_codes:
        return redirect(url_for("recovery.forgot_password"))

    form = AccessCodeForm()

    if form.validate_on_submit():
        entered_code = form.access_code.data
        user_question_one = form.question_one.data
        user_question_two = form.question_two.data
        access_code_info = access_codes.get(email)
        if access_code_info:
            correct_code, expiration_time = access_code_info
            if datetime.now() <= expiration_time and entered_code == correct_code:
                del access_codes[email]
                user = User.query.filter_by(email=email).first()
                if (
                    user.question_one == user_question_one
                    and user.question_two == user_question_two
                ):
                    token = user.get_reset_token()
                    return redirect(url_for("recovery.reset_password", token=token))

            else:
                flash("Invalid or expired access code.", "error")
        else:
            flash("Invalid access code.", "error")

    return render_template("recovery/accessCode.html", email=email, form=form)


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
@limiter.limit("50 per hour")
def reset_password(token):
    user_id = User.verify_reset_token(token)
    user = User.query.get(user_id)

    if user is None:
        flash("That is an invalid or expired token", "error")
        return redirect(url_for("recovery.forgot_password"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        new_password = bleach.clean(form.password.data)
        user.password = user.hash_password(new_password)
        db.session.commit()
        current_app.logger.info(
            f"Password Resetted: {user.id}",
            extra={
                "user_id": user.id,
                "address": request.remote_addr,
                "page": request.path,
                "category": "Password Recovery",
            },
        )
        return redirect(url_for("auth.login"))

    return render_template("recovery/resetPassword.html", form=form)
