from flask import render_template, request, redirect, url_for
from app.signup import bp
from ..models import User
from ..extensions import db


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        email = request.form.get("email")
        gender = request.form.get("gender")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        age = request.form.get("age")
        phone = request.form.get("phone")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = "Username already exists. Please choose a different username."
            return render_template("signup/signup.html", error=error)

        if password != confirm_password:
            error = "Passwords do not match. Please try again."
            return render_template("signup/signup.html", error=error)

        new_user = User(
            username=username,
            password=password,
            role="user",
            email=email,
            gender=gender,
            first_name=first_name,
            last_name=last_name,
            age=age,
            phone=phone,
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login.login"))

    return render_template("signup/signup.html")
