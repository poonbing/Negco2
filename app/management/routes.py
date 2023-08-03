# Python Modules
from flask import (
    redirect,
    render_template,
    request,
    url_for,
    abort,
    flash,
    send_file,
    current_app,
)
from flask_login import current_user, login_required
from io import BytesIO

# Local Modules
from app import limiter
from app.management import bp
from .utils import role_required, update_password
from ..models import User, LockedUser, Session
from ..extensions import db
from ..forms import SettingsForm
from ..models import User
from app import limiter


@bp.route("/profile_picture")
@login_required
@limiter.limit("4/second")
def profile_picture():
    user = current_user
    return send_file(BytesIO(user.profile_picture), mimetype="image/jpeg")


@bp.route("/show_users", methods=["GET"])
@login_required
@role_required("admin")
@limiter.limit("4/second")
def show_users():
    all_users = User.query.all()
    return render_template("management/users.html", users=all_users)


@bp.route("/locked-accounts", methods=["GET", "POST"])
@login_required
@role_required("admin")
@limiter.limit("4/second")
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


@bp.route("/delete/<string:user_id>")
@limiter.limit("2/second")
def delete_user(user_id):
    user_to_delete = User.query.get_or_404(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash("User deleted succesfully!")
    return redirect(url_for("management.show_users"))


@bp.route("/settings", methods=["GET", "POST"])
@login_required
@limiter.limit("4/second")
def settings():
    user = current_user
    form = SettingsForm()
    sessions = Session.query.filter_by(user_id=user.id).all()

    if form.validate_on_submit():
        if form.profile_picture.data:
            user.profile_picture = form.profile_picture.data.read()

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone = form.phone.data
        user.gender = form.gender.data
        user.email = form.email.data

        db.session.commit()

    return render_template(
        "management/settings.html",
        user=user,
        sessions=sessions,
        form=form,
    )


@bp.route("/<string:user_id>/settings", methods=["GET", "POST"])
@login_required
@role_required("admin")
@limiter.limit("4/second")
def admin_settings(user_id):
    user = User.query.get(user_id)
    form = SettingsForm()
    sessions = Session.query.filter_by(user_id=user.id).all()

    if form.validate_on_submit():
        if form.profile_picture.data:
            user.profile_picture = form.profile_picture.data.read()

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone = form.phone.data
        user.gender = form.gender.data
        user.email = form.email.data

        db.session.commit()
    return render_template(
        "management/admin_settings.html",
        user=user,
        sessions=sessions,
        form=form,
    )


@bp.route("/dashboard")
@login_required
@limiter.limit("4/second")
def dashboard():
    user = current_user

    return render_template("management/dashboard.html", username=user.username)
