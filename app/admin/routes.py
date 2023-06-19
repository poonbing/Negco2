from flask import redirect, session, url_for, render_template
from app.admin import bp
from ..models import User


@bp.route("/show_users", methods=["GET"])
def show_users():
    if "username" in session:
        username = session["username"]
        user = User.query.filter_by(username=username).first()
        print(user)
        if user.role == "admin":
            all_users = User.query.all()
            return render_template("admin/users.html", users=all_users)
        else:
            return redirect(url_for("user.dashboard"))
    else:
        return redirect(url_for("login.login"))
