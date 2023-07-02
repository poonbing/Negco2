from flask import redirect, session, url_for, render_template, request
from flask_login import login_required, current_user
from app.admin import bp
from ..models import User, LockedUser
from ..extensions import db


@bp.route("/show_users", methods=["GET"])
@login_required
def show_users():
    if current_user.role == "admin":
        all_users = User.query.all()
        return render_template("admin/users.html", users=all_users)
    else:
        return redirect(url_for("user.dashboard"))


@bp.route("/locked-accounts", methods=["GET", "POST"])
@login_required
def locked_accounts():
    if current_user.role != "admin":
        return redirect(url_for("user.dashboard"))

    if request.method == "POST":
        locked_account_ids = request.form.getlist("unlock_account")
        for account_id in locked_account_ids:
            user = User.query.get(account_id)
            if user:
                user.unlock_account()

        return redirect(url_for("admin.locked_accounts"))

    locked_accounts = db.session.query(User).join(LockedUser).all()

    return render_template(
        "admin/locked_accounts.html", locked_accounts=locked_accounts
    )
