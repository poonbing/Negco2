# Python Modules
from flask import redirect, render_template, request, url_for, abort, flash
from flask_login import current_user, login_required


# Local Modules
from app.management import bp
from .utils import admin_required, save_picture
from ..models import User, LockedUser, Session
from ..extensions import db
from ..forms import SettingsForm
from ..models import User


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
            flash("Password and confirm password do not match.", "error")
            return render_template(
                "management/settings.html",
                user=user,
                sessions=sessions,
                form=form,
            )

        db.session.commit()

        flash("User information updated successfully!", "success")
        return render_template(
            "management/settings.html",
            user=user,
            sessions=sessions,
            form=form,
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
            flash("Password and confirm password do not match.", "error")
            return render_template(
                "management/settings.html",
                user=user,
                sessions=sessions,
                form=form,
            )

        db.session.commit()

        flash("User information updated successfully!", "success")
        return render_template(
            "management/settings.html",
            user=user,
            sessions=sessions,
            form=form,
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
