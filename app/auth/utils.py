from flask import redirect, url_for
from flask_login import current_user
from functools import wraps


def not_logged_in_required(view_func):
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for("management.dashboard"))
        return view_func(*args, **kwargs)

    return decorated_function
