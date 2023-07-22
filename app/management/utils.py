# Python Modules
from flask import redirect, url_for
from flask_login import current_user
from functools import wraps


def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(
                required_role
            ):
                return redirect(url_for("management.dashboard"))
            return func(*args, **kwargs)

        return decorated_view

    return decorator


def update_password(user, form):
    new_password = form.password.data
    confirm_password = form.confirm_password.data

    if new_password and new_password == confirm_password:
        user.password = new_password
        return True
    else:
        return False
