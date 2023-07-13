# Python Modules
from flask import redirect, url_for
from flask_login import current_user
from functools import wraps
from PIL import Image
import secrets
import os

# Loc
from config import Config


def admin_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            return redirect(url_for("management.dashboard"))
        return view_func(*args, **kwargs)

    return decorated_view


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(Config.UPLOAD_FOLDER, picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def update_info(user, form):
    if form.profile_picture.data:
        profile_picture = save_picture(form.profile_picture.data)
        user.profile_picture = profile_picture

    user.first_name = form.first_name.data
    user.last_name = form.last_name.data
    user.phone = form.phone.data
    user.gender = form.gender.data
    user.email = form.email.data


def update_password(user, form):
    new_password = form.password.data
    confirm_password = form.confirm_password.data

    if new_password and new_password == confirm_password:
        user.password = new_password
        return True
    else:
        return False
