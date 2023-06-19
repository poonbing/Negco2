from config import Config
from flask_xcaptcha import XCaptcha
from flask import Flask, render_template, request, redirect, url_for, session
from random import randint
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    xcaptcha = XCaptcha(app=app)
    db.init_app(app)

    # Mock user data for demonstration purposes
    class User(db.Model):
        __tablename__ = "users"

        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), unique=True)
        password = db.Column(db.String(50))
        role = db.Column(db.String(20))
        email = db.Column(db.String(100), unique=True)
        gender = db.Column(db.String(10))
        first_name = db.Column(db.String(50))
        last_name = db.Column(db.String(50))
        age = db.Column(db.Integer)
        phone = db.Column(db.String(15))

    with app.app_context():
        db.create_all()

    access_codes = {}

    # Generate a random 6-digit access code
    def generate_access_code():
        return str(randint(100000, 999999))

    # from app.login import bp as login_bp

    # app.register_blueprint(login_bp)

    # from app.signup import bp as signup_bp

    # app.register_blueprint(signup_bp)

    # from app.settings import bp as settings_bp

    # app.register_blueprint(settings_bp)

    @app.route("/")
    def home():
        if "username" in session:
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                if not xcaptcha.verify():
                    error = "xCaptcha verification failed. Please try again."
                    return render_template("login.html", error=error)
                session["username"] = username
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid username or password."
                return render_template("login.html", error=error)

        return render_template("login.html")

    @app.route("/dashboard")
    def dashboard():
        if "username" in session:
            username = session["username"]
            return render_template("dashboard.html", username=username)
        else:
            return redirect(url_for("login"))

    @app.route("/logout")
    def logout():
        session.pop("username", None)
        return redirect(url_for("login"))

    @app.route("/settings", methods=["GET", "POST"])
    def settings():
        if "username" in session:
            username = session["username"]
            user = User.query.filter_by(username=username).first()

            if request.method == "POST":
                if request.form.get("first_name"):
                    user.first_name = request.form.get("first_name")
                if request.form.get("last_name"):
                    user.last_name = request.form.get("last_name")
                if request.form.get("phone"):
                    user.phone = request.form.get("phone")
                if request.form.get("gender"):
                    user.gender = request.form.get("gender")
                if request.form.get("email"):
                    user.email = request.form.get("email")
                if request.form.get("password"):
                    new_password = request.form.get("password")
                    confirm_password = request.form.get("confirm_password")
                    if new_password == confirm_password:
                        user.password = new_password
                    else:
                        error_message = "Password and confirm password do not match."
                        return render_template(
                            "settings.html",
                            username=username,
                            user=user,
                            error_message=error_message,
                        )

                db.session.commit()

                success_message = "User information updated successfully!"
                return render_template(
                    "settings.html",
                    username=username,
                    user=user,
                    success_message=success_message,
                )
            else:
                return render_template("settings.html", user=user)
        else:
            return redirect(url_for("login"))

    @app.route("/forgot_password", methods=["GET", "POST"])
    def forgot_password():
        if request.method == "POST":
            email = request.form.get("email")
            if email == "admin@example.com":
                # Generate and store the access code
                access_code = generate_access_code()
                print(access_code)
                access_codes[email] = access_code

                return redirect(url_for("enter_access_code", email=email))
            else:
                error = "Invalid email address."
                return render_template("forgot_password.html", error=error)

        return render_template("forgot_password.html")

    # @app.route("/enter_access_code", methods=["GET", "POST"])
    # def enter_access_code():
    #     email = request.args.get("email")
    #     print(email)
    #     if not email or email not in access_codes:
    #         return redirect(url_for("forgot_password"))

    #     if request.method == "POST":
    #         entered_code = request.form.get("access_code")
    #         correct_code = access_codes[email]
    #         if entered_code == correct_code:
    #             # Remove the access code from the dictionary
    #             del access_codes[email]
    #             return redirect(url_for("success", email=email))
    #         else:
    #             error = "Invalid access code."
    #             return render_template("enter_access_code.html", error=error)

    #     return render_template("enter_access_code.html", email=email)

    # @app.route("/success", methods=["GET", "POST"])
    # def success():
    #     return render_template("success.html")

    # @app.route("/reset_password", methods=["GET", "POST"])
    # def reset_password():
    #     email = request.args.get("email")
    #     if not email or email not in users:
    #         return redirect(url_for("forgot_password"))

    #     if request.method == "POST":
    #         new_password = request.form.get("password")
    #         # Update the user's password in the database or user data dictionary
    #         users[email]["password"] = new_password
    #         return redirect(url_for("login"))

    #     return render_template("reset_password.html")

    @app.route("/users", methods=["GET"])
    def show_users():
        if "username" in session:
            username = session["username"]
            user = User.query.filter_by(username=username).first()

            if user.role == "admin":
                all_users = User.query.all()
                return render_template("users.html", users=all_users)
            else:
                return redirect(url_for("dashboard"))
        else:
            return redirect(url_for("login"))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app