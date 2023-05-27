from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock user data for demonstration purposes
users = {"admin": "admin", "youshen": "youshen123"}


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            return redirect(url_for("dashboard", username=username))
        else:
            error = "Invalid username or password."
            return render_template("login.html", error=error)

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    username = request.args.get("username")
    if username:
        return render_template("home.html", username=username)
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
