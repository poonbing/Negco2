# Python Modules
from flask import (
    redirect,
    render_template,
    request,
    url_for,
    flash,
    jsonify,
    send_file,
    session,
)
from flask_login import current_user, login_required
from io import BytesIO


# Local Modules
from app import limiter
from app.management import bp
from .utils import role_required, compress_and_resize, generate_api_key
from ..models import User, LockedUser, Session, APIKey
from ..extensions import db
from ..forms import SettingsForm, UnlockAccountForm, GenerateApiKeyForm
from ..models import User
from app import limiter
from config import Config


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
    return render_template("management/users.html")


@bp.route("/get_users_data", methods=["GET"])
@login_required
@role_required("admin")
@limiter.limit("4/second")
def get_users_data():
    all_users = User.query.all()
    user_data = []

    for user in all_users:
        user_data.append(
            {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "email": user.email,
            }
        )

    return jsonify(user_data)


@bp.route("/locked-accounts", methods=["GET", "POST"])
@login_required
@role_required("admin")
@limiter.limit("4/second")
def locked_accounts():
    locked_accounts = User.query.join(LockedUser).all()

    form = UnlockAccountForm()
    if form.validate_on_submit():
        selected_accounts = [
            account.id for account in locked_accounts if form.unlock_account.data
        ]
        for account_id in selected_accounts:
            user = User.query.get(account_id)
            if user:
                user.unlock_account()

        return redirect(url_for("management.locked_accounts"))

    return render_template(
        "management/lockedAccounts.html", locked_accounts=locked_accounts, form=form
    )


@bp.route("/delete/<string:user_id>")
@limiter.limit("2/second")
def delete_user(user_id):
    user_to_delete = User.query.get_or_404(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash("User deleted succesfully!", "success")
    return redirect(url_for("management.show_users"))


@bp.route("/settings/api", methods=["GET", "POST"])
@login_required
@limiter.limit("4/second")
def api_settings():
    form = GenerateApiKeyForm()
    if form.validate_on_submit():
        api_key = APIKey(current_user.id, Config.ENCRYPTION_KEY)
        db.session.add(api_key)
        db.session.commit()

    api_keys = APIKey.query.filter_by(user_id=current_user.id).all()

    return render_template("management/api_settings.html", api_keys=api_keys, form=form)


@bp.route("/")
@bp.route("/settings/general", methods=["GET", "POST"])
@login_required
@limiter.limit("4/second")
def settings():
    user = current_user
    form = SettingsForm()
    sessions = Session.query.filter_by(user_id=user.id).all()

    if form.validate_on_submit():
        if form.profile_picture.data:
            user.profile_picture = compress_and_resize(form.profile_picture.data.read())

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone = form.phone.data
        user.gender = form.gender.data
        user.email = form.email.data
        if form.password.data:
            if form.password.data != form.confirm_password.data:
                flash("Password and Confirm Password must be the same", "error")
            else:
                user.password = user.hash_password(form.password.data)

        db.session.commit()
        flash("Setting Information changes successful", "success")

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
            user.profile_picture = compress_and_resize(form.profile_picture.data.read())

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone = form.phone.data
        user.gender = form.gender.data
        user.email = form.email.data
        if form.password.data:
            if form.password.data != form.confirm_password.data:
                flash("Password and Confirm Password must be the same", "error")
            else:
                user.password = user.hash_password(form.password.data)

        db.session.commit()
        flash("Setting Information changes successful", "success")

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
