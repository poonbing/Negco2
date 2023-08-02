# Python Modules
from flask import redirect, render_template, request, url_for, abort, flash, send_file
from flask_login import current_user, login_required
from io import BytesIO

# Local Modules
from app.management import bp
from .utils import role_required
from ..models import User, LockedUser, Session
from ..extensions import db
from ..forms import SettingsForm
from ..models import User


@bp.route("/profile_picture")
@login_required
def profile_picture():
    return send_file(BytesIO(current_user.profile_picture), mimetype="image/jpeg")


@bp.route("/show_users", methods=["GET"])
@login_required
@role_required("admin")
def show_users():
    all_users = User.query.all()
    return render_template("management/users.html", users=all_users)


@bp.route("/locked-accounts", methods=["GET", "POST"])
@login_required
@role_required("admin")
def locked_accounts():
    if request.method == "POST":
        locked_account_ids = request.form.getlist("unlock_account")
        for account_id in locked_account_ids:
            user = User.query.filter_by(id=account_id).first()

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
    form = SettingsForm()
    sessions = Session.query.filter_by(user_id=user.id).all()

    if form.validate_on_submit():
        if form.profile_picture.data:
            user.profile_picture = form.profile_picture.data.read()

        if form.first_name.data:
            user.first_name = form.first_name.data

        if form.last_name.data:
            user.last_name = form.last_name.data

        if form.phone.data:
            user.phone = form.phone.data

        if form.gender.data:
            user.gender = form.gender.data

        if form.email.data:
            user.email = form.email.data

        if form.password.data:
            user.password = user.hash_password(form.password.data)

        db.session.commit()

    return render_template(
        "management/settings.html",
        user=user,
        sessions=sessions,
        form=form,
    )


@bp.route("/<int:user_id>/settings", methods=["GET", "POST"])
@login_required
@role_required("admin")
def admin_settings(user_id):
    user = User.query.filter_by(id=user_id).first()
    form = SettingsForm()
    sessions = Session.query.filter_by(user_id=user.id).all()

    if form.validate_on_submit():
        if form.profile_picture.data:
            user.profile_picture = form.profile_picture.data.read()

        if form.first_name.data:
            user.first_name = form.first_name.data

        if form.last_name.data:
            user.last_name = form.last_name.data

        if form.phone.data:
            user.phone = form.phone.data

        if form.gender.data:
            user.gender = form.gender.data

        if form.email.data:
            user.email = form.email.data

        if form.password.data:
            user.password = user.hash_password(form.password.data)

        db.session.commit()

    return render_template(
        "management/admin_settings.html",
        user=user,
        sessions=sessions,
        form=form,
    )


@bp.route("/dashboard")
@login_required
def dashboard():
    user = current_user
    return render_template("management/dashboard.html", user=user)
