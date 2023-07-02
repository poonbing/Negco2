from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.admin import bp
from ..models import User, LockedUser
from functools import wraps


def admin_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            return redirect(url_for("user.dashboard"))
        return view_func(*args, **kwargs)

    return decorated_view


@bp.route("/show_users", methods=["GET"])
@login_required
@admin_required
def show_users():
    all_users = User.query.all()
    return render_template("admin/users.html", users=all_users)


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

        return redirect(url_for("admin.locked_accounts"))

    locked_accounts = User.query.join(LockedUser).all()

    return render_template(
        "admin/locked_accounts.html", locked_accounts=locked_accounts
    )
