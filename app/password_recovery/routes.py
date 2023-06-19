from flask import redirect, session, url_for, render_template, request
from app.password_recovery import bp
from ..models import User
from random import randint
from ..extensions import db

access_codes = {}


# Generate a random 6-digit access code
def generate_access_code():
    return str(randint(100000, 999999))


@bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        if email == "admin@example.com":
            # Generate and store the access code
            access_code = generate_access_code()
            print(access_code)
            access_codes[email] = access_code

            return redirect(url_for("password_recovery.enter_access_code", email=email))
        else:
            error = "Invalid email address."
            return render_template("password/forgot_password.html", error=error)

    return render_template("password/forgot_password.html")


@bp.route("/enter_access_code", methods=["GET", "POST"])
def enter_access_code():
    email = request.args.get("email")
    print(email)
    if not email or email not in access_codes:
        return redirect(url_for("password_recovery.forgot_password"))

    if request.method == "POST":
        entered_code = request.form.get("access_code")
        correct_code = access_codes[email]
        if entered_code == correct_code:
            # Remove the access code from the dictionary
            del access_codes[email]
            return redirect(url_for("password_recovery.success", email=email))
        else:
            error = "Invalid access code."
            return render_template("password/enter_access_code.html", error=error)

    return render_template("password/enter_access_code.html", email=email)


@bp.route("/success", methods=["GET", "POST"])
def success():
    return render_template("password/success.html")


@bp.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    email = request.args.get("email")
    if not email:
        return redirect(url_for("password_recovery.forgot_password"))

    user = User.query.filter_by(email=email).first()
    if not user:
        return redirect(url_for("password_recovery.forgot_password"))

    if request.method == "POST":
        new_password = request.form.get("password")
        # Update the user's password in the database
        user.password = new_password
        db.session.commit()
        return redirect(url_for("login.login"))

    return render_template("password/reset_password.html")
