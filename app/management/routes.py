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
import pyotp
import hashlib

# Local Modules
from app import limiter
from app.management import bp
from .utils import role_required, compress_and_resize, check_image_format
from ..models import User, LockedUser, Session, APIKey, Log
from ..extensions import db
from ..forms import (
    SettingsForm,
    UnlockAccountForm,
    GenerateApiKeyForm,
    QuestionForm,
    MFAForm,
)
from ..models import User
from app import limiter
from config import Config
import bleach
from datetime import date, timedelta


@bp.route("/profile_picture")
@login_required
@limiter.limit("4/second")
def profile_picture():
    user = current_user
    profile_picture_bytes = user.profile_picture

    image_format = check_image_format(profile_picture_bytes)

    if image_format == "JPG":
        mimetype = "image/jpeg"
    elif image_format == "PNG":
        mimetype = "image/png"
    else:
        return "Invalid image format"

    return send_file(BytesIO(profile_picture_bytes), mimetype=mimetype)


@bp.route("/show_logs", methods=["GET", "POST"])
@login_required
@role_required("admin")
@limiter.limit("4/second")
def logs_settings():
    return render_template("management/logs.html")


@bp.route("/get_logs_data", methods=["GET"])
@login_required
@role_required("admin")
@limiter.limit("4/second")
def get_logs_data():
    all_logs = Log.query.all()
    logs_data = []

    for log in all_logs:
        logs_data.append(
            {
                "id": log.id,
                "timestamp": log.timestamp,
                "source": log.source,
                "logged user": log.logged_user,
                "address": log.address,
                "category": log.category,
                "log text": log.text,
            }
        )

    return jsonify(logs_data)


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


@bp.route("/deletekey/<string:api_key>")
@login_required
@limiter.limit("2/second")
def delete_api_key(api_key):
    api_keys = APIKey.query.filter_by(user_id=current_user.id).all()
    decrypted_key_info = []

    for api_key_obj in api_keys:
        decrypted_key = api_key_obj.decrypt_key(Config.ENCRYPTION_KEY)
        decrypted_key_info.append((api_key_obj, decrypted_key))

    for api_key_obj, decrypted_key in decrypted_key_info:
        if decrypted_key == api_key:
            db.session.delete(api_key_obj)
            db.session.commit()
            flash("API Key deleted successfully!", "success")
            break

    return redirect(url_for("management.api_settings"))


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
    decrypted_key_info = []
    for api_key in api_keys:
        if not api_key.has_expired:
            decrypted_key = api_key.decrypt_key(Config.ENCRYPTION_KEY)
            decrypted_key_info.append((decrypted_key, api_key.expiration_time))
        else:
            db.session.delete(api_key)

    db.session.commit()

    return render_template(
        "management/api_settings.html",
        decrypted_key_info=decrypted_key_info,
        form=form,
    )


@bp.route("/settings/security", methods=["GET", "POST"])
@login_required
@limiter.limit("4/second")
def security_settings():
    user = current_user

    form = QuestionForm()
    form1 = MFAForm()
    user = User.query.filter_by(id=user.id).first()
    # decrypted_secret = user.decrypt_secret(Config.ENCRYPTION_KEY)
    if user.secret:
        uri = pyotp.totp.TOTP(user.secret, digest=hashlib.sha256).provisioning_uri(
            name=user.username, issuer_name="NEGCO2"
        )
    else:
        uri = ""
    print(f"URI: {uri}")

    if form1.validate_on_submit():
        if user.is_secret_empty():
            user.secret = pyotp.random_base32()

            db.session.commit()
            flash("MultiFactor Authentication added successfully", "success")

    if form.validate_on_submit():
        if form.question_one.data:
            user.question_one = bleach.clean(form.question_one.data)
        if form.question_two.data:
            user.question_two = bleach.clean(form.question_two.data)
        if form.question_three.data:
            user.question_three = bleach.clean(form.question_three.data)

        db.session.commit()
        flash("Security Setting changes successful", "success")

    return render_template(
        "management/security_settings.html", form=form, form1=form1, uri=uri
    )


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

        user.first_name = bleach.clean(form.first_name.data)
        user.last_name = bleach.clean(form.last_name.data)
        user.phone = bleach.clean(form.phone.data)
        user.gender = bleach.clean(form.gender.data)
        user.email = bleach.clean(form.email.data)
        if form.password.data:
            if form.password.data != form.confirm_password.data:
                flash("Password and Confirm Password must be the same", "error")
            else:
                user.password = user.hash_password(form.password.data)
                user.password_expires = date.today() + timedelta(days=30)

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

        user.first_name = bleach.clean(form.first_name.data)
        user.last_name = bleach.clean(form.last_name.data)
        user.phone = bleach.clean(form.phone.data)
        user.gender = bleach.clean(form.gender.data)
        user.email = bleach.clean(form.email.data)
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
    if user.password_expires == date.today():
        flash("Please reset your password", "error")
        return redirect(url_for("management.settings"))

    return render_template("management/dashboard.html")
