from flask import Flask, session, redirect, url_for, render_template, request, url_for
import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

from helpers import *

conn = sqlite3.connect("db.sqlite3", check_same_thread=False)
c = conn.cursor()

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"

BASE_URL = "http://0.0.0.0:1234/url/"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        if not request.form.get("url"):
            "please fill out all required fields"

        auto_code = random_str()

        codes = c.execute("SELECT * FROM urls WHERE auto_code=:auto_code OR code=:auto_code", {"auto_code" : auto_code}).fetchall()

        while len(codes) != 0:
            auto_code = random_str()

            codes = c.execute("SELECT * FROM urls WHERE auto_code=:auto_code OR code=:auto_code", {"auto_code" : auto_code}).fetchall()

        import time
        from datetime import date

        # get today's date
        today = date.today()

        # mm/dd/yyyy
        date = today.strftime("%m/%d/%y")

        # pure timestamp
        ts = time.gmtime()

        # readable timestamp
        timestamp = time.strftime("%x %X", ts)

        c.execute("INSERT INTO urls (original_url, auto_code, code, date, timestamp, user_id) VALUES (:o_url, :code, :code, :date, :time, :u_id)", {"o_url": request.form.get("url"), "code": auto_code, "date": date, "time": timestamp, "u_id": session.get("user_id")})

        conn.commit()

        # is user logged in
        if session.get("user_id"):
            return render_template("confirm.html", BASE_URL=BASE_URL, code=auto_code, original_url=request.form.get("url"))
        return render_template("success.html", BASE_URL=BASE_URL, auto_code=auto_code, old=request.form.get("url"))

    else:
        return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if the form is valid

            if not request.form.get("email") or not request.form.get("password") or not request.form.get("confirmation"):
                return "please fill out all fields"

            if request.form.get("password") != request.form.get("confirmation"):
                return "password confirmation doesn't match password"

            # check if email exist in the database
            exist = c.execute("SELECT * FROM users WHERE email=:email", {"email": request.form.get("email")}).fetchall()

            if len(exist) != 0:
                return "user already registered"

            # hash the password
            pwhash = generate_password_hash(request.form.get("password"), method="pbkdf2:sha256", salt_length=8)

            # insert the row
            c.execute("INSERT INTO users (email, password) VALUES (:email, :password)", {"email": request.form.get("email"), "password": pwhash})
            conn.commit()

            # return success
            return "registered successfully!"
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        # check the form is valid
        if not request.form.get("email") or not request.form.get("password"):
            return "please fill out all required fields"

        # check if email exist in the database
        user = c.execute("SELECT * FROM users WHERE email=:email", {"email": request.form.get("email")}).fetchall()

        if len(user) != 1:
            return "you didn't register"

        # check the password is same to password hash
        pwhash = user[0][2]
        if check_password_hash(pwhash, request.form.get("password")) == False:
            return "wrong password"

        # login the user using session
        session["user_id"] = user[0][0]

        # return success
        return redirect("/dashboard")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/url/<string:code>")
def url(code):

    result = c.execute("SELECT original_url FROM urls WHERE code=:code", {"code": code}).fetchall()

    if len(result) != 1:
        return "404"

    return redirect(result[0][0])


@app.route("/update", methods=["POST"])
@login_required
def update():

    if not request.form.get("new"):
        return "please fill out ALL required fields"

    if not request.form.get("new").isalnum():
        return "You must provide ONLY alpha numeric value"

    codes = c.execute("SELECT * FROM urls WHERE auto_code != :new AND code=:new", {"new": request.form.get("new")}).fetchall()

    if len(codes) != 0:
        return "code already exists"

    c.execute("UPDATE urls SET code=:new WHERE auto_code=:code", {"new": request.form.get("new"), "code": request.form.get("code")})
    conn.commit()

    return redirect("/dashboard")

@app.route("/dashboard")
@login_required
def dashboard():
    urls = c.execute("SELECT * FROM urls WHERE user_id=:u_id", {"u_id": session.get("user_id")}).fetchall()
    print(urls)
    return render_template("dashboard.html", BASE_URL=BASE_URL, urls=urls)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234, debug=True)