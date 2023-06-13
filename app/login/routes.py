from flask import render_template, request, redirect, session, url_for
from app.login import bp

users = {
    "admin": {
        "username": "admin",
        "password": "admin123",
        "role": "admin",
        "email": "admin@example.com",
        "gender": "male",
        "first_name": "you",
        "phone": "99999999",
        "last_name": "shen",
        "age": 18,
    },
    "user1": {
        "username": "user1",
        "password": "user123",
        "role": "user",
        "email": "user1@example.com",
        "gender": "female",
        "first_name": "Ocean",
        "last_name": "Man",
        "age": 18,
    },
    "user2": {
        "username": "user2",
        "password": "user234",
        "role": "user",
        "email": "user2@example.com",
        "gender": "male",
        "first_name": "Jon",
        "last_name": "Lim",
        "age": 18,
    },
}


@bp.route("/login", methods=["GET", "POST"])
def login(xcaptcha):
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username]["password"] == password:
            if not xcaptcha.verify():
                error = "xCaptcha verification failed. Please try again."
                return render_template("login.html", error=error)
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password."
            return render_template("login.html", error=error)

    return render_template("login.html")
